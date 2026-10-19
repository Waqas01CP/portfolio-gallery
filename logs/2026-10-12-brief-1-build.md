---
type: log
description: "Brief 1 and its Addendum 1: the repository built from nothing to standing on its own, locally. The engine copied from the owner's site and generalised, two designs, the gallery, the checks and their defeat cases, the gates, the workflows and every document. Nothing published. Round 2, 2026-10-15 to 16: the owner's answers applied, axe-core in the checks workflow, gate A's allowed text and the Chrome launcher's start. Round 3, 2026-10-16: the deploy job, skipped in every site-mode run, fixed, and a check that says when workflow jobs run. Round 4, 2026-10-18: the setup guide corrected from the owner's run of every step and test. Round 5, 2026-10-18: dark mode by the design's word, and CAPABILITIES' architecture lane kept out of the repository. Round 6, 2026-10-18: a copy cleans itself up, once."
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

---

# Round 2, 2026-10-15 to 16 UTC: the owner's answers to Report 1

Model: Claude Opus 5.5 (claude-opus-5-5), in Claude Code, the same session
continued. HEAD at start: 43edeb2. HEAD at end: the commit that adds this
section. Mode: mutating. Ran from 2026-10-15 22:58Z, paused at the
owner's interruption at 23:16Z, and resumed at his word on 2026-10-16
07:31Z. A background run of the defeat harness made no progress in those
eight hours, so the machine was most likely asleep too. His local date
(UTC+5) was 2026-10-16 throughout, and his answers carry that date.

## What was asked

His answers to Report 1, checked with the portfolio architecture chat and
pasted to this seat: make the changes, commit locally, do not push, and
report in the brief's report file. In short:

1. Designs are CSS only, as built.
2. The default design keeps his site's look, credited to Waqas01CP.
3. CONTRIBUTING.md promises "a first response within 7 days", one promise
   only.
4. The README links his portfolio site beside the credit.
5. The repository stays on his personal account. The Code of Conduct's
   contact is a dedicated address of his, which his site's ADR-0012
   allows in CODE_OF_CONDUCT.md only. The pre-publish search allows his
   name in LICENSE and README.md and this address in CODE_OF_CONDUCT.md,
   and fails anywhere else; his two personal addresses stay barred
   everywhere. The placeholder goes from the Code of Conduct and from the
   setup steps.
6. The commit identity stays: Waqas01CP with GitHub's no-reply address.
7. Records 0006 to 0011 accepted; 0012 held as proposed.
8. `font-display: optional` stays in the default design.

Also settled: the ruleset's bypass list stays empty; `pull_request_target`
is not a stop condition, and step 5 with its stop condition stays; records
name "Waqas01CP, the repository's owner"; the authority order is left to
this repository's own chat. The chat ran the master CV search over the 129
objects of the history at 43edeb2: 0 hits, and its defeat case found hits.
The aim: the owner finishes the setup steps before 2026-11-02.

## Errors this seat made

1. **Backslashes through a Git Bash heredoc, again**: the trap the brief
   named, Report 1's error 1.1, and this seat's own handoff. A Python edit
   to the scratch gate harness turned an escaped tab into a real one and
   broke a string. Cost: one failed parse, nothing committed. Restored
   from a copy made first; the edit redone with the file tool.
2. **The owner's decisions dated 2026-10-16 UTC** in thirteen files; he
   gave them on 2026-10-15 UTC, and 2026-10-16 is his local date. Caught
   from the gate proof's UTC timestamps, before any commit; corrected
   everywhere, with the local date noted once in the records' index.
3. **commands.md's first axe section claimed an `&&`** its commands do not
   have. Caught on reading back, before any commit.
4. **The default design's comment on its fonts**, written in 206c858, said
   "none in 136 loads" after the count had reached 272, and that a late
   font "is used from the next page view", which CSS Fonts 4 does not
   promise. Found this round; corrected in e794feb.
5. **tools/cdp.py since 64f9c64**: a failed start left its Chrome
   running, and a port-file read refused by Windows failed the start.
   Found when one defeat case hit the refusal on 2026-10-16. Cost: that
   run's evidence, and an orphaned headless Chrome, stopped by hand.
   Fixed in 322e0ea.

## What was done

Commits, each through gates A, B and C:

- 328cdad Gate A: text allowed in a file is taken out of each line before
  the other private patterns are matched there.
- 322e0ea The Chrome launcher's two start failures.
- c7e3fd9 axe-core in the checks workflow; ADR-0011 accepted.
- e794feb The owner's other answers.
- The commit that adds this section: STATE.md, completed.md,
  CAPABILITIES.md and this log.

Where each answer landed [VERIFIED, read in the committed files]:

1. ADR-0006 accepted; ADR-0001's note and CLAUDE.md's floor line 6 say so.
2. ADR-0013. Its Confirmation checked on a built gallery: the Default
   card reads "By Waqas01CP", and the demo's footer "The Default design,
   by Waqas01CP, on sample content."
3. CONTRIBUTING.md: "A first response within 7 days." No other time is
   promised anywhere in the repository.
4. README.md's credit links https://waqas01cp.github.io/ (ADR-0002,
   Changes).
5. CODE_OF_CONDUCT.md line 45 holds the address, and the placeholder is
   gone. The setup steps' "before you start" now asks only that the
   pre-publish search has passed on the commit to be pushed. ADR-0002 and
   ADR-0005, Changes; CLAUDE.md. The address is in
   .git/info/never-commit with `@allow CODE_OF_CONDUCT.md`. Gate A
   refused it there for the surname it holds until 328cdad.
