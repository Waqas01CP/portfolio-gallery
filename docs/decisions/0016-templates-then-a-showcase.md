---
status: accepted
topic: process
description: "The gallery shows templates first, each with an optional In use link to its author's own site, then a showcase of contributors' own sites, each a folder of one entry and one screenshot, checked as files and, never rendered, by its response on the pull request and weekly. The footer credit names the design and its author. Read before changing the showcase, its checks or limits, the gallery's order, or the credit."
date: 2026-10-19
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0016: Templates first, then a showcase of contributors' own sites

## Context and Problem Statement

The gallery showed designs anyone can use. A contributor with a portfolio
of their own, built some other way, had no place in it, and a design's
author could not show the design at work on their own site. How should
the gallery take both, with no code from contributors, without the runner
rendering their sites, and with a review load the owner can carry?

## Decision Drivers

- The owner's direction and decisions D1 to D3, 2026-10-18: templates
  first, each with an optional "In use" link; a showcase after, preview
  and link only; the showcase picture a screenshot its submitter supplies,
  checked as design images are, and the runner never loads a
  contributor's site (D1); the footer credit naming the design's author
  and this repository, both linked, still removable (D2); the showcase
  rules after emmabostian/developer-portfolios, with a scheduled check
  that flags and never edits (D3).
- His answers of 2026-10-19 to the seat's Report 7: Q1 to Q6 below.
- ADR-0001, lines 1, 2, 5 and 6; ADR-0006: a pull request from outside
  touches one folder, and the scope check reads file names only.

## Assumptions

- A1. A scheduled workflow in a public repository is disabled after 60
  days without activity, and its notices go to the user who last changed
  its cron line. **Sourced**: GitHub Docs, "Events that trigger
  workflows", read 2026-10-19.
- A2. A page that links to a profile shows that the profile's holder
  controls the page. **Sourced**: Mastodon's profile verification, read
  2026-10-19, a precedent.
- A3. A parked domain shows in the final host after redirects, and in a
  few phrases once the host has changed, without rendering. **Sourced**:
  emmabostian/developer-portfolios' parking check, read at its source
  2026-10-19, a precedent; it misses parking pages its list does not know.
- A4. No ordinary snip meets the cap of 20 MiB. **Measured** 2026-10-20
  (updated that day; it read "Ordinary screenshots fit the limits",
  measured 2026-10-19 on first screens up to 1920 by 1080, the largest a
  PNG of 657 KB): full-screen captures of five busy pages, a wall of
  photographs among them, by headless Chrome 155 at full HD, at 4K at 100%
  and 150% scaling, on a 16-inch MacBook Pro's Retina screen and on a 5K
  display, re-encoded by Windows' WIC and GDI+ encoders too, were at most
  12,439,711 bytes at 4K and 16,928,260 at 5K, both PNGs from GDI+, the
  largest of the three encoders; GitHub takes at most 25 MiB through a
  browser (GitHub Docs, "About large files on GitHub", read
  2026-10-20). The served copies made from them, WebP at quality 0.82,
  were at most 147,498 bytes for the card and 401,498 for the full view.
- A5. Ordinary screenshots carry metadata. **Measured** 2026-10-19:
  Windows' GDI+ JPEG encoder writes an EXIF block of three resolution
  tags; two Mac screenshots from public repositories carry an eXIf chunk
  and an XMP block saying "Screenshot", one with Apple's iDOT chunk. A
  rule against all EXIF and XMP would refuse them; a location is what
  could harm a contributor.
- A6. The gallery stays within ADR-0009's limits with a full showcase.
  **Re-measured** 2026-10-21, the cards packed in their pictures' shapes,
  copies drawn from 13 real snips of every shape measured, the owner's
  among them: with 0, 10 and 50 cards, Lighthouse default mobile, median
  of five, LCP 1,075, 1,504 and 1,654 ms, CLS 0 in every run, TBT 38, 0
  and 0 ms, 74,587, 309,817 and 330,177 bytes loaded at first; with the
  desktop preset, where the cards are packed in three columns, at 10 and
  50 cards LCP 365 and 406 ms, CLS 0 in every run, TBT 0, 728,686 and
  802,861 bytes at first; every card at 50, scrolled to the end,
  2,964,813 bytes. As re-measured on 2026-10-20 with served copies made from full-screen
  captures of up to 9.5 MB: with 0, 10 and 50 cards, LCP 1,128, 1,507 and
  1,656 ms, CLS 0, TBT 33, 16 and 70 ms, 70,310, 274,900 and 297,780 bytes
  loaded at first; every card at 50, scrolled to the end, 3,274,139 bytes.
  As first measured, on 2026-10-19, with the screenshots served as
  supplied:
  **Measured** 2026-10-19, Lighthouse 13.5.0, default mobile, median of
  five, served from 127.0.0.1: with 0, 10 and 50 showcase cards, LCP
  1,113, 1,149 and 1,662 ms, CLS 0, TBT 71, 54 and 38 ms; 70, 974 and
  997 KB loaded, since Chrome fetches lazy pictures some way ahead of
  the view. Every picture on the 50-card page: 7.63 MB.
