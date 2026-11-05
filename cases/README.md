# Conformance cases

[`actor-core-0.1.json`](actor-core-0.1.json) is the first executable case
manifest. Each entry has a stable ID, an observable requirement category, and
source-test provenance. `runner/run.py` maps those IDs to black-box protocol
procedures.

[`portable-text-0.1.json`](portable-text-0.1.json) is an independent opt-in
draft. Its `TXT-*` cases specify double-quoted text as a list of one-character
atoms in submitted goals, loaded source, DCGs, list operations, Unicode text,
and serialized-term round trips. The initial runner reaches those semantics
through an ACTOR session; this does not make the draft an implicit requirement
of every node already advertising `actor`.

[`portable-text-0.2.json`](portable-text-0.2.json) expands that experiment to 26
cases. It specifies Unicode scalar values without normalization and distinguishes
textual source reading from preservation of constructed `src_list/1` terms.
Additional boundaries include option and input readers, URI/private/copied/DCG
source, serialization and HTTP peers. See [draft 0.2](../profiles/portable-text-0.2.md)
for coverage limits and [the runner](../runner/portable_text.py) for the public
protocol procedures. A full run requires explicit `--peer` and `--source-base`
fixtures; a selected local subset does not. Version 0.1 remains unchanged.

The remaining extraction backlog is grouped by the minimum advertised
profile.

[`actor-behaviours-0.1.json`](actor-behaviours-0.1.json) is an opt-in,
black-box generic-server and supervisor suite. Its cases consolidate portable
semantics from the implementation-specific SWI and Trealla unit suites while
leaving runtime internals and implementation workarounds in their home
repositories.

[`demonstrator-tutorials-0.1.json`](demonstrator-tutorials-0.1.json) contains
topology-dependent regressions extracted from the published tutorials. These
are black-box browser-protocol tests, but they are not profile requirements:
for example, `DEMO-019` intentionally contacts the demonstrator's N3 and N4.

## RELATION

- accepted advertised relation
- conjunction of advertised relations
- rejection of an unadvertised relation
- rejection of source loading and non-relational goals

## ISOBASE

- successful `/call` with template bindings
- multiple solutions and finite paging
- `once=true`
- logical failure
- goal exception
- malformed goal text
- Prolog and JSON response formats
- stable public `/node_info` profile metadata

## ISOTOPE

- session spawn and ownership
- call, next, and final-page signalling
- stop followed by session reuse
- abort of a running goal
- halt and lifecycle notification
- output delivery
- prompt/respond input round trip
- source loading and persistence across calls

## ACTOR

- remote spawn and normal completion notification
- one-way send driving a remote receive
- explicit exit reason propagation
- monitor and demonitor semantics
- bidirectional actor-message routing
- links and multiple monitors
- inherited terminal output and acknowledged delivery
- inherited prompt/respond input
- connection loss, cleanup, and reconnect behaviour

Before implementation, each remaining item must receive a stable ID and an
exact wire or API contract. Existing implementation tests are evidence for
defining the contract, not the contract itself.

## Worker combinators

[`actor-workers-0.1.json`](actor-workers-0.1.json) is a separate draft public-interface
profile with eight stable `WC-*` cases. The assertions and fixtures are identical
for SWI and Trealla. See [its contract](../profiles/actor-workers-0.1.md) for the
covered ordering, determinism and cleanup guarantees and the explicit exclusions.

[`worker-diagnostics-0.1.json`](worker-diagnostics-0.1.json) is exploratory;
`WCD-001` probes previously observed cleanup ownership errors. Its results are
reported separately and are not used to claim or deny the worker profile.

## Baseline 0.1 selections

The [machine-readable index](../baselines/0.1.json) distinguishes required,
supporting and diagnostic packs. New required packs are `isobase-http-0.1`,
`language-actor-0.1`, `interop-http-0.1`, `interop-actor-0.1` and
`wire-capabilities-0.1`. `isobase-diagnostics-0.1` records unresolved observations.
Their stable IDs map to the [baseline contract](../baselines/0.1.md); the new
runner accepts HTTP or WebSocket endpoints. Existing suites and their IDs are
preserved, not silently merged into a claim that every node implements ACTOR.

## Ownership and lifecycle across clients

The draft [ownership/lifecycle pack](../profiles/ownership-lifecycle-0.1.md)
exercises submitted-goal termination authority, explicit owner termination
controls and independent monitor delivery after socket closure, including a
computing grandchild. It requires a disposable private fixture and two
execution-only principals; see the profile for provisioning and runner flags.
The original links/monitors pack and historical reports are unchanged.

The required draft `source-copying-0.1.json` tests five local ACTOR source-copy
boundaries through `runner/baseline.py`: primitive guard restoration (SCOPY-001),
named guard control (002), an inline nondeterministic worker with its own copied
generator (003), named worker control (004), and preservation of receive option
lists/timeout callbacks (005). The pacing cases install a worker monitor before
requesting stop, wait for normal worker termination, then release the controller.
Root-level assertion timeouts and session teardown bound failed fixtures.
The pack is required by `profiles/actor-release-0.1.json` together with the
separate authenticated ownership/lifecycle pack.

## Manual-boundary migration

The draft `uri-atoms-0.1.json` requires URI atoms and exact Boolean errors at
RPC/promise and source-URI boundaries. The ACTOR draft
`manual-option-sources-0.1.json` adds actor-address node validation, nonbinding
policy validation, duplicate handling and preservation of all clauses across
mixed source kinds. Both reflect the Appendix B decisions of 2026-11-04 and
are supporting checks, without changing historical baseline or release packs.
The local API adapter is documented in [the adapter guide](../adapters/README.md).

