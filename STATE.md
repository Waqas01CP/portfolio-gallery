---
type: state
description: What exists right now in portfolio-gallery, what is blocked and on whom, and where the proof is. Where to start, then checked against the code.
status: current
---

# STATE

**Verified against commit 96675dc, the last commit before this file's
update, 2026-10-18 UTC, by the Brief 1 implementing session's fourth
round**: the file defeat cases run on its tree and the gates passed on
it; the setup guide's test design run with axe both ways; the
repository's ruleset, pull requests and runs read from GitHub's public
API (logs/2026-10-12-brief-1-build.md, Round 4). This is the only line in
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

Public, set up and tested. The owner followed every setup step and Tests
1 to 4 between 2026-10-16 and 18 (the architecture chat's report, checked
against GitHub's API where it can be). main takes changes only by pull
request, with the checks and the scope check required; this seat commits
on a branch, which the owner pushes and opens as a pull request. Open:
step 5's policy, provable only by a scope run on or after 2026-11-02; the
owner's decision on dark mode in the design contract; ADR-0012, held.

## Publishing

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| The Actions policy allowing `pull_request_target` (step 5) | PARTIAL | [BELIEVED] set by the owner (the chat's report); the scope check ran on every pull request, but until 2026-11-02 GitHub runs it without the policy too | 2026-10-18 | ADR-0006, A2; setup Test 1 |
| This branch, setup-guide-fixes, merged to main | PENDING | the owner pushes it and opens the pull request; checks and scope must pass | 2026-10-18 | 96675dc |

## Decisions waiting on the owner

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| Lighthouse in CI | PENDING | held as proposed by the owner; speed measured locally | 2026-10-15 | ADR-0012 |
| Dark mode in the design contract | PENDING | [VERIFIED] the page declares light and dark, so a design that sets no colours fails axe in device dark; CONTRIBUTING.md says a design is checked in dark "if it offers both"; options in the report of 2026-10-18 | 2026-10-18 | logs/2026-10-12-brief-1-build.md |

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

- Whether a template copy shows a link back to its template on GitHub
  (Test 4 showed its first runs start on their own; the link was not
  reported).
- Whether the step 5 policy lets the scope check run once GitHub enforces
  its block, from 2026-11-02.
- Whether Chrome runs on the runner with its sandbox; it runs with
  --no-sandbox, as the workflows set (ADR-0010, A3).
- Why a panel hidden by script without aria-hidden was exposed at load on
  the owner's site at 0403c68 but not on this engine.
- The cause of the default design's rare anchor misses with swap (font
  timing is a hypothesis; optional removed them, ADR-0014).
