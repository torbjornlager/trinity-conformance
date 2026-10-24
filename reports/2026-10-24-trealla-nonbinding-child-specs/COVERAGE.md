# Supervisor child-specification validation draft 0.1 — 24 October 2026

**7/12 selected assertions pass; 5 failures.**
Identical public-interface goals execute on disposable native ACTOR nodes.
This separate draft does not amend baseline 0.1 or certify arbitrary lifecycle
interleavings. GNU ACTOR, SWI-WASM and remote operation are not measured.

| Case | SWI | Trealla |
| --- | --- | --- |
| SV-001 | [fail](swi-child-specs.json) | [pass](trealla-child-specs.json) |
| SV-002 | [fail](swi-child-specs.json) | [pass](trealla-child-specs.json) |
| SV-003 | [fail](swi-child-specs.json) | [pass](trealla-child-specs.json) |
| SV-004 | [fail](swi-child-specs.json) | [pass](trealla-child-specs.json) |
| SV-005 | [fail](swi-child-specs.json) | [pass](trealla-child-specs.json) |
| SV-006 | [pass](swi-child-specs.json) | [pass](trealla-child-specs.json) |

## Failures

- **swi / SV-001**: ConformanceFailure: expected success, got {'data': 'Arguments are not sufficiently instantiated', 'details': 'error(instantiation_error,_)', 'type': 'error'}; preceding events were []
- **swi / SV-002**: ConformanceFailure: expected success, got {'data': 'Arguments are not sufficiently instantiated', 'details': 'error(instantiation_error,_)', 'type': 'error'}; preceding events were []
- **swi / SV-003**: ConformanceFailure: expected success, got {'data': 'Arguments are not sufficiently instantiated', 'details': 'error(instantiation_error,_)', 'type': 'error'}; preceding events were []
- **swi / SV-004**: ConformanceFailure: expected success, got {'data': 'Arguments are not sufficiently instantiated', 'details': 'error(instantiation_error,_)', 'type': 'error'}; preceding events were []
- **swi / SV-005**: ConformanceFailure: expected success, got {'data': 'Arguments are not sufficiently instantiated', 'details': 'error(instantiation_error,_)', 'type': 'error'}; preceding events were []

## Evidence and limits

See [REPORT.md](REPORT.md) for method, selected contracts and preservation.
[provenance.json](provenance.json) identifies exact source revisions, engine
hashes, commands, node configuration and test input hashes. The SWI source is
the demonstrator manifest pin, loaded from its separate native repository.
Cases use no fixed sleeps, runtime imports or private registry access.
Specifications arrive as ordinary messages, selecting runtime validation.
Existing admission-path diagnostics remain separate and unresolved.
Both fixture nodes were stopped. The Trealla candidate includes the repair under
test; its source hashes stayed stable during execution. Installed runtimes and
n3/n5 were unchanged. No GUI, TLS, remote-link, resource-limit or general cleanup
certification is claimed.
