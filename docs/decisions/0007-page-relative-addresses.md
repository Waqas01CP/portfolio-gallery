---
status: accepted
topic: hosting
description: "Every URL a page uses is relative to the page, so one build works at a user site's root, under /<repository>/ and under a custom domain, with nothing to configure. Read before writing any link, path or asset reference."
date: 2026-10-12
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0007: Every URL relative to the page

## Context and Problem Statement

The operator's site writes every internal link root-relative, /static/...,
because it is served at a domain's root (its ADR-0002). A copy of this
repository is served at https://<user>.github.io/portfolio-gallery/ unless
its owner renames it <user>.github.io, and the gallery's demos sit two
folders deeper still. A root-relative link breaks at every address but
the root. The build could learn the base path, `actions/configure-pages`
outputs it ("/my-repo" or ""), but then a local build and a deployed one
would differ, and a site moved to a custom domain would need a rebuild.

## Decision Drivers

- ADR-0004: a user configures nothing beyond one design setting.
- The brief of 2026-10-11: "The engine must work at both."

## Assumptions

- A1. `actions/configure-pages` outputs base_url, origin, host and
  base_path. **Sourced**: its action.yml at v6.0.0
  (45bfe0192ca1faeb007ade9deae92b16b8254a0d), read 2026-10-12.
- A2. A browser resolves a worker script's URL against the URL given, and
  a CSS url() against the stylesheet's own URL. **Sourced** from the HTML
  and CSS specifications as commonly implemented; **measured** 2026-10-12:
  the knot's worker and the default design's fonts load in the gallery
  demos two folders deep, with no request failing (tools/check_browser.py,
  requests).
- A3. GitHub Pages redirects /<repository> to /<repository>/. **Believed**,
  not verified; the setup steps' last test opens the address without the
  slash.

## Considered Options

- Every URL relative to the page
- Root-relative URLs, with the base path from configure-pages
- A `<base href>` element written by the build

## Decision Outcome

Chosen option: "Every URL relative to the page".

We will write every URL a page loads or links to within the site relative
to that page: static/site.js from a site's root page, ../../static/site.js
from a gallery demo.
We will resolve the knot's worker against site.js's own URL.
We will have tools/check_built.py refuse any root-relative or absolute URL
for a file the page loads, and any relative URL that names a file the
build did not write, letter for letter.
We will configure no site URL and no base path.

### Consequences

- Positive: one build works at any address, a local server included, and a
  custom domain needs no rebuild.
- Negative: a page at a new depth needs its own prefix; the build passes
  `root` to every template.
- Neutral: the site URL the brief listed among the settings is not needed.

### Confirmation

**A root-relative path fails.** check_built.py on a planted
`/static/site.js`.

**A link to a missing or wrongly cased file fails.** check_built.py on
`Static/site.js`.

**Live only:** the site loads with no failed request at
https://<user>.github.io/portfolio-gallery/ and, after a rename, at
https://<user>.github.io/ (docs/setup-on-github.md, the last steps).

## Pros and Cons of the Options

### Relative to the page

- Good: nothing to configure; works anywhere.
- Bad: every template must use the prefix it is given.

### Root-relative with a base path

- Good: one form of URL in every template.
- Bad: local and deployed builds differ, and moving the site means
  rebuilding it.

### A base element

- Good: one line.
- Bad: changes how every in-page anchor resolves, and the page's policy
  sets base-uri 'none' (ADR-0006).

## More Information

- Departs from the operator's site's ADR-0002 rule, root-relative links,
  for the reason above; that rule binds his site, not this repository.

## Changes

| Date | Change | Why |
|---|---|---|
| 2026-10-15 | **Accepted** by the owner, unchanged. | His answer 7 to the seat's report of 2026-10-13, checked with the portfolio architecture chat. |
