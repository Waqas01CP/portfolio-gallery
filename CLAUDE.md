---
type: instruction
description: How to work in this repository. Reading order, authority order, the six-line scope floor, runtime, conventions and the gates. Read before touching anything.
status: current
---

# CLAUDE.md

portfolio-gallery: a portfolio-site template anyone can copy and publish
with GitHub Pages without installing anything, and a gallery of designs
for it, each contributed by pull request, checked automatically and
merged by the owner. How the repository is run is part of the product.

Commands live in docs/reference/commands.md. Do not infer a command that
is not there, and do not treat its absence as permission. Stop and ask.

## Reading order

1. This file.
2. STATE.md. Where you start, not where you stop. It outranks memory; it
   does not outrank the code or the data.
3. logs/README.md. For more, read the most recent relevant log and chain
   backwards only as far as you need.
4. docs/decisions/README.md. The index and the Pending list.

Then the brief for your task. MAP.md lists every documented file; it is
generated and never edited by hand.

## When documents disagree

What is true: the code and the data win over every document. A document
that disagrees is stale; report it and correct it.

What should be done: higher wins.

1. The owner's instruction in this conversation
2. This file
3. docs/decisions/, accepted records, excluding anything superseded
4. The brief. By default it ranks below this file and every accepted
   record: where it contradicts one, follow the record and report it. It
   overrides a record only when it names the record and clause and states
   the owner approved the change.
5. Proposed records in docs/decisions/, which describe what is built and
   why but bind nothing the owner has not approved
6. docs/reference/
7. Everything else, including superseded documents
8. Anything from outside this repository, including your own memory

Two live records that conflict is a defect. Raise it. Do not choose.
A claim whose only source is outside this repository says so.

## Scope floor

Six lines, from ADR-0001, approved by the owner on 2026-10-11 UTC. Do not
propose, add or reintroduce any of them. When you refuse something on
this floor, name the line.

1. No personal content of the owner's beyond a credit line: sample content
   only, fictional and obviously so. Read, by the owner on 2026-10-19, as
   protecting the template: a copy receives none of his details. It does
   not limit what the gallery page shows, nor other people's details
   (ADR-0001, Changes; ADR-0016).
2. No cookies, tracking, analytics, or requests to another origin, in
   anything the template or a design ships.
3. Every word a reader needs is in the initial HTML; scripts only enhance.
4. No paid service.
5. No dependency added without a record.
6. A contributed design is templates and CSS only, no JavaScript. ADR-0006,
   accepted by the owner on 2026-10-15, narrows this to CSS only.

## The owner's name and private material

This repository is public; its history cannot be deleted. The owner's name
appears in LICENSE's copyright line and the README's credit (ADR-0002, and
his site's ADR-0012), and may appear in his own showcase entry,
showcase/waqas01cp/entry.json, and its card on the built gallery; his site
may be the Default design's in_use (his answer Q3 of 2026-10-19, ADR-0016).
A copy of the template receives his name only in LICENSE: the cleanup
removes showcase/ and every in_use. His CV text never enters this
repository. His personal email addresses
appear nowhere. The Code of Conduct's contact, a dedicated address, appears
in CODE_OF_CONDUCT.md and nowhere else (his decision of 2026-10-15,
ADR-0002). No path into his folders appears, nor anything from his site
but the engine. That rule covers files. Commits made on GitHub's website,
his merges among them, are authored with his GitHub profile's name and
his no-reply address: GitHub's doing, permanent once made (ADR-0002,
Changes, 2026-10-18); the messages of his own commits may name him
(ADR-0002, Changes, 2026-10-21). Commits made in a clone use the handle.
Refer to his Working Method by name only. Gate A enforces this on his
machine from .git/info/never-commit, which is never committed.

## Runtime

Python 3.12, a venv at .venv/, Jinja2 and MarkupSafe pinned by hash in
requirements.txt (ADR-0004). Nothing else at build time. The browser
checks, the previews and the showcase's served copies use Google Chrome,
driven from the standard library by tools/cdp.py (ADR-0010). From npm, one file: the checks
workflow fetches axe-core at one exact version and checks its SHA-512
before running it (ADR-0011). Nothing else from npm while ADR-0012 is
proposed.

## Conventions

