# Coverage matrix — interoperability baseline 0.1

Recorded 2026-10-21. Status: **scoped draft; known failures remain**. See the
[baseline](../../baselines/0.1.md), [difference register](../../docs/BASELINE_DIFFERENCES.md)
and [reproduction guide](../../docs/BASELINE_RUNNER.md). Counts describe executed
cases, not complete language/profile certification. Links point to raw evidence.

## Required local/server selections

| Pack | Native SWI | Native Trealla | GNU ISOBASE | WASM Worker | WASM main |
|---|---|---|---|---|---|
| isobase-http | [10/10](swi-isobase-http.json) | [8/10; 2 fail](trealla-isobase-http.json) | [10/10](gnu-isobase-http.json) | not applicable | not applicable |
| language-actor | [7/7](swi-language-actor.json) | [7/7](trealla-language-actor.json) | not applicable | [7/7](swi-wasm-worker-language-actor.json) | [7/7](swi-wasm-main-language-actor.json) |
| wire-capabilities | [3/3](swi-wire-capabilities.json) | [3/3](trealla-wire-capabilities.json) | not applicable | not applicable | not applicable |

Browser rows execute the same seven LC assertions in real SWI-WASM engines
under Node with test coordinator plumbing. They are not browser UI/network
or server-wire certification. Native HTTP/ACTOR fixtures use public sandboxed
server routes. GNU advertises ISOBASE and is not tested for actor features.

## Required HTTP interoperability

Rows are callers; columns are HTTP destinations. Each cell covers HC-001
(RPC paging) and HC-002 (promise template/caller independence).

| Caller → peer | SWI | Trealla | GNU |
|---|---|---|---|
| swi | [2/2](swi-interop-http-to-swi.json) | [2/2](swi-interop-http-to-trealla.json) | [2/2](swi-interop-http-to-gnu.json) |
| trealla | [0/2; 2 fail](trealla-interop-http-to-swi.json) | [0/2; 2 fail](trealla-interop-http-to-trealla.json) | [0/2; 2 fail](trealla-interop-http-to-gnu.json) |
| gnu | [2/2](gnu-interop-http-to-swi.json) | [1/2; 1 fail](gnu-interop-http-to-trealla.json) | [2/2](gnu-interop-http-to-gnu.json) |

## Required ACTOR interoperability

Three public cases per direction: remote source/synchronous paging, canonical
asynchronous answers, and unrelated monitor/message preservation. GNU is
outside ACTOR; browser real-network interoperation is not measured here.

| Caller → peer | SWI | Trealla |
|---|---|---|
| swi | [3/3](swi-interop-actor-to-swi.json) | [3/3](swi-interop-actor-to-trealla.json) |
| trealla | [3/3](trealla-interop-actor-to-swi.json) | [3/3](trealla-interop-actor-to-trealla.json) |

## Separately versioned supporting ACTOR contracts

| Suite | SWI | Trealla |
|---|---|---|
| actor-core-0.1 | [7/7](swi-actor-core.json) | [7/7](trealla-actor-core.json) |
| actor-workers-0.1 | [8/8](swi-actor-workers.json) | [8/8](trealla-actor-workers.json) |
| actor-behaviours-0.1 | [10/10](swi-actor-behaviours.json) | [10/10](trealla-actor-behaviours.json) |
| actor-supervisors-0.1 | [8/8](swi-actor-supervisors.json) | [8/8](trealla-actor-supervisors.json) |

These suites retain their own scopes and IDs. Their numeric identity check
does not define the baseline language representation; baseline LC-001 uses
opaque identity. They are not claimed as complete browser-engine tests.

## Required failures — retained without waivers