6. commands.md's Gates section gives the two `git config` lines;
   CLAUDE.md points to them.
7. Records 0006 to 0011 accepted, each with a Changes row; 0012 held, with
   a Changes row; the index's Pending list holds 0012 alone.
8. ADR-0014, sourced from CSS Fonts Module Level 4, read 2026-10-15.

His site's ADR-0012 Changes row allowing the address was read at his
site's a8f1da0: dated 2026-10-16, his local date, committed 2026-10-15
22:56Z.

**ADR-0011 built.** The checks workflow fetches axe-core 4.14.0's tarball
from the npm registry, checks it with `sha512sum --check --strict` against
the registry's integrity value written in the workflow in hex, extracts
`package/axe.min.js` alone, and runs `tools/ci.py checks --axe`. The
registry was read again on 2026-10-15: MPL-2.0, no dependencies, the same
integrity value as on 2026-10-12, served directly with no redirect. The
fetch and check ran here in the workflow's form and in the PowerShell and
Git Bash forms commands.md gives; each refused a copy with one byte added.
The extracted file is byte-identical to the one run on 2026-10-13.

**Proofs** [VERIFIED]:

- Gates, in a scratch clone with the working gates committed first,
  2026-10-15 23:05Z to 23:08Z: 22 of 22 as expected, 18 defeat cases
  refused and 4 controls passed. New: the address in another file, the
  surname beside the address in CODE_OF_CONDUCT.md, a commit under the
  address; control, the address in its own file.
- The Chrome launcher: both failures planted against 43edeb2's cdp.py
  left 11 and 10 processes running, and the refused read raised. Against
  322e0ea: none left, Chrome started after three refused reads, and 40
  starts and closes left no process and no profile folder.
- The defeat harness on a fresh clone of e794feb, with a new venv from the hash-pinned requirements, `prove_checks.py --browser --axe`, 2026-10-16 07:48:32Z to 08:04:06Z, 934 s: 47 defeat cases (38 file, 9 browser, the axe case among them) failed as built, naming what failed; 8 controls passed, axe's among them.
- `tools/ci.py checks --axe` on the same clone, 08:04:06Z to 08:14:38Z, 632 s, exit 0: both designs pass their file checks; two builds each of the site (14 files) and the gallery (18 files) byte-identical; the built files 0 problems; the content trace 196 blocks traced, 0 not, every CV line on the page, 8 of 8 sources; the browser checks 623 s, 0 failures (tree 48 runs, keyboard 8, joins 4, anchors 136, words 4, motion 3, axe 36).
- The pre-publish search at e794feb: PASS. 155 blobs across all 12
  commits, every text blob judged at each path it has in any commit (152
  pairs), 12 commit headers, and the site and gallery freshly built (32
  files). The name on LICENSE line 3 and README.md line 69, the address
  on CODE_OF_CONDUCT.md line 45, nothing else. Its defeat run, six cases
  planted in a scratch clone, each on its own branch: a personal address
  committed then deleted, the address in CONTRIBUTING.md, the surname
  beside the address in CODE_OF_CONDUCT.md, the first name alone there,
  an identical copy of CODE_OF_CONDUCT.md at another path, and the name in
  a commit message. All six found.
- The first defeat run on the working tree, 2026-10-15 23:11Z to
  2026-10-16 07:41Z across the pause, is not used as evidence: 45 cases
  failed as built and 7 of 8 controls passed, and the two unproven were
  error 5's.

## Rejected alternatives

