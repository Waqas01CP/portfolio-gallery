"""Lighthouse on each page against ADR-0009's speed goals (ADR-0012).

  python tools/check_speed.py _site
  python tools/check_speed.py _gallery --designs plain --skip-gallery-page
  python tools/check_speed.py _gallery --designs "" --runs 1

Lighthouse's default mobile run, five times a page: the median Largest
Contentful Paint within 2.5 s, the median Cumulative Layout Shift at most
0.1, the median Total Blocking Time under 200 ms, a median over that
reported and one over 600 ms failed (ADR-0012, Changes). Lighthouse comes from
tools/lighthouse/, installed by `npm ci --ignore-scripts`, which checks
every package against the lockfile's hash and runs none of their install
scripts; Chrome is the one tools/cdp.py finds, with its own temporary
profile. Error reporting to Lighthouse's makers is off.

Each page is served from 127.0.0.1 without compression, which GitHub
Pages adds, and on a shared runner: a number here is evidence that a
change made a page slower, not a phone's measurement (ADR-0012). A missing
Node or Lighthouse fails, naming what to install; it is never a skip
(ADR-0008, gate D).
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cdp import MissingTool, Server, find_chrome  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
# Lighthouse's command line as npm ci installs it here; PG_LIGHTHOUSE names
# another, as PG_CHROME does Chrome, for the proofs' copies of the tree.
CLI = Path(os.environ.get("PG_LIGHTHOUSE")
           or ROOT / "tools" / "lighthouse" / "node_modules" / "lighthouse" / "cli" / "index.js")
INSTALL = "npm ci --ignore-scripts --prefix tools/lighthouse"
# ADR-0009's goals: (audit, label, unit, the most a median may be, inclusive).
# TBT's goal is "under 200 ms", so its most is just below it.
GOALS = (("largest-contentful-paint", "LCP", "ms", 2500),
         ("cumulative-layout-shift", "CLS", "", 0.1),
         ("total-blocking-time", "TBT", "ms", 199.999))
# TBT follows the machine's load: one page measured 298 ms on this seat's
# machine while it was busy and 25 ms while it was not (2026-10-29), and a
# design, CSS only, cannot change it. So a TBT median over the goal is
# reported, and only one over this fails: a 600 ms script, ADR-0012's own
# case, measures over 1,000 (the owner's choice, ADR-0012, Changes).
TBT_FAILS_OVER = 600
RUN_SECONDS = 180


def shown(label: str, unit: str, value: float) -> str:
    return f"{value:.3f}" if not unit else f"{value:,.0f} {unit}"


def lighthouse(node: str, url: str, chrome: str, out: Path) -> dict:
    flags = "--headless=new --no-first-run --no-default-browser-check"
    # As in tools/cdp.py: the workflows set this on GitHub's runner only,
    # in jobs that hold no write token (ADR-0010).
    if os.environ.get("PG_CHROME_NO_SANDBOX") == "1":
        flags += " --no-sandbox"
    result = subprocess.run(
        [node, str(CLI), url, "--quiet", "--output=json", f"--output-path={out}",
         "--only-categories=performance", "--no-enable-error-reporting", f"--chrome-flags={flags}"],
        env={**os.environ, "CHROME_PATH": chrome}, capture_output=True, text=True,
        timeout=RUN_SECONDS)
    if result.returncode or not out.is_file():
        raise RuntimeError(f"Lighthouse exited with {result.returncode}: "
                           f"{(result.stderr or result.stdout).strip()[-600:]}")
    report = json.loads(out.read_text(encoding="utf-8"))
    if report.get("runtimeError"):
        raise RuntimeError(f"Lighthouse could not load the page: {report['runtimeError'].get('message')}")
    return report["audits"]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Lighthouse on each page against ADR-0009's speed goals.")
    parser.add_argument("folder", nargs="?", default="_site")
    parser.add_argument("--designs", metavar="NAME[,NAME]",
                        help="in a gallery, measure only these designs' demos; empty for none")
    parser.add_argument("--skip-gallery-page", action="store_true",
                        help="in a gallery, leave out the gallery page")
    parser.add_argument("--runs", type=int, default=5, help="runs a page, the median taken (default 5)")
    args = parser.parse_args(argv)
    root = Path(args.folder).resolve()
    if not (root / "index.html").is_file():
        print(f"no built page in {root}; run python build.py first", file=sys.stderr)
        return 2
    if args.runs < 1:
        print("--runs must be at least 1", file=sys.stderr)
        return 2
    demos = sorted(p.relative_to(root).as_posix() for p in (root / "designs").glob("*/index.html"))
    pages = demos + ["index.html"] if demos else ["index.html"]
    # The same narrowing as tools/check_browser.py's, so each job measures
    # the pages it checks (ADR-0019); a name the gallery lacks is refused.
    if args.designs is not None or args.skip_gallery_page:
        if not demos:
            print("--designs and --skip-gallery-page apply to a built gallery only", file=sys.stderr)
            return 2
        if args.designs is not None:
            names = [n for n in args.designs.split(",") if n]
            known = {d.split("/")[1] for d in demos}
            missing = sorted(set(names) - known)
            if missing:
                print(f"--designs names no design in this gallery: {', '.join(missing)}", file=sys.stderr)
                return 2
            pages = [d for d in demos if d.split("/")[1] in names] + ["index.html"]
        if args.skip_gallery_page:
            pages = [p for p in pages if p != "index.html"]
    if not pages:
        print("no page to measure, as asked")
        return 0
    try:
        node = shutil.which("node")
        if not node:
            raise MissingTool("Node.js was not found; install Node 22.19 or later (ADR-0012)")
        if not CLI.is_file():
            raise MissingTool(f"Lighthouse is not installed at {CLI}; run {INSTALL}")
        chrome = find_chrome()
    except MissingTool as error:
        print(f"missing tool: {error}", file=sys.stderr)
        return 1
    failures, notes, rows = [], [], []
    with Server(root) as server, tempfile.TemporaryDirectory(prefix="pg-speed-") as work:
        for page in pages:
            runs = []
            for n in range(args.runs):
                try:
                    audits = lighthouse(node, f"{server.origin}/{page}", chrome, Path(work) / f"run-{n}.json")
                except (RuntimeError, subprocess.TimeoutExpired) as error:
                    failures.append(f"{page}: run {n + 1}: {error}")
                    break
                runs.append([audits[audit]["numericValue"] for audit, *_ in GOALS])
            if len(runs) < args.runs:
                continue
            medians = [statistics.median(values) for values in zip(*runs)]
            cells = []
            for (audit, label, unit, most), median, values in zip(GOALS, medians, zip(*runs)):
                cells.append(f"{label} {shown(label, unit, median)}")
                if median > most:
                    goal = "under 200 ms" if label == "TBT" else f"at most {shown(label, unit, most)}"
                    said = (f"{page}: {label} median {shown(label, unit, median)}, over the goal, "
                            f"{goal} (runs: {', '.join(shown(label, unit, v) for v in values)})")
                    if label == "TBT" and median <= TBT_FAILS_OVER:
                        notes.append(f"{said}; reported, since TBT follows the runner's load; it fails "
                                     f"over {TBT_FAILS_OVER:,} ms (ADR-0012, Changes)")
                    else:
                        failures.append(said)
            rows.append((page, cells))
            print(f"  {page}: {', '.join(cells)} (median of {args.runs})")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary and rows:
        with open(summary, "a", encoding="utf-8") as out:
            out.write(f"\n### Speed, Lighthouse's default mobile run, median of {args.runs}\n\n"
                      "| Page | LCP | CLS | TBT |\n|---|---|---|---|\n")
            for page, cells in rows:
                out.write(f"| {page} | " + " | ".join(c.split(" ", 1)[1] for c in cells) + " |\n")
            for note in notes:
                out.write(f"\nNote: {note}\n")
    for note in notes:
        print(f"  NOTE {note}")
    for failure in failures:
        print(f"  FAIL {failure}")
    print(f"\n{'PASS' if not failures else 'FAIL'}: {len(failures)} failure(s), {len(rows)} page(s) measured")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
