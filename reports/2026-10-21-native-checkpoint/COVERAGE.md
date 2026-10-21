# Native conformance checkpoint — 21 October 2026

**All 60 selected required cases and 66 supporting ACTOR assertions passed** on the configured disposable native fixtures. Separate diagnostics and experimental results below remain unresolved. This is a scoped checkpoint, not full language, security or lifecycle certification.

Runtime sources were clean and committed before execution:

- Native SWI: `88d5732c428cb3d4e47b7ae49c2762ee01233503`, SWI-Prolog 10.1.17.
- Native Trealla: `96f2badea97892c947d427b3aa9ba2cde8ee8760`, pinned Trealla v3.13.10 with its matching library.
- Shared test definitions: conformance commit `5265e6613dbe618bd2f6af8037a966145ff74a03`; no manifests or assertions changed.

GNU and both SWI-WASM engines were **not rerun**. Their [previous matrix](../2026-10-21-baseline-0.1/COVERAGE.md) remains historical evidence, not a pass claim for this checkpoint.

## Required native selections

| Pack | SWI | Trealla |
|---|---|---|
| isobase-http | [10 pass / 10](swi-isobase-http.json) | [10 pass / 10](trealla-isobase-http.json) |
| language-actor | [7 pass / 7](swi-language-actor.json) | [7 pass / 7](trealla-language-actor.json) |
| wire-capabilities | [3 pass / 3](swi-wire-capabilities.json) | [3 pass / 3](trealla-wire-capabilities.json) |

## Required HTTP interoperability

Rows are callers; columns are destinations.

| Caller → peer | SWI | Trealla |
|---|---|---|
| swi | [2 pass / 2](swi-interop-http-to-swi.json) | [2 pass / 2](swi-interop-http-to-trealla.json) |
| trealla | [2 pass / 2](trealla-interop-http-to-swi.json) | [2 pass / 2](trealla-interop-http-to-trealla.json) |

## Required ACTOR interoperability

Rows are callers; columns are destinations.

| Caller → peer | SWI | Trealla |
|---|---|---|
| swi | [3 pass / 3](swi-interop-actor-to-swi.json) | [3 pass / 3](swi-interop-actor-to-trealla.json) |
| trealla | [3 pass / 3](trealla-interop-actor-to-swi.json) | [3 pass / 3](trealla-interop-actor-to-trealla.json) |

ACTOR cases cover remote source/synchronous paging and spawn monitoring, canonical asynchronous terms, and preservation of unrelated messages/monitors. The richer Unicode, exception and literal `'$VAR'/1` vectors also run in the implementation interoperability group below.

## Separately versioned supporting ACTOR contracts

| Suite | SWI | Trealla |
|---|---|---|
| actor-core-0.1 | [7 pass / 7](swi-actor-core.json) | [7 pass / 7](trealla-actor-core.json) |
| actor-workers-0.1 | [8 pass / 8](swi-actor-workers.json) | [8 pass / 8](trealla-actor-workers.json) |
| actor-behaviours-0.1 | [10 pass / 10](swi-actor-behaviours.json) | [10 pass / 10](trealla-actor-behaviours.json) |
| actor-supervisors-0.1 | [8 pass / 8](swi-actor-supervisors.json) | [8 pass / 8](trealla-actor-supervisors.json) |

All 66 supporting assertions passed. These retain their existing scopes and IDs; they do not certify the entire ACTOR profile.

## Native implementation interoperability runner

The committed Trealla `tools/test.sh interop` completed **69 invocation groups**, exit 0, in 100.48 seconds. This is not an additional 69-case language conformance count. [Complete log](native-interop.log), [exit/configuration](native-interop.json).

This includes native SWI/Trealla transport, header/hello canonical negotiation, Unicode exact answers, synchronous calls, sources, monitors, naming, statecharts, delegated lineages, ownership, and HTTP client/server checks. Browser terminal/correlation wire fixtures run as part of this native suite; actual browser runtimes and UI were not rerun.

