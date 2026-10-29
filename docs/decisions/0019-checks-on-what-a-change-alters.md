---
status: accepted
topic: build
description: "The browser checks of a pull request or a push look only at the pages the change alters, found by building the gallery from the base too and comparing the built files; every page is checked when the checks themselves change, when the base cannot be read or built, by hand, and each Monday. Read before changing tools/ci.py's selection, checks.yml or checks-weekly.yml."
date: 2026-10-28
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0019: Checks on what a change alters

## Context and Problem Statement

Every run of the checks workflow ran the browser checks on every design:
about 250 s a design on GitHub's runner, 3,020 s for twelve on
2026-10-25, against a limit raised that day from 45 to 90 minutes. On
2026-10-25 UTC the owner answered that raise: "it should not be the
case, since the prior designs were not touched then they should not be
checked again and only under the case when something in those design
changes." On 2026-10-28 UTC he made it the first priority: only what is
changed is checked, what remains the same is passed, the gallery will
grow, and nothing that works now may break. How does a run know which
pages a change alters, without ever skipping one it does?

## Decision Drivers

- His words of 2026-10-25 and 2026-10-28 UTC, in this repository's
  implementing session.
- A missed page is worse than a slow run: a check that skips a changed
  page passes what it never looked at.
- The ruleset requires the check `checks` (docs/setup-on-github.md, step
  7); it must report on every pull request, or nothing can merge.
- A contributor's pull request must not be able to choose what it is
  checked against (ADR-0006).
- No new dependency (scope floor line 5).

## Assumptions

- A1. Two builds of the same source, as of the same month, are byte for
  byte the same. Basis: measured; every run of `tools/ci.py checks`
  builds the site and the gallery twice and compares them, and fails
  otherwise.
- A2. A page's browser results depend on its own built files, the
  engine's shared files (static/), the checks' own code, axe-core and
  the browser. Basis: tools/check_browser.py serves the built folder and
  variants made from it, read this session; the browser is the one
  input from outside the repository.
- A3. A design's browser checks take about 250 s on GitHub's runner, and
  the 90-minute limit holds about 21 designs. Basis: measured, 3,020 s
  for twelve, run 40203263050, 2026-10-25.
- A4. A contributor's pull request that changes anything outside one
  design folder or its own showcase entry fails the scope check, which
  runs from the default branch. Basis: ADR-0006; scope.yml.
- A5. A workflow skipped by a `paths` filter leaves a required check
  waiting, so the pull request cannot merge. Basis: GitHub's
  documentation on required status checks, as this seat knows it; not
  read this session.
- A6. A scheduled run holds no permissions. Basis: stated by the owner,
  answer Q2 of 2026-10-19; tools/check_workflows.py enforces it.

## Considered Options

1. Every page on every run, as before.
2. A `paths` filter on the workflow, so it runs only for some files.
3. Inside the run, choose designs by the names of the changed files.
4. Inside the run, build the gallery from the base too and check the
   pages whose built files differ.
5. Every page on every run, split across parallel jobs.

## Decision Outcome

Chosen: option 4, with every page checked whenever there is doubt.

- **The base.** On a pull request, the merge's first parent, the main it
  merges into. On a push to main, the main before it, fetched. A run
  started by hand (Actions, Checks, Run workflow) has none.
- **The selection** (tools/ci.py, `select`). The gallery is built from
  the base as well, by the base's own build.py, as of the same month. A
  design's demo is checked when any file under its built folder
  differs, or is new. The gallery page is checked when anything outside
  designs/ differs, or the showcase's sources changed. When the engine's
  shared files (static/) differ, every page is checked.
- **Every page** is checked when a file that decides how pages are
  checked changed (CHECKING in tools/ci.py: build.py, requirements.txt,
  tools/ci.py, tools/check_browser.py, tools/cdp.py, checks.yml, which
  pins axe-core); when the base is not in the clone, cannot be read, or
  does not build; when there is no base; and each Monday, in
  checks-weekly.yml, which copies the default branch anonymously and
  holds no permissions. Its axe-core pin is held equal to checks.yml's
  by tools/check_workflows.py.
- **Only the browser checks narrow.** The file checks, both builds of
  the site and the gallery, the content traces, the pictures and the
  cleanup check run in full on every run; they take minutes, not hours.
- **The job keeps its name** and always runs, so the required check
  always reports. Its summary on GitHub lists what was checked and what
  was unchanged.
- **Locally**, `tools/ci.py checks` without `--since` checks every page,
  as before; `tools/ci.py changes --since REF` shows the selection alone.

### Consequences

