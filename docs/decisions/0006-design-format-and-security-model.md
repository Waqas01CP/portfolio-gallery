---
status: accepted
topic: security
description: "What a design may contain (CSS only, on the engine's fixed HTML, with fonts and images), and the six layers that keep a contribution from running anything or reaching visitors, with what they cannot promise. Read before changing the design format, a check, a workflow or a repository setting."
date: 2026-10-12
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0006: The design format and the security model

## Context and Problem Statement

A design is code from a stranger that, once merged, every user of it
publishes under their own name, and that the gallery serves at
waqas01cp.github.io/portfolio-gallery/, the same origin as the operator's
portfolio. Three things are at stake. What a design can do in a visitor's
browser: run script, load from elsewhere, track. What a pull request can do
on GitHub's runners: on main, the deploy job may publish the site. And
whether the page stays accessible and keeps every word whatever the design.

The operator approved, on 2026-10-11, "templates and CSS only, no
JavaScript" (ADR-0001 line 6), on the condition that "rules are being
followed and no malware or things like that." A design that brings
templates can reshape the page; one that brings only CSS cannot, and
cannot run code at build time either.

## Decision Drivers

- ADR-0001 lines 2, 3 and 6; ADR-0003.
- The operator's condition of 2026-10-11, above.
- A Jinja2 template is code that runs during the build; outside Jinja2's
  sandbox it can reach Python's internals.

## Assumptions

- A1. `pull_request_target` runs the workflow from the base repository's
  default branch, and `actions/checkout` without a ref checks out that
  branch. **Sourced**: GitHub Docs, "Securely using pull_request_target"
  and "Events that trigger workflows", read 2026-10-12: "the workflow, and
  any subsequent actions/checkout call that does not specify a ref, is
  taken from the base repository's default branch".
- A2. GitHub blocks `pull_request_target` in public repositories by a
  default policy, in "evaluate" mode now and enforced from 2026-11-02, and
  a repository may allow it with an Actions policy of its own. **Sourced**:
  the same page and "About Actions policies", read 2026-10-12: "If the
  workflow must continue to use pull_request_target, create or update an
  applicable Actions event policy that explicitly allows
  pull_request_target." Whether a repository created after the policy's
  release is blocked from its first day is **not stated** there; the setup
  steps create the allowing policy either way.
- A3. `pull_request_target` workflows run regardless of the approval
  setting for outside contributors. **Sourced**: GitHub Docs, "Managing
  GitHub Actions settings for a repository", read 2026-10-12.
- A4. `pull_request` workflows from a fork get a read-only token and no
  secrets. **Sourced**: "Events that trigger workflows", read 2026-10-12.
- A5. A meta Content-Security-Policy cannot set frame-ancestors, report-uri
  or sandbox. **Sourced** from the CSP specification as the brief states
  it; **not re-read** this session.
- A6. Chromium builds a section's full accessibility tree at load from the
  DOM without the section's style when the section skips its layout.
  **Measured** on the operator's site (its standing checks, 2026-10-07) and
  here: the plain design's list markers entered the tree only once laid
  out, and the tree check failed it on 2026-10-12.

## Considered Options

- CSS only, on the engine's fixed HTML (recommended)
- CSS and Jinja2 templates, the templates rendered in Jinja2's
  SandboxedEnvironment
- Anything, with review as the only gate

## Decision Outcome

Chosen option: "CSS only, on the engine's fixed HTML", decided by the
owner on 2026-10-15 UTC: "Designs are CSS only. Keep it as built."

