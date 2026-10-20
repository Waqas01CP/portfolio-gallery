---
status: accepted
topic: build
description: "The gallery's previews and the browser checks use the Google Chrome already on the runner, driven over its DevTools protocol by Python's standard library: no package added. Screenshots are taken in a job that holds no write token. Read before changing the screenshots, the browser checks or the deploy workflow."
date: 2026-10-12
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0010: Headless Chrome, driven from Python's standard library

## Context and Problem Statement

The brief requires the deploy workflow to take each design's preview with
headless Chrome on the runner, and the standing checks need a browser.
The operator's site drives Chrome through puppeteer-core in its session's
scratch space, which is not its dependency. Here the browser runs in CI,
so whatever drives it is a dependency (ADR-0001 line 5). Chrome itself is
on GitHub's runner. A browser also parses contributed fonts and images, so
the job that runs it should not be the job that can publish.

## Decision Drivers

- ADR-0001 line 5; ADR-0004; ADR-0006.
- The brief: previews by headless Chrome, never supplied by a contributor.

## Assumptions

- A1. Google Chrome 154 is on the Ubuntu 24.04 runner. **Sourced**:
  actions/runner-images, Ubuntu2404-Readme.md, image 20261004.327.1, read
  2026-10-12.
- A2. Chrome's DevTools protocol is reachable over a WebSocket on
  127.0.0.1 when started with --remote-debugging-port=0, writing the port
  to DevToolsActivePort in its profile. **Measured** 2026-10-12, Chrome
  154.0.8037.98 on Windows: tools/cdp.py connects, captures WebP
  screenshots and reads the accessibility tree.
- A3. Ubuntu 24.04 restricts the user namespaces Chrome's sandbox uses, so
  Chrome may need --no-sandbox there. **Not verified**: the workflows set
  PG_CHROME_NO_SANDBOX=1 only in jobs that hold no write token, and the
  first run on GitHub shows whether it is needed.

## Considered Options

- Chrome over the DevTools protocol, from Python's standard library
- puppeteer-core from npm
- Chrome's own --screenshot flag, and no browser checks in CI

## Decision Outcome

Chosen option: "Chrome over the DevTools protocol, from Python's standard
library".

We will drive the Chrome already on the runner, or on the user's machine,
with tools/cdp.py: a WebSocket client and the protocol's JSON, in the
standard library, each Chrome with a fresh profile in a temporary folder.
We will add no package for it.
We will take the gallery's previews in a job of their own, with only
contents: read, and publish nothing from it but WebP files at
designs/<name>/preview.webp, each checked (tools/ci.py assemble).
We will run the browser checks on every design in CI, on pull_request,
with a read-only token.

### Consequences

- Positive: no npm tree to pin, audit or update.
- Positive: a font crafted against Chrome cannot reach the job that
  publishes.
- Negative: tools/cdp.py is ours to maintain; the protocol changes slowly
  but does change.
- Neutral: users who want the browser checks locally need Chrome, which is
  found or named by PG_CHROME.

### Confirmation

**A missing Chrome is a refusal.** PG_CHROME set to a missing file; the
tools exit 1 naming it.

**The assemble step refuses anything but previews.** A shots folder holding
a .js file, or a preview over 300 KB; refused.

**Live only:** the deploy run's screenshot job produces one preview per
design and the published gallery shows them.

## Pros and Cons of the Options

### Standard library over the protocol

- Good: no dependency; one language for every check.
- Bad: a small protocol client to maintain.

### puppeteer-core

- Good: mature, widely used.
- Bad: an npm dependency tree in CI, each version a record.

### --screenshot only

- Good: no code.
- Bad: no control over reduced motion, size or format, and no browser
  checks in CI at all.

## More Information

- The protocol: chromedevtools.github.io/devtools-protocol.
- Revisit if the protocol client grows past a few hundred lines, or if a
  maintained package offers the same with fewer risks.

## Changes

| Date | Change | Why |
|---|---|---|
| 2026-10-15 | **Accepted** by the owner, unchanged. | His answer 7 to the seat's report of 2026-10-13, checked with the portfolio architecture chat. |
| 2026-10-20 | **Chrome also decodes contributors' screenshots**, to draw the showcase's served copies (ADR-0016, Changes, 2026-10-20): in the deploy's screenshot job, which holds no write token and whose pictures tools/ci.py assemble checks before publishing, and in the pull request's checks, which run the pull request's own code with a read-only token already. On the runner Chrome runs without its sandbox (PG_CHROME_NO_SANDBOX, A3), so a flaw in an image decoder would reach that job, and no further than its artifact. That Chrome runs with the GPU off: on the seat's machine, drawing a large capture with it on hung or came out blank. | The owner's decision of 2026-10-20 that the build makes the served copies; Chrome is the decoder already on the runner, and any other would be a dependency (scope floor line 5). |
