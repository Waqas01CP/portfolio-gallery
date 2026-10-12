---
status: accepted
topic: build
description: "The build: a small Python generator with Jinja2, the only dependency, pinned by hash; run by GitHub Actions so a user installs nothing; local builds kept; nothing built is committed. Read before changing the build or adding any dependency."
date: 2026-10-11
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0004: Build with a Python generator, on GitHub Actions

## Context and Problem Statement

The engine copied from the operator's site is a small Python generator,
built locally with its output committed (that site's ADR-0006). A template
has different users: many will not have Python, and a user who forks the
repository and edits one file in the browser should get a site without
installing anything. A build on GitHub's runners serves them, and brings
two risks a local build does not have: the build now runs on a machine
that, on the main branch, can publish the site, and the build's
dependencies are fetched there on every run.

## Decision Drivers

- The strategy the operator adopted on 2026-10-11: "a build that runs on
  GitHub itself. Then a user forks, edits one file in the browser, and has
  a site without installing Python."
- His condition the same day: "approved but have to make sure that rules
  are being followed and no malware or things like that."
- Scope floor lines 4 and 5 (ADR-0001): no paid service; no dependency
  without a record.

## Assumptions

- A1. GitHub Actions is free for public repositories on GitHub's own
  runners. **Sourced**: GitHub's billing documentation, as recorded in the
  operator's Tooling and Cost Constraints; not re-read this session.
- A2. GitHub's Ubuntu 24.04 runner carries Python 3.12 and Google Chrome.
  **Sourced**: actions/runner-images, Ubuntu2404-Readme.md, image
  20261004.327.1, read 2026-10-12: Python 3.12.3, Google Chrome
  154.0.8037.97.
- A3. pip refuses a downloaded file whose hash is not listed, once any
  requirement carries a hash. **Measured** 2026-10-12: requirements.txt
  with every file's SHA-256 from PyPI installed cleanly into a fresh venv
  on Windows; a wrong hash is a defeat case for the session log.

## Considered Options

- The Python generator, built by GitHub Actions; local builds kept
- The Python generator, built locally, output committed (the operator's
  site's way)
- A site framework with its own GitHub Pages integration (Jekyll, Astro)

## Decision Outcome

Chosen option: "The Python generator, built by GitHub Actions; local builds
kept", approved by the operator on 2026-10-11 UTC.

We will build every site and the gallery with build.py, a small Python
generator, and Jinja2, its one templating library, with MarkupSafe as
Jinja2's own requirement; nothing else.
We will pin both to exact versions with the SHA-256 of every file PyPI
serves for them, so a tampered release cannot be installed.
We will run the build in GitHub Actions on every push to main, and publish
its output with GitHub Pages; a user installs nothing.
We will keep local builds working with the same commands
(docs/reference/commands.md).
We will commit nothing built: the output lives in _site/, which git
ignores.
We will hold each content fact once, in content/, and generate all markup
from it, and the build will refuse shortened text that is not a cut of its
source.

### Consequences

- Positive: a user's journey is a fork, three settings and an edit in the
  browser (docs/how-to/use-this-template.md).
- Positive: Jinja2 and MarkupSafe are installed by hash on every run.
- Negative: a build that depends on GitHub Actions stops when Actions does;
  a local build and a manual upload remain possible.
- Negative: the deploy job holds the right to publish; ADR-0006 keeps
  contributed files away from anything that runs there.
- Neutral: without committed output, the operator's site's rebuild gate
  becomes "the staged tree builds" (ADR-0008, gate B).

### Confirmation

**pip installs only the pinned files.** `python -m pip install -r
requirements.txt` in a fresh venv; `pip list --not-required` shows Jinja2
and pip only.

**Two builds are byte-identical.** `python tools/ci.py checks` builds the
site and the gallery twice each and compares every byte; a change that
makes the output depend on the clock or on file order fails it.

**Nothing built is committed.** Gate A refuses `_site/*` and `_gallery/*`
(tools/never-commit.txt).

**Live only:** a push to main publishes the site within one deploy run;
the setup steps end with that test.

## Pros and Cons of the Options

### Built by GitHub Actions

- Good: no install for users; one build for everyone.
- Bad: the build runs where publishing rights are held.

### Built locally, output committed

- Good: what is served is what was committed, and the operator's site has
  run it for weeks.
- Bad: every user needs Python, and every commit carries built files.

### A site framework

- Good: GitHub Pages builds Jekyll itself.
- Bad: gives up the engine, its content checks and its accessibility work,
  which are what the template offers.

## More Information

- The engine and the content model come from the operator's site, its
  ADR-0006, copied under its ADR-0012 (docs/reference/provenance.md).
- ADR-0010 records the one tool the workflows use beyond Python: Chrome,
  already on the runner.
- Revisit if the generator outgrows one templating library, or if GitHub
  Actions stops being free for public repositories.

## Changes
