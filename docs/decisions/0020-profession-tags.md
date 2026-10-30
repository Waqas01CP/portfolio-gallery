---
status: accepted
topic: content
description: "Designs and showcase entries may name the professions they suit or work in, as ids from one list, src/professions.json; each gallery card shows them. Read before adding a profession, a filter, or a field to design.json or entry.json."
date: 2026-10-29
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0020: Profession tags on designs and showcase entries

## Context and Problem Statement

Ten of the seventeen designs are made for a profession and say so only in
their description ("For game developers: ..."); a showcase entry says
nothing of its author's work. The owner wants each profile to carry a
profession, so the gallery can later give it its own section or filter by
it. Free text would make "ML", "Machine learning" and "AI" three groups; a
filter needs one list.

## Decision Drivers

- The owner's approval of 2026-10-29 UTC: "the professional tag is
  approved and you can work on it".
- His rule for the checks' work, 2026-10-28: nothing breaks and no one is
  inconvenienced. An open pull request, a contributor's entry and every
  copy of the template must stay valid as they are.
- ADR-0001 line 3: every word a reader needs is in the initial HTML.

## Assumptions

- A1. Ten designs are made for a profession and seven for anyone.
  **Measured**: their descriptions, 2026-10-29.
- A2. The showcase holds two entries, one a contributor's. **Measured**:
  showcase/, 2026-10-29.
- A3. With two entries a filter would show mostly empty groups, so a label
  now and a filter later. **Stated by the owner**, 2026-10-29: tags "so
  later it can have its own sections or filtered".

## Considered Options

- An optional list of ids from one fixed list (chosen)
- Free text
- A required field

## Decision Outcome

Chosen option: "An optional list of ids from one fixed list", because a
fixed list makes groups a filter can trust, and an optional field leaves
every design, entry, pull request and copy valid as it is.

We will let design.json and a showcase entry's entry.json carry
`professions`: one to three ids from src/professions.json, each once.
Left out, the design suits anyone, or the entry names none.
We will keep one list, src/professions.json, mapping each id to the
label the gallery shows, fourteen to start: software, frontend, backend,
mobile, devops, security, ml, data, embedded, games, qa, devrel,
writing, design. The seat proposed them; the owner changes the list by a
pull request to that file.
We will hold the rule in tools/check_design.py, which reads the list,
and have tools/check_showcase.py take both from it, so a copy of the
template, which removes the showcase check, keeps them; and have
build.py refuse an id it has no label for.
We will show on each card "Profession:" or "Professions:" and the
labels, in the page's HTML.
We will tag the ten designs made for a profession and the two entries.

### Consequences

- Good: sections or a filter later read one field, with no text to parse.
- Good: nothing that exists becomes invalid.
- Bad: a profession not on the list needs the list changed first.
- Neutral: a design's description still says who it is for.

### Confirmation

Defeat cases in tools/prove_checks.py: in design.json, a profession not on
the list, the field as text, four, one twice and an empty list; in an
entry, one not on the list; the build refusing an id with no label.
Controls from the list pass in both.

## Pros and Cons of the Options

### An optional list of ids

- Good: one spelling per profession; checked.
- Bad: a new profession waits on a change to the list.

### Free text

- Good: anyone writes what they are.
- Bad: no two people write it the same way; no filter can trust it.

### A required field

- Good: every card tagged.
- Bad: every open pull request and every copy fails until it adds one,
  and a design for anyone has nothing true to name.

## More Information

- Sections or a filter by profession: not built. Either needs no script,
  by sections the build writes, or uses one only to enhance (ADR-0001
  line 3).
- The design format: ADR-0006. The showcase entry's format: ADR-0016.

## Changes

| Date | Change | Why |
|---|---|---|
| 2026-10-30 | **Form; nothing decided moves.** The Decision Outcome reworded as We will lines, its substance unchanged. | The architecture chat's review of ADR-0018 to ADR-0021, Brief 15, 2026-10-30 UTC. |