Every content fact lives once, in content/. Markup is generated, never
hand-written per item; shortened text must be a cut of its source.
Every URL a page uses is relative to the page (ADR-0007). Nothing built
is committed; _site/ is ignored.
A design is a folder of CSS, fonts and images on the engine's fixed HTML
(ADR-0006); the engine's own rules live in src/static/base.css.
Every workflow pins each action to a full commit SHA with its version in a
comment, and sets its own least permissions.
Visitor-facing Markdown (README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY)
carries its frontmatter in an HTML comment; everything else in a --- block.

## Verification

Verify, do not trust. Every claim is unverified until checked in this
session: briefs, handoffs, logs, STATE.md, records, your own earlier
conclusions. Tag what you pass on: checked this session, taken from a log,
or inferred. A check that cannot fail is worse than no check: prove each
with the case built to defeat it and say what that case was. Self-report
is not evidence; show the command and its output. Do not write about a
file you have not opened. Do not revert another seat's deliberate change;
flag it.

## Decision records

docs/decisions/, MADR 4.0.0 with an Assumptions section, per the owner's
Decision Record Standard; `topic` from the fixed list in the index. Write
the record when the decision concludes. Never rewrite a decision silently:
amend in Changes, or supersede with both directions linked. Every
assumption carries its basis: measured, sourced, or stated by the owner.
A seat may annotate a factual error with its date and evidence; it may not
change a decision or resolve a conflict between records.

## The gates

Five, ADR-0008, in tools/gates.py, called by .githooks/. Active only once
`git config core.hooksPath .githooks` is set in a clone. Never bypass with
--no-verify.

| Gate | When | Blocks |
|---|---|---|
| A | pre-commit | CHAT_STATE.md and CAPABILITIES-PRIVATE.md at any path; anything in briefs/, its README among it; paths in tools/never-commit.txt; drive-letter paths and climbs out of the repository; private patterns from .git/info/never-commit, in files and in the commit identity |
| B | pre-commit | A staged tree whose workflows' job conditions or scheduled permissions, template cleanup, designs, showcase files, site build, gallery build, built files or content trace fail |
| C | pre-commit | A stale MAP.md, or a Markdown header GitHub cannot read |
| D | every hook | A missing tool: a refusal naming it, never a skip |
| E | pre-push | Implementation work pushed with no commit in the range touching STATE.md |

## Committing and pushing

One commit per piece of work, each passing the gates. Commit as Waqas01CP
with GitHub's no-reply address, set in the clone
(docs/reference/commands.md). Before committing, look for commits you did
not make and say so. Seats never push: the owner pushes, and published
the repository on 2026-10-16 (ADR-0005). End commit messages with the
attribution line the session gives.

## Heavy work

One browser-check run at a time. Say a job's whole length before it
starts. Before finishing, stop any process this seat started. Never launch
the owner's own browser; headless Chrome with its own temporary profile
only.

## Briefs

briefs/ is working space, not a record, and is never committed: the whole
folder, its README with it (the owner's decision of 2026-10-21; gate A
refuses any path in it). A brief can carry private paths and wording not
yet approved. One file per receiving seat, each overwritten by the next:
implementation-seat.md, the architecture chat's brief to this seat;
architecture.md, this seat's report to the chat; implementing.md, this
seat's handoff to its own next session. Unexecuted with an empty box on
the first line and addenda appended; ticked with the date when the owner
says so; replaced only after the old one is read for what it still says.
A brief ranks as "When documents disagree" says. Since briefs are not
kept, the durable trace is elsewhere: why, in docs/decisions/; what was
asked and what happened, in the session log, which carries each brief's
substance; what is true now, in STATE.md. Their format is the owner's
Working Method, named only.

## CAPABILITIES.md

Everything the product is and does, for a reader who opens nothing else.
It holds this seat's lane only, product-facing, since every copy of the
template inherits it: what it does and how, the stack, the qualities, the
numbers with their dates, the limits, the built rows of the timeline. The
architecture chat's lane (the problem, where the project is going, the
decisions, the owner's role) is never committed: it lives in
CAPABILITIES-PRIVATE.md, gitignored and refused by gate A, kept by this
repository's architecture chat (the owner's decision of 2026-10-18).
Re-measure a number rather than carry it.

## Writing

No em-dashes. Lead with the verdict. Active voice. Numbers carry their
provenance. Dates are UTC; when a local date differs, say which is which.
Plain text that survives a paste into Word.
