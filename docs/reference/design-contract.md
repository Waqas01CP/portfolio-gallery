---
type: reference
description: "What a design styles: the engine's fixed HTML, its classes and states, the custom properties the engine sets and reads, what base.css guarantees, and the rules the checks hold every design to. Read before writing or reviewing a design."
status: current
---

# The design contract

A design is one stylesheet, `design.css`, on HTML that is the same for
every design (ADR-0006). To see the HTML, build the site and open
`_site/index.html`, or open any gallery demo and view its source. The
`plain` design is a short worked example of covering all of it;
`default` is the full one.

## Load order

Each page loads, in order: the design's `design.css`; the engine's
`static/base.css`; `static/layout.css`, which the build writes from the
content. base.css comes after the design, so on equal terms its rules win.

## The page

```
body
  a.skip                                  skip link (base.css places it)
  nav.dnav.dark         "Sections"        the menu as a bar: links, theme switch
  div.rail.dark         aria-hidden       a progress rail, decoration
  nav.mbar.dark         "Sections"        the menu as a phone bar, a <details>
  main#main
    section#intro.intro.dark              always first
    div.page
      section#projects.sec               each section that has content,
      section#timeline.sec               in this order; a section with
      section#work.sec                   nothing to show is left out,
      section#education.sec              with its menu entry
      section#certifications.sec
      section#skills.sec
      section#contact.sec.sec-last
  footer.foot
```

**Show exactly one of `.dnav` and `.mbar` at each width.** Both are named
"Sections"; the tree check fails a page that exposes two, or none.

Every section opens with `header.sec-head`: a decorative `.fade-word`
(aria-hidden), and `.sec-title` holding `.sec-n` (aria-hidden) and the
`h2`.

## The sections

- **Intro**: `.intro-glow`, `canvas.knot` (both aria-hidden), `.avail`,
  `h1.intro-name` (two `span`s, the second `.serif`), `.headline`,
  `.intro-grid` with `.intro-main` (`.facts`, `.lede` paragraphs, `.cta`
  buttons) and `ul.results` of `li.result` cards (`.result-label`,
  `.result-fig` with `.result-num`/`.result-suffix` or `.result-word`, and
  `.result-text`), then `.strip` with `.strip-static`.
- **Projects**: an optional `.feature` (`.feature-label`, `.feature-main`
  with `.feature-num` and `.feature-text`, `ul.feature-pairs`,
  `.feature-note`), then `.proj-grid`: for each project `article.proj`
  (`.proj-lead` for tier 1) with `.proj-body`, `.proj-head` (`.proj-dates`,
  `h3`, `.proj-sub`, `.proj-summary`), `.proj-side` (`.proj-fact`,
  `ul.chips.chips-mono`, `.proj-actions` with `.btn` links and
  `button.depth-toggle`), followed by its panel `div.depth` (`.depth-head`,
  `ol.depth-list` with `.depth-n` numbers, aria-hidden).
- **Timeline**: `div.tl#tlx-grid` with `.tl-lanes` (`.tl-head`,
  `.tl-filters` of `button.tl-filter.lane-<lane>`, `.tl-scale`),
  `.tl-empty`, and `.tl-body` holding `.tl-axis` (aria-hidden: `.tl-spine`,
  `.tl-month`, `.tl-year`, `.tl-year-line`, `.tl-read`) and `ol.tl-list`:
  `li.tl-band` for the degree and `li.tl-entry.lane-<lane>` for the rest,
  each with `details.tl-card` (`summary` with `.tl-meta`, `.tl-dates`,
  `.tl-title`, `.tl-org`; `.tl-pop` with `.tl-close`, `.tl-detail`,
  `.tl-links`). Lanes are `builds`, `work` and `certifications`; entries
  also carry `after-band`, `in-band` or `before-band`.
- **Work**: `.jobs` of `article.job` (`.job-head` with `.job-top`, `.tile`,
  `.job-dates`, `h3`, `.job-org`, `.job-loc`, `.job-links`; `ul.job-list`).
- **Education**: `article.degree` (`.degree-head`, `.degree-org`,
  `.degree-cgpa`, `.degree-courses` with `ul.chips.chips-soft`).