- One commit per answer, as this seat's handoff suggested: the answers
  share files (CLAUDE.md, commands.md, the records' index). Four commits
  by piece of work instead, with an intermediate version staged through
  git's index where a file belonged to two.
- A Python script to fetch axe-core: ADR-0011 records the hash in the
  workflow, so the workflow checks it in shell, and commands.md gives the
  same steps for PowerShell and Git Bash.
- Allowing the surname in CODE_OF_CONDUCT.md: it would let the name stand
  alone there; the owner allowed the address only.
- Records for the response time and the commit identity: neither weighed
  options, and each lives where it binds.

## Checked and found already correct

- Step 9's ruleset: bypass list empty, required approvals 0, as the chat
  settled.
- SECURITY.md promises no time, so the 7 days stay the one promise.

## Not done

- Nothing published.
- The master CV search on the commits after 43edeb2.
- Lighthouse in CI (ADR-0012, held).
- The workflows, axe's step among them, have never run.
- The architecture chat's lane of CAPABILITIES.md.

## Findings and recommendations

1. The master CV search ran at 43edeb2; the setup steps now ask that it
   pass on the commit to be pushed, so it needs one more run.
2. The setup steps still open with "Do not start until the portfolio
   architecture chat has checked these steps." The seat left it for the
   chat to clear.
3. The Windows sharing violation on DevToolsActivePort is Windows'
   mandatory locking; the runner's Linux has none, so CI was not exposed.
   Inferred, not tested on the runner.

---

# Round 3, 2026-10-16 UTC: the deploy job never ran in site mode

Model: Claude Opus 5.5 (claude-opus-5-5), in Claude Code, the same session
continued. HEAD at start: 6a4de5e, which the owner had pushed: the
repository has been public since his push (first runs 2026-10-16 19:48Z),
with origin at https://github.com/Waqas01CP/portfolio-gallery.git and main
equal to origin/main. HEAD at end: the commit that adds this section.
Mode: mutating. Ran from about 20:55Z; his local date (UTC+5) was
2026-10-17.

## What was asked

The portfolio architecture chat, relayed by the owner during setup step 8:
the deploy job has no `if:`, so it takes the default `success()`, which is
false when an earlier job in its chain was skipped; shots is skipped in
site mode, so deploy is too, and every copy of the template would never
publish (actions/runner issue 491). Fix it with an explicit condition,
check checks.yml and scope.yml for the same pattern, add a static check
to the file checks that refuses a job which needs a conditional job and
has no explicit `if:`, prove it with its defeat case, commit locally and
report the commit. The owner pushes it directly, before step 9 adds the
ruleset; rerunning step 8 is the first real proof.

Its addendum the same evening: step 8's skipped shots was the owner's
variable, set wrongly and since corrected; Deploy run 38967233877 (21:08Z)
went green in all four jobs and the gallery is live with both cards. The
fault stands. Rerunning step 8 no longer proves the fix, since this
repository now runs in gallery mode: propose how the fix is proven in
site mode, and write the owner's steps. One way: set PORTFOLIO_GALLERY
to false, run Deploy, check deploy goes green, set it back and rerun.

## Errors this seat made

1. **The fault itself**, in deploy.yml since b798834: this seat wrote a
   chain of jobs where one is skipped by design and did not give the jobs
   after it a condition. Report 1 called the workflows "checked as files";
   no check read when a job runs. Cost: two Deploy runs on GitHub that
   published nothing while showing green, and a round.
2. **A date again**: the new check's docstring said GitHub's pages were
   read 2026-10-17, his local date; they were read 2026-10-16 UTC. Caught
   from a UTC timestamp before the commit.
3. **A defeat case that did not test what it named**: the first "skip two
   jobs back" case caught a job that needed a conditional job directly.
   Caught on reading it; rewritten so deploy needs a job with no `if:`
   that needs shots, and shown to be missed when the check follows needs
   one step only.

## What was done

**The facts, from GitHub's public API** [VERIFIED]: the push run of
6a4de5e (19:48Z) and the dispatch of step 8 (20:34Z) both show build and
assemble succeeded, shots and deploy skipped, and the run green. The
Checks run of the push passed on the runner in 9 minutes: every step
green, the axe fetch and its SHA-512 check among them, every check with
axe in 8 min 53 s. The gallery's address answered 404. GitHub's
documentation, read 2026-10-16: "a failure or skip applies to all jobs in
the dependency chain from the point of failure or skip onwards"; "a
default status check of `success()` is applied unless you include one of
these functions"; "a job that is skipped will report its status as
'Success'"; and `!cancelled()` is recommended over `always()`.

**Step 8's skipped shots**: this seat inferred from the job graph that
the build had not read `PORTFOLIO_GALLERY` as `true` (the job's log needs
a signed-in reader, and this machine has no GitHub CLI); the chat's
addendum confirmed the variable was set wrongly and is corrected. Run
38967233877 [VERIFIED from the API]: build, shots, assemble and deploy
green, 21:08Z to 21:09Z. The gallery answered 200 with both cards and
both previews, each demo and script 200, and the address without its
slash a 301 to the one with it, which settles that open question.

**The site-mode proof**: Test 4 in the setup steps, a copy made with "Use
this template" whose Deploy must start, fail only for want of Pages, and
then publish the sample site once its Pages source is set; the copy is
deleted after. Preferred to the chat's toggle because it takes the path
every copy takes, leaves the gallery up, and shows whether a copy's first
commit runs its workflows. Its cost: a public copy, for the test's
length, carrying the same credit lines and Code of Conduct address that
every copy carries. The toggle stays the alternative, in the report.

**Website commits and the owner's email** [VERIFIED from GitHub's
documentation, read 2026-10-16]: unless "Keep my email addresses private"
is on, an edit or a merge made on GitHub's website is authored with a
verified address of his choosing, which can be personal, and gate A sees
none of them. Test 4's copy, Part D's tests and every future merge are
such commits. Setup step 12 sets the privacy and blocks command-line
pushes that expose an address. No website commit existed on 2026-10-16:
the only branch is main, its commits all no-reply.

**The fix** (1f14aa7): deploy runs on `!cancelled() && needs.assemble.result
== 'success'`; assemble moves from `always()` to `!cancelled()` with the
same results named. checks.yml and scope.yml each have one job and no
`needs`, so the pattern cannot arise there.

**The check**, tools/check_workflows.py, standard library only: a job can
be skipped if it has an `if:` or needs a job that can be. Every job that
needs one must have an `if:` holding `always()`, `cancelled()` or
`failure()`, since any other `if:` still gets `success()`, and with the
first two must name `needs.<job>.result` for each job it needs. It refuses
a `needs` naming no job, and reports anything it cannot read at the job
level as unreadable. It reads the jobs, needs and conditions of all three
workflows correctly (printed and compared by eye). ci.py checks and gate
B run it first.

**Proofs** [VERIFIED]:

- The check on 6a4de5e's deploy.yml: FAIL, "job 'deploy': has no if: of
  its own". On the fixed workflows: 3 of 3 ok.
- The file defeat cases, 2026-10-16 21:01Z to 21:02Z: 43 failed as built
  (38 as before, 5 new: the deploy job as published, an `if:` with no
  status function, `!cancelled()` without the result, a skip two jobs
  back, an alias for `needs`), and 7 controls passed, the workflow check's
  among them. The browser defeat cases are unchanged since e794feb's run.
