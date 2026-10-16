---
status: accepted
topic: process
description: "The scope floor, six lines: what this template and every design will never do. Read before proposing any feature, dependency or design rule."
date: 2026-10-11
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0001: The scope floor

## Context and Problem Statement

This repository is a portfolio-site template that anyone may copy, and a
gallery of designs that anyone may contribute. Each copy publishes a
person's site under their name, and each contributed design changes what
every user of it publishes. Two forces pull against each other. A template
grows by adding what users ask for: analytics, comment boxes, a contact
form, animations, a framework. And every such addition is something a user
inherits without choosing it, and something a contributor can use to reach
every visitor of every site that adopts a design.

A floor written before the first feature is cheaper than one found by a
reviewer, and any reviewer asked to harden or extend a template proposes
crossing it within a few turns.

## Decision Drivers

- The operator's priority, 2026-10-10: credibility through how the
  repository is run, over stars.
- The operator's condition on the build, 2026-10-11: "have to make sure
  that rules are being followed and no malware or things like that."
- His site's own floor (its ADR-0004), from which these lines descend.

## Assumptions

- A1. A user's site is read by employers and admissions readers who judge
  it partly by whether it respects them: no tracking, no pop-ups, readable
  without scripts. **Stated** by the operator through his site's floor,
  carried here by the brief of 2026-10-11.
- A2. Six lines are enough for a template; the other eight lines of his
  site's floor govern one person's claims, not a template's behaviour.
  **Stated** by the operator, who approved this floor on 2026-10-11 UTC.

## Considered Options

- The six lines below
- His site's fourteen lines, carried whole
- No written floor; judge each proposal as it comes

## Decision Outcome

Chosen option: "The six lines below", approved by the operator on
2026-10-11 UTC.

We will ship no personal content of the owner's beyond a credit line: the
template carries sample content only, fictional and obviously so.
We will add no cookies, tracking, analytics or requests to another
origin, in anything the template or a design ships.
We will put every word a reader needs in the initial HTML; scripts only
enhance.
We will use no paid service.
We will add no dependency without a record.
We will accept a contributed design as templates and CSS only, with no
JavaScript (ADR-0006, accepted 2026-10-15, narrows this to CSS only).

### Consequences

- Positive: a user inherits a site that collects nothing and works without
  scripts, and a contributor cannot use a design to reach visitors.
- Positive: a proposal that crosses a line is refused by naming the line,
  without re-arguing it.
- Negative: features users of other templates expect, such as a contact
  form or visit counts, will not be offered.
- Neutral: removing a line takes its own record, not an exception granted
  in passing.

### Confirmation

**The built pages request nothing from another origin.**
tools/check_built.py and the requests check of tools/check_browser.py;
each fails on a planted request to another origin.

**Every word is in the initial HTML.** The content trace reads the built
HTML, not the content files; the words check of tools/check_browser.py
compares every design with scripts off.

**No dependency is added without a record.** requirements.txt lists Jinja2
and MarkupSafe only, each with ADR-0004; the workflows install nothing
else. Review of every pull request.

**Sample content only.** The pre-publish search for the owner's name, run
before publication (ADR-0005), passes only for LICENSE and README.md.

## Pros and Cons of the Options

### The six lines below

- Good: short enough to carry into every brief; each line names behaviour a
  check can test.
- Bad: lines 1 and 6 depend on review as much as on checks.

### His site's fourteen lines

- Good: already proven on his site.
- Bad: eight of them govern one person's claims and would bind every user's
  content.

### No written floor

- Good: no up-front work.
- Bad: every proposal is argued from scratch, and the template drifts
  toward whatever was asked last.

## More Information

- Restated in CLAUDE.md, which governs; each line names this record.
- ADR-0006 narrows line 6 to CSS only, as a recommendation the operator is
  asked to confirm.
- Revisit only with a record that names the line it removes.

## Changes

| Date | Change | Why |
|---|---|---|
| 2026-10-15 | Line 6's note updated: ADR-0006, accepted by the owner on 2026-10-15, narrows "templates and CSS only" to CSS only. The note read "pending the operator's answer". The floor line itself is unchanged. | The owner's answer 1 to the seat's report of 2026-10-13, checked with the portfolio architecture chat: "Designs are CSS only. Keep it as built." |
