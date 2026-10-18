---
type: state
description: What exists right now in portfolio-gallery, what is blocked and on whom, and where the proof is. Where to start, then checked against the code.
status: current
---

# STATE

**Verified against commit d612b96, the last commit before this file's
update, 2026-10-18 UTC, by the Brief 1 implementing session's fifth
round**: a fresh clone of it run through every defeat case with the
browser and axe and every check with axe, and the gates proven on a clone
of it (logs/2026-10-12-brief-1-build.md, Round 5). This is the only line
in this file that names a commit.

This file is where to start, not where to stop. It outranks memory. It does
not outrank the code or the data: where a row disagrees with them, the row
is stale; report it and correct it.

Organised by task, not by session.

## How to read a row

STATUS is DONE, PARTIAL or PENDING. DONE only when built and exercised,
never when merely examined. Evidence is [VERIFIED] (exercised and
observed) or [BELIEVED] (reasoned from reading, not run). Proof is a
commit, a decision record or a log filename, never a file path.

## How to maintain it

Update the affected rows in the same commit as the work, or in the last
commit of a series (gate E checks the push). When a row becomes DONE, move
it to docs/reference/completed.md in the same commit. When a blocker
clears, remove it from Blocked and record the clearing in its row.

## Headline

Public, set up and tested; main changes only by pull request. The owner's
decisions of 2026-10-18 are built on the branch dark-mode-and-capabilities,
not yet pushed: a design says in design.json whether it offers dark, and
CAPABILITIES' architecture lane is kept out of the repository. Open: the
branch's merge; what copies of the template should inherit (a question to
the owner); step 5's policy, provable only on or after 2026-11-02;
ADR-0012, held.

## Publishing

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| The Actions policy allowing `pull_request_target` (step 5) | PARTIAL | [BELIEVED] set by the owner (the chat's report); until 2026-11-02 GitHub runs the scope check without the policy too | 2026-10-18 | ADR-0006, A2; setup Test 1 |
| This branch, dark-mode-and-capabilities, merged to main | PENDING | the owner pushes it and opens the pull request; checks and scope must pass | 2026-10-18 | 39e49e6, d612b96 |

## Decisions waiting on the owner

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| Lighthouse in CI | PENDING | held as proposed by the owner; speed measured locally | 2026-10-15 | ADR-0012 |
| What a copy of the template inherits | PENDING | [VERIFIED] a copy inherits every tracked file: the records, logs, STATE.md, CLAUDE.md, the Code of Conduct's address, CODEOWNERS; options in the report of 2026-10-18 | 2026-10-18 | logs/2026-10-12-brief-1-build.md |

## Built, not yet complete

DONE rows are in docs/reference/completed.md.

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| CODEOWNERS and the issue templates | PARTIAL | [BELIEVED] written; not exercised until an outside contribution arrives | 2026-10-18 | b798834 |

## Blocked, and on whom

| Item | Blocked on | Who | Since |
|---|---|---|---|
| Step 5's proof | The date: Test 1 again on or after 2026-11-02 | The owner | 2026-10-18 |
| Merging this branch | The owner's push and pull request | The owner | 2026-10-18 |

## Known unverified

- Whether a template copy shows a link back to its template on GitHub.
- Whether the step 5 policy lets the scope check run once GitHub enforces
  its block, from 2026-11-02.
- Whether Chrome runs on the runner with its sandbox; it runs with
  --no-sandbox, as the workflows set (ADR-0010, A3).
- Why a panel hidden by script without aria-hidden was exposed at load on
  the owner's site at 0403c68 but not on this engine.
- The cause of the default design's rare anchor misses with swap (font
  timing is a hypothesis; optional removed them, ADR-0014).
