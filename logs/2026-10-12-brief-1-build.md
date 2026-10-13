---
type: log
description: "Brief 1 and its Addendum 1: the repository built from nothing to standing on its own, locally. The engine copied from the owner's site and generalised, two designs, the gallery, the checks and their defeat cases, the gates, the workflows and every document. Nothing published."
status: current
---

# 2026-10-12: Brief 1, portfolio-gallery built to stand on its own

Model: Claude Opus 5.5 (claude-opus-5-5), in Claude Code. HEAD at start:
none, the folder held only `.gitignore` and `briefs/`. HEAD at end: the
commit that adds this log. Mode: mutating. Brief: Brief 1,
`briefs/implementation-seat.md`, with its Addendum 1 of 2026-10-12. Previous
log: none. The session ran from 2026-10-12 17:25Z to 23:32Z, paused, and
resumed 2026-10-13 07:42Z UTC; the file keeps the date it started. The
machine's local date (UTC+5) ran five hours ahead throughout.

## What was asked

The brief is never committed, so its substance is here.

**The verdict.** Build `portfolio-gallery` in this folder: a portfolio-site
generator anyone can fork and publish with GitHub Pages without installing
anything, whose own Pages site is a gallery of designs, each contributed by
pull request, checked by GitHub Actions and reviewed by the owner before he
merges it. Copy the engine from his site's repository, keep none of his
content, build until it stands on its own. **Publish nothing**: no GitHub
repository, no remote, no push; he creates the repository himself from
click-by-click steps this seat writes.

**The owner's words and decisions, as the brief recorded them.** On why
(2026-10-10): "what i want now is credibility like if there is a choice
between getting stars, forks and people starting to interact and do PRs and
other practices then i would prefer this over even if later they sell the
repo"; "i do not want a license that scares away people". On the gallery:
"the gallery showcases different and people can use them or push their own"
(not to be called a store). He adopted as rules for the gallery a strategy
ending: "What will actually impress an interviewer is how the repo is run:
clear docs, working checks, accessibility verified, issues answered and
pull requests reviewed well ... a build that runs on GitHub itself." His six
decisions of 2026-10-11 UTC: (1) MIT, credit asked in the README, a
removable "Built with portfolio-gallery" footer link on by default, "MIT it
is, as long as it yields the best of results and portfolio chat does not
say anything against this"; (2) designs as folders by fork and pull
request, "approved"; (3) the build on GitHub Actions, local builds kept,
"approved but have to make sure that rules are being followed and no
malware or things like that"; (4) the scope floor, with his question
"will this be visually available meaning if someone is browsing and seeing
designs then can they see all the designs with just a click?", answered yes
and so a requirement; (5) a fresh session builds, then a review; (6)
published only once it stands on its own. Name `portfolio-gallery` under
`Waqas01CP`.

**The scope floor**, approved 2026-10-11: no personal content of his
beyond a credit line; no cookies, tracking, analytics or requests to
another origin; every word in the initial HTML; no paid service; no
dependency without a record; a contributed design templates and CSS only,
no JavaScript. Sample content fictional and obviously so.

**What his site's ADR-0012 binds.** The copy may carry the generator,
templates, stylesheet, scripts and generic checks, none of his content or
the checks' private forms (gate A's digest of his vault's folder name).
Before publication the copy is searched for his name, email, master CV
text and that digest; his name only in LICENSE's copyright line and the
README's credit (settled by that record's Changes row of 2026-10-12,
Addendum 1).

