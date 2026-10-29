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
      the deploy makes them (tools/screenshots.py: the previews, the
      gallery page's own picture, and the showcase's served copies, so a
      screenshot Chrome cannot read fails
      here) and held to assemble's rules; the template cleanup, while
      there is one (tools/check_template_cleanup.py); and the browser checks on
      every design's page, with axe when given axe.min.js.
      .github/workflows/checks.yml runs this, always with --axe, after
      fetching axe-core and checking its SHA-512 (ADR-0011).

  python tools/ci.py checks --since REF [--quick] [--axe FILE]
      The same, with the browser checks only on the pages the change since
      REF alters (ADR-0019): the gallery is built from REF too, and a
      design's demo is checked when any of its built files or the engine's
      shared ones differ; the gallery page when it or the showcase does.
      Every other check runs in full. Every page is checked when a file
      that decides how pages are checked changed (CHECKING below), or when
      REF cannot be read or built. checks.yml passes the merge's base on a
      pull request and the previous main on a push.

  python tools/ci.py changes --since REF
      Only what `checks --since REF` would check, and why.

  python tools/ci.py build --mode site|gallery [--out DIR]
      The deploy workflow's build: the site, or the gallery, built and its
      files checked, with the content trace for a site. No browser.

  python tools/ci.py pictures --gallery DIR
      A built gallery's pictures made, as the screenshot job makes them,
      and held to assemble's rules. Headless Chrome.

  python tools/ci.py pages --mode site|gallery
      The deploy workflow's question before it publishes: is GitHub Pages
      on, publishing from GitHub Actions? It asks GitHub's API with the
      run's own token (Pages: read). On, it says so. Off in a copy, whose
      owner has not turned it on yet, it ends with a notice in the run's
      summary and an annotation, naming the setting and how to run Deploy
      again, and publishes nothing: a red first run reads as a broken
      template (the owner's decision of 2026-10-23, ADR-0015, Changes).
      Off in the gallery, set to publish from a branch, or any other
      answer, it fails: the gallery would be down, or the site published
      would not be the one built. Writes on=true or on=false to
      GITHUB_OUTPUT. pages_verdict() is the decision, and
      tools/check_workflows.py holds it to its table.

  python tools/ci.py assemble --site DIR --shots DIR
      The deploy workflow's last step before publishing: takes from the
      screenshot job's folder only the pictures the gallery shows, each a
      WebP image within its limit: preview.webp, the gallery page's own
      picture (300 KB; ADR-0017, Changes, 2026-10-23),
      designs/<name>/preview.webp for each
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
import io
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tarfile
import tempfile
import urllib.error
import urllib.request
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

# What the run says when GitHub Pages is off in a copy; the copy's README
# and its prompt name the same title (tools/check_prompt.py holds them).
PAGES_OFF_TITLE = "Turn on GitHub Pages to publish your site"
PAGES_OFF_STEPS = ("In this repository: Settings, then Pages, and under Build and deployment set Source to "
                   "GitHub Actions. Then Actions, Deploy, Run workflow, or commit any change: the next run "
                   "publishes.")
PAGES_SETTING = "Settings, Pages, Build and deployment, Source: GitHub Actions"

# The files that decide how a page is checked rather than what it is: a
# change to any of them means every page is checked (ADR-0019). The pages
# themselves are compared as built, so the engine, the designs, the content
# and the samples need no entry here; build.py neither, since what it does
# to a page shows in the page. Its one part in the checking, the showcase's
# shape limits the packing check reads, is covered by checking the gallery
# page whenever build.py changes (ADR-0019, Changes, 2026-10-29).
CHECKING = ("requirements.txt", "tools/ci.py", "tools/check_browser.py", "tools/cdp.py",
            ".github/workflows/checks.yml")


def pages_verdict(mode: str, status: int, build_type: str | None) -> tuple[str, str]:
    """What Deploy does, by what GitHub's API says of Pages: ("publish",
    "notice" or "fail", the message). Only a 404 means Pages is off."""
    if status == 200 and build_type == "workflow":
        return "publish", "GitHub Pages is on, publishing from GitHub Actions"
    if status == 200:
        return "fail", (f"GitHub Pages publishes from a branch here, not from GitHub Actions, so what "
                        f"it shows is not what was built and checked; set {PAGES_SETTING}")
    if status == 404 and mode == "gallery":
        return "fail", f"GitHub Pages is off, so the gallery is not published; set {PAGES_SETTING}"
    if status == 404:
        return "notice", f"GitHub Pages is off, so this run published nothing. {PAGES_OFF_STEPS}"
    return "fail", f"GitHub's API answered {status} when asked whether GitHub Pages is on"


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


class Selection:
    """What the browser checks look at after a change (ADR-0019): every page,
    with the reason; or the designs whose demos changed, those that did not,
    and whether the gallery page did."""

    def __init__(self, reason: str = "", check: list[str] | None = None,
                 unchanged: list[str] | None = None, page: bool = True) -> None:
        self.everything = check is None
        self.reason = reason
        self.check = check or []
        self.unchanged = unchanged or []
        self.page = page

    def lines(self, base: str) -> list[str]:
        if self.everything:
            return [f"since {base}: every page is checked: {self.reason}"]
        return [f"since {base}:",
                f"  check: {', '.join(self.check) or 'no design'}",
                f"  unchanged, passed at the base: {', '.join(self.unchanged) or 'none'}",
                f"  the gallery page: {'checked' if self.page else 'unchanged'}"]


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True)


