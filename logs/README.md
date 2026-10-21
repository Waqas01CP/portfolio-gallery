---
type: index
description: The session log index. Read this first for what prior sessions did, then chain backwards through the most recent relevant log only as far as needed.
status: current
---

# Session logs

One log per session, newest at the top. This table is the navigation index
for all session history.

## How to use this file

Read this table first. It tells you what prior sessions did. When you need
detail beyond it, read the most recent relevant log; that log references
the one before it. Chain backwards only as far as you need, and stop when
you have enough. Do not read the directory.

## How to maintain it

Append your row in the same commit as your work, or in the session's last
commit when the work went out as several. A log with no row here is
invisible; if you find one, read it and add its row before anything else.
Never delete or modify a row: a correction is a new row saying so. Rows
are compressed, with no prose and no reasoning. One session, one file; a
session that continues across rounds adds a row per round, each naming the
same file.

## Log format

The session-log template in the owner's cross-project Working Method,
which lives in his private folders and is not linked from here: a header
with date, model, HEAD and mode; what was asked; errors this seat made;
what was done, each claim tagged verified or believed; rejected
alternatives; checked and found correct; not done; findings and
recommendations.

## Reorganisation

When this directory passes about 80 files at its root, split by year into
subdirectories and leave this index at the top pointing into them.

## Index

| Date (UTC) | Log file | Session | What was done | Outcome |
|---|---|---|---|---|
| 2026-10-22 | 2026-10-12-brief-1-build.md | Brief 11, Round 11: his answers; documents a person and an AI can both follow; the README's prompt | Showcase entry and Question forms; borderless showcase cards; his own commit messages may name him; the README's table of paths, live pictures and a self-contained prompt for an AI, held to the repository by tools/check_prompt.py in ci.py and gate B; CLAUDE.md routes other AIs to the README; agent-instruction conventions researched; ADR-0017 | On the branch guides-and-prompt, not pushed; every check with axe and the deploy's path pass on a fresh clone; 129 defeat cases and 33 controls; gates 29 of 29 |
| 2026-10-21 | 2026-10-12-brief-1-build.md | Brief 10, Round 10: the template, cards in their own shapes, briefs off the repository | One pull request template for a design or a showcase entry; showcase cards in their pictures' shapes within 2.4 either way, packed by grid-lanes or gallery.js in folder order, sizes reserved; the packing check; the briefs folder untracked and refused by gate A; Test 6 recorded; ADR-0016 and ADR-0008 Changes | On the branch showcase-shapes, not pushed; every check with axe and the deploy's path with 13 snips pass on a fresh clone; 121 defeat cases and 32 controls; gates 28 of 28 |
| 2026-10-20 | 2026-10-12-brief-1-build.md | Brief 9, Round 9: a showcase screenshot is any snip | Full-screen snips measured up to 5K, the cap set at 20 MiB; served copies drawn by Chrome, GPU off, image chunk only; no width, shape or name rule; the gallery re-measured; ADR-0016 and ADR-0010 Changes | On the branch showcase-any-snip, not pushed; every defeat case and every check pass on a fresh clone; the deploy's path rehearsed; gates 27 of 27 |
| 2026-10-19 | 2026-10-12-brief-1-build.md | Brief 1, Round 8: the owner's answers on the showcase | Screenshots and the gallery measured; the showcase built: files, scope, responses never rendered, the gallery's two sections, the credit, the weekly check with no permissions, the cleanup; 40 defeat cases and 7 planted controls; ADR-0016 | On the branch showcase, not pushed; every defeat case and every check pass on a fresh clone; gates 27 of 27 |
| 2026-10-19 | 2026-10-12-brief-1-build.md | Brief 1, Round 7: the chat's fixes from setup Test 5, and the showcase | The content trace's failure names the CV line and what to do, 1 defeat case; the CV-first rule in the guide and both READMEs; "Make it yours" shrunk; ADR-0015's A3 measured; the showcase proposed with a draft ADR-0016 | On the branch content-trace-guidance, not pushed; 55 file defeat cases and 8 controls; every check with axe on a fresh clone; gates 25 of 25 |
| 2026-10-18 | 2026-10-12-brief-1-build.md | Brief 1, Round 6: the owner's decision on what copies inherit | The template cleanup workflow with its guards and check, 6 defeat cases; "Make it yours" in the user guide; setup Test 5; ADR-0015; JetBrains' precedent read at source | On the branch template-cleanup, not pushed; on a fresh clone 54 file defeat cases, 8 controls and every check pass; gates 25 of 25 |
| 2026-10-18 | 2026-10-12-brief-1-build.md | Brief 1, Round 5: the owner's decisions on dark mode and CAPABILITIES | design.json's dark drives the colour-scheme tag and the Dark switch, 6 defeat cases; CAPABILITIES-PRIVATE.md ignored and refused by gate A; the copies question put to the owner | On the branch dark-mode-and-capabilities, not pushed; on a fresh clone 58 defeat cases, 9 controls and every check pass |
| 2026-10-18 | 2026-10-12-brief-1-build.md | Brief 1, Round 4: the chat's fixes after the owner's run of every setup step and test | The setup guide corrected (steps 2, 9, 11, 12; Tests 1 and 2; a dated rerun of Test 1); website commit names recorded; the workflow check's limit stated; the dark-mode question put to the owner | On the branch setup-guide-fixes, not pushed; file defeat cases and gates pass; search PASS |
| 2026-10-16 | 2026-10-12-brief-1-build.md | Brief 1, Round 3: the chat's finding during setup step 8 | The deploy job given a condition so it runs when shots is skipped; tools/check_workflows.py in gate B and ci.py checks, 5 defeat cases; setup step 12 (email privacy) and Test 4 (site-mode proof) | Public since the owner's push; gallery live; the fix committed, not pushed; proven on GitHub only by Test 4 |
| 2026-10-15 to 16 | 2026-10-12-brief-1-build.md | Brief 1, Round 2: the owner's answers to Report 1 | Records 0006 to 0011 accepted, 0013 and 0014 written; axe-core in the checks workflow; the Code of Conduct's contact, with gate A's allowed-text rule; the Chrome launcher's start fixed | Not published; on a fresh clone 47 defeat cases and 8 controls as expected and the full checks with axe pass; pre-publish search PASS; the CV search to rerun on the final commit |
| 2026-10-12 to 13 | 2026-10-12-brief-1-build.md | Brief 1 with Addendum 1; first session | Engine copied from the owner's site at 5f3b84d and generalised; sample content; default and plain designs; gallery; file and browser checks, 46 defeat cases; gates, 15 defeat cases; workflows; documents; setup steps | Stands on its own locally; not published; workflows never run; pull_request_target needs an Actions policy; 8 questions for the owner |
