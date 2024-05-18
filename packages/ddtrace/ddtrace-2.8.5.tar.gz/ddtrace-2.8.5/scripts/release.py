from collections import namedtuple
import json
import os
import re
import subprocess
from typing import Any
from typing import Callable
from typing import Optional

from datadog_api_client import ApiClient
from datadog_api_client import Configuration
from datadog_api_client.v1.api.notebooks_api import NotebooksApi
from github import Github
import requests


"""This release notes script is built to create a release notes draft
for release candidates, patches, and minor releases.

Setup:
1. Create a Personal access token (classic), not a fine grained one, on Github:
https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#creating-a-personal-access-token-classic
2. Give the Github token repo, user, audit_log, project permissions. On the next page authorize your token for Datadog SSO.
3. Add `export GH_TOKEN=<github token>` to your `.zhrc` file.

4. Get API key and Application key for staging: https://ddstaging.datadoghq.com/organization-settings/api-keys
5. Add export DD_API_KEY_STAGING=<api_key> and  export DD_APP_KEY_STAGING=<app_key> to your `.zhrc` file.

6. Install pandoc with `brew install pandoc`

Create an activate a virtual environment, and install required packages :
`python -m venv venv && source venv/bin/activate && pip install pygithub requests datadog-api-client reno`


Usage:
The script should be run from the `scripts` directory.

Required:
    BASE - The base branch you are building your release candidate, patch, or minor release off of.
        If this is a rc1, then just specify the branch you'll create after the release is published. e.g. BASE=2.9

Optional:
    RC - Whether or not this is a release candidate. e.g. RC=1 or RC=0
    PATCH - Whether or not this a patch release. e.g. PATCH=1 or PATCH=0
    PRINT - Whether or not the release notes should be printed to CLI or be used to create a Github release. Default is 0 e.g. PRINT=1 or PRINT=0
    NOTEBOOK - Whether or not to create a notebook in staging. Note this only works for RC1s since those are usually what we create notebooks for.
    Default is 1 for RC1s, 0 for everything else e.g. NOTEBOOK=0 or NOTEBOOK=1
    DRY_RUN - When set to "1", this script does not write anything to github. This can be useful for development testing.
Examples:
Generate release notes and staging testing notebook for next release candidate version of 2.11: `BASE=2.11 RC=1 python release.py`

Generate release notes for next patch version of 2.13: `BASE=2.13 PATCH=1 python release.py`

Generate release notes for the 2.15 release: `BASE=2.15 python release.py`
"""  # noqa

MAX_GH_RELEASE_NOTES_LENGTH = 125000
ReleaseParameters = namedtuple("ReleaseParameters", ["branch", "name", "tag", "dd_repo", "rn", "prerelease"])
DEFAULT_BRANCH = "main"
DRY_RUN = os.getenv("DRY_RUN", "0") == "1"
CHANGELOG_FILENAME = "../CHANGELOG.md"


def _ensure_current_checkout():
    subprocess.run("git fetch", shell=True, cwd=os.pardir)


def _decide_next_release_number(base: str, candidate: bool = False) -> int:
    """Return the next number to use as a patch or release candidate version, based on existing tags on the remote"""
    search = r"v%s.0\.?rc((\d+$))" % base if candidate else r"v%s.((\d+))" % base
    tags = dd_repo.get_tags()
    latest_version = 0
    for tag in tags:
        try:
            other_num = int(re.findall(search, tag.name)[0][0])
        except (IndexError, ValueError, TypeError):
            continue
        if other_num > latest_version:
            latest_version = other_num
    return latest_version + 1


def _get_rc_parameters(dd_repo, base: str, rc, patch) -> ReleaseParameters:
    """Build a ReleaseParameters object representing the in-progress release candidate"""
    # patch value should always be 0 if we're doing an RC
    new_rc_version = _decide_next_release_number(base, candidate=True)
    release_branch = DEFAULT_BRANCH if new_rc_version == 1 else base
    rn = clean_release_notes(generate_release_notes(release_branch))
    version_string = "%s.0rc%s" % (base, str(new_rc_version))
    tag_name = "v%s" % version_string
    return ReleaseParameters(release_branch, version_string, tag_name, dd_repo, rn, True)


