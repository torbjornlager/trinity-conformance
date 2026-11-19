# Common ACTOR naming alignment — 19 November 2026

Ordinary actor names now have one [client-context contract](../../profiles/client-naming-0.1.md):
independent clients can use identical names without seeing, removing or blocking
each other's registrations. Local descendants and toplevels on one retained
connection share the namespace. Explicitly published services retain their
independent node-wide registry and existing publication authority.

**Trealla candidate code is aligned and verified locally; it is not committed,
pushed or deployed.** SWI, ECLiPSe and browser implementations needed no naming
code changes for this selection. Live Trealla still runs its previous release.
The earlier SWI cleanup API candidate remains a separate change.

## Shared observations

The same eight [manifest cases](../../cases/client-naming-0.1.json) drive native
and public WebSocket sessions and real Chromium browser sessions. Independent
clients intentionally use equal credentials (anonymous identity for these runs).
No assertion, error expectation or deadline was weakened between candidates.

| Configuration | Result | Boundary |
|---|---|---|
| Native SWI 11.0.0, candidate source | 8/8 | Two independent loopback WebSockets |
| Native Trealla 3.14.20, patched source | 8/8 | Same |
| Live ECLiPSe N7 | 8/8 | Public isolated WebSockets; every session start paced by 5 seconds |
| Packaged SWI-WASM Worker | 7 pass / 1 unsupported | Independent browser pages/coordinators |
| Packaged SWI-WASM main | 7 pass / 1 unsupported | Same |
| Original Trealla source, regression control | 1 pass / 7 fail | Same native goals; only same-connection sharing passes |
| Original single-client local-naming pack | 12/12 | Six cases on SWI and patched Trealla |

CN-001–006 and CN-008 check hidden lookup, independent duplicate names, foreign
unregister, named sends/monitors, inherited names and independent disconnection.
CN-007 checks two toplevels on one retained connection. The browser session API
does not expose that operation; its two unsupported rows remain explicit and
its strict adapter exits nonzero. There is no claim that one browser coordinator
hosts multiple network clients. These are 38 passing executions and two unsupported
operations in the shared selection, not 40 independent features or a full ACTOR
qualification.

The browser package remains `0363b38b3d4939a53f62a57b23fbc4e73997e79f`, with
SWI-Prolog 10.1.19 / swipl-wasm 8.2.5. Browser engine/runtime files and ECLiPSe
services were not changed. The results establish the tested name-scope behavior;
other browser naming error-formal/liveness findings in the full report remain
outside this selection. Retained HTTP session naming and public service
provisioning are also outside these black-box checks.

## Trealla implementation

`actors.pl` stores ordinary bindings with their client namespace. Its
context-aware lookup is shared by `whereis/2`, named sends, named monitors and
PID-name collision checks. Startup reservation collisions use the reservation's
owning namespace. Publication, rollback, unregister and context retirement retain
the namespace key, so an identical name/PID in another context is preserved.

When an actor actually dies, cleanup enumerates aliases for that exact PID across
all contexts. Observed remote retirement similarly removes only exact target
aliases, preserving same-named bindings to different PIDs. The separate
`registered_service/2` registry is unchanged. Trusted standalone callers retain
their shared ordinary namespace; public clients need published services for
intentional discovery across context boundaries.

Native namespace regression tests now exercise cross-context lookup, duplicate
registration, foreign unregister, independent pending reservations, same-PID
aliases across contexts, exact remote alias withdrawal, service visibility,
repeated teardown, late admission and publication during source preparation.
The receiver-lineage component test now queries surviving names in their owning
lineage instead of assuming node-wide visibility. Its lifecycle assertions are
retained. The SWI wire interoperability test likewise queries each owning
lineage, checks that unrelated observers see no names, and checks that a fresh
connection using the same token starts with an empty namespace and can reuse
the names. Native spawn-time monitors and explicit lineage-close notifications
remain required; the native close-while-paged condition is preserved. The original Trealla regression control confirms the new pack detects
the former behavior rather than merely accepting both models.

## Native regression validation

The maintained Trealla runner passes **106 unit groups and 69 interoperability
groups**, with no skipped groups, using the verified Trealla 3.14.20 and SWI
11.0.0 engines. Frozen unit and interoperability input hashes remain unchanged
within each run. The focused updated wire/native lineage check passes too.
All **114 conformance-runner tests pass** on Node 22. Native service visibility,
reservation isolation, alias retirement and teardown checks pass. Deliberate
connection/probe closures produce some expected diagnostics in the broad logs;
these results use the maintained runner's exit status and explicit pass markers,
not a claim that stderr is empty.

The owned lab was removed after exporting the results. Baseline persistent
Compose container and image identities remain unchanged. Candidate source
changes remain uncommitted and undeployed.

## Relation to the context gate

The unchanged 61-row retained-context selection records **45 pass / 12 fail /
4 blocked / 0 error**. The previous repair batch recorded 42/15/4/0.
Trealla CTX-006/007/008 now pass without changing those assertions.
The remaining HTTP-principal, remote promise/round-trip and obsolete attachment
instrumentation findings remain separate open work. This naming decision does
not restore an older remote delegation model or revise promise ownership.

The [full run](../2026-11-19-deployed-conformance/REPORT.md) and
[first repair batch](../2026-11-19-conformance-repairs/REPORT.md) remain unchanged
historical records. Their original failures have not been relabeled.

## Reproduction and evidence

Use the commands in [the profile](../../profiles/client-naming-0.1.md).
[Observations](observations), [provenance](provenance.json),
[verification](verification.json), [service preservation](preservation.json) and
[export hashes](files-sha256.json) identify source inputs and validation results.
The private artifact directory is
`trinity-demonstrator/.trinity/conformance-naming-20261119`.

Broad native tests run in an owned, network-isolated Linux Docker lab using the
same Trealla/GNU/SWI image inputs as the preceding full run. Updated source and
public test-support files were copied into that lab; installed engines, release
pins, live configuration and quotas were unchanged. ECLiPSe checks used only the
authorized public test sessions and unique ordinary names.

Initial broad-test attempts lacked copied test-support files or a sibling SWI
checkout path; those failures are retained privately. The final lab includes
those public fixtures and the expected sibling path. Its readiness tool is a
small Python equivalent of the runner's only netcat operation, `nc -z HOST PORT`.
An additional cross-client monitor probe did not receive its expected actor
termination notification within five seconds after socket closure. Those failed
observations remain in the private focused-lineage logs; their cause is not
resolved here. This naming selection makes no general end-to-end no-orphan
claim. Component connection cleanup and the explicit lineage-close checks are
separate evidence.

An initial browser attempt omitted UTF-8 response/document metadata, corrupting
the main engine's embedded WASM payload. Explicit UTF-8 metadata, matching the
maintained browser adapters, restores main-mode startup; the initial attempt is
archived separately as a fixture error.