- `tools/ci.py checks --axe` on the working tree that became 1f14aa7, 21:03:28Z to 21:15:40Z, 732 s, exit 0: the workflow check first, 3 of 3 ok; designs; two builds each byte-identical; built files; the trace; the browser checks 720 s, 0 failures (axe 36 runs).
- Gates, in a scratch clone of 1f14aa7, 21:16:15Z to 21:20:11Z: 23 of 23 as expected, 19 defeat cases refused and 4 controls passed; new is "B: a deploy job with no if:".
- The pre-publish search runs on the final commit after this section is committed; Report 3 gives its result.

## Rejected alternatives

- PyYAML for the check: a dependency needs a record and the owner's
  approval (floor line 5); the workflows use a small subset of YAML, read
  here by indentation, with anything else refused.
- Accepting any explicit `if:`, as the chat's wording allows: GitHub still
  adds `success()` to an `if:` with no status function, so such a job is
  skipped the same way.
- `always()` for deploy: GitHub's page recommends `!cancelled()`, so a
  cancelled run stops.
- The chat's toggle of `PORTFOLIO_GALLERY` as the proof: it does not take a
  copy's path and takes the gallery down for a few minutes; kept in the
  report as the alternative to Test 4.

## Checked and found already correct

- docs/how-to/use-this-template.md already told users their first Deploy
  run may fail before Pages is set up; it now also says shots shows as
  skipped.
- Chrome runs on GitHub's runner with --no-sandbox, as the workflows set:
  the browser checks and the previews both ran there.

## Findings and recommendations

1. Edits and merges on GitHub's website escape gate A, and use his
   account's chosen address unless it is kept private: setup step 12,
   before Test 4, Part D or any merge.
2. Steps 4 and 5 have not been reported to this seat; step 5 must exist
   before 2026-11-02.
3. Another project's tests ran on this machine during this round's local
   checks; the browser checks took 720 s against 623 s the day before.

## Not done

- Nothing pushed by this seat. The fix is proven on GitHub only by Test 4,
  after the owner's push.
- The scope check has not yet run; no pull request has been opened.

---

# Round 4, 2026-10-18 UTC: the setup guide as followed

Model: Claude Opus 5.5 (claude-opus-5-5), in Claude Code, the same session
continued. HEAD at start: e0b0f5e, equal to origin/main after the owner's
push; main is protected by a ruleset, so this round's work is on the
branch setup-guide-fixes. HEAD at end: the commit that adds this section,
on that branch. Mode: mutating. Ran from about 12:10Z.

## What was asked

The portfolio architecture chat, relayed by the owner: setup steps 1 to
12 and Tests 1 to 4 are done, each result checked against GitHub's API.
Eight fixes: step 9.7 and Test 1 (scope cannot be added to the ruleset
before it has run); Test 2's CSS, which fails axe in device dark, with
`:root { color-scheme: light; }` as the remedy; Test 2's steps, with
direct links and a wait for both checks; a question for the owner on dark
mode in the design contract, proposed, not decided; step 11's
description and the label's; step 12's second box optional; website
commits carry his profile name, to be said and recorded; and
check_workflows.py's limit, to be stated. Deliver on a branch; the owner
pushes it and opens the first real pull request to main.

## Errors this seat made

1. **Test 2's CSS went stale when axe joined CI.** It was checked on
   2026-10-12 with every check then standing; c7e3fd9 added axe to the
   checks on 2026-10-16 and the guide's "checked with every check" was
   not rerun. Cost: a failed checks run in the owner's setup (PR 5 at
   4d96a72, 09:46Z to 09:59Z, read from the API) and the chat's run to
   find the cause.
2. **The guide's Test 2 steps** led to two pull requests of one file each
   (PRs 2 and 3), each failing the design check, rightly. Cost: two
   pull requests that cannot be deleted.
3. **Step 9 asked for a check the picker cannot offer** before it has run.
4. **Step 11's title promised a description** no sub-step set.
5. **Step 12 made blocking command-line pushes mandatory**, which would
   refuse pushes from any of his repositories that commit with an
   account address.
6. **This round's first defeat case for website commits** expected the
   name anywhere in the output, which another case already put there, so
   it could not fail. Tied to its own commit before it was run.

## What was done

**Checked from GitHub's API** [VERIFIED]: the ruleset `main` is active
with deletion, non_fast_forward, pull_request (0 approvals) and required
checks "checks" and "scope", both from GitHub Actions (integration 15368);
the bypass list is not shown to an unauthenticated reader. Pull requests
1 to 5 are closed unmerged; every commit in them is authored with his profile's name and the
no-reply address, and committed by GitHub. Scope ran on
each (pull_request_target): failed on PRs 1 and 4, passed on 2, 3 and 5;
on PR 4 in 6 s, with checks passing in 9 min; on PR 5 (edfe07f) both
passed, checks 10:52Z to 11:06Z. The CSS on PR 5 is the guide's with
`:root { color-scheme: light; }` first. pg-copy-test answers 404.

**Test 2's CSS, reproduced** on Chrome 154, axe-core 4.14.0, a gallery
with the test design: without the line, 4 failures in 221 s, all on the
test design in device dark at 360 and 1366 px, color-contrast on the
menu's `a[aria-current]`; with it, 0 in 207 s. The chat's run on
Chromium 141 found the same.

