# Local naming and registration draft 0.1 — 24 October 2026

**12/12 selected assertions pass; 0 failures.**
Identical public-interface goals execute on disposable native ACTOR nodes.
This separate draft does not amend baseline 0.1 or certify arbitrary lifecycle
interleavings. GNU ACTOR, SWI-WASM and remote operation are not measured.

| Case | SWI | Trealla |
| --- | --- | --- |
| LN-001 | [pass](swi-local-naming.json) | [pass](trealla-local-naming.json) |
| LN-002 | [pass](swi-local-naming.json) | [pass](trealla-local-naming.json) |
| LN-003 | [pass](swi-local-naming.json) | [pass](trealla-local-naming.json) |
| LN-004 | [pass](swi-local-naming.json) | [pass](trealla-local-naming.json) |
| LN-005 | [pass](swi-local-naming.json) | [pass](trealla-local-naming.json) |
| LN-006 | [pass](swi-local-naming.json) | [pass](trealla-local-naming.json) |

## Failures

No selected required failure was observed in this run.

## Evidence and limits

See [REPORT.md](REPORT.md) for method, selected contracts and preservation.
[provenance.json](provenance.json) identifies exact source revisions, engine
hashes, commands, node configuration and test input hashes. The SWI source is
the demonstrator manifest pin, loaded from its separate native repository.
Cases use no fixed sleeps, runtime imports or private registry access.
Actors acknowledge named routing and terminate only on explicit stop messages.
Exact termination notifications precede stale-pid and name-reuse checks.
Both fixture nodes were stopped; runtime code, installed runtimes and n3/n5
were unchanged. No GUI, TLS, remote-link, resource-limit or general cleanup
certification is claimed.
