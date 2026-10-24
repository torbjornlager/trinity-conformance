# Generic-server waits draft 0.1 — 24 October 2026

**12/12 selected assertions pass; 0 failures.**
Identical public-interface goals execute on disposable native ACTOR nodes.
This separate draft does not amend baseline 0.1 or certify arbitrary lifecycle
interleavings. GNU ACTOR, SWI-WASM and remote operation are not measured.

| Case | SWI | Trealla |
| --- | --- | --- |
| SW-001 | [pass](swi-server-waits.json) | [pass](trealla-server-waits.json) |
| SW-002 | [pass](swi-server-waits.json) | [pass](trealla-server-waits.json) |
| SW-003 | [pass](swi-server-waits.json) | [pass](trealla-server-waits.json) |
| SW-004 | [pass](swi-server-waits.json) | [pass](trealla-server-waits.json) |
| SW-005 | [pass](swi-server-waits.json) | [pass](trealla-server-waits.json) |
| SW-006 | [pass](swi-server-waits.json) | [pass](trealla-server-waits.json) |

## Failures

No selected required failure was observed in this run.

## Evidence and limits

See [REPORT.md](REPORT.md) for method, selected contracts and preservation.
[provenance.json](provenance.json) identifies exact source revisions, engine
hashes, commands, node configuration and test input hashes. The SWI source is
the demonstrator manifest pin, loaded from its separate native repository.
Cases use no fixed sleeps, runtime imports or private registry access.
Server callbacks announce acceptance and await explicit release/crash messages.
A barrier request establishes reply readiness before mismatch/poll checks.
Both fixture nodes were stopped; runtime code, installed runtimes and n3/n5
were unchanged. No GUI, TLS, remote-link, resource-limit or general cleanup
certification is claimed.
