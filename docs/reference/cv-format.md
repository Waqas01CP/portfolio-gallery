---
type: reference
description: The Markdown shape the content trace reads a CV in, with what it checks in each direction. Read before writing content/cv.md or turning the trace off.
status: current
---

# The CV format

The content trace (`tools/check_content.py`) checks that every claim on
your site comes from your CV, and that everything in your CV reached the
site. It reads the CV as ordinary Markdown in the shape below, so the file
also reads well on GitHub. `content/cv.md` is the sample.

```
# Your Name

Headline part | Headline part | Headline part
City, Country
Open to junior roles
[you@example.com](mailto:you@example.com) | [example.com](https://example.com/)

## Summary

One paragraph.

## Intro

One paragraph, if your site has an Intro paragraph.

## Projects

### Project Name: what it is | Jan 2026 to Present

*Stack, Stack. Status sentence. Summary sentence.* ([Code](https://example.com/code))

- A bullet.
- Another bullet.

## Experience

### Role, Organisation | Jul 2025 to Present

Location

- A bullet.

## Education

### Degree, University | Sep 2021 to Jun 2025

Grade: 3.6 / 4.0 CGPA
Relevant coursework: One, Two, Three

## Certifications

- [Certificate title](https://example.com/credential), Issuer (Mar 2025)

## Skills

- Label: One, Two, Three
```

- `#` is your name; the lines under it, before the first `##`, are the
  header.
- `##` starts a section; `###` an entry, `Title | Dates`.
- A project's italic line holds its stack, status and summary sentences,
  and ends with its links in brackets.
- A line `Label: value` is checked by its value; `Relevant coursework:` is
  split at its commas.
- `<!-- comments -->` are ignored.

An item's `source` in items.json names its entry as
`"<section> / <entry title>"`, such as `"Projects / Project Name: what it
is"`; in a section of plain lines, such as Certifications, the title is
the line's link text.

## What is checked

**Page to CV.** Every block of text on the built page, its title, meta
description, alt text and labels included, is a cut of one CV line, or
pieces cut from one CV entry, or interface text: the engine's own labels,
and the words content/site.json and items.json give the controls (contact
labels and lines, proof link labels), each listed in the report.

**CV to page.** Your name, every header line, every entry's title and
dates, every bullet, the summary and intro, every italic-line sentence,
every project link as a link, every course, every certificate with its
link and date, and every skills line appear on the page whole, in the
CV's word order.

**Sources.** Every item's `source` names an entry the CV has.

Run it after any change to content:

```
python build.py
python tools/check_content.py
```

A failure names the CV's file and line: for text on the page the CV
lacks, the nearest CV line, when one is close; for CV text the page
lacks, the line it is on. It ends with what to do. The usual cause is a
fact changed in site.json or items.json and not in the CV.

## Turning it off

Set `"content_trace": false` in `content/config.json` if you would rather
not keep a CV in the repository. The checks then print that the trace is
off; nothing is checked silently.
