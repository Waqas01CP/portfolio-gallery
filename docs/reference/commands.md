---
type: reference
description: Every command that exists in this repository, each with what it exits and why. The environment, the build, the checks, the CI entry point, the gates and the map. Read before running anything.
status: current
---

# Commands

Every command runs from the repository root. Each was run in the session
that recorded it, 2026-10-12 UTC, on Windows with Python 3.12.10, and
exited as described. Do not infer a command that is not here.

## Environment

The build runs only inside a venv at `.venv/`, with the versions pinned in
`requirements.txt`; build.py refuses to run outside a venv or against any
other installed version, because a different version can change the output
with no visible cause. pip checks every downloaded file against the SHA-256
listed (ADR-0004).

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt      Windows
.venv/bin/python -m pip install -r requirements.txt          macOS, Linux
```

Then activate it (`.venv\Scripts\Activate.ps1` in PowerShell,
`source .venv/Scripts/activate` in Git Bash, `source .venv/bin/activate`
elsewhere), or call `.venv/Scripts/python` directly as below.

Check that nothing else is installed: `python -m pip list --not-required`
prints Jinja2 and pip only.

## Build

```
python build.py                          the site, in config.json's design
python build.py --design plain           the site, in another design
python build.py --gallery                every design, and the gallery page
python build.py --as-of 2026-10          as of a given month
python build.py --out DIR                somewhere other than _site/
```

Exit 0 on success. On any content failure it exits 1, names every failing
item, and writes nothing. To look at the result, serve the folder:
`python -m http.server --directory _site 8000` and open
http://127.0.0.1:8000/ in your own browser.

## Checks

```
python tools/check_design.py [NAME ...]          designs: files, sizes, design.json, CSS
python tools/check_built.py [_site] [--previews] built files, without a browser
python tools/check_content.py [--cv FILE] [--page FILE]   the content trace
python tools/check_browser.py [_site] [--quick] [--axe FILE] [--only NAMES]
python tools/screenshots.py [_site]              the gallery's previews
python tools/scope_check.py --files LIST.tsv     a pull request's scope, locally
```

Each exits 0 on a pass, 1 on a failure with every problem printed, and 2
on a usage error or a missing input. The browser checks and the
screenshots need Google Chrome; set PG_CHROME to its path if it is not in
the usual place. They start their own headless Chrome with an empty
temporary profile and never touch your browser. A full browser run on the
gallery's two designs takes about 10 to 15 minutes on the machine of
2026-10-12; `--quick` is for iterating and is not a pass.

## The CI entry point

The workflows call these, and they run the same locally:

```
python tools/ci.py checks [--quick] [--axe FILE]
python tools/ci.py build --mode site|gallery [--out DIR]
python tools/ci.py assemble --site DIR --shots DIR
```

`checks` is everything a pull request must pass: designs, two builds each
of the site and the gallery compared byte for byte, the built files, the
content trace and the browser checks. It stops at the first failure with
that tool's exit code.

## Gates

Activate the hooks once per clone:

```
git config core.hooksPath .githooks
```

A fresh clone has no gates until this is run, and nothing catches the
omission (ADR-0008). `--no-verify` bypasses every gate and is never used.

Private patterns for gate A, such as a name or an email that must never
be committed, go in `.git/info/never-commit`, one per line; the format is
in tools/gates.py. That file lives inside git's own folder and is never
committed.

## Map

```
python tools/generate_map.py            write MAP.md
python tools/generate_map.py --check    compare the staged MAP.md with the staged files
```

Stage the Markdown files first, then regenerate and stage MAP.md. Exit 0
current, 1 a file needs fixing, 2 stale.