- A7. Review takes a few minutes per showcase entry. **Inferred**; to be
  measured on the first entries.

## Considered Options

- One folder per person, showcase/<login>/
- One showcase.json listing everyone
- A showcase of links only, with no screenshot

## Decision Outcome

Chosen option: "One folder per person", decided by the owner on
2026-10-19 UTC (his answer Q1), with his answers Q2 to Q6.

We will take a showcase entry as showcase/<login>/entry.json and one
screenshot, where the login is the pull request author's from the event,
and refuse any other path in that pull request (ADR-0006, Changes).
We will check the screenshot's format by its first bytes, still,
landscape, between MIN_WIDTH 1,024 and MAX_WIDTH 1,920 pixels wide, at
most MAX_BYTES 500 KB, with no location in its metadata; any normal
screenshot of a first screen passes, with HD the target (Q6, A4, A5).
(Changed by the owner on 2026-10-20: any screenshot as its tool saved
it, no width, shape or name rule, a cap of 20 MiB, and served copies
made from it; see Changes.)
We will fetch each site, never render it (Q4): https with a verified
certificate at every hop, never an IP address or a private host, a 200
web page, no parking host or sale phrase, and for an entry a link from
its home page to github.com/<login> (Q5). A 403 or 429 is reported for
the owner to open by hand.
We will fetch on the pull request the sites it changes, and weekly every
site and in_use link, from a workflow that holds no permissions and
reports by failing (Q2).
We will show templates first, then the showcase, each with a count and in
folder order; a showcase card shows its screenshot whole, scaled to fit
with bands in the card's colour (since 2026-10-20 in its own shape, the
cards packed; bands only beyond the shape limits: Changes), loading as it
scrolls into view, and
opening full size on a click; contributors' links carry rel="ugc
nofollow".
We will name the design and its author in the default-on footer credit,
each linked, removable as before (D2).
We will remove showcase/ and every design's in_use from each copy with
the template cleanup (ADR-0015, Changes; Q3).

### Consequences

- Positive: a place for every contributor, a design still placed first;
  no contributor code; no site rendered by this project's runner.
- Positive: the owner's own site may be an entry, and the Default
  design's in_use may link it, while no copy receives either (Q3).
- Negative: a supplied screenshot can misrepresent its site; only the
  owner's review catches it.
- Negative: a weekly network check that can be wrong both ways, and that
  GitHub stops after 60 quiet days (A1).
- Negative: about 1 MB loads with the gallery once the showcase has a
  few entries (A6), within ADR-0009's limits. (2026-10-20: about 0.3 MB,
  with served copies.)
- Neutral: real names, links and screenshots in the repository and its
  history, though not in any copy.

### Confirmation

tools/check_showcase.py in gate B and on every pull request, with a
defeat case for each rule in tools/prove_checks.py, the response rules
proven against a local server; the scope rule's four defeat cases; the
built gallery's rules in check_built.py; the cleanup's in
check_template_cleanup.py. Setup Test 6: the owner's own entry by pull
request, as an outsider's, then the weekly workflow run by hand.

## Pros and Cons of the Options

### One folder per person

- Good: one entry per person by construction; the scope check stays a
  rule about file names; no two pull requests edit one file.
- Bad: one folder per entry.

### One showcase.json

- Good: one file to read.
- Bad: every pull request edits the same file, and the scope check,
  reading file names only, could not tell whose entry changed.

### Links only

- Good: nothing to review but an address.
- Bad: the owner's direction asks for a preview, and the runner may not
  take one.

## More Information

- emmabostian/developer-portfolios, read at its source 2026-10-19: one
  Markdown list of 2,054 entries; a submitter's checklist (loads, not
  parked); weekly link and parking checks that open issues. **Primary, a
  precedent.** Taken: the response-only parking check, the weekly
  schedule, flag and never remove. Not taken: 403 and 429 counted as
  live, unverified certificates, a borrowed browser User-Agent, actions
  pinned by tag, one shared list, an issue opened by a token that can
  write.
- GitHub Docs, "Events that trigger workflows" and "Workflow syntax",
  read 2026-10-19: **First-party documentation**.
- Mastodon, profile verification; Google Search Central, "Qualify your
  outbound links": **First-party documentation** of their own
  mechanisms.
- Apple, "How to take a screenshot on your Mac" and Preview's resize and
  export pages; Microsoft, "Use Snipping Tool to capture screenshots" and
  "Draw, Create, and Edit with Paint": **First-party documentation**, for
  the contributor's steps in docs/how-to/add-to-the-showcase.md.
