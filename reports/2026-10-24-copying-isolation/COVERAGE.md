# Actor copying and private-source isolation draft 0.1 — 24 October 2026

**12/12 selected assertions pass; 0 failures.**
Identical public-interface goals execute on disposable native ACTOR nodes.
This separate draft does not amend baseline 0.1 or certify arbitrary lifecycle
interleavings. GNU ACTOR, SWI-WASM and remote operation are not measured.

| Case | SWI | Trealla |
| --- | --- | --- |
| CI-001 | [pass](swi-copying-isolation.json) | [pass](trealla-copying-isolation.json) |
| CI-002 | [pass](swi-copying-isolation.json) | [pass](trealla-copying-isolation.json) |
| CI-003 | [pass](swi-copying-isolation.json) | [pass](trealla-copying-isolation.json) |
| CI-004 | [pass](swi-copying-isolation.json) | [pass](trealla-copying-isolation.json) |
| CI-005 | [pass](swi-copying-isolation.json) | [pass](trealla-copying-isolation.json) |
| CI-006 | [pass](swi-copying-isolation.json) | [pass](trealla-copying-isolation.json) |

## Failures

No selected required failure was observed in this run.

## Evidence and limits

See [REPORT.md](REPORT.md) for method, selected contracts and preservation.
[provenance.json](provenance.json) identifies exact source revisions, engine
hashes, commands, node configuration and test input hashes. The SWI source is
the demonstrator manifest pin, loaded from its separate native repository.
Cases use no fixed sleeps, runtime imports or private registry access.
Child observations and release messages establish copying/isolation barriers.
Minimal dynamic declarations enable the selected private-database mutation.
Both fixture nodes were stopped; runtime code, installed runtimes and n3/n5
were unchanged. No GUI, TLS, remote-link, resource-limit or general cleanup
certification is claimed.
