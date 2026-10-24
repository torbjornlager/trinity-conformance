# Entry-marker controls — 24 October 2026

All four diagnostic observations completed, without probe timeouts/errors:

| Control | SWI | Trealla |
| --- | --- | --- |
| AMC-001 throw(admission_runtime_error) | Query error; marker present | Query error; marker present |
| AMC-002 fail | Logical failure; marker present | Logical failure; marker present |

These controls support interpreting an absent marker in the main admission run
as no query entry, rather than automatic deletion of ordinary data on any query
exception or failure. They do not prove behavior for every control exception or
arbitrary cleanup path. They are observations, not extra conformance passes.

Raw reports contain exact sent command objects and decoded responses, including
entry follow-up and halt. No output callback is used. See the main
../2026-10-24-admission-paths/REPORT.md for capture method, revisions and limits.
Both control fixture nodes stopped; every source/engine/library/live-node
preservation check passed. Runtime code and installed engines were unchanged.
