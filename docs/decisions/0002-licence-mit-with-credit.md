---
status: accepted
topic: process
description: "The licence: MIT. Credit asked for in the README, and a footer link to this project on by default, which a user may turn off. Read before changing the licence, the credit or the footer."
date: 2026-10-11
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0002: MIT licence, with credit asked and a removable footer link

## Context and Problem Statement

A template is only useful if people may copy it, and a gallery only grows
if people contribute to it. The licence decides both. A permissive licence
lets anyone use, change, share and sell the code; a restrictive one keeps
more control and turns more people away. The operator also wants credit
for the work, and a code licence can require only that its notice stays in
the code, not that a site shows anything.

## Decision Drivers

- The operator's priority, 2026-10-10: interaction, forks and pull
  requests over control, "even if later they sell the repo"; and "i do not
  want a license that scares away people".
- His site's research 0004 and its addendum, 2026-10-10: MIT fits that
  priority and PolyForm Noncommercial does not.
- GitHub's Terms of Service, section D.6: content added to a repository
  with a licence is licensed under the same terms, so contributions need
  no separate agreement.

## Assumptions

- A1. Less restrictive licences draw more interest. **Sourced**: Stewart,
  Ammeter and Maruping, Information Systems Research 17(2), 2006, read
  from its abstract in his site's research 0004.
- A2. MIT's only condition is that the copyright and licence notices stay
  with copies; it cannot require a visible credit. **Sourced**:
  choosealicense.com, read 2026-10-07 (research 0004).
- A3. The MIT copyright line names the owner by his name. **Stated** by the operator's site's ADR-0012, Changes row of
  2026-10-12, which allows his name in exactly two places here: this line
  and the README's credit.

## Considered Options

- MIT, credit asked in the README, a footer link on by default
- PolyForm Noncommercial
- CC BY 4.0 for the whole repository
- No licence

## Decision Outcome

Chosen option: "MIT, credit asked in the README, a footer link on by
default", decided by the operator on 2026-10-11 UTC: "MIT it is, as long as
it yields the best of results and portfolio chat does not say anything
against this." His site's architecture chat agreed on 2026-10-12, which
meets that condition.

We will license this repository under the MIT licence, with the owner's
copyright line.
We will ask for credit in the README, as a request, not a condition.
We will put a "Built with portfolio-gallery" link in every site's footer
by default, and let a user turn it off with one setting, `credit` in
content/config.json.
We will accept contributions under the same licence, as GitHub's terms
provide, and say so in CONTRIBUTING.md.
We will keep the fonts and other assets a design ships under their own
licences, each named in the design's design.json, with the licence text
beside each font.

### Consequences

- Positive: nothing in the licence turns a user or a contributor away.
- Positive: the footer link gives visible credit on every site that keeps
  it, which a fork alone does not.
- Negative: anyone may sell a copy, and the credit can be removed.
- Neutral: his name appears in this repository in exactly two places.

### Confirmation

**LICENSE is the MIT text with the copyright line.** Read it.

**The footer link renders by default and goes when turned off.** Build
with `credit` true and false; the link is present, then absent. Not yet a
standing test; recorded in STATE.md.

**His name appears only in LICENSE and README.md.** Gate A refuses it
anywhere else on the maintainer's machine (.git/info/never-commit), and the
pre-publish search confirms it before publication.

## Pros and Cons of the Options

### MIT with credit asked

- Good: the licence the most-used templates carry (research 0004: three of
  five MIT).
- Bad: credit is a request.

### PolyForm Noncommercial

- Good: keeps commercial use.
- Bad: not open source, and its line between commercial and not is unclear
  for a job-seeker's portfolio.

### CC BY 4.0

- Good: requires credit.
- Bad: Creative Commons recommends against its licences for software.

### No licence

- Good: no work.
- Bad: copiers get no permission at all.

## More Information

- Evidence: the operator's site, docs/research/0004, section 2 and its
  addendum; its ADR-0012 and Changes rows of 2026-10-10 and 2026-10-12.
- Revisit if the operator decides to require credit, which needs a
  different licence and a new record.

## Changes

| Date | Change | Why |
|---|---|---|
| 2026-10-15 | **The README's credit links his portfolio site**, https://waqas01cp.github.io/, beside the link to his GitHub profile. His name stays in LICENSE and README.md alone. | The owner's answer 4 to the seat's report of 2026-10-13, checked with the portfolio architecture chat. |
| 2026-10-15 | **The Code of Conduct's contact for reports is a dedicated address of his**, in CODE_OF_CONDUCT.md and nowhere else, replaceable later by an ordinary commit. His two personal addresses stay barred everywhere. Gate A and the pre-publish search allow the address in that file alone and refuse it, and the surname it holds, anywhere else (ADR-0008, Changes). The repository stays on his personal account. | The owner's answer 5 to the seat's report of 2026-10-13, checked with the portfolio architecture chat. GitHub's private content reports reach maintainers only in organisation-owned repositories (the seat's report, from GitHub's documentation, 2026-10-12), so a personal repository needs a written contact. His site's ADR-0012 allows the address in CODE_OF_CONDUCT.md alone, in its Changes row dated 2026-10-16, his local date (committed 2026-10-15 22:56 UTC), read by this seat at his site's a8f1da0. |
| 2026-10-18 | **Commits made on GitHub's website carry his profile's name.** An edit or a merge there is authored with his GitHub profile's name and his no-reply address; GitHub sets them, not a file. Pull requests 1 to 5 of the setup tests already carry it, and pull request refs cannot be deleted. The rule of two places covers files; the author name of a website commit or merge is his profile's name. The pre-publish search allows it there alone, with his no-reply address. | The portfolio architecture chat, 2026-10-18, from GitHub's API; confirmed by this seat the same day: pull requests 1 to 5, each commit authored with the no-reply address and committed by GitHub. |
| 2026-10-19 | **The footer credit names the design and its author**: "Built with portfolio-gallery, design <name> by <author>", the project and the author each linked, on by default and removable by config.json's credit, as before; the MIT licence asks only that LICENSE stays, and use-this-template.md asks politely that the credit stays. check_built.py refuses a credit without both links; the content trace takes the design's name and author as interface text. **His name may also appear in his own showcase entry, showcase/waqas01cp/entry.json, and on its card in the built gallery**, and his site in an in_use link; what a copy receives holds his name only in LICENSE, which MIT requires, and the cleaned-copy check proves the showcase and every in_use go. Gate A's private list and the pre-publish search allow exactly that. | The owner's decision D2 of 2026-10-18 and his answer Q3 of 2026-10-19, through the portfolio architecture chat (ADR-0016; ADR-0001, Changes). |
