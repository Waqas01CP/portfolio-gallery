---
type: explanation
description: "Everything portfolio-gallery is and does, in one file: what it does end to end, how data is stored, the stack, its engineering qualities and what enforces each, measured numbers with their dates, how it was built, and its limits. For any chat or person who will open nothing else."
status: current
---

# Capabilities

**What this file is.** Everything this repository is and does, in one
place, for a reader who will open nothing else: any chat that needs to know
the project, and any person who reads README.md to use it and this file
for the nuance.

**Current as of 2026-10-23 UTC**, written by the implementing seat in its
lane: what the system does and how, the stack, the qualities, the numbers,
the limits, and the timeline's rows for what was built. **The architecture
chat's lane is kept privately**: the problem the project solves, where it
is going, the decisions it restates and the owner's role live in a file
that is never committed, because every copy of the template inherits what
is (the owner's decision of 2026-10-18). The decisions themselves are
public, in docs/decisions/.

It decides nothing. Where it disagrees with the code or a record, it is
stale.

---

## In one paragraph

A portfolio-site generator anyone can copy and publish with GitHub Pages
without installing anything, and a gallery of designs for it. A user
writes their content once in four files, picks a design by one setting,
and a GitHub Actions workflow builds a one-page site with every word in
the first response, no cookies, no tracking and nothing loaded from another
site. Designs are folders of CSS, fonts and images, contributed by pull
request, checked automatically for scope, file safety and accessibility,
and merged only by the owner. After the designs, the gallery shows a
showcase of contributors' own portfolio sites, each a link and a
screenshot its author supplies, checked as files and, never rendered, by
its response. It costs nothing to run: GitHub's free
public-repository features only. Public on GitHub since 2026-10-16; the
gallery is live at https://waqas01cp.github.io/portfolio-gallery/.

## What it does, end to end

1. **Content.** `content/config.json` (settings), `site.json` (the page's
   own text), `items.json` (dated items) and optionally `cv.md`, the
   source the content trace checks against (docs/reference/content.md).
2. **Build.** `build.py` checks every field before writing anything,
   refuses shortened text that is not a cut of its source, computes the
   timeline and the project grid, renders 13 Jinja2 templates into one
   page, writes the layout's positions into a generated stylesheet so no
   inline style is needed, and copies the engine's scripts and the
   design's files into `_site/` (ADR-0004). In gallery mode it builds every
   design on the same content, each at `designs/<name>/`, except a
   template made for a profession, shown with its own invented person from
   `samples/<name>/`, a whole content folder traced to its own CV
   (ADR-0018); and a gallery
   page: templates first, each with an optional "In use" link to its
   author's own site, then the showcase from `showcase/` (ADR-0016),
   each card's picture in its screenshot's own shape within 2.4 either
   way, its size reserved in the HTML from the screenshot's header. The
   footer's credit names the project, the design and its author.
3. **Checks before publishing.** The built files (no load from another
   origin, the policy tag, links resolve letter for letter) and the content
   trace; a failure publishes nothing.
4. **Previews** (the gallery only). Headless Chrome takes each design's
   first screen, and then the gallery page's own top, 1366 by 1280 pixels,
   which the README shows, in a job with no write token; only checked WebP
   files reach the published site (ADR-0010; ADR-0017, Changes).
5. **Publish.** GitHub Pages, from the deploy workflow's artifact, once a
   job has asked GitHub whether Pages is on. In a copy whose owner has not
   turned it on yet, the run ends with a notice saying how and publishes
   nothing, rather than failing red; in the gallery an off Pages fails
   (ADR-0015, Changes, 2026-10-23).
6. **In the browser.** The page is whole without scripts. site.js closes
   the "In depth" panels, runs the timeline's lane filters and cards, the
   section menu, the progress marker, a Dark switch for the visit when
   the design offers dark, and the effects a design turns on: a 3D knot drawn in a worker,
   card tilt, a moving strip with a pause control, scroll effects. Under
   reduced motion nothing moves. On the gallery, the showcase's cards are
   packed as on Pinterest: by CSS grid-lanes where the browser has it,
   else by gallery.js, each card in turn in the column whose bottom is
   highest, so they run in folder order; without either, in rows. A
   card's picture opens its larger copy in the page's own dialog, shown
   as a modal, with a Close button, Escape and a click outside to close
   it; without scripts, the plain link (ADR-0016, Changes, 2026-10-23).
7. **Contributions.** The README opens with a row for each thing a
   visitor may want to do, and carries a self-contained prompt they can
   give their own AI assistant, held to the repository by
   tools/check_prompt.py (ADR-0017); AGENTS.md routes coding agents to it,
   or, for work on the project, to CLAUDE.md. Issue forms: Bug, Design proposal,
   Showcase entry (removal, impersonation, an entry gone bad) and
   Question. A design pull request passes the scope check (from
   the default branch, reading only the file list), the design checks and
   the browser checks on every design the change alters, then the owner's
   review (ADR-0006, ADR-0019).
   A showcase entry, `showcase/<login>/` with entry.json and one
   screenshot as its tool saved it, any size, passes the scope check as
   its author's own, the file checks, Chrome drawing the gallery's copies
   of the screenshot, and a fetch of its site, never rendered: https, a 200 page, not
   parked, linking to the author's GitHub profile; then the owner's review.
   Every site is fetched again weekly by a workflow that holds no
   permissions and reports by failing (ADR-0016).
8. **A copy cleans itself up.** In a repository made with "Use this
   template", a workflow removes the project's own files once, puts a
   README and an AGENTS.md of the copy's own in place and commits; it
   never runs here or in a fork (ADR-0015). The showcase and every
   design's "In use" link go with them. The copy's README opens with
   turning GitHub Pages on, once, and carries a short
   prompt for the owner's AI assistant: content and its CV trace, the
   design, publishing, a failed build; checked here before any copy
   receives it (ADR-0017, Changes, 2026-10-23).

## How data is stored, and where it may go

- **No database, no server code.** Content is four files in the user's
  repository; the site is static.
- **Nothing about a visitor is kept.** No cookies, no storage, no
  requests to another origin; the Content-Security-Policy in every page
  refuses them even if a check misses one.
- **The owner's private material never enters the repository.** Gate A
  refuses his name outside LICENSE, README.md and his own showcase entry,
  his personal email
  addresses anywhere, the Code of Conduct's contact address outside
  CODE_OF_CONDUCT.md, and his private folder name, from a pattern file in
  git's own folder that is never committed (ADR-0008, ADR-0002).

## Tech stack

| Area | What is used |
|---|---|
| Build | Python 3.12 in a venv; Jinja2 3.1.6 and MarkupSafe 3.0.3, pinned with the SHA-256 of every file PyPI serves (ADR-0004) |
| Page | HTML, CSS and plain JavaScript; no framework |
| Designs | Seventeen, each credited to the owner and maintained by the project (ADR-0013, Changes, 2026-10-24 and 28). `default`: Manrope, JetBrains Mono and Instrument Serif under the SIL Open Font License, none reserving a name (checked in each WOFF2's name table, 2026-10-12); `bento`: Nunito, `poster`: Anton, `sentinel`: Chakra Petch, `latent`: Space Grotesk, `pocket`: Plus Jakarta Sans, `assert`: Public Sans and `pipeline`: Barlow Semi Condensed, the same licence, none reserving a name (each WOFF2's name table, 2026-10-24); `cyanotype`: Architects Daughter, `handbook`: Literata, `frost`: Bricolage Grotesque, `savepoint`: Pixelify Sans and `broadcast`: Archivo, the same licence, none naming a Reserved Font Name in its licence text (read 2026-10-28); `broadsheet`, `console`, `plain` and `signal`: system fonts. The ten made for professions are shown with their own sample people (ADR-0018) |
| CI and hosting | GitHub Actions on ubuntu-24.04 and GitHub Pages, free for public repositories; every action pinned to a full commit SHA |
| Browser checks and previews | Google Chrome, driven over its DevTools protocol by tools/cdp.py, standard library only (ADR-0010) |
| Accessibility rules in CI | axe-core 4.14.0 from npm, MPL-2.0, fetched by exact version in the checks workflow and checked against the registry's SHA-512 before it runs; never shipped in a site (ADR-0011) |
| Proposed, not added | Lighthouse 13.5.0 (ADR-0012), run only locally from a scratch folder; held as proposed by the owner on 2026-10-15 |

## Engineering qualities, and what enforces each

| Quality | What enforces it |
|---|---|
| A design cannot run code or load from elsewhere | The design format (ADR-0006); tools/check_design.py; the scope check; the page's Content-Security-Policy |
| A workflow job runs when it should | tools/check_workflows.py: a job after one that can be skipped must say when it runs, or GitHub skips it too and reports success |
| A pull request cannot change how it is checked | scope.yml on `pull_request_target`, from the default branch; it fails any change outside one design folder or its author's own showcase entry |
| A contributor's file never reaches a visitor | tools/screenshots.py draws WebP copies of a showcase screenshot, image chunk only, in a job with no write token; tools/ci.py assemble refuses anything else |
| A contributor's site is never rendered by the project | tools/check_showcase.py fetches responses only, bounded in time, size and redirects, refusing private addresses; the weekly workflow holds no permissions (tools/check_workflows.py refuses any) |
| Every word in the first response, readable without scripts | The fixed HTML; the words check compares every design with no design, scripts off |
| Checks that grow with the change, not the gallery | A pull request's browser checks look only at the pages whose built files differ from its base's; every page when the checks change, when in doubt, by hand and each Monday (ADR-0019) |
| Accessibility, for every design | The standing checks: the tree at load, keyboard, joins, anchors, words, motion, no page scrolling sideways from 320 px to 1366 px and at 1080 by 1920, and axe-core's rules, contrast among them (docs/reference/standing-checks.md) |
| A check can fail | tools/prove_checks.py runs each on its defeat case: 153 file cases, with 33 planted file controls (2026-10-29), and 24 browser cases, with 12 controls (2026-10-28) |
| Claims trace to the user's CV | tools/check_content.py, page to CV and CV to page |
| Deterministic output | Two builds compared byte for byte in CI |
| Nothing private published | Gates A to E; the pre-publish search |

## Measured numbers

| What | Value | Date | Source |
|---|---|---|---|
| Source | build.py 1,136 lines; 15 tools, 6,996 lines; 13 templates, 615 lines; scripts and engine styles 1,087 lines; designs, lines of CSS: default 1,521, bento 366, poster 356, broadsheet 322, console 304, signal 301, plain 300; workflows 401 lines | 2026-10-24 | `wc -l` at 4521c00 |
| Sample site, built | index.html 39,195 bytes (6,239 gzipped); site.js 22,481 (7,219); knot.js 5,715 (2,256); base.css 3,099 (1,489); layout.css 1,947 (562); default design.css 49,498 (11,160); fonts 78,396 | 2026-10-12 | `wc -c`; Python's gzip, level 6 |
| Gallery page | 3,778 bytes (1,485 gzipped); plain design.css 11,678 bytes | 2026-10-12 | same |
| Builds | site in each design and the gallery: exit 0, twice each, byte-identical (default 14 files, plain 8, gallery 18), from a fresh clone | 2026-10-12 | the session log |
| Content trace, sample | 196 blocks traced, 0 not; every CV line on the page; 8 of 8 sources name a CV entry | 2026-10-19 | tools/check_content.py |
| Full checks | `tools/ci.py checks` on a fresh clone: exit 0 in 503 s on the seat's Windows machine; the browser checks 496 s of it (tree 48 runs, keyboard 8, joins 4, anchors 136, words 4, motion 3), 0 failures. Rerun with the default design's fonts optional, 2026-10-13: 0 failures, no anchor misses, 483 s. With axe, `tools/ci.py checks --axe` on a fresh clone of e794feb, 2026-10-16: exit 0 in 632 s; the browser checks 623 s of it (axe 36 runs), 0 failures. On GitHub's runner, 2026-10-16: every check with axe in 8 min 53 s, run 38957566173. On a fresh clone of d612b96, 2026-10-18: exit 0 in 622 s, the browser checks 614 s, 0 failures. On a fresh clone of db055e5, 2026-10-19: exit 0 in 648 s, the browser checks 634 s, 0 failures. On a fresh clone of 5a7cecf, 2026-10-19: exit 0 in 642 s, the browser checks 627 s, 0 failures; and every browser check with axe on a gallery holding ten showcase entries, 0 failures in 620 s. On a fresh clone of 3020bb4, 2026-10-20: exit 0 in 667 s, the browser checks 642 s, 0 failures; and every browser check with axe on a gallery assembled from ten real snips, 0 failures in 644 s. On a fresh clone of b17d883, 2026-10-21: exit 0 in 643 s, the browser checks 621 s (packing 12 runs), 0 failures; and every browser check with axe on a gallery assembled from 13 real snips of every shape, 0 failures in 622 s. On a fresh clone of 3fed37d, 2026-10-22: exit 0 in 665 s, the browser checks 638 s, 0 failures; and every browser check with axe on a gallery assembled from 13 real snips, 0 failures in 629 s. On a fresh clone of eb27870, 2026-10-23: exit 0 in 1,033 s on a slower hour, the browser checks 967 s, 0 failures (the tree check alone took the same 187 to 200 s before and after that commit's change). On a fresh clone of 42f5760: exit 0 in 678 s, the browser checks 648 s, the overlay among them, 0 failures. With seven designs, on a fresh clone of e669723, 2026-10-24: exit 0 in 2,042 s, the browser checks 1,997 s (tree 168 runs, keyboard 28, joins 14, anchors 476, words 14, motion 8, packing 12, overlay 4, axe 96), 0 failures; on one of 20bf01c the same day, exit 0 in 2,255 s, the browser checks 2,205 s, 0 failures, after a first try that lost Chrome's connection while the machine slept. With twelve designs, on a fresh clone of 3f65c4f, 2026-10-25: exit 0 in 3,676 s, the browser checks 3,606 s (tree 288 runs, keyboard 48, joins 24, anchors 816, words 24, motion 13, packing 12, overlay 4, axe 156), 0 failures, on the retry after hibernation broke the first. On GitHub's runner with twelve designs, 2026-10-25: 3,157 s on pull request 21, 3,020 s on its merge (run 40203263050) and 3,062 s after pull request 22 (run 40220415146), inside the 90-minute limit. Narrowed to one changed design, 2026-10-28, in a scratch clone: exit 0 in 362 s, the browser checks 286 s of it on Bento alone. On GitHub's runner with seventeen designs, 2026-10-28 and 29: every page 75.4 minutes (runs 40776363105 and 40844380486), about 4.4 minutes a design. Pull request 26 replayed under the tuned rule, its five designs and the gallery page, every check with axe: 1,982 s, the browser checks 1,827 s of it | 2026-10-12 to 29 | the session log; GitHub's API |
| Defeat cases | 176 (152 file, 24 browser) fail as built, naming what failed; 12 controls and 35 planted controls pass, on a fresh clone of 27db869, in 4,792 s, except two older cases that pull request 22's showcase entry broke, on main too; after 1e9137c both, with the five controls and five cases of their families, pass rerun each on a fresh copy, in 878 s. Gates: 27 defeat cases refused, 5 controls passed, on a clone of 3f65c4f (2026-10-25) | 2026-10-28 | tools/prove_checks.py; the session log |
| Speed, sample site | Lighthouse 13.5.0, default mobile, median of five, served uncompressed from 127.0.0.1 (GitHub Pages compresses), Chrome 154 on the seat's Windows machine. Default design with font-display: optional (as committed), 2026-10-13: LCP 2,108 ms, CLS 0, TBT 40 ms (runs 174, 37, 40, 46, 25), 197,433 bytes. The same design with swap, 2026-10-12: LCP 2,179 ms, CLS 0, TBT 195 ms (runs 195, 248, 280, 22, 64). Plain, 2026-10-12: LCP 1,389 ms, CLS 0.048, TBT 0 ms, 79,399 bytes. ADR-0009's limits: 2,500 ms, 0.1, 200 ms | 2026-10-12 and 13 | the session log |
| Showcase screenshots | Full-screen snips of four pages, a wall of photographs among them, by headless Chrome 155 and re-encoded by Windows' WIC and GDI+: at full HD up to 2,525,046 bytes, at 4K up to 12,439,711, on a 5K display up to 16,928,260 (all the photo wall, GDI+); the cap is 20 MiB. Their served copies, WebP at 0.82: the card at most 147,498 bytes, the full view 401,498 | 2026-10-20 | the session log, Round 9 |
| Gallery with a showcase | 0, 10 and 50 cards packed in their pictures' shapes, copies drawn from 13 real snips of every shape, the owner's among them: page 4,729, 10,383 and 32,599 bytes, gallery.js 3,094; Lighthouse 13.5.0 default mobile, median of five: LCP 1,075, 1,504 and 1,654 ms, CLS 0 in every run, TBT 38, 0 and 0 ms, 74,587, 309,817 and 330,177 bytes loaded at first; desktop preset, three columns packed, at 10 and 50: LCP 365 and 406 ms, CLS 0 in every run, TBT 0; every card, scrolled to the end, 2,964,813 bytes at 50 | 2026-10-21 | the session log, Round 10 |
| Showcase shapes | First screens 0.56 to 0.62 times as tall as wide on desktops and laptops, 2.16 to 2.22 on phones; ultrawide monitors 2.39 and 3.56 times as wide as tall; whole pages of eight portfolio sites 0.56 to 10.21 at desktop widths, 2.16 to 34.76 at a phone's; the owner's snip 1.59. Limits set at 2.4 either way. Card copies at most 1,024 wide: the largest 128,784 bytes | 2026-10-21 | the session log, Round 10 |
| Decision records | 17: 16 accepted, 1 proposed (ADR-0012, held by the owner) | 2026-10-23 | docs/decisions/ |
| Gallery picture | The gallery page's top, 1366 by 1280 CSS pixels at full size, WebP: 89,268 bytes, the heading, the links and the first row of templates; the limit is 300 KB | 2026-10-23 | tools/screenshots.py; the session log |

