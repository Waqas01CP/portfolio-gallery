"""The one entry point the workflows call, and the same commands locally.

  python tools/ci.py checks [--quick] [--axe FILE]
      Everything a pull request must pass: the workflows' job conditions
      (tools/check_workflows.py); every design checked; the showcase's
      files checked, while the project has the tool (tools/check_showcase.py,
      no fetching; checks.yml fetches a pull request's sites); the
      prompts for an AI assistant, the README's and a copy's, against the
      repository, while the project has it (tools/check_prompt.py); the site
      built in the design content/config.json names and the gallery built
      with every design, each built twice and compared byte for byte; the
      built files checked; the content trace; the gallery's pictures made as
      the deploy makes them (tools/screenshots.py: the previews, and the
      showcase's served copies, so a screenshot Chrome cannot read fails
      here) and held to assemble's rules; the template cleanup, while
      there is one (tools/check_template_cleanup.py); and the browser checks on
      every design's page, with axe when given axe.min.js.
      .github/workflows/checks.yml runs this, always with --axe, after
      fetching axe-core and checking its SHA-512 (ADR-0011).

  python tools/ci.py build --mode site|gallery [--out DIR]
      The deploy workflow's build: the site, or the gallery, built and its
      files checked, with the content trace for a site. No browser.

  python tools/ci.py pictures --gallery DIR
      A built gallery's pictures made, as the screenshot job makes them,
      and held to assemble's rules. Headless Chrome.

  python tools/ci.py assemble --site DIR --shots DIR
      The deploy workflow's last step before publishing: takes from the
      screenshot job's folder only the pictures the gallery shows, each a
      WebP image within its limit: designs/<name>/preview.webp for each
      design (300 KB), and showcase/<login>/card.webp (300 KB) and full.webp
      (1 MB) for each showcase entry, which must hold their image and
      nothing else, no EXIF, XMP or colour profile; it refuses anything
      else, and anything missing; then checks the site with its pictures
      (ADR-0010; ADR-0016, Changes, 2026-10-20). The folder is the screenshot
      job's _shots/, uploaded whole, as the build job uploads _site/.

Each step runs its own tool, prints what it ran, and stops the run at the
first failure with that tool's exit code. Standard library only; the
build needs the venv (docs/reference/commands.md).
"""

from __future__ import annotations

import argparse
import filecmp
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
sys.path.insert(0, str(ROOT))
from build import PREVIEW_FILE, SHOWCASE_CARD, SHOWCASE_FULL  # noqa: E402

PREVIEW_LIMIT = 300 * 1024
# A showcase entry's served copies (ADR-0016, Changes, 2026-10-20). Measured
# that day, at quality 0.82, from full-screen captures up to 5120 by 2880:
# the card's at most 147,498 bytes and the full view's 401,498, both for a
# wall of photographs.
SERVED_LIMITS = {SHOWCASE_CARD: 300 * 1024, SHOWCASE_FULL: 1024 * 1024}
SERVED_RE = re.compile(r"showcase/([a-z0-9](?:[a-z0-9]|-(?=[a-z0-9])){0,38})/(card|full)\.webp")


def served_problem(path: Path, limit: int, image_only: bool) -> str | None:
    """Why a picture from the screenshot job may not be published. A
    showcase copy must hold its image and nothing else: no EXIF, XMP or
    colour profile, no animation (image_only)."""
    if path.is_symlink() or not path.is_file():
        return "not a regular file"
    if path.stat().st_size > limit:
        return f"over {limit // 1024} KB"
    data = path.read_bytes()
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return "not a WebP image"
    if not image_only:
        return None
    pos = 12
    while pos + 8 <= len(data):
        kind, length = struct.unpack("<4sI", data[pos:pos + 8])
        if kind not in (b"VP8 ", b"VP8L", b"VP8X", b"ALPH"):
            return (f"carries a {kind.decode('latin-1').strip()} chunk: a served copy holds its "
                    f"image and no metadata")
        if kind == b"VP8X" and data[pos + 8] & ~0x10:
            return "its header announces metadata or animation: a served copy holds its image only"
        pos += 8 + length + (length & 1)
    return None


