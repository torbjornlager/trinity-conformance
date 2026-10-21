# Candidate adapters

The conformance cases should share their assertions and expected outcomes.
Adapters should contain only the minimum implementation-specific mechanics
needed to launch and stop a candidate or invoke a portable local API.

The anticipated adapters are:

- `swi` — start the SWI-Prolog reference node
- `trealla` — start the native Trealla node
- `external` — test an already-running node from its base URL

Candidate configuration will eventually need at least:

- advertised profile
- HTTP base URL
- WebSocket endpoint
- startup command, when managed by the runner
- readiness probe
- authentication material, where required
- shutdown command or process handle

Wire-level cases should prefer the `external` adapter so that a new
implementation does not require changes to the conformance logic.

## Current adapter

`runner/run.py` implements the first `external` adapter directly. It accepts a
WebSocket URL, optional bearer token, optional Origin header, advertised
profile, and timeout. Candidate process management remains deliberately out
of scope: CI or a developer starts the node, waits for readiness, invokes the
runner, and then stops the node.

## Bounded baseline adapters

`local_baseline.py` starts isolated loopback SWI, Trealla and GNU nodes with
explicit fixture configuration, grants GNU only the test origins, captures
provenance and cleans up its processes. It does not restart N3/N5.
`wasm.cjs` imports the runtime repository's test-only engine setup and runs the
same LC goal manifest in Worker/main modes. The coordinator is a test fixture;
no browser server or real-network certification is inferred. See
[the runner guide](../docs/BASELINE_RUNNER.md).