**What to carry and what to leave.** Carry the generator and content model,
the content trace made generic (a user's own CV), the accessibility work
(setShown, m.sp(), `.vh` with `white-space: pre`, reduced motion), every
word in the initial HTML, `content-visibility` with its condition, the
generic gates, the performance goals, the standing checks with their
defeat cases. Never carry his content, CHAT_STATE.md, briefs, logs, his
records as text, gate A's private patterns, or the LinkedIn and GitHub marks
unless their terms are read first. Generalise `CV_FILE`, `CV_URL`,
`SITE_HOST`, `NO_PROOF_IDS`, comments naming his items, root-relative paths
(a fork is served under /portfolio-gallery/), the macros comment quoting his
name; keep the fonts' OFL texts with the fonts.

**The gallery.** One page, every design a card with a screenshot, name,
author linked, one line and a live demo one click away; screenshots taken
by the deploy workflow with headless Chrome; the page meets the same floor;
at least two designs at launch, `default` (his site's look) and one clearly
different.

**The security model**, CSS only recommended (ask him), six layers: a scope
check on `pull_request_target` that reads only the changed-file list;
content checks on `pull_request`; a CSP meta tag; repository settings
(approval level, ruleset, CODEOWNERS, no workflow-created pull requests,
private vulnerability reporting); actions pinned to full SHAs with least
permissions; his review last. State its limits plainly.

**What to do**: state back first, with the questions only he can answer;
the skeleton per his New Project Setup; the engine; the design format and
two designs; the build and the gallery with screenshots; the checks as
scripts run the same locally and in CI; the workflows; the documents
(README, CONTRIBUTING, Code of Conduct 2.1 with its licence verified,
SECURITY, templates, CODEOWNERS, two how-tos, `docs/setup-on-github.md`);
the standing checks with defeat cases first, headless only; the
pre-publish search; report in `briefs/architecture.md` and hand off in
`briefs/implementing.md`.

**Stop if** anything would publish, a decision or floor line would have to
change, the engine cannot work without his content, a GitHub behaviour the
design depends on proves false, or a dependency beyond Jinja2 and
MarkupSafe is needed.

**Addendum 1** (the architecture chat of his site, 2026-10-12): the name
conflict is settled as above, and that chat agrees with MIT; the report and
setup steps go to "the portfolio architecture chat", which verifies against
both repositories; and one more question for him: `default` is his own
site's look, so anyone could publish a site that looks like his; keep it,
or give `default` its own look with his kept out or offered under another
name.

## Errors this seat made

1. **Backslashes through a Git Bash heredoc.** Python edit scripts passed
   through a quoted heredoc lost a backslash: `\\0` arrived as `\0` and
   wrote ten NUL bytes into tools/prove_checks.py. Cost: one failed run.
   Caught by Python refusing the file. Fixed by a script written with the
   file tool; every file scanned since: no NUL outside `.pyc`. The brief
   named this trap; it was met anyway, in the edit scripts.
2. **The owner's name in fourteen places.** His full name as
   `decision-makers` in all twelve records, as his Decision Record
   Standard's template has it, and in a line of the records' index; and
   his first name opening the setup document. Cost: none committed; caught by
   this seat's own search before the first commit. Replaced by his handle.
   The standard and his ADR-0012 disagree here: reported.
3. **The joins model broke lines only where a node began.** Five false
   joins in a quick run. Caught on reading them; fixed to break at a
   node's start and end, then validated (below).
4. **A gallery without previews failed check_built.py**, which would have
   refused every commit at gate B. Caught by the defeat harness's control.
   Fixed: previews are required only with `--previews`.
5. **The assemble step expected the wrong artifact layout**
   (`designs/<name>/preview.webp`; upload-artifact stores the path from the
   first wildcard, `<name>/preview.webp`). Caught by reading its README at
   the pinned SHA before any run. Fixed.
6. **Two defeat cases did not test what they named.** The tree check's
   first case (setShown without aria-hidden) did not expose anything on
   this page, and the anchors case ran in quick mode, which skips the cell
   where it fails. Cost: two unproven cases until replaced. Both now fail
   as built (below).
7. **Test 2 of the setup steps would have failed.** Its minimal design
   failed the checks twice: first, both menus shown and list markers drawn
   (found by reasoning, before running); then the `<summary>` disclosure
   triangle (found by running it). Cost: one 13-minute run. Fixed in the
   setup document and the design contract, then run clean (below).
8. **The browser check crashed printing a failure** holding "▸" when its
   output went to a file on Windows (cp1252). Cost: one 13-minute run's
   failures unreadable. Fixed: every tool that prints page text escapes it.
9. **A time written before it was measured.** commands.md said a browser
   run takes "about 10 to 15 minutes"; corrected to the measured 487 s.
10. **The axe check could not run on the gallery page**: it laid out
    sections through base.css, which the gallery page does not load. The
    final runs' axe step stopped with a script error and reported nothing.
    Cost: one rerun. Fixed; then 36 cells ran.
11. **A misread wait.** A timestamp printed by this seat's own command was
    read as the end of a background test. Cost: none; caught on reading
    the test's own output file, which held only its start.
12. **A threshold tuned before the cause was tested.** The anchors check's
    32 px allowance was set from the misses seen first; a later run missed
    by 40 px. The cause was then tested (below) and fixed in the design
    rather than by widening the allowance again.

## What was done

Each commit passed gates A, B and C from the second on; the first was made
before the hooks were switched on, because gate B builds the engine, and
gates A and C were run on it by hand and passed. [VERIFIED]

1. **Skeleton** (c411847): CLAUDE.md, twelve records, STATE.md, the logs
   index, two deferred entries, the briefs README, LICENSE, the map
   generator, the gates and hooks.
2. **Engine** (7af9697): copied by file from his site at
   5f3b84d1ff8a8aaabbc9261bc9c4042b07f5a96f, generalised as
   docs/reference/provenance.md lists. Sample content for Alex Example,
   two designs, the gallery page, the file checks and ci.py.
3. **Browser checks** (64f9c64): tools/cdp.py, check_browser.py,
   screenshots.py, prove_checks.py, standing-checks.md.
4. **Workflows** (b798834): scope, checks, deploy; scope_check.py;
   CODEOWNERS; the pull request template and issue forms.
5. **Checks hardened by the first full runs** (0169b54): the anchors
   reload, hidden spaces between links, reports that survive any
   character.
6. **Documents** (bd63dba): README, CONTRIBUTING, CODE_OF_CONDUCT,
   SECURITY, the how-tos, the setup steps.
7. **Fixes from the final runs** (the next commit): the default design's
   fonts optional; the axe check on the gallery page; the design
   contract's advice on web fonts.
8. **This log**, the index row, STATE.md, completed.md and CAPABILITIES.md
   (the last commit).

**Evidence, each run this session:**

- Fonts: the three WOFF2 files' name tables, read with Node's built-in
  Brotli, carry copyright lines and the OFL URL and no Reserved Font Name.
  [VERIFIED]
- requirements.txt: every file hash for Jinja2 3.1.6 (2) and MarkupSafe
  3.0.3 (89), from PyPI's JSON API; a fresh venv installs it; `pip list
  --not-required` shows Jinja2 and pip. [VERIFIED]
- Fresh clone at b798834, the documented commands: site in default (14
  files), site in plain (8), gallery (18), each built twice, exit 0, `diff
  -r` identical. [VERIFIED]
- `tools/ci.py checks` in that clone: designs 0 problems; two builds
  identical; built files 0 problems; content trace 196 blocks traced, 0
  not, every CV line found, 8 of 8 sources; browser checks: tree 48 runs,
  keyboard 8, joins 4, anchors 136, words 4, motion 3; 494 s in all, 487 s
  of it the browser checks. It failed on one anchor (below). [VERIFIED]
- Anchors: three more runs found one small miss per run, a different
  target each time, 16 to 21 px, all in the default design, by address;
  the plain design none. The check now reloads a miss of at most 32 px once
  and notes it; a larger miss fails at once. As built: pass with one note.
  Without base.css's `:target` rule: 4 failures (misses of 360 to 1,163 px)
  and notes. [VERIFIED] Cause: web fonts arriving after the jump, a
  hypothesis, not tested.
- Joins model: on his site at 6812c4f (exported read-only with `git
  archive` into scratch), 58 joins at 360 px and 43 at 1366 px, where his
  record says 58 and 45 with the widths the other way round; 0 and 0 at
  c97b99e, the fix. [VERIFIED]
- Tree at load: on his site at 0403c68, 5 "In depth" headings and 5 Close
  buttons in the full tree at 360 px, against 0 without the rule. On this
  engine, a panel hidden by script without aria-hidden was **not** exposed
  (projects at 1,610 px; his at 2,317 px); markup hidden without
  aria-hidden in a skipped section was (199 text entries against 198), and
  the check fails on it. [VERIFIED] Why the script case differs is not
  known.
- Defeat cases, tools/prove_checks.py: every control passes; each file
  case and each browser case fails as built, naming what failed (the counts
  are in the last run below). [VERIFIED]
- Gates, in a scratch clone with the private patterns copied in: 15 defeat
  cases refused (CHAT_STATE.md, a brief, a drive-letter path, a climb, a
  path from never-commit.txt, his name outside its places, his email in a
  file and in the commit identity, a design with @import, a cut that is not
  a cut, a stale map, an unreadable header, the map generator missing, the
  venv missing, a push without STATE.md) and 3 controls passed (his name in
  LICENSE, prose naming a folder, a series with STATE.md last). [VERIFIED]
- Scope check's pull-request path, with the API and event faked: owner
  passes; owner with `[scope: as contributor]` on an engine file fails;
  first-timer on build.py fails; contributor's design passes; a file count
  that disagrees with the event fails. The real API's fields (`filename`,
  `status`, `previous_filename`, `changed_files`) read from three public
  pull requests of actions/checkout. [VERIFIED]
- Workflows: parsed with PyYAML 6.0.2 in a scratch venv (not a
  dependency); all 12 `uses:` pinned to 40-character SHAs with a version
  comment; permissions as ADR-0006 says; upload-pages-artifact's own inner
  action pinned by SHA too. [VERIFIED] They have not run on GitHub.
- The minimal test design of Test 2, run through every check alongside the
  two designs: see the last run below.
- Pre-publish search (scratch script, patterns from .git/info/never-commit,
  printing no email): every blob in the history, every commit header and
  the built site and gallery; see the last run below. Its own defeat: an
  email planted in a scratch clone's commit and deleted in the next is
  found. [VERIFIED]

**GitHub facts read this session**, from docs.github.com's article API,
2026-10-12: `pull_request_target` runs from the default branch and a
checkout without `ref` takes the default branch; fork `pull_request` runs
get a read-only token and no secrets; "Workflows don't run in forked
repositories by default"; `pull_request_target` runs regardless of the
approval setting; "By default, all first-time contributors require
approval"; the three approval levels and GitHub's warning on the first
two; new personal repositories default to a read-only token and no
workflow-created pull requests; "Require actions to be pinned to a
full-length commit SHA"; rulesets' rules; CODEOWNERS locations and empty
owners; private vulnerability reporting's place; a template copy "starts
with a single commit" and its commits appear in the contribution graph;
content reports to maintainers exist only for organisation-owned
repositories. The Contributor Covenant 2.1 text is under CC BY 4.0 (its
repository's README and LICENSE.md at tag 2.1). Ubuntu 24.04 runner image
20261004.327.1: Chrome 154.0.8037.97, Python 3.12.3.

## Final runs, 2026-10-12 22:56Z to 2026-10-13 UTC

On a fresh clone of bd63dba, one job at a time. The session paused from
23:32Z to 07:42Z at the owner's interruption, and resumed on his word.
[VERIFIED, each]

1. `tools/ci.py checks`: exit 0 in 503 s; browser checks 496 s, 0
   failures, no anchor notes.
2. `tools/prove_checks.py --browser`: 46 defeat cases (38 file, 8 browser)
   each failing as built and naming what failed; 7 controls passing; 645 s.
3. Every browser check with the setup's Test 2 design added beside the two
   designs: the test design passed every check; the run failed once on the
   default design's anchors (#contact, 40 px at 360 px, scripts off) with
   four smaller misses noted.
4. axe-core 4.14.0 (scratch install): 36 cells, both designs and the
   gallery page, 0 violations, after error 10 was fixed. Defeat: faint
   text and an image without alt planted in the plain design; image-alt in
   every cell, color-contrast in the light ones.
5. Lighthouse 13.5.0, default mobile, median of five, served uncompressed
   from 127.0.0.1: default LCP 2,179 ms, CLS 0, TBT 195 ms (runs 195, 248,
   280, 22, 64); plain LCP 1,389 ms, CLS 0.048, TBT 0 ms.

**The anchor misses, tested.** The default design as built missed 1 load
in 136; with `font-display: optional`, 0 in 136; with no web fonts, 0 in
136. Over the session the default design as built missed about 10 times
in some 900 loads, 16 to 40 px, mostly with scripts off; plain, on system
fonts, never. Moderate evidence that the cause is the web fonts arriving
after the jump. The default design now uses `font-display: optional`.
Rerun with it, 2026-10-13 08:01Z: every browser check on both designs, 0
failures and no anchor misses in 136, 483 s; the default preview
byte-identical to the one taken with swap, so the fonts were used;
Lighthouse on the default site, LCP 2,108 ms, CLS 0, TBT 40 ms (runs 174,
37, 40, 46, 25). Swap is the owner's site's choice and may be his here;
it is listed for him to decide. [VERIFIED]

## External contract changes

**GitHub now blocks `pull_request_target` in public repositories by a
default policy.** "Securely using pull_request_target", read 2026-10-12:
"For public repositories that do not already have an applicable Actions
event policy, GitHub adds a default policy that blocks workflows triggered
by `pull_request_target`." It "Currently runs in **evaluate** mode", and
"On November 2, 2026, GitHub will enforce the default policy". Remedy, same
page: "create or update an applicable Actions event policy that explicitly
allows pull_request_target." The brief, written before, did not know it.
The setup steps add the policy (step 5).

## Rejected alternatives

- A Node driver or puppeteer-core for the browser: an npm dependency in CI;
  Python's standard library over the DevTools protocol instead (ADR-0010).
- Root-relative URLs with the base path from configure-pages: local and
  deployed builds would differ (ADR-0007).
- `style-src-attr 'unsafe-inline'` for the layout's inline styles: support
  for that directive in every browser was not established; the positions
  moved to a generated stylesheet instead.
- A hard-coded repository name to choose gallery or site: a repository
  variable, unset in every copy, instead.
- Committing the built output, as his site does: the build runs on Actions
  (his decision 3); gate B builds the staged tree instead.
- Frontmatter tables at the top of the visitor-facing files: the same keys
  in an HTML comment.
- The `pull_request` trigger for the scope check: a pull request could
  rewrite it.
- Retrying every anchor miss: would hide the misplacement the check exists
  for; only a miss of a line or so is retried.

## Checked and found already correct

The brief's claims on `pull_request_target`, fork tokens, workflow-created
pull requests, the runner's Chrome and Python, configure-pages' outputs,
and its unverified one that forks start with workflows off, which GitHub's
own page states. His site's three fonts reserve no name. GitHub's MIT text
matches the LICENSE written.

## Not done

- Nothing published: no remote, no push, no repository (ADR-0005).
- The workflows have not run; the first push and the setup's tests prove
  them.
- axe and Lighthouse are not in CI; their records are proposed. Their local
  results are below or in the report.
- The master CV part of the pre-publish search: his site's implementing
  seat runs it, through the architecture chat.
- The registry of Confirmation clauses the Working Method describes (6.3)
  is not built; the defeat harness covers the checks' clauses.
- A real screen reader by ear, and any browser but Chrome.
- The architecture chat's lane of CAPABILITIES.md, and CHAT_STATE.md,
  which waits for that chat.

## Findings and recommendations

Findings:

1. The `pull_request_target` default policy (above).
2. The owner's Decision Record Standard puts his name in every record's
   `decision-makers`; his ADR-0012 allows it in two places here. Records
   here use his handle.
3. GitHub's documentation now says the default approval level covers all
   first-time contributors; the brief said only accounts new to GitHub.
4. Anchors in the default design miss by a line on about 1 load in 136.
5. On this engine a panel hidden by script without aria-hidden was not
   exposed at load, unlike his site at 0403c68; markup was.
6. Manrope's OFL text says "Copyright 2018 ... googlefonts/manrope"; the
   font file's own name table says "Copyright 2019 ... sharanda/manrope".
   Both name the Manrope Project Authors.

Recommendations (each the owner's or the chat's to decide):

1. CSS only for v1 (ADR-0006).
2. "Require approval for all external contributors".
3. "Use this template" for users, forks for contributors.
4. For the anchor finding: re-align to the target once the fonts are in,
   in site.js, if the reader has not scrolled; or `font-display: optional`
   in the default design, which changes how it looks on a slow connection.

## Noticed and not investigated

- Whether GitHub runs workflows for a template copy's first commit.
- Whether a template copy shows a link back on GitHub.
- GitHub Pages' redirect from /portfolio-gallery to /portfolio-gallery/.