- **Certifications**: `ul.certs` of `a.cert`, `.cert-acc` and `.cert-ink`
  alternating (`.cert-flood`, `.cert-top`, `.cert-name` with `.cert-title`
  and `.cert-org`, `.cert-view`).
- **Skills**: `ul.skills` of `li.skill` (`h3` with `.skill-n`,
  `ul.chips.chips-soft`).
- **Contact**: `ul.routes` of `a.route.route-<n>`, `.route-mail` on an
  email address (`.route-top` with `.route-icon`, `.route-body` with
  `.route-label`, `.route-line`, `.route-addr`).
- **Footer**: `.foot-name`, `.foot-loc`, `.foot-link`s, `.foot-demo` in a
  gallery demo, `.foot-credit`.

Shared pieces: `.wrap` (the content width), `.btn`, `.btn-acc`, `.btn-sm`,
`.chips`, `.serif`, `.mono`, `.i` (inline icons, aria-hidden), `.glare`
(on `[data-tilt]` cards).

## States to style

- `html.js`: the script has run. Controls that need it start `hidden`.
- `html[data-theme="dark"]` or `[data-theme="light"]`: the visitor's switch,
  for this visit. Without it, follow `prefers-color-scheme`.
- `.dark`: on the Intro and the menus, which the default design sets dark.
- `button.depth-toggle[aria-expanded="true"]`, `.proj.is-open`: a panel is
  open. `details[open]`, `.tl-entry.is-open`: a timeline card is open.
- `.tl[data-hide~="<lane>"]`: lanes switched off (base.css hides them).
- `a[aria-current]` in the menus: the section in view.

## Custom properties

The engine sets these; a design reads them.

| Property | Where | Meaning |
|---|---|---|
| `--span-wide`, `--span-mid` | each `article.proj` | grid columns of six, three or two cards to a row |
| `--rows` | `#tlx-grid` | timeline rows, four per month |
| `--row`, `--span` | each `.tl-entry`, `.tl-band`, `.tl-month`, `.tl-year` | a grid row and its length |
| `--x`, `--w`, `--gl`, `--gr` | each `.tl-entry` | its share of the lane, and its gutters, when entries overlap |
| `--p`, `--t`, `--mx`, `--my`, `--pop` | set by site.js | progress, tick position, pointer position, a card's popover offset |

A design sets these on `:root`; the engine reads them. 1 or unset means
on, 0 off.

| Property | Turns |
|---|---|
| `--pg-knot` | the 3D knot in the Intro (also off if `canvas.knot` is not displayed) |
| `--pg-tilt` | cards tilting toward the pointer |
| `--pg-strip` | the moving availability strip |
| `--pg-scroll` | the timeline's reading line and the faded words' drift |
| `--pg-theme` | the theme switch |
| `--knot` | (on `.intro`) the knot's colour |

## What base.css guarantees

`[hidden]` is not displayed; `.vh` text is hidden from sight and still
read, keeping its spaces; the skip link appears on focus; off-screen
sections skip their layout, with the `:target` undo; switched-off lanes
are hidden; under `prefers-reduced-motion` nothing animates or
transitions.

## The rules every design is checked against

- Files: see ADR-0006 and tools/check_design.py. No `@import`; `url()`
  only to the design's own `fonts/` and `img/`.
- **Keep every word.** A design may not hide content or add text: with
  scripts off and every disclosure open, the page's words under the design
  equal its words with no design at all. Decorative generated content
  takes empty alternative text, `content: "+" / ""`, so it stays out of
  the tree. List markers are exempt, but see the next rule.
- **The same page at load.** Anything a screen reader would meet only once
  a section is laid out fails the tree check: list markers in a skipped
  section are the known case (the plain design draws none).
- **No words run together.** Pieces of one line laid out as separate boxes
  need the hidden spaces the HTML carries; a design that lays out as boxes
  pieces the HTML joins without one fails the joins check.
- **Nothing moves under reduced motion**, whatever `!important` says.
- One "Sections" menu at each width; anchors land at their target; no
  request leaves the site.