## How it was built

Every decision is a record in docs/decisions/, and what each session did
is in logs/.

| Date | What changed |
|---|---|
| 2026-10-12 | The engine copied by file from the owner's site at 5f3b84d and generalised; sample content; the default and plain designs; the gallery; the file and browser checks with their defeat cases; the gates; the workflows; the documents. Not published |
| 2026-10-15 to 16 | The owner's answers applied: records 0006 to 0011 accepted, 0013 and 0014 written; axe-core in the checks workflow; the Code of Conduct's contact, allowed by gate A in that file alone; the Chrome launcher's start made safe. Not published |
| 2026-10-16 | Published by the owner; the gallery live. The deploy job, skipped in every site-mode run, found by the architecture chat and fixed; the workflow check added |
| 2026-10-17 to 18 | Every setup step and Tests 1 to 4 followed by the owner; main protected by a ruleset; the setup guide corrected from what the run showed |
| 2026-10-18 | A design says in design.json whether it offers dark; a light-only design's page stays light with no Dark switch. CAPABILITIES' architecture lane kept out of the repository |
| 2026-10-18 | A copy of the template cleans itself up once: the project's own files removed by a workflow, listed in the user guide for a copy whose cleanup did not run |
| 2026-10-19 | A failed content trace names the CV's line and what to do; the user guide puts the CV first |
| 2026-10-19 | The gallery's templates first, then a showcase of contributors' own sites, checked as files and by response, never rendered, on each pull request and weekly; the footer credit names the design and its author |
| 2026-10-20 | A showcase screenshot is any snip, as its tool saved it; the deploy draws small copies from it, with no metadata, and never publishes the file |
| 2026-10-21 | Showcase cards in their pictures' own shapes, packed as on Pinterest; one pull request template for a design or a showcase entry; the briefs folder off the repository |
| 2026-10-22 | The README routes every visitor and carries a checked prompt for their AI assistant; Showcase entry and Question forms; borderless showcase cards with rounded pictures |
| 2026-10-23 | AGENTS.md routes coding agents, and a copy receives its own; a copy's README carries a short prompt for its owner's AI; the deploy takes a picture of the gallery page, which leads the README |
| 2026-10-23 | A copy's first Deploy ends with a notice, not red, while GitHub Pages is off, and its README leads with turning Pages on; a showcase card's larger copy opens in an overlay that can be closed |
| 2026-10-24 | Five designs of the owner's join the templates, Bento, Broadsheet, Console, Poster and Signal; Plain raised to the same standard; all seven credited to him and maintained by the project |
| 2026-10-24 | Five more, each for a profession and shown with its own invented person: Sentinel for security, Latent for machine learning, Pocket for mobile, Assert for QA, Pipeline for DevOps; a template may carry a sample person of its own |
| 2026-10-28 | Five more for professions, each held to a measured bar of distinctness: Cyanotype for embedded and robotics, Handbook for technical writers, Frost for frontend developers, Savepoint for game developers, Broadcast for developer advocates; each sample person with their profession's own sections; a site with a section left out builds |

