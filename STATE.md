---
type: state
description: What exists right now in portfolio-gallery, what is blocked and on whom, and where the proof is. Where to start, then checked against the code.
status: current
---

# STATE

**Verified against commit d5771c3, the last commit before this file's
update, 2026-10-18 UTC, by the Brief 1 implementing session's sixth
round**: a fresh clone of it run through the file defeat cases and every
check with axe, and the gates proven on a clone of it
(logs/2026-10-12-brief-1-build.md, Round 6). This is the only line in
this file that names a commit.

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
decision on what copies inherit is built on the branch template-cleanup,
not yet pushed: a workflow removes the project's own files once in each
copy, and the user guide lists them for a copy whose cleanup did not run.
Open: the branch's merge, then setup Test 5 in a real copy; step 5's
policy, provable only on or after 2026-11-02; ADR-0012, held.

## Publishing

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| The Actions policy allowing `pull_request_target` (step 5) | PARTIAL | [BELIEVED] set by the owner (the chat's report); until 2026-11-02 GitHub runs the scope check without the policy too | 2026-10-18 | ADR-0006, A2; setup Test 1 |
| This branch, template-cleanup, merged to main | PENDING | the owner pushes it and opens the pull request; checks and scope must pass | 2026-10-18 | d46f349, d5771c3 |
| The template cleanup in a real copy | PENDING | setup Test 5, after the merge; whether the workflow's token may delete workflow files is known only then | 2026-10-18 | ADR-0015 |

## Decisions waiting on the owner

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| Lighthouse in CI | PENDING | held as proposed by the owner; speed measured locally | 2026-10-15 | ADR-0012 |

## Built, not yet complete

DONE rows are in docs/reference/completed.md.

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| CODEOWNERS and the issue templates | PARTIAL | [BELIEVED] written; not exercised until an outside contribution arrives | 2026-10-18 | b798834 |
| The template cleanup | PARTIAL | [VERIFIED] its check and six defeat cases, on a fresh clone; [BELIEVED] on GitHub until Test 5 | 2026-10-18 | d46f349; ADR-0015 |

## Blocked, and on whom

| Item | Blocked on | Who | Since |
|---|---|---|---|
| Step 5's proof | The date: Test 1 again on or after 2026-11-02 | The owner | 2026-10-18 |
| Merging this branch, then Test 5 | The owner's push, pull request and test | The owner | 2026-10-18 |

## Known unverified

- Whether a workflow's own token may delete a workflow file; GitHub's
  documentation is silent, and a practitioner's log shows it may not
  create or change one (ADR-0015, A3). Test 5 shows it.
- Whether a template copy shows a link back to its template on GitHub.
- Whether the step 5 policy lets the scope check run once GitHub enforces
  its block, from 2026-11-02.
- Whether Chrome runs on the runner with its sandbox; it runs with
  --no-sandbox, as the workflows set (ADR-0010, A3).
- Why a panel hidden by script without aria-hidden was exposed at load on
  the owner's site at 0403c68 but not on this engine.
- The cause of the default design's rare anchor misses with swap (font
  timing is a hypothesis; optional removed them, ADR-0014).