def differs(a: Path, b: Path) -> bool:
    """Whether two built folders differ, a missing one counting as different."""
    return not (a.is_dir() and b.is_dir()) or bool(same_tree(a, b))


def select(since: str, as_of: str, gallery: Path) -> Selection:
    """Compare the gallery built from this tree with the one built from
    `since`. Any doubt checks every page: the base unreadable or unbuildable,
    or a change to how pages are checked."""
    found = git("rev-parse", "--verify", "--quiet", f"{since}^{{commit}}")
    if found.returncode != 0:
        return Selection(f"the base {since} is not in this clone")
    sha = found.stdout.decode().strip()
    # Names separated by NUL, so a name with spaces, as a screenshot's often
    # has, or one git would quote, stays whole.
    listed = git("diff", "--name-only", "-z", sha)
    extra = git("ls-files", "--others", "--exclude-standard", "-z")
    if listed.returncode != 0 or extra.returncode != 0:
        return Selection("git could not list what changed")
    changed = {n for n in (listed.stdout + extra.stdout).decode("utf-8", "surrogateescape").split("\0") if n}
    deciding = sorted(changed & set(CHECKING))
    if deciding:
        return Selection(f"{', '.join(deciding)} changed, which decides how pages are checked")
    with tempfile.TemporaryDirectory(prefix="pg-base-") as tmp:
        source, out = Path(tmp) / "source", Path(tmp) / "out"
        tree = git("archive", "--format=tar", sha)
        if tree.returncode != 0:
            return Selection(f"git could not read the base {sha[:7]}")
        with tarfile.open(fileobj=io.BytesIO(tree.stdout)) as tar:
            tar.extractall(source, filter="data")
        built = subprocess.run([sys.executable, "build.py", "--as-of", as_of, "--gallery", "--out", str(out)],
                               cwd=source, capture_output=True, text=True)
        if built.returncode != 0:
            last = (built.stdout + built.stderr).strip().splitlines()[-1:] or ["no output"]
            return Selection(f"the base {sha[:7]} does not build: {last[0]}")
        if differs(gallery / "static", out / "static"):
            return Selection("the engine's shared files differ")
        names = sorted(p.parent.name for p in (gallery / "designs").glob("*/index.html"))
        check = [n for n in names if differs(gallery / "designs" / n, out / "designs" / n)]
        # The gallery page: its own files, everything outside designs/, and
        # the showcase's sources, whose served copies the screenshots make.
        def outside(root: Path) -> set[str]:
            return {p.relative_to(root).as_posix() for p in root.rglob("*")
                    if p.is_file() and p.relative_to(root).parts[0] != "designs"}
        here, there = outside(gallery), outside(out)
        page = (here != there or any(not filecmp.cmp(gallery / n, out / n, shallow=False) for n in here)
                or any(n.startswith("showcase/") for n in changed)
                or "build.py" in changed)
        return Selection(check=check, unchanged=[n for n in names if n not in check], page=page)


