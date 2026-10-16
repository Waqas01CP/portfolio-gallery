---
status: accepted
topic: process
description: "The repository gates: what each blocks, where it fires and the case built to defeat it. Generic forms of the operator's site's gates, with private patterns kept out of the repository. Read before building or changing a gate."
date: 2026-10-12
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0008: The repository gates

## Context and Problem Statement

The Working Method asks for gates before the first feature, each proven
able to fire. The operator's site has five (its ADR-0007), and this
repository may carry their generic forms but not their private ones, such
as gate A's digest of his vault's folder name (his site's ADR-0012). Two
things differ here. Nothing built is committed (ADR-0004), so a gate that
compares committed output with a fresh build has nothing to compare. And
the repository is public, so a pattern that names what must never be
committed would itself publish it.

## Decision Drivers

- The Working Method's four gates, and its rule that a gate which cannot
  fail is worse than none.
- His site's ADR-0007 and ADR-0012.
- ADR-0005: his name only in LICENSE and README.md; his email nowhere.

## Assumptions

- A1. Local hooks are enough on the maintainer's machine; GitHub enforces
  the rest through the ruleset and the workflows. **Stated** by the
  brief, which keeps his site's local-hook model and adds CI.
- A2. git never commits anything under its own folder, .git/.
  **Sourced**: git's documentation of the repository layout; relied on by
  .git/info/exclude.

## Considered Options

- Local hooks, with a local never-commit list in .git/info
- His site's gates copied with their private patterns
- CI only

## Decision Outcome

Chosen option: "Local hooks, with a local never-commit list in .git/info".

We will block, before each commit (gate A), CHAT_STATE.md at any path,
briefs/ but its README, every path tools/never-commit.txt lists, any
drive-letter absolute path or climb out of the repository in a staged text
file, and every private pattern in .git/info/never-commit, in staged text
and in the commit's author and committer.
We will refuse a commit whose staged tree does not build, or whose built
files fail their checks (gate B).
We will refuse a commit that leaves MAP.md stale or a Markdown header
GitHub cannot read (gate C).
We will treat a missing tool as a refusal, never a skip (gate D).
We will refuse a push of implementation work with no commit in the range
touching STATE.md (gate E).
We will prove each gate with the case built to defeat it before it counts.

### Consequences

- Positive: the owner's private names stay out of the history without
  being written into it.
- Positive: a commit that would break the deploy is caught before it is
  made.
- Negative: hooks live in the working copy; a fresh clone has none until
  `git config core.hooksPath .githooks`, and nothing catches the omission.
- Negative: gate B takes some seconds per commit.

### Confirmation

**CHAT_STATE.md is refused.** Stage it with -f; the commit is refused.

**A drive-letter path is refused.** Stage a file holding one; refused,
naming the file and line.

**A private pattern is refused, in a file and in the identity.** A planted
pattern in a file, and a commit under an identity holding one; both
refused.

**A staged tree that does not build is refused.** Stage a design with
@import; refused by gate B.

**A stale map is refused.** Stage a new Markdown file without
regenerating MAP.md; refused.

**A missing tool is refused.** Rename tools/generate_map.py; refused,
naming it.

**A push without STATE.md is refused; with it last, allowed.** Feed gate E
a range touching tools/ only, then a range whose last commit touches
STATE.md.

## Pros and Cons of the Options

### Local hooks with a local list

- Good: nothing private written into a public repository.
- Bad: each maintainer keeps his own list.

### His site's gates as they are

- Good: proven.
- Bad: would publish his private forms, which his ADR-0012 forbids.

### CI only

- Good: cannot be skipped.
- Bad: catches a private string only after it is pushed, when it can no
  longer be deleted.

## More Information

- Gates and their defeat cases: tools/gates.py; the proofs: the session
  log of 2026-10-12.
- Revisit when a second maintainer joins.

## Changes

| Date | Change | Why |
|---|---|---|
| 2026-10-15 | **Accepted** by the owner. | His answer 7 to the seat's report of 2026-10-13, checked with the portfolio architecture chat. |
| 2026-10-15 | **Gate A takes text allowed in a file out of each line before matching the other private patterns there.** So the Code of Conduct's address, allowed in CODE_OF_CONDUCT.md alone, does not count as the surname it holds, and the surname on its own is still refused in that file. Decision Driver "his email nowhere" now reads with the exception in ADR-0002's Changes row of this date. Defeat cases added: the address in another file, the surname beside the address in CODE_OF_CONDUCT.md, a commit under the address; control: the address in its own file passes. | The owner's answer 5 to the seat's report of 2026-10-13: the address in CODE_OF_CONDUCT.md only. Without this, gate A refused the address for the surname it holds. |
