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

---

# Round 8, 2026-10-19 UTC: templates first, then a showcase

Model: Claude Opus 5.5 (claude-opus-5-5), in Claude Code, the same session
continued. HEAD at start: 4396a20, the website merge of pull request 9,
whose tree is 1953bb4's (compared here); Checks and Scope green on the
pull request, Checks and Deploy green on main, Template cleanup skipped
(GitHub's API). Local main updated; content-trace-guidance deleted
locally. Work on the branch showcase. HEAD at end: the commit that adds
this section. Mode: mutating. Ran from about 14:20Z.

## What was asked

The portfolio architecture chat, relayed by the owner: his answers to
Report 7's six questions (one folder per login; the weekly check with no
permissions, its failure the notice; floor line 1 read as protecting the
template, so his own site may be an entry and the Default design's
in_use; never renders means fetching responses is allowed; the home page
links to github.com/<login>; no exact screenshot size, the card showing it
whole with bands, HD the target). Measure screenshot sizes and the
gallery's weight and Lighthouse with 10 and 50 cards before fixing the
screenshot rules; investigate, not build, a screenshot workflow in a
contributor's fork; then build everything settled, with a defeat case for
every rule and the fetch cases on a local server, and no entry for the
owner's site.

## Errors this seat made

1. **A capture script waited on lazy pictures** that never load outside
   the view, and timed out on the phone view. A scratch script; the
   capture was taken again without the wait.
2. **check_built.py's first credit rule** asked for a link other than the
   project's, which Plain's credit lacks, since Plain's author is the
   project. Caught on reading it back, before any run; the rule now asks
   for the project's link, then the author's.

## The measurements

**Screenshots** [VERIFIED, 14:30Z to 14:45Z]. First screens of the
gallery's Default and Plain demos and of two live portfolio sites, the
owner's and brittanychiang.com, captured by headless Chrome 154 at device
scale 1, in bytes:

| Site | 1280x720 PNG | JPEG q85 | WebP q82 | 1920x1080 PNG | JPEG | WebP |
|---|---|---|---|---|---|---|
| Default | 426,464 | 114,554 | 65,800 | 611,863 | 192,528 | 107,566 |
| Plain | 52,739 | 94,344 | 51,830 | 75,620 | 139,733 | 69,842 |
| Owner's site | 460,892 | 117,322 | 67,578 | 628,364 | 188,963 | 106,258 |
| brittanychiang.com | 200,927 | 97,877 | 56,868 | 257,119 | 140,435 | 78,196 |

The operating system's tool could not be driven headless here. The same
pixels re-encoded with Windows' own encoders, GDI+ (System.Drawing) and
WIC (PresentationCore), at JPEG quality 85: at 1280x720, PNG 43,779 to
476,882 and JPEG 100,593 to 121,691; at 1920x1080, PNG 65,081 to 656,604
and JPEG 148,756 to 202,262. At a Retina Mac's density, 1280x720 at
scale 2 is 2560x1440: PNG 158,343 to 1,399,366. Metadata: Chrome's files
carry none but an ICC profile; Windows' GDI+ JPEG writes an EXIF block of
three resolution tags (0x5110 to 0x5112); two Mac screenshots from public
repositories carry eXIf and an XMP block saying "Screenshot", one with
Apple's iDOT chunk. So "no EXIF or XMP" would refuse ordinary
screenshots; the rule is no location.

**The gallery** [VERIFIED, 14:45Z to 14:59Z]. Built with 0, 10 and 50
entries, the screenshots cycling through the 1280x720 captures: the page
4,681, 10,575 and 33,881 bytes; every file on it 69,427, 1,777,947 and
7,626,211 bytes. Lighthouse 13.5.0, default mobile, median of five, from
127.0.0.1: LCP 1,113, 1,149 and 1,662 ms; CLS 0; TBT 71, 54 and 38 ms;
70,310, 973,985 and 997,291 bytes loaded, since Chrome fetches lazy
pictures some way ahead of the view. Within ADR-0009's limits in every
case. Looked at in light, dark and at a phone's width: each screenshot
whole, bands in the card's colour.

**The limits** chosen from them: MIN_WIDTH 1,024, MAX_WIDTH 1,920,
MAX_BYTES 500 KB, landscape, still, PNG, JPEG or WebP by first bytes, no
GPS in EXIF or XMP. Every 1280x720 capture passes in every format and
encoder; at 1920x1080 every JPEG and WebP passes and the PNGs of the three
busier sites (517 to 657 KB) do not; every 2560x1440 capture fails on
width. The two Mac screenshots pass.

**The fork workflow, investigated** [sourced and measured]: a
workflow_dispatch workflow in this repository, guarded to run only in a
fork, taking the screenshot of the URL in the contributor's entry.json
with the runner's Chrome and committing it to their branch with the
fork's own token. A fork's Actions are off until its owner enables them
("Events that trigger workflows", already cited by use-this-template.md);
the workflow must be on the fork's default branch to be run by hand
("Manually running a workflow", read 2026-10-19); public repositories run
free on standard runners (GitHub's billing documentation, read
2026-10-19); the deploy's screenshot job took 12 to 14 s for two designs
on GitHub's runner (runs 39265254071 and 39165247248). Costs: one more
workflow here holding contents: write in forks, removed from copies; the
contributor's click to enable Actions and its warning; sites that refuse
datacenter addresses give a blank or blocked capture. Not built; the
manual screenshot stays the default.

## What was built

- tools/check_showcase.py: the files, and with --fetch-changed,
  --fetch-all or --fetch-url the responses, never rendered.
- The scope check takes showcase/<author>/; build.py reads showcase/ and
  in_use; the gallery shows Templates, then Showcase, each with a count;
  the footer credit names the design and its author; check_built.py,
  check_design.py, check_content.py and check_workflows.py learn the new
  rules; checks.yml fetches a pull request's changed sites;
  showcase-links.yml checks weekly with permissions: {} and an anonymous
  clone (tried here: it needs no token).
- The template cleanup removes showcase/, the how-to, the tool and the
  weekly workflow, and drops in_use from every design.json; its check
  plants both and proves them gone.
- docs/how-to/add-to-the-showcase.md; CONTRIBUTING.md, the README, the
  user guide, add-a-design.md, content.md, standing-checks.md and
  commands.md; the setup guide's Test 6 and the weekly check's notes.
- ADR-0016, accepted; Changes rows on ADR-0001, 0002, 0006 and 0015;
  CLAUDE.md's rule of places and floor line 1's reading.
- Gate A's private list allows his name in showcase/waqas01cp/entry.json;
  the pre-publish search allows it there and on his own card in the built
  gallery.

## Proofs

- File defeat cases on the working tree, before the commit: 95 failed as built, 40 of
  them new; 7 planted controls passed (a Mac screenshot with EXIF and
  XMP; a JPEG with Windows' EXIF; a WebP; the author's own entry in scope;
  a page linking its profile; a 403 reported, not failed; a gallery with
  an entry); 9 controls passed; 144 s.
- Live, 2026-10-19: the owner's site and brittanychiang.com pass with
  their owners' logins and fail with another; example.com fails for its
  missing link; http:// fails; expired.badssl.com fails for its
  certificate; 10.0.0.1 fails as an IP address.
- Gates, in a clone of 5a7cecf, 17:56Z to 18:03Z: 27 of 27 as expected,
  22 defeat cases refused and 5 controls passed, among them his name
  allowed in his own entry and refused in another's.
- On a fresh clone of 5a7cecf with a new venv, 18:03Z to 18:45Z: every defeat case with the browser and axe, exit 0 in 1,227 s, 105 failed as built (95 file, 10 browser), 11 controls and 7 planted controls passed; tools/ci.py checks --axe, exit 0 in 642 s, the browser checks 0 failures in 627 s, the cleanup's check removing 55 files from its copy; and a gallery holding ten showcase entries: its files checked, then every browser check with axe, 0 failures in 620 s.
- The pre-publish search runs on the final commit; Report 8 gives its
  result.

## Rejected alternatives

- Refusing all EXIF and XMP: it refuses ordinary Mac and Windows
  screenshots (measured); location is the harm.
- An exact screenshot size: the owner's answer Q6.
- One shared showcase.json: the scope check could not tell whose entry
  changed.
- actions/checkout in the weekly workflow: whether it works with
  permissions: {} was not established here; an anonymous clone needs no
  token at all.
- Requiring the engine's generator tag on an in_use site: the owner's own
  site, the Default design's likely in_use, does not carry this engine's.

## Not done

- Nothing pushed; the branch waits for the owner, whose merge approves
  the limits.
- Test 6, the owner's own entry, after the merge.
- The fork screenshot workflow: investigated only.
- Test 1 once more, on or after 2026-11-02.

---

# Round 9, 2026-10-20 UTC: a showcase screenshot is any snip, as it comes

