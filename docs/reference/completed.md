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
