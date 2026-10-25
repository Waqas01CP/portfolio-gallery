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
python build.py --content samples/NAME   a sample person's site, from their own content
```

Exit 0 on success. On any content failure it exits 1, names every failing
item, and writes nothing. To look at the result, serve the folder:
`python -m http.server --directory _site 8000` and open
http://127.0.0.1:8000/ in your own browser.

## Checks

```
python tools/check_workflows.py [FILE ...]      when each workflow job runs
python tools/check_template_cleanup.py          what a copy keeps after its cleanup
python tools/check_design.py [NAME ...]          designs: files, sizes, design.json, CSS
python tools/check_showcase.py                   the showcase's files
python tools/check_showcase.py --fetch-all       also every showcase site and In use link, by response
python tools/check_showcase.py --fetch-url URL [--login LOGIN]   one address's response
python tools/check_built.py [_site] [--previews] built files, without a browser
python tools/check_prompt.py [README]            the prompts for an AI, the README's and a copy's, and AGENTS.md, against the repository
python tools/check_content.py [--cv FILE] [--page FILE] [--content DIR]   the content trace
python tools/check_browser.py [_site] [--quick] [--axe FILE] [--only NAMES]
python tools/screenshots.py [_site]              the gallery's previews, showcase copies and own picture
python tools/ci.py pictures --gallery _site      those pictures made and checked
python tools/scope_check.py --files LIST.tsv [--author LOGIN]   a pull request's scope, locally
```

Each exits 0 on a pass, 1 on a failure with every problem printed, and 2
on a usage error or a missing input. The browser checks and the
screenshots need Google Chrome; set PG_CHROME to its path if it is not in
the usual place. They start their own headless Chrome with an empty
temporary profile and never touch your browser. A full browser run on the
gallery's two designs took 487 s on the seat's Windows machine on
2026-10-12, about four minutes per design, and 623 s with `--axe` on
2026-10-16; on its seven designs, 1,997 s with `--axe` on 2026-10-24,
and on twelve, 3,606 s on 2026-10-25.
`--quick` is for iterating and is not a pass.

To prove the checks can fail, run each on the case built to defeat it:

```
python tools/prove_checks.py            the file checks, about a minute
python tools/prove_checks.py --browser  also the browser checks
python tools/prove_checks.py --browser --axe .cache/package/axe.min.js
```

### axe-core

The checks workflow fetches axe-core itself (ADR-0011). To run axe on your
own computer, fetch the same file into `.cache/`, which git ignores, and
check it against `AXE_SHA512` in `.github/workflows/checks.yml` before
using it. Each form below was run on 2026-10-15 UTC; each refused a copy
with one byte added.

In PowerShell (Windows PowerShell 5.1 needs `-UseBasicParsing`):

```
New-Item -ItemType Directory -Force .cache
Invoke-WebRequest https://registry.npmjs.org/axe-core/-/axe-core-4.14.0.tgz -OutFile .cache\axe-core.tgz -UseBasicParsing
$want = (Select-String -Path .github\workflows\checks.yml -Pattern 'AXE_SHA512: (\w+)').Matches[0].Groups[1].Value
(Get-FileHash .cache\axe-core.tgz -Algorithm SHA512).Hash -eq $want
tar -xzf .cache\axe-core.tgz -C .cache package/axe.min.js
```

The fourth line must print `True`; if it prints `False`, delete `.cache`
and use nothing from it. In Git Bash or on Linux:

```
mkdir -p .cache
curl --fail --proto '=https' -o .cache/axe-core.tgz https://registry.npmjs.org/axe-core/-/axe-core-4.14.0.tgz
echo "$(sed -n 's/^ *AXE_SHA512: //p' .github/workflows/checks.yml)  .cache/axe-core.tgz" | sha512sum --check --strict
tar -xzf .cache/axe-core.tgz -C .cache package/axe.min.js
```

The third line must print `OK`; if it prints `FAILED`, delete `.cache`
and use nothing from it. The version in the address is `AXE_VERSION` in
the same workflow; change both together. Then pass `--axe .cache/package/axe.min.js`
to check_browser.py, ci.py checks or prove_checks.py.

## The CI entry point

The workflows call these, and they run the same locally:

```
python tools/ci.py checks [--quick] [--axe FILE]
python tools/ci.py build --mode site|gallery [--out DIR]
python tools/ci.py assemble --site DIR --shots DIR
python tools/ci.py pages --mode site|gallery
```

`pages` is Deploy's question before it publishes, whether GitHub Pages is on; it reads GITHUB_REPOSITORY, GITHUB_TOKEN and GITHUB_API_URL as GitHub Actions sets them, so it runs only there, or against a fake API as the defeat cases run it.

`checks` is everything a pull request must pass: the workflows' job
conditions, designs, two builds each of the site and the gallery compared
byte for byte, the built files, the content trace and the browser checks,
axe among them when given `--axe`, as the checks workflow always gives
it. It stops at the first failure with that tool's exit code.

## Gates

Activate the hooks once per clone:

```
git config core.hooksPath .githooks
```

A fresh clone has no gates until this is run, and nothing catches the
omission (ADR-0008). `--no-verify` bypasses every gate and is never used.

Commits to this repository are made as Waqas01CP with GitHub's no-reply
address (the owner's decision of 2026-10-15), set once per clone so a
global identity never reaches the history:

```
git config user.name Waqas01CP
git config user.email 135085564+Waqas01CP@users.noreply.github.com
```

Gate A refuses a commit whose author or committer holds a private
pattern, so a forgotten setting is caught on the maintainer's machine.

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
