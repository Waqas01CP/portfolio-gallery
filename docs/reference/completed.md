---
type: reference
description: Where DONE rows from STATE.md move, so the state file holds only what is unsettled. Nothing is ever deleted from here.
status: current
---

# Completed

DONE rows move here from `STATE.md` in the same commit that completes them,
so every session reads only what is still unsettled. Rows are never deleted.

Proof is a commit, a decision record or a log filename. Never a file path.

| Task | Evidence | Date | Proof |
|---|---|---|---|
| Skeleton, records, map, gates; each gate proven on its defeat case | [VERIFIED] | 2026-10-12 | c411847, 0169b54; logs/2026-10-12-brief-1-build.md |
| Engine copied and generalised; sample content; default and plain designs; gallery | [VERIFIED] | 2026-10-12 | 7af9697, 0169b54 |
| File checks, browser checks, previews, the defeat harness | [VERIFIED] | 2026-10-12 | 64f9c64, 0169b54 |
| The owner's answers to Report 1 applied: CSS only, the default design's look, the response time, the README's link, the Code of Conduct's contact, the commit identity, records 0006 to 0011 accepted, 0013 and 0014 written, fonts optional | [VERIFIED] gates A, B and C passed on each commit; the pre-publish search passed | 2026-10-16 | e794feb; ADR-0002, ADR-0013, ADR-0014 |
| Gate A: text allowed in a file taken out before the other patterns | [VERIFIED] 18 defeat cases refused and 4 controls passed, in a scratch clone | 2026-10-15 | 328cdad; ADR-0008 |
| The Chrome launcher: a failed start stops its Chrome; a refused port-file read is retried | [VERIFIED] both failures planted: 11 and 10 processes left before, none after; 40 starts and closes left nothing | 2026-10-16 | 322e0ea; logs/2026-10-12-brief-1-build.md |
| Checks on GitHub's runner, axe-core included: fetched, checked by SHA-512, run | [VERIFIED] run 38957566173 on 6a4de5e, every step green, the checks 8 min 53 s (GitHub's API) | 2026-10-16 | c7e3fd9; ADR-0011 |
| Deploy on GitHub in gallery mode: build, shots, assemble, deploy; the gallery live with both designs and their previews, the address without its slash redirected | [VERIFIED] run 38967233877, every job green; the pages fetched | 2026-10-16 | 6a4de5e; ADR-0010 |
| The workflow check: a job after a skippable job must say when it runs | [VERIFIED] 5 defeat cases and a control; gate B and ci.py checks run it | 2026-10-16 | 1f14aa7; ADR-0008 |
| The scope check on GitHub: refused a change outside designs/ in 6 s (pull request 4), passed a design (pull request 5) | [VERIFIED] check runs from GitHub's API | 2026-10-18 | b798834; ADR-0006 |
| Deploy in site mode, in a template copy: deploy ran and published the sample site (Test 4, run 39124404420); the copy's first runs started on their own | [BELIEVED] the chat's report; the copy is deleted, so its runs cannot be read now | 2026-10-18 | 1f14aa7 |
| Setup steps 1 to 12 and Tests 1 to 4 followed by the owner | [BELIEVED] the chat's report; [VERIFIED] the ruleset, pull requests 1 to 5 and their runs from the API | 2026-10-18 | 96675dc; ADR-0005 |
| The account's email kept private for website commits (step 12) | [BELIEVED] the chat's report; [VERIFIED] pull requests 1 to 5 authored with the no-reply address | 2026-10-18 | ADR-0002 |
| The setup guide's fixes merged: pull request 6, merge 5fe7e11, its tree 165fa5a's; Checks and Deploy green on it | [VERIFIED] trees compared; [BELIEVED] the runs, from the chat's report | 2026-10-18 | 96675dc, 165fa5a |
| Dark mode by the design's word: design.json's dark; a light-only tag and no Dark switch for false; checked in check_design.py, build.py and check_built.py | [VERIFIED] 6 defeat cases; the maintained designs' pages byte-identical; the guide's light-only test design passes every check with axe | 2026-10-18 | 39e49e6; ADR-0006 |
| CAPABILITIES' architecture lane kept out of the repository: CAPABILITIES-PRIVATE.md ignored and refused by gate A | [VERIFIED] 2 gate defeat cases | 2026-10-18 | d612b96; ADR-0008 |
| Dark mode and the private lane merged: pull request 7, merge 2b70358, its tree bb5a4bb's | [VERIFIED] trees compared | 2026-10-18 | 39e49e6, d612b96, bb5a4bb |
| The "Make it yours" list and what a copy's first commit runs, in the user guide | [VERIFIED] read in the committed file; the first-commit runs from setup Test 4 | 2026-10-18 | d46f349; ADR-0015 |
| The template cleanup merged: pull request 8, merge 122dc8b, its tree 1173d13's; Checks and Deploy green on main, and Template cleanup's job skipped there | [VERIFIED] trees compared; the runs read from GitHub's API | 2026-10-18 | d46f349, d5771c3, 1173d13 |
| The template cleanup in a real copy: once, all 27 listed paths and both workflows removed, 52 files kept, then Checks and Deploy green on the cleaned files | [VERIFIED] by the architecture chat on the copy's commits and runs before it was deleted (setup Test 5) | 2026-10-18 | ADR-0015 |
| A failed content trace names the CV line and what to do; the guides say the CV comes first | [VERIFIED] a defeat case, Test 5's edit, unproven under main's message | 2026-10-19 | db055e5 |
| The content trace's guidance merged: pull request 9, merge 4396a20, its tree 1953bb4's; Checks and Deploy green on main, Template cleanup skipped | [VERIFIED] trees compared; the runs read from GitHub's API | 2026-10-19 | db055e5, 1953bb4 |
| The showcase merged: pull request 10, merge e904357, its tree 33ab03d's; Checks and Deploy green on main, Template cleanup skipped; the gallery live with no entry | [VERIFIED] trees compared; the runs read from GitHub's API | 2026-10-19 | 5a7cecf, 33ab03d |
| Any snip as a showcase screenshot merged: pull request 11, merge 4562645, its tree a8ad6e3's; Checks and Deploy green on main, its shots job gathering and assemble taking the pictures; Template cleanup skipped | [VERIFIED] trees compared; the runs and their jobs read from GitHub's API | 2026-10-20 | 3020bb4, fceaace, a8ad6e3 |
| The showcase: files, scope, responses, served copies, gallery, weekly check, credit, cleanup; setup Test 6, the owner's own entry from a plain snip of 1077x1713, pull request 13: Scope and Checks success at ca4dfa0, Checks and Deploy success on main at fa2a687, Template cleanup skipped, Showcase links by hand success (run 39507307570); an earlier head, entry.json alone, failed Checks at the fetch step | [VERIFIED] the runs and their jobs read from GitHub's API | 2026-10-20 | 5a7cecf, 3020bb4, fceaace; ADR-0016; setup Test 6 |
| No floor and no pixel ceiling for showcase screenshots; the tool's own file name kept | [VERIFIED] the owner's answers to Report 9, through the chat's Brief 10 | 2026-10-20 | ADR-0016, Changes |
| Showcase cards in their own shapes, packed; one pull request template; the briefs folder off the repository: pull request 14, merge aaa6757, its tree d9e0e6a's; Scope and Checks success on the pull request, the packing check's grid-lanes mode among them on the runner's Chrome; Checks and Deploy success on main, Template cleanup skipped | [VERIFIED] trees compared; the runs read from GitHub's API | 2026-10-21 | 56c6dc3 to d9e0e6a; ADR-0016, ADR-0008 |
| The showcase's shape limits, 2.4 either way, accepted; his name allowed in his own commit messages | [VERIFIED] the owner's answers to Report 10, through the chat's Brief 11 | 2026-10-21 | ADR-0016, Changes; ADR-0002, Changes |
