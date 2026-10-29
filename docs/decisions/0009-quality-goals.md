---
status: accepted
topic: build
description: "The quality bar every site and every design meets: the accessibility checks of the standing list, and Core Web Vitals goals under Lighthouse's default mobile run. Read before adding a check, a heavy element or a design rule."
date: 2026-10-12
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0009: Quality goals, for every site and every design

## Context and Problem Statement

The strategy the operator adopted says what will impress a reader is how
the repository is run: "clear docs, working checks, accessibility
verified". His site sets its bar in two records: performance as Core Web
Vitals goals rather than a byte figure (its ADR-0009), and accessibility
proven by checks that each fail on a case built to defeat them (its
standing checks). Here the same bar must hold for designs the owner did
not write, and must be checkable on GitHub's runners as well as locally.

## Decision Drivers

- The strategy, adopted 2026-10-11.
- His site's ADR-0009, its condition on layout skipping, and its standing
  checks.
- Research 0005 of his site: none of nine template and gallery projects
  surveyed checks accessibility or performance.

## Assumptions

- A1. Google's "good" thresholds are LCP within 2.5 s, CLS at most 0.1 and
  INP at most 200 ms at the 75th percentile; Total Blocking Time under
  200 ms is the lab proxy. **Sourced**: web.dev, read 2026-10-02 by the
  operator's site (its ADR-0009).
- A2. The NVDA model of words run together reproduces a known-bad page.
  **Measured** 2026-10-12: on the operator's site at 6812c4f, the model
  here finds 58 joins at 360 px and 43 at 1366 px (his record: 58 and 45,
  with the widths the other way round), and 0 and 0 at c97b99e, the fix.

## Considered Options

- The standing checks and Core Web Vitals goals, for every design
- Automated rules only (axe), no tree or keyboard checks
- Review by eye

## Decision Outcome

Chosen option: "The standing checks and Core Web Vitals goals, for every
design".

We will hold every design to the checks in
docs/reference/standing-checks.md, each proven by its defeat case: the
accessibility tree at load matching the page without layout skipping,
keyboard through every panel, no words run together, anchors, the same
words as the page with no design, no request to another origin, nothing
moving under reduced motion.
We will hold every site to LCP within 2.5 s, CLS at most 0.1 and TBT under
200 ms, each the median of five Lighthouse default mobile runs.
We will run the checks that need no new dependency in CI on every pull
request, and the rest locally until their records are accepted (ADR-0011,
ADR-0012).

### Consequences

- Positive: a design is accepted on measured accessibility, not on looks.
- Negative: the browser checks take minutes per design on a runner.
- Negative: until ADR-0011 and ADR-0012 are accepted, contrast and speed
  are checked locally by the maintainer, not by CI.

### Confirmation

**Each standing check fails on its defeat case.** The session log of
2026-10-12 records each.

**Lighthouse medians meet the goals.** Recorded with their date and
machine in CAPABILITIES.md.

## Pros and Cons of the Options

### The standing checks for every design

- Good: what the operator's site verified, extended to contributions.
- Bad: slow, and the tree check needs Chrome.

### axe only

- Good: one tool, fast.
- Bad: misses what the site's own history found: a hidden panel read
  aloud, words run together.

### By eye

- Good: no tooling.
- Bad: against the strategy; nothing a reader can check.

## More Information

- His site's ADR-0009 Changes, 2026-10-06: a fail on any measuring machine
  is a fail.

## Changes

| Date | Change | Why |
|---|---|---|
| 2026-10-15 | **Accepted** by the owner, unchanged. With ADR-0011 accepted the same day, contrast is checked in CI by axe-core; Consequences' "until ADR-0011 and ADR-0012 are accepted, contrast and speed are checked locally" now holds for speed only, while ADR-0012 is proposed. | His answer 7 to the seat's report of 2026-10-13, checked with the portfolio architecture chat. |
| 2026-10-28 | **No page scrolls sideways**, a standing check in tools/check_browser.py for every design: at 320, 360 and 390 px, at 1080 by 1920 and at 1366 px, every section laid out, scripts on and off. | Poster in Round 14 and Sentinel in Round 15 scrolled sideways on a phone, found only by eye; the seat recommended the check in Report 14, and the owner approved building it on 2026-10-28 UTC. |
| 2026-10-29 | **Speed is checked in CI** on each page a change alters, ADR-0012 accepted. The goals are unchanged; in CI, LCP and CLS fail over them, and TBT over its goal is reported and fails over 600 ms, since TBT follows a shared runner's load (ADR-0012, Changes). | The owner's instruction of 2026-10-29 UTC: "the things that are pending such as the lighthouse is your end of work so if you can do it now then do it"; his choice the same day, after the seat put TBT's variance to him: "do recheck that specific part otherwise i choose option A as long as you weigh in the cons properly". |
