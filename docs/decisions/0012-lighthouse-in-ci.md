---
status: proposed
topic: build
description: "Proposed, awaiting the owner's approval: run Lighthouse in CI against ADR-0009's speed goals, installed from a committed lockfile. Until accepted, Lighthouse runs only locally. Read before adding Lighthouse to a workflow."
date: 2026-10-12
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0012: Lighthouse in CI (proposed)

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
