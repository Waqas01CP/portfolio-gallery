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