We will accept a design as one folder holding exactly design.css,
design.json, fonts/*.woff2 with each font's licence text in fonts/*.txt,
and images in img/ as PNG, WebP or JPEG; no SVG, HTML, JavaScript or
template, no other folder, no link, and no preview image.
We will give every design the same HTML and the engine's base.css, which
loads after the design and keeps what a screen reader and a reader who
turned off motion depend on.
We will hold every contribution behind six layers:
1. a scope check on `pull_request_target`, run from the default branch,
   that reads only the pull request's list of changed files through the
   API with a read-only token, never checks out or runs the pull request,
   and fails any file outside one designs/<name>/ folder or of a type not
   allowed, or any change to a design the project maintains;
2. content checks on `pull_request`, with a read-only token and no secrets,
   that check every design's files, sizes, design.json and CSS (no
   @import, no url() outside the design's own fonts/ and img/, nothing that
   loads or runs), build the site and the gallery, and run the standing
   checks on every design; these run the pull request's own copy of the
   checks, which layer 1 makes safe by failing any pull request that
   changes them;
3. a Content-Security-Policy meta tag in every page, so a browser refuses
   scripts, styles, fonts and images from any other origin, and every
   inline script and style, even if a check misses one;
4. repository settings, set by the owner from docs/setup-on-github.md: an
   Actions policy that allows the events the workflows use, approval of
   workflows for all outside contributors, every action pinned to a full
   commit SHA, a ruleset on main requiring a pull request and both checks
   and blocking force-push and deletion, CODEOWNERS naming the owner for
   everything outside designs/, workflows not allowed to create or approve
   pull requests, and private vulnerability reporting on;
5. every third-party action pinned to a full commit SHA with its version
   in a comment, and each workflow's permissions set to the least it
   needs;
6. the owner's review: he merges every pull request himself.
We will take the gallery's previews ourselves, in the deploy workflow, by
headless Chrome, in a job that holds no write token, and publish only
WebP files from it (ADR-0010).
We will state in CONTRIBUTING.md what the checks cannot see: intent,
taste, plagiarism, and whether an image or a modified font is the
contributor's to give.

### Consequences

- Positive: a merged design cannot run script, load anything from
  elsewhere, or reshape the page; every design is checked for keyboard and
  screen reader use by construction.
- Positive: one setting swaps designs, because every design styles the
  same page.
- Negative: designers cannot change the HTML; a design that needs new
  markup needs an engine change first, proposed in an issue.
- Negative: layer 1 depends on GitHub allowing `pull_request_target` for
  this repository; without the owner's Actions policy it stops running on
  2026-11-02 at the latest, and with it required, design pull requests
  could not merge.
- Negative: fonts and images are parsed by the browser on the runner and in
  visitors' browsers; a malformed file aimed at a parser bug is beyond what
  these checks can see. Chrome's own font sanitiser and sandbox are the
  defence.
- Neutral: the gallery shares an origin with the operator's site; the
  policy refuses anything but this site's own files, and a design brings
  no script.

### Confirmation

**A design with a .js file fails.** tools/check_design.py and
tools/scope_check.py on a planted design.js; the session log records each
defeat.

**A design with an .svg fails.** Same, with logo.svg.

**CSS with @import fails, escaped or not.** check_design.py on `@import`
and on `@\69mport`.

**A url() to another origin fails.** check_design.py on
`url(https://example.org/x.png)`, and check_built.py on the built page.

**A file outside the design's folder fails.** scope_check.py on a list
holding tools/check_design.py.

**A file over its size limit fails.** check_design.py on a 101 KB
design.css.

**A design.json missing a field fails.** check_design.py with no
author_url.

**A built page holding a request to another origin fails.**
check_built.py and the requests check of check_browser.py on a planted
image from example.org.

**A hidden panel not aria-hidden fails.** check_built.py on markup, and the
tree check of check_browser.py on the same markup in a section that skips
its layout. A panel hidden by the script without aria-hidden was not
exposed at load on this engine in Chrome 154 (2026-10-12), though it was on
the operator's site at 0403c68; setShown keeps the two together anyway.

**A design that adds or hides words fails.** The words check of
check_browser.py, on a design with `::before { content: "..." }`.

**Live only:** a test pull request from a fork touching tools/ fails the
scope check on GitHub, and one adding a design passes both checks
(docs/setup-on-github.md, the last steps).

## Pros and Cons of the Options

### CSS only

- Good: nothing contributed runs anywhere; the checks that matter cannot be
  designed around; CSS Zen Garden proved one HTML can carry many designs
  (the operator's site, research 0005).
- Bad: narrower than the operator's approved "templates and CSS".

### CSS and sandboxed templates

- Good: designers may reshape the page.
- Bad: a template runs during the build, on the machine that publishes;
  the sandbox is the only guard, accessibility and "every word in the HTML"
  must be re-checked per design and can be designed around, and one
  setting no longer swaps designs cleanly.

### Anything, review only

- Good: maximum freedom.
- Bad: against ADR-0001 line 6, and the owner's review becomes the only
  thing between a stranger and every visitor.

## More Information

- If the operator chooses templates too: render contributed templates only
  in Jinja2's SandboxedEnvironment, which ships with Jinja2 and adds no
  dependency, and record it as a Changes row here.
- GitHub Security Lab, "Preventing pwn requests", the standard warning on
  `pull_request_target`, cited by GitHub's page above.
- His site's research 0005: academicpages closes misdirected pull requests
  with a `pull_request_target` workflow; the scope check here gives the
  author a readable reason instead.
- Revisit if GitHub removes `pull_request_target` for public repositories
  outright, or if a design needs markup the engine lacks.

## Changes

| Date | Change | Why |
|---|---|---|
| 2026-10-15 | **Accepted** by the owner. Decision Outcome read "proposed: the operator was asked on 2026-10-12 to choose between it and templates too" and now records his decision; the description loses its "Proposed" sentence. Nothing else changed. | His answer 1 to the seat's report of 2026-10-13, checked with the portfolio architecture chat. |
