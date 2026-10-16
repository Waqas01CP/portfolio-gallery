---
type: reference
description: The checks every change and every design runs, each with its pass line and the case built to defeat it, and where each runs. Read before adding, changing or trusting a check.
status: current
---

# Standing checks

Every check here ran first on its defeat case, and counts as a pass only
once that case has failed. A check whose defeat case passes is unproven.
The proofs of 2026-10-12, 13 and 15 are in `logs/2026-10-12-brief-1-build.md`.

| Check | Tool | Runs | Pass | Defeat case |
|---|---|---|---|---|
| Designs | check_design.py | gate B, CI | Only allowed files, within size, design.json complete, CSS with no @import, no url() outside the design, nothing that loads or runs | A .js file; an .svg; `@import`; `@\69mport`; `url(https://...)`; `url(../..)`; a 101 KB stylesheet; no author_url |
| Scope | scope_check.py | CI, `pull_request_target` | Every changed path in one designs/<name>/ folder, of an allowed type, not a maintained design | A path in tools/; two designs; a .js file in a design |
| Build twice | ci.py checks | CI | Two builds of the site and of the gallery byte-identical | Output that depends on the clock or file order |
| Built files | check_built.py | gate B, CI, deploy | The policy tag first; nothing loaded from another origin; no inline script or style; links resolve, letter for letter; hidden markup inside sections also aria-hidden | A planted image from example.org; a root-relative path; a `hidden` element without aria-hidden |
| Content trace | check_content.py | gate B, CI, deploy | Every block traces to the CV; every CV line reaches the page; every source names an entry | A number changed on the page; a date style the CV does not use |
| Tree at load | check_browser.py | CI | Full accessibility mode: the tree equals the page without layout skipping, at 360 and 1366 px, light and dark, scripts on and off; default mode adds nothing; one "Sections" menu exposed | Markup hidden without aria-hidden in a skipped section; list markers there |
| Keyboard | check_browser.py | CI | Tab reaches each "In depth" control; Enter opens it and its text enters the tree; Tab moves in; Close closes it and returns focus; the control closes it; no Tab stop inside aria-hidden | The Close handler not returning focus |
| Joins | check_browser.py | CI | No two words a screen reader would read as one, at 360 and 1366 px | The owner's site at 6812c4f: 58 and 43 joins; 0 and 0 at c97b99e |
| Anchors | check_browser.py | CI | Every in-page target, by link and by address, scripts on and off, lands within 3 px of its scroll margin or at the page's end. By address, a miss of at most 32 px is loaded once more and noted if the second load lands, because a design's web fonts can arrive after the jump (with font-display: swap, the default design missed by 16 to 40 px on about 1 load in 100; with optional, none in 272; 2026-10-12 and 13) | base.css without its `:target` undo: misses of 360 to 1,163 px |
| Words | check_browser.py | CI, gallery | Every design's words equal the page's with no design | `::before { content: "..." }`; a section hidden with display: none |
| Requests | check_browser.py | CI | No request to another origin, no policy violation, no script error | A planted image from example.org; an injected inline style |
| Motion | check_browser.py | CI | Under reduced motion, no animation frame and no running animation in 3 s | A design's `!important` infinite animation |
| axe | check_browser.py --axe | CI, axe-core 4.14.0 fetched and checked by SHA-512 (ADR-0011) | axe-core's default rules: 0 violations at 360 and 1366 px, light, device dark, switched dark, panels closed and open | Faint text and an image without alt (prove_checks.py --axe); a tarball with one byte added, refused by its SHA-512 |
| Lighthouse | Lighthouse 13.5.0 | locally until ADR-0012 | Default mobile, median of five: LCP at most 2.5 s, CLS at most 0.1, TBT under 200 ms | A 600 ms synchronous script |
| Gates A to E | gates.py | every commit and push | ADR-0008 | ADR-0008's Confirmation |

## How the browser checks see the page

Each load is a fresh browsing context in a headless Chrome with its own
empty profile, served from 127.0.0.1. "Without the rule" is the built
folder with base.css's two layout-skipping lines removed; "no design" is
that folder with every design.css emptied. The tree is the DevTools
protocol's full accessibility tree, read 1.5 s after the load event.

**The tree, compared.** Two lists per tree, walked from the root: the
text nodes' text, and every other named node as role and name; whitespace
collapsed, lower-cased, empty entries dropped. Full mode must match the
reference entry for entry; default mode must add nothing.

**Why it can fail.** In a section that skips its layout, Chromium builds
the full tree at load from the DOM without the section's style: it reads
`aria-hidden`, `alt` and a `<details>`'s open state, but not what `hidden`
or CSS hides, and creates no list markers. So anything hidden inside a
section must also carry `aria-hidden` (setShown in site.js), and a design
draws no list markers there. Mechanism inferred from measurements on the
owner's site and here, not from Chromium's source.

**Joins, modelled.** NVDA's browse mode reads a line as the tree's text
pieces end to end. A line breaks at the start and end of every non-ignored
node whose element is not laid out inline; ignored nodes such as plain
spans never break one. A join is two touching pieces, neither with a space
at the touching end, where the DOM between them holds whitespace. The
model reproduced the owner's site's known-bad page (above); it is a model
of one screen reader, and a real one remains the test.

**Words.** Scripts off, so every panel is open; every `<details>` opened
through the DOM; the text of the main content and the footer, leaving out
buttons and list markers, which a design may legitimately hide or draw.
