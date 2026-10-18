"""Check that the template cleanup leaves a copy that works (ADR-0015).

  python tools/check_template_cleanup.py

Copies this repository's files to a temporary folder and there runs
.github/template-cleanup/cleanup.py as GitHub Actions would:

  1. as Waqas01CP/portfolio-gallery itself: nothing may change;
  2. as a fork of it: nothing may change;
  3. as a copy: every path remove.txt lists is gone, CODE_OF_CONDUCT.md and
     .github/CODEOWNERS above all, since they name the project's owner;
     README.md is the copy's own; .github/template-cleanup/ is gone, so it
     acts once; nothing else changed;
  4. with only the script left and no list, as a later run would find it:
     nothing may change;
  5. the cleaned copy passes its own checks without a browser: its
     workflows, its designs, the site and the gallery built, their files
     checked, the content trace;
  6. every relative link in the cleaned copy's Markdown names a file that
     exists.

Exit 0 on a pass; 1 on a failure, each printed; 2 when there is no
cleanup to check. Standard library only; needs the venv, as the build
does.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLEANUP = Path(".github/template-cleanup")
PROJECT = "Waqas01CP/portfolio-gallery"
MUST_GO = ("CODE_OF_CONDUCT.md", ".github/CODEOWNERS")
LINK = re.compile(r"\]\(([^)\s]+)\)")


SKIP = {".git", ".venv", "__pycache__", ".cache", "_gallery"}


def tracked() -> list[str]:
    def ls(*extra):
        out = subprocess.run(["git", "ls-files", "-z", *extra], cwd=ROOT, capture_output=True, check=True)
        return [p for p in out.stdout.decode().split("\0") if p]
    try:
        # Files written but not yet staged belong to the tree being checked.
        return sorted(set(ls()) | set(ls("--others", "--exclude-standard")))
    except (OSError, subprocess.CalledProcessError):
        # No repository, as in gate B's staged tree and the defeat
        # harness's copy: every file but the venv and build output.
        return sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file()
                      and not any(part in SKIP or part.startswith("_site")
                                  for part in p.relative_to(ROOT).parts))


def snapshot(folder: Path) -> dict[str, str]:
    return {p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in folder.rglob("*") if p.is_file()}


def run_cleanup(copy: Path, repository: str, fork: bool, work: Path) -> subprocess.CompletedProcess:
    event = work / f"event-{len(list(work.glob('event-*')))}.json"
    event.write_text(json.dumps({"repository": {"full_name": repository, "fork": fork}}), encoding="utf-8")
    env = dict(os.environ, GITHUB_REPOSITORY=repository, GITHUB_EVENT_PATH=str(event))
    return subprocess.run([sys.executable, str(copy / CLEANUP / "cleanup.py")], cwd=copy, env=env,
                          capture_output=True, text=True)


def main() -> int:
    sys.stdout.reconfigure(errors="backslashreplace")
    if not (ROOT / CLEANUP / "cleanup.py").is_file():
        print("no template cleanup to check", file=sys.stderr)
        return 2
    problems: list[str] = []
    work = Path(tempfile.mkdtemp(prefix="pg-cleanup-"))
    try:
        copy = work / "repo"
        for name in tracked():
            source = ROOT / name
            if source.is_file():
                (copy / name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, copy / name)
        before = snapshot(copy)
        listed = [line.strip() for line in (copy / CLEANUP / "remove.txt").read_text(encoding="utf-8").splitlines()
                  if line.strip() and not line.strip().startswith("#")]

        # 1 and 2: the guards.
        for label, repository, fork in (("Waqas01CP/portfolio-gallery", PROJECT, False),
                                        ("a fork", "someone/portfolio-gallery", True)):
            result = run_cleanup(copy, repository, fork, work)
            if result.returncode != 0 or snapshot(copy) != before:
                problems.append(f"the cleanup changed files in {label}, or failed there "
                                f"(exit {result.returncode}): {result.stdout.strip()[-200:]}")
                return report(problems)
        print(f"ok   guards: nothing changes in {PROJECT} or in a fork")

        # 3: a copy.
        result = run_cleanup(copy, "someone/my-portfolio", False, work)
        if result.returncode != 0:
            problems.append(f"the cleanup failed in a copy (exit {result.returncode}): "
                            f"{(result.stdout + result.stderr).strip()[-300:]}")
            return report(problems)
        after = snapshot(copy)
        for entry in listed:
            if (copy / entry).exists():
                problems.append(f"the cleanup left {entry}, which remove.txt lists")
        for entry in MUST_GO:
            if (copy / entry).exists():
                problems.append(f"the cleanup left {entry}, which names the project's owner")
        if (copy / CLEANUP).exists():
            problems.append("the cleanup left .github/template-cleanup/, so it acts more than once")
        if after.get("README.md") != before.get(f"{CLEANUP.as_posix()}/copy-README.md"):
            problems.append("README.md is not the copy's own (.github/template-cleanup/copy-README.md)")
        gone = {p for p in before if p not in after}
        for path in sorted(gone):
            if not any(path == e or path.startswith(e.rstrip("/") + "/") for e in listed + [CLEANUP.as_posix()]):
                problems.append(f"the cleanup removed {path}, which remove.txt does not list")
        for path in sorted(p for p in after if p in before and after[p] != before[p] and p != "README.md"):
            problems.append(f"the cleanup changed {path}")
        print(f"ok   a copy: {len(gone)} files removed, README.md replaced" if not problems else
              "FAIL a copy")

        # 4: a later run, with the script and no list.
        (copy / CLEANUP).mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / CLEANUP / "cleanup.py", copy / CLEANUP / "cleanup.py")
        later = snapshot(copy)
        result = run_cleanup(copy, "someone/my-portfolio", False, work)
        shutil.rmtree(copy / CLEANUP)
        if result.returncode != 0 or snapshot(copy) != {k: v for k, v in later.items()
                                                       if not k.startswith(CLEANUP.as_posix() + "/")}:
            problems.append("a later run, with no list, changed files")
        else:
            print("ok   a later run changes nothing")

        # 5: the cleaned copy's own checks.
        as_of = datetime.now(timezone.utc).strftime("%Y-%m")
        steps = [["tools/check_workflows.py"], ["tools/check_design.py"],
                 ["build.py", "--as-of", as_of, "--out", "_site"], ["tools/check_built.py", "_site"],
                 ["tools/check_content.py", "--page", "_site/index.html"],
                 ["build.py", "--as-of", as_of, "--gallery", "--out", "_gallery"],
                 ["tools/check_built.py", "_gallery"]]
        for step in steps:
            result = subprocess.run([sys.executable, *step], cwd=copy, capture_output=True, text=True)
            if result.returncode != 0:
                problems.append(f"the cleaned copy fails {' '.join(step)}: "
                                f"{(result.stdout + result.stderr).strip()[-400:]}")
                break
        else:
            print("ok   the cleaned copy passes its workflows, designs, builds, built files and trace")

        # 6: links.
        broken, checked = [], 0
        for md in sorted(copy.rglob("*.md")):
            if any(part.startswith(("_site", "_gallery", ".venv")) for part in md.relative_to(copy).parts):
                continue
            for target in LINK.findall(md.read_text(encoding="utf-8")):
                if re.match(r"[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
                    continue
                checked += 1
                path = (md.parent / target.split("#", 1)[0]).resolve()
                if not path.exists():
                    broken.append(f"{md.relative_to(copy).as_posix()} links to {target}, which the copy lacks")
        problems += broken
        if not broken:
            print(f"ok   every relative link in the copy's Markdown resolves ({checked} links)")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return report(problems)


def report(problems: list[str]) -> int:
    for problem in problems:
        print(f"FAIL {problem}")
    print(f"\n{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
