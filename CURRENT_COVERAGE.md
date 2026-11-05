# Current Web Prolog conformance coverage

Updated **5 November 2026**. The [Appendix B source-unit matrix](docs/APPENDIX_B_COVERAGE.md)
and its [machine-readable ledger](requirements/appendix-b-0.1.json) now provide
requirement-level accounting. This first inventory has 353 manuscript source
units, including related prose groups and signatures. Earlier test selections
still need full clause mapping; these unit counts are not a conformance percentage.

The [cluster peer-policy release](reports/2026-11-05-cluster-peer-policy/README.md)
is committed, pushed and deployed to N0–N6. All twelve runtime/asset services run
consumer image revision `1581acc`, with unchanged qualified runtime pins.
N3/N4 now permit N5; N5 now permits N3. All **51 public context checks pass,
with no policy exclusions**. External spawn/source destinations remain denied
in six controls. All 38 consumer CI groups qualify after a complete WASM rerun;
the initial browser failure and one intermediate N5 context timeout remain recorded.
The report distinguishes successful reruns from unresolved intermittent behavior.
N5's persistent self-route credential remains owner-only and mounted read-only.

The [previous native context release](reports/2026-11-05-native-context-release/README.md)
retains its historical `3c8702a` image record, 2,421 selected public checks and
nine policy exclusions. Broader library and browser selections were not repeated
for this policy-only change; their dated evidence is retained.

The [previous standard-library release](reports/2026-11-05-standard-library-release/README.md)
retains its historical `1b04f27` image record, 36-group CI and 2,379 public checks.
Its required forms and callback semantics remain covered by the new live selection.

The required library forms and described semantics work across all five runtime
modes. Library callback errors require exact callable types and original culprits
at invocation, with lazy unused callbacks and unchanged application exceptions.
The final Trealla repair also preserves this behaviour inside nested meta-calls.
The report retains the initial failed nested probe and the repeated final gates.
Full external ISO mode/error coverage and complete lifetime/transport clause mapping
remain open; these checks do not certify the complete language.

The [native retained-context audit](reports/2026-11-05-native-retained-context/README.md)
retains its original **31 passing, nine failing and 11 blocked** observations.
The subsequent [development repair](reports/2026-11-05-native-retained-context-repair/README.md)
passes **all 51 probes**, including previously blocked native and mixed-runtime
routes. Context identity now survives remote return while separate clients remain
isolated. Fresh authenticated HTTP requests have distinct promise owners;
Trealla ordinary names are scoped to their client context. SWI exposes cleanup,
and Trealla exports public language goals. New upstream tests exercise attachment
closure, late replay, immutable bindings and narrowed transport authority.
These are scoped development results. Repaired source units return to unverified
pending complete obligation mapping; the following release records public promotion.

The [attachment repair qualification](reports/2026-11-05-native-context-attachment-repair/README.md)
adds atomic last-attachment retirement on both native runtimes. Four deterministic
positive checks cover both orderings; two negative controls reproduce the old
race on disposable copies. All 51 context probes pass on committed native sources.
N5 outgoing credential-file support, read-only Compose overlays and exact consumer
pins are committed. All 38 consumer CI groups, seven browser package groups, the
full native suite and the clean Trealla unit/interoperability run pass. Source
qualification is complete for this selection; the public release is recorded above.

The [preceding runtime repair release](reports/2026-11-05-public-runtime-repair-release/README.md)
records the earlier localhost, remote output and N5–N4 ping-pong fixes. The
[standard-library development snapshot](reports/2026-11-05-standard-library/README.md)
retains the original 57-case baseline and 65-case qualification, with its own
historical manifests and scope.

The [preceding promise release](reports/2026-11-05-public-promise-release/README.md)
records the full browser package qualification, 34 earlier consumer CI groups
and its separate 132-check live selection. The [localhost development
record](reports/2026-11-05-localhost-rpc/README.md) is historical evidence before
promotion. Counts from different selections are not added together.

The earlier [4 November release](reports/2026-11-04-appendix-b-public-deployment/README.md)
retains its separate 456-assertion transport/creation/supervisor selection.
Those counts are not added to the new release's live checks.

