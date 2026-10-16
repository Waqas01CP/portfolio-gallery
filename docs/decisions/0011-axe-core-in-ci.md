---
status: accepted
topic: build
description: "Run axe-core in CI on every design, fetched from npm by exact version and checked against its published SHA-512. Read before changing axe's version or how the checks workflow runs it."
date: 2026-10-12
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0011: axe-core in CI

## Context and Problem Statement

axe-core checks a rendered page against a set of WCAG rules, contrast
among them, which none of the other checks covers. The operator's site
runs it outside the repository, in a session's scratch space. Here the
check matters most for designs the owner did not write, which is where CI
runs. Run in CI, axe-core is a dependency, and scope floor line 5 requires
a record and the owner's approval before it is added.

## Decision Drivers

- ADR-0001 line 5; ADR-0009.
- tools/check_browser.py already runs axe when given the file (--axe).

## Assumptions

- A1. axe-core 4.14.0 is published on npm under MPL-2.0 with no
  dependencies, with a SHA-512 integrity value in the registry. **Sourced**:
  registry.npmjs.org/axe-core, read 2026-10-12; published 2026-10-05.
- A2. Using axe-core in CI without shipping it in any site puts no licence
  duty on this repository; MPL-2.0's duties attach to distributing its
  files. **Believed**, from MPL-2.0's text as commonly read; not checked
  with a lawyer.
- A3. axe finds a subset of accessibility failures and never proves their
  absence. **Sourced**: as the operator's site's research 0005 rates it.

## Considered Options

- axe-core in CI, fetched by version and checked by hash
- axe-core only locally, as the operator's site does
- axe-core's file committed into the repository

## Decision Outcome

Chosen option: "axe-core in CI, fetched by version and checked by hash",
decided by the owner on 2026-10-15 UTC.

We will fetch axe-core's npm tarball at one exact version in the checks
workflow, verify its SHA-512 against the value recorded in the workflow,
and pass axe.min.js to tools/check_browser.py with --axe.
We will run axe's default rules on every design at 360 and 1366 px, light,
device dark and switched dark, panels closed and open, and fail on any
violation.

### Consequences

- Positive: contrast and other WCAG rules are checked on every design pull
  request.
- Negative: one more download per run, and one version to keep current.

### Confirmation

**A page with faint text and an image without alt fails.** The defeat case
of the operator's site's standing checks, run here with --axe.

## Pros and Cons of the Options

### In CI, by hash

- Good: every contribution checked; nothing committed.
- Bad: a network fetch on each run.

### Locally only

- Good: no dependency.
- Bad: a contributor's design merges unchecked for contrast unless the
  owner runs it himself.

### Committed

- Good: no fetch.
- Bad: 600 KB of third-party code in the repository, under its own licence.

## More Information

- Until this record is accepted, the checks workflow does not run axe and
  says so. The seat ran axe-core 4.14.0 locally on 2026-10-13 UTC, from a
  scratch folder: 36 cells, both designs and the gallery page, 0
  violations; its defeat case (faint text and an image without alt in the
  plain design) reported image-alt in every cell and color-contrast in the
  light ones (session log).

## Changes

| Date | Change | Why |
|---|---|---|
| 2026-10-15 | **Accepted** by the owner, and built: the checks workflow fetches axe-core 4.14.0's tarball from the npm registry, checks it with sha512sum against the registry's integrity value, written in the workflow in hex, and passes axe.min.js to tools/ci.py checks --axe. The title, the description and Decision Outcome lose "proposed"; More Information's "Until this record is accepted" is history. A1 re-read 2026-10-15: the same version, MPL-2.0, no dependencies, the same integrity value. The defeat case is in tools/prove_checks.py, run with --browser --axe FILE. | His answer 7 to the seat's report of 2026-10-13, checked with the portfolio architecture chat. |
