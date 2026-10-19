"""The one entry point the workflows call, and the same commands locally.

  python tools/ci.py checks [--quick] [--axe FILE]
      Everything a pull request must pass: the workflows' job conditions
      (tools/check_workflows.py); every design checked; the showcase's
      files checked, while the project has the tool (tools/check_showcase.py,
      no fetching; checks.yml fetches a pull request's sites); the site
      built in the design content/config.json names and the gallery built
      with every design, each built twice and compared byte for byte; the
      built files checked; the content trace; the template cleanup, while
      there is one (tools/check_template_cleanup.py); and the browser checks on
      every design's page, with axe when given axe.min.js.
      .github/workflows/checks.yml runs this, always with --axe, after
      fetching axe-core and checking its SHA-512 (ADR-0011).

  python tools/ci.py build --mode site|gallery [--out DIR]
      The deploy workflow's build: the site, or the gallery, built and its
      files checked, with the content trace for a site. No browser.

  python tools/ci.py assemble --site DIR --shots DIR
      The deploy workflow's last step before publishing: takes the gallery
      previews from the screenshot job's folder, only files at
      <name>/preview.webp for designs the site has, each a WebP image under
      300 KB, and refuses anything else; then checks the site with its
      previews (ADR-0010). The folder is laid out as upload-artifact stores
      _site/designs/*/preview.webp: the path from the first wildcard on
      (its README at v7.0.1).

Each step runs its own tool, prints what it ran, and stops the run at the
first failure with that tool's exit code. Standard library only; the
build needs the venv (docs/reference/commands.md).
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
sys.path.insert(0, str(ROOT))
from build import PREVIEW_FILE  # noqa: E402

PREVIEW_LIMIT = 300 * 1024


class Failed(Exception):
    def __init__(self, code: int) -> None:
        self.code = code


def run(*args: str) -> None:
    shown = " ".join(str(a) for a in args)
    print(f"\n=== {shown}", flush=True)
    code = subprocess.run([sys.executable, *map(str, args)], cwd=ROOT).returncode
    if code != 0:
        print(f"=== FAILED with exit {code}: {shown}", flush=True)
        raise Failed(code)


def same_tree(a: Path, b: Path) -> list[str]:
    """Files that differ between two builds, by content."""
    names_a = {p.relative_to(a).as_posix() for p in a.rglob("*") if p.is_file()}
    names_b = {p.relative_to(b).as_posix() for p in b.rglob("*") if p.is_file()}
    differ = sorted(names_a ^ names_b)
    differ += [n for n in sorted(names_a & names_b)
               if not filecmp.cmp(a / n, b / n, shallow=False)]
    return differ


def twice(as_of: str, *mode: str) -> None:
    """Build twice into fresh folders and compare every byte."""
    with tempfile.TemporaryDirectory(prefix="pg-twice-") as tmp:
        first, second = Path(tmp) / "a", Path(tmp) / "b"
        run("build.py", "--as-of", as_of, *mode, "--out", first)
        run("build.py", "--as-of", as_of, *mode, "--out", second)
        differ = same_tree(first, second)
        what = " ".join(mode) or "the site"
        if differ:
            print(f"=== FAILED: two builds of {what} differ: {', '.join(differ[:10])}")
            raise Failed(1)
        count = sum(1 for p in first.rglob("*") if p.is_file())
        print(f"=== two builds of {what}: {count} files, byte-identical")


def checks(quick: bool, axe: Path | None) -> None:
    as_of = datetime.now(timezone.utc).strftime("%Y-%m")
    run("tools/check_workflows.py")
    run("tools/check_design.py")
    # The showcase's files; a cleaned copy of the template has no showcase
    # and not this tool (ADR-0016).
    if (ROOT / "tools" / "check_showcase.py").is_file():
        run("tools/check_showcase.py")
    twice(as_of)
    twice(as_of, "--gallery")
    site, gallery = ROOT / "_site", ROOT / "_gallery"
    run("build.py", "--as-of", as_of, "--out", site)
    run("tools/check_built.py", site)
    run("tools/check_content.py", "--page", site / "index.html")
    run("build.py", "--as-of", as_of, "--gallery", "--out", gallery)
    run("tools/check_built.py", gallery)
    # The template cleanup, while there is one (a cleaned copy has none),
    # after the checks it repeats on the cleaned copy, so a fault in the
    # tree itself is reported by the check that finds it first.
    if (ROOT / ".github" / "template-cleanup" / "cleanup.py").is_file():
        run("tools/check_template_cleanup.py")
    browser = ["tools/check_browser.py", gallery]
    if quick:
        browser.append("--quick")
    if axe:
        browser += ["--axe", axe]
    run(*browser)


def build(mode: str, out: Path) -> None:
    run("build.py", *(["--gallery"] if mode == "gallery" else []), "--out", out)
    run("tools/check_built.py", out)
    if mode == "site":
        run("tools/check_content.py", "--page", out / "index.html")


def assemble(site: Path, shots: Path) -> None:
    demos = {p.parent.name for p in (site / "designs").glob("*/index.html")}
    if not demos:
        print(f"=== FAILED: {site} is not a built gallery")
        raise Failed(1)
    taken = {}
    for path in sorted(shots.rglob("*")):
        if path.is_dir() and not path.is_symlink():
            continue
        relative = path.relative_to(shots).as_posix()
        parts = relative.split("/")
        problem = None
        if path.is_symlink() or not path.is_file():
            problem = "not a regular file"
        elif len(parts) != 2 or parts[1] != PREVIEW_FILE:
            problem = f"not <name>/{PREVIEW_FILE}"
        elif parts[0] not in demos:
            problem = "no such design in the site"
        elif path.stat().st_size > PREVIEW_LIMIT:
            problem = f"over {PREVIEW_LIMIT // 1024} KB"
        else:
            head = path.read_bytes()[:12]
            if head[:4] != b"RIFF" or head[8:12] != b"WEBP":
                problem = "not a WebP image"
        if problem:
            print(f"=== FAILED: the screenshot job's {relative}: {problem}")
            raise Failed(1)
        taken[parts[0]] = path
    missing = sorted(demos - set(taken))
    if missing:
        print(f"=== FAILED: no preview for {', '.join(missing)}")
        raise Failed(1)
    for name, path in taken.items():
        shutil.copyfile(path, site / "designs" / name / PREVIEW_FILE)
    print(f"=== took {len(taken)} preview(s): {', '.join(sorted(taken))}")
    run("tools/check_built.py", site, "--previews")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="The workflows' entry point.")
    sub = parser.add_subparsers(dest="command", required=True)
    c = sub.add_parser("checks")
    c.add_argument("--quick", action="store_true")
    c.add_argument("--axe", type=Path)
    b = sub.add_parser("build")
    b.add_argument("--mode", choices=("site", "gallery"), required=True)
    b.add_argument("--out", type=Path, default=ROOT / "_site")
    a = sub.add_parser("assemble")
    a.add_argument("--site", type=Path, required=True)
    a.add_argument("--shots", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "checks":
            checks(args.quick, args.axe)
        elif args.command == "build":
            build(args.mode, args.out.resolve())
        else:
            assemble(args.site.resolve(), args.shots.resolve())
    except Failed as failure:
        return failure.code
    print("\n=== all passed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