The [introspection audit](reports/2026-11-04-runtime-introspection/README.md)
and [promise repair evidence](reports/2026-11-05-promise-context/README.md)
record development findings before promotion. The browser ownership failure is
resolved; the required GNU library forms are deployed, while
full ISO mode/error coverage and full clause mapping remain open.
Native retained-context propagation passes its scoped repair selection; complete
lifetime/transport coverage remains open after the scoped public promotion. GNU ISOBASE is
not required to provide ACTOR APIs.

The checkpoint below is historical. Its N5 SSO topology, revisions and case
counts do not describe the latest public deployment; its evidence remains intact.

# Historical 1 November checkpoint

Updated **1 November 2026**. The deployed ACTOR selection passes **44/44 on
N3, N4 and N5 (132/132)**. The isolated release checkpoint passes **44/44 per
engine (88/88)**. The latest demonstrator CI also passes both jobs.

These are distinct evidence selections. The live metadata/source check below
confirms which node configurations are running; it does not repeat the case
executions. Older broad matrices and diagnostics retain their original dates
and source pins in the [historical evidence index](#historical-and-broader-evidence).

## Deployed nodes

The [read-only state check](reports/2026-11-01-coverage-state-refresh/state.json)
on 1 November confirms N1–N4 public metadata, N5's SSO boundary and the live
N3/N4/N5 source hashes. The [deployed case report](reports/2026-11-01-public-native-reliability/REPORT.txt)
records the 44-case selection on each ACTOR node earlier the same day.

| Node | Running surface | Latest selected evidence |
|---|---|---|
| N1 | Public ISOBASE | `/node_info` returns 200 and advertises `isobase`. No fresh N1 conformance run in this update. |
| N2 | Public ISOTOPE | `/node_info` returns 200 and advertises `isotope`. No fresh N2 conformance run in this update. |
| N3 | Public ACTOR, SWI-Prolog 10.1.19 | [44/44 pass over public WSS](reports/2026-11-01-public-native-reliability/observations/n3-public/results.json), using separate anonymous connections with connection-scoped ownership. |
| N4 | Public ACTOR, SWI-Prolog 10.1.19 | [44/44 pass over public WSS](reports/2026-11-01-public-native-reliability/observations/n4-public/results.json), with the same client model. |
| N5 | SSO-protected ACTOR, Trealla 3.14.20 | [44/44 pass on the deployed backend](reports/2026-11-01-public-native-reliability/observations/n5-execution-only/results.json), using two distinct execution-only identities. A separate authenticated public-browser query passes four committed-exit conditions. |

N3/N4 retain the images deployed from native SWI `91d5c52`. All **72 runtime
Prolog files** checked in each container match both the accepted release source
`7405ebb` and the latest native revision `ce5aa98`; the intervening changes are
test-only. N5's **204 tracked Prolog files** match deployed Trealla `2ebaeb9`.
The state record identifies exact revisions, image identities, engine versions
and source-manifest hashes. N5 is healthy; unauthenticated public `node_info`
still redirects to SSO sign-in.

The N5 44-case result concerns the actual deployed backend, reached by a helper
in its network namespace. It is not 44 public-proxy executions. The separate
public-browser check uses an existing owner session; authority-denial assertions
use the execution-only clients, whose temporary credentials were revoked.
See the [deployment summary](reports/2026-11-01-public-native-reliability/SUMMARY.json)
for the access paths and counts.

## Scoped ACTOR release checkpoint

[`actor-release-0.2`](profiles/actor-release-0.2.json) requires all expected case
IDs exactly once, all passing. Missing, duplicate, unsupported or failed cases
and nonzero runner exits cannot satisfy the gate. It comprises eight packs:

| Pack | Native SWI | Native Trealla | Selected boundary |
|---|---|---|---|
| actor-core 0.1 | [7/7](reports/2026-11-01-native-reliability/observations/accepted-final/swi/actor-core-0.1.json) | [7/7](reports/2026-11-01-native-reliability/observations/accepted-final/trealla/actor-core-0.1.json) | Actor search and message interaction |
| selective-receive 0.1 | [6/6](reports/2026-11-01-native-reliability/observations/accepted-final/swi/selective-receive-0.1.json) | [6/6](reports/2026-11-01-native-reliability/observations/accepted-final/trealla/selective-receive-0.1.json) | Matching, guard commitment, rollback and body cut scope |
| links-monitors 0.1 | [6/6](reports/2026-11-01-native-reliability/observations/accepted-final/swi/links-monitors-0.1.json) | [6/6](reports/2026-11-01-native-reliability/observations/accepted-final/trealla/links-monitors-0.1.json) | Links, monitor events and termination |
| copying-isolation 0.1 | [6/6](reports/2026-11-01-native-reliability/observations/accepted-final/swi/copying-isolation-0.1.json) | [6/6](reports/2026-11-01-native-reliability/observations/accepted-final/trealla/copying-isolation-0.1.json) | Variable sharing, private source and isolation |
| source-copying 0.1 | [5/5](reports/2026-11-01-native-reliability/observations/accepted-final/swi/source-copying-0.1.json) | [5/5](reports/2026-11-01-native-reliability/observations/accepted-final/trealla/source-copying-0.1.json) | Copied primitive/named guards, inline/named workers and timeout callbacks |
| toplevel-waits 0.1 | [6/6](reports/2026-11-01-native-reliability/observations/accepted-final/swi/toplevel-waits-0.1.json) | [6/6](reports/2026-11-01-native-reliability/observations/accepted-final/trealla/toplevel-waits-0.1.json) | Caller targeting, timeout, late replies and unrelated traffic |
| ownership-lifecycle 0.1 | [4/4](reports/2026-11-01-native-reliability/observations/accepted-final/swi/ownership-lifecycle-0.1.json) | [4/4](reports/2026-11-01-native-reliability/observations/accepted-final/trealla/ownership-lifecycle-0.1.json) | Foreign exit denial/target survival, owner exit and socket-loss child/grandchild cascades |
| committed-exit 0.1 | [4/4](reports/2026-11-01-native-reliability/observations/accepted-final/swi/committed-exit-0.1.json) | [4/4](reports/2026-11-01-native-reliability/observations/accepted-final/trealla/committed-exit-0.1.json) | Caught control cannot resume receive or timeout callbacks; ordinary exception control |
| **Total** | **44/44** | **44/44** | **88 case executions** |

This isolated checkpoint uses SWI **7405ebb / 10.1.19** and Trealla
**2ebaeb9 / 3.14.20**, in disposable private ARM64 loopback fixtures with two
distinct execution-only principals. Its
[provenance](reports/2026-11-01-native-reliability/observations/accepted-final/provenance.json)
and [environment](reports/2026-11-01-native-reliability/environment.json)
identify exact source, executable and suite-input hashes. The deployment driver
uses the same 44 case IDs in separately authorised live fixtures; the release
wrapper itself remains restricted to disposable fixtures.

The earlier 40-case `actor-release-0.1` remains explicitly selectable. The
single-pack runner default remains backward compatible. Neither is the current
44-case release selection.

## Implementation and browser checks

Both complete native scripts pass in the
[1 November reliability checkpoint](reports/2026-11-01-native-reliability/REPORT.txt).
Two native before/after regressions and **250 passing Trealla invocations**
(WebSocket 200, demonitor 20, isolation 10, sandbox 10, synchronous waits 10)
accompany it. These repetitions do not increase the 44-case feature coverage
or estimate race probabilities. The shared committed-exit cases also pass on
the older public sandbox path; the native regressions are the negative controls
for the underlying runtime repair.

The latest [demonstrator CI run](https://github.com/torbjornlager/trinity-demonstrator/actions/runs/41303605424)
passes **all 37 main check groups and the separate WASM job**, using demonstrator
`84992b5`, native SWI `ce5aa98` and browser package `f9dfc66`. It includes native
and integration tiers, browser equivalence, implementation WASM checks and
consumer regressions. See the [CI selection record](reports/2026-11-01-coverage-state-refresh/ci.json).
The native revision and browser schema-provenance update change tests/metadata,
not runtime or schema bytes. CI success is not evidence that those repository
heads were redeployed, nor a shared 44-case browser conformance result.

## Historical and broader evidence

The following selections remain useful outside the current 44-case gate.
Their reports identify older sources, engines and fixture policies; they are
not reruns of today's deployed configurations. All original failures and
intermediate observations remain unchanged. The
[previous detailed roll-up](https://github.com/torbjornlager/trinity-conformance/blob/533e5677265899ad26bdd73a0541d495a9956ffc/CURRENT_COVERAGE.md)
retains the per-pack/per-direction links and chronological diagnostic ledger.

| Area | Dated evidence and scope |
|---|---|
| Broad native ACTOR/ISOBASE, worker/behaviour/supervisor packs and ACTOR interoperability | [23 October matrix](reports/2026-10-23-receive-handoff-acceptance/COVERAGE.md), on its SWI 10.1.18 / Trealla 3.14.8 candidate configurations. Packs outside the eight current release packs retain this older evidence. |
| GNU ISOBASE and two WASM language modes | [21 October all-node matrix](reports/2026-10-21-gnu-request-framing/COVERAGE.md): GNU 10/10 selected HTTP cases; each real WASM engine 7/7 selected language cases under Node. These are not fresh GNU deployment or browser-UI attestations. |
| HTTP caller/peer interoperability and promise/yield | [25 October URI close-out](reports/2026-10-25-uri-closeout/REPORT.md): native HC selections and 24/24 promise/yield executions. Directions involving GNU retain the older 21 October peers. |
| Local server waits, naming, creation and child specifications | [24 October server waits](reports/2026-10-24-server-waits/COVERAGE.md), [naming](reports/2026-10-24-local-naming/COVERAGE.md), [creation](reports/2026-10-24-swi-spawn-source-creation-validation/COVERAGE.md), [child specs](reports/2026-10-24-swi-spawn-source-child-specs/COVERAGE.md). Not included in the 44-case release gate. |
| Character-list text, Unicode and browser UI | [26 October four-mode checkpoint](reports/2026-10-26-text-migration-checkpoint/COVERAGE.md): SWI 26/26; Trealla 22/26 with escaped JSON and 26/26 with literal UTF-8 JSON; each browser mode 32 passed assertions/controls and three URI/CORS diagnostics. The controls overlap; the experimental text contract is not promoted by the ACTOR gate. |
| Cyclic answers and actor output | [25 October cyclic-answer repair](reports/2026-10-25-cyclic-answer-rejection/COVERAGE.md) and [write/output checks](reports/2026-10-25-write-output/COVERAGE.md). These are focused candidate results with their own representation and engine limits. |
| Ownership/lifecycle boundary experiments | [31 October follow-up](reports/2026-10-31-ownership-lifecycle/REPORT.md), separate from the later release and deployment selections. |

A historical failed diagnostic is not relabelled as a current defect or a pass
without rerunning that assertion on an identified configuration. Later green
implementation suites do not silently replace a different historical case ID.

## Coverage limits and maintenance

- The 44-case gate covers selected ACTOR contracts, not the whole language.
  Counts are case executions, not predicate inventories or unique features.
- N1/N2's live profile metadata is not a fresh ISOBASE/ISOTOPE conformance run.
  No full current GNU, RELATION or ISOTOPE shared suite is established here.
- Browser implementation CI and the four N5 public-browser conditions do not
  establish complete browser-network, UI or end-to-end cross-engine coverage.
- General hostile-input/TLS/credential isolation, whitelist containment,
  arbitrary network partitions, deadline accuracy under load, resource bounds,
  remote namespace races and exhaustive shutdown schedules remain outside the
  selected evidence. Public actor absence does not prove host-thread termination.
- Do not sum historical, isolated, deployed, CI and repeated-run counts as
  independent feature coverage. Exact sources, policy, transport, case IDs and
  executable hashes are part of each result's identity.

For updates, verify the relevant reports and live source correspondence, state
which interface and principal model were tested, and supersede only the same
selected assertions. Retain dated records and clearly identify surfaces not
rerun. See the [runner instructions](docs/BASELINE_RUNNER.md) and
[baseline difference register](docs/BASELINE_DIFFERENCES.md).