def chosen(since: str | None, as_of: str, gallery: Path) -> Selection | None:
    """The selection for a run, printed, and written to the run's summary on
    GitHub; None for a run with no base, which checks every page."""
    if not since:
        return None
    # A fault in the selection itself checks every page rather than stop
    # the run: as safe, and nobody waits on a red run for nothing.
    try:
        selection = select(since, as_of, gallery)
    except Exception as error:  # noqa: BLE001
        selection = Selection(f"the selection failed ({type(error).__name__}: {error})")
    lines = selection.lines(since)
    print("\n=== the browser checks, " + "\n".join(lines), flush=True)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as out:
            out.write("### What the browser checks looked at\n\n" + "\n".join(lines) + "\n")
    return selection


def plan(since: str | None) -> None:
    """The browser checks' share-out for a run on GitHub (ADR-0019, Changes,
    2026-10-29): the designs whose pages to check, one job each, and whether
    the gallery page is checked, written to GITHUB_OUTPUT as designs (a
    JSON list), count and page. With no base, or on any doubt, every page."""
    as_of = datetime.now(timezone.utc).strftime("%Y-%m")
    with tempfile.TemporaryDirectory(prefix="pg-plan-") as tmp:
        gallery = Path(tmp) / "gallery"
        run("build.py", "--as-of", as_of, "--gallery", "--out", gallery)
        names = sorted(p.parent.name for p in (gallery / "designs").glob("*/index.html"))
        selection = chosen(since, as_of, gallery)
    if selection is None or selection.everything:
        designs, page = names, True
        print(f"\n=== the plan: every page, {len(names)} design(s) and the gallery page")
    else:
        designs, page = selection.check, selection.page
        print(f"\n=== the plan: {len(designs)} design(s){' and the gallery page' if page else ''}")
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as out:
            out.write(f"designs={json.dumps(designs)}\ncount={len(designs)}\npage={'true' if page else 'false'}\n")


# The verdict's table: each part of a run on GitHub, the result it must
# have, given the plan. A part the plan gave nothing to do must be skipped,
# never failed or cancelled; any other result fails the run.
def verdict(env: dict[str, str]) -> int:
    count, page = env.get("PLANNED_COUNT", ""), env.get("PLANNED_PAGE", "")
    expected = {
        "plan": "success",
        "files": "success",
        "browser": "success" if count not in ("", "0") else "skipped",
        "gallery page": "success" if page == "true" else "skipped",
    }
    keys = {"plan": "RESULT_PLAN", "files": "RESULT_FILES", "browser": "RESULT_BROWSER",
            "gallery page": "RESULT_PAGE"}
    if count == "" or page not in ("true", "false"):
        expected["plan"] = "success, with a plan"
    rows, ok = [], True
    for part, want in expected.items():
        got = env.get(keys[part], "") or "no result"
        held = got == want
        ok = ok and held
        rows.append(f"  {'ok  ' if held else 'FAIL'} {part}: {got}, expected {want}")
    lines = [f"the plan: {count or 'none'} design(s), the gallery page {'checked' if page == 'true' else 'not checked'}"]
    lines += rows
    print("\n".join(lines))
    summary = env.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as out:
            out.write("### The checks' verdict\n\n" + "\n".join(lines) + "\n")
    print(f"\n=== {'all parts passed' if ok else 'FAILED: a part did not pass, or ran when it should not'}")
    return 0 if ok else 1


