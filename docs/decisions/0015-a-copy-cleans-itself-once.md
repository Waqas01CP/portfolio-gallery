---
status: accepted
topic: build
description: "A copy made with Use this template removes the project's own files once, by a workflow that holds contents: write and never runs here or in a fork; the user guide lists the same files for when it does not run. Read before changing what a copy keeps, the cleanup workflow, or a project-only workflow."
date: 2026-10-18
decision-makers: Waqas01CP, the repository's owner
# consulted:
# informed:
---

# ADR-0015: A copy cleans itself up, once

## Context and Problem Statement

Every copy of the template inherits every committed file, about 110, and
most serve only this project: its decision records, logs, state, map,
contribution rules and tools, a Code of Conduct naming the owner's
address, and a CODEOWNERS file naming him. Reports about a stranger's
site would reach him, and the project's direction and his decisions
travel into strangers' repositories, the reason the owner gave on
2026-10-18 for keeping the architecture lane of CAPABILITIES out of the
repository. How should a copy lose what is not its own?

## Decision Drivers

- The owner's decision of 2026-10-18: a "Make it yours" list in the user
  guide now, and a cleanup workflow that runs once in a copy, his idea,
  in place of a separate template repository.
- ADR-0001: no install for a user; whatever happens must happen on
  GitHub.
- ADR-0006: every workflow holds the least it needs.

## Assumptions