def _get_patch_parameters(dd_repo, base: str, rc, patch) -> ReleaseParameters:
    """Build a ReleaseParameters object representing the in-progress patch release"""
    name = "%s.%s" % (base, str(_decide_next_release_number(base)))
    release_notes = clean_release_notes(generate_release_notes(base))
    return ReleaseParameters(base, name, "v%s" % name, dd_repo, release_notes, False)


def _get_minor_parameters(dd_repo, base: str, rc, patch) -> ReleaseParameters:
    """Build a ReleaseParameters object representing the in-progress minor release"""
    name = "%s.0" % base

    rn_raw = generate_release_notes(base)
    rn_sections_clean = create_release_notes_sections(rn_raw, base)
    release_notes = ""
    rn_key_order = [
        "Prelude",
        "New Features",
        "Known Issues",
        "Upgrade Notes",
        "Deprecation Notes",
        "Bug Fixes",
        "Other Changes",
    ]
    for key in rn_key_order:
        try:
            release_notes += "### %s\n\n%s" % (key, rn_sections_clean[key])
        except KeyError:
            continue
    return ReleaseParameters(base, name, "v%s" % name, dd_repo, release_notes, False)


def create_release_draft(dd_repo, base, rc, patch):
    _ensure_current_checkout()
    args = (dd_repo, base, rc, patch)
    if rc:
        parameters = _get_rc_parameters(*args)
    elif patch:
        parameters = _get_patch_parameters(*args)
    else:
        parameters = _get_minor_parameters(*args)

    create_draft_release_github(parameters)

    return parameters.name, parameters.rn


def clean_release_notes(rn_raw: str) -> str:
    """removes everything from the given string except for release notes that haven't been released yet"""
    return rn_raw.decode().split("## v")[0].replace("\n## Unreleased\n", "", 1).replace("# Release Notes\n", "", 1)


def generate_release_notes(branch: str) -> str:
    subprocess.check_output(
        "git checkout {branch} && \
            git pull origin {branch}".format(
            branch=branch
        ),
        shell=True,
        cwd=os.pardir,
    )

    rn_raw = subprocess.check_output(
        "reno report --no-show-source | \
            pandoc -f rst -t gfm --wrap=none",
        shell=True,
        cwd=os.pardir,
    )
    return rn_raw


def create_release_notes_sections(rn_raw, branch):
    # get anything in unreleased section in case there were updates since the last RC
    unreleased = clean_release_notes(rn_raw)
    unreleased = break_into_release_sections(unreleased)
    try:
        unreleased_sections = dict(section.split("\n\n-") for section in unreleased)
        for key in unreleased_sections.keys():
            # add back in the "-" bullet point, and remove the extra newline
            unreleased_sections[key] = "-" + unreleased_sections[key][:-2]
    except ValueError:
        unreleased_sections = {}
    relevant_rns = []
    if unreleased_sections:
        relevant_rns.append(unreleased_sections)

    rns = rn_raw.decode().split("## v")
    # grab the sections from the RC(s)
    for rn in rns:
        if rn.startswith("%s.0" % branch):
            # cut out the version section
            sections = break_into_release_sections(rn)
            prelude_section = {}
            # if there is a prelude, we need to grab that separately since it has different syntax
            if sections[0].startswith(" Prelude\n\n"):
                prelude_section[" Prelude"] = sections[0].split("\n\n", 1)[1]
                sections = sections[1:]
            sections_dict = {**dict(section.split("\n\n", 1) for section in sections), **prelude_section}
            relevant_rns.append(sections_dict)
    # join all the sections from different relevant RCs together
    keys = set().union(*relevant_rns)
    rns_dict = {k: "".join(dic.get(k, "") for dic in relevant_rns) for k in keys}
    rn_sections_clean = {}
    for key in rns_dict.keys():
        rn_sections_clean[key.lstrip()] = rns_dict[key]
    return rn_sections_clean


