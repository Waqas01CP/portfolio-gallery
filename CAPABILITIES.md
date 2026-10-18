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

**Current as of 2026-10-18 UTC**, written by the implementing seat in its
lane: what the system does and how, the stack, the qualities, the numbers,
the limits, and the timeline's rows for what was built. **The architecture
chat's lane is not yet written**: the problem the project solves, where it
is going, the decisions it restates and the owner's role are for the
chat this repository will have once it is published (the owner's decision
of 2026-10-10). Until then the brief that started it and the records stand
in.

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
and merged only by the owner. It costs nothing to run: GitHub's free
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
   design on the same content, each at `designs/<name>/`, and a gallery
   page.
3. **Checks before publishing.** The built files (no load from another
   origin, the policy tag, links resolve letter for letter) and the content
   trace; a failure publishes nothing.
4. **Previews** (the gallery only). Headless Chrome takes each design's
   first screen in a job with no write token; only checked WebP files
   reach the published site (ADR-0010).
5. **Publish.** GitHub Pages, from the deploy workflow's artifact.
6. **In the browser.** The page is whole without scripts. site.js closes
   the "In depth" panels, runs the timeline's lane filters and cards, the
   section menu, the progress marker and a light or dark switch for the
   visit, and the effects a design turns on: a 3D knot drawn in a worker,
   card tilt, a moving strip with a pause control, scroll effects. Under
   reduced motion nothing moves.
7. **Contributions.** A design pull request passes the scope check (from
   the default branch, reading only the file list), the design checks and
   the browser checks on every design, then the owner's review (ADR-0006).

## How data is stored, and where it may go

- **No database, no server code.** Content is four files in the user's
  repository; the site is static.
- **Nothing about a visitor is kept.** No cookies, no storage, no
  requests to another origin; the Content-Security-Policy in every page
  refuses them even if a check misses one.
- **The owner's private material never enters the repository.** Gate A
  refuses his name outside LICENSE and README.md, his personal email
  addresses anywhere, the Code of Conduct's contact address outside
  CODE_OF_CONDUCT.md, and his private folder name, from a pattern file in
  git's own folder that is never committed (ADR-0008, ADR-0002).

## Tech stack