- **IB-006 — trealla-isobase-http**: ConformanceFailure: expected 'success([a,b],false).', got 'error(error(existence_error(procedure,baseline_q/1),baseline_q/1)).\n' [Raw report](trealla-isobase-http.json).
- **IB-010 — trealla-isobase-http**: ConformanceFailure: expected 'success([ok],false).', got 'error(error(existence_error(procedure,baseline_private/0),baseline_private/0)).\n' [Raw report](trealla-isobase-http.json).
- **HC-001 — trealla-interop-http-to-swi**: ConformanceFailure: expected 'success([[a,b,c]],false).', got 'error(error(existence_error(procedure,rpc/3),rpc/3)).\n' [Raw report](trealla-interop-http-to-swi.json).
- **HC-002 — trealla-interop-http-to-swi**: ConformanceFailure: expected 'success([ok],false).', got 'error(error(existence_error(procedure,promise/4),promise/4)).\n' [Raw report](trealla-interop-http-to-swi.json).
- **HC-001 — trealla-interop-http-to-trealla**: ConformanceFailure: expected 'success([[a,b,c]],false).', got 'error(error(existence_error(procedure,rpc/3),rpc/3)).\n' [Raw report](trealla-interop-http-to-trealla.json).
- **HC-002 — trealla-interop-http-to-trealla**: ConformanceFailure: expected 'success([ok],false).', got 'error(error(existence_error(procedure,promise/4),promise/4)).\n' [Raw report](trealla-interop-http-to-trealla.json).
- **HC-001 — trealla-interop-http-to-gnu**: ConformanceFailure: expected 'success([[a,b,c]],false).', got 'error(error(existence_error(procedure,rpc/3),rpc/3)).\n' [Raw report](trealla-interop-http-to-gnu.json).
- **HC-002 — trealla-interop-http-to-gnu**: ConformanceFailure: expected 'success([ok],false).', got 'error(error(existence_error(procedure,promise/4),promise/4)).\n' [Raw report](trealla-interop-http-to-gnu.json).
- **HC-002 — gnu-interop-http-to-trealla**: ConformanceFailure: expected 'success([ok],false).', got 'error(timeout_or_worker_failure).\n' [Raw report](gnu-interop-http-to-trealla.json).

The failed HTTP source-loading cases remain required failures. The Trealla
HTTP callable context reports `rpc/3` and `promise/4` unavailable even though
its ACTOR paths provide them. GNU → Trealla HC-002 reports a worker timeout;
the unparenthesized operator-goal diagnostic records a related HTTP framing
difference, but this run does not establish a complete causal repair. No
runtime change or expected-failure substitution was made.

## Separate diagnostics and experimental text

| Diagnostic suite | SWI | Trealla | GNU |
|---|---|---|---|
| isobase-diagnostics | [6/6 observed](swi-isobase-diagnostics.json) | [5/6 observed; 1 incomplete](trealla-isobase-diagnostics.json) | [6/6 observed](gnu-isobase-diagnostics.json) |
| supervisor-diagnostics | [4/5; 1 fail](swi-supervisor-diagnostics.json) | [5/5](trealla-supervisor-diagnostics.json) | not applicable |
| worker-diagnostics | [1/1](swi-worker-diagnostics.json) | [1/1](trealla-worker-diagnostics.json) | not applicable |
| portable-text | [0/7; 7 fail](swi-portable-text.json) | [7/7](trealla-portable-text.json) | not applicable |

Diagnostic/experimental counts are excluded from required totals. Existing
SCD-001 preserves the static/runtime-bound nested supervisor admission
difference. A timeout means an observation is incomplete, not a semantic
pass. GNU contract 0.2.0 has additional obligations; these observations do
not waive them or rerun its historical broad/39-probe audit.

## Provenance and coverage limits

[provenance.json](provenance.json) records source revisions, dirty test/doc
paths, configuration, binary hashes, input-file hashes and subprocess exits.
The test-only browser export is the only executable runtime-repository edit.
GNU binaries were already built; no runtime source or installed engine was
repaired or upgraded. Existing N3/N5 processes were left running unchanged.