**Committed on setup-guide-fixes** (96675dc), each item as the chat
asked: step 9.7 adds checks only, and Test 1 adds scope once its pull
request has run it; Test 2's CSS with the line and why, its steps by the
two direct links, and a wait for both checks; step 2's and step 11's
description as the owner set it, and the label's; step 12's second box
optional, and its first now says website commits carry the profile's
name; CLAUDE.md and ADR-0002's Changes record that name on website
commits and merges; check_workflows.py's docstring and standing-checks.md
state its limit, which this seat confirmed (`!cancelled() &&
needs.assemble.result != 'success'` passes, exit 0). Two additions: a
status line opening the guide, and Test 1 to run once more on or after
2026-11-02, because until then GitHub only evaluates its block on
`pull_request_target` and the scope check runs with or without step 5's
policy; every scope run so far was on 2026-10-17 or 18.

**The pre-publish search** now allows his profile's name as the author or
committer name of a commit with his no-reply address, and nowhere else.
Its defeat run, in a scratch clone: 7 of 7 cases found, the new one his
name as a commit's author with another address; and the control, his
name with his no-reply address, not reported.

**Proofs** [VERIFIED]: the file defeat cases, 13:32Z to 13:33Z, 43 failed
as built and 7 controls passed; gates A, B and C passed on 96675dc.

**The question for the owner, proposed**: (a) the contract asks every
design to be legible in light and in dark, and a light-only design adds
`:root { color-scheme: light; }` and hides the Dark switch, both shown in
add-a-design.md; or (b) the engine stops declaring dark for every design:
a design says in design.json whether it offers dark, and the engine
writes the colour-scheme tag from that and leaves the switch out when it
does not. Recommended: (b), so the least CSS passes as it is and no
design shows a switch that does nothing; it changes the design format,
so ADR-0006 gains a Changes row, and the two maintained designs declare
dark. Either way CONTRIBUTING.md's "dark if it offers both" changes.

## Rejected alternatives

- Changing the contract or the engine now: the chat asked for a proposal
  and the owner's decision.
- A new record for website commit names: it is a fact GitHub sets, not a
  choice; ADR-0002's Changes holds it beside the rule it qualifies.

## Not done

- Nothing pushed; the branch waits for the owner.
- Step 5's proof, on or after 2026-11-02.
- The dark-mode decision and what follows from it.

---

# Round 5, 2026-10-18 UTC: dark mode by the design's word; CAPABILITIES' private lane

Model: Claude Opus 5.5 (claude-opus-5-5), in Claude Code, the same session
continued. HEAD at start: 5fe7e11, the website merge of pull request 6,
whose tree is 165fa5a's (compared here). Work on the branch
dark-mode-and-capabilities. HEAD at end: the commit that adds this
section, on that branch. Mode: mutating. Ran from about 15:35Z.

## What was asked

The portfolio architecture chat, relayed by the owner, after verifying
Report 4 (pull request 6 merged as 5fe7e11; Checks and Deploy green on it;
its CV search over 220 objects found no CV text). Two of the owner's
decisions of 2026-10-18:

1. Dark mode, option (b): a design states in design.json whether it
   offers dark; when it does not, the engine writes a light-only
   colour-scheme tag and leaves out the Dark switch. An ADR-0006 Changes
   row; build.py, the templates and check_design.py changed, each with a
   defeat case; CONTRIBUTING.md and add-a-design.md to match; then show
   that the guide's Test 2 CSS passes without its colour-scheme line, and
   simplify Test 2 if it does.
2. CAPABILITIES: the public file stays, in this seat's lane only and
   product-facing. The architecture chat's lane is never committed: a
   gitignored file this repository's chat will keep, its name this seat's
   to choose, in .gitignore and gate A with a defeat case. The public
   file's line on that lane and CLAUDE.md's section to say so. And a
   question to propose on: copies inherit the public CAPABILITIES.md.

Commit on a branch; the owner pushes it and opens the pull request.

## Errors this seat made

1. **Backslashes through a Git Bash heredoc, a third time**: two `\\n` in
   an edit to tools/prove_checks.py reached the file as line breaks and
   broke two strings. Caught by Python refusing the file, before any run
   or commit; repaired with the file tool, and the whole diff read for
   other damage. Every later edit this round went through scripts written
   with the file tool.
2. **The Dark switch's `{% endif %}` at a line's end** ate the newline
   after each switch, changing both maintained designs' pages by one
   whitespace each. Caught by diffing a gallery built from main against
   the branch's; moved to the next line's start, after which the pages
   are byte-identical.
3. **A background job started with `&`** inside a background command, so
   its notification came at once; watched by its log instead.

## What was done

**Dark mode** (39e49e6). design.json's `dark`, true or false, required.
build.py's `load_design` refuses anything else and passes it on;
base.html.j2 writes `light dark` or `light`; nav.html.j2 includes both
Dark switches only for `true`; site.js no longer reads `--pg-theme`, which
`dark` replaces, and plain's design.css loses it. check_design.py
requires `dark`; check_built.py refuses a site page whose colour-scheme
tag and Dark switch disagree (the gallery's own page, which has no menu,
is not held to it). Both maintained designs say `true`. A gallery built
from main and one from the branch differ only in site.js and plain's
design.css [VERIFIED by diff]. The contract gains "Light and dark" and
loses `--pg-theme`; add-a-design.md shows `dark` and what it does;
CONTRIBUTING.md reviews dark "when its design.json says it offers dark";
ADR-0006's Changes row records the decision.

**Test 2 without its line** [VERIFIED]: the guide's three-line CSS with
`"dark": false`, built into a gallery beside both designs: its page has
`content="light"` and no switch; every check with axe, 15:40Z to 15:56Z,
0 failures in 960 s (tree 72 runs, keyboard 12, joins 6, anchors 204,
words 6, motion 4, axe 48). The guide's Test 2 now drops the line and
says `"dark": false`.

