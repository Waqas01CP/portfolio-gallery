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
- A4. Ordinary screenshots fit the limits. **Measured** 2026-10-19:
  first screens of the gallery's two designs and two live portfolio
  sites, captured by headless Chrome and re-encoded by Windows' own GDI+
  and WIC encoders, were at 1280 by 720 at most 477 KB as PNG, 122 KB as
  JPEG and 68 KB as WebP; at 1920 by 1080 at most 657 KB as PNG, 202 KB as
  JPEG and 108 KB as WebP; at 2560 by 1440, a Retina Mac's density, 158 KB
  to 1.40 MB as PNG.
- A5. Ordinary screenshots carry metadata. **Measured** 2026-10-19:
  Windows' GDI+ JPEG encoder writes an EXIF block of three resolution
  tags; two Mac screenshots from public repositories carry an eXIf chunk
  and an XMP block saying "Screenshot", one with Apple's iDOT chunk. A
  rule against all EXIF and XMP would refuse them; a location is what
  could harm a contributor.
- A6. The gallery stays within ADR-0009's limits with a full showcase.
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
with bands in the card's colour, loading as it scrolls into view, and
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
  few entries (A6), within ADR-0009's limits.
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
