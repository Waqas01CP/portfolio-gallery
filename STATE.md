---
type: state
description: What exists right now in portfolio-gallery, what is blocked and on whom, and where the proof is. Where to start, then checked against the code.
status: current
---

# STATE

**Verified against main at 6d65e12 and the branch report-17-decisions
after it, 2026-11-10 UTC, by the Brief 1 implementing session's
thirty-second round**: the weekly run's eighteen speed tables, as the
owner copied them from GitHub, set against ADR-0009's goals; the gates
and the pre-publish search (logs/2026-10-12-brief-1-build.md, Round 32). This is the only line in
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
Since pull requests 24 to 33: the browser checks look only at the pages
a change alters, every page by hand and each Monday (ADR-0019), shared
out across jobs that run side by side on GitHub, a check of every page
about 5 minutes against 76 on one runner, with Lighthouse about 6;
Chrome's start given 60 s and a second try; a standing check that no
page scrolls sideways; seventeen designs, ten of them for professions,
and profession tags (ADR-0020); speed checked in CI, ADR-0012 accepted
with the owner's option A; a like button on each template and site, a
post in Discussions, nineteen made on 2026-10-29 (ADR-0021), a like an
upvote or a thumbs up on the post, added together, the owner's choice.
No attempt to edit a post, which GitHub refuses the workflow (pull
request 54). Brief 15's corrections to four records' form merged in pull
request 55. A link preview on the gallery page, Open Graph and X card
tags and a committed picture, merged in pull request 56 and shown by
LinkedIn's Post Inspector (ADR-0022, accepted by the owner on
2026-11-06; previews on a copy's own site deferred until a user asks).
The weekly run of every page passed on 2026-11-02, shared out in 21
jobs; step 5's policy is proven by a scope run after GitHub's block took
effect; its speed tables show TBT 0 ms on every page. Waiting: more
Mondays' numbers before the owner decides on TBT's 600 ms ceiling.

## Publishing

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| None open | DONE | Step 5's policy proven 2026-11-04, moved to docs/reference/completed.md | 2026-11-05 | the session log, Round 30 |

## Decisions waiting on the owner

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| None open | DONE | ADR-0022 accepted by the owner, its reading of ADR-0007 with it; previews on a copy's own site deferred | 2026-11-06 | ADR-0022, Changes |

## Built, not yet complete

DONE rows are in docs/reference/completed.md.

| Task | Status | Evidence | Date | Proof |
|---|---|---|---|---|
| Checks on what a change alters | PARTIAL | [VERIFIED] on GitHub, the six runs of pull requests 24 to 26 and their merges, each checking every page as designed, for a file then in CHECKING (tools/ci.py, tools/check_browser.py, build.py), replayed on the same commits; Phase 2 on GitHub, pull request 28's run checking every page side by side in 5 min 8 s against 76 min for pull request 27's on one runner, one design's job failing at Chrome's start and the verdict with it, as built, then green on a rerun; pull request 29, Chrome's start fixed, every page in 5.2 min with all eighteen starts within it; pull request 30 checked every page for a change to the gallery page's own stylesheet, the rule narrowed on lighthouse; the weekly run of 2026-11-02 shared out on GitHub, every page in 21 jobs, all passing, 6.4 minutes from 12:50Z, eight hours after its 04:41 schedule (GitHub's API, run 41447942168); [BELIEVED] a narrowed run on GitHub, not yet seen there | 2026-10-29 | 27db869, 40c9610; ADR-0019, Changes |
| Profession tags | DONE | [VERIFIED] pull request 30 green on GitHub and merged; the gallery built with twelve labels; nine cases | 2026-10-29 | ADR-0020; pull request 30 |
| Speed in CI | PARTIAL | [VERIFIED] on GitHub: pull request 32's run checked every page with Lighthouse in 6.4 min, green, and its merge's 6.2; here, every page measured and the speed cases; the weekly run of 2026-11-02 with Lighthouse on every page, passing, so no median over 600 ms TBT, LCP over 2.5 s or CLS over 0.1 (run 41447942168); its medians, from the jobs' summaries as the owner copied them on 2026-11-10: LCP 1,376 to 2,103 ms (Console the lowest; Frost 2,103 and Default 2,102 the highest), CLS 0.000 on every page but Plain's 0.047, TBT 0 ms on all eighteen pages; [BELIEVED] whether TBT stays at 0 ms on the runner over more Mondays, which decides whether 600 ms can come down | 2026-11-10 | ADR-0012, Changes |
| Like buttons | DONE | [VERIFIED] on GitHub: nineteen posts made by the workflow on 2026-10-29; after pull request 53, the owner's upvote on Frost's post counted, the live card showing 1 like; the rewrite of the first posts refused by GitHub, a warning each, removed in pull request 54; here, the like cases, and with the author rule or the upvotes removed each case fails | 2026-10-30 | ADR-0021, Changes |
| CODEOWNERS and the issue templates | PARTIAL | [VERIFIED] CODEOWNERS asked the owner's review the moment pull request 22, the first from outside, opened, and its author filled the pull request template's showcase section (GitHub's API); [BELIEVED] the issue templates, which no one has used yet | 2026-10-28 | b798834; pull request 22 |
| The showcase packed by its pictures' shapes | PARTIAL | [VERIFIED] the packing check at 390 and 1366 px, light and dark, by the script, by Chrome's grid-lanes and with scripts off, and its defeat cases, on a fresh clone, and on GitHub's runner in pull request 14's checks; [BELIEVED] in Safari 26.4's own grid-lanes, which the seat cannot run | 2026-10-22 | b17d883, ba93032; ADR-0016, Changes |
| The README's routes and prompt; the Showcase entry and Question forms | PARTIAL | [VERIFIED] the prompt check and its defeat cases; on main, GitHub's own page serves the prompt's block with its copy button's text and the three pictures through its image proxy (2026-10-23); the forms parsed; [BELIEVED] the four forms in the issue chooser, which needs a sign-in, until the owner looks | 2026-10-23 | 0ce2c71, pull request 15; ADR-0017 |
| The showcase's overlay | PARTIAL | [VERIFIED] the overlay check at 390 and 1366 px, light and dark, axe open and closed, with scripts off, and its defeat cases; the tree at load the same as main's; on the live gallery the owner opened it and closed it each way (taken from Brief 14); [BELIEVED] in Safari and Firefox, whose dialog the seat cannot run | 2026-10-23 | 42f5760, pull request 17; ADR-0016, Changes |

## Blocked, and on whom

| Item | Blocked on | Who | Since |
|---|---|---|---|

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
- Whether Chrome runs on the runner with its sandbox; it runs with
  --no-sandbox, as the workflows set (ADR-0010, A3).
- Why a panel hidden by script without aria-hidden was exposed at load on
  the owner's site at 0403c68 but not on this engine.
- The cause of the default design's rare anchor misses with swap (font
  timing is a hypothesis; optional removed them, ADR-0014).
