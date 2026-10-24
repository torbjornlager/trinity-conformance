# Selective receive draft 0.1 — 24 October 2026

**12/12 selected assertions pass; 0 failures.**
Identical public-interface goals execute on disposable native ACTOR nodes.
This separate draft does not amend baseline 0.1 or certify arbitrary lifecycle
interleavings. GNU ACTOR, SWI-WASM and remote operation are not measured.

| Case | SWI | Trealla |
| --- | --- | --- |
| SR-001 | [pass](swi-selective-receive.json) | [pass](trealla-selective-receive.json) |
| SR-002 | [pass](swi-selective-receive.json) | [pass](trealla-selective-receive.json) |
| SR-003 | [pass](swi-selective-receive.json) | [pass](trealla-selective-receive.json) |
| SR-004 | [pass](swi-selective-receive.json) | [pass](trealla-selective-receive.json) |
| SR-005 | [pass](swi-selective-receive.json) | [pass](trealla-selective-receive.json) |
| SR-006 | [pass](swi-selective-receive.json) | [pass](trealla-selective-receive.json) |

## Failures

No selected required failure was observed in this run.

## Evidence and limits

See [REPORT.md](REPORT.md) for method, selected contracts and preservation.
[provenance.json](provenance.json) identifies exact source revisions, engine
hashes, commands, node configuration and test input hashes. The SWI source is
the demonstrator manifest pin, loaded from its separate native repository.
Cases use no fixed sleeps, runtime imports or private registry access.
All candidate messages are self-sent before zero-time polls; no sleep is used.
Guards have no external side effects, and cuts are tested inside selected bodies.
Both fixture nodes were stopped; runtime code, installed runtimes and n3/n5
were unchanged. No GUI, TLS, remote-link, resource-limit or general cleanup
certification is claimed.
