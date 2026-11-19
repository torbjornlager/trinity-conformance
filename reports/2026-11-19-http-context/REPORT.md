# HTTP client-context follow-up — 19 November 2026

The earlier connection-cleanup harness repair and report are now pushed:
Trealla `7946acd` and conformance `c2ae55c`. This follow-up investigates the next
HTTP and remote context boundaries on owned, network-isolated Linux fixtures.
No live node, installed engine, consumer pin or trust setting changed.

## HTTP findings and candidate repair

| Boundary | SWI | Trealla baseline | Trealla candidate |
|---|---|---|---|
| Fresh anonymous HTTP request | Separate request owner | Separate request owner | Unchanged |
| Fresh authenticated HTTP request | Principal-wide promise sharing, explicitly documented | Separate request owner | Unchanged |
| Separate retained HTTP sessions, equal credentials | Promise isolation | Shares trusted-local promise store | Isolated session namespaces |
| Later request to the same retained session | Owner can collect | Owner can collect, subject to foreign interference | Owner can collect; foreign cleanup cannot interfere |

The [fresh-request baseline](default-mode-compatibility.json) retains the
SWI CTX-010 failure against the older isolation expectation. This is a documented
contract mismatch, not an accidental implementation regression. Choosing fresh
request isolation would deliberately change SWI's current contract; that choice
is pending. No such SWI change is included in this patch.

Trealla's retained HTTP sessions exposed a separate implementation gap. Their
actors had no client namespace, so promise ownership fell back to trusted-local
sharing. The [candidate patch](trealla.patch) gives each session an
`isotope_session/1` namespace, inherited by local children. Language names and
promises use it, while HTTP route authentication still uses the principal.
Session retirement removes ordinary registrations and disposes of that
namespace's promises. Closed namespaces reject registration and promise creation.
Admin authority remains an explicit property of the session principal; public
sessions do not gain it from sharing a credential.

The change belongs upstream in `trealla-port`. Optional HTTP session routes are
enabled only on the disposable test fixture; deployment configuration is
unchanged. The runtime patch, regression and documentation remain uncommitted.
The SWI fixture uses `dc93b05`, including the earlier public promise-cleanup API
repair; the demonstrator's pinned SWI source remains unchanged.

## Verification

The new [HTTP session selection](../../profiles/http-session-context-0.1.md)
uses an acknowledged producer-arrival barrier. While its answer is held, a
foreign session must receive an unknown-reference error; its cleanup must not
dispose of the owner's reference. The owner then observes pending status and
collects after release. Exactly one producer request is allowed. A separate
Trealla case checks name lookup, duplicate names and withdrawal across sessions.

- Final [session observations](sessions.json): **3/3 pass**, exact versioned
  inventory verified; adapter exit 0.
- [Unchanged Trealla control](sessions-baseline.json): SWI's check passes;
  both Trealla checks fail, adapter exit 1. The tests detect the original gap.
- All **69 interoperability groups pass**, including both connection-cleanup
  modes from the preceding repair.
- The **114 conformance runner tests pass** using Node 22.23.4. An initial
  invocation used the host's Node 10 and failed three existing WASM adapter
  tests because `Object.fromEntries` is unavailable; no code change was needed.
- Unit coverage records **106 passes and one timeout out of 107 groups**.
  The standard runner stopped at cache-cleanup group 47 after 30 seconds.
  An isolated candidate run and an unchanged-source baseline also exceeded
  that same deadline. The other 60 groups ran through a private tail of the
  unchanged runner at the original bounds and passed. This is not an all-green
  full-unit result. Failed observations remain retained.
- The final HTTP session unit regression passes after checking namespace
  isolation, retained owner access, disposal of queue/worker/timer resources,
  preserved neighboring names, and rejected creation/registration after closure.
  Its final added closed-creation assertion was checked separately after the
  broad run; runtime implementation inputs did not change.
- Default adapter mode still produces the same **22 pass / 1 fail** inventory
  when remote routes are omitted. Existing context manifests and expectations
  remain unchanged.

An [initial four-row probe](initial-http-actor-scope-probe.json) also submitted
actor name operations to SWI's HTTP route. SWI correctly rejected them at its
ISOTOPE ceiling. That failed probe is retained; it is not relabeled as a naming
pass. The three-case selection explicitly limits its HTTP ACTOR name extension
to Trealla. Shared ACTOR naming remains qualified on the WebSocket surface.

## Remote context investigation

The [fresh original context run](context-baseline.json), without the six
controlled-producer cases or the attachment gate, records **42 pass / 9 fail /
4 blocked** across 55 observations. It is a baseline, not a new release gate.

SWI-origin round trips return actual results but cannot see the origin's names
or collect its promises. The origin namespace is not restored. Trealla-origin
return probes fail to produce a result and remain blocked; a timeout alone does
not establish the exact source-export or return-path cause. Trealla-origin
remote sibling checks separately show foreign promise collection, consistent
with Trealla's documented lack of outbound per-client lineage propagation.

The [separate remote-context design](../../profiles/remote-client-context-design.md)
sets the next implementation order: per-client outbound delegation first,
explicit return-phase controls second, then a deliberate choice about context
resumption. Matching an existing lineage token on a new connection must never
silently grant access to an origin context. This follow-up changes no remote
runtime behavior or old CTX-016/017 expectations.

## Reproduction and provenance

Use the command in the [HTTP profile](../../profiles/http-session-context-0.1.md)
with SWI 11.0.0, Trealla 3.14.20 and its matching library. The fixture used image
`sha256:93daa029dbdabb5777fc72cbcd6afdcc2593e54ea5ce65286ce34e0aeb2ebe2d`.
Source revisions, runtime-file hashes, selection counts and known limits are in
[the summary](SUMMARY.json). Raw observations identify their own source and
adapter hashes; [export hashes](files-sha256.json) cover this record.

The [adapter patch](adapter.patch) adds an explicit HTTP-only selection; default
retained-context behavior is preserved. The [Trealla patch](trealla.patch)
applies to `7946acd` and includes its new unit regression. Runtime test commands
retain the standard 30-second bound:

```sh
TPL=/opt/trealla/tpl SWIPL=/usr/bin/swipl TEST_PORT_BASE=26060 ./tools/test.sh unit
TPL=/opt/trealla/tpl SWIPL=/usr/bin/swipl TEST_PORT_BASE=28060 ./tools/test.sh interop
```

Logs in this directory retain the standard unit failure, subsequent tail,
isolated/baseline cache probes, focused session check and interoperability
result. Private inputs, cloned-source bundles, initial probes and fixture logs
remain under `trinity-demonstrator/.trinity/http-context-20261119`. The initial
unit and interoperability suites ran concurrently; the isolated cache probe
also timed out after the interoperability suite had finished. No deadline was
enlarged and no failed observation was reclassified as a pass.