def break_into_release_sections(rn):
    return [ele for ele in re.split(r"[^#](#)\1{2}[^#]", rn)[1:] if ele != "#"]


def create_draft_release_github(release_parameters: ReleaseParameters):
    base_branch = dd_repo.get_branch(branch=release_parameters.branch)
    print_release_notes = bool(os.getenv("PRINT"))
    if print_release_notes:
        print(
            """RELEASE NOTES INFO:\nName:%s\nTag:%s\nprerelease:%s\ntarget_commitish:%s\nmessage:%s
              """
            % (
                release_parameters.name,
                release_parameters.tag,
                release_parameters.prerelease,
                base_branch,
                release_parameters.rn,
            )
        )
    else:
        _dry(
            lambda: dd_repo.create_git_release(
                name=release_parameters.name,
                tag=release_parameters.tag,
                prerelease=release_parameters.prerelease,
                draft=True,
                target_commitish=base_branch,
                message=release_parameters.rn[:MAX_GH_RELEASE_NOTES_LENGTH],
            ),
            f"create_git_release(name={release_parameters.name}, tag={release_parameters.tag}, "
            f"prerelease={release_parameters.prerelease}, draft=True, target_commitish={base_branch}, "
            f"message={release_parameters.rn[:100]}...)",
        )
        print("\nPlease review your release notes draft here: https://github.com/DataDog/dd-trace-py/releases")

    return release_parameters.name, release_parameters.rn


def get_ddtrace_repo():
    gh_token = os.getenv("GH_TOKEN")
    if not gh_token:
        raise ValueError(
            "We need a Github token to generate the release notes. Please follow the instructions in the script."
        )
    return Github(gh_token).get_repo(full_name_or_id="DataDog/dd-trace-py")


def add_release_to_changelog(name: str, release_notes: str):
    separator = "---"
    with open(CHANGELOG_FILENAME, "r") as changelog_file:
        contents = changelog_file.read()
    existing_release_notes_lines = contents.split("\n")
    insert_index = existing_release_notes_lines.index(separator)
    new_notes = ["", separator, "", f"## {name}", ""] + release_notes.split("\n")
    composite = (
        existing_release_notes_lines[: insert_index - 1] + new_notes + existing_release_notes_lines[insert_index:]
    )
    with open(CHANGELOG_FILENAME, "w") as changelog_file:
        changelog_file.write("\n".join(composite))


def commit_and_push(dd_repo, branch_name: str, release_name: str):
    subprocess.check_output(f"git checkout -b {branch_name}", shell=True, cwd=os.pardir)
    subprocess.check_output("git add -A", shell=True, cwd=os.pardir)
    print(f"Committing changes to {CHANGELOG_FILENAME} on branch {branch_name}")
    pr_body = f"update changelog for version {release_name}"
    subprocess.check_output(f"git commit -m '{pr_body} via release script'", shell=True, cwd=os.pardir)
    subprocess.check_output(f"git push origin {branch_name}", shell=True, cwd=os.pardir)
    dd_repo.create_pull(DEFAULT_BRANCH, branch_name, title=f"chore: {pr_body}", body=f"- [x] {pr_body}", draft=False)


def create_changelog_pull_request(dd_repo, name: str, release_notes: str):
    subprocess.check_output(f"git checkout {DEFAULT_BRANCH}", shell=True, cwd=os.pardir)
    add_release_to_changelog(name, release_notes)
    if not DRY_RUN:
        commit_and_push(dd_repo, f"release.script/changelog-update-{name}", name)
    else:
        diff = subprocess.check_output("git diff", shell=True, cwd=os.pardir)
        subprocess.check_output("git stash", shell=True, cwd=os.pardir)
        diff = "\n".join(line.decode() for line in diff.split(b"\n"))
        print(
            f"\nDRY RUN: The following diff would be committed:\n\n{diff}\n\nDRY RUN: These changes have been stashed."
        )


