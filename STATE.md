---
type: state
description: What exists right now in portfolio-gallery, what is blocked and on whom, and where the proof is. Where to start, then checked against the code.
status: current
---

# STATE

**Verified against commit 27db869 and the fix after it, 2026-10-28 UTC,
by the Brief 1 implementing session's seventeenth round, under the
owner's request of 2026-10-28**: every defeat case with the browser and
axe on a fresh clone of 27db869, all but two older cases that pull
request 22's showcase entry broke, on main too; those two, with their
families, rerun after the fix; a one-design change through the whole
run, narrowed, in a scratch clone (logs/2026-10-12-brief-1-build.md,
Round 17). This is the only line in
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
own shapes, packed (pull request 14). The README routes every kind of
visitor and carries a checked prompt for their AI assistant, with the
Showcase entry and Question forms (pull request 15, ADR-0017); AGENTS.md
for coding agents, and a copy's own; a short prompt in a copy's README;
the gallery page's own picture leading the README (pull request 16). A
copy's first Deploy ends with a notice, not red, while GitHub Pages is
off, shown in the owner's own copy, and the copy's README leads with
turning it on (ADR-0015, Changes); a showcase card's larger copy opens in
an overlay that can be closed (ADR-0016, Changes); pull requests 17 to
19. Twelve designs on main and live: five of the owner's, Bento,
Broadsheet, Console, Poster and Signal, with Plain raised to the same
standard (pull request 20), and five for professions, each shown with its
own invented person, Sentinel, Latent, Pocket, Assert and Pipeline (pull
request 21; ADR-0018). The first contribution from outside, a showcase
entry, merged in pull request 22, CODEOWNERS asking the owner's review.
On the branch checks-for-changes, not yet pushed: the browser checks look
only at the pages a change alters, every page by hand and each Monday
(ADR-0019); on width-check, cut from it, a standing check that no page
scrolls sideways (ADR-0009, Changes); on more-professions, cut from that,
five more designs for professions. Waiting: his push of the three, in that order, and his judgment of the
five designs' final look; step 5's policy, provable only on or
after 2026-11-02; ADR-0012, held.

## Publishing

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| The Actions policy allowing `pull_request_target` (step 5) | PARTIAL | [BELIEVED] set by the owner (the chat's report); until 2026-11-02 GitHub runs the scope check without the policy too | 2026-10-18 | ADR-0006, A2; setup Test 1 |

## Decisions waiting on the owner

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| Lighthouse in CI | PENDING | held as proposed by the owner; speed measured locally | 2026-10-15 | ADR-0012 |

## Built, not yet complete

DONE rows are in docs/reference/completed.md.

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| Checks on what a change alters: the browser checks of a pull request or push only on the pages whose built files differ from the base's; every page when the checks change, the base cannot be read or built, by hand, and each Monday | PARTIAL | [VERIFIED] the selection's defeat cases, a narrowed run's case and control, and a one-design change through the whole run (362 s against 3,676 s for every page); [BELIEVED] on GitHub until the branch merges: the base fetched on a push, the run's summary, the weekly workflow. Phase 2, a run of every page in parallel jobs, before about 19 designs | 2026-10-28 | 27db869; ADR-0019 |
| No page scrolls sideways: a standing check on every design and the gallery page, at 320, 360 and 390 px, 1080 by 1920 and 1366 px, every section laid out, scripts on and off | PARTIAL | [VERIFIED] the twelve designs and the gallery page pass, 130 runs in 110 s; its defeat case (a 1400 px element) fails and its control (the same in a box that scrolls itself) passes; [BELIEVED] on GitHub's runner until its pull request runs | 2026-10-28 | ADR-0009, Changes; 2026-10-12-brief-1-build.md, Round 18 |
| Five more designs for professions, Broadcast, Cyanotype, Frost, Handbook and Savepoint, each shown with its own sample person of their profession's shape | PARTIAL | [VERIFIED] every browser check with axe on the five designs and the gallery page: the first run's only failures were the run's own missing showcase pictures and Broadcast's education dates in yellow on white, both fixed and rerun; Frost and Broadcast again after their last changes, 0 failures in 754 s; no page scrolls sideways: the twelve designs and the gallery page, 130 runs, and the five new ones, 60 runs, then Frost and Broadcast again, 30; each looked at, at 1366 by 768, 390 by 844 and 1080 by 1920; their box placement measured against all seventeen (the session log, Round 19); [BELIEVED] the owner's judgment of the final look, and the previews the deploy takes | 2026-10-28 | cd7bd89; ADR-0013, Changes; ADR-0018, Changes |
| CODEOWNERS and the issue templates | PARTIAL | [VERIFIED] CODEOWNERS asked the owner's review the moment pull request 22, the first from outside, opened, and its author filled the pull request template's showcase section (GitHub's API); [BELIEVED] the issue templates, which no one has used yet | 2026-10-28 | b798834; pull request 22 |
| The showcase packed by its pictures' shapes | PARTIAL | [VERIFIED] the packing check at 390 and 1366 px, light and dark, by the script, by Chrome's grid-lanes and with scripts off, and its defeat cases, on a fresh clone, and on GitHub's runner in pull request 14's checks; [BELIEVED] in Safari 26.4's own grid-lanes, which the seat cannot run | 2026-10-22 | b17d883, ba93032; ADR-0016, Changes |
| The README's routes and prompt; the Showcase entry and Question forms | PARTIAL | [VERIFIED] the prompt check and its defeat cases; on main, GitHub's own page serves the prompt's block with its copy button's text and the three pictures through its image proxy (2026-10-23); the forms parsed; [BELIEVED] the four forms in the issue chooser, which needs a sign-in, until the owner looks | 2026-10-23 | 0ce2c71, pull request 15; ADR-0017 |
| The showcase's overlay | PARTIAL | [VERIFIED] the overlay check at 390 and 1366 px, light and dark, axe open and closed, with scripts off, and its defeat cases; the tree at load the same as main's; on the live gallery the owner opened it and closed it each way (taken from Brief 14); [BELIEVED] in Safari and Firefox, whose dialog the seat cannot run | 2026-10-23 | 42f5760, pull request 17; ADR-0016, Changes |

## Blocked, and on whom

| Item | Blocked on | Who | Since |
|---|---|---|---|
| Step 5's proof | The date: Test 1 again on or after 2026-11-02 | The owner | 2026-10-18 |
| Merging checks-for-changes, then width-check, then more-professions | The owner's push and merge | The owner | 2026-10-28 |

## Known unverified

- Whether GitHub accepts the two issue forms added on 2026-10-22; one it
  cannot read shows an error in the issue chooser, which needs a sign-in.
- Whether a design whose one theme is dark (Console: dark false,
  color-scheme: dark on its root) shows the browser's own parts dark in
  Safari and Firefox, as in Chrome.
- Whether coding agents follow AGENTS.md as their documentation says;
  read from first-party documentation, not tried with each agent.
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
