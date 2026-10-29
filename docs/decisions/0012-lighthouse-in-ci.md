---
status: accepted
topic: build
description: "Accepted: Lighthouse runs in CI on each page a change alters, installed by npm ci --ignore-scripts from a committed lockfile; LCP and CLS fail over ADR-0009's goals, TBT over its goal is reported and fails over 600 ms. Read before changing the speed check, its limits or its dependency."
date: 2026-10-12
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0012: Lighthouse in CI

## Context and Problem Statement

ADR-0009 sets speed goals as Lighthouse medians. A design can break them
with heavy fonts or large images, so the place to measure is on each
design pull request. Lighthouse is an npm package with 28 direct
dependencies at 13.5.0, so in CI it is a dependency tree, not a file, and
scope floor line 5 requires a record and the owner's approval. A runner's
speed also varies, so a CI number is evidence of a regression, not a
measurement to compare with a phone.

## Decision Drivers

- ADR-0001 line 5; ADR-0009.

## Assumptions

- A1. Lighthouse 13.5.0 is published under Apache-2.0 with 28 dependencies.
  **Sourced**: registry.npmjs.org/lighthouse, read 2026-10-12; published
  2026-09-18.
- A2. Lighthouse results vary between machines, and the median of five is
  twice as stable as one run. **Sourced** by the operator's site's ADR-0009,
  from Lighthouse's variability documentation, read 2026-10-02.

## Considered Options

- Lighthouse in CI from a committed lockfile (proposed)
- Lighthouse only locally, as the operator's site does
- `npx lighthouse@version` with no lockfile

## Decision Outcome

Chosen option: "Lighthouse in CI from a committed lockfile", **proposed**,
for the owner's approval.

We will commit a package.json and package-lock.json for Lighthouse alone
under tools/lighthouse/, install them with `npm ci`, which checks every
package against the lockfile's hashes, and run five default mobile runs per
design against ADR-0009's goals.
We will report CI numbers as evidence of a regression, and keep the goals'
pass or fail on the maintainer's measurements as ADR-0009 sets.

### Consequences

- Positive: a design that makes the page slow is caught before review.
- Negative: an npm tree to keep current, and minutes per design per run.

### Confirmation

**A 600 ms synchronous script fails the TBT goal.** The operator's site's
defeat case; here, a scratch copy of site.js with a busy loop.

## Pros and Cons of the Options

### From a lockfile

- Good: every package checked by hash.
- Bad: the heaviest dependency the project would have.

### Locally only

- Good: no dependency.
- Bad: contributions are measured only when the owner runs it.

### npx without a lockfile

- Good: one line.
- Bad: transitive versions float; nothing pins what runs.

## More Information

- Until this record is accepted, the seat measures locally and records the
  numbers with their date and machine in CAPABILITIES.md.

## Changes

| Date | Change | Why |
|---|---|---|
| 2026-10-15 | **Held as proposed** by the owner. Lighthouse runs only locally. | His answer 7 to the seat's report of 2026-10-13, checked with the portfolio architecture chat. |
| 2026-10-29 | **Accepted** by the owner, and built. Lighthouse 13.5.0, the newest at least two weeks old (13.6.0 was two days old), in tools/lighthouse/: 114 packages, each from registry.npmjs.org with its hash in package-lock.json, none with an install script, installed by `npm ci --ignore-scripts`; Node 24 from actions/setup-node v7.1.0 at a full SHA. tools/check_speed.py runs the default mobile run five times on each page a job checks, in that page's own job; `tools/ci.py checks --speed` runs it locally. **Option A, the owner's**: a median LCP or CLS over ADR-0009's goal fails; a median TBT over 200 ms is reported in the run and its summary, and fails only over 600 ms. Why: TBT follows the machine's load (Bento's demo measured 298 ms with this machine busy, then 59 and 25 ms with it quieter, nothing else changed), GitHub's runners are shared, and a design, CSS only, cannot move it. Weighed against it: a rise between 200 and 600 ms passes unblocked; only the engine's own script can cause one, a change this seat makes and must read the speed table for; the ceiling is lowered towards 200 once the weekly runs show GitHub's margin. LCP and CLS barely moved with load. The numbers CAPABILITIES records stay the maintainer's measurements, as decided. tools/check_workflows.py now refuses an action not at a full commit SHA, and npm run any way but `npm ci --ignore-scripts`. Confirmation met: a 600 ms script once the page has loaded fails on TBT (run as the script starts, it lands before the first paint and fails LCP instead); a 100 ms one is reported and passes; a 3 MB stylesheet fails LCP; the page moved down after it loads fails CLS; Plain's demo as built passes. | The owner's instruction of 2026-10-29 UTC: "the things that are pending such as the lighthouse is your end of work so if you can do it now then do it"; his choice the same day, after the seat put TBT's variance to him: "do recheck that specific part otherwise i choose option A as long as you weigh in the cons properly". |