def create_notebook(dd_repo, name, rn, base):
    dd_api_key = os.getenv("DD_API_KEY_STAGING")
    dd_app_key = os.getenv("DD_APP_KEY_STAGING")
    if not dd_api_key or not dd_app_key:
        raise ValueError(
            "We need DD_API_KEY_STAGING and DD_APP_KEY_STAGING values. Please follow the instructions in the script."
        )
    if int(name[-1]) == 1:
        last_version = base[:-1] + str(int(base[-1]) - 1)
    else:
        print(
            "Since this is not the RC1 for this release."
            "Please add the release notes for this release to the notebook."
        )
        return
    commit_hashes = (
        subprocess.check_output(
            'git log {last_version}..{latest_branch} --oneline | cut -d " " -f 1'.format(
                last_version=last_version, latest_branch=DEFAULT_BRANCH
            ),
            shell=True,
            cwd=os.pardir,
        )
        .decode("utf8")
        .strip("\n")
        .split("\n")
    )

    commits = []
    # get the commit objects
    for commit_hash in commit_hashes:
        try:
            commits.append(dd_repo.get_commit(commit_hash))
        except Exception:
            print("Couldn't get commit hash %s for notebook, please add this manually" % commit_hash)

    prs_details = []
    # from each commit:
    # 1. get release note text
    # 2. pull out author and turn into email
    # 3. get PR number and create link
    for commit in commits:
        files = commit.files
        for file in files:
            filename = file.filename
            if filename.startswith("releasenotes/notes/"):
                try:
                    # we need to make another api call to get ContentFile object so we can see what's in there
                    rn_piece = dd_repo.get_contents(filename).decoded_content.decode("utf8")
                except Exception:
                    print(
                        """File contents were not obtained for {file} in commit {commit}."""
                        """It's likely this file was deleted in a PR""".format(file=file, commit=commit)
                    )
                    continue
                try:
                    # removes unwanted new lines, whitespace and characters from rn_file_content
                    rn_piece = re.sub("[-|]", "", rn_piece)
                    rn_piece = re.sub(r"\s+", " ", rn_piece.strip())
                except Exception:
                    print(f"Failed to format release note: {rn_piece}")

                author = commit.author.name
                if author:
                    author = author.split(" ")
                    author_slack = "@" + author[0] + "." + author[-1]
                    author_dd = author_slack + "@datadoghq.com"
                pr_num = re.findall(r"\(#(\d{4})\)", commit.commit.message)[0]
                url = "https://github.com/DataDog/dd-trace-py/pull/{pr_num}".format(pr_num=pr_num)
                prs_details.append(
                    {"author_slack": author_slack, "author_dd": author_dd, "url": url, "rn_piece": rn_piece}
                )

    # Group PRs by release note scope (feature, fix, deprecation, etc)
    # This is not necessary it just makes the notebook easier to read
    prs_details = sorted(prs_details, key=lambda prd: prd["rn_piece"])
    notebook_rns = ""
    for pr_detail in prs_details:
        notebook_rns += f"\n- [ ] {pr_detail['rn_piece']}\n  - PR:{pr_detail['url']},"
        "Tester: {pr_detail['author_dd']}\n  - Findings: "

    # create the review notebook and add the release notes formatted for testing
    # get notebook template
    template_notebook = subprocess.check_output(
        'curl -X GET "https://api.datadoghq.com/api/v1/notebooks/4888117" \
    -H "Accept: application/json" \
    -H "DD-API-KEY: {dd_api_key}" \
    -H "DD-APPLICATION-KEY: {dd_app_key}"'.format(
            dd_api_key=dd_api_key, dd_app_key=dd_app_key
        ),
        shell=True,
        cwd=os.pardir,
    )
    data = template_notebook.decode("utf8")
    data = json.loads(data)
    # change the text inside of our template to include release notes
    data["data"]["attributes"]["cells"][1]["attributes"]["definition"][
        "text"
    ] = f"# Relenv \n - [ ] Relenv is checked: https://ddstaging.datadoghq.com/dashboard/h8c-888-v2e/python-reliability-env-dashboard \n# Release notes to test {notebook_rns}\n## Release Notes that will not be tested\n- <any release notes for PRs that don't need manual testing>\n"  # noqa

    # grab the latest commit id on the latest branch to mark the rc notebook with
    main_branch = dd_repo.get_branch(branch=DEFAULT_BRANCH)
    commit_id = main_branch.commit

    # pull the cells out to be transferred into a new notebook
    cells = data["data"]["attributes"]["cells"]
    nb_name = "ddtrace-py testing %s commit %s" % (name, commit_id.sha)
    interpolated_notebook = {
        "data": {
            "attributes": {
                "cells": cells,
                "name": nb_name,
                "time": {"live_span": "1d"},
            },
            "type": "notebooks",
        }
    }

    notebook_json = json.dumps(interpolated_notebook, indent=4, sort_keys=True)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "DD-API-KEY": dd_api_key,
        "DD-APPLICATION-KEY": dd_app_key,
    }
    # create new release notebook
    _dry(lambda: requests.post("https://api.datadoghq.com/api/v1/notebooks", data=notebook_json, headers=headers))

    configuration = Configuration()
    configuration.api_key["apiKeyAuth"] = dd_api_key
    configuration.api_key["appKeyAuth"] = dd_app_key
    with ApiClient(configuration) as api_client:
        api_instance = NotebooksApi(api_client)
        response = api_instance.list_notebooks(query=nb_name)

    nb_id = response._data_store["data"][0]["id"]
    nb_url = "https://ddstaging.datadoghq.com/notebook/%s" % (nb_id)

    print("\nNotebook created at %s\n" % nb_url)

    # eliminate duplicates of handles for the slack messages
    author_slack_handles = " ".join({pr_detail["author_slack"] for pr_detail in prs_details})
    print("Message to post in #apm-python-release once deployed to staging:\n")
    print(
        """It's time to test the {version} release candidate! The owners of pull requests with release notes in {version} are {author_slack_handles}.
Everyone mentioned here: before the end of the day tomorrow, please ensure that you've filled in the testing strategy in the release notebook {nb_url} on all release notes you're the owner of, according to the expectations here: https://datadoghq.atlassian.net/wiki/spaces/APMPY/pages/2868085694/Staging+testing+expectations+for+dd-trace-py+contributors
You can start doing your tests immediately, using {version}.

Check the release notebook {nb_url} for asynchronous updates on the release process. If you have questions or need help with anything, let me know! I'm here to help. Thanks all for your dedication to maintaining a rock-solid library.""".format(  # noqa
            version=name, author_slack_handles=author_slack_handles, nb_url=nb_url
        )
    )


