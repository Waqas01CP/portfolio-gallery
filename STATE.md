---
type: state
description: What exists right now in portfolio-gallery, what is blocked and on whom, and where the proof is. Where to start, then checked against the code.
status: current
---

# STATE

**Verified against commit e794feb, the last commit before this file's
update, 2026-10-16 UTC, by the Brief 1 implementing session's second
round**: a fresh clone of it checked in full with axe and every defeat
case run, and the pre-publish search run over the whole history
(logs/2026-10-12-brief-1-build.md, Round 2). This is the only line in
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

Built and checked locally; every question to the owner answered; not
published. His answers of 2026-10-15 UTC are applied: records 0006 to
0011 accepted and 0013 and 0014 written, axe-core in the checks workflow,
the Code of Conduct's contact in place. The workflows have never run:
they wait for the owner to follow docs/setup-on-github.md, which he aims
to finish before 2026-11-02, once the pre-publish search has passed on
the commit he will push.

## Publishing

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| Workflows run on GitHub: scope, checks with axe, deploy | PENDING | [BELIEVED] parsed and checked as files only | 2026-10-16 | b798834, c7e3fd9; ADR-0005 |
| Chrome's sandbox on the Ubuntu 24.04 runner | PENDING | not testable before the first push | 2026-10-12 | ADR-0010, A3 |
| The repository's Actions policy allowing `pull_request_target` | PENDING | GitHub's default policy blocks it from 2026-11-02; setup step 5 sets it, Test 1 proves it | 2026-10-15 | ADR-0006, A2; logs/2026-10-12-brief-1-build.md |
| The pre-publish search on the commit to be pushed | PARTIAL | [VERIFIED] the seat's part passed on the whole history through this series; the master CV part passed at 43edeb2 (taken from the architecture chat's message of 2026-10-15), not yet run on the commits after it | 2026-10-16 | ADR-0005; logs/2026-10-12-brief-1-build.md |

## Decisions waiting on the owner

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| Lighthouse in CI | PENDING | held as proposed by the owner; speed measured locally | 2026-10-15 | ADR-0012 |

## Built, not yet complete

DONE rows are in docs/reference/completed.md.

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| Workflows, scope check, CODEOWNERS, templates | PARTIAL | [VERIFIED] as files; not run | 2026-10-12 | b798834 |
| Documents: README, CONTRIBUTING, Code of Conduct, SECURITY, how-tos, setup steps | PARTIAL | [BELIEVED] written and read back, every open question answered; the setup steps are exercised only when the owner follows them | 2026-10-16 | bd63dba, e794feb |
| axe-core in the checks workflow | PARTIAL | [VERIFIED] the fetch, the SHA-512 check and the extraction run here in the workflow's form and both local forms, a copy with one byte added refused; axe through ci.py checks and its defeat case run here. [BELIEVED] the workflow step on GitHub's runner, not yet run | 2026-10-16 | c7e3fd9; ADR-0011 |

## Blocked, and on whom

| Item | Blocked on | Who | Since |
|---|---|---|---|
| Publishing | The master CV search on the commit to be pushed; then the owner following the setup steps | The architecture chat; the owner | 2026-10-16 |

## Known unverified

- Whether a template copy shows a link back to its template on GitHub.
- Whether GitHub runs a template copy's workflows on its first commit.
- Whether GitHub Pages redirects /portfolio-gallery to /portfolio-gallery/
  (the setup's step 8 checks it).
- Whether a repository on a personal account is offered Actions event
  policies, and whether one can target one workflow file: GitHub's page
  says "all public repositories" without naming personal accounts (the
  architecture chat, 2026-10-15). Step 5 says what to do if not; Test 1
  proves it.
- Why a panel hidden by script without aria-hidden was exposed at load on
  the owner's site at 0403c68 but not on this engine.
- The cause of the default design's rare anchor misses with swap (font
  timing is a hypothesis; optional removed them, ADR-0014).