- Investigated, not built: a workflow a contributor runs in their own
  fork to take the screenshot there (the session log, Round 8).

## Changes

| Date | Change | Why |
|---|---|---|
| 2026-10-20 | **A showcase screenshot is any snip, as its tool saved it.** The check keeps what every ordinary snip meets: PNG, JPEG or WebP by its first bytes, a still image, no location in its metadata; MIN_WIDTH, MAX_WIDTH and the landscape rule are gone, and the file keeps the name its tool gave it ("Screenshot 2026-10-20 at 11.30.12.png"), a choice of the implementing seat for the same aim. One cap stays, for the repository's history alone: 20 MiB, above every ordinary snip measured (A4). **The screenshot is never published:** the deploy's screenshot job decodes it in headless Chrome 155 with the GPU off, in a job with no write token, and draws two served copies, WebP at quality 0.82, never enlarged: card.webp fitting 1366 by 900 and full.webp fitting 2560 by 2560, which a click opens; each holds its image chunk alone, no EXIF, XMP or colour profile, which tools/ci.py assemble checks before anything is published. The pull request's checks make the same copies, so a file Chrome cannot read fails there. HEIF is named and refused: no browser engine the project runs reads it, and a decoder would be a dependency (scope floor line 5). No floor on size is set; the owner's review sees each screenshot. A6 re-measured. | The owner's decision of 2026-10-20 UTC, approved as proposed through the portfolio architecture chat (its Brief 9), from his aim: contributors "just take a snip and add it". The limits of 2026-10-19 asked most contributors to resize: a full-HD PNG snip of a busy page is 517 to 657 KB, and a Retina capture 2560 pixels wide. |
| 2026-10-20 | **Each showcase card takes its picture's shape, and the cards are packed as on Pinterest.** The picture is shown at the card's full width in its own proportions, whole, never cropped, and the card grows to fit it; the cards run in columns with no gap left under a short one, in folder order. "Shown whole" stays; "scaled to fit, with bands" is now the behaviour beyond two shape limits only: at most 2.4 times as tall as wide and 2.4 times as wide as tall, a 21:9 screen's shape, the most elongated first screen measured either way (below). Beyond them the picture box stops at the limit and shows the picture whole inside it, shrunk, with bands: transparent pixels in card.webp, so the card's colour shows through in either theme. Nothing is refused for its shape. **Measured 2026-10-21:** first screens are 0.56 to 0.62 times as tall as wide on desktops and laptops (StatCounter's commonest, June to August 2026: 1920x1080, 1536x864, 1366x768, 1280x720; a 1440x900 Retina), 2.16 to 2.22 on phones (414x896, 360x800, 390x844, 393x873), 2.33 on 21:9 phones; ultrawide monitors are 2.39 (3440x1440) and 3.56 (5120x1440) times as wide as tall; whole pages of eight portfolio sites, the owner's among them, run 0.56 to 10.21 times as tall as wide at desktop widths and 2.16 to 34.76 at a phone's, so no limit separates a page from a screen; it caps how tall a card grows. The owner's own snip is 1.59. **Built:** build.py reads each screenshot's size from its header, turned a quarter where its EXIF says so in PNG and JPEG, as Chrome turns them (and not in WebP, which Chrome does not turn), and reserves the card's picture at its copy's size, so the page does not shift (CLS 0, ADR-0009); card.webp is at most 1,024 pixels wide; tools/screenshots.py draws each copy at the size the build gave it and fails an entry Chrome reads at another size. The packing: CSS grid-lanes where the browser has it, which only Safari 26.4 and later ships (caniuse, 12.49% of users, read 2026-10-21; Chrome 140 to 158, Edge and Firefox behind a flag; WebKit, "Introducing CSS Grid Lanes", 2025-12-19); else static/gallery.js, which places each card in turn in the column whose bottom is highest, as grid-lanes does; with neither, rows of the same columns. Every way, no card sits above the one before it, so the eye, the keyboard and a screen reader meet the cards in folder order (scope floor line 3: every word in the HTML, the script only places). A CSS column layout was rejected: it fills down each column while focus runs across. A6 re-measured. | The owner's decision of 2026-10-20 UTC, through the portfolio architecture chat (its Brief 10), after he saw his own 1077x1713 snip shrunk narrow in the fixed box, its text unreadable: "the pinterest idea ... option A but with more add ons". The limits are the implementing seat's proposal from measurement, for the chat to check against his aim before he merges. |
| 2026-10-21 | **A showcase card has no border or panel of its own; its picture has rounded corners**, on the card colour with a hairline edge, so any bands still read as part of the picture, and the name, host and description sit beneath it on the page, as on Pinterest. The templates' cards are unchanged. | The owner's answer of 2026-10-21 to the seat's Report 10, 3.7, through the chat's Brief 11: "the seat can add the add-ons if they are not a lot of work as visuals matter"; the light ones named there. |
