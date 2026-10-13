---
type: state
description: What exists right now in portfolio-gallery, what is blocked and on whom, and where the proof is. Where to start, then checked against the code.
status: current
---

# STATE

**Verified against commit 206c858, the last commit before this file's
update, 2026-10-13 UTC, by the Brief 1 implementing session**: a fresh
clone of the commit before it built, checked in full and every defeat
case run; that commit's two changes (the default design's fonts, the axe
check) then run through every browser check, axe and Lighthouse
(logs/2026-10-12-brief-1-build.md). This is the only line in this file
that names a commit.

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

Built and checked locally; not published. The engine, the sample content,
two designs, the gallery, the file and browser checks with their defeat
cases, the gates and the documents work and are proven here. The workflows
have never run: they wait for the owner to create the repository from
docs/setup-on-github.md, after the architecture chat has checked it and
after his answers to the open questions.

## Publishing

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| Workflows run on GitHub: scope, checks, deploy | PENDING | [BELIEVED] parsed and checked as files only | 2026-10-12 | b798834; ADR-0005 |
| Chrome's sandbox on the Ubuntu 24.04 runner | PENDING | not testable before the first push | 2026-10-12 | ADR-0010, A3 |
| The repository's Actions policy allowing `pull_request_target` | PENDING | GitHub's default policy blocks it from 2026-11-02 | 2026-10-12 | ADR-0006, A2; logs/2026-10-12-brief-1-build.md |
| The pre-publish search's master CV part | PENDING | the owner's site's seat runs it | 2026-10-12 | ADR-0005 |

## Decisions waiting on the owner

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| CSS only, or templates too | PENDING | CSS only is built | 2026-10-12 | ADR-0006, proposed |
| The default design's look | PENDING | his site's look is built as `default` | 2026-10-12 | logs/2026-10-12-brief-1-build.md |
| Response time promised to contributors | PENDING | CONTRIBUTING.md says it is not set | 2026-10-12 | logs/2026-10-12-brief-1-build.md |
| Whether the README links his site | PENDING | it credits his GitHub profile only | 2026-10-12 | logs/2026-10-12-brief-1-build.md |
| The Code of Conduct's contact | PENDING | marked pending in CODE_OF_CONDUCT.md; blocks publishing | 2026-10-12 | logs/2026-10-12-brief-1-build.md |
| The default design's fonts: `font-display: optional` (anchors), or swap as on his site | PENDING | optional is committed; the preview is byte-identical to swap's | 2026-10-13 | logs/2026-10-12-brief-1-build.md |
| The commit identity | PENDING | commits made as Waqas01CP with GitHub's no-reply address | 2026-10-12 | logs/2026-10-12-brief-1-build.md |
| Records 0006 to 0012 | PENDING | proposed | 2026-10-12 | ADR-0006 to ADR-0012 |

## Built this session, not yet complete

DONE rows of this session are in docs/reference/completed.md.

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| Workflows, scope check, CODEOWNERS, templates | PARTIAL | [VERIFIED] as files; not run | 2026-10-12 | b798834 |
| Documents: README, CONTRIBUTING, Code of Conduct, SECURITY, how-tos, setup steps | PARTIAL | [BELIEVED] written and read back; the setup steps are exercised only when the owner follows them | 2026-10-12 | bd63dba |
| axe and Lighthouse in CI | PENDING | proposed records; run locally only | 2026-10-12 | ADR-0011, ADR-0012 |

## Blocked, and on whom

| Item | Blocked on | Who | Since |
|---|---|---|---|
| Publishing | The Code of Conduct's contact; the architecture chat's check of the setup steps; the master CV search | The owner; the architecture chat | 2026-10-12 |

## Known unverified

- Whether a template copy shows a link back to its template on GitHub.
- Whether GitHub runs a template copy's workflows on its first commit.
- Whether GitHub Pages redirects /portfolio-gallery to /portfolio-gallery/
  (the setup's step 8 checks it).
- Whether an Actions policy can target one workflow file in a personal
  repository, as the setup's step 5 assumes; it says what to do if not.
- Why a panel hidden by script without aria-hidden was exposed at load on
  the owner's site at 0403c68 but not on this engine.
- The cause of the default design's rare anchor misses (font timing is a
  hypothesis).
