---
type: index
description: The decision record index for portfolio-gallery, with the fixed topic list and the Pending list of decisions identified but not concluded.
status: current
---

# Decision records

MADR 4.0.0 with an Assumptions section, per the owner's Decision Record
Standard. One choice per record, written at the moment it was concluded.
Decision-maker on every record: the repository's owner, Waqas01CP. His name appears in
this repository only in LICENSE and README.md (his site's ADR-0012).

## How to read this

Records are numbered in the order they were concluded, not by importance.
The status column tells you whether a record is in force. **Proposed**
means written by the implementing seat for the owner to accept; until he
does, it describes what is built and why, and binds nothing he has not
approved. Follow a superseded record's pointer to its replacement.

A record's decision is never silently rewritten. An amendment that leaves
it in force goes in its Changes table; a replacement is a new record that
supersedes it. Before superseding, ask whether any rule is still in force
and not carried into the later record.

## Topic list

Fixed. A record's `topic` takes exactly one of these. Adding a topic is
itself a decision.

| Topic | Covers |
|---|---|
| process | How the repository is run: contributions, licence, gates, publishing |
| build | The generator, its dependencies, the workflows, the checks |
| security | What a contribution may contain and what keeps it from running |
| design | The design format's visual contract, typography, motion |
| hosting | Where sites are served from and how they are addressed |
| content | The content model and how claims trace to a source |

## Index

| ID | Title | Status |
|---|---|---|
| [0001](0001-scope-floor.md) | The scope floor | Accepted |
| [0002](0002-licence-mit-with-credit.md) | MIT licence, with credit asked and a removable footer link | Accepted |
| [0003](0003-designs-by-fork-and-pull-request.md) | Designs arrive as folders, by fork and pull request | Accepted |
| [0004](0004-build-on-github-actions.md) | Build with a Python generator, on GitHub Actions | Accepted |
| [0005](0005-published-when-it-stands-alone.md) | Published only once it stands on its own | Accepted |
| [0006](0006-design-format-and-security-model.md) | The design format and the security model | Accepted |
| [0007](0007-page-relative-addresses.md) | Every URL relative to the page | Accepted |
| [0008](0008-repository-gates.md) | The repository gates | Accepted |
| [0009](0009-quality-goals.md) | Quality goals, for every site and every design | Accepted |
| [0010](0010-headless-chrome-from-the-standard-library.md) | Headless Chrome, driven from Python's standard library | Accepted |
| [0011](0011-axe-core-in-ci.md) | axe-core in CI | Accepted |
| [0012](0012-lighthouse-in-ci.md) | Lighthouse in CI | Proposed |
| [0013](0013-default-design-keeps-the-owners-look.md) | The default design keeps the owner's site's look | Accepted |
| [0014](0014-web-fonts-with-font-display-optional.md) | Web fonts with font-display: optional | Accepted |
| [0015](0015-a-copy-cleans-itself-once.md) | A copy cleans itself up, once | Accepted |
| [0016](0016-templates-then-a-showcase.md) | Templates first, then a showcase of contributors' own sites | Accepted |

Records 0001 to 0005 carry the owner's decisions of 2026-10-11 UTC, written
on 2026-10-12 by the implementing seat from the brief that recorded them;
the brief is never committed, so these records and the session log of
2026-10-12 are where his words now live.

## Pending

Decisions identified but not yet concluded. Each waits on the owner.

- **ADR-0012, Lighthouse in CI.** Held as proposed by the owner on
  2026-10-15. Until he accepts it, the speed goals of ADR-0009 are
  measured locally by the maintainer, not by CI.

The owner's answers, dated 2026-10-16 in his local time (UTC+5) and
given on 2026-10-15 UTC, concluded the rest: CSS only (ADR-0006); the
default design keeps his site's look, credited to Waqas01CP (ADR-0013);
a first response to contributors within 7 days (CONTRIBUTING.md); the
README links his portfolio site, and the Code of Conduct's contact (both
ADR-0002, Changes); the commit identity, Waqas01CP with GitHub's
no-reply address (docs/reference/commands.md); records 0006 to 0011
accepted; and `font-display: optional` in the default design (ADR-0014).
