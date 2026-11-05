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

The WASM adapter runs each assertion in its own process and loads a manifest's
`source` before its goal. `browser-local-compatibility-0.1` separately tests the
documented browser registration errors and supervisor record format; passing it
does not change results for the native naming and child-specification manifests.

`local_isobase.py --output /fresh/path` runs the unchanged current shared HTTP
packs against disposable native SWI and GNU nodes. It validates demonstrator
setup, gives GNU only the two explicit loopback origins and records schema-2
reports with the runner's normal accounting. The old GNU ISOBASE 0.2 draft is a
separate comparison target; it does not replace the current language manual.

## Draft manual-boundary checks

`local_manual_boundaries.py` runs the same `uri-atoms-0.1` and
`manual-option-sources-0.1` query assertions against explicitly selected local
SWI and Trealla checkouts. An optional GNU worker runs the ISOBASE selection.
Each case has a fresh process and a bounded timeout. The report records source
revisions, dirty-file hashes, executable hashes and contract hashes. These are
standalone API checks; they do not certify public-node admission or transport.

```sh
python3 adapters/local_manual_boundaries.py \
  --swi-root /path/to/swi-prolog-node --swipl /verified/swipl \
  --trealla-root /path/to/trealla-port --tpl /released/trealla/tpl \
  --gnu-worker /path/to/gprolog-port/isobase/query-worker \
  --output /fresh/local-report.json
```

For Worker and main execution, pass the same manifests to `adapters/wasm.cjs`
with a built runtime package and `WP_WASM_SOURCE_DIR` set to its `web/wasm`
directory. Historical packs and release selections retain their old contracts;
these draft packs are opt-in during implementation migration.

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

`adapters/local_retained_context.py` now defaults to all four native route
combinations and exits nonzero for any failed, blocked or errored observation.
Use the [maintained retained-context gate](../profiles/retained-context-0.1.md)
for routine qualification: `runner/context_release.py` additionally requires all
51 original observations plus six controlled producer cases exactly once, every
route and the attachment controls. Pass `--controlled-promises` to the adapter
when running the new cases directly.
Partial `--routes` selections remain diagnostic and cannot satisfy the full gate.
The [original audit](../reports/2026-11-05-native-retained-context/README.md) and
[repair](../reports/2026-11-05-native-retained-context-repair/README.md) remain historical.

`adapters/local_attachment_race.py` tests both attachment orderings on disposable
copies of the committed runtimes. A barrier pauses retirement after its last
attachment decision. Moving retirement outside the lock is a negative control:
the harness must reproduce a successful attachment followed by context closure.
No installed engine, upstream checkout or public node is modified by the adapter.
See the [qualification](../reports/2026-11-05-native-context-attachment-repair/README.md).


`adapters/public_promise_self_route.py` is an explicit public-route diagnostic,
not a local fixture or automatic conformance gate. Pass an authorised `--url`,
a private JSON `--credentials-file` containing an execute-only `token`, and a
fresh `--output` directory. Its fixed default is twenty alternating original and
producer-timestamped attempts. It halts each retained toplevel and preserves a
timeout as a failure even if a separate diagnostic retry recovers. Use
`runner/promise_self_route_analysis.py --report RESULTS --output ANALYSIS` for
phase summaries. Tokens must be provisioned/revoked by the deployment owner;
the adapter neither grants authority nor changes public policy.
See the [N5 diagnostic](../reports/2026-11-05-public-self-route-diagnostic/README.md).


The native standard-library adapter accepts `--manifest` for an explicitly
versioned shared selection. Its default remains historical 0.1; select
`cases/standard-library-0.2.json` for all 146 original/finite mode/error cases.
The browser runner's `LIBRARY_MANIFEST` override selects that same file through
real Chrome Worker/main engines. Exact manifest hashes are part of each report;
[finite-case results](../reports/2026-11-05-library-finite-cases/README.md) are kept
separate from the earlier public 112-case certificate.