**The private lane** (d612b96). The file is CAPABILITIES-PRIVATE.md, a
name that says what it is beside CAPABILITIES.md. .gitignore ignores it
at any depth; gate A refuses it at any path and in any letter case, as it
refuses CHAT_STATE.md. CAPABILITIES.md says the lane is kept privately and
loses its paragraph on the seats, which described the owner's role.
CLAUDE.md's section and gate table, and ADR-0008's Changes, match.

**Proofs** [VERIFIED]:

- File defeat cases on the working tree, 15:38Z to 15:40Z: 48 failed as
  built, 5 new (no dark, dark neither true nor false, a build without it,
  a light-only tag with the switch, a page offering dark without it); 7
  controls passed.
- Every defeat case on a fresh clone of d612b96 with a new venv, `prove_checks.py --browser --axe`, 15:57:51Z to 16:16:59Z, 1,148 s: 58 failed as built (48 file, 10 browser), the 6 dark-mode cases among them; 9 controls passed, axe's among them.
- `tools/ci.py checks --axe` on the same clone, 16:16:59Z to 16:27:21Z: exit 0 in 622 s; the workflow check, both designs, two builds each byte-identical (14 and 18 files), the built files, the trace (196 of 196), the browser checks 614 s with 0 failures (axe 36 runs).
- Gates, in a clone of d612b96, 16:27:35Z to 16:30:26Z: 25 of 25 as expected, 21 defeat cases refused and 4 controls passed; new are CAPABILITIES-PRIVATE.md staged with -f at the root and as docs/capabilities-private.md.
- The pre-publish search runs on the final commit after this section is committed; Report 5 gives its result.

**The question, proposed**: see Report 5's section 6. A copy inherits
not only CAPABILITIES.md but every file that serves only this project.

## Rejected alternatives

- Keeping `--pg-theme` beside `dark`: two sources for one fact, and a
  design saying `true` in design.json could still hide its switch.
- `dark` optional with a default: the decision asks the design to state
  it, and a default would decide for contributors who never read it.
- Naming the private file after the chat (as CHAT_STATE.md is): its
  content is a lane of CAPABILITIES, and the name says so beside it.

## Not done

- Nothing pushed; the branch waits for the owner.
- What to do about project files in copies: the owner's to decide.

---

# Round 6, 2026-10-18 UTC: a copy cleans itself up, once

Model: Claude Opus 5.5 (claude-opus-5-5), in Claude Code, the same session
continued. HEAD at start: 2b70358, the website merge of pull request 7,
whose tree is bb5a4bb's (compared here). Work on the branch
template-cleanup. HEAD at end: the commit that adds this section, on that
branch. Mode: mutating. Ran from about 18:00Z.

## What was asked

The portfolio architecture chat, relayed by the owner, after reading the
dark-mode branch before he pushed it: his decision of 2026-10-18 on what
copies inherit. Option (a) now, a "Make it yours" list in the user guide,
CODE_OF_CONDUCT.md and CODEOWNERS first; and, in place of (c), his idea: a
cleanup workflow that runs once in a copy, removes the project-only files
and commits. Read JetBrains' intellij-platform-plugin-template's cleanup at
its source and rate it as research 0004 rates sources. Guard it: never in
Waqas01CP/portfolio-gallery, once and idempotent in a copy. Establish by
test, not by forum, whether the workflow's token can change files under
.github/workflows/, and if not, make project-only workflows inert in a
copy. Make sure the copy's checks and build pass after the cleanup, and
say what the user sees. contents: write in the cleanup job only. Record
it. Prove it by a setup test like Test 4. Then shrink the list to what the
cleanup cannot remove. And, from the owner: the guide's line "Not
verified: whether GitHub runs workflows for the first commit of a template
copy" is to say what Test 4 saw.

## Errors this seat made

1. **The new check first listed files with git**, which neither gate B's
   staged tree nor the defeat harness's copy has: all six of its defeat
   cases and its control failed on a traceback, not on what they plant.
   Caught by the harness's first run, before any commit; it now walks the
   folder when there is no repository.
2. **Two claims in the user guide's first draft** went past the evidence:
   that Template cleanup starts "within a minute" beside Checks and Deploy,
   which Test 4 could not have seen, and that GitHub "does not let" the
   token change workflow files, which rests on one practitioner's log.
   Caught on reading back; reworded before the commit.
3. **The cleanup's check ran before the design check** in gate B and
   ci.py checks, so a staged design with a fault surfaced as "the cleaned
   copy fails tools/check_design.py", one step from its cause. Caught by
   the gate proofs (24 of 25); moved after the checks it repeats in
   d5771c3, after which 25 of 25.
4. **The gate harness's planted design** (scratch) had no `dark` since
   Round 5, so "B: a design with @import" was refused for two faults, not
   the one it names. Caught the same run; it now says `"dark": false`.

## What was done

**Research** [VERIFIED, read 2026-10-18]. JetBrains'
`.github/workflows/template-cleanup.yml` at its source (repository a
template, 3,764 stars; file last changed 2026-09-28, b871890), rated
**Primary, a precedent**: on push to main when the repository's name is
not the template's; `contents: write`; replaces files from
`.github/template-cleanup/`; deletes the project's own files and two
workflow files, its own among them; pushes with the workflow's token
through ad-m/github-push-action; actions not pinned. Their issue 486
(2024-11-04) quotes a run's log, "refusing to allow a GitHub App to create
or update workflow ... without `workflows` permission", rated
**Practitioner report, one user's run**; searching their issues found no
report of the cleanup's deletions failing. GitHub's documentation, rated
**First-party**: events from the workflow's token start no new run, except
workflow_dispatch and repository_dispatch; the token's permissions have no
workflows scope.

