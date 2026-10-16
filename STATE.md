---
type: state
description: What exists right now in portfolio-gallery, what is blocked and on whom, and where the proof is. Where to start, then checked against the code.
status: current
---

# STATE

**Verified against commit 1f14aa7, the last commit before this file's
update, 2026-10-16 UTC, by the Brief 1 implementing session's third
round**: every check with axe and every file defeat case run on its
tree, the gates proven on a clone of it, and the repository's runs on
GitHub read from its public API (logs/2026-10-12-brief-1-build.md,
Round 3). This is the only line in this file that names a commit.

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

Public on GitHub since the owner's push of 2026-10-16, and the gallery is
live at https://waqas01cp.github.io/portfolio-gallery/ with both designs
(Deploy run 38967233877, 21:08Z). The deploy job was skipped in every
site-mode run, so no copy of the template would have published; the fix
and a check that refuses the pattern are committed, and wait for the
owner's push and Test 4 of the setup steps, a template copy that
publishes in site mode. Seats never push.

## Publishing

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| Deploy on GitHub, site mode | PARTIAL | [VERIFIED] skipped in runs 38957566263 and 38963263769 as published; fixed in this series; [BELIEVED] fixed on GitHub until Test 4 runs | 2026-10-16 | logs/2026-10-12-brief-1-build.md |
| The scope check on GitHub | PENDING | no pull request yet; Tests 1 and 2 | 2026-10-16 | ADR-0006 |
| The repository's Actions policy allowing `pull_request_target` | PENDING | GitHub's default policy blocks it from 2026-11-02; step 5 sets it, Test 1 proves it | 2026-10-15 | ADR-0006, A2 |
| The account's email kept private for website commits | PENDING | setup step 12; no website commit exists yet (GitHub's API, 2026-10-16) | 2026-10-16 | logs/2026-10-12-brief-1-build.md |

## Decisions waiting on the owner

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| Lighthouse in CI | PENDING | held as proposed by the owner; speed measured locally | 2026-10-15 | ADR-0012 |

## Built, not yet complete

DONE rows are in docs/reference/completed.md.

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| Workflows, scope check, CODEOWNERS, templates | PARTIAL | [VERIFIED] Checks and Deploy ran on GitHub (completed.md); the scope check, CODEOWNERS and the templates wait for Part D's tests | 2026-10-16 | b798834, 1f14aa7 |
| Documents: README, CONTRIBUTING, Code of Conduct, SECURITY, how-tos, setup steps | PARTIAL | [BELIEVED] written and read back; steps 3, 6, 7 and 8 evidently followed (the runs on GitHub); the others not yet reported to this seat | 2026-10-16 | bd63dba, e794feb |

## Blocked, and on whom

| Item | Blocked on | Who | Since |
|---|---|---|---|
| The site-mode proof | The push of this series, before step 9's ruleset; then Test 4 | The owner | 2026-10-16 |

## Known unverified

- Whether a template copy shows a link back to its template on GitHub,
  and whether GitHub runs its workflows on its first commit (Test 4
  shows both).
- Whether a repository on a personal account is offered Actions event
  policies, and whether one can target one workflow file: GitHub's page
  says "all public repositories" without naming personal accounts (the
  architecture chat, 2026-10-15). Step 5 says what to do if not; Test 1
  proves it.
- Whether Chrome runs on the runner with its sandbox; it runs with
  --no-sandbox, as the workflows set (ADR-0010, A3).
- Why a panel hidden by script without aria-hidden was exposed at load on
  the owner's site at 0403c68 but not on this engine.
- The cause of the default design's rare anchor misses with swap (font
  timing is a hypothesis; optional removed them, ADR-0014).
