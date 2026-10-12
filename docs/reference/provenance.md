---
type: reference
description: Where the engine came from, what was copied, what was changed and what was left out, with the source commit. Read before comparing this repository with its source or porting a fix between them.
status: current
---

# Provenance

The engine was copied on 2026-10-12 UTC from the repository of the
owner's own portfolio site, `Waqas01CP/waqas01cp.github.io`, at commit
`5f3b84d1ff8a8aaabbc9261bc9c4042b07f5a96f`, by copying files: that
repository was never cloned or forked into this one, and its history is
not here. This repository's history starts with its own first commit.

Its ADR-0012 permits the copy: "the generator, the templates, the
stylesheet, the scripts and the generic checks", and none of the owner's
content or the checks' private forms.

## Copied, then changed

| Here | From | What changed |
|---|---|---|
| `build.py` | `build.py` | Generalised: settings in content/config.json; page-relative URLs (ADR-0007); `no_proof` takes a reason for any item instead of naming three of the owner's items; the timeline's start computed or set; sections left out when empty; contact routes as a list; a degree's grade as text; designs and the gallery; a generated layout stylesheet in place of inline styles; output to _site/, never committed. |
| `src/templates/*.html.j2` | the same | The owner's words and examples removed from comments; the CSP meta tag; style attributes moved to static/layout.css; LinkedIn and GitHub marks removed; contact cards by position; the gallery page and the demo and credit lines added. |
| `src/static/site.js` | the same | The worker found beside the script; the effects read from the design's switches; the strip's control shown with setShown. |
| `src/static/knot.js` | the same | Its header comment only. |
| `src/static/base.css` | `src/static/site.css`, part | The rules accessibility depends on, moved out of the stylesheet so every design keeps them. |
| `designs/default/design.css` | `src/static/site.css`, the rest | Fonts loaded from the design's folder; the contact cards by position; one comment that quoted the owner's content rewritten. |
| `designs/default/fonts/` | `src/static/fonts/` | Unchanged: Manrope, JetBrains Mono and Instrument Serif subsets with their OFL texts. None reserves a font name, by the OFL texts and by each WOFF2 file's own name table, read 2026-10-12. |
| `tools/check_content.py` | `tools/check_content.py` | Reads a CV in the generic Markdown shape of docs/reference/cv-format.md instead of the owner's master CV; checks items' sources. |
| `tools/gates.py`, `tools/generate_map.py`, `.githooks/` | the same | Gate A's private patterns and digest removed; private patterns moved to .git/info/never-commit; gate B builds the staged tree, since nothing built is committed; the map reads comment frontmatter too. |

## Written here

The design format and its check, the plain design, the gallery, the
screenshots, the browser checks and their protocol client, the scope
check, the CI entry point, the workflows, the sample content and every
document.

## Left out

The owner's content, CV, records, logs, briefs, research, design system
draft and CHAT_STATE.md; gate A's private patterns and its digest; the
LinkedIn and GitHub marks (their owners' terms were not read for this
repository, and the owner's site's own record supports only GitHub's).

## Measurements quoted from the source

base.css, site.js and knot.js quote measurements made on the owner's site:
layout skipping's effect on Total Blocking Time (his ADR-0009, Changes,
2026-10-06), the knot's first draw on the main thread, and the screen
reader joins that m.sp() fixes (his logs of 2026-10-07). They are that
site's numbers, cited as the reason for each rule, not measurements of
this repository's sample site; this repository's own are in
CAPABILITIES.md.
