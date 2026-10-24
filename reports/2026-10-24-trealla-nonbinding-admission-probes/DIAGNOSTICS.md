# Admission paths — diagnostic matrix, 24 October 2026

**20 completed observations; 0 diagnostic errors. No conformance passes are assigned.**

Each cell describes an actual response and whether the query entry marker
was present. A successful response may contain a caught error or record an
undispatched request; it is not an acceptance verdict.

| Probe | Surface | SWI | Trealla |
| --- | --- | --- | --- |
| AP-001 | valid-initial / literal | [success; entered](swi-admission-paths.json) | [success; entered](trealla-admission-paths.json) |
| AP-002 | valid-initial / runtime | [error; before entry](swi-admission-paths.json) | [success; entered](trealla-admission-paths.json) |
| AP-003 | missing-start / literal | [success; entered; caught missing_start_option](swi-admission-paths.json) | [success; entered; caught missing_start_option](trealla-admission-paths.json) |
| AP-004 | missing-start / runtime | [error; before entry](swi-admission-paths.json) | [success; entered; caught missing_start_option](trealla-admission-paths.json) |
| AP-005 | dynamic-valid / literal | [success; entered; pattern literal; Reply=ok](swi-admission-paths.json) | [success; entered; pattern literal; Reply=ok](trealla-admission-paths.json) |
| AP-006 | dynamic-valid / runtime | [success; entered; pattern unbound; Matched=yes; Reply=ok](swi-admission-paths.json) | [success; entered; pattern unbound; Matched=yes; Reply=ok](trealla-admission-paths.json) |
| AP-007 | dynamic-invalid / literal | [success; entered; pattern literal; Reply=Reply; caught missing_start_option](swi-admission-paths.json) | [success; entered; pattern literal; Reply=Reply; caught missing_start_option](trealla-admission-paths.json) |
| AP-008 | dynamic-invalid / runtime | [success; entered; pattern unbound; Matched=yes; Reply=Reply; caught missing_start_option](swi-admission-paths.json) | [success; entered; pattern unbound; Matched=yes; Reply=Reply; caught missing_start_option](trealla-admission-paths.json) |
| AP-009 | validation-order / literal | [error; before entry](swi-admission-paths.json) | [success; entered; caught spawn_option error](trealla-admission-paths.json) |
| AP-010 | validation-order / runtime | [success; entered; caught spawn_option error](swi-admission-paths.json) | [success; entered; caught spawn_option error](trealla-admission-paths.json) |

## Evidence and limits

[REPORT.md](REPORT.md) explains the findings, source inspection and limits.
Raw reports contain exact sent command objects and received responses,
including terminal errors, entry-check responses and halt acknowledgements.
No output markers, sleeps, runtime imports or private registry inspection
are used. Entry is checked through an ordinary self-message on the same shell.
The existing required matrices and their failures remain unchanged.
Disposable nodes stopped. The patched Trealla source stayed stable during the run;
installed runtimes and n3/n5 stayed unchanged.