**Retained diagnostic:** during `Trealla statechart invocation -> Trealla`, the log prints `Error: syntax error, start of rule expected, $trealla_actor_1000000146:1`. That invocation subsequently reports its assertions passed, and the runner exits 0. This checkpoint does not classify or fix the parser message, or treat a zero exit as evidence that it disappeared. Existing Trealla parser investigations remain separate.

## Separate diagnostics and experimental text

| Pack | SWI | Trealla |
|---|---|---|
| isobase-diagnostics | [6 observed / 6](swi-isobase-diagnostics.json) | [5 observed, 1 incomplete / 6](trealla-isobase-diagnostics.json) |
| supervisor-diagnostics | [4 pass, 1 fail / 5](swi-supervisor-diagnostics.json) | [5 pass / 5](trealla-supervisor-diagnostics.json) |
| worker-diagnostics | [1 pass / 1](swi-worker-diagnostics.json) | [1 pass / 1](trealla-worker-diagnostics.json) |
| portable-text | [7 fail / 7](swi-portable-text.json) | [7 pass / 7](trealla-portable-text.json) |

- **SCD-001, SWI:** runtime-bound nested child-specification admission returns `instantiation_error`; Trealla accepts this form. The diagnostic remains a raw failed observation, excluded from required/supporting totals.
- **IBD-006, Trealla:** the unparenthesized HTTP operator-goal diagnostic times out after ten seconds. Five other ISOBASE diagnostic observations were obtained. The timeout remains incomplete evidence, not a semantic pass.
- **Experimental Portable Text:** SWI passes 0/7; Trealla passes 7/7. This experimental character-list contract is not promoted into ACTOR requirements.
- Worker stress observations passed on both engines; they do not prove the absence of intermittent races. The earlier rare `creation_race` remains unresolved and its 6,000-iteration investigation was not repeated here.

## Peer authentication and the initial fixture rejection

The first run used open disposable nodes without outbound peer credentials. SWI public queries now carry delegated-lineage metadata when spawning remotely; Trealla correctly rejected IX-001–003 with `permission_error(use,transport_lineage,...)`. These three failures remain in the [initial report](initial-uncredentialed/swi-interop-actor-to-trealla.json) and its [provenance](initial-uncredentialed/provenance.json). They were not waived, relabelled as unsupported, or edited into passes.

The final matrix above comes from a fresh run with explicitly configured test-peer authentication: a fixture bearer token grants only `execute` and `internal_transport` on the disposable Trealla node, and an endpoint-specific SWI transport-options hook sends it. See [peer_transport_fixture.pl](peer_transport_fixture.pl). The token is public test data, not a deployed credential. Anonymous clients gain no lineage authority; the committed interoperability group independently checks their rejection.

This is configuration of new local fixtures, not a relaxation of the runtime boundary or a change to existing N3/N5 policies. All thirty shared reports were rerun after configuring peer trust. Initial and final reports are retained separately.

## Reproduction, provenance and limits

[provenance.json](provenance.json) records launch commands, all thirty report commands, fixture settings, revisions, manifest/runner hashes, engine hashes and tracked-runtime-tree hashes before/after. Both runtime checkouts remained clean; tracked files and engine hashes were unchanged. Existing N3/N5 processes were not restarted. Installed engines, runtime code and book examples were not changed.

Use the existing [runner instructions](../../docs/BASELINE_RUNNER.md), pairing the Trealla executable with its adjacent library. Native public-query interoperability requires explicitly configured peer trust for delegated-lineage metadata; an open execution endpoint alone does not grant that authority. The existing all-node launcher does not configure this extra peer credential automatically.

The thirty final reports and thirty initial reports passed schema and count validation using `runner/validate_reports.py`. No assertions, timeouts or expected results were changed to obtain the final matrix. All reported failures outside required/supporting scopes remain explicit.

Not established: complete language/profile compliance, malformed negotiated-answer validation, hostile-input security, arbitrary network/resource policies, multi-hop delegated cleanup, remote cancellation, cache expiry, portable strings, GNU ISO mode coverage or browser UI/network conformance.

## Execution accounting

