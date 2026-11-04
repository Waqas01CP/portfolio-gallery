---
status: proposed
topic: hosting
description: "The gallery page carries Open Graph and X card tags naming its own address and a committed picture, src/social-card.jpg, so a shared link shows a preview; a copy's cleanup removes the picture and with it the tags, and no site carries them. Read before changing the gallery page's head, its picture, or giving a site link previews."
date: 2026-11-04
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0022: A link preview for the gallery page

## Context and Problem Statement

The owner is adding the gallery's address to his LinkedIn profile's
Featured section. Read by his resume chat on 2026-11-03, the page set no
Open Graph tags, so LinkedIn showed no picture. A site that shows a shared
link reads the page's og: tags, whose addresses must be absolute; every
URL the engine writes is relative to the page and names no address of its
own (ADR-0007). The deploy's picture of the gallery page, preview.webp, is
WebP, which LinkedIn does not list.

## Decision Drivers

- Brief 16 of 2026-11-03 UTC, from the portfolio architecture chat via the
  owner: the four og tags, og:type website and an X card on the gallery
  page, og:url and og:image absolute; the picture the seat made on
  2026-10-29; a copy must not inherit it; any count kept from going stale.
- ADR-0007: one build works at any address, with nothing to configure.
- ADR-0001 line 1: a copy receives none of the owner's details, read as
  protecting the template.

## Assumptions

- A1. LinkedIn's sharing needs og:title, og:image, og:description and
  og:url, the picture at least 1200 by 627 pixels and at most 5 MB, 1.91:1
  recommended. **Sourced**: "Make your website shareable on LinkedIn"
  (answer a521928), read 2026-11-04: "Max file size: 5 MB", "Minimum image
  dimensions: 1200 (w) x 627 (h) pixels", "Recommended ratio: 1.91:1".
  The page lists file types, "JPG, PNG, or GIF", only for single image
  ads, not for shared links; JPEG is in both.
- A2. X reads the og: tags where its own are missing, but needs
  twitter:card to show a large picture. **Sourced, at one remove**: X's
  developer documentation, "Cards markup" and "Getting started with
  Cards", in a search's excerpts on 2026-11-04: "it first checks for the
  Twitter-specific property, and if not present, falls back to the
  supported Open Graph property"; the pages answered this seat's fetch
  with 402 and 404, so not read whole.
- A3. The picture is 2560 by 1280 pixels, 365,061 bytes, a JPEG holding a
  JFIF header and a colour profile and no EXIF, XMP or comment; it shows
  the title over the gallery's own design previews, every person in them
  invented, and no count. **Measured** 2026-11-04 (its segments read; the
  picture viewed). Made by the seat on 2026-10-29 from the gallery's
  previews, lettered in the Default design's Manrope and Instrument Serif,
  both under the OFL.
- A4. LinkedIn shows a 2:1 picture cropped a little toward 1.91:1.
  **Believed**, from the brief; LinkedIn's page does not say. The owner's
  Post Inspector run after the merge shows it.
- A5. The gallery is published only at
  https://waqas01cp.github.io/portfolio-gallery/. **Measured**: the deploy
  builds the gallery only where the variable PORTFOLIO_GALLERY is true,
  set only in the project's own repository (.github/workflows/deploy.yml);
  the address answered on 2026-10-16 (the session log, Round 3).

## Considered Options

- A committed picture, tags on the gallery page only, its address fixed
  in build.py (chosen)
- A JPEG of the gallery page taken by the deploy in Chrome, as
  preview.webp is
- The address from the deploy, as configure-pages gives it

## Decision Outcome

Chosen option: "A committed picture, tags on the gallery page only", because
it gives the preview the brief asks for with one file and no new job, and
leaves every site and every copy as it was.

We will commit the picture as src/social-card.jpg and have build.py
publish it at the gallery's root as social-card.jpg.
We will write in the gallery page's head, while that file is in the tree,
og:type website, og:url, og:title, og:description, og:image with its
type, width, height and alt, twitter:card summary_large_image and
twitter:image:alt, with og:url the gallery's address,
GALLERY_URL in build.py, and og:image that address and social-card.jpg.
We will give the description tag and og:description one text, its count
of designs the build's own, and say what is true of the designs: checked
automatically, and welcome by pull request, not each contributed by one.
We will list src/social-card.jpg in the template cleanup's remove.txt, so
a copy's gallery carries no preview naming the project's address.
We will have tools/check_built.py refuse a gallery page without the
preview while the picture is in the tree, and with one once it is not;
any tag missing, or an address not the project's; the picture missing,
not a JPEG, smaller than 1200 by 627, over 5 MB, not the size its tags
state, or holding any block beyond its image and colour profile; a count
of designs in a description that is not the number shown; and any
preview on another page, a site's among them.

This reads ADR-0007 as leaving these tags outside it: they are neither
loaded nor linked by the page, but read by other sites, which need them
absolute; the gallery's address is the project's, fixed in build.py as
PROJECT_URL is, so nothing is configured and a local build and a
deployed one stay identical, ADR-0007's reason. The owner's acceptance of
this record confirms that reading.

### Consequences

- Good: a shared link to the gallery shows its picture and its words on
  LinkedIn, X and the sites that read Open Graph.
- Good: the count in the description cannot go stale; a copy and every
  site are unchanged.
- Bad: the picture is a fixed image; a new design does not appear on it
  until it is remade. It names no count, so it does not go wrong.
- Bad: a site that caches previews, LinkedIn among them, shows the old
  one until asked again, as by its Post Inspector.
- Neutral: the page grows by eleven meta tags; it loads nothing more.

### Confirmation

Defeat cases in tools/prove_checks.py, each failing check_built as built:
og:image left out; og:image relative to the page; the picture 1200 by
600; over 5 MB; carrying EXIF; its stated width not its own; a count of
16 designs; the gallery without its preview while the picture is here; a
copy's gallery keeping it once the picture is gone; a site page with an
og: tag. A control: a copy's gallery, the picture removed, passes. The
template cleanup's check shows a copy loses the picture and its gallery
still passes. **Live only:** after the merge, LinkedIn's Post Inspector
on the address shows the picture, the title and the description.

## Pros and Cons of the Options

### A committed picture, the address fixed

- Good: one file; the picture made to be read small.
- Bad: remade by hand when the gallery changes much.

### A JPEG of the gallery page from the deploy

- Good: always current.
- Bad: a page's first screen read at a thumbnail's size shows small text
  and little else; a new picture job and its checks.

### The address from the deploy

- Good: right for any repository that publishes a gallery.
- Bad: a local build and a deployed one differ, which ADR-0007 refused;
  only the project's own repository publishes a gallery.

## More Information

- Not built: link previews on a copy's own site. Each needs its absolute
  address and a picture of at least 1200 by 627. The address could be a
  setting in content/config.json, against ADR-0004's one setting and
  ADR-0007's nothing to configure, or given by the deploy, which ADR-0007
  refused for differing builds; the picture could be a file in content/,
  or taken by the deploy in Chrome, which a copy's deploy does not run
  today. Its words would come from site.json's name and headline, as its
  description tag's do now. It waits on the owner (Brief 16).
- The picture's sources stay outside the repository; the picture is the
  only part committed.

## Changes

| Date | Change | Why |
|---|---|---|
