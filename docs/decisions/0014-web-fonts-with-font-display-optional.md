---
status: accepted
topic: design
description: "The default design loads its web fonts with font-display: optional, not swap as on the owner's site, so a link to a section lands where it should and a late font never moves the text. Read before changing a design's @font-face rules."
date: 2026-10-15
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0014: Web fonts with font-display: optional

## Context and Problem Statement

The default design came from the owner's site with `font-display: swap` on
its three fonts. With swap, a font that arrives after the browser has
jumped to a linked section changes the width and line breaks of the text
above it, and the section moves: the anchors check saw misses of 16 to
40 px on about 1 load in 100. Which `font-display` should the default
design use?

## Decision Drivers

- ADR-0009: every in-page target lands where it should, and nothing
  shifts the layout.
- The look should not change for a visitor whose fonts arrive in time.

## Assumptions

- A1. With swap, anchors landed 16 to 40 px off on about 1 load in 100;
  with optional, none in 272 loads; with no web fonts, none in 136.
  **Measured**: the anchors check, 2026-10-12 and 13 (the session log).
- A2. With optional, a font that is not ready for the text's first paint
  is not used for that page view, and never moves the layout.
  **Sourced**: CSS Fonts Module Level 4, the font-display descriptor,
  read 2026-10-15: "If the font can be loaded "immediately" (such that
  it's available to be used for the "first paint" of the text), the font
  is used", and "An optional font must never cause the layout of the page
  to "jump" as it loads in."
- A3. The fonts are preloaded, so they normally arrive before the first
  paint: the gallery preview taken with optional is byte-identical to the
  one taken with swap. **Measured**: 2026-10-13 (the session log).

## Considered Options

- optional
- swap, as on the owner's site
- fallback
- No web fonts

## Decision Outcome

Chosen option: "optional", decided by the owner on 2026-10-15 UTC: "Keep
font-display: optional in the default design."

We will load the default design's fonts with `font-display: optional`.
We will advise optional to every design with web fonts
(docs/reference/design-contract.md), and keep the anchors check's one
reload of a miss of at most 32 px for a design that chooses otherwise.

### Consequences

- Positive: links to a section land; a late font never shifts the text.
- Negative: on a slow first visit the fallback font stays for that page
  view, and the browser may abort the font's download (A2's source).
- Neutral: the owner's site keeps swap; the two differ here.

### Confirmation

**The default design's three @font-face rules say optional.** Read
designs/default/design.css; its comment says why.

**Anchors land.** The anchors check passes on every pull request; a miss
of the kind swap caused fails it, or is noted when a second load lands.

## Pros and Cons of the Options

### optional

- Good: nothing moves; the same look whenever the fonts arrive in time.
- Bad: the fallback font for a slow first view.

### swap

- Good: the font always shows in the end.
- Bad: a late font moves the text under a link's target.

### fallback

- Good: a shorter window for a late font than swap's.
- Bad: a font swapped in within that window still moves the text;
  reasoned from its definition, not measured.

### No web fonts

- Good: nothing to wait for.
- Bad: the design loses its look.

## More Information

- Asked in the seat's report of 2026-10-13, question 6.8; answered on
  2026-10-15 UTC, in answers dated 2026-10-16 in his local time.

## Changes
