"""The scope check: a pull request from outside may add or change one design
folder, or its author's own showcase entry, and nothing else (ADR-0006,
layer 1; ADR-0016).

  python tools/scope_check.py --pr NUMBER          in the workflow
  python tools/scope_check.py --files LIST.tsv [--author LOGIN]
                                                   locally: one line per
                                                   file, "status<TAB>path",
                                                   or "renamed<TAB>new<TAB>old";
                                                   the author as the event
                                                   would give it

In the workflow, this file runs from the base branch, never from the pull
request: .github/workflows/scope.yml uses the pull_request_target trigger,
checks out the base branch, and never checks out or runs anything from the
pull request. This script reads only the list of changed file names,
through GitHub's API, with a read-only token. A pull request that edits
this script, a workflow or any check changes nothing about how it is
checked here, and fails this check for touching them.

The rules:

  - every changed path, and every old path of a renamed file, lies in one
    designs/<name>/ folder, the same for all;
  - each is a file the design format allows: design.css, design.json,
    fonts/*.woff2, fonts/*.txt, img/*.png, *.webp, *.jpg, *.jpeg;
  - the folder is not one the project maintains: default, plain and the
    owner's other designs (ADR-0013, Changes, 2026-10-24);
  - at most 40 files.

Or, for a showcase entry:

  - every changed path lies in showcase/<login>/, where login is the pull
    request author's GitHub login in lower case, from the event GitHub
    sends, never from anything the pull request contains;
  - each is entry.json or a screenshot named as its tool saved it, ending
    .png, .jpg, .jpeg or .webp in any case, with no folder, no control
    character, not hidden (build.py's SHOWCASE_IMAGE_RE);
  - no design folder in the same pull request.

A pull request opened by the repository's owner, a member or a
collaborator is a maintainer's change: the scope is not limited, the check
says so, and the review covers it. The trust level comes from the event
GitHub sends, not from anything the pull request contains. A maintainer
can still be checked as a contributor would be, to test this check, by
putting the marker [scope: as contributor] in the pull request's
description; the marker can only make the check stricter, so anyone may
use it.

Exit 0 in scope, 1 out of scope, each reason printed for the contributor
(and written to the job summary in the workflow), 2 on a usage or API
error. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

DESIGN_PATH_RE = re.compile(
    r"^designs/(?P<name>[a-z0-9]+(?:-[a-z0-9]+)*)/"
    r"(?:design\.css|design\.json"
    r"|fonts/[A-Za-z0-9][A-Za-z0-9._-]{0,80}\.(?:woff2|txt)"
    r"|img/[A-Za-z0-9][A-Za-z0-9._-]{0,80}\.(?:png|webp|jpg|jpeg))$")
SHOWCASE_PATH_RE = re.compile(
    r"^showcase/(?P<login>[a-z0-9](?:[a-z0-9]|-(?=[a-z0-9])){0,38})/"
    r"(?:entry\.json|(?i:[^/\\.\x00-\x1f\x7f][^/\\\x00-\x1f\x7f]{0,115}\.(?:png|jpe?g|webp)))$")
# The project's own designs, each credited to the owner (ADR-0013,
# Changes, 2026-10-24). A design dropped from designs/ leaves this list too.
MAINTAINED = {"default", "plain", "bento", "broadsheet", "console", "poster", "signal",
              "assert", "latent", "pipeline", "pocket", "sentinel",
              "broadcast", "cyanotype", "frost", "handbook", "savepoint"}
MAINTAINER_ASSOCIATIONS = {"OWNER", "MEMBER", "COLLABORATOR"}
AS_CONTRIBUTOR = "[scope: as contributor]"
FILE_LIMIT = 40
API = "https://api.github.com"


def showcase_problems(changes: list[tuple[str, str, str | None]], author: str | None) -> tuple[list[str], str]:
    """(problems, the folder) for a pull request that touches showcase/."""
    problems, logins = [], set()
    own = (author or "").lower()
    for status, path, old in changes:
        for which in filter(None, (path, old)):
            match = SHOWCASE_PATH_RE.match(which)
            if match:
                logins.add(match["login"])
            elif which.startswith("designs/"):
                problems.append(f"{which}: a design folder beside a showcase entry; one pull "
                                f"request carries one or the other")
            elif which.startswith("showcase/"):
                problems.append(f"{which}: a showcase entry is showcase/<your-login>/entry.json and "
                                f"one screenshot, a .png, .jpg, .jpeg or .webp file, nothing else "
                                f"(docs/how-to/add-to-the-showcase.md)")
            else:
                problems.append(f"{which}: outside showcase/. A showcase pull request changes its "
                                f"author's own entry only (CONTRIBUTING.md)")
    if not own:
        problems.append("the pull request's author is not known, so whose entry this is cannot "
                        "be checked")
    for login in sorted(logins - {own}):
        problems.append(f"showcase/{login}/ is not the author's own entry: yours is "
                        f"showcase/{own}/, named by your GitHub login in lower case")
    return problems, f"showcase/{own}/"


def scope_problems(changes: list[tuple[str, str, str | None]],
                   author: str | None = None) -> tuple[list[str], str | None]:
    """(problems, the folder in scope) for a list of (status, path, old path)."""
    problems, names = [], set()
    if not changes:
        return ["the pull request changes no files"], None
    if len(changes) > FILE_LIMIT:
        problems.append(f"{len(changes)} files; a design has at most {FILE_LIMIT}")
    if any(which.startswith("showcase/") for _, path, old in changes for which in filter(None, (path, old))):
        found, folder = showcase_problems(changes, author)
        return problems + found, folder
    for status, path, old in changes:
        for which in filter(None, (path, old)):
            match = DESIGN_PATH_RE.match(which)
            if not match:
                if which.startswith("designs/"):
                    problems.append(f"{which}: not a file a design may hold. Allowed: design.css, "
                                    f"design.json, fonts/*.woff2 with fonts/*.txt licences, and "
                                    f"img/*.png, *.webp, *.jpg or *.jpeg (docs/how-to/add-a-design.md)")
                else:
                    problems.append(f"{which}: outside designs/. A design pull request changes "
                                    f"one design folder only; to change anything else, open an "
                                    f"issue first (CONTRIBUTING.md)")
                continue
            names.add(match["name"])
    if len(names) > 1:
        problems.append(f"changes {len(names)} designs ({', '.join(sorted(names))}); one pull "
                        f"request carries one design")
    for name in sorted(names & MAINTAINED):
        problems.append(f"designs/{name}/ is maintained by the project; propose a change to it "
                        f"in an issue")
    return problems, (f"designs/{next(iter(names))}/" if len(names) == 1 else None)


def read_files(path: str) -> list[tuple[str, str, str | None]]:
    changes = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if parts == [""]:
                continue
            changes.append((parts[0], parts[1], parts[2] if len(parts) > 2 else None))
    return changes


def api_get(url: str, token: str):
    request = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "portfolio-gallery-scope-check"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def pr_files(repository: str, number: int, token: str) -> list[tuple[str, str, str | None]]:
    """Every file of the pull request, page by page. The API lists at most
    3,000; a longer list cannot be checked whole, so it fails."""
    changes = []
    for page in range(1, 31):
        batch = api_get(f"{API}/repos/{repository}/pulls/{number}/files?per_page=100&page={page}", token)
        changes += [(f["status"], f["filename"], f.get("previous_filename")) for f in batch]
        if len(batch) < 100:
            break
    return changes


def summary(lines: list[str]) -> None:
    target = os.environ.get("GITHUB_STEP_SUMMARY")
    if target:
        with open(target, "a", encoding="utf-8") as handle:
            handle.write("\n".join(lines) + "\n")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Check a pull request's scope.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--pr", type=int)
    source.add_argument("--files")
    parser.add_argument("--author", help="with --files: the pull request author's login")
    args = parser.parse_args(argv)

    association, author = None, args.author
    if args.pr is not None:
        token, repository = os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_REPOSITORY")
        event_path = os.environ.get("GITHUB_EVENT_PATH")
        if not (token and repository and event_path):
            print("--pr needs GITHUB_TOKEN, GITHUB_REPOSITORY and GITHUB_EVENT_PATH", file=sys.stderr)
            return 2
        with open(event_path, encoding="utf-8") as handle:
            event = json.load(handle)
        pull = event.get("pull_request") or {}
        association = pull.get("author_association")
        author = (pull.get("user") or {}).get("login")
        if AS_CONTRIBUTOR in (pull.get("body") or ""):
            print(f"The description holds {AS_CONTRIBUTOR}: checked as a contributor's.")
            association = None
        expected = pull.get("changed_files")
        try:
            changes = pr_files(repository, args.pr, token)
        except (urllib.error.URLError, json.JSONDecodeError) as error:
            print(f"could not read the pull request's files: {error}", file=sys.stderr)
            return 2
        if expected is not None and len(changes) != expected:
            print(f"read {len(changes)} files but the pull request changes {expected}; the list "
                  f"cannot be checked whole", file=sys.stderr)
            return 1
    else:
        changes = read_files(args.files)

    if association in MAINTAINER_ASSOCIATIONS:
        message = (f"A maintainer's pull request ({association}): the scope is not limited, "
                   f"and the review covers all {len(changes)} file(s).")
        print(message)
        summary(["## Scope check", "", message])
        return 0
    problems, folder = scope_problems(changes, author)
    if problems:
        print("Out of scope:")
        for problem in problems:
            print(f"  - {problem}")
        summary(["## Scope check: out of scope", "",
                 "A pull request from outside the project adds or changes one design "
                 "folder, or its author's own showcase entry, and nothing else. What needs "
                 "to change:", ""]
                + [f"- {p}" for p in problems])
        return 1
    message = f"In scope: {len(changes)} file(s), all in {folder}."
    print(message)
    summary(["## Scope check", "", message])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
