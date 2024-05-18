import base64
import collections
import gzip
import json
import time
from typing import Optional

from ddtrace import constants
from ddtrace._trace._limits import MAX_SPAN_META_VALUE_LEN
from ddtrace.appsec import _processor as appsec_processor
from ddtrace.appsec._asm_request_context import add_context_callback
from ddtrace.appsec._asm_request_context import call_waf_callback
from ddtrace.appsec._asm_request_context import remove_context_callback
from ddtrace.appsec._constants import API_SECURITY
from ddtrace.appsec._constants import SPAN_DATA_NAMES
from ddtrace.internal.logger import get_logger
from ddtrace.internal.service import Service
from ddtrace.settings.asm import config as asm_config


log = get_logger(__name__)
_sentinel = object()


# Max number of endpoint hashes to keep in the hashtable
MAX_HASHTABLE_SIZE = 4096

M_INFINITY = float("-inf")


class TooLargeSchemaException(Exception):
    pass


class APIManager(Service):
    COLLECTED = [
        ("REQUEST_HEADERS_NO_COOKIES", API_SECURITY.REQUEST_HEADERS_NO_COOKIES, dict),
        ("REQUEST_COOKIES", API_SECURITY.REQUEST_COOKIES, dict),
        ("REQUEST_QUERY", API_SECURITY.REQUEST_QUERY, dict),
        ("REQUEST_PATH_PARAMS", API_SECURITY.REQUEST_PATH_PARAMS, dict),
        ("REQUEST_BODY", API_SECURITY.REQUEST_BODY, None),
        ("RESPONSE_HEADERS_NO_COOKIES", API_SECURITY.RESPONSE_HEADERS_NO_COOKIES, dict),
        ("RESPONSE_BODY", API_SECURITY.RESPONSE_BODY, lambda f: f()),
    ]

    _instance: Optional["APIManager"] = None

    @classmethod
    def enable(cls) -> None:
        if cls._instance is not None:
            log.debug("%s already enabled", cls.__name__)
            return

        asm_config._api_security_active = True
        log.debug("Enabling %s", cls.__name__)
        cls._instance = cls()
        cls._instance.start()
        log.debug("%s enabled", cls.__name__)

    @classmethod
    def disable(cls) -> None:
        if cls._instance is None:
            log.debug("%s not enabled", cls.__name__)
            return

        asm_config._api_security_active = False
        log.debug("Disabling %s", cls.__name__)
        cls._instance.stop()
        cls._instance = None
        log.debug("%s disabled", cls.__name__)

    def __init__(self) -> None:
        super(APIManager, self).__init__()

        log.debug("%s initialized", self.__class__.__name__)
        self._hashtable: collections.OrderedDict[int, float] = collections.OrderedDict()

    def _stop_service(self) -> None:
        remove_context_callback(self._schema_callback, global_callback=True)
        self._hashtable.clear()

    def _start_service(self) -> None:
        add_context_callback(self._schema_callback, global_callback=True)

    def _should_collect_schema(self, env, priority: int) -> bool:
        # Rate limit per route
        if priority <= 0:
            return False

        method = env.waf_addresses.get(SPAN_DATA_NAMES.REQUEST_METHOD)
        route = env.waf_addresses.get(SPAN_DATA_NAMES.REQUEST_ROUTE)
        status = env.waf_addresses.get(SPAN_DATA_NAMES.RESPONSE_STATUS)
        # Framework is not fully supported
        if method is None or route is None or status is None:
            log.debug(
                "unsupported groupkey for api security [method %s] [route %s] [status %s]",
                bool(method),
                bool(route),
                bool(status),
            )
            return False
        end_point_hash = hash((route, method, status))
        current_time = time.monotonic()
        previous_time = self._hashtable.get(end_point_hash, M_INFINITY)
        if previous_time >= current_time - asm_config._api_security_sample_delay:
            return False
        if previous_time is M_INFINITY:
            if len(self._hashtable) >= MAX_HASHTABLE_SIZE:
                self._hashtable.popitem(last=False)
        else:
            self._hashtable.move_to_end(end_point_hash)
        self._hashtable[end_point_hash] = current_time
        return True

    def _schema_callback(self, env):
        from ddtrace.appsec._utils import _appsec_apisec_features_is_active

        if env.span is None or not _appsec_apisec_features_is_active():
            return
        root = env.span._local_root or env.span
        if not root or any(meta_name in root._meta for _, meta_name, _ in self.COLLECTED):
            return

        try:
            # check both current span and root span for sampling priority
            # if sampling has not yet run for the span, we default to treating it as sampled
            if root.context.sampling_priority is None and env.span.context.sampling_priority is None:
                priorities = (1,)
            else:
                priorities = (root.context.sampling_priority or 0, env.span.context.sampling_priority or 0)
            # if any of them is set to USER_KEEP or USER_REJECT, we should respect it
            if constants.USER_KEEP in priorities:
                priority = constants.USER_KEEP
            elif constants.USER_REJECT in priorities:
                priority = constants.USER_REJECT
            else:
                priority = max(priorities)
            if not self._should_collect_schema(env, priority):
                return
        except Exception:
            log.warning("Failed to sample request for schema generation", exc_info=True)
            return

        # we need the request content type on the span
        try:
            headers = env.waf_addresses.get(SPAN_DATA_NAMES.REQUEST_HEADERS_NO_COOKIES, _sentinel)
            if headers is not _sentinel:
                appsec_processor._set_headers(root, headers, kind="request")
        except Exception:
            log.debug("Failed to enrich request span with headers", exc_info=True)

        waf_payload = {"PROCESSOR_SETTINGS": {"extract-schema": True}}
        for address, _, transform in self.COLLECTED:
            if not asm_config._api_security_parse_response_body and address == "RESPONSE_BODY":
                continue
            value = env.waf_addresses.get(SPAN_DATA_NAMES[address], _sentinel)
            if value is _sentinel:
                log.debug("no value for %s", address)
                continue
            if transform is not None:
                value = transform(value)
            waf_payload[address] = value

        result = call_waf_callback(waf_payload)
        if result is None:
            return
        for meta, schema in result.derivatives.items():
            b64_gzip_content = b""
            try:
                b64_gzip_content = base64.b64encode(
                    gzip.compress(json.dumps(schema, separators=",:").encode())
                ).decode()
                if len(b64_gzip_content) >= MAX_SPAN_META_VALUE_LEN:
                    raise TooLargeSchemaException
                root._meta[meta] = b64_gzip_content
            except Exception:
                self._log_limiter.limit(
                    log.warning,
                    "Failed to get schema from %r [schema length=%d]:\n%s",
                    address,
                    len(b64_gzip_content),
                    repr(value)[:256],
                    exc_info=True,
                )