**Built** (d46f349, with the check's order in d5771c3):

- `.github/template-cleanup/remove.txt`, the project-only paths, those
  naming the owner first; `copy-README.md`, a copy's README with a credit
  line to the project and no name; `cleanup.py`, which refuses unless
  GITHUB_REPOSITORY is another repository and the event says it is not a
  fork, refuses a listed path that is absolute, climbs out or names a
  workflow file, deletes what is listed, puts the README in place, and
  deletes its own folder last, so a later run finds nothing.
- `.github/workflows/template-cleanup.yml`: on push to main and by hand;
  the job only where the repository is not Waqas01CP/portfolio-gallery and
  not a fork; `contents: write` in that job, `permissions: {}` above it;
  checks out the newest default branch, so a second run sees the work
  done; commits as github-actions[bot]; then, only when it cleaned, tries
  to delete scope.yml and itself in a commit of their own and leaves a
  notice either way. scope.yml's job now runs only in this repository.
- `tools/check_template_cleanup.py`, in ci.py checks and gate B while the
  cleanup exists, and its six defeat cases with a control.
- use-this-template.md: step 1 says what Test 4 saw of a first commit; a
  new step 2, "Make it yours", with what the cleanup does, the list for a
  copy whose cleanup did not run, CODE_OF_CONDUCT.md and CODEOWNERS first,
  and the two workflow files that may stay; the link to add-a-design.md
  points at the project, since a copy loses it.
- The setup guide's Test 5: a throwaway copy, pg-cleanup-test, whose runs
  and files the chat reads before it is deleted.
- ADR-0015, accepted; ADR-0008's Changes; the index; standing-checks.md,
  commands.md and CLAUDE.md's gate table.

**What a user sees**: three runs for the copy's first commit, Checks,
Deploy and Template cleanup; then a commit "Make it yours: remove
portfolio-gallery's project files" by github-actions, with perhaps a
second removing the two workflows, or a notice in the run that they stay.
The cleanup's commits start no run; the user's next commit builds and
checks the cleaned files.

**Proofs** [VERIFIED]:

- The check on the tree, 8 s: the guards change nothing as this
  repository or as a fork; as a copy 49 files go and README.md is
  replaced; a later run changes nothing; the cleaned copy passes its
  workflows, designs, builds, built files and trace; its 5 relative
  Markdown links resolve.
- File defeat cases, 18:26Z to 18:28Z: 54 failed as built, 6 new for the
  cleanup (CODE_OF_CONDUCT.md left off the list; build.py put on it; each
  guard removed; its folder not removed; a kept document linking to a
  removed record); 8 controls passed, the cleanup's among them.
- On a fresh clone of d5771c3 with a new venv, 18:53Z to 19:05Z: the file defeat cases, 54 failed as built and 8 controls passed; then `tools/ci.py checks --axe`, exit 0 in 633 s, the cleanup's check after the content trace (50 files removed in its copy, a fresh clone's tree), the browser checks 621 s with 0 failures. The same run on d46f349, before the reorder: exit 0 in 637 s.
- Gates, in a clone of d5771c3, 18:48Z to 18:52Z: 25 of 25 as expected, 21 defeat cases refused and 4 controls passed. On d46f349 the run was 24 of 25 (errors 3 and 4).
- The pre-publish search runs on the final commit after this section is committed; Report 6 gives its result.

## Rejected alternatives

- A guard by the repository's name alone, as JetBrains has: a copy that
  keeps the name would be skipped and a fork caught only by accident; the
  guard here is the full name and the fork flag.
- Running the cleanup on every push and deleting whatever matches: a user
  who later adds a `logs/` of their own would lose it; the list deletes
  itself, so the cleanup acts once.
- Granting `actions: write` to disable the workflow afterwards: more
  permission than the job needs.

## Not done

- Nothing pushed; the branch waits for the owner.
- Test 5, the owner's, then the chat's reading, before the list in the
  guide can shrink to what the cleanup truly leaves.

---

# Round 7, 2026-10-19 UTC: the content trace says where and what to do

Model: Claude Opus 5.5 (claude-opus-5-5), in Claude Code, the same session
continued. HEAD at start: 122dc8b, the website merge of pull request 8,
whose tree is 1173d13's (compared here). Local main updated from origin;
the merged branches setup-guide-fixes, dark-mode-and-capabilities and
template-cleanup deleted locally. Work on the branch
content-trace-guidance. HEAD at end: the commit that adds this section,
on that branch. Mode: mutating. Ran from about 12:00Z.

## What was asked

The portfolio architecture chat, relayed by the owner, after setup Test 5:
record that the workflow's token may delete workflow files (ADR-0015,
A3); correct Test 5's step 5, which changed a fact in site.json alone and
predicted green; make the rule that every edit to site.json or items.json
must also be in cv.md impossible to miss, in the user guide before the
field list, in the copy's README and in the content trace's failure
message, which is to name content/cv.md, say what to do and point at the
nearest CV line, with a defeat case for the message; shrink "Make it
yours" to the fallback for a copy whose cleanup did not run, in neutral
wording. And, as a proposal only, the showcase: the owner's direction and
his decisions D1 to D3 of 2026-10-18, with options and a record.

