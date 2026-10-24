# Local creation-option validation draft 0.1 — 24 October 2026

**12/12 selected assertions pass; 0 failures.**
Identical public-interface goals execute on disposable native ACTOR nodes.
This separate draft does not amend baseline 0.1 or certify arbitrary lifecycle
interleavings. GNU ACTOR, SWI-WASM and remote operation are not measured.

| Case | SWI | Trealla |
| --- | --- | --- |
| CV-001 | [pass](swi-creation-validation.json) | [pass](trealla-creation-validation.json) |
| CV-002 | [pass](swi-creation-validation.json) | [pass](trealla-creation-validation.json) |
| CV-003 | [pass](swi-creation-validation.json) | [pass](trealla-creation-validation.json) |
| CV-004 | [pass](swi-creation-validation.json) | [pass](trealla-creation-validation.json) |
| CV-005 | [pass](swi-creation-validation.json) | [pass](trealla-creation-validation.json) |
| CV-006 | [pass](swi-creation-validation.json) | [pass](trealla-creation-validation.json) |

## Failures

No selected required failure was observed in this run.

## Evidence and limits

See [REPORT.md](REPORT.md) for method, selected contracts and preservation.
[provenance.json](provenance.json) identifies exact source revisions, engine
hashes, commands, node configuration and test input hashes. The SWI source is
the demonstrator manifest pin, loaded from its separate native repository.
Cases use no fixed sleeps, runtime imports or private registry access.
Formal error terms are checked without implementation-specific contexts.
Valid creation and exact termination acknowledgements bound startup checks.
This selection uses runtime-supplied option lists. The separate initial
literal-option run retains unresolved admission-path failures; see REPORT.md.
Both fixture nodes were stopped. The Trealla candidate includes the repair under
test; its source hashes stayed stable during execution. Installed runtimes and
n3/n5 were unchanged. No GUI, TLS, remote-link, resource-limit or general cleanup
certification is claimed.
