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