def showcase_logins(site: Path) -> set[str]:
    """The entries a built gallery shows, from its own page."""
    return {m[0] for m in SERVED_RE.findall((site / "index.html").read_text(encoding="utf-8"))}


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
    # The README's prompt for an AI assistant against what it restates;
    # a cleaned copy has neither the prompt nor this tool (ADR-0017).
    if (ROOT / "tools" / "check_prompt.py").is_file():
        run("tools/check_prompt.py")
    twice(as_of)
    twice(as_of, "--gallery")
    site, gallery = ROOT / "_site", ROOT / "_gallery"
    run("build.py", "--as-of", as_of, "--out", site)
    run("tools/check_built.py", site)
    run("tools/check_content.py", "--page", site / "index.html")
    run("build.py", "--as-of", as_of, "--gallery", "--out", gallery)
    run("tools/check_built.py", gallery)
    # The pictures, as the deploy's screenshot job makes them: so a
    # showcase screenshot Chrome cannot read fails here, on its pull
    # request, before it can reach main (ADR-0016, Changes, 2026-10-20).
    run("tools/screenshots.py", gallery)
    pictures(gallery)
    run("tools/check_built.py", gallery, "--previews")
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


def expected_pictures(site: Path) -> dict[str, tuple[int, bool]]:
    """Every picture the screenshot job must supply for this gallery, with
    its limit and whether it must be image only."""
    demos = {p.parent.name for p in (site / "designs").glob("*/index.html")}
    wanted = {f"designs/{name}/{PREVIEW_FILE}": (PREVIEW_LIMIT, False) for name in demos}
    for login in showcase_logins(site):
        for name, limit in SERVED_LIMITS.items():
            wanted[f"showcase/{login}/{name}"] = (limit, True)
    return wanted


def pictures(gallery: Path) -> None:
    """The pictures the screenshot job wrote into a gallery, held to
    assemble's rules."""
    wanted = expected_pictures(gallery)
    for relative, (limit, image_only) in sorted(wanted.items()):
        problem = served_problem(gallery / relative, limit, image_only)
        if problem:
            print(f"=== FAILED: {relative}: {problem}")
            raise Failed(1)
    print(f"=== {len(wanted)} picture(s) made and checked")


def assemble(site: Path, shots: Path) -> None:
    if not any((site / "designs").glob("*/index.html")):
        print(f"=== FAILED: {site} is not a built gallery")
        raise Failed(1)
    wanted = expected_pictures(site)
    taken = {}
    for path in sorted(shots.rglob("*")):
        if path.is_dir() and not path.is_symlink():
            continue
        relative = path.relative_to(shots).as_posix()
        if relative not in wanted:
            problem = (f"not a picture this gallery shows: designs/<name>/{PREVIEW_FILE} or "
                       f"showcase/<login>/{SHOWCASE_CARD} and {SHOWCASE_FULL}")
        else:
            problem = served_problem(path, *wanted[relative])
        if problem:
            print(f"=== FAILED: the screenshot job's {relative}: {problem}")
            raise Failed(1)
        taken[relative] = path
    missing = sorted(set(wanted) - set(taken))
    if missing:
        print(f"=== FAILED: the screenshot job supplied no {', '.join(missing)}")
        raise Failed(1)
    for relative, path in taken.items():
        (site / relative).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, site / relative)
    print(f"=== took {len(taken)} picture(s): {', '.join(sorted(taken))}")
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
    p = sub.add_parser("pictures")
    p.add_argument("--gallery", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "checks":
            checks(args.quick, args.axe)
        elif args.command == "build":
            build(args.mode, args.out.resolve())
        elif args.command == "pictures":
            run("tools/screenshots.py", args.gallery.resolve())
            pictures(args.gallery.resolve())
        else:
            assemble(args.site.resolve(), args.shots.resolve())
    except Failed as failure:
        return failure.code
    print("\n=== all passed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
