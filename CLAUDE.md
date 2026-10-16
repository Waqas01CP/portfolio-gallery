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
   only, fictional and obviously so.
2. No cookies, tracking, analytics, or requests to another origin, in
   anything the template or a design ships.
3. Every word a reader needs is in the initial HTML; scripts only enhance.
4. No paid service.
5. No dependency added without a record.
6. A contributed design is templates and CSS only, no JavaScript. ADR-0006
   proposes CSS only, pending the owner's answer; what is built is CSS only.

## The owner's name and private material

This repository is public; its history cannot be deleted. The owner's name
appears in exactly two places, LICENSE's copyright line and the README's
credit (ADR-0002, and his site's ADR-0012). His email appears nowhere, nor
does any path into his folders or anything from his site but the engine.
Refer to his Working Method by name only. Gate A enforces this on his
machine from .git/info/never-commit, which is never committed.

## Runtime

Python 3.12, a venv at .venv/, Jinja2 and MarkupSafe pinned by hash in
requirements.txt (ADR-0004). Nothing else at build time. The browser
checks and the previews use Google Chrome, driven from the standard
library by tools/cdp.py (ADR-0010). From npm, one file: the checks
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
| A | pre-commit | CHAT_STATE.md; briefs/ but its README; paths in tools/never-commit.txt; drive-letter paths and climbs out of the repository; private patterns from .git/info/never-commit, in files and in the commit identity |
| B | pre-commit | A staged tree whose designs, site build, gallery build, built files or content trace fail |
| C | pre-commit | A stale MAP.md, or a Markdown header GitHub cannot read |
| D | every hook | A missing tool: a refusal naming it, never a skip |
| E | pre-push | Implementation work pushed with no commit in the range touching STATE.md |

## Committing and pushing

One commit per piece of work, each passing the gates. Before committing,
look for commits you did not make and say so. Nothing is pushed and no
remote exists until the owner publishes it himself (ADR-0005). End commit
messages with the attribution line the session gives.

## Heavy work

One browser-check run at a time. Say a job's whole length before it
starts. Before finishing, stop any process this seat started. Never launch
the owner's own browser; headless Chrome with its own temporary profile
only.

## Briefs

briefs/, gitignored, one file per receiving seat: implementation-seat.md,
the brief to this seat; architecture.md, this seat's report;
implementing.md, this seat's handoff. Unexecuted with an empty box on the
first line and addenda appended; ticked with the date when the owner says
so; replaced only after the old one is read for what it still says.

## CAPABILITIES.md

Everything the project is and does, for a reader who opens nothing else.
This seat's lane: what it does and how, the stack, the qualities, the
numbers with their dates, the limits, the built rows of the timeline. The
architecture chat's, once it exists: the purpose, where it is going, the
decisions and the owner's role. Re-measure a number rather than carry it.

## Writing

No em-dashes. Lead with the verdict. Active voice. Numbers carry their
provenance. Dates are UTC; when a local date differs, say which is which.
Plain text that survives a paste into Word.
