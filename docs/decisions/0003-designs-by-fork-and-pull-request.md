---
status: accepted
topic: process
description: "How designs arrive: each as one folder under designs/, from a contributor's fork, by pull request, checked automatically and merged only by the owner. No contributor branches here. Read before changing how contributions are taken."
date: 2026-10-11
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0003: Designs arrive as folders, by fork and pull request

## Context and Problem Statement

The gallery shows designs other people make, and each must reach this
repository somehow. The operator first described contributors having
"their own branch (or whatever is the best approach)" (2026-10-10). The
ways differ in who needs write access, whether a contribution stays in
step with fixes to the engine, whether a visitor can see it, and what
GitHub Pages can publish, which is one branch.

## Decision Drivers

- The operator's words, 2026-10-10: "the gallery showcases different and
  people can use them or push their own".
- His condition of 2026-10-11 that rules are followed and nothing harmful
  gets in.
- GitHub Pages publishes one branch or one workflow's artifact.

## Assumptions

- A1. A contributor needs no permission to push to their own fork.
  **Sourced**: GitHub's documentation of the fork-and-pull model, "You do
  not need permission from the upstream repository to push to a fork you
  created", read 2026-10-10 (the brief).
- A2. A pull request from a fork runs its `pull_request` workflows with a
  read-only token and no secrets. **Sourced**: GitHub Docs, Events that
  trigger workflows, "Workflows in forked repositories", read 2026-10-12:
  "The `GITHUB_TOKEN` has read-only permissions in pull requests from
  forked repositories."

## Considered Options

- One folder per design, by fork and pull request
- A branch per contributor in this repository
- Designs hosted elsewhere and listed here by link

## Decision Outcome

Chosen option: "One folder per design, by fork and pull request",
approved by the operator on 2026-10-11 UTC.

We will take each design as one folder, designs/<name>/, added on a branch
of the contributor's own fork and proposed by pull request.
We will give no contributor a branch, or write access, in this repository.
We will check every design pull request automatically (ADR-0006), and the
owner will review and merge each one himself.
We will build every merged design into the gallery from the same commit as
the engine, so every design always runs on the current engine.

### Consequences

- Positive: strangers need no access; the owner's merge is the gate.
- Positive: the gallery always shows every design on the current engine.
- Negative: a contributor must learn forks and pull requests;
  docs/how-to/add-a-design.md walks through it.
- Neutral: a design's history lives in this repository once merged.

### Confirmation

**A pull request touching anything outside one design folder fails.**
tools/scope_check.py on its defeat cases; on GitHub, the setup steps'
test pull request.

**Only the owner merges.** Live only: the ruleset on main requires a pull
request and the checks; contributors have no write access.

## Pros and Cons of the Options

### Fork and pull request

- Good: the standard open-source route, visible, needs no access.
- Bad: harder for a first-time contributor than uploading a file.

### A branch per contributor

- Good: one repository.
- Bad: needs write access for strangers, drifts away from engine fixes,
  stays invisible to visitors, and Pages publishes one branch.

### Designs hosted elsewhere

- Good: nothing to review here.
- Bad: nothing can be checked, and a link can change after review, as CSS
  Zen Garden's submissions show (the operator's site, research 0005).

## More Information

- ADR-0006 sets what a design folder may hold and how it is checked.
- Revisit if contributions arrive in a volume one reviewer cannot handle.

## Changes
