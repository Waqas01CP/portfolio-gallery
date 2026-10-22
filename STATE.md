---
type: state
description: What exists right now in portfolio-gallery, what is blocked and on whom, and where the proof is. Where to start, then checked against the code.
status: current
---

# STATE

**Verified against commit 3fed37d, the last commit before this file's
update, 2026-10-22 UTC, by the Brief 1 implementing session's eleventh
round, under Brief 11**: a fresh clone of it through every check with axe,
every defeat case with the browser and axe, the deploy's own path with 13
real snips and every browser check on what it assembled; the gates proven
on a clone of it (logs/2026-10-12-brief-1-build.md, Round 11). This is the only line in
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
showcase is live with the owner's own entry, its cards in their pictures'
own shapes, packed (pull request 14). On the branch guides-and-prompt,
not yet pushed: the README routes every kind of visitor and carries a
checked, self-contained prompt for their AI assistant (ADR-0017); issue
forms for a showcase entry and a question; borderless showcase cards with
rounded pictures; his own commit messages may name him (ADR-0002,
Changes). Waiting: the owner's merge, and his word on AGENTS.md, a copy's
own prompt and a gallery picture; step 5's policy, provable only on or
after 2026-11-02; ADR-0012, held.

## Publishing

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| The Actions policy allowing `pull_request_target` (step 5) | PARTIAL | [BELIEVED] set by the owner (the chat's report); until 2026-11-02 GitHub runs the scope check without the policy too | 2026-10-18 | ADR-0006, A2; setup Test 1 |
| This branch, guides-and-prompt, merged to main | PENDING | the owner pushes it, reads the README on the branch, and opens the pull request; checks and scope must pass | 2026-10-22 | b77f3e0, 2b641d4, 495a2ba, 3fed37d |

## Decisions waiting on the owner

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| Lighthouse in CI | PENDING | held as proposed by the owner; speed measured locally | 2026-10-15 | ADR-0012 |
| AGENTS.md for coding agents; a short prompt in a copy's README; a picture of the gallery page in the README | PENDING | proposed with their sources, none built | 2026-10-22 | ADR-0017 |

## Built, not yet complete

DONE rows are in docs/reference/completed.md.

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| CODEOWNERS and the issue templates | PARTIAL | [BELIEVED] written; not exercised until an outside contribution arrives | 2026-10-18 | b798834 |
| The showcase packed by its pictures' shapes | PARTIAL | [VERIFIED] the packing check at 390 and 1366 px, light and dark, by the script, by Chrome's grid-lanes and with scripts off, and its defeat cases, on a fresh clone, and on GitHub's runner in pull request 14's checks; [BELIEVED] in Safari 26.4's own grid-lanes, which the seat cannot run | 2026-10-22 | b17d883, ba93032; ADR-0016, Changes |
| The README's routes and prompt; the Showcase entry and Question forms | PARTIAL | [VERIFIED] the prompt check and its defeat cases on a fresh clone; the README rendered by GitHub's Markdown API and looked at; the forms parsed; [BELIEVED] the copy button on GitHub's page and the forms in its issue chooser, until the owner sees them on the branch | 2026-10-22 | 3fed37d, b77f3e0; ADR-0017 |

## Blocked, and on whom

| Item | Blocked on | Who | Since |
|---|---|---|---|
| Step 5's proof | The date: Test 1 again on or after 2026-11-02 | The owner | 2026-10-18 |
| Merging this branch | The owner's push, his look at the README on the branch, the pull request and the merge | The owner | 2026-10-22 |

## Known unverified

- Whether GitHub accepts the two new issue forms; one it cannot read
  shows an error in the issue chooser, which the owner sees on the branch.
- How Safari 26.4 and later, the one browser shipping grid-lanes, packs
  the cards; Chrome's own grid-lanes, behind its flag, matched the
  script's places within 1 px on 2026-10-21.
- Whether a Mac's own PNG encoder stays under the 20 MiB cap for a 5K
  wall of photographs; Chrome's encoder gave 9.5 MB and Windows' up to
  16.9 MB.
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