- A1. A copy's first commit starts its workflows on its own. **Measured**:
  setup Test 4, 2026-10-18, pg-copy-test's first commit started Checks
  and Deploy (the portfolio architecture chat's report).
- A2. A commit pushed with the workflow's own token starts no new run.
  **Sourced**: GitHub Docs, "GITHUB_TOKEN", read 2026-10-18: "events
  triggered by the GITHUB_TOKEN will not create a new workflow run", with
  exceptions for workflow_dispatch and repository_dispatch.
- A3. The workflow's own token cannot create or change a workflow file.
  **Sourced**, not from GitHub's documentation: a run's log quoted in
  JetBrains/intellij-platform-plugin-template issue 486 (2024-11-04)
  reads "refusing to allow a GitHub App to create or update workflow
  ... without `workflows` permission"; GitHub's list of the token's
  permissions, read 2026-10-18, has no workflows permission. Whether it
  may delete one is not known: JetBrains' cleanup deletes two and no
  report of its failing was found. Setup Test 5 establishes it.
  **Measured** (annotated 2026-10-19): it may delete one. In setup Test
  5, 2026-10-18, the cleanup's second commit in pg-cleanup-test deleted
  scope.yml and template-cleanup.yml, and its log read "Removed scope.yml
  and template-cleanup.yml." (the architecture chat's reading of the
  copy's commits and run, before the copy was deleted).
- A4. Forks start with workflows off, and a fork keeps the project's
  files on purpose. **Sourced**: GitHub Docs, "Events that trigger
  workflows", read 2026-10-12.

## Considered Options

- A cleanup workflow in the copy, with the guide's list for when it does
  not run
- The guide's list alone
- Every project-only file under one folder
- A separate template repository

## Decision Outcome

Chosen option: "A cleanup workflow in the copy, with the guide's list
for when it does not run", decided by the owner on 2026-10-18 UTC.

We will remove, once, in a copy, every path listed in
.github/template-cleanup/remove.txt, put a copy's own README in place of
the project's, and delete the list and its script last, so that a later
run has nothing to do.
We will run it from .github/workflows/template-cleanup.yml on a push to
main, with `contents: write` in its one job and nothing elsewhere; its
condition excludes Waqas01CP/portfolio-gallery and every fork, and
cleanup.py refuses both again by itself.
We will try to delete the project's own workflows, scope.yml and the
cleanup itself, in a separate commit, and leave a notice if GitHub
refuses; scope.yml runs only in Waqas01CP/portfolio-gallery, so a copy
that keeps it runs nothing.
We will keep in a copy what it needs to build, check and publish its
site, the user's guide and references, and LICENSE, whose notice the MIT
licence keeps with every copy.
We will list the same files in the user guide, CODE_OF_CONDUCT.md and
.github/CODEOWNERS first, for a copy whose cleanup did not run.

### Consequences

- Positive: a copy carries no reports route to the owner and none of the
  project's records, without a second repository to keep in step.
- Positive: the user does nothing; the commit shows what went.
- Negative: one workflow in this repository holds a write permission,
  though it never runs here.
- Negative: two workflow files may stay in a copy (A3), inert. (2026-10-19:
  in Test 5 they went; they stay only if GitHub refuses the deletion.)
- Negative: the guard names this repository; renaming or transferring it
  needs the guard changed with it.
- Neutral: the copy's first runs check the uncleaned files; its next
  commit checks the cleaned ones (A2).

### Confirmation

**The cleanup leaves a copy that works.** tools/check_template_cleanup.py,
in gate B and on every pull request while the cleanup exists: nothing
changes as this repository or as a fork; as a copy every listed path
goes, CODE_OF_CONDUCT.md and .github/CODEOWNERS above all, the README is
replaced and the cleanup's folder goes; a later run changes nothing; the
cleaned copy passes its own file checks and builds; every relative link
in its Markdown resolves. Six defeat cases in tools/prove_checks.py.

**It runs once, in a real copy, and what GitHub allows is known.** Setup
Test 5: a throwaway copy, its runs and files read by the architecture
chat, then deleted.

**It never runs here.** After this record merges, the cleanup's run on
main in this repository shows its job skipped.

Results, 2026-10-18: in Test 5 the copy's first commit started Checks,
Deploy and Template cleanup; the cleanup removed all 27 listed paths,
replaced the README and removed its own folder, then removed the two
workflows; the copy kept 52 files, its `.github/` only checks.yml and
deploy.yml, and the owner's name only in LICENSE; after Pages was set and
content changed, Checks and Deploy went green on the cleaned files (the
architecture chat's report). Here, the cleanup's run on the merge of pull
request 8, 39165247220, has its job skipped (read from GitHub's API on
2026-10-19).

## Pros and Cons of the Options

### A cleanup workflow

- Good: every copy is cleaned, with nothing asked of its owner.
- Bad: a write permission in a workflow, and workflow files it may not
  remove.

### The list alone

- Good: nothing runs.
- Bad: each user must read and act; the files arrive regardless.

### One folder

- Good: one folder to delete.
- Bad: a large move with every link changed, and still the user's work.

### A separate template repository

- Good: copies receive nothing of the project.
- Bad: a second repository and a way to keep it in step, by a token held
  as a secret or by hand.

## More Information

- Precedent: JetBrains/intellij-platform-plugin-template's
  `.github/workflows/template-cleanup.yml`, read at its source on
  2026-10-18 (last changed 2026-09-28, b871890): **Primary, a precedent**.
  It runs on push to main when the repository's name is not the
  template's, holds `contents: write`, replaces files from
  `.github/template-cleanup/`, deletes the project's own files and its own
  workflow, and pushes with the workflow's token through a third-party
  action. Taken here: the trigger, the folder of replacement files, the
  least permission. Not taken: a guard by name alone (a copy that keeps
  the name would be skipped, and a fork with it too, by accident rather
  than by rule); actions not pinned to a commit; a third-party push
  action; deleting LICENSE.
- JetBrains' issue 486, the log in A3: **Practitioner report, one
  user's run**.
- GitHub Docs, "GITHUB_TOKEN" and "Workflow syntax", read 2026-10-18:
  **First-party documentation**.

## Changes

| Date | Change | Why |
|---|---|---|
| 2026-10-19 | **A3 measured: the workflow's own token may delete workflow files.** The decision stands: the cleanup still tries the deletion in a commit of its own and leaves a notice if GitHub ever refuses. The user guide's "Make it yours" now lists the two workflows with the rest, for a copy whose cleanup did not run, in place of saying they may stay. | Setup Test 5, 2026-10-18, as read by the portfolio architecture chat; first-party by test. |
| 2026-10-19 | **The cleanup also removes the showcase and every in_use**: remove.txt gains showcase/, docs/how-to/add-to-the-showcase.md and tools/check_showcase.py; cleanup.py drops in_use from every designs/*/design.json; the workflow's second commit also tries .github/workflows/showcase-links.yml. check_template_cleanup.py plants an entry and an in_use in its copy and proves both go, with two defeat cases. | ADR-0016 and the owner's answer Q3 of 2026-10-19: copies receive none of his details. |
| 2026-10-21 | **remove.txt no longer lists briefs**, which no copy can receive since the folder left the repository (ADR-0008, Changes, 2026-10-21), **and lists tools/check_prompt.py**, which checks the project's own README (ADR-0017). The new issue forms go with `.github/ISSUE_TEMPLATE/`, as before. | The owner's answer of 2026-10-21 to the seat's Report 10, 4.2, through the chat's Brief 11. |
| 2026-10-23 | **The copy's README carries a prompt for an AI assistant** (ADR-0017, Changes, 2026-10-23). check_template_cleanup.py now builds the cleaned copy's site with `tools/ci.py build --mode site`, the command that prompt gives, and checks that the copy's README carries the prompt, that every path it names is in the copy and that every command it gives is in a guide the copy keeps; four defeat cases. | The owner's yes of 2026-10-23 to the seat's Report 11, 3.6, through the chat's Brief 12. |
| 2026-10-23 | **The cleanup puts a copy's own AGENTS.md in place**, copy-AGENTS.md beside copy-README.md, both named in cleanup.py's OWN (ADR-0017, Changes, 2026-10-23). check_template_cleanup.py checks both are the copy's own; one defeat case, the cleanup leaving the project's. | The owner's yes of 2026-10-23 to the seat's Report 11, 3.4, through the chat's Brief 12. |