The optional `supervisor-common-0.1.json` pack checks common supervisor inspection
and count formats, atom IDs, respawn results, preparation admission, and halt
after child shutdown. Select it with
`local_manual_boundaries.py --suite supervisor-common-0.1`, or pass the manifest
to `wasm.cjs` for Worker/main execution. These are supporting API checks; they
do not certify public-node transport or full Appendix B conformance.

The optional `statechart-document-0.1.json` pack checks that exactly one XML
source is required, before fetching or actor creation. The separate
`adapters/local_statechart_documents.py` runner uses disposable SWI/Trealla
nodes and a loopback document server to verify caller fetching with destination
source access disabled, and document-base preservation for later relative
fetches. It records the exact fetch paths and source/executable hashes. Example:

```sh
python3 adapters/local_statechart_documents.py \
  --swi-root /path/to/swi-prolog-node --swipl /verified/swipl \
  --trealla-root /path/to/trealla-port --tpl /released/trealla/tpl \
  --output /fresh/directory/live-documents.json
```

Browser semantic checks exercise the generated public APIs and real WASM
engines with mocked document transport in main and Worker modes. These remain
supporting checks rather than release or full-protocol certification.

The optional `rpc-timeout-0.1.json` pack checks numeric execution/HTTP limits,
nonbinding validation and rejection before source work. Use `--suite
rpc-timeout-0.1` with the local API adapter, or pass the manifest to `wasm.cjs`.
`adapters/local_rpc_timeouts.py` additionally runs disposable HTTP peers and
SWI/Trealla/GNU execution nodes. It checks execution requests and owner caps,
whole-request transport deadlines (including slow headers/body/drip), per-page
renewal, independent source fetching, error terms, retry and stream cleanup.
Pass `--swi-root`, `--trealla-root`, `--gnu-root`, `--swipl`, `--tpl`, and a fresh
`--output` path. These are supporting checks, with exact source and executable
provenance, rather than release certification.

The optional `http-transport-options-0.1.json` pack checks the closed HTTP option
schema, nonbinding validation of every duplicate, malformed text and fields,
reserved proxy fields, and validation before dispatch. It runs with
`--suite http-transport-options-0.1` in `local_manual_boundaries.py` or through
`wasm.cjs` in either browser mode. The public schema is shared; caller policy
(including forbidden browser fields and the GNU destination allowlist) still applies.

`adapters/local_http_transport_options.py` uses a disposable HTTP peer to capture
actual SWI, Trealla and GNU requests. It checks atom/string/character-list values,
UTF-8 header bytes and Basic credentials, Basic/Bearer RPC and promise requests,
case-insensitive first-field precedence across aliases and pages, empty values,
explicit query-owner retention, and separation from URI source fetching. Pass
`--swi-root`, `--trealla-root`, `--gnu-root`, `--swipl`, `--tpl`, and a fresh
`--output` path. Browser semantic tests additionally check the real WASM public
APIs and Fetch options with mocked transport in main and Worker modes. Broker
handler and TLS tests are local supporting checks; they do not certify Linux
worker containment or a deployed worker/broker pair.

Creation validation now follows Appendix B formal errors: Boolean atoms outside
the permitted domain raise `domain_error(boolean,Value)`, while non-atoms
raise `type_error(atom,Value)`. The initial supervisor-failure check requires
a wrapped caller exception, an unbound output and completed sibling rollback
before checking the surviving conflicting actor. The earlier asynchronous
startup-notification expectation is superseded by that common contract.

`runtime-introspection-0.1.json` checks the five language capabilities, Boolean
values, portable isolation values, enumeration and failed matching. It accepts
host differences in capability values. Use the local API adapter's explicit
`--suite runtime-introspection-0.1` selection or `wasm.cjs` in either mode.
`appendix-library-probes-0.1.json` is a separate supporting availability check;
its GNU failures remain visible and do not become introspection failures.
The opt-in `adapters/wasm_promise_context.cjs` scenario
`appendix_promise_context_parent_child` repeats the original context-wide
lookup diagnostic using real parent/child WASM actors and a mocked HTTP answer.
It passes on the 5 November development repair. Upstream runtime tests now also
include coordinator claim controls and real Chrome/HTTP ownership/lifetime
checks in both execution modes; see `reports/2026-11-05-promise-context/README.md`.
The requirement ledger and renderer are linked from `docs/APPENDIX_B_COVERAGE.md`.


The draft `local-node-rpc-0.1.json` pack checks the retained `localhost`
destination through stateless HTTP calls: paging, RPC/promise source isolation,
goal/template sharing, caller-fetched URI source and failure/error answers.
For URI cases, `--peer` must serve `local_node_loaded(one). local_node_loaded(two).`
at its root. The existing `runner/baseline.py` runs the HTTP pack. The explicit
`adapters/local_node_rpc.py` adapter starts disposable SWI, Trealla and GNU
listeners and a source fixture; it records source and executable hashes. It
never changes a live node or owner egress policy. The [5 November development
repair evidence](../reports/2026-11-05-localhost-rpc/README.md) also covers the
actual contained GNU broker path and the reported N2-source example.


`standard-library-0.1.json` supplies 112 common goals and one private-source
fixture for the Appendix B list/index, integer, iteration and solution-processing
forms. `adapters/local_standard_library.py` runs fresh SWI/Trealla/GNU HTTP
workers and retained SWI/Trealla sessions, recording runtime source and binary
hashes. The upstream browser real-session runner accepts the same file through
`LIBRARY_MANIFEST`; upstream fixture copies must remain byte-identical.
[The development repair](../reports/2026-11-05-standard-library/README.md) retains
the earlier baseline. [The public release](../reports/2026-11-05-standard-library-release/README.md)
records exact callback errors, the nested Trealla follow-up and deployed pins. This selection does not
expand every external ISO mode or error refinement into a complete contract.
