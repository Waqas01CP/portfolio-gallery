"""Make a copy of portfolio-gallery its owner's: run once, by
.github/workflows/template-cleanup.yml, in a repository made with "Use this
template" (ADR-0015).

  python .github/template-cleanup/cleanup.py

It refuses, changing nothing, in Waqas01CP/portfolio-gallery itself and in
any fork of it, whatever the workflow's own condition says: the
repository's name comes from GITHUB_REPOSITORY, and whether it is a fork
from the event GitHub passes in GITHUB_EVENT_PATH. Outside GitHub Actions,
with neither set, it refuses too.

Otherwise it deletes every path listed in remove.txt beside this file that
exists, drops "in_use", a link to a design author's own site, from every
designs/*/design.json (ADR-0016), puts copy-README.md in place of
README.md, and deletes this folder last. With the folder gone a later run finds nothing to do, so it acts
once. It never touches .github/workflows/: the workflow's own next step
tries that, by a separate commit.

Prints each path it removed. Exit 0 when it cleaned or refused; 1 when a
listed path is absolute, climbs out of the repository, or names a
workflow file. Standard library only.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PROJECT = "Waqas01CP/portfolio-gallery"


def refusal() -> str | None:
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    if not repository:
        return "GITHUB_REPOSITORY is not set: this runs only in a copy, in GitHub Actions"
    if repository.lower() == PROJECT.lower():
        return f"this is {PROJECT} itself"
    event = os.environ.get("GITHUB_EVENT_PATH", "")
    try:
        fork = json.loads(Path(event).read_text(encoding="utf-8"))["repository"]["fork"]
    except (OSError, ValueError, KeyError, TypeError):
        return "the event does not say whether this repository is a fork"
    if fork is not False:
        return "this repository is a fork; a fork keeps the project's files"
    return None


def listed() -> list[str]:
    paths = []
    for number, line in enumerate((HERE / "remove.txt").read_text(encoding="utf-8").splitlines(), 1):
        entry = line.strip()
        if not entry or entry.startswith("#"):
            continue
        parts = PurePosixPath(entry).parts
        if entry.startswith("/") or ".." in parts or ":" in entry or "\\" in entry:
            sys.exit(f"remove.txt, line {number}: '{entry}' is not a path inside the repository")
        if parts[:2] == (".github", "workflows"):
            sys.exit(f"remove.txt, line {number}: '{entry}' is a workflow file; the workflow handles those")
        paths.append(entry)
    return paths


def main() -> int:
    if not (HERE / "remove.txt").is_file():
        print("Nothing to clean: this copy was cleaned up already.")
        return 0
    reason = refusal()
    if reason:
        print(f"Changing nothing: {reason}.")
        return 0
    for entry in listed():
        target = ROOT / entry
        if target.is_dir() and not target.is_symlink():
            shutil.rmtree(target)
        elif target.exists() or target.is_symlink():
            target.unlink()
        else:
            continue
        print(f"removed {entry}")
    # A design's "In use" link shows its author's site in the project's
    # gallery; a copy's own gallery has no use for it.
    for meta_path in sorted((ROOT / "designs").glob("*/design.json")):
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(meta, dict) and "in_use" in meta:
            del meta["in_use"]
            meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n",
                                 encoding="utf-8", newline="\n")
            print(f"dropped in_use from {meta_path.relative_to(ROOT).as_posix()}")
    shutil.copyfile(HERE / "copy-README.md", ROOT / "README.md")
    print("replaced README.md with a copy's own")
    shutil.rmtree(HERE)
    print("removed .github/template-cleanup, so this runs once")
    return 0


if __name__ == "__main__":
    sys.exit(main())