def _dry(fn: Callable, description: Optional[str] = None) -> Any:
    if DRY_RUN:
        print("Dry run - would call:")
        print(description or fn.__name__)
    else:
        return fn()


if __name__ == "__main__":
    subprocess.check_output(
        "git stash",
        shell=True,
        cwd=os.pardir,
    )
    start_branch = (
        subprocess.check_output(
            "git rev-parse --abbrev-ref HEAD",
            shell=True,
            cwd=os.pardir,
        )
        .decode()
        .strip()
    )

    base = os.getenv("BASE")
    rc = bool(os.getenv("RC"))
    patch = bool(os.getenv("PATCH"))

    if base is None:
        raise ValueError("Need to specify the base version with envar e.g. BASE=2.10")
    if ".x" in base:
        raise ValueError("Base branch must be a fully qualified semantic version.")

    dd_repo = get_ddtrace_repo()
    name, rn = create_release_draft(dd_repo, base, rc, patch)

    if rc:
        if not DRY_RUN and os.getenv("NOTEBOOK", 1):
            print("Creating Notebook")
            create_notebook(dd_repo, name, rn, base)
        else:
            print(
                (
                    "Currently the release script only supports making notebooks for RC1s."
                    "No notebook will be created at this time."
                )
            )
    else:
        create_changelog_pull_request(dd_repo, name, rn)

    # switch back to original git branch
    subprocess.check_output(
        "git checkout {start_branch}".format(start_branch=start_branch),
        shell=True,
        cwd=os.pardir,
    )
    print(
        (
            "\nYou've been switch back to your original branch, if you had uncommitted changes before"
            "running this command, run `git stash pop` to get them back."
        )
    )
