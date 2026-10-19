---
type: state
description: What exists right now in portfolio-gallery, what is blocked and on whom, and where the proof is. Where to start, then checked against the code.
status: current
---

# STATE

**Verified against commit 5a7cecf, the last commit before this file's
update, 2026-10-19 UTC, by the Brief 1 implementing session's eighth
round**: a fresh clone of it run through every defeat case with the
browser and axe, every check with axe, and the browser checks on a gallery
holding ten showcase entries; the gates proven on a clone of it
(logs/2026-10-12-brief-1-build.md, Round 8). This is the only line in
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

Public, set up and tested; main changes only by pull request. On the
branch showcase, not yet pushed: the gallery's templates first, then a
showcase of contributors' own sites, checked as files and, never
rendered, by their responses, on the pull request and weekly; the footer
credit names the design and its author (ADR-0016). Merging it approves
the screenshot limits; then setup Test 6, the owner's own entry. Waiting:
step 5's policy, provable only on or after 2026-11-02; ADR-0012, held.

## Publishing

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| The Actions policy allowing `pull_request_target` (step 5) | PARTIAL | [BELIEVED] set by the owner (the chat's report); until 2026-11-02 GitHub runs the scope check without the policy too | 2026-10-18 | ADR-0006, A2; setup Test 1 |
| This branch, showcase, merged to main | PENDING | the owner pushes it and opens the pull request; checks and scope must pass; merging approves the screenshot limits | 2026-10-19 | 5a7cecf |

## Decisions waiting on the owner

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| Lighthouse in CI | PENDING | held as proposed by the owner; speed measured locally | 2026-10-15 | ADR-0012 |
| The screenshot limits: 1,024 to 1,920 pixels wide, 500 KB, no location | PENDING | proposed from measurements, built as constants; the owner's merge approves them | 2026-10-19 | ADR-0016, A4 to A6 |

## Built, not yet complete

DONE rows are in docs/reference/completed.md.

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| CODEOWNERS and the issue templates | PARTIAL | [BELIEVED] written; not exercised until an outside contribution arrives | 2026-10-18 | b798834 |
| The showcase: files, scope, responses, gallery, weekly check, credit, cleanup | PARTIAL | [VERIFIED] 40 defeat cases and 7 planted controls, on a fresh clone; the browser checks on a gallery with ten entries; [BELIEVED] on GitHub until setup Test 6 | 2026-10-19 | 5a7cecf; ADR-0016 |

## Blocked, and on whom

| Item | Blocked on | Who | Since |
|---|---|---|---|
| Step 5's proof | The date: Test 1 again on or after 2026-11-02 | The owner | 2026-10-18 |
| Merging this branch, then Test 6 | The owner's push, pull request, merge and his own entry | The owner | 2026-10-19 |

## Known unverified

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
