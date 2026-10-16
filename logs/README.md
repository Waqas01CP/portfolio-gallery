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
| 2026-10-15 to 16 | 2026-10-12-brief-1-build.md | Brief 1, Round 2: the owner's answers to Report 1 | Records 0006 to 0011 accepted, 0013 and 0014 written; axe-core in the checks workflow; the Code of Conduct's contact, with gate A's allowed-text rule; the Chrome launcher's start fixed | Not published; on a fresh clone 47 defeat cases and 8 controls as expected and the full checks with axe pass; pre-publish search PASS; the CV search to rerun on the final commit |
| 2026-10-12 to 13 | 2026-10-12-brief-1-build.md | Brief 1 with Addendum 1; first session | Engine copied from the owner's site at 5f3b84d and generalised; sample content; default and plain designs; gallery; file and browser checks, 46 defeat cases; gates, 15 defeat cases; workflows; documents; setup steps | Stands on its own locally; not published; workflows never run; pull_request_target needs an Actions policy; 8 questions for the owner |
