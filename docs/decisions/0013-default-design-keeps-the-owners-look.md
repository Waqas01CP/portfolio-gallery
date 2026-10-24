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

| Date | Change | Why |
|---|---|---|
| 2026-10-24 | **Every design the owner commissions is credited to him, and the project maintains it.** Plain's author, "portfolio-gallery" since 2026-10-12 (the implementing seat's choice; no record decided it), becomes Waqas01CP, with his GitHub profile as author_url, as Default's is. Five more designs of his join the Templates, each credited to Waqas01CP: Bento, Broadsheet, Console, Poster and Signal. All seven are in tools/scope_check.py's MAINTAINED, so a contributor's change to one is refused and proposed in an issue; a design dropped from designs/ leaves that list too. tools/check_built.py now refuses a footer credit whose author link is the project's own address, with a defeat case: Plain's old credit. His designs are built to two bars of his: each looks finished and deliberate (simple is allowed, unfinished is not), and any two differ in at least three of five dimensions (layout and structure; type; colour palette; shapes and ornament; density and rhythm), always in layout or palette. | The owner's decision of 2026-10-24 and his two additions of that date, through the portfolio architecture chat's Brief 14; the five dimensions are the chat's way of making his "at least 40-50%" checkable. Maintaining the five, as Default and Plain are, is the implementing seat's call, which the brief left to it; reported in Report 14 for him to overrule. |
| 2026-10-24 | **Five more designs of his, each made for a profession**: Assert (QA and testing), Latent (machine learning), Pipeline (DevOps and cloud), Pocket (mobile) and Sentinel (security), each credited to Waqas01CP and in tools/scope_check.py's MAINTAINED, as the row above sets for every design he commissions. Each is shown in the gallery with its own invented person of its profession (ADR-0018). They are held to his two bars and to his request of the same day: clearly distinct from each other and from the seven before them, and not modelled on his own taste. | The owner's request of 2026-10-24 UTC in the implementing session, after judging Round 14's five as mostly look-alikes; his answers of the same day, five designs for those professions, each with its own sample person. |