| Area | What is used |
|---|---|
| Build | Python 3.12 in a venv; Jinja2 3.1.6 and MarkupSafe 3.0.3, pinned with the SHA-256 of every file PyPI serves (ADR-0004) |
| Page | HTML, CSS and plain JavaScript; no framework |
| Designs | `default`: Manrope, JetBrains Mono and Instrument Serif under the SIL Open Font License, none reserving a name (checked in each WOFF2's name table, 2026-10-12); `plain`: system fonts |
| CI and hosting | GitHub Actions on ubuntu-24.04 and GitHub Pages, free for public repositories; every action pinned to a full commit SHA |
| Browser checks and previews | Google Chrome, driven over its DevTools protocol by tools/cdp.py, standard library only (ADR-0010) |
| Accessibility rules in CI | axe-core 4.14.0 from npm, MPL-2.0, fetched by exact version in the checks workflow and checked against the registry's SHA-512 before it runs; never shipped in a site (ADR-0011) |
| Proposed, not added | Lighthouse 13.5.0 (ADR-0012), run only locally from a scratch folder; held as proposed by the owner on 2026-10-15 |

## Engineering qualities, and what enforces each

| Quality | What enforces it |
|---|---|
| A design cannot run code or load from elsewhere | The design format (ADR-0006); tools/check_design.py; the scope check; the page's Content-Security-Policy |
| A workflow job runs when it should | tools/check_workflows.py: a job after one that can be skipped must say when it runs, or GitHub skips it too and reports success |
| A pull request cannot change how it is checked | scope.yml on `pull_request_target`, from the default branch; it fails any change outside one design folder |
| Every word in the first response, readable without scripts | The fixed HTML; the words check compares every design with no design, scripts off |
| Accessibility, for every design | The standing checks: the tree at load, keyboard, joins, anchors, words, motion, and axe-core's rules, contrast among them (docs/reference/standing-checks.md) |
| A check can fail | tools/prove_checks.py runs each on its defeat case: 43 file cases and 9 browser cases, with 9 controls |
| Claims trace to the user's CV | tools/check_content.py, page to CV and CV to page |
| Deterministic output | Two builds compared byte for byte in CI |
| Nothing private published | Gates A to E; the pre-publish search |

## Measured numbers

| What | Value | Date | Source |
|---|---|---|---|
| Source | build.py 1,019 lines; 12 tools, 3,798 lines; 13 templates, 566 lines; scripts and engine styles 871 lines; designs: default 1,521 lines of CSS, plain 251; workflows 237 lines | 2026-10-16 | `wc -l` |
| Sample site, built | index.html 39,195 bytes (6,239 gzipped); site.js 22,481 (7,219); knot.js 5,715 (2,256); base.css 3,099 (1,489); layout.css 1,947 (562); default design.css 49,498 (11,160); fonts 78,396 | 2026-10-12 | `wc -c`; Python's gzip, level 6 |
| Gallery page | 3,778 bytes (1,485 gzipped); plain design.css 11,678 bytes | 2026-10-12 | same |
| Builds | site in each design and the gallery: exit 0, twice each, byte-identical (default 14 files, plain 8, gallery 18), from a fresh clone | 2026-10-12 | the session log |
| Content trace, sample | 196 blocks traced, 0 not; every CV line on the page; 8 of 8 sources name a CV entry | 2026-10-12 | tools/check_content.py |
| Full checks | `tools/ci.py checks` on a fresh clone: exit 0 in 503 s on the seat's Windows machine; the browser checks 496 s of it (tree 48 runs, keyboard 8, joins 4, anchors 136, words 4, motion 3), 0 failures. Rerun with the default design's fonts optional, 2026-10-13: 0 failures, no anchor misses, 483 s. With axe, `tools/ci.py checks --axe` on a fresh clone of e794feb, 2026-10-16: exit 0 in 632 s; the browser checks 623 s of it (axe 36 runs), 0 failures. On GitHub's runner, 2026-10-16: every check with axe in 8 min 53 s, run 38957566173 | 2026-10-12, 13 and 16 | the session log; GitHub's API |
| Defeat cases | 52 (43 file, 9 browser, axe's among them) fail as built, naming what failed; 9 controls pass. 47 cases and 8 controls on a fresh clone of e794feb in 934 s; the 5 workflow cases and their control on 1f14aa7's tree. Gates: 19 defeat cases refused, 4 controls passed | 2026-10-15 and 16 | tools/prove_checks.py --browser --axe; the session log |
| Speed, sample site | Lighthouse 13.5.0, default mobile, median of five, served uncompressed from 127.0.0.1 (GitHub Pages compresses), Chrome 154 on the seat's Windows machine. Default design with font-display: optional (as committed), 2026-10-13: LCP 2,108 ms, CLS 0, TBT 40 ms (runs 174, 37, 40, 46, 25), 197,433 bytes. The same design with swap, 2026-10-12: LCP 2,179 ms, CLS 0, TBT 195 ms (runs 195, 248, 280, 22, 64). Plain, 2026-10-12: LCP 1,389 ms, CLS 0.048, TBT 0 ms, 79,399 bytes. ADR-0009's limits: 2,500 ms, 0.1, 200 ms | 2026-10-12 and 13 | the session log |
| Decision records | 14: 13 accepted, 1 proposed (ADR-0012, held by the owner) | 2026-10-16 | docs/decisions/ |

## How it was built

**Seats.** The owner, Waqas01CP, decided scope and every non-trivial
choice; the implementing seat, Claude Code, built to a brief written by
his site's implementing seat and amended by his site's architecture chat.

| Date | What changed |
|---|---|
| 2026-10-12 | The engine copied by file from the owner's site at 5f3b84d and generalised; sample content; the default and plain designs; the gallery; the file and browser checks with their defeat cases; the gates; the workflows; the documents. Not published |
| 2026-10-15 to 16 | The owner's answers applied: records 0006 to 0011 accepted, 0013 and 0014 written; axe-core in the checks workflow; the Code of Conduct's contact, allowed by gate A in that file alone; the Chrome launcher's start made safe. Not published |
| 2026-10-16 | Published by the owner; the gallery live. The deploy job, skipped in every site-mode run, found by the architecture chat and fixed; the workflow check added |
| 2026-10-17 to 18 | Every setup step and Tests 1 to 4 followed by the owner; main protected by a ruleset; the setup guide corrected from what the run showed |

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
- **A design that sets no colours fails in dark mode.** The page declares
  light and dark, so on a device set to dark such a design gets the
  browser's dark defaults and fails axe's contrast rule; `:root {
  color-scheme: light; }` keeps it light. Whether the contract should ask
  every design for dark, or the engine change, is the owner's to decide
  (2026-10-18).
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
- **Tested in Chrome 154 on Windows only.** No other browser, and no
  screen reader by ear: the joins check is a model of NVDA, validated on
  the owner's site's known-bad page.
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