| Invocation | Scope | Exit | Evidence |
|---|---|---|---|
| trealla-isobase-http | required | 0 | [report](trealla-isobase-http.json), [log](trealla-isobase-http.log) |
| trealla-isobase-diagnostics | diagnostic | 1 | [report](trealla-isobase-diagnostics.json), [log](trealla-isobase-diagnostics.log) |
| trealla-language-actor | required | 0 | [report](trealla-language-actor.json), [log](trealla-language-actor.log) |
| trealla-wire-capabilities | required | 0 | [report](trealla-wire-capabilities.json), [log](trealla-wire-capabilities.log) |
| trealla-actor-core | supporting | 0 | [report](trealla-actor-core.json), [log](trealla-actor-core.log) |
| trealla-actor-workers | supporting | 0 | [report](trealla-actor-workers.json), [log](trealla-actor-workers.log) |
| trealla-actor-behaviours | supporting | 0 | [report](trealla-actor-behaviours.json), [log](trealla-actor-behaviours.log) |
| trealla-actor-supervisors | supporting | 0 | [report](trealla-actor-supervisors.json), [log](trealla-actor-supervisors.log) |
| trealla-supervisor-diagnostics | diagnostic | 0 | [report](trealla-supervisor-diagnostics.json), [log](trealla-supervisor-diagnostics.log) |
| trealla-worker-diagnostics | diagnostic | 0 | [report](trealla-worker-diagnostics.json), [log](trealla-worker-diagnostics.log) |
| trealla-portable-text | experimental | 0 | [report](trealla-portable-text.json), [log](trealla-portable-text.log) |
| swi-isobase-http | required | 0 | [report](swi-isobase-http.json), [log](swi-isobase-http.log) |
| swi-isobase-diagnostics | diagnostic | 0 | [report](swi-isobase-diagnostics.json), [log](swi-isobase-diagnostics.log) |
| swi-language-actor | required | 0 | [report](swi-language-actor.json), [log](swi-language-actor.log) |
| swi-wire-capabilities | required | 0 | [report](swi-wire-capabilities.json), [log](swi-wire-capabilities.log) |
| swi-actor-core | supporting | 0 | [report](swi-actor-core.json), [log](swi-actor-core.log) |
| swi-actor-workers | supporting | 0 | [report](swi-actor-workers.json), [log](swi-actor-workers.log) |
| swi-actor-behaviours | supporting | 0 | [report](swi-actor-behaviours.json), [log](swi-actor-behaviours.log) |
| swi-actor-supervisors | supporting | 0 | [report](swi-actor-supervisors.json), [log](swi-actor-supervisors.log) |
| swi-supervisor-diagnostics | diagnostic | 1 | [report](swi-supervisor-diagnostics.json), [log](swi-supervisor-diagnostics.log) |
| swi-worker-diagnostics | diagnostic | 0 | [report](swi-worker-diagnostics.json), [log](swi-worker-diagnostics.log) |
| swi-portable-text | experimental | 1 | [report](swi-portable-text.json), [log](swi-portable-text.log) |
| trealla-interop-http-to-trealla | required | 0 | [report](trealla-interop-http-to-trealla.json), [log](trealla-interop-http-to-trealla.log) |
| trealla-interop-actor-to-trealla | required | 0 | [report](trealla-interop-actor-to-trealla.json), [log](trealla-interop-actor-to-trealla.log) |
| trealla-interop-http-to-swi | required | 0 | [report](trealla-interop-http-to-swi.json), [log](trealla-interop-http-to-swi.log) |
| trealla-interop-actor-to-swi | required | 0 | [report](trealla-interop-actor-to-swi.json), [log](trealla-interop-actor-to-swi.log) |
| swi-interop-http-to-trealla | required | 0 | [report](swi-interop-http-to-trealla.json), [log](swi-interop-http-to-trealla.log) |
| swi-interop-actor-to-trealla | required | 0 | [report](swi-interop-actor-to-trealla.json), [log](swi-interop-actor-to-trealla.log) |
| swi-interop-http-to-swi | required | 0 | [report](swi-interop-http-to-swi.json), [log](swi-interop-http-to-swi.log) |
| swi-interop-actor-to-swi | required | 0 | [report](swi-interop-actor-to-swi.json), [log](swi-interop-actor-to-swi.log) |