- Good, because a pull request that changes one design checks that
  design's page, and the gallery page only if it changed: on this
  machine, one design's change through the whole run took MEASURED
  (2026-10-28), where every page took 3,676 s for twelve (2026-10-25).
- Good, because the selection compares what is built, not file names: a
  change to content/ checks exactly the designs shown with that content,
  and none shown with their own sample person (ADR-0018).
- Good, because doubt checks everything: a wrong guess costs time, never
  a page.
- Bad, because a fault that reaches an unchanged page from outside, such
  as a newer Chrome on the runner, is found by the weekly run, up to a
  week later, not by the next pull request.
- Bad, because a run that checks every page still grows with the
  gallery: about 71 minutes for seventeen designs, estimated from A3.
  Splitting those runs across parallel jobs (option 5) is the next step,
  needed before about 19 designs.
- Neutral: the base's build adds about 8 s to a run (measured on this
  machine, 2026-10-28).

### Confirmation

tools/prove_checks.py, each case on a copy made a repository whose last
commit is the change: one design's stylesheet selects that design alone;
the shared sample content selects every design shown with it and no
other; a sample person's content selects their design alone; a template
selects every design; base.css, and a file in CHECKING, check every page;
a base not in the clone, and one that does not build, check every page; a
showcase entry checks the gallery page and no design; documentation alone
checks no page. tools/check_browser.py refuses a design the gallery
lacks, and designs named for a site; a narrowed run fails on a fault in
the design it checks, and the control shows it looks at no other. Two
cases hold the two workflows' axe-core pins equal. Replayed on pull
request 22, a showcase entry, the selection checks the gallery page and
no design.

## Pros and Cons of the Options

### 1. Every page on every run

- Good, because nothing is ever skipped.
- Bad, because every run grows with the gallery; the 90-minute limit
  holds about 21 designs, and the owner asked for this to end.

### 2. A `paths` filter on the workflow

- Bad, because a required check that never runs leaves the pull request
  unable to merge (A5).
- Bad, because a file's name does not say which pages it alters.

### 3. Designs chosen by changed file names

- Good, because it needs no second build.
- Bad, because the engine, the content and the samples reach pages
  indirectly: a change to content/ alters seven designs' demos and none
  of the other five, which no list of paths says without restating the
  build.

### 4. The built pages compared with the base's (chosen)

- Good, because it checks exactly the pages whose built files differ, by
  the build itself.
- Good, because it needs only git and the build, both already there.
- Bad, because it trusts A1 and A2; the weekly run of every page is the
  net under A2.

### 5. Every page, in parallel jobs

- Good, because a run of every page stays near one design's length per
  job.
- Bad, because it still spends a machine on every unchanged page of
  every pull request.
- Not instead of option 4 but after it: for the runs that check every
  page.

## More Information

- tools/ci.py (`select`, `chosen`, CHECKING); tools/check_browser.py
  (`--designs`, `--skip-gallery-page`); .github/workflows/checks.yml and
  checks-weekly.yml; docs/reference/standing-checks.md.
- ADR-0006 (the scope check), ADR-0011 (axe-core), ADR-0015 (a copy's
  cleanup removes checks-weekly.yml with the project's other workflows).

## Changes

| Date | Change |
|---|---|
| 2026-10-28 | Written, from the owner's word of 2026-10-25 and his instruction of 2026-10-28 UTC. |
| 2026-10-29 | **build.py leaves CHECKING; a change to it checks the gallery page.** The audit at the owner's request found every run since this record checked every page, each for a file then in CHECKING: tools/ci.py (pull request 24), tools/check_browser.py (25), and build.py (26), whose change, a fix for left-out sections, altered no existing page by a byte. What build.py does to a page shows in the page, which the selection compares; its one part in the checking is the showcase's shape limits the packing check reads, so its change now checks the gallery page. Replayed with this rule, pull request 26 checks its five new designs and the gallery page instead of seventeen. **A selection that fails checks every page** rather than end the run red. **A new push to a pull request cancels the run for its old commit**; on main every run finishes. Considered and left: skipping the run on main after a merge whose tree its pull request already checked, because GitHub keeps no record of the base a merged pull request's run was tested against (the run's pull_requests field is empty after the merge), so the skip could not be proven safe. Measured: every page of seventeen designs takes 75.4 minutes on GitHub's runner (runs 40776363105 and 40844380486), about 4.4 minutes a design; the 90-minute limit falls at about 20 designs, so Phase 2, runs of every page in parallel jobs, is due before the gallery reaches 20. | The owner's request of 2026-10-29 UTC for an audit of the merges' time and of the checks as a guard; the session log, Round 20. |
