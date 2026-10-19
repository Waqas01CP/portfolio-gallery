---
type: reference
description: "The content schema: what config.json, site.json and items.json hold, which rules the build enforces, how shortened text is checked against its source, and its limits. Read before writing or editing content."
status: current
---

# Content

Four files in `content/` hold every word and setting of a site. Markup is
generated from them by `build.py`, so a date or a fact is written once,
here, and nowhere else (ADR-0004). The sample content describes Alex
Example, an invented person; replace it with your own.

| File | Holds |
|---|---|
| `config.json` | The settings: the design, the CV files, the content trace, the credit line |
| `site.json` | The text that belongs to the page rather than to one item: name, headline, summary, highlights, skills, contact |
| `items.json` | Every dated item: projects, work, the degree, certificates |
| `cv.md` | Your CV in Markdown, the source the content trace checks the page against (docs/reference/cv-format.md) |

With the content trace on, the default, **every fact in `site.json` and
`items.json` must also be in `cv.md`**: change a fact in one and change it
in the other, or the build fails, naming the CV line to look at
(docs/reference/cv-format.md).

JSON, not YAML, because Python's standard library reads JSON and a YAML
parser would be a second dependency (ADR-0001 line 5). Anything committed
here is public, your CV included.

## config.json

| Setting | Meaning | Sample |
|---|---|---|
| `design` | The folder in `designs/` your site uses | `"default"` |
| `cv_pdf` | A PDF to offer as "Download CV", a path in the repository, or `""` for none | `"content/Alex_Example_CV.pdf"` |
| `cv_source` | Your CV in Markdown, for the content trace | `"content/cv.md"` |
| `content_trace` | Check every word on the page against `cv_source`: `true` or `false` | `true` |
| `credit` | Show the credit line in the footer, "Built with portfolio-gallery", with the design and its author, each linked: `true` or `false` | `true` |
| `timeline_start` | The month the timeline starts at, `YYYY-MM`, or `""` for January of the earliest year an item outside the degree starts | `""` |

A path must name the file exactly, letter for letter: GitHub Pages
matches names by case, and Windows and macOS do not, so a link that works
on your computer can fail on the site. The build checks names against the
folder's own listing.

## site.json

| Field | Notes |
|---|---|
| `name` | Required. The first word is set on the first line of the Intro, the rest on the second. |
| `headline` | Required. A list, shown joined by `|`. |
| `location` | Required. |
| `summary` | Required. The Intro's first paragraph. |
| `availability` | Optional. A short line, such as "Open to junior roles". |
| `intro` | Optional. The Intro's second paragraph. |
| `highlights` | Optional. Figures on the opening screen. Each names an `item`, a source in `from`, a `figure`, its `text`, and optionally `before`. **The words, in order, must be a cut of the source**: `site/summary` or `<item>/bullets/<n>`, counted from 1. |
| `feature` | Optional. The figure at the head of Projects: `item`, `from`, `label`, `figure`, `text`, `note`, and optional `pairs` of `{figure, text}`, **each a cut of its source**. |
| `skills` | A list of `{label, items}`. No levels of any kind. |
| `contact` | Required, at least one. Each `{label, url, text}`, with optional `line` (what the route is for) and `cta` (the Intro button's words). `url` is `mailto:` or an absolute `https:` address. The first route is the accented button. |

## items.json

Every item carries `id` (a lowercase slug, unique, and not one the page
uses itself: `main`, `top`, a section's id, or starting `depth-`,
`toggle-`, `tl-`, `tlx-` or `h-`), `lane`, `title`, `start` (`YYYY-MM`),
`end` (`YYYY-MM` or `present`), and `source`, the CV entry it comes from,
as `"<section> / <entry>"` (the content trace checks the entry exists).

And exactly one proof route: `proof`, a list of `{label, url}` links a
reader can check, or `no_proof`, the reason there is none, shown nowhere
but required, so leaving a claim unproven is a decision, not an oversight.

| Lane | Section | Required | Optional |
|---|---|---|---|
| `builds` | Projects | `tier` (1, 2, 3), `stack` (list), `layer1`, `bullets` (list) | `status`, `layer2`, `detail`, `date_style` |
| `work` | Work | `org`, `location`, `bullets` | `org_short`, `detail`, `date_style` |
| `band` | Education, and the band on the timeline | `org` | `org_short`, `grade`, `coursework` (list), `date_style` |
| `certifications` | Certifications | `proof` | `org`, `date_style` |

- `layer1`: the one-line fact on a project card, **a cut of one of its
  bullets**.
- `layer2`: the summary under the title.
- `bullets`: the full detail, shown in the project's "In depth" panel, or
  in full for work. HTML fragments limited to `<strong>` and `<a href>`;
  the build refuses any other tag, attribute or comment. A project with
  one bullet has no panel, so **its `layer2` then its `layer1` must carry
  the whole bullet, word for word**.
- `detail`: the text on the item's timeline card, **a cut of its status
  and `layer2`, its `layer1`, or one bullet**.
- `org_short`: a shorter name for the timeline, **a cut of `org`**.
- `tier`: order and prominence only. Tier 1 takes a full row. Down the
  file, tier must not decrease; the build refuses, naming both items,
  rather than sorting.
- `date_style`: `compact` (default: "Nov to Dec 2025"), `full` ("Jan 2024
  to Feb 2024") or `long` ("June 2026 to July 2026"). Pick the one your CV
  uses, or the content trace will report the dates missing.

## What "a cut" means

Shortened text is stored as written, and the build refuses any that is not
a cut of its source: the same words in the same order, some left out.
Change a number in a bullet and every cut of it that carries the number
fails the build until it is changed too. Changing a fact by leaving words
out is not something a program can detect; that stays a reader's check.

## What the build refuses

Everything above, plus: a field a lane does not define, a missing
required field, a wrong type, an empty value, an unknown lane or date
style, a malformed date, an end before its start, a start after the
as-of month, an item outside the degree that starts before the timeline or
ends after the as-of month, a duplicate id, more than one degree, a link
that is not `https:`, `http:` or `mailto:`, and a highlight or feature that
names a missing item or source. It checks everything before writing
anything, reports every failing item by id, and exits 1.

## Limits

- **One degree on the timeline.** The band lane draws one degree; a second
  fails the build. Recorded 2026-10-12.
- **English labels.** Section names and control labels are the engine's,
  in English, and the page is marked `lang="en"`.
- **Eight sections, in a fixed order.** A section with nothing to show is
  left out, menu entry and all.