Not established: full ISO mode coverage, hostile-input/security containment,
all resource bounds, cache-expiry policies, arbitrary source-fetch/network
policies, RELATION, complete ISOTOPE HTTP sessions, remote cancellation or
delegated-lineage cleanup. Receiver wire tests do not replace client-side
fault-injection regressions for every spawn-wait race.

## Execution completeness

| Invocation | Exit | Evidence |
|---|---|---|
| swi-isobase-http | 0 | [report](swi-isobase-http.json) |
| swi-isobase-diagnostics | 0 | [report](swi-isobase-diagnostics.json) |
| trealla-isobase-http | 1 | [report](trealla-isobase-http.json) |
| trealla-isobase-diagnostics | 1 | [report](trealla-isobase-diagnostics.json) |
| gnu-isobase-http | 0 | [report](gnu-isobase-http.json) |
| gnu-isobase-diagnostics | 0 | [report](gnu-isobase-diagnostics.json) |
| swi-language-actor | 0 | [report](swi-language-actor.json) |
| swi-wire-capabilities | 0 | [report](swi-wire-capabilities.json) |
| swi-actor-core | 0 | [report](swi-actor-core.json) |
| swi-actor-workers | 0 | [report](swi-actor-workers.json) |
| swi-actor-behaviours | 0 | [report](swi-actor-behaviours.json) |
| swi-actor-supervisors | 0 | [report](swi-actor-supervisors.json) |
| swi-supervisor-diagnostics | 1 | [report](swi-supervisor-diagnostics.json) |
| swi-worker-diagnostics | 0 | [report](swi-worker-diagnostics.json) |
| swi-portable-text | 1 | [report](swi-portable-text.json) |
| trealla-language-actor | 0 | [report](trealla-language-actor.json) |
| trealla-wire-capabilities | 0 | [report](trealla-wire-capabilities.json) |
| trealla-actor-core | 0 | [report](trealla-actor-core.json) |
| trealla-actor-workers | 0 | [report](trealla-actor-workers.json) |
| trealla-actor-behaviours | 0 | [report](trealla-actor-behaviours.json) |
| trealla-actor-supervisors | 0 | [report](trealla-actor-supervisors.json) |
| trealla-supervisor-diagnostics | 0 | [report](trealla-supervisor-diagnostics.json) |
| trealla-worker-diagnostics | 0 | [report](trealla-worker-diagnostics.json) |
| trealla-portable-text | 0 | [report](trealla-portable-text.json) |
| swi-interop-http-to-swi | 0 | [report](swi-interop-http-to-swi.json) |
| swi-interop-http-to-trealla | 0 | [report](swi-interop-http-to-trealla.json) |
| swi-interop-http-to-gnu | 0 | [report](swi-interop-http-to-gnu.json) |
| swi-interop-actor-to-swi | 0 | [report](swi-interop-actor-to-swi.json) |
| swi-interop-actor-to-trealla | 0 | [report](swi-interop-actor-to-trealla.json) |
| trealla-interop-http-to-swi | 1 | [report](trealla-interop-http-to-swi.json) |
| trealla-interop-http-to-trealla | 1 | [report](trealla-interop-http-to-trealla.json) |
| trealla-interop-http-to-gnu | 1 | [report](trealla-interop-http-to-gnu.json) |
| trealla-interop-actor-to-swi | 0 | [report](trealla-interop-actor-to-swi.json) |
| trealla-interop-actor-to-trealla | 0 | [report](trealla-interop-actor-to-trealla.json) |
| gnu-interop-http-to-swi | 0 | [report](gnu-interop-http-to-swi.json) |
| gnu-interop-http-to-trealla | 1 | [report](gnu-interop-http-to-trealla.json) |
| gnu-interop-http-to-gnu | 0 | [report](gnu-interop-http-to-gnu.json) |
| swi-wasm-worker-language-actor | 0 | [report](swi-wasm-worker-language-actor.json) |
| swi-wasm-main-language-actor | 0 | [report](swi-wasm-main-language-actor.json) |