## What it does not do, and its limits

**Excluded by decision:** the scope floor, ADR-0001: no owner's content
beyond a credit line; no cookies, tracking, analytics or requests to
another origin; every word in the initial HTML; no paid service; no
dependency without a record; designs are CSS only (ADR-0006).

**Limits, as measured or known on 2026-10-12:**

- **Proven on GitHub, 2026-10-16 to 18**: Checks (9 minutes on a push,
  13.5 on a design's pull request), Deploy in gallery mode and, in a
  template copy, in site mode, and the scope check (4 to 6 seconds), with
  Chrome run without its sandbox (ADR-0010). Step 5's policy for the
  scope check is proven only by a run on or after 2026-11-02, when GitHub
  starts enforcing its block.
- **Light only, or light and dark, by the design's word.** A design says
  in design.json whether it offers dark (ADR-0006, Changes, 2026-10-18).
  A design that does not offer dark has one theme, the same on every
  device, and no Dark switch: light, or dark where its own CSS says so,
  as Console's does; one that offers dark follows the device and carries
  the switch, and is checked in both.
- **`pull_request_target` needs the owner's Actions policy.** GitHub blocks
  it by default in public repositories from 2026-11-02; without the policy
  the scope check stops running (docs/setup-on-github.md, step 5).
- **Anchors and web fonts.** With `font-display: swap`, the default design's
  anchors landed 16 to 40 px off on about 1 load in 100, when its fonts
  arrived after the jump. With `font-display: optional`, as committed since
  2026-10-13: none in 272 loads. The owner kept optional on 2026-10-15
  (ADR-0014): on a slow first visit the fallback font stays for that
  page view.
- **Blocking time varies by run on this machine**: the default design's
  median was 195 ms one evening (single runs up to 280 ms) and 40 ms the
  next morning, against ADR-0009's 200 ms. It passed both times as a
  median; under ADR-0009 a fail on any machine is a fail.
- **One degree on the timeline**; English labels; eight sections in a
  fixed order (docs/reference/content.md).
- **Tested in Chrome on Windows only**, 154 to 156. No other browser, and
  no screen reader by ear: the joins check is a model of NVDA, validated
  on the owner's site's known-bad page.
- **The showcase's packing, 2026-10-21.** Only Safari 26.4 and later
  ships CSS grid-lanes (caniuse: 12.49% of users); Chrome's own, behind
  its experimental flag, is what the checks run, and it placed the cards
  as gallery.js does, within 1 px. Elsewhere gallery.js packs them; with
  scripts off and no grid-lanes, the cards sit in rows, with gaps under
  the shorter ones, in the same order.
- **Speed is checked locally, not in CI**, while ADR-0012 is proposed.
  Contrast is checked in CI by axe-core (ADR-0011).

## Where the evidence lives

| Question | File |
|---|---|
| How to use it | README.md, docs/how-to/use-this-template.md |
| How to contribute a design | CONTRIBUTING.md, docs/how-to/add-a-design.md |
| How to build and check it | docs/reference/commands.md |
| What exists now, and what is blocked | STATE.md |
| Why it is shaped as it is | docs/decisions/ |
| The checks and their defeat cases | docs/reference/standing-checks.md |
| Where the engine came from | docs/reference/provenance.md |
| What each session did | logs/README.md |
| What was deliberately not done | docs/deferred/ |
| Every documented file | MAP.md |

## Keeping this file current

At the close of any session that changes a capability or a measured
number: update its section and the date at the top; re-measure a number
rather than carrying it forward, with its new date and source.
