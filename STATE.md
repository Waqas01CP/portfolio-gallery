---
type: state
description: What exists right now in portfolio-gallery, what is blocked and on whom, and where the proof is. Where to start, then checked against the code.
status: current
---

# STATE

**Verified against commit fceaace, the last commit before this file's
update, 2026-10-20 UTC, by the Brief 1 implementing session's ninth round,
under Brief 9**: a fresh clone of it run through every defeat case with
the browser and axe; a fresh clone of 3020bb4, which differs from it only
in the defeat harness, through every check with axe and the deploy's own
path with ten real snips, then the browser checks on what it assembled; the gates proven on a clone of 3020bb4
(logs/2026-10-12-brief-1-build.md, Round 9). This is the only line in
this file that names commits.

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

Public, set up and tested; main changes only by pull request. The
showcase merged on 2026-10-19 (pull request 10) and is live with no
entry. On the branch showcase-any-snip, not yet pushed: a showcase
screenshot is any snip as its tool saved it, and the deploy draws the
gallery's copies from it (ADR-0016, Changes, 2026-10-20). After its merge,
setup Test 6, the owner's own entry. Waiting: step 5's policy, provable
only on or after 2026-11-02; ADR-0012, held.

## Publishing

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| The Actions policy allowing `pull_request_target` (step 5) | PARTIAL | [BELIEVED] set by the owner (the chat's report); until 2026-11-02 GitHub runs the scope check without the policy too | 2026-10-18 | ADR-0006, A2; setup Test 1 |
| This branch, showcase-any-snip, merged to main | PENDING | the owner pushes it and opens the pull request; checks and scope must pass | 2026-10-20 | 3020bb4, fceaace |

## Decisions waiting on the owner

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| Lighthouse in CI | PENDING | held as proposed by the owner; speed measured locally | 2026-10-15 | ADR-0012 |
| A floor or a pixel ceiling for showcase screenshots | PENDING | offered, neither built: the review sees every screenshot, and a file Chrome cannot draw fails on its pull request | 2026-10-20 | ADR-0016, Changes |

## Built, not yet complete

DONE rows are in docs/reference/completed.md.

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| CODEOWNERS and the issue templates | PARTIAL | [BELIEVED] written; not exercised until an outside contribution arrives | 2026-10-18 | b798834 |
| The showcase: files, scope, responses, served copies, gallery, weekly check, credit, cleanup | PARTIAL | [VERIFIED] its defeat cases and planted controls, the deploy's path rehearsed with ten real snips, on a fresh clone; live on GitHub with no entry; [BELIEVED] for an entry until setup Test 6 | 2026-10-20 | 5a7cecf, 3020bb4, fceaace; ADR-0016 |

## Blocked, and on whom

| Item | Blocked on | Who | Since |
|---|---|---|---|
| Step 5's proof | The date: Test 1 again on or after 2026-11-02 | The owner | 2026-10-18 |
| Merging this branch, then Test 6 | The owner's push, pull request, merge and his own entry | The owner | 2026-10-20 |

## Known unverified

- Whether the deploy's shots job gathers and uploads its pictures on
  GitHub's runner as rehearsed here; the first deploy after the merge
  shows it.
- Whether a Mac's own PNG encoder stays under the 20 MiB cap for a 5K
  wall of photographs; Chrome's encoder gave 9.5 MB and Windows' up to
  16.9 MB.
- Whether the weekly showcase workflow's anonymous clone and fetches run
  on GitHub's runner as they do here; Test 6, step 6, shows it.
- Whether listed sites answer GitHub's runner as they answer this
  machine; bot protection answers some datacenter addresses with 403,
  which the check reports for a check by hand.
- Whether a template copy shows a link back to its template on GitHub.
- Whether the step 5 policy lets the scope check run once GitHub enforces
  its block, from 2026-11-02.
- Whether Chrome runs on the runner with its sandbox; it runs with
  --no-sandbox, as the workflows set (ADR-0010, A3).
- Why a panel hidden by script without aria-hidden was exposed at load on
  the owner's site at 0403c68 but not on this engine.
- The cause of the default design's rare anchor misses with swap (font
  timing is a hypothesis; optional removed them, ADR-0014).
