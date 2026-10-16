---
status: accepted
topic: design
description: "The default design keeps the look of the owner's own site, credited to Waqas01CP as its author, so a site made from the template unchanged looks like his. Read before changing the default design, its credit or the design a new site starts with."
date: 2026-10-15
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0013: The default design keeps the owner's site's look

## Context and Problem Statement

The engine was copied from the owner's site, and its stylesheet became the
`default` design (docs/reference/provenance.md). `default` is the design
content/config.json names, so every site made from the template looks like
his until its user picks another design, and the gallery's first card is
his work. Should `default` keep that look, take a look of its own, or
should his look leave the repository?

## Decision Drivers

- The brief's Addendum 1 asked for his look as the default, and for his
  answer to this question.
- ADR-0005's context: the gallery is for the owner's credibility as well
  as for its users.
- A user of the template should get a finished, checked design on the
  first build.

## Assumptions

- A1. The default design's stylesheet is the owner's own work, from his
  site's stylesheet at 5f3b84d, published here under this repository's MIT
  licence. **Stated** by the owner: MIT for this repository (ADR-0002), and
  his answer 2 of 2026-10-15 keeping his look here.
- A2. Its three fonts are under the SIL Open Font License and reserve no
  name. **Measured**: each WOFF2 file's name table and each licence text,
  read 2026-10-12 (docs/reference/provenance.md).
- A3. The design passes every standing check, axe included. **Measured**:
  tools/ci.py checks and axe-core 4.14.0, 2026-10-12, 13 and 15 (the
  session log).

## Considered Options

- Keep his look as `default`, credited to Waqas01CP
- Give `default` a look of its own, and keep his under another name
- Leave his look out

## Decision Outcome

Chosen option: "Keep his look as `default`, credited to Waqas01CP",
decided by the owner on 2026-10-15 UTC: "The default design keeps the
look of his site, credited to Waqas01CP as its author."

We will keep `default` as the look of the owner's site, with `author`
Waqas01CP in its design.json, shown on its gallery card and in its demo's
footer.
We will keep `default` as the design content/config.json names, so a new
site starts with it.
We will maintain it as the project's own design: the scope check refuses a
contributor's change to it (tools/scope_check.py).

### Consequences

- Positive: the template's first build is a finished design that passes
  every check.
- Positive: the gallery opens with his own work, credited to his handle.
- Negative: a site made from the template unchanged looks like his, and a
  visitor may take one for the other. The footer's credit line, on by
  default, names this project, not him.
- Neutral: his name does not appear with it; the credit is his handle
  (ADR-0002).

### Confirmation

**The default design is credited to Waqas01CP.** designs/default/
design.json's `author` is `Waqas01CP`; the built gallery's Default card
and the demo's footer show it.

**A new site starts with it.** content/config.json's `design` is
`default`.

## Pros and Cons of the Options

### His look as default

- Good: finished and checked; shows his work first.
- Bad: sites made from the template look like his until changed.

### A look of its own

- Good: sites made from the template would not look like his.
- Bad: a new design to make and check before publishing.

### Leave his look out

- Good: no site is mistaken for his.
- Bad: the gallery loses its most complete design.

## More Information

- Asked in the seat's report of 2026-10-13, question 6.2; answered on
  2026-10-15 UTC, in answers dated 2026-10-16 in his local time.
- Revisit if sites made from the template are mistaken for his.

## Changes