## Checked before starting

[VERIFIED, GitHub's API, 2026-10-19] Pull request 8 merged at
2026-10-18 20:51:50Z as 122dc8b, head 1173d13. On it, Checks and Scope
succeeded; on main, Checks and Deploy succeeded, and Template cleanup's
run 39165247220 concluded skipped, its one job skipped: ADR-0015's third
confirmation.

## Errors this seat made

1. **Test 5's step 5, written in Round 6**, changed one word of
   site.json's "location" and predicted green. The content trace refused
   it, correctly: content/cv.md line 12 holds the same text. The step was
   never run against the trace before it was written. It cost the owner
   two commits and three runs (the chat's report). Step 5 now edits a
   contact line, which the trace takes as written; run here first: the
   trace passes, 196 blocks, and the word shows under Contact.
2. **The full-check script** (scratch) did not start: GNU tar read the
   "C:" of the axe tarball's path as a remote host. Fixed with
   --force-local; nothing in the repository.
3. **The first commit attempt** passed its message through PowerShell 5.1,
   which split it at its inner double quotes; git refused and nothing was
   committed. Committed from a file.
4. **CAPABILITIES.md's "Decision records" row** still said 14 records,
   13 accepted, after Round 6 added ADR-0015, accepted. Found on
   re-measuring the numbers; now 15, 14 accepted, 1 proposed.

## What was done

**The trace's failure message** (tools/check_content.py, db055e5). The
report opens by naming the CV file. Each NOT TRACED block is followed by
the nearest CV line and its number, when one holds at least half the
text's characters in runs of three or more, or by "no line of
content/cv.md is close"; for a block the page's markup splits, the
pointer names the piece that fails on its own. Each MISSING line carries
its CV line number; line numbers survive the CV's comments. A failure
ends with "What to do": the page's words come from site.json and
items.json, so a change to either usually needs the same change in the
CV; for each kind of failure, what to change; or turn the trace off.
Test 5's edit now reads, in part:

    NOT TRACED: Example City, Examplelund
      nearest in content/cv.md, line 12: Example City, Exampleland
    MISSING: Example City, Exampleland (content/cv.md, line 12)

Also run: a number changed on the page points at line 31; new text with
nothing like it in the CV says no line is close; site.json and cv.md
changed together pass, 196 traced; a contact line changed alone passes.

**Its defeat case** (tools/prove_checks.py): Test 5's edit, which passes
only if the output names the NOT TRACED text, cv.md's line 12 for both
directions, and what to do. Proven both ways: with this check it fails
as built; with main's check_content.py under the new harness, the trace
still exits 1 but the case is unproven, 1 of 55.

**The rule where a user meets it.** use-this-template.md's "Write your
content" (step 4; the chat called it step 3) says it before the field
list, puts cv.md first in the list, and says that the browser commits one
file at a time, so the first of two commits fails and the second goes
green; step 5 says a failure names the nearest cv.md line. The copy's
README, the README's step 3, content.md and cv-format.md say it too.

**"Make it yours"** describes the cleanup's two commits as fact, lists
the two workflows in the fallback with the rest, and drops the paragraph
on files that may stay. CODE_OF_CONDUCT.md and CODEOWNERS are described
by what they do, not by whom they name. A sweep of the 52 files a cleaned
copy keeps found one more: tools/check_browser.py's docstring said "His
method", naming a file a copy lacks; now neutral.

**Records and guides.** ADR-0015: A3 annotated as measured, the "may
stay" consequence annotated, Confirmation's results, a Changes row. The
setup guide's status, Test 5's steps 2, 3 and 5, and what Test 5 proved.
standing-checks.md's trace row names the new defeat case.

**The showcase**, proposed in Report 7 with a draft record; nothing built.
Read for it, 2026-10-19: emmabostian/developer-portfolios at its source
(its CONTRIBUTING.md, pull request template, link-check and
parking-redirect workflows and script), **Primary, a precedent**; GitHub
Docs on the schedule event and on workflow permissions, **First-party
documentation**; Mastodon's profile verification and Google's "Qualify
your outbound links", **First-party documentation** of their own
mechanisms.

**Proofs** [VERIFIED]:

- File defeat cases on the working tree: 55 failed as built and 8
  controls passed, 96 s.
- On a fresh clone of db055e5 with a new venv, 12:38Z to 12:49Z: `tools/ci.py checks --axe`, exit 0 in 648 s; the trace 196 blocks, 0 not traced; the cleanup's check removed 50 files in its copy and resolved its 5 links; the browser checks 0 failures in 634 s.
- Gates, in a clone of db055e5, 12:49Z to 12:55Z: 25 of 25 as expected, 21 defeat cases refused and 4 controls passed.
- The pre-publish search runs on the final commit after this section is
  committed; Report 7 gives its result.

## Rejected alternatives

- Pointing a failed block at the CV line with the most words in common:
  "Example City", a line of its own under Experience, beat line 12 for
  "Example City, Examplelund". The nearest line is judged by shared
  characters in runs, so a misspelt word still counts.
- "Change both files in the same commit" in the message: the browser's
  editor commits one file at a time.
- A workflow_dispatch fallback in "Make it yours" (run the cleanup by
  hand): plausible from the workflow's triggers, never tested; left out of
  the user guide.

## Not done

- Nothing pushed; the branch waits for the owner.
- The showcase: waiting on the owner's answers.
- Test 1 once more, on or after 2026-11-02.