def checks(quick: bool, axe: Path | None, since: str | None = None, browser_checks: bool = True) -> None:
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
    # Each sample person's own site, in the design it shows, built and traced
    # to that person's CV as a user's site is; the gallery shows the same
    # content in that design's demo (ADR-0018). A cleaned copy has none.
    samples = ROOT / "samples"
    for folder in sorted(samples.iterdir()) if samples.is_dir() else []:
        own = ROOT / "_samples" / folder.name
        run("build.py", "--as-of", as_of, "--content", folder, "--out", own)
        run("tools/check_built.py", own)
        run("tools/check_content.py", "--content", folder, "--page", own / "index.html")
    run("build.py", "--as-of", as_of, "--gallery", "--out", gallery)
    run("tools/check_built.py", gallery)
    # Compared before the pictures are added to it, as the base is built.
    selection = chosen(since, as_of, gallery) if browser_checks else None
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
    if not browser_checks:
        print("\n=== the browser checks: run in their own jobs, as the plan shares them out")
        return
    browser = ["tools/check_browser.py", gallery]
    if quick:
        browser.append("--quick")
    if axe:
        browser += ["--axe", axe]
    if selection and not selection.everything:
        if not selection.check and not selection.page:
            print("\n=== the browser checks: no page changed; nothing to check")
            return
        browser += ["--designs", ",".join(selection.check)]
        if not selection.page:
            browser.append("--skip-gallery-page")
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
    # The gallery page's own picture, which the README shows.
    wanted[PREVIEW_FILE] = (PREVIEW_LIMIT, False)
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
            problem = (f"not a picture this gallery shows: {PREVIEW_FILE}, designs/<name>/{PREVIEW_FILE} or "
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


def pages(mode: str) -> None:
    api = os.environ.get("GITHUB_API_URL", "https://api.github.com").rstrip("/")
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    if not repository:
        print("=== FAILED: GITHUB_REPOSITORY is not set: this runs in GitHub Actions")
        raise Failed(1)
    request = urllib.request.Request(f"{api}/repos/{repository}/pages", headers={
        "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {os.environ.get('GITHUB_TOKEN', '')}"})
    build_type = None
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            status = response.status
            build_type = json.loads(response.read().decode("utf-8")).get("build_type")
    except urllib.error.HTTPError as error:
        status = error.code
    except (urllib.error.URLError, OSError, ValueError, AttributeError) as error:
        print(f"::error title=GitHub Pages::GitHub's API could not be asked whether GitHub Pages is on: {error}")
        raise Failed(1)
    verdict, message = pages_verdict(mode, status, build_type)
    print(f"=== {mode}: GitHub's API answered {status}, build_type {build_type}: {verdict}")
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as out:
            out.write(f"on={'true' if verdict == 'publish' else 'false'}\n")
    if verdict == "fail":
        print(f"::error title=GitHub Pages::{message}")
        raise Failed(1)
    if verdict == "notice":
        print(f"::notice title={PAGES_OFF_TITLE}::{message}")
        summary = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary:
            with open(summary, "a", encoding="utf-8") as out:
                out.write(f"## {PAGES_OFF_TITLE}\n\n"
                          "GitHub Pages is off in this repository, so this run published nothing. "
                          "Turn it on once:\n\n"
                          "1. **Settings**, then **Pages** in the left sidebar.\n"
                          "2. Under \"Build and deployment\", set **Source** to **GitHub Actions**.\n"
                          "3. **Actions**, then **Deploy** in the left list, then **Run workflow**, and the "
                          "green **Run workflow** button. Or commit any change: the next run publishes.\n")
    else:
        print(f"=== {message}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="The workflows' entry point.")
    sub = parser.add_subparsers(dest="command", required=True)
    c = sub.add_parser("checks")
    c.add_argument("--quick", action="store_true")
    c.add_argument("--axe", type=Path)
    c.add_argument("--since", metavar="REF")
    c.add_argument("--no-browser", action="store_true")
    w = sub.add_parser("changes")
    w.add_argument("--since", metavar="REF", required=True)
    n = sub.add_parser("plan")
    n.add_argument("--since", metavar="REF")
    sub.add_parser("verdict")
    b = sub.add_parser("build")
    b.add_argument("--mode", choices=("site", "gallery"), required=True)
    b.add_argument("--out", type=Path, default=ROOT / "_site")
    a = sub.add_parser("assemble")
    a.add_argument("--site", type=Path, required=True)
    a.add_argument("--shots", type=Path, required=True)
    p = sub.add_parser("pictures")
    p.add_argument("--gallery", type=Path, required=True)
    g = sub.add_parser("pages")
    g.add_argument("--mode", choices=("site", "gallery"), required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "checks":
            checks(args.quick, args.axe, args.since, browser_checks=not args.no_browser)
        elif args.command == "plan":
            plan(args.since)
            return 0
        elif args.command == "verdict":
            return verdict(dict(os.environ))
        elif args.command == "changes":
            as_of = datetime.now(timezone.utc).strftime("%Y-%m")
            with tempfile.TemporaryDirectory(prefix="pg-head-") as tmp:
                run("build.py", "--as-of", as_of, "--gallery", "--out", Path(tmp) / "gallery")
                chosen(args.since, as_of, Path(tmp) / "gallery")
            return 0
        elif args.command == "build":
            build(args.mode, args.out.resolve())
        elif args.command == "pictures":
            run("tools/screenshots.py", args.gallery.resolve())
            pictures(args.gallery.resolve())
        elif args.command == "pages":
            pages(args.mode)
            return 0
        else:
            assemble(args.site.resolve(), args.shots.resolve())
    except Failed as failure:
        return failure.code
    print("\n=== all passed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
