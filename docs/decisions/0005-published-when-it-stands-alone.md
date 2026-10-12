---
status: accepted
topic: process
description: "This repository is published only once it stands on its own, by the owner himself, from written click-by-click steps, after a review and a search for his personal content. Read before anything that would publish, push or create a remote."
date: 2026-10-11
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0005: Published only once it stands on its own

## Context and Problem Statement

Anything committed to a public repository cannot be deleted: it stays in
the history and in every clone. This repository is built from the engine
of the operator's own site, which holds his content, his private checks
and his workflow. A first push that carries a trace of any of it, or an
engine that does not yet work for a stranger, cannot be taken back. Being
early has a cost too: the gallery and the credibility it is for start
only once it is public.

## Decision Drivers

- The operator's decision of 2026-10-10: "once it can stand on its own then
  i initialize a dedicated chat for it."
- His site's ADR-0012 Confirmation: before a copy of the engine is
  published, it is searched for his name, his email, his master CV's text
  and gate A's digest.
- The Working Method: a public commit cannot be deleted.

## Assumptions

- A1. Settings such as the ruleset, the Actions approval level and the
  Pages source are set after the repository exists and before the first
  outside pull request. **Sourced**: GitHub Docs pages read 2026-10-12, as
  docs/setup-on-github.md cites.

## Considered Options

- Built locally until it stands on its own, then published by the owner
- Published early and built in public

## Decision Outcome

Chosen option: "Built locally until it stands on its own, then published
by the owner", approved by the operator on 2026-10-11 UTC.

We will build this repository locally, with no remote and no push, until
it stands on its own.
We will publish it only by the owner's own hand, following
docs/setup-on-github.md, after his site's architecture chat has checked
those steps.
We will run the pre-publish search of his site's ADR-0012 before the first
push, and publish only if it finds his name in LICENSE and README.md
alone, and his email, his master CV's text and gate A's digest nowhere.
We will let no seat create a remote, push, or create the repository.

### Consequences

- Positive: nothing private and nothing broken reaches a public history.
- Negative: the workflows cannot run before the first push; they are
  checked locally as files, and proven by a test pull request after.
- Neutral: the architecture chat for this repository starts once it is
  public.

### Confirmation

**No remote exists before publication.** `git remote -v` prints nothing.

**The pre-publish search passes.** Its commands and result are in the
session log and in the seat's report; the master CV part is run by the
operator's site's implementing seat.

**Live only:** the setup steps end with a test pull request that shows each
workflow running on GitHub.

## Pros and Cons of the Options

### Built locally, then published

- Good: the history starts clean and the engine works on day one.
- Bad: the workflows are unproven until after the first push.

### Built in public

- Good: workflows run from the first day.
- Bad: every mistake is permanent.

## More Information

- docs/setup-on-github.md holds the steps; the operator follows them only
  after the architecture chat has checked them (the brief's Addendum 1).
- Revisit never: once published, this record is history.

## Changes
