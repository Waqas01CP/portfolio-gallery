---
status: accepted
topic: content
description: "A template may be shown in the gallery with its own invented person, one of the profession it suits, from samples/<design>/, a whole content folder held to the same build rules and content trace as content/. Every other template, and every user's site, keeps one content folder for all designs. Read before adding or changing a sample person, or a template made for a profession."
date: 2026-10-24
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0018: A template shown with its own sample person

## Context and Problem Statement

Every design styled the same page with the same sample person, Alex
Example, a junior software engineer, in every demo of the gallery. On
2026-10-24 UTC the owner judged the five designs of Round 14 to read
mostly as look-alikes, and asked for new ones, each for a professional in
a tech field (cybersecurity, AI and ML, mobile development, QA,
DevOps), clearly distinct from each other and not modelled on his own
taste. A design is CSS only on fixed HTML (ADR-0006; scope floor line 6)
and may not add words, so a template made for a security analyst would
still show a junior software engineer's page. How can a template read as
its profession's site?

## Decision Drivers

- His request of 2026-10-24 UTC, in this repository's implementing
  session: distinct designs, each for a profession, with variety over his
  own taste.
- A user's own site is built from their own content, in whatever design
  they pick; that must not change.
- Every fact a page shows traces to a CV (ADR-0009's standing checks; the
  content trace), sample content included; sample content is fictional
  and obviously so (scope floor line 1).
- No new dependency, and nothing a contributor's design must now carry.

## Assumptions

- A1. A design cannot make a page read as another profession's by CSS
  alone, because the words are the content's. **Measured**: the words
  check refuses any design that adds or hides text (tools/check_browser.py,
  words), and Round 14's five, each in its own style, all showed Alex
  Example's headline and projects.
- A2. A content folder is enough to describe another person: config.json,
  cv.md, site.json and items.json, as content/ holds them. **Measured**:
  build.py --content builds a sample person's whole site from one, and
  check_content.py --content traces it to that person's CV (2026-10-24).
- A3. Users never build the gallery; a copy of the template builds only
  its own site, from content/. **Measured**: Deploy builds the gallery only
  where PORTFOLIO_GALLERY is set (ADR-0016), and the cleanup removes
  samples/ from a copy (tools/check_template_cleanup.py).

## Considered Options

- Its own sample person, from samples/<design>/
- The same sample person for every design, the profession shown by look
  alone
- Its own sample person and sections of its own, such as CTFs or
  publications, by changing the engine's page and content model

## Decision Outcome

Chosen option: "Its own sample person, from samples/<design>/", decided by
the owner on 2026-10-24 UTC (2026-10-25 in his local time), choosing it from the three above when the
implementing seat asked, as the seat recommended.

We will let a template be shown in the gallery with its own invented
person: samples/<design>/ holds config.json, cv.md, site.json and
items.json, a whole content folder whose config names that design.
We will build that design's demo from it, with its own generated layout
beside the demo (designs/<design>/layout.css in the gallery), and every
other demo from content/, as before.
We will refuse a sample for a design that does not exist, one that names
another design, and one that is not a whole content folder (build.py), and
hold each sample to the content trace against its own CV, building that
person's own site in CI as a user's is built (tools/ci.py checks).
We will name, on each gallery card, the person a template is shown with.
We will remove samples/ from every copy of the template.

### Consequences

- Positive: a template made for a profession is shown as that
  profession's site, so the gallery reads as variety rather than one page
  restyled.
- Positive: a user changing designs still keeps their own content; a
  sample is also a worked example of a whole content folder.
- Negative: each sample is one more CV and two content files to keep true
  to each other, and one more site built and traced on every run.
- Neutral: designs contributed by others are shown with content/, as
  before; samples/ is outside the folder a contributor's pull request may
  change (tools/scope_check.py), so samples stay the project's.

### Confirmation

tools/prove_checks.py: a sample for a design that does not exist, and one
naming another design, fail the build; a sample person's fact not in
their CV fails the content trace; a gallery demo shown with its own
sample person builds and passes check_built.py (a planted control).

## Pros and Cons of the Options

### Its own sample person

- Good: each profession's template shows a page of that profession.
- Good: no change to the design format or the engine's HTML.
- Bad: sample content to write and keep traced, per template.

### The same sample person

- Good: nothing new to build.
- Bad: every demo shows the same junior software engineer, so the
  templates read alike, which is what the owner asked to fix.

### Own sections too

- Good: the closest match to each profession.
- Bad: changes the engine's page and content model for every site and
  every design; the largest change, likely two rounds or more.

## More Information

- Asked and answered in the implementing session on 2026-10-24 UTC; the
  session log, Round 15, carries his words.
- Revisit if a profession needs a section the content model lacks.

## Changes
