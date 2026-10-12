---
type: reference
description: What the briefs folder is and how it behaves. Working space, not a record; briefs and reports are overwritten and never committed. The durable trace is the session log.
status: current
---

# Briefs

**This folder is working space, not a record.** It holds the latest brief
or report addressed to each seat: the specification the architecture chat
hands a fresh implementing session, the seat's report back, and the seat's
own handoff. Only this file is tracked; the rest is in `.gitignore`.

The format is the owner's cross-project Working Method, which lives in his
private folders and is deliberately not linked from here, because this
repository is public. A brief that needs a private path carries it, and a
brief is never committed.

## Why the briefs themselves are not committed

A brief is transient by design, and it can carry private paths and wording
not yet approved. The durable trace lives elsewhere:

| Question | Where the answer lives |
|---|---|
| Why was this decided | `docs/decisions/` |
| What was asked in a round | the session log's own summary |
| What happened | `logs/`, indexed in `logs/README.md` |
| What the state is now | `STATE.md` |

**So the session log carries the brief's substance.** A log that records
only what was built, without what was asked, breaks that chain.

## Rank

A brief ranks below `CLAUDE.md` and every accepted record. Where it
contradicts one, follow the record and report the contradiction. The only
exception is a brief that names the record and the clause and states that
the owner approved the override.

## Convention

One file per receiving seat, each overwritten by the next:

| File | From | To |
|---|---|---|
| `implementation-seat.md` | the architecture chat | the implementing seat |
| `architecture.md` | the implementing seat | the architecture chat |
| `implementing.md` | the implementing seat | its own next session, as a handoff |

Each file is unexecuted, with an empty box on its first line and any
addendum appended; executed, ticked with the date when the owner says it
was acted on; and replaced only after it has been read for what it still
says.
