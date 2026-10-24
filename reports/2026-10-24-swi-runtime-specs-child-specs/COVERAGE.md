# Supervisor child-specification validation draft 0.1 — 24 October 2026

**12/12 selected assertions pass; 0 failures.**
Identical public-interface goals execute on disposable native ACTOR nodes.
This separate draft does not amend baseline 0.1 or certify arbitrary lifecycle
interleavings. GNU ACTOR, SWI-WASM and remote operation are not measured.

| Case | SWI | Trealla |
| --- | --- | --- |
| SV-001 | [pass](swi-child-specs.json) | [pass](trealla-child-specs.json) |
| SV-002 | [pass](swi-child-specs.json) | [pass](trealla-child-specs.json) |
| SV-003 | [pass](swi-child-specs.json) | [pass](trealla-child-specs.json) |
| SV-004 | [pass](swi-child-specs.json) | [pass](trealla-child-specs.json) |
| SV-005 | [pass](swi-child-specs.json) | [pass](trealla-child-specs.json) |
| SV-006 | [pass](swi-child-specs.json) | [pass](trealla-child-specs.json) |

## Failures

No selected required failure was observed in this run.

## Evidence and limits

See [REPORT.md](REPORT.md) for method, selected contracts and preservation.
[provenance.json](provenance.json) identifies exact source revisions, engine
hashes, commands, node configuration and test input hashes. The SWI source is
the demonstrator manifest pin, loaded from its separate native repository.
Cases use no fixed sleeps, runtime imports or private registry access.
Specifications arrive as ordinary messages, selecting runtime validation.
Existing admission-path diagnostics remain separate and unresolved.
Both fixture nodes stopped. The SWI working-tree candidate contains the repair
under test; its files stayed stable during execution. The dependency pin,
installed runtimes and n3/n5 were unchanged. No GUI, TLS, remote-link, resource-limit or general cleanup
certification is claimed.