Model: Claude Opus 5.5 (claude-opus-5-5), in Claude Code, the same session
continued. HEAD at start: e904357, the website merge of pull request 10,
whose tree is 33ab03d's (compared here); Checks and Deploy green on main,
Template cleanup skipped (GitHub's API). The local clone was already on
main at e904357 with the branch showcase deleted, by the owner. Work on
the branch showcase-any-snip. HEAD at end: the commit that adds this
section. Mode: mutating. Ran from about 10:30Z.

## What was asked

The portfolio architecture chat's Brief 9, stored word for word in
briefs/implementation-seat.md in place of Brief 1, read first for what it
still says (carried in CLAUDE.md and the handoff). The owner's aim of
2026-10-20: contributors "just take a snip and add it". His decision that
day: any screenshot as a tool saves it; the check keeps PNG, JPEG or WebP
by first bytes, a still image and no location; no width, shape or
landscape rule; the build makes the served copy; one cap, for the
repository's history, set from measurement above any ordinary full-screen
snip of a busy page on a 4K screen and a Retina Mac; Test 6 held until
this merges. To work out and report: how the served copy is made and
what a click opens; the security of decoding untrusted images; the cap's
value; whether any floor is needed; whether HEIF is worth accepting.

## Errors this seat made

1. **The limits of 2026-10-19 were this seat's design**, built as
   proposed in Report 8: the owner's Q6 said "any normal screenshot of the
   site's first screen works" and "HD as the target, not larger"; this
   seat read the target as a limit, chose 1,024 to 1,920 pixels and
   500 KB, and wrote resize steps for contributors. Its own measurements
   showed most full-HD and every Retina snip would need them. The chat
   names its part as its E36; this is the seat's.
2. **Round 8 left docs/deferred/showcase-of-users-sites.md open** after
   ADR-0016 built the showcase. Found reading Brief 1; closed.
3. **Two scratch edit scripts were written through a Git Bash heredoc**,
   which turned escapes into real newlines; both failed to parse and
   changed nothing. Rewritten with the file tool, as the handoff's first
   tool trap says.
4. **A defeat case expected the wrong words**: the check refused a copy
   carrying Chrome's colour profile at its header flag, before naming the
   chunk. The rule held (exit 1); the case now expects the words both
   refusals share.
5. **The defeat harness held its large planted snips in memory** for the
   whole run, tens of megabytes built when the cases were listed. With the
   machine near its memory limit (206 MB of 7.8 GB free, 1 GB of 32 GB
   commit free, other sessions' processes), the first fresh run's
   browser and axe controls and one axe case failed with MemoryError,
   while the same browser checks passed in ci.py checks beside them. Each
   snip is now made as its case plants it (fceaace), and the run repeated.

## The measurements

**Full-screen snips** [VERIFIED, 2026-10-20, headless Chrome 155, which
had updated itself from 154 since Round 8]. Five screens: full HD
(1920x1080), 4K at 150% (2560x1440 at scale 1.5), 4K at 100%
(3840x2160), a 16-inch MacBook Pro (1728x1117 at scale 2, 3456x2234) and
a 5K display (2560x1440 at scale 2, 5120x2880). Pages: the Default
design, the owner's site, brittanychiang.com, and Flickr's Explore, a
wall of photographs. Unsplash answered headless Chrome with its bot
protection's "Access Denied", Wikimedia Commons did not resolve from this
machine, and NASA's image page failed every capture: each was looked at
and dropped. PNG bytes, Chrome's encoder / Windows' WIC / GDI+:

| Page | Full HD | 4K 150% | 4K 100% | MBP 16" | 5K |
|---|---|---|---|---|---|
| Default | 575,396 / 600,067 / 481,533 | 1,507,968 / 1,564,956 / 1,387,214 | 1,067,165 / 1,119,006 / 952,840 | 1,921,589 / 1,946,917 / 1,791,819 | 2,363,844 / 2,414,117 / 2,204,865 |
| Owner's site | 644,272 / 671,095 / 540,592 | 1,616,738 / 1,662,091 / 1,425,775 | 1,257,323 / 1,319,046 / 1,092,855 | 1,982,988 / 2,002,629 / 1,839,644 | 2,481,408 / 2,491,928 / 2,208,833 |
| brittanychiang.com | 257,119 / 279,794 / 213,160 | 531,573 / 568,527 / 441,399 | 411,023 / 440,791 / 354,133 | 656,767 / 695,081 / 550,594 | 764,986 / 812,063 / 633,945 |
| Flickr photos | 1,730,782 / 1,751,729 / 2,525,046 | 6,161,385 / 6,350,538 / 10,236,568 | 8,209,980 / 8,391,552 / 12,439,711 | 4,958,681 / 5,122,437 / 8,328,730 | 9,494,065 / 9,901,544 / 16,928,260 |

The largest: 12,439,711 bytes at 4K and 16,928,260 at 5K, both GDI+. A
Mac's own PNG encoder could not be measured here. GitHub takes at most
25 MiB through a browser ("About large files on GitHub", read
2026-10-20). **The cap: 20 MiB (20,971,520 bytes)**, above every snip
measured and below GitHub's own limit.

**The served copies** [VERIFIED]. Drawn by OffscreenCanvas from
createImageBitmap and encoded by Chrome as WebP. With the GPU on, drawing
a large capture hung, or came out blank: a 1366x883 card of 2,810 bytes
from a 656,767-byte capture. With --disable-gpu, three drawing methods
gave the same bytes five times each (55,490 bytes, 292 colours in a
64x64 sample). At quality 0.82, from every capture above: the card,
fitting 1366x900, at most 147,498 bytes; the full view, fitting
2560x2560, at most 401,498; at quality 0.75 they were 110,708 and
300,462. Chrome's encoder adds an sRGB colour profile (ICCP) to a canvas's
WebP; the copies are rewritten to their image chunk alone, and decode to
the same size and colours.

**The gallery** [VERIFIED, 11:11Z to 11:17Z], 0, 10 and 50 entries cycling
through the captures above (originals 0, 10,057,430 and 107,247,534
bytes, never served): the page 4,681, 10,469 and 33,349 bytes; every card
copy 0, 461,556 and 3,176,044 (largest 147,016); every full copy 0,
1,037,294 and 7,348,486 (largest 401,016); the page with every card,
scrolled to the end, 69,427, 536,771 and 3,274,139. Lighthouse 13.5.0,
default mobile, median of five: LCP 1,128, 1,507 and 1,656 ms; CLS 0;
TBT 33, 16 and 70 ms; 70,310, 274,900 and 297,780 bytes loaded at first,
against 973,985 and 997,291 at 10 and 50 in Round 8. Within ADR-0009.

**HEIF** [sourced]: caniuse, read 2026-10-20, lists no support in Chrome,
Edge or Firefox, Safari only, and notes HEIC "is complex and expensive to
license"; Apple's screenshot page says a Mac saves PNG, and HEIF only with
its HDR option on macOS Tahoe 26 or later.

## What was built

- tools/check_showcase.py: no width, shape or landscape rule; the cap
  20 MiB; a HEIF file named as such. The screenshot keeps its tool's name
  ("Screenshot 2026-10-20 at 11.30.12.png"), any image suffix in any
  case, no folder, no control character, not hidden: a choice of this
  seat for the owner's aim, the same rule in build.py and the scope check.
- tools/screenshots.py makes each entry's card.webp and full.webp with
  Chrome, GPU off, quality 0.82, never enlarged, image chunk only; the
  screenshot is never published. build.py no longer copies it; the
  gallery's card shows card.webp and opens full.webp.
- The deploy's shots job makes the previews and the copies and uploads
  only those pictures, gathered in _shots/, as one folder; ci.py assemble
  takes only the pictures the gallery shows, WebP within 300 KB (card) and
  1 MB (full), image chunk only, and refuses the screenshot itself.
  ci.py checks makes them on every pull request; ci.py pictures makes and
  checks them alone. check_built.py allows them missing until --previews.
- docs/how-to/add-to-the-showcase.md: snip, save, upload, under the
  tool's own name; no sizes, no Paint, no Preview. CONTRIBUTING.md, the
  setup guide's Test 6 (a plain snip), standing-checks.md, commands.md,
  CLAUDE.md's runtime line; ADR-0016's Changes with A4 and A6; ADR-0010's
  Changes (Chrome decodes contributors' screenshots); the deferred
  showcase entry closed.

## Proofs

- File defeat cases on the working tree: 100 failed as built and 15
  planted controls passed, 199 s. New: 21 MB over the cap; HEIF under
  .heic and under .png; a GIF; a hidden file in scope; a served copy with
  EXIF, with a colour profile, missing; the screenshot among the
  pictures. Planted controls: snips at the largest sizes measured, a
  Windows full-HD PNG of 2,525,046 bytes, a Retina 2560-wide PNG with Mac
  metadata, a 4K PNG of 12,439,711, a 5K PNG of 16,928,260, a portrait
  snip, a Mac's own file name in the check and in scope, and assemble
  taking a gallery's four pictures. Gone: portrait, narrower, wider.
- Browser: copies from a screenshot with EXIF and XMP, and from one under
  a Mac's name, hold their image alone; a maker keeping Chrome's colour
  profile, and one publishing the screenshot itself, are refused.
- Gates, in a clone of 3020bb4, 11:28Z to 11:36Z: 27 of 27 as expected.
- On fresh clones, 11:36Z to 12:43Z. Of 3020bb4: `tools/ci.py checks --axe`, exit 0 in 667 s, two pictures made and checked, the cleanup's check removing 55 files, the browser checks 0 failures in 642 s; then the deploy's own path with the ten largest captures (up to 9,494,065 bytes) under a Mac's file names: the check passed them, 22 pictures were made, gathered as the shots job gathers them and assembled, the built files 0 problems, and every browser check with axe on the assembled gallery 0 failures in 644 s. Every defeat case with the browser and axe: on 3020bb4, three browser runs died of MemoryError (error 5); on fceaace, 12:17Z to 12:40Z, all 112 failed as built (100 file, 12 browser), 17 planted controls and 10 of 11 controls passed, the axe control dying of MemoryError again (334 MB free); run alone at 12:43Z on the same clone, it passed, 36 runs, 0 failures in 151 s.
- The pre-publish search runs on the final commit; Report 9 gives its
  result.

## Rejected alternatives

- A new decoding library, such as Pillow: a dependency needing a record
  (scope floor line 5); Chrome is on the runner and in the tools.
- Serving the screenshot itself on a click: its metadata and size would
  reach visitors, and visitors' browsers would decode a stranger's file.
- One served copy for both the card and the click: the card's at 1366
  wide shows little more when opened; the full copy, at most 401 KB, loads
  only on a click.
- A floor on size: the owner's review sees every screenshot; a tiny one is
  declined there. Not added; offered.
- A ceiling on pixels against a decompression bomb: Chrome decodes the
  screenshot on the pull request, so a file it cannot draw fails there and
  never merges. Not added; offered.
- HEIF: a decoder would be a dependency with licensing costs, for a Mac
  setting that is off by default.

## Not done

- Nothing pushed; the branch waits for the owner.
- Test 6, the owner's own entry, after the merge: snip, save, upload.
- Test 1 once more, on or after 2026-11-02.

---

# Round 10, 2026-10-21 UTC: the template for both kinds, cards in their own shapes, briefs off the repository

Model: Claude Opus 5.5 (claude-opus-5-5), in Claude Code, the same session
continued. HEAD at start: fa2a687, the website merge of pull request 13,
whose tree is ca4dfa0's; 4562645, the merge of pull request 11, has
a8ad6e3's tree (both compared here). Commits not made by this seat:
be09e43 and ca4dfa0, the owner's own entry made on GitHub's website, and
the merges of pull requests 11 and 13. Work on the branch showcase-shapes.
HEAD at end: the commit that adds this section. Mode: mutating. Ran on
2026-10-21 UTC, the fresh-clone proofs from 12:19Z.

## What was asked

The portfolio architecture chat's Brief 10, stored word for word in
briefs/implementation-seat.md in place of Brief 9, read first for what it
still says (the owner's aim for the showcase, in his words, carried). The
owner's answers to Report 9: keep the tool's own file name, no pixel
ceiling, no floor. Three parts. One: the pull request template covers a
showcase entry as well as a design, one template, after checking GitHub's
documentation that a contributor reaches any but the default only by a
link with a template query. Two: each showcase card takes its picture's
shape, at the card's full width, whole, and the cards are packed as on
Pinterest, in an order a keyboard and a screen reader share; limits on
shape both ways, set from measurement, in the display only, never a
refusal; each picture's space reserved; the gallery re-measured at 0, 10
and 50 entries. Three: the briefs folder leaves the repository, its
README with it, as on his site that day. Record Test 6, which passed.

## Checked before starting

[VERIFIED] from GitHub's public API: pull request 11 merged as 4562645 on
2026-10-20 at 19:47Z; Checks and Deploy green on main, Deploy's jobs
build, shots, assemble and deploy each success, so the shots job's new
gathering into _shots/ ran on GitHub's runner; Template cleanup skipped.
Pull request 12, entry.json alone at f791ea8, closed unmerged: Scope
success, Checks failed at step 4, "Fetch the showcase sites this pull
request adds or changes"; its message is in a log that needs a signed-in
read [BELIEVED: the files' check, which that step runs first, refusing an
entry with no screenshot]. Pull request 13 at ca4dfa0: Scope and Checks
success; merged as fa2a687 at 21:56Z; Checks and Deploy success on main,
Deploy's four jobs each success; Template cleanup skipped; Showcase links
by hand, run 39507307570, success. His snip: a PNG of 1077x1713 pixels,
762,666 bytes, under the name his tool gave it.

## Errors this seat made

1. **CAPABILITIES.md's "Current as of" line stayed at 2026-10-18** through
   Rounds 7 to 9, each of which changed the file. Found this round;
   corrected to 2026-10-21.
2. **One more scratch edit script went through a Git Bash heredoc** and
   failed to parse; nothing changed; rewritten with the file tool. In a
   second, a Python string's escaped newline became a real one; caught on
   reading the result and fixed before it ran.
3. **The card copy of a picture beyond the tall limit came out 1,025
   pixels wide**, one over the card's 1,024, from rounding the height cap
   up. Seen in the first build's copies, before any commit; the cap is now
   whole pixels.
4. **Two of this round's own test inputs were wrong**: the WebP for the
   orientation test carried a second header, so Chrome could not decode
   it; and a planted control failed because the owner's real entry, now
   on main, needed copies too. Each fixed in the test, not the code.
5. **The defeat harnesses assumed an empty showcase on main.** Since
   fa2a687 main holds the owner's entry. On the first fresh run of
   b17d883, tools/prove_checks.py stopped at a case that creates
   showcase/, its assemble and browser controls failed for want of his
   served copies and pictures, and the scratch gate harness's control
   for his name in his own entry was refused for two screenshots. Every
   check behaved; the harnesses did not. Fixed in 234ad59 and in the
   scratch harness. The rerun found one more of the kind: the case for a
   maker publishing the screenshot itself read the file by its
   URL-quoted name, and on his name, which holds spaces, it crashed
   instead of proving the refusal. Fixed in ba93032, with
   tools/screenshots.py now writing a name the console cannot, as a
   Mac's narrow no-break space on Windows, escaped rather than stopping.

## The measurements

**Browser support for native masonry** [sourced, read 2026-10-21]:
caniuse, "CSS Grid Lanes": supported by default only in Safari and Safari
on iOS 26.4 and later, 12.49% of users; Chrome 140 to 158, Edge 140 to
155 and Firefox 77 to 161 have it disabled by default; Samsung Internet
none. WebKit, "Introducing CSS Grid Lanes" (2025-12-19): each item goes
to the lane that places it closest to the top; `fit-tolerance`, default
1em, ignores smaller differences; the layout lets a keyboard "tab across
the lanes to all currently-visible content". Chrome Platform Status had
no entry found. [VERIFIED] Chrome 155 with
--enable-experimental-web-platform-features supports `display:
grid-lanes` and places six test items as WebKit describes; without the
flag, and with the older CSSMasonryLayout flag, it does not.

**Shapes of real snips** [VERIFIED, 2026-10-21, headless Chrome 155, GPU
off, PNG]: first screens of portfolio sites and a photo wall at
1920x1080 (0.56 times as tall as wide), 1366x768 (0.56), a Retina
1440x900 at scale 2 (2880x1800, 0.62); phones at 390x844 and 360x800 at
scale 3 (1170x2532, 2.16; 1080x2400, 2.22); ultrawides at 3440x1440
(2.39 times as wide as tall) and 5120x1440 (3.56); whole pages at 1366
and 1920 wide (2.83, 2.01, 3.47). Common screens [sourced, StatCounter,
June to August 2026]: desktop 1920x1080, 1536x864, 1366x768, 1280x720
(all 0.56); mobile 414x896 (2.16), 360x800 (2.22), 390x844 (2.16),
393x873 (2.22). Whole pages [VERIFIED] of eight portfolio sites, the
owner's among them, at 1366, 1920 and 390 CSS pixels wide: 0.56 to 10.21
times as tall as wide at the desktop widths (the owner's 10.21 at 1366)
and 2.16 to 34.76 at 390; a one-screen site is 0.56. The owner's own snip
is 1.59. So no limit separates a page from a screen; a limit caps how
tall a card grows, and how short. **Proposed: 2.4 either way**, a 21:9
screen's shape: every phone's first screen (at most 2.22; 21:9 phones
2.33) and a 3440x1440 ultrawide (2.39) show at their own shape; a whole
page, a 5120x1440 monitor and a strip are shown within 2.4, with bands.

**EXIF orientation in Chrome** [VERIFIED, Chrome 156, which had updated
itself during the round]: a 40x20 picture with Orientation 6 is shown
20x40 from PNG (eXIf) and JPEG, and 40x20 from WebP, by createImageBitmap
and by an img alike.

**Served copies** [VERIFIED] from the 13 snips, card.webp at most 1,024
wide: largest 128,784 bytes (a phone's photo wall), banded copies 4,234
to 109,214; full.webp largest 180,682.

**The gallery** [VERIFIED, Lighthouse 13.5.0, default mobile, median of
five, served uncompressed from 127.0.0.1], with 0, 10 and 50 cards drawn
from the 13 snips, the owner's entry among the 10 and 50: page 4,729,
10,383 and 32,599 bytes, gallery.js 3,094; LCP 1,075, 1,504 and 1,654 ms;
CLS 0 in every run; TBT 38, 0 and 0 ms; 74,587, 309,817 and 330,177
bytes loaded at first; every card at 50, scrolled to the end, 2,964,813
bytes. With the desktop preset, where three columns are packed, at 10
and 50: LCP 365 and 406 ms, CLS 0 in every run, TBT 0, 728,686 and
802,861 bytes at first. Within ADR-0009.

## What was built

**Part 3, the briefs folder** (56c6dc3). briefs/README.md untracked,
kept on disk; .gitignore ignores briefs/ whole; gate A refuses any path
in briefs/, its docstring and message reworded; CLAUDE.md's gate row and
Briefs section, which now carries what the README said: working space,
never committed, one file per seat, the box and tick, the brief's rank,
and where the durable trace lives. MAP.md regenerated. ADR-0008, Changes.
remove.txt still lists briefs; kept, since the cleanup skips a listed
path that is absent (below).

**Part 1, the template** (d8ccfce). GitHub's documentation, read
2026-10-21, "Creating a pull request template for your repository":
contributors "will automatically see the template's contents in the pull
request body"; others sit in a PULL_REQUEST_TEMPLATE/ folder and are
reached only with the `template` query parameter. So one template: the
opening comment names both kinds and says to delete the other section;
"A design" holds main's checklist line for line; "A showcase entry"
three lines. The showcase how-to's step 4, add-a-design's step 3,
CONTRIBUTING's step 5 and setup Test 6's step 4 say which section to
keep. It is still in remove.txt.

**Part 2, the cards** (b17d883). build.py: SHOWCASE_TALL and
SHOWCASE_WIDE, 2.4; showcase_shapes() gives each copy's size and the
picture's place in it; the size comes from the screenshot's header,
turned for an EXIF quarter turn in PNG and JPEG (check_showcase's
readers, which now read Orientation; WebP's is left, as Chrome leaves
it). The gallery's img carries that size. screenshots.py draws each copy
at it, with transparent bands beyond the limits, and fails an entry
Chrome reads at another size. gallery.css: the showcase list a grid of
the same columns, `display: grid-lanes` inside @supports; gallery.js,
new, same origin, packs where grid-lanes is missing. check_built: each
showcase picture's width and height, within the limits; with --previews,
each card's copy the size reserved. check_browser: the packing check.
prove_checks: the cases below. ADR-0016, Changes; standing-checks.md;
the how-to.

**The harness** (234ad59, ba93032): allows for entries on main (error 5).

## Proofs

All on 2026-10-21, one browser job at a time, Chrome 156.

- **Part 1** [VERIFIED]: nothing in the repository checks a template's
  text, so a scratch script read it against the documents: the comment
  closes before the first section; the two sections are named as each
  guide says to keep them; the design checklist is main's line for line;
  the showcase section names no tool, size or rename; every path it names
  and the how-to heading it quotes exist; remove.txt lists it. 0 problems.
- **Every check with axe**, `tools/ci.py checks --axe`, on a fresh clone
  of b17d883: exit 0 in 643 s, the browser checks 621 s (tree 48 runs,
  keyboard 8, joins 4, anchors 136, words 4, motion 3, packing 12, axe
  36), 0 failures; the cleanup's check 0 problems.
- **The deploy's own path** on that clone with the 13 real snips under a
  Mac's file names, the owner's entry beside them: the files' check
  passed; build, screenshots.py, the shots job's gathering (30 pictures),
  assemble exit 0, check_built --previews on the assembled gallery 0
  problems; every browser check with axe on it, the packing check on 14
  cards among them, 0 failures in 622 s.
- **Every defeat case with the browser and axe**, on a fresh clone of
  ba93032: exit 0 in 1,673 s; 121 defeat cases (104 file, 17 browser)
  fail as built, naming what failed; 11 controls and 21 planted controls
  pass. New this round: a showcase picture without its width and height;
  a picture beyond the tall limit and one beyond the wide limit shown at
  their own shape; a card's copy not the size reserved; a build that
  ignores a PNG's EXIF turn; and, in the browser on nine planted shapes,
  CSS columns filling down (a card above the one before it), a picture
  without its reserved size, the tall limit taken out, and the script
  taken out (gaps). Controls: a copy at its reserved
  size; a JPEG turned by its EXIF; copies from a PNG turned by its EXIF;
  the packed showcase with nine shapes. The run on 234ad59 had 120 of 121,
  the 121st crashing in the harness (error 5).
- **The gates**, on a scratch clone of 234ad59: 23 defeat cases refused
  (briefs/README.md staged with -f among them, "briefs/ is working space
  and is never committed, its README with it") and 5 controls passed.
- **The cleanup with a listed path absent** [VERIFIED]: cleanup.py skips
  a listed path that does not exist and prints nothing for it; its check
  fails only on a listed path still present afterwards. On the fresh
  clone, which has no briefs folder, the check passed: guards hold, 56
  files removed, a later run changes nothing, the cleaned copy builds and
  checks, its 5 links resolve.
- **The pre-publish search** at this section's commit: see Report 10, 5;
  it finds the owner's name in the messages of two of his own website
  commits, be09e43 and f791ea8, and nothing else.

## Rejected alternatives

- **CSS columns** (`columns: 3`): fills down each column while focus runs
  across; its defeat case is the check's.
- **Grid rows spanned by script**: every gap rounds to the row unit, and
  fine units mean thousands of rows; the script places cards absolutely
  instead, reading the columns from the grid itself, exact to the pixel.
- **Bands as a CSS box around the image**: needs each card's ratio in a
  style attribute or attr(), which the policy refuses or browsers lack;
  bands drawn into the copy as transparent pixels need neither.
- **A tall limit near 2.0, below phones**: would band every phone snip,
  the hassle the owner's aim rules out.
- **srcset with two card widths**: fewer bytes on desktops, at the cost
  of a third copy per entry; 1,024 wide kept every card under 130 KB.

## Not done

- Nothing pushed. The chat checks the limits against the owner's aim
  before he merges.
- No issue form for a showcase entry; the seat's view is in Report 10.
- The "add-ons" Pinterest's look implies: reported, not built.
- Safari's own grid-lanes, the one shipped, not run; Chrome's flagged one
  stands in.
- Test 1 once more, on or after 2026-11-02.

---

# Round 11, 2026-10-22 UTC: his answers, the forms and add-ons, documents a person and an AI can both follow, the README's prompt

Model: Claude Opus 5.5 (claude-opus-5-5), in Claude Code, the same session
continued. HEAD at start: aaa6757, the website merge of pull request 14,
whose tree is d9e0e6a's (compared here); Scope and Checks success on the
pull request, Checks and Deploy success on main, Template cleanup skipped
(GitHub's API). The owner had ticked Brief 10 and Report 10. Work on the
branch guides-and-prompt. HEAD at end: the commit that adds this
section. Mode: mutating.

## What was asked

The portfolio architecture chat's Brief 11, of 2026-10-21, stored word for
word in place of Brief 10, read first for what it still says (the owner's
aim for the showcase, carried). His answers to Report 10: the limits of
2.4 accepted; his name in his own commit messages fine, to be recorded and
allowed by the pre-publish search, with a defeat for another account's;
a Showcase entry issue form; the light add-ons; briefs off the cleanup's
list. Part 1: audit how a person and an AI arriving cold enter and
navigate the documents for each purpose, research the conventions for
agent instructions from first-party sources, build the clear
improvements, propose any new file or convention, and say what a copy's
owner and their AI start from. Part 2: a self-contained, comprehensive
prompt for an AI in the README, which asks the person what they want to
do and guides them, kept accurate by a check in ci.py and the gates,
safe, easy to copy; a better README with pictures that stay current; a
view on a copy's own prompt.

## Errors this seat made

1. **docs/decisions/README.md said his name appears "only in LICENSE and
   README.md"** since his showcase entry made it untrue (Round 8).
   Corrected.
2. **A first version of the search's allowance would have let the seat's
   own commits name him**, since they carry his no-reply address under
   the handle. Caught reading it, before any run; his own commits are
   now those under his profile's name, and a defeat case covers the
   seat's identity.
3. **Gate C refused a commit once**: MAP.md had been regenerated before the
   new record was staged, and the map is made from staged files.
4. **A defeat case looked for text across a line break**, and was fixed in
   the case.
5. **The first README floated the showcase picture beside its paragraph**,
   which at 390 px squeezed the text to a few words a line; seen in the
   rendered look before any commit, and unfloated.

## Research

First-party sources on instructions for AI agents, read 2026-10-21 and
22; only two pages carry a date. agents.md: AGENTS.md is "a simple, open
format for guiding coding agents", stewarded by the Agentic AI Foundation
under the Linux Foundation, read by Codex, Jules, Cursor, Gemini CLI,
GitHub Copilot's coding agent and others; the nearest file wins. OpenAI's
Codex documentation: reads AGENTS.md from the project root down, one per
folder, AGENTS.override.md first, 32 KiB combined by default. Cursor's
documentation: supports AGENTS.md at the root and in subfolders. GitHub's
Copilot support table: AGENTS.md, CLAUDE.md or GEMINI.md read by the cloud
agent, code review, VS Code chat (AGENTS.md only) and the CLI. Claude
Code's documentation: reads CLAUDE.md, or AGENTS.md when there is none;
with both, only CLAUDE.md. Gemini CLI's (updated 2026-06-18): GEMINI.md
by default, AGENTS.md if configured. llmstxt.org (2024-09-03, modified
2026-08-10): a proposal for websites. Repository settings, from GitHub's
API: issues on, Discussions off, labels without "showcase".

## What was built

- **Forms** (b77f3e0): Showcase entry (removal, impersonation, an entry
  gone bad) and Question; the how-to names the form.
- **Add-ons** (2b641d4): showcase cards without border or panel, the
  picture's corners rounded on the card colour with a hairline edge.
- **His answers** (495a2ba): no briefs in remove.txt or the user guide;
  ADR-0002, Changes, and CLAUDE.md: his own commit messages may name him.
  The pre-publish search, a scratch tool, allows exactly that.
- **The README and its prompt** (3fed37d): "What do you want to do?",
  nine rows; pictures by their live addresses (both design previews and
  the owner's showcase card); "Ask an AI assistant to guide you", a closed
  details section holding the prompt, about 220 lines: how to behave,
  what the project is, how it is organised, seven paths (A to G) each
  with steps, rules, checks and review, and a maintainer-only note.
  tools/check_prompt.py, in ci.py checks and gate B, holds its 24 paths,
  23 facts, 7 commands and 5 safety rules to their sources; on the
  cleanup's list. CLAUDE.md opens by sending any other AI to the README.
  ADR-0017; ADR-0015, Changes; standing-checks.md; commands.md;
  docs/decisions/README.md.

## Proofs

All on 2026-10-22, one browser job at a time, Chrome 156, on a fresh
clone of 3fed37d unless named.

- **Every check with axe**, `tools/ci.py checks --axe`: exit 0 in 665 s,
  the prompt check among them; the browser checks 638 s (tree 48 runs,
  keyboard 8, joins 4, anchors 136, words 4, motion 3, packing 12, axe 36),
  0 failures, the borderless cards included, light and dark, 390 and
  1366 px.
- **The deploy's own path** with the 13 real snips under a Mac's file
  names, the owner's entry beside them: 30 pictures gathered and
  assembled, check_built --previews 0 problems; every browser check with
  axe on the assembled gallery, 0 failures in 629 s.
- **Every defeat case with the browser and axe**: exit 0 in 1,627 s; 129
  defeat cases (112 file, 17 browser) fail as built, naming what failed;
  12 controls and 21 planted controls pass. New: the prompt naming a path
  that does not exist; the cap stated as 25 MB; SHOWCASE_TALL changed to
  3.0 in build.py; the scope marker changed in scope_check.py; an issue
  form the prompt does not name; a command in no guide; a safety rule taken
  out; a fact reworded out of the check's sight. Control: the prompt check
  on the unchanged copy.
- **The gates**, on a scratch clone of 3fed37d: 24 defeat cases refused,
  the README's prompt naming a missing path among them (gate B, naming
  check_prompt.py); 5 controls passed.
- **The cleanup**, on the fresh clone, which has no briefs folder: guards
  hold, 60 files removed, a later run changes nothing, the cleaned copy
  builds and checks, its 5 links resolve.
- **The pre-publish search's new allowance**, in a scratch clone: the
  owner's name in a commit message by another account, found; under the
  seat's identity, the handle with his no-reply address, found; written as
  his website commits are, passes.
- **The README as rendered**: GitHub's Markdown API, in a README's mode,
  rendered the draft; headless Chrome showed it with GitHub's styles at
  1012 and 390 px, light and dark: the table, the closed section, the
  prompt as a text block, the three pictures loaded through GitHub's image
  proxy (200, WebP). The owner reads it on the branch, where GitHub adds
  the copy button.
- **The issue forms** parse as YAML with the fields GitHub's form schema
  expects (PyYAML in a scratch folder, not the project).

## Rejected alternatives

- **AGENTS.md now**: proposed, not added (Brief 11: propose any new
  convention). Claude Code would keep reading CLAUDE.md, so it reaches
  other agents only; a copy would need its own or the cleanup's removal.
- **A prompt in its own file**: an AI given the README would have to
  fetch it, against "self contained".
- **llms.txt**: a proposal for websites.
- **Pictures committed to the repository**: they go stale; the live
  ones are rewritten by every deploy.
- **A gallery overview picture**: needs one more deploy capture and shows
  on a branch only after a merge; proposed.

## Not done

- Nothing pushed.
- AGENTS.md, a copy's own prompt, a gallery picture: proposals.
- Test 1 once more, on or after 2026-11-02.

# Round 12, 2026-10-23 UTC: AGENTS.md, a copy's own prompt, a picture of the gallery

Model: Claude Opus 5.5 (claude-opus-5-5), in Claude Code, the same session
continued. HEAD at start: 0ce2c71, the website merge of pull request 15,
whose tree is bc48b45's (eaae956, compared here); Scope and Checks success
on the pull request, Checks and Deploy success on main, Template cleanup
skipped (GitHub's API). The owner had ticked Brief 11 and Report 11. Work
on the branch agents-and-copy-prompt. HEAD at end: the commit that adds
this section. Mode: mutating.

## What was asked

The portfolio architecture chat's Brief 12, of 2026-10-23, stored word for
word in place of Brief 11, read first for what it still says (the owner's
aim for the showcase, carried). His answers to Report 11, 8.1: AGENTS.md
yes, a copy's own prompt yes, a picture of the gallery page yes; designs
of his own for the templates are for later. Part 1: AGENTS.md, a short
router for coding agents other than Claude Code, duplicating no rule; a
decision, with its reason, whether a copy loses it or receives its own;
whatever it names held to the repository by the prompt check or a
sibling, with a defeat case. Part 2: a short prompt for a site owner in
copy-README.md, with the same rules on secrets and acting, held to its
sources and tested here, the cleanup test showing a copy's README carrying
it. Part 3: a picture of the gallery page, captured by the deploy beside
the previews, in assemble's list, shown in the README by its live address;
say what it shows before the first deploy after the merge. Do not touch
showcase/: the owner's friend may add an entry meanwhile.

## Errors this seat made

1. **The tree check, which this seat wrote in Round 1, held a race**, and
   it failed the defeat harness's browser control once on 2026-10-23,
   on a page that was right. site.js starts the page, the strip's pause
   button among it, from an idle callback with a 1.5 s timeout; the check
   read the tree 1.5 s after load. On the first load in a newly started
   Chrome the start came later in 1 of 15 tries (2,273 ms), so the button
   was missing from one tree and not the other. Fixed in eb27870: the
   check counts the page's pending idle callbacks and reads the tree,
   with scripts on, once they have run. In 20 newly started Chromes the
   wait was needed once and the button was read every time; the tree's
   defeat case still fails. A CPU slowed six times did not reproduce it;
   a newly started Chrome did.
2. **The cleanup test's new step first looked for the copy prompt's
   commands in every Markdown file a copy keeps, its README among them,**
   which holds the prompt itself: that half could never fail. Caught
   reading it, before any run; the README is left out now, and a defeat
   case proves the step.
3. **One new defeat case expected the wrong text**: the check failed as
   it should, but printed its source through Python's quoting, which the
   expected text did not match, so the harness reported the case
   unproven. The message is plain now.
4. **CAPABILITIES.md counted 16 decision records "as of 2026-10-19"**
   through Round 11, which added ADR-0017. Re-measured: 17.
5. **The handoff's settled list still said his name appears "only in
   LICENSE and README.md"**, untrue since his showcase entry; corrected
   there (the handoff is not committed).

## Research and the copy's AGENTS.md

Claude Code's documentation, "How Claude remembers your project", read
again 2026-10-23: with an AGENTS.md and no CLAUDE.md, CLAUDE.local.md or
.claude/CLAUDE.md in the working directory or above it, Claude Code reads
the AGENTS.md (v2.1.277 or later, its default setting
`claude-md-or-agents-md`); with both, CLAUDE.md only. The other sources are
Round 11's (ADR-0017, A1 to A3). So here AGENTS.md reaches every coding
agent but Claude Code, which keeps reading CLAUDE.md; and a cleaned copy,
which has no CLAUDE.md, has its AGENTS.md read by Claude Code too.

Decided: **a copy receives its own AGENTS.md**, from
.github/template-cleanup/copy-AGENTS.md, put in place by the cleanup as
copy-README.md is. Why: a copy's owner is the person most likely to open a
coding agent in a clone, and AGENTS.md is the file those agents load
without being asked, Claude Code among them in a copy; the content trace
is the rule an agent breaks unknowingly (it changes site.json alone and the
build fails), and the copy's prompt is where it is explained. The
project's own AGENTS.md cannot stay in a copy: it routes to CLAUDE.md and
STATE.md, which the cleanup removes. Losing it would leave every agent in
a copy with nothing loaded.

Checked from GitHub on 2026-10-23, for Round 11's open items: GitHub's
page for main serves the README's prompt in a block carrying its copy
button's text, and the three pictures through its image proxy (200,
WebP). The issue chooser needs a sign-in, so the four forms there are the
owner's to see.

## What was built

- **A copy's own prompt** (08761a4): copy-README.md gains "Ask an AI
  assistant to help", a closed section holding a prompt of about 90
  lines for a site owner's AI: how to behave (the gallery prompt's rules
  on secrets and acting, less the security route), the files, A write or
  change the content with the CV trace, B choose a design, C publish, D
  read a failed build, and the optional local build. tools/check_prompt.py
  checks it against what a copy keeps: its 16 paths exist and none is on
  remove.txt; 7 facts (the settings, the trace's starting value, the
  Deploy and Checks workflows' names, Deploy's jobs, the step a failed
  build names, the Python version); its 4 commands in
  use-this-template.md; 4 safety rules. use-this-template.md gains "Build
  on your own computer, if you like", since a copy loses commands.md and
  had no local commands at all. check_template_cleanup.py builds the
  cleaned copy with `tools/ci.py build --mode site`, the prompt's own
  command, and shows its README carrying the prompt with every path in
  the copy and every command in a guide the copy keeps.
- **AGENTS.md and a copy's own** (248123c): the router at the root, and
  copy-AGENTS.md, which cleanup.py puts in place in a copy beside its
  README; tools/check_prompt.py holds both (the files each names, the
  sections each links under their headings' own words, the section
  holding the README's prompt); CLAUDE.md says rules live there, not in
  AGENTS.md; the user guide's manual cleanup puts both of a copy's own
  files in place.
- **The gallery page's picture** (b63f70d): tools/screenshots.py takes the
  gallery page's top, 1366 by 1280 CSS pixels at full size, after the
  previews and the showcase's copies, as preview.webp at the gallery's
  root; deploy.yml's shots job gathers it; assemble requires it and checks
  it as a preview, within 300 KB; check_built --previews requires it. The
  README leads with it by its live address; the two design previews move
  to "Make your own site". tools/check_prompt.py holds each README address
  on the live gallery to what the deploy publishes.
- **The tree check's race** (eb27870): see Errors, 1.
- ADR-0017 and ADR-0015, Changes; standing-checks.md; commands.md;
  CAPABILITIES.md, whose count of decision records had stood at 16 since
  2026-10-19 and is 17.

## What the gallery's picture shows before the first deploy

Measured 2026-10-23: through GitHub's image proxy, its address answers
404 with "Cache-Control: no-cache, no-store", so nothing holds the
failure; on the branch, and on main until the first deploy after the
merge ends, the README shows a broken picture with its alt text. GitHub
Pages serves pictures with max-age=600, so after that deploy the README
shows it on its next load, at most about ten minutes old thereafter.

## Proofs

All on 2026-10-23, one browser job at a time, Chrome 156, on fresh clones
of the branch: b63f70d for the gates, the cleanup and the deploy's path,
and eb27870, after the tree check's fix, for every check and every
defeat case.

- **Every check with axe**, `tools/ci.py checks --axe`, on eb27870: exit 0
  in 1,033 s; the browser checks 967 s (tree 48 runs, keyboard 8, joins
  4, anchors 136, words 4, motion 3, packing 12, axe 36), 0 failures,
  light and dark, 390 and 1366 px. On b63f70d before the fix: exit 0 in
  661 s, the browser checks 631 s, 0 failures. The tree check alone, the old code and the new alternately on one gallery: 200 and 190 s before the fix, 200 and 187 s after, so the wait costs nothing measurable; the slower runs were the machine's, as the defeat cases, most of which the change does not touch, took 2,808 s against 1,813 s that morning. The prompt check
  passes on all four documents and the README's 8 addresses on the live
  gallery; 5 pictures made and checked, the gallery's own 89,268 bytes.
- **Every defeat case with the browser and axe**, on eb27870: exit 0 in
  2,808 s; 151 defeat cases (133 file, 18 browser) fail as built, naming
  what failed; 12 controls and 21 planted controls pass; 0 unproven. 22
  are new: 11 for a copy's prompt, 6 for AGENTS.md and a copy's, 5 for
  the gallery's picture. On b63f70d the browser control failed once, the
  race in Errors, 1; every case then behaved as built.
- **The gates**, on a scratch clone of b63f70d: 26 defeat cases refused,
  AGENTS.md naming a file that does not exist and a copy's prompt naming
  a file no copy receives among them (gate B, naming check_prompt.py); 5
  controls passed; exit 0 in 385 s.
- **The cleanup**, on the fresh clone: guards hold, 61 files removed,
  README.md and AGENTS.md the copy's own, a later run changes nothing, the
  cleaned copy builds and checks (its site by `tools/ci.py build --mode
  site`), its 9 links resolve, its README carries its prompt with 16 paths
  in the copy and 4 commands in its guides. A copy made by cleanup.py and
  kept to look at: its README opens "# My portfolio" with "## Ask an AI
  assistant to help" holding the prompt; its own AGENTS.md; no CLAUDE.md
  and no cleanup folder; `tools/ci.py build --mode site` in it, all
  passed.
- **The deploy's own path** with the 13 real snips beside the owner's
  entry: deploy.yml's gathering step, run as written, gathered 31
  pictures, the gallery's own among them (89,268 bytes); assemble and
  check_built --previews, 0 problems; every browser check with axe on the
  assembled gallery, 0 failures in 682 s.
- **The race and its fix**: on the first load in a newly started Chrome,
  the strip started 2,273 ms after load in 1 of 15 tries, its pause button
  missing at the 1.5 s read; a CPU slowed six times did not reproduce it.
  With the fix, in 20 newly started Chromes the wait was needed once (one
  idle callback pending at 1.5 s, 0.06 s more) and the button was read
  every time; the tree's defeat case still fails.
- **The README as rendered**: GitHub's Markdown API, in a README's mode,
  rendered README.md, the copy's README and both AGENTS.md files; headless
  Chrome showed them with GitHub's styles at 1012 and 390 px, light and
  dark, none scrolling sideways. The gallery's picture, broken on the
  branch as expected, and with its address pointed at the deploy's own
  capture, as after the merge: it leads the page, above the table. Both
  prompts render as text blocks in their closed sections; the anchors
  GitHub gives the headings equal the check's. GitHub's file view shows
  AGENTS.md's header as a small table, as it does CLAUDE.md's (read from
  main's CLAUDE.md page); the API shows it as text.

## Rejected alternatives

- **A copy losing AGENTS.md**: agents in a copy would load nothing, and
  the content trace is the rule they would break unknowingly.
- **The project's AGENTS.md kept in a copy**: it routes to CLAUDE.md and
  STATE.md, which the cleanup removes.
- **check_prompt.py kept in a copy, to check the copy's prompt there**:
  a copy's owner edits their README freely, and a check failing on their
  own words would be the hassle the owner's aim rules out; the prompt is
  checked here, before any copy receives it.
- **The gallery's first screen at 1366 by 900**: the heading fills it and
  the template cards are cut off; 1280 holds the first row whole.
- **A capture of the whole page**: it grows with every entry, and a
  section that skips its layout paints blank beyond the view.
- **Three pictures at the README's top**: they would push "What do you
  want to do?" far down; the design previews moved to "Make your own
  site", where a design is chosen.

## Not done

- Nothing pushed.
- A real copy made from the template after the merge, to see its README
  and AGENTS.md on GitHub; the cleanup test stands in for it.
- Test 1 once more, on or after 2026-11-02.

# Round 13, 2026-10-23 UTC: a copy's first run with Pages off, and the showcase's overlay

Model: Claude Opus 5.5 (claude-opus-5-5), in Claude Code, the same session
continued. HEAD at start: 4e771b7, the website merge of pull request 16,
whose tree is 573bbde's (1b783b9, compared here); Scope and Checks success
on the pull request, Checks and Deploy success on main, Template cleanup
skipped (GitHub's API); the gallery's own picture live, 200, image/webp,
99,280 bytes from the runner's Chrome. The owner had ticked Brief 12 and
Report 12. Work on the branch copy-first-run-and-overlay. HEAD at end: the
commit that adds this section. Mode: mutating.

## What was asked

The portfolio architecture chat's Brief 13, of 2026-10-23, with its
Addendum 1, stored word for word in place of Brief 12, read first for what
it still says (the owner's aim for the showcase, his designs for the
templates decided for later, showcase/ left to contributors). Brief 13:
in a real copy the owner made, the first Deploy failed red because GitHub
Pages is off until the copy's owner turns it on. Decided by him on the
chat's recommendation: the copy's README leads with turning Pages on, with
the exact clicks and how to run Deploy again; with Pages off, Deploy in a
copy does not fail but ends with a notice, in the run's summary and an
annotation, and publishes nothing; a real failure still fails; the
gallery's own Deploy unchanged, an off Pages failing loudly. The seat to
judge whether the cleanup should also open an issue. Confirm from the
source that configure-pages cannot turn Pages on with the run's own
token. Addendum 1: a showcase card's larger copy opens, with scripts on,
in an overlay that can be closed: a Close button, Escape, a click outside,
focus in and back; the browser's own dialog preferred; with scripts off,
the plain link.

## Errors this seat made

1. **The test server in tools/cdp.py, written by this seat in Round 1,
   served .webp with no media type on this machine.** Python's table
   comes from the machine, and this Windows has none for .webp, so in the
   browser checks a link to a picture downloaded it rather than opening
   it; pictures inside a page loaded anyway, by sniffing, so nothing
   showed until the overlay check's scripts-off half failed on a page
   that was right. Found by probing: the Live demo link navigated, the
   card's link to full.webp did not. Fixed in 42f5760: the server serves
   each type the built site uses as GitHub Pages does (the live full.webp
   is image/webp).
2. **A commit message counted sixteen defeat cases where there were
   eleven**; corrected by amending, before any push.
3. **The setup guide's new line first dated the fix of the skipped deploy
   job 2026-10-17, the local date**; the commit is 2026-10-16 21:16 UTC.
   Corrected before the commit.
4. **The first overlay defeat case, "no Close button", swapped the button
   for a span** that the size check would still have counted; caught by
   reading it, before any run.

## Checked from the source

- actions/configure-pages' action.yml at the pinned 45bfe01 (v6.0.0), read
  2026-10-23: `enablement` "requires a token other than `GITHUB_TOKEN`".
  Its src/api-client.js treats any failed lookup as Pages being off; it
  does not single out 404.
- GitHub's REST documentation, "Get a GitHub Pages site", read 2026-10-23:
  200 or 404; `build_type` "legacy" (built from a branch) or "workflow".
  GitHub's permissions table for GitHub Apps, read the same day: GET
  /repos/{owner}/{repo}/pages needs Pages: read, for installation access
  tokens, which a workflow's own token is.
- A README's callout: GitHub's Markdown API renders `> [!IMPORTANT]` as a
  callout in its gfm mode only; GitHub's repository page renders one as
  the coloured box (cli/cli's README, read 2026-10-23,
  `markdown-alert-important`).

## What was built

- **A copy's first run** (e459014): Deploy gains a job, pages, Pages: read,
  which runs `tools/ci.py pages`: it asks GitHub's API whether Pages is on.
  pages_verdict decides: publishing from GitHub Actions, publish; a 404 in
  a copy, a notice titled "Turn on GitHub Pages to publish your site", as
  an annotation and in the run's summary with the three steps, and
  on=false, so deploy is skipped and the run ends green; a 404 in the
  gallery, a branch source, or any other answer, a failure. The build and
  checks never wait on it. tools/check_workflows.py holds the wiring (the
  publishing job needs pages and runs only when it says on; no other job
  reads it; no continue-on-error) and pages_verdict's table. The copy's
  README opens with an IMPORTANT callout: the setting, the notice's title,
  Actions, Deploy, Run workflow, or any commit. tools/check_prompt.py holds
  that lead and both prompts' new lines to ci.py and deploy.yml. The user
  guide, the README's walk-through and the setup guide's first push, step
  8 and Test 4 say what a first run now shows. ADR-0015 and ADR-0004,
  Changes.
- **No issue in the copy**: the seat's judgment, in ADR-0015's row. The
  README GitHub shows on the copy's front page leads with the setting, and
  every Deploy run until then ends with the notice; an issue would be a
  third copy of one instruction, an artifact the owner must close, and
  issues: write for a job that otherwise writes only its own files.
- **The showcase's overlay** (42f5760): the gallery's own `<dialog>`,
  shown with showModal(), chosen over a hand-built overlay because the
  browser then makes the page behind inert, keeps focus inside and closes
  it on Escape by itself. gallery.js, with scripts on, opens it on a click
  or Enter on a card's picture: the picture made in the page with its size
  from the build (build.py passes full_size), the entry's name above it, a
  Close button, an X named "Close", which takes focus; the button, Escape
  and a click outside the picture close it, and focus returns to the
  card's link. gallery.css shows the picture whole within the window, at
  its own size or smaller, on the page's colours in either theme, with no
  motion. With scripts off the card is the plain link it was.
  tools/check_browser.py's overlay check, and tools/cdp.py's test server
  serving .webp as image/webp (Errors). ADR-0016, Changes.

## Proofs

All on 2026-10-23, one browser job at a time, Chrome 156, on a fresh
clone of 42f5760 unless named.

- **Every check with axe**, `tools/ci.py checks --axe`: exit 0 in 678 s;
  the browser checks 648 s (tree 48 runs, keyboard 8, joins 4, anchors
  136, words 4, motion 3, packing 12, overlay 4, axe 36), 0 failures,
  light and dark. The prompt check passes on all four documents, the copy
  README's lead (5 facts) and the README's 8 addresses on the live
  gallery; 5 pictures made and checked. The first try, at 18:22Z, lost
  Chrome's DevTools connection at the browser checks' first load
  (ConnectionResetError), after every file check, build and picture had
  passed; the defeat harness, started a minute later, ran its own Chrome
  without fault, and the retry above passed on the same clone.
- **Every defeat case with the browser and axe**: exit 0 in 1,914 s; 167
  defeat cases fail as built, naming what failed; 12 controls and 23
  planted controls pass; 0 unproven. 16 are new: 5 workflow cases (a
  copy's Deploy failing red with Pages off; the gallery's quiet with
  Pages off; the build waiting on pages; continue-on-error on the build;
  deploy publishing whatever Pages says), 3 for the pages step against a
  fake GitHub API (the gallery with Pages off; a branch source; the API
  answering 500), 3 for the copy's README and prompts (the notice's title
  changed in ci.py; the README not leading with the callout; Run workflow
  named while Deploy cannot be started by hand), and 5 for the overlay
  (no Close button; focus not returned; the dialog open with scripts off;
  the picture cropped to a square; the dialog shown without showModal).
  2 new planted controls: a copy with Pages off ends with the notice,
  the summary and on=false, exit 0; the gallery with Pages on publishes.
- **The gates**, on a scratch clone of 42f5760: 27 defeat cases refused,
  a copy's Deploy failing red with Pages off among them (gate B, naming
  check_workflows.py); 5 controls passed; exit 0 in 417 s.
- **The cleanup**: guards hold, 61 files removed, README.md and AGENTS.md
  the copy's own, a later run changes nothing, the cleaned copy builds and
  checks, its 9 links resolve, its README carries its prompt. A copy made
  by cleanup.py and kept to look at: its README opens with the callout,
  "First, once: turn on GitHub Pages"; its own workflow check passes its
  five workflows, the Pages rules among them; `tools/ci.py build --mode
  site` in it, all passed.
- **The deploy's own path** with the 13 real snips beside the owner's
  entry: deploy.yml's gathering step gathered 31 pictures; assemble and
  check_built --previews, 0 problems; every browser check with axe on the
  assembled gallery, 0 failures in 657 s, overlay 4 runs.
- **The tree at load**, the gallery page's whole accessibility tree, main's
  build against the branch's, at 390 and 1366 px, light and dark, scripts
  on and off: the same in all 8 cells (36 text entries, 26 named nodes).
- **The overlay, looked at**: opened by Enter on the first card in light
  and dark, at 390 and 1366 px: a modal, focus on Close, the picture
  358 by 569 and 511 by 812, both the 0.629 of its 1077 by 1713, within
  the window; Escape closed it, focus back on the card.
- **The pages step's output**, against a fake API answering 404 in a copy:
  exit 0; the annotation "::notice title=Turn on GitHub Pages to publish
  your site::" with the setting and Run workflow; on=false; the summary
  headed the same, with the three steps.
- **The READMEs as rendered**: GitHub's Markdown API rendered both; in its
  gfm mode the copy's README opens with the Important callout, which
  GitHub's repository page renders likewise (cli/cli's, read the same
  day); headless Chrome showed both with GitHub's styles at 1012 and 390
  px, light and dark, none scrolling sideways.

## Rejected alternatives

- **configure-pages' enablement**: needs a token other than the run's own;
  asking each copy's owner for one is worse than one setting.
- **configure-pages with continue-on-error**: it fails alike for Pages off
  and for any other fault, so it cannot tell a notice from a failure, and
  continue-on-error would end a failed run green.
- **The pages job before build, or the build waiting on it**: with Pages
  off a broken build would never run, and the run would end green; the
  workflow check now refuses that.
- **An issue in the copy**: see What was built.
- **A hand-built overlay**: the inert page, the focus held inside and
  Escape would all be the seat's to write and to get right; the browser's
  dialog gives them.
- **The overlay's picture in the page's HTML**: an `<img>` without a
  source is not valid HTML; the script makes it when the overlay opens.

## Not done

- Nothing pushed.
- The real copy, made by the owner after the merge, its first Deploy
  ending with the notice and no red, then Pages turned on and Deploy
  publishing; the chat reads it through the API before he deletes it.
- Test 1 once more, on or after 2026-11-02.

# Round 14, 2026-10-24 UTC: five designs of the owner's, and Plain raised to the same standard

Model: Claude Opus 5.5 (claude-opus-5-5), in Claude Code, the same session
continued. HEAD at start: 040b028, the website merge of pull request 19;
pull requests 17, 18 and 19 merged on 2026-10-23 (85f9244, d99b909,
040b028), each merge's tree its head's, or its head's with pull request
18's one file, and Checks and Deploy success on all three on main, read
from GitHub's API this round; the owner's showcase card live with its new
line. The two merges on top of the branch's base are the owner's, made on
GitHub's website. Work on the branch more-designs. HEAD at end: the commit
that adds this section. Mode: mutating.

## What was asked

The portfolio architecture chat's Brief 14, of 2026-10-24, stored word for
word in place of Brief 13 (executed, ticked), read first for what it still
says: the owner's aim for the showcase, carried since Brief 9. A gallery
with two designs does not read as a gallery: five designs of his own, in
Templates, built fast on the rules the project has, without a proposal
round; he judges them once from screenshots before he merges and may drop
any. His trade-off, in his words: "decrease quality by 10% in exchange for
50% speed", but no cut that a check needs. His two additions of
2026-10-24: a quality floor (of Plain: "very plain and the sites should not
be like that"; simple allowed, unfinished not), and real difference: "all
5 should differ from each other by at least 40-50%", made checkable by the
chat as five dimensions (layout and structure; type; colour palette;
shapes and ornament; density and rhythm), any two of the seven designs
differing in at least three, always in layout or palette. Plain: its
author becomes Waqas01CP (his decision: every design he commissions is
credited to him), recorded, with check_built's credit rule, its defeat
cases and the prompt's checked facts updated; its purpose kept (high
contrast, system fonts, no motion, one column, a printout of every word)
and its look raised to the floor; still maintained. Each new design within
the contract and through every check a contributor's design must pass.
Screenshots at 1366 and 390 px for him, with Plain before and after, and
the difference table; how to drop a design. Proof on a fresh clone: every
check, every defeat case, the gates, the pre-publish search, the gallery
with all seven looked at.

## Errors this seat made

1. **Bento's first screen grid also styled the strip under it.** The rule
   `.intro .wrap` matched the strip's paragraph, which carries the class
   wrap too, so the strip took the hero tile's grid and background. Seen
   in the first whole-page screenshot; fixed before any commit with
   `.intro > .wrap`.
2. **Three designs coloured the headline's separators in their rule
   colour**, a colour meant never to be text: Plain #BDBDBD on white
   (1.9:1), Broadsheet #A79F8E on newsprint (2.3:1), Console #3F6B3A on
   black (3.1:1). Caught by reading the screenshots before axe ran, fixed
   before any commit; axe then passed all seven.
3. **Console's marks ran into the next word**: `"\25B8 "` in CSS ends the
   escape with its space, so the mark and the title touched. Seen in a
   screenshot; fixed with a second space before any commit.
4. **The first file proofs left six controls unproven**: tools/prove_checks.py
   planted previews for Default and Plain by name, so a gallery of seven
   lacked five. Fixed in 5fdccd9: it plants one for every design a gallery
   builds.
5. **Poster set its In depth heading in forced capitals, and the keyboard
   check failed it** on the full checks of a fresh clone of 4521c00, at
   360 and 1366 px: "depth-tide-tracker's text did not enter the tree".
   It had, in capitals: Chrome gives a heading's name in the case CSS
   shows, and the check finds the panel by its heading's own text. Every
   other check, axe included, and every other design had passed. The
   seat's quick runs before the commit (axe, words, joins) had not
   included the keyboard check. Fixed in e669723: the heading keeps its
   own case; the keyboard check then passed on all seven, 28 runs. The
   run was stopped, with the defeat harness it had started, and run
   again on a fresh clone of e669723.
6. **Poster scrolled sideways on a phone**, by 34 px at 360 px and 4 px at
   390 px: its longest section title, Certifications, in Anton at its
   52 px minimum, was wider than the space beside its sticker. The seat's
   first width reading, in the screenshot script, measured each page at
   load, while the sections below the first screen still skipped their
   layout, so it saw nothing; and no standing check measures a page's
   width. Found while checking the report's own claim, with every section
   laid out; fixed in 20bf01c (the title sizes with the screen, from 38
   px, and a longer word wraps). After it, no page scrolls sideways at
   320, 360, 390 or 1366 px, light or dark. A standing check for it is
   recommended to the chat, not added: it would raise the bar for
   contributors' designs too.

## What was built

- **Plain, raised** (5fdccd9): the same purpose and the same one column;
  its look now from type and spacing alone: a name in heavy weight at up
  to 80 px, small-capital labels, a 4 px rule over each section, hairlines
  between entries in place of a 2 px box around everything, figures in
  monospace, an 8 px rhythm, buttons square and solid. Black on white, or
  white on black; its print styles kept. Author Waqas01CP, author_url his
  profile. check_built.py refuses a footer credit whose author link is the
  project's own address, with a defeat case planting Plain's old credit.
- **Five designs** (f969f48), each credited to Waqas01CP, CSS only:
  Bento, Broadsheet, Console, Poster and Signal (the table below). Bento
  carries Nunito (variable, 39,128 bytes) and Poster Anton (18,612 bytes),
  each from Fontsource 5.2.7 on npm, the latin subset, under the OFL with
  Google Fonts' text; neither reserves a name, by the licence text and by
  each WOFF2's name table, read with Node's Brotli. The other three use
  the system's faces. Only Signal offers dark, with a switch; Console has
  one theme, dark, setting color-scheme: dark on its own root.
- **Maintained**: all seven in tools/scope_check.py's MAINTAINED, so a
  contributor's change to one is refused and proposed in an issue; the
  seat's call, which the brief left open. ADR-0013, Changes, 2026-10-24,
  records the credit, the maintaining and the two bars.
- **One theme may be dark**: the design contract, the design guide,
  check_design.py's message, the template's comment and CAPABILITIES now
  say that a design without dark has one theme, the same on every device,
  which may be dark. The engine is unchanged: the page still declares
  light and carries no switch; ADR-0006's decision is unchanged.
- **The README** points to the gallery for the designs beyond its two
  pictures, without a count, so dropping a design leaves it true; the
  setup guide's step 8 expects a card per design. No checked fact in
  either prompt named Plain's author or needed a change: both say "such
  as designs/default/ and designs/plain/".
- **Poster's In depth heading** (e669723) keeps its own case (Errors, 5),
  and its section titles size with the screen (20bf01c; Errors, 6).
- **The browser proofs** (4521c00) keep Default and Plain in each case's
  copy, the designs they were written against, so a run stays as long as
  with two; the browser control and the standing checks run all seven.

## The seven designs on five dimensions

The seat's description of each, from the stylesheets and the screenshots;
a judgment, not a measurement.

| Design | Layout and structure | Type | Palette | Shapes and ornament | Density and rhythm |
|---|---|---|---|---|---|
| Default | A dark full first screen with the 3D knot; card grids two or three across; the timeline drawn to scale on a wide screen | Manrope, Instrument Serif italic, JetBrains Mono; large display sizes | Dark navy and lime; light or dark by the device | Rounded cards, glows, the knot, tilting cards, a moving strip | Spacious |
| Plain | One narrow column at every width; the menu a row of links | The system's sans-serif and monospace; a fixed scale; small-capital labels | Black on white, or white on black; blue links | Square; a heavy rule over each section, hairlines between entries | Compact and even, an 8 px rhythm |
| Broadsheet | A centred nameplate; text in ruled columns, two across; the degree boxed as a notice | The system's serifs (Georgia, Charter), bold and italic; narrow sans small capitals; a drop cap | Warm newsprint, ink black, a deep ink blue; light only | Hairline, double and heavy rules, double-ruled boxes, middots; no rounding | Dense: small type, tight leading |
| Console | A side pane menu beside the content on a wide screen; the timeline as log lines | The system's monospace throughout, few sizes | Near-black with phosphor green, amber and cyan; always dark | Dashed boxes with labels set into the line, bracket and prompt marks, a block cursor, a status bar | Compact |
| Signal | A red first screen; each section's title and huge number held in a left column while its entries run on the right | The system's grotesque (Helvetica, Arial) bold, from a 200 px name to 12 px spaced capitals | White, black and a signal-red field; dark offered | Heavy 6 px rules and huge numerals; square; nothing else | Airy, wide white space |
| Bento | Rounded tiles on a tinted ground: a mosaic first screen; sections as tiles, two to a row on a wide screen | Nunito, a rounded sans-serif, at heavy weights | Lilac ground, white tiles, peach, mint, sky and butter, a violet accent; light only | Large radii, soft shadows, pills, round badges holding the engine's icons | Medium, generously padded |
| Poster | Full-width colour bands, one per section; cards two across inside them | Anton, tall and condensed, in capitals at up to 232 px; the system's sans-serif for text; monospace labels | Saturated yellow, cobalt, hot pink and black on cream; light only | Thick black outlines, hard offset shadows, rotated stickers, a dot screen | Chunky: big type, heavy blocks |

Dimensions in which each pair differs (L layout, T type, P palette, S
shapes, D density), counted strictly: where two are close, they count as
the same.

| Pair | Differ in | Count |
|---|---|---|
| Default, Plain | L T P S D | 5 |
| Default, Broadsheet | L T P S D | 5 |
| Default, Console | L T S D (both dark with a green accent: P the same) | 4 |
| Default, Signal | L P S (both grotesque, both roomy) | 3 |
| Default, Bento | L T P (both rounded, both roomy) | 3 |
| Default, Poster | L T P S | 4 |
| Plain, Broadsheet | L T P (both ruled, both close-set) | 3 |
| Plain, Console | L T P S | 4 |
| Plain, Signal | L P D (both system sans, both ruled) | 3 |
| Plain, Bento | L T P S D | 5 |
| Plain, Poster | L T P S D | 5 |
| Broadsheet, Console | L T P S | 4 |
| Broadsheet, Signal | L T P D | 4 |
| Broadsheet, Bento | L T P S D | 5 |
| Broadsheet, Poster | L T P S D | 5 |
| Console, Signal | L T P S D | 5 |
| Console, Bento | L T P S D | 5 |
| Console, Poster | L T P S D | 5 |
| Signal, Bento | L T P S | 4 |
| Signal, Poster | L T P S D | 5 |
| Bento, Poster | L T P S D | 5 |

All 21 pairs differ in at least three; every pair differs in layout, and
all but one (Default and Console) in palette too.

## Proofs

All on 2026-10-24, one browser job at a time, Chrome 156, on a fresh
clone of e669723 unless named.

- **Every check with axe on a fresh clone of 20bf01c**, Poster's title
  fix, the branch's last code commit: exit 0 in 2,255 s, the browser
  checks 2,205 s, the same runs as below, 0 failures. The first try, from
  13:14Z, lasted 27,482 s and lost Chrome's DevTools connection in the
  browser checks ("the browser closed the connection"), after every file
  check, build and picture had passed; the machine had most likely slept.
  The retry, on the same clone from 20:54Z, passed. On that clone's
  gallery, the seat's width measurement with every section laid out: no
  page scrolls sideways at 320, 360, 390 or 1366 px, light or dark, 8
  pages. The defeat harness and the gates were not repeated for 20bf01c,
  which changes Poster's stylesheet alone; no defeat case touches Poster.

- **Every check with axe**, `tools/ci.py checks --axe`: exit 0 in 2,042 s;
  the browser checks 1,997 s (tree 168 runs, keyboard 28, joins 14,
  anchors 476, words 14, motion 8, packing 12, overlay 4, axe 96), 0
  failures, at 360 and 1366 px, light, device dark and switched dark. The
  design check passes all seven; two builds of the site (14 files) and of
  the gallery (33 files) byte-identical; check_built 0 problems on both;
  the content trace passes; 10 pictures made and checked, a preview for
  each design among them; the prompt check passes on all four documents,
  the README's 8 live addresses among it; the cleanup removes 61 files. On
  a fresh clone of 4521c00 the same run failed the keyboard check on
  Poster alone (Errors, 5), everything else passing: tree, joins, anchors,
  words, motion, packing, overlay and axe, all seven designs.
- **Every defeat case with the browser and axe**: exit 0 in 2,977 s; 168
  defeat cases (145 file, 23 browser) fail as built, naming what failed;
  12 controls, the browser and axe controls over all seven designs among
  them, and 23 planted controls pass; 0 unproven. New: the credit naming
  the project as the design's author.
- **The gates**, on a scratch clone of 4521c00: 27 defeat cases refused, 5
  controls passed, exit 0 in 452 s. e669723 changes Poster's stylesheet
  alone and passed gates A, B and C on its commit.
- **The pre-publish search**, every ref, pull request refs 1 to 19
  fetched: PASS; 497 blobs at 491 paths across 78 commits, 78 commit
  headers, 57 built files; the name only at LICENSE:3, README.md:344 and
  showcase/waqas01cp/entry.json:1, and in his own website commit
  messages, allowed; the contact address only at CODE_OF_CONDUCT.md:45.
- **Before committing**, on a gallery built in the working tree: axe,
  words and joins over all seven, 0 failures in 522 s (axe 96 runs); the
  drop cap in Broadsheet passes words and joins. The file defeat cases:
  145 and 19 planted controls, 0 unproven.
- **The fonts**: Nunito's and Anton's licence texts carry no Reserved Font
  Name; each WOFF2's name table (Node's Brotli) holds its copyright line
  and the OFL address, nothing more.
- **Looked at**: every design, whole, at 1366 and 390 px, light, and dark
  for Default, Plain and Signal, and the gallery page with its seven cards
  and their previews, light and dark, from the fresh clone's gallery.
  Plain before (main's) and after, at both widths
  in both themes. 28 pictures kept for the owner in the gitignored briefs
  folder, with a page to see them at once.

## Cuts, for speed

Each a cut the owner's trade-off allows, none of anything a check needs.
What each saved is the seat's estimate, not a measurement.

- **Light only: Broadsheet, Bento, Poster; dark only: Console.** Only
  Signal offers both. Saved a second palette per design and its contrast
  tuning in two more themes, about a third of each design's colour work.
- **System fonts: Broadsheet, Console, Signal.** Saved sourcing, the
  licence text, the name-table read and the preload for each; the cost is
  Linux's faces in the previews the runner takes (STATE, Known
  unverified).
- **None of the engine's effects in the five** (the knot, tilting cards,
  the moving strip, the scroll drift): nothing to tune for motion or to
  stop under reduced motion.
- **The timeline as a list in all five**, not drawn to scale as Default's
  is: Default's to-scale timeline is the engine's most intricate layout.
- **The menu as a row of links at every width**, not the engine's phone
  bar, which is a disclosure menu needing its own styling in each design.
- **No print styles in the five**; Plain keeps its printout.
- **No images**: the dot screen, the hero tile's colour and the terminal's
  dots are CSS gradients.

## Rejected alternatives

- **Console offering light too**: the engine's light theme is what a light
  device shows by default, so the gallery's preview, taken light, would
  not show the design; a Dark switch on a page already dark would do
  nothing.
- **Web fonts in every design**: each needs its source, licence text, a
  name-table read and a preload; the system's serif, grotesque and
  monospace faces carry Broadsheet, Signal and Console.
- **A count of designs in the README**: it would go stale when one is
  dropped or added.
- **The browser defeat cases over all seven designs**: each builds a
  gallery and runs a check over every design in it, so seven would make
  the harness about three times as long (inferred from the two-design
  run) for no more proof of the check failing.

## Not done

- Nothing pushed.
- The owner's judgment of the five, from the screenshots; he may drop any.
- The previews on the live gallery, taken by the deploy after the merge.
- A standing check that no page scrolls sideways: recommended to the
  chat (Errors, 6), not built, since it would bind contributors too.
- Test 1 once more, on or after 2026-11-02.

# Round 15, 2026-10-24 to 25 UTC: five designs for five professions, each with its own sample person

Model: Claude Opus 5.5 (claude-opus-5-5), in Claude Code, the same session
continued. HEAD at start: 3ec3c74, the end of Round 14 on the branch
more-designs, not pushed. Work on the branch profession-designs, cut from
it, so that it holds Round 14's commits until those merge. HEAD at end:
the commit that adds this section. Mode: mutating. No brief: the owner's
instruction in this conversation, which ranks first (CLAUDE.md).

## What was asked

The owner, on 2026-10-24 UTC (2026-10-25 in his local time), after
judging Round 14's screenshots: he approves those five and will push
them, though he may take them down later; rather than asking for changes
to them, new designs, "like 5 more or maybe 3 more", because "most of the
sites looks like a look-alike which i do not want as all sites should be
distinct and for the people of profession". Within the technical world:
"a portfolio for a cybersecurity professional, AI, or mobile deleveloper,
SE or QA engineer or ML and so on". His principles kept: responsive, on
a phone, a desktop and a desktop in portrait orientation; "you should not
take my taste as i require variety". He asked the seat to state back its
understanding and ask what it needed. The seat stated it back and named
the limit: every demo showed the same sample person, so a design for a
profession would still show a junior software engineer's page. Asked two
questions; his answers: each new template is shown with its own sample
person of its profession (ADR-0018), and five designs, for
cybersecurity, AI and ML, mobile development, QA and DevOps.

## Errors this seat made

1. **The first commit of the engine change named samples/ in the README's
   prompt before any sample existed.** Gate B refused it (the prompt check:
   "it names samples/, which does not exist"); the line went in with the
   samples.
2. **A commit of the Checks time limit was refused by gate C** (MAP.md
   stale while the map generator's own change was unstaged), and the
   staged file then went into the designs commit, whose message did not
   say so; amended before any push, to 3f65c4f.
3. **Latent's held panel centred content taller than the window**, so the
   name was cut off at the top and could not be scrolled to. Seen in the
   first screenshot; the panel now starts at the top when it overflows.
4. **Pipeline's first header was dark navy with a green accent**, close to
   Default's dark first screen with lime; seen in the screenshots and
   made light, a status page's white header and green banner.
5. **Pocket**: its feature card set white text on a light orange
   gradient, about 2.3:1, fixed by eye before any check; its status pill
   was 3.8:1 and its first targets could not reach a 72 px margin under
   the app bar, both found by the browser checks on the five new designs;
   fixed (a darker green; every margin the bar's own 64 px).
6. **Sentinel scrolled sideways at 320 px**, by 16 px: the surname
   Placeholder in Chakra Petch capitals at the name's 42 px minimum. Found
   by the width measurement on the fresh clone; fixed in 1cb1d44 (the name
   sizes with the screen from 32 px, and a longer one wraps).

## What was built

- **A template shown with its own sample person** (ceae4f1; ADR-0018):
  samples/<design>/ holds config.json, cv.md, site.json and items.json, a
  whole content folder naming that design. The gallery builds that
  design's demo from it, with its own layout.css beside the demo; every
  other demo, and every user's site, from content/, byte-identical to
  before when there is no sample. build.py refuses a sample for a design
  that does not exist, one naming another design, and one that is not a
  whole content folder; build.py and check_content.py take --content; ci.py
  checks builds each sample person's own site and traces it to their CV.
  Each gallery card names its person. A copy removes samples/. Four new
  proofs.
- **Five sample people** (3f65c4f), invented and obviously so, every link
  to example.com, each traced to their own CV with 0 untraced blocks:
  Morgan Placeholder, security analyst; Noor Sample, machine learning
  engineer; Jamie Demo, mobile developer; Casey Testcase, QA engineer;
  Taylor Sandbox, DevOps engineer.
- **Five designs** (3f65c4f), each credited to Waqas01CP, maintained, CSS
  only, one OFL font each from Fontsource 5.2.x with Google Fonts' licence
  text, none reserving a name by the text and the WOFF2 name table:
  Sentinel (security; Chakra Petch), Latent (machine learning; Space
  Grotesk), Pocket (mobile; Plus Jakarta Sans), Assert (QA; Public Sans),
  Pipeline (DevOps; Barlow Semi Condensed). Structure first: a clearance
  card and bracketed panels; a split screen with a held panel; the page as
  a phone app in a bezel; a test matrix of hairline cells; a status header
  over a pipeline's rail.
- **Sentinel's name sizes with the screen** (1cb1d44; Errors, 6).
- **Checks may run 90 minutes** (3f65c4f): twelve designs take near an
  hour; the checks are unchanged.
- The map leaves samples/ out, as content/; ADR-0013 records the five.

## The twelve designs, pairwise

The five new designs on the five dimensions (the seven before them are in
Round 14's table); the seat's judgment, not a measurement.

| Design | Layout and structure | Type | Palette | Shapes and ornament | Density and rhythm |
|---|---|---|---|---|---|
| Sentinel | A clearance card across the first screen; bracketed panels in a dashboard; the timeline an audit log | Chakra Petch, squared, in capitals; system sans text; monospace data | Graphite, signal orange, green and amber; always dark | Targeting brackets at panel corners, angled buttons, severity bars, a radar grid | Medium |
| Latent | A split screen: a dark panel held on the left at the window's height, the sections scrolling on a white sheet | Space Grotesk; monospace labels | A deep indigo field lit cyan and violet; a white sheet with indigo blue | Soft light in the field, metric bars, gently rounded cards | Airy |
| Pocket | The page as a phone app in a bezel, centred on a gradient; a sticky app bar of chips; widgets; grouped lists | Plus Jakarta Sans at heavy weights | Coral to pink to violet around an app's grey and white, blue controls | Large radii, app icons, chevrons, a bottom sheet's grabber, the bezel | Compact list rows |
| Assert | A test report: every section a table of hairline cells, the figures as passed checks | Public Sans; monospace capitals for column labels | White and cool grey, a navy menu, one pass green | Hairline cells, ticks in circles, square corners | Dense, tabular |
| Pipeline | A status header with a green banner, then the sections as numbered stages down a rail | Barlow Semi Condensed in capitals; system sans text | White and blue-grey, a green banner, blue, a navy footer | Rail and nodes, uptime bars, status lights | Medium |

How many of the five dimensions each pair differs in, counted strictly
(where two are close, the same):

| | Defa | Plai | Broa | Cons | Sign | Bent | Post | Sent | Late | Pock | Asse | Pipe |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Default | - | 5 | 5 | 4 | 3 | 3 | 4 | 5 | 3 | 5 | 5 | 5 |
| Plain | 5 | - | 3 | 4 | 3 | 5 | 5 | 5 | 5 | 5 | 3 | 4 |
| Broadsheet | 5 | 3 | - | 4 | 4 | 5 | 5 | 5 | 5 | 5 | 4 | 5 |
| Console | 4 | 4 | 4 | - | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 5 |
| Signal | 3 | 3 | 4 | 5 | - | 4 | 5 | 5 | 4 | 5 | 5 | 5 |
| Bento | 3 | 5 | 5 | 5 | 4 | - | 5 | 5 | 3 | 3 | 5 | 4 |
| Poster | 4 | 5 | 5 | 5 | 5 | 5 | - | 4 | 5 | 5 | 5 | 5 |
| Sentinel | 5 | 5 | 5 | 4 | 5 | 5 | 4 | - | 5 | 5 | 5 | 3 |
| Latent | 3 | 5 | 5 | 5 | 4 | 3 | 5 | 5 | - | 5 | 5 | 5 |
| Pocket | 5 | 5 | 5 | 5 | 5 | 3 | 5 | 5 | 5 | - | 5 | 5 |
| Assert | 5 | 3 | 4 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | - | 4 |
| Pipeline | 5 | 4 | 5 | 5 | 5 | 4 | 5 | 3 | 5 | 5 | 4 | - |

All 66 pairs differ in at least three; every pair in layout. The nine at
three: Default with Signal, Bento and Latent; Plain with Broadsheet,
Signal and Assert; Bento with Latent and Pocket; Sentinel with Pipeline.

## Proofs

On 2026-10-24 and 25 UTC, one browser job at a time, Chrome 156, on a
fresh clone of 3f65c4f unless named.

- **The gates**, on a scratch clone of 3f65c4f: 27 defeat cases refused, 5
  controls passed, exit 0 in 599 s (22:54Z on the 24th).
- **The first run of the checks did not count**: the machine hibernated
  during it; it lasted 32,050 s and lost Chrome's DevTools connection in
  the browser checks, after every file check, build, sample person's
  trace and picture had passed. The defeat harness that followed ran
  across the same sleep and was stopped, with all 18 of its processes,
  before it ended. Both ran again on the same clone, under a wrapper that
  asks Windows not to sleep for idleness while it runs.
- **Every check with axe** (the retry, from 10:33Z on the 25th): exit 0 in
  3,676 s; the browser checks 3,606 s (tree 288 runs, keyboard 48, joins
  24, anchors 816, words 24, motion 13, packing 12, overlay 4, axe 156),
  0 failures, all twelve designs. Two builds of the gallery, 58 files,
  byte-identical; each sample person's own site built, its files checked
  and traced to their own CV; 15 pictures made and checked; the cleanup
  removes 82 files, samples/ among them.
- **Every defeat case with the browser and axe**: exit 0 in 3,698 s; 171
  defeat cases (148 file, 23 browser) fail as built, naming what failed;
  12 controls, the browser and axe controls over all twelve designs among
  them, and 24 planted controls pass; 0 unproven. New: a sample for a
  design that does not exist; a sample naming another design; a sample
  person's fact not in their CV; and the control of a demo shown with its
  own sample person.
- **Width**, the seat's measurement with every section laid out, on that
  clone's gallery: no page scrolls sideways at 320, 360, 390, 1080 or 1366
  px, light or dark, but Sentinel at 320 px (Errors, 6). After 1cb1d44,
  on a gallery built in the working tree: no page at any of the five,
  and Sentinel's tree, keyboard, joins, anchors, words and axe checks, 0
  failures in 342 s. 1cb1d44 changes Sentinel's stylesheet alone and
  passed gates A, B and C on its commit.
- **The pre-publish search** at 3f65c4f, every ref, pull request refs 1 to
  19: PASS; 571 blobs, 83 commits, 87 built files.
- **Before committing**: every browser check with axe on a gallery of the
  five new demos, 0 failures but Pocket's two (Errors, 5) and the
  showcase pictures that gallery lacked by construction; after Pocket's
  fix, its anchors and axe 0 failures in 213 s. Each sample person traced
  before writing the next: about 190 blocks each, 0 untraced, every CV
  line on the page. The fonts: no Reserved Font Name in the licence texts
  or the WOFF2 name tables.
- **Looked at**: each new design whole at 1366, 390 and 1080 by 1920, and
  the gallery with its twelve cards; 18 pictures kept for the owner in the
  gitignored briefs folder, with a page to see them at once.

## Rejected alternatives

- **The same sample person for every design**: every demo would still
  read as a junior software engineer's page, the look-alike the owner
  named.
- **Sections of each profession's own**: a change to the engine's page and
  content model for every site; the owner chose the sample person alone.
- **Sample content inside the design folder**: a design is CSS, fonts and
  images (ADR-0006), and the scope check would let a contributor's design
  bring words; samples/ is the project's own, outside what a contributor's
  pull request may change.
- **Fewer checks to fit the 45-minute limit**: the limit grows instead.

## Not done

- Nothing pushed. more-designs (Round 14) and profession-designs (this
  round) both wait on the owner; profession-designs holds more-designs'
  commits, so its pull request shows only this round's once more-designs
  is merged.
- The owner's judgment of the five, from the screenshots.
- A standing check that no page scrolls sideways (Round 14), still for the
  chat and the owner.
- Test 1 once more, on or after 2026-11-02.

# Round 16, 2026-10-28 UTC: a status check after the merges; five more designs proposed

Model: Claude Opus 5.5 (claude-opus-5-5), in Claude Code, the same session
continued. HEAD at start: fdfdf6a on profession-designs; the local main
fast-forwarded to origin's 56077aa; work on the branch
records-after-merges, cut from it. HEAD at end: the commit that adds this
section. Mode: mutating, records only. No brief: the owner's instructions
in this conversation.

## What was asked

- 2026-10-25 UTC, on Round 15's report that the Checks limit rose from 45
  to 90 minutes: "it should not be the case, since the prior designs were
  not touched then they should not be checked again and only under the
  case when something in those design changes." To be remembered, not
  built. Both merges, he said, were done.
- 2026-10-28 UTC: run a check, since things may have changed; a status
  report; what is pending, since the project seems complete to him.
- Then: leave for now the pending items that are his own and need no
  seat; do what can be completed. Round 15's five are "somewhat better
  and reasonable" than Round 14's, which "looked basic", but still
  resemble each other by "30-45%": "how the boxes are placed and what is
  written and the other placements". Propose five more, "60-75%
  distinct", "state of the art", and taking nothing from existing
  websites, so that no one can raise a claim.

## Errors this seat made

1. **A path the Windows Python could not read.** A download went to Git
   Bash's /tmp, which Windows Python does not see; repeated into the
   scratchpad.
2. **A guessed address.** The first check of the live demos asked for
   demo/<design>/ and got twelve 404s; the gallery links
   designs/<design>/index.html, which answered 200 for all twelve.
3. **A long heredoc in Git Bash.** The shell could not parse it and ran
   nothing; the text went through a scratch file instead.

## What was found

- Read from GitHub's public API, unauthenticated (no gh on this machine):
  pull request 20 merged 2026-10-24 22:28Z and 21 on 2026-10-25 14:39Z,
  each merge's tree its branch head's (3ec3c74, fdfdf6a). Scope and
  Checks passed on both pull requests and on main; Checks 1,918 and
  1,888 s with seven designs, 3,157 and 3,020 s with twelve, inside 90
  minutes; Deploy 89 to 94 s.
- Pull request 22, the first from outside: Choudhary-Khuzaim's showcase
  entry, entry.json and a 3.1 MB screenshot, opened 17:19Z on 2026-10-25;
  CODEOWNERS requested the owner's review at once; the pull request
  template's showcase section filled; approved 17:42Z, merged 18:15Z
  (56077aa, main's tree with the entry's two files). Scope passed seven
  times, Checks 3,041 s and on main 3,062 s, Deploy 94 s. The weekly
  showcase check passed on 2026-10-26.
- The live gallery: twelve template cards, each naming its person; two
  showcase cards; all twelve demos answer 200 with their own design.css,
  the five sample demos with their own layout.css. The runner's previews
  of Broadsheet, Console and Signal, on Linux's faces, read as on Windows.
- On 56077aa here: check_workflows, check_template_cleanup, check_design
  (12), check_showcase and its --fetch-all (both sites 200, each linking
  to its author's profile), check_prompt, check_content, the gallery build
  and check_built (13 pages): 0 problems each; MAP.md current.
- The seat's processes: none running. The Python processes on the
  machine were another project's session's.

## What was done

- The records: STATE's verified line, headline, Publishing and Blocked
  rows; the two design rows and the two merges to completed.md, with
  pull request 22; the CODEOWNERS row; the runner-preview line out of
  Known unverified; two rows waiting on the owner (five more designs, and
  checks only for the designs a change touches); CAPABILITIES' runner
  times for twelve designs; this section.
- The eight local branches merged into main and gone from GitHub were
  deleted with git branch -d, which refuses an unmerged branch.

## The likeness, measured

A scratch script, not committed: for each design's demo, at 1366x768,
390x844 and 1080x1920, on the first screen, the Projects screen and the
Work screen, the box of each engine block in view (the menu, name,
headline, facts, summary, buttons, figures, strip, section titles, the
first three projects, the first two jobs) marked on a grid of about 85 px
cells; two designs' likeness is the mean Jaccard overlap of the same
blocks' cells, a block in view in one only counting 0, averaged over the
nine screen-viewports. Run once over the twelve live demos, 105 s:

- Round 15's five: 33% alike on average, 18% to 55%; Round 14's six: 31%,
  20% to 46%; all 66 pairs: 29%, 10% to 58%.
- Most alike: Bento and Sentinel 58%, Pipeline and Sentinel 55%,
  Broadsheet and Pipeline 54%, Bento and Pipeline 51%.

It matches the owner's own 30 to 45% for Round 15. Round 15's judged rule,
three of five dimensions with layout always among them, passed every pair;
the rule was too coarse to see what he sees.

Two more causes, read from the content and the designs: all six sample
people share one shape (3 projects, 2 jobs, 1 degree, 2 certificates, 3
figures, 3 contact routes, 3 skill groups, a feature figure, a three-part
headline), so every page has the same menu and the same count of boxes;
and all eleven designs after Default set the engine's four motion switches
(knot, tilt, strip, scroll) to 0.

## The proposal

Gitignored, for the owner to judge: briefs/round16-proposal/index.html,
wireframes at the three sizes. The bar: by the script, no pair above 35%
alike and each new design's mean at most 25%; judged, at least 8 of 12
aspects different from every other design. Five designs, each with its own
sample person of a different content shape:

- Cyanotype, for embedded and robotics engineers (Rowan Fixture): an
  engineering drawing sheet on blue grid paper, the menu as a title block
  at the bottom right, figures as callout balloons around a board outline.
- Handbook, for technical writers (Quinn Lorem): a cloth-bound book, a
  cover first screen, thumb-index tabs as the menu, chapters with margin
  notes; light and dark.
- Frost, for frontend developers (Avery Mockup, no degree): frosted glass
  over a moving aurora, a floating capsule menu, a kinetic name, project
  cards that stack as a deck; light and dark.
- Savepoint, for game developers (Robin Tileset): a pause screen, a hotbar
  menu, a player card, a level-select grid, an inventory of skills.
- Broadcast, for developer advocates (Drew Helloworld): a programme
  monitor with a lower third, a moving ticker with pause, segment bumpers,
  an episode guide, work as end credits.

No website is a reference; decoration is drawn in CSS; fonts OFL with no
Reserved Font Name; names avoid tech products' names. Estimated cost:
seventeen designs would take Checks about 71 minutes on GitHub, scaled
from 3,020 s for twelve; the 90-minute limit falls at about 21 designs.

## Not done

- The five designs: not built until the owner chooses.
- Checks only for the designs a change touches, and the standing check
  that no page scrolls sideways: waiting on his word; both change what
  every pull request runs.
- His own items, deferred by him: Test 1 on or after 2026-11-02, the four
  issue forms in the chooser, ADR-0012.
- Nothing pushed: records-after-merges waits on the owner.

# Round 17, 2026-10-28 UTC: checks on what a change alters

Model: Claude Opus 5.5 (claude-opus-5-5), in Claude Code, the same session
continued. HEAD at start: 87e9a6b on records-after-merges, which the owner
was merging; work on the branch checks-for-changes, cut from it. HEAD at
end: the commit that adds this section. Mode: mutating. No brief: the
owner's instructions in this conversation.

## What was asked

The owner, 2026-10-28 UTC, after Round 16's report that seventeen designs
would take Checks about 71 minutes: the change-only checks "has to start
now before you do anything else and consider this no.1 priority". "a
sound implementation plan on how you will do this work without breaking
anything or inconveniencing anyone as it is logical that only what is
changed is checked and what remains the same is passed. this will keep
the time only to what needs to be checked because this gallery will grow
and i do not want it to like check runs for days. so make sure that
while you work on this, no other issues are raised or current working is
broken." Also: the pull request text for records-after-merges first, so
he could merge while the seat worked; the five proposed designs approved
("only final look can tell 100% how good they are"); each person's
sections and counts may differ "as long as that is how their profession
portfolios are", nothing a profession's portfolio should have left out;
the standing width check and these checks may be built "if feasible".

## The plan, as stated to him before the work

Phase 1, this round: the job keeps its name, checks, which the ruleset
requires, and always reports, so no path filter; only the browser checks
narrow; "changed" decided by building the gallery from the base too and
comparing built files, not by file names; every page on any doubt (the
checks' own code, the base unreadable or unbuildable, a run by hand, the
weekly run, a local run without --since); the base a pull request's merge
parent or a push's previous main; a weekly run of every page as the net
for changes from outside, such as a newer Chrome; the run's summary
listing what was checked; defeat cases for every rule; ADR-0019. Phase 2,
later and separate: runs of every page split across parallel jobs, a
final job still named checks, before about 19 designs.

## Errors this seat made

1. **The harness's cleanup and git's read-only files.** The new cases make
   the copy a git repository; on Windows, git's object files are read-only
   and shutil.rmtree refused them, so the first run stopped after the
   first new case. The harness now restores write permission before
   deleting (writable in tools/prove_checks.py).
2. **A case built wrong.** "A base that does not build" first broke
   content/config.json's design, which the gallery build does not read;
   the base built and the case failed. It now breaks a design's
   design.json, which the gallery build does read, and passes.
3. **File names split on spaces.** The changed files were first split on
   whitespace, so a screenshot's name with spaces came apart, and a name
   git quotes would not have matched. Found in review before the commit;
   the names are NUL-separated now.
4. **remove.txt cannot list a workflow.** The weekly workflow was first
   added to the copy's removal list, which refuses workflow files; it is
   removed by the cleanup workflow's own step, beside scope.yml and
   showcase-links.yml.
5. **Two commands mistyped**: `git cherry-pick -q`, which git does not
   take, and the keep-awake helper given a relative interpreter path,
   which Windows could not start; both rerun correctly.

## What was built

- tools/ci.py: `select` builds the gallery from the base by the base's own
  build.py and compares built files; a design's demo is checked when its
  folder differs or is new, the gallery page when anything outside
  designs/ differs or the showcase changed, every page when static/
  differs, when a file in CHECKING changed (build.py, requirements.txt,
  tools/ci.py, tools/check_browser.py, tools/cdp.py, checks.yml), or when
  the base is missing, unreadable or does not build. `checks --since REF`
  passes the selection to the browser checks and writes it to the run's
  summary; `changes --since REF` prints it alone.
- tools/check_browser.py: `--designs` and `--skip-gallery-page`; a design
  the gallery lacks is a usage error.
- checks.yml: the base (a pull request's merge parent; a push's previous
  main, fetched), `--since`, and Run workflow for every page.
  checks-weekly.yml: every page each Monday at 04:41 UTC, anonymous clone,
  no permissions, only in this repository; the copy's cleanup removes it.
  tools/check_workflows.py holds the two workflows' axe-core pins equal.
- ADR-0019; standing-checks.md, commands.md, setup-on-github.md,
  add-a-design.md, use-this-template.md and the README's line on the
  accessibility checks.
- Found while proving it, on main too: pull request 22's real showcase
  entry, a 3360x2100 screenshot of 3.1 MB, broke two older defeat cases.
  "pictures: a maker that publishes the screenshot itself" met that
  entry's size failure before the planted one's, so its expected words
  were missing; "packing: a showcase picture without its reserved size"
  hung in the wait for pictures to decode and ended in a TimeoutError
  after 60 s, not a failure naming its cause. Reproduced on a clone of
  56077aa, main, without this branch; passed with that entry removed. The
  cases that plant their own entries now empty the copy's showcase first
  (own_showcase), and the packing check gives up waiting after 20 s and
  reports the picture as not loaded.

## Proofs

- The file harness on the working tree before the commit: 152 defeat
  cases, 30 planted controls, 0 unproven, in 538 s; among them the ten
  selection cases, the two usage cases and the two axe-pin cases.
- Every defeat case with the browser and axe on a fresh clone of 27db869,
  kept awake: 176 defeat cases and 35 planted controls, 2 unproven, the
  two above, in 4,792 s; the narrowed case failed on the fault in the
  design it checks, and its control passed.
- After the fix, the served-copy and packing families rerun, each on a
  fresh copy: the twelve cases of the served-copy and packing families, five controls and seven defeat cases, each as expected, in 878 s, the two that failed among them; committed as 1e9137c.
- End to end, in a scratch clone: one design's stylesheet changed, `ci.py
  checks --since HEAD~1 --axe`: exit 0 in 362 s, the browser checks 286 s
  of it on Bento alone, against 3,676 s for every page of twelve designs
  (2026-10-25). Pull request 22 replayed on the new tools: no design, the
  gallery page checked, in 8 s of selection. A change to content/: the
  seven designs shown with it, none of the five with their own person.
- tools/check_workflows.py, check_template_cleanup.py and check_prompt.py:
  0 problems each; gates A, B and C on the commit.

## Not done

- Phase 2: a run of every page split across parallel jobs, a final job
  still named checks; needed before about 19 designs.
- On GitHub only, until this branch merges: the base fetched on a push to
  main, the run's summary, and checks-weekly.yml, which runs from main.
- Nothing pushed: checks-for-changes waits on the owner, after
  records-after-merges.

# Round 18, 2026-10-28 UTC: a standing check that no page scrolls sideways

Model: Claude Opus 5.5 (claude-opus-5-5), in Claude Code, the same session
continued. Work on the branch width-check, cut from checks-for-changes.
Mode: mutating. No brief: the owner's answer of 2026-10-28 UTC to Round
16's question 3, "yes, you can build them if feasible", which covers the
check recommended in Report 14 after Poster (Round 14) and Sentinel
(Round 15) scrolled sideways on a phone, each found only by eye.

## What was built

- tools/check_browser.py, `width`: each page loaded once with scripts and
  once without, every section laid out, then set to 320, 360 and 390 px,
  1080 by 1920 and 1366 px; it fails when the document is wider than the
  window, naming the deepest elements past the edge. A box that scrolls
  inside itself passes. It runs on every design a change alters and on
  the gallery page, as every browser check does since ADR-0019.
- docs: standing-checks.md, design-contract.md (the rule and its usual
  cures), add-a-design.md, CONTRIBUTING.md; ADR-0009, Changes.

## Proofs

- On the twelve designs and the gallery page, built from this tree: 130
  runs, 0 failures, in 110 s.
- Its defeat case, Plain's footer name set 1400 px wide, fails with "the
  page scrolls"; its control, the same inside a footer that scrolls
  itself, passes; each on a fresh copy, in 22 s and 19 s.
- The checks themselves change in this branch, so its run on GitHub
  checks every page.

## Not done

- Nothing pushed: width-check waits on the owner, after
  checks-for-changes.
