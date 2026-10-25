# Current Web Prolog conformance coverage

Consolidated on **25 October 2026**, from committed evidence through
`826d694` in trinity-conformance plus the explicit URI close-out and experimental-text follow-ups
below. This is the latest recorded result for each
selected area, **not a single rerun of today's runtime heads or deployed nodes**.
All selected required and supporting assertions below pass in their cited runs.
Diagnostic failures, incomplete observations and experimental differences remain
separate. Passing a finite pack does not certify the whole Web Prolog language.

The matrix uses committed reports plus the explicitly labelled B25 Boolean and U25 URI
close-outs and the E25 experimental-text follow-up. Unrelated uncommitted acceptance staging material is
excluded; the most recent committed broad native checkpoint is 23 October.
Later narrow results supersede only their corresponding selections. E25 runs
the new experimental pack on disposable archived sources with unchanged readers;
it supersedes no required-profile result. This consolidation changes no runtime,
dependency pin, installed engine or live n3/n5 process.

## Reading the evidence

Each result links to a raw report. Counts are executed case selections, not
predicate inventories, unique language features or proof of race freedom.
**Unmeasured** means no assertion was selected for that surface; **outside
profile** means GNU ISOBASE has no ACTOR obligation here; **not applicable** means
the tested browser engine is not an HTTP/ACTOR server. None means pass.
Do not sum these tables: the HTTP selections recur in several batches and the
packs have overlapping subject matter and different tested configurations.

| Evidence | Tested configuration and scope | Exact provenance |
|---|---|---|
| B23: broad native, 23 Oct | SWI 10.1.18 separate core build containing 09b6299; Trealla 3.14.8 plus candidate receive-handoff primitive. Native sources f218370 / cf26bd0. Not a v3.14.10 or current-head rerun. | [Provenance](reports/2026-10-23-receive-handoff-acceptance/provenance.json), [matrix](reports/2026-10-23-receive-handoff-acceptance/COVERAGE.md) |
| G21: all-node follow-up, 21 Oct | GNU 1.6.0 with request-framing working-tree repair over b529b3c; SWI 10.1.17 and Trealla 3.13.10 peers. Both real SWI-WASM engines execute language cases under Node, not a browser UI. | [Provenance](reports/2026-10-21-gnu-request-framing/provenance.json), [matrix](reports/2026-10-21-gnu-request-framing/COVERAGE.md) |
| P24: promise callback follow-up, 24 Oct | SWI native source pin f316e65; Trealla 3.14.10 with callback-context candidate over fe94735. Separate SWI 10.1.18 core plus HTTP shutdown candidate. | [Provenance](reports/2026-10-24-promise-callback-context/provenance.json), [report](reports/2026-10-24-promise-callback-context/REPORT.md) |
| L24: six local packs, 24 Oct | SWI pin f316e65; Trealla source d4e96a3 with unmodified 3.14.10 and matching library. Separate verified SWI 10.1.18 core plus HTTP shutdown candidate. | Each linked pack has its own provenance.json and REPORT.md. |
| S24: spawn/admission follow-up, 24 Oct | SWI working-tree repair over 8c90a4d, subsequently committed as 786737f; Trealla source 7220bb5 with unmodified 3.14.10. Pin f316e65 was not promoted. | [Provenance](reports/2026-10-24-swi-spawn-source-admission-probes/provenance.json), [report](reports/2026-10-24-swi-spawn-source-admission-probes/REPORT.md) |
| B24: Boolean compatibility follow-up, 24 Oct | SWI Boolean working-tree repair over 786737f; Trealla Boolean working-tree repair over 7220bb5. Separate verified SWI 10.1.18 and unmodified Trealla 3.14.10; pin unchanged. Shared pack is unchanged. | [Provenance](reports/2026-10-24-boolean-toplevel-waits/provenance.json), [report](reports/2026-10-24-boolean-toplevel-waits/REPORT.md) |
| U24: URI compatibility follow-up, 24 Oct | SWI URI/Boolean working tree over 786737f and Trealla URI/Boolean working tree over 7220bb5. Same separate engines; pin unchanged. | [Provenance](reports/2026-10-24-uri-promise-http/provenance.json), [matrix](reports/2026-10-24-uri-promise-http/COVERAGE.md) |
| B25: Boolean close-out, 25 Oct | Boolean-only source over SWI 412e5b5 / Trealla 6fb21f1, subsequently committed as 4703f49 / df6698d. Separate verified SWI 10.1.18 and unmodified Trealla 3.14.10; two unchanged toplevel-wait selections. | [Provenance](reports/2026-10-25-boolean-closeout/checks/shared/provenance.json), [report](reports/2026-10-25-boolean-closeout/REPORT.md) |
| U25: URI close-out, 25 Oct | URI source candidates over separately committed Boolean sources 4703f49 / df6698d, using the same separate engines. Four promise/yield and four HTTP caller/peer selections. No deployment/pin update. | [Provenance](reports/2026-10-25-uri-closeout/checks/shared/provenance.json), [report](reports/2026-10-25-uri-closeout/REPORT.md) |
| E25: experimental portable-text 0.2, 25 Oct | Archived committed SWI 786737f and Trealla 7220bb5; pending runtime changes excluded. Same separate engines, unchanged reader defaults, opposite implementation as HTTP peer. Not a deployed or portable-text-configured rerun. | [Provenance](reports/2026-10-25-portable-text-0.2/provenance.json), [matrix](reports/2026-10-25-portable-text-0.2/COVERAGE.md) |

Source revisions, working-tree patches, binary/library hashes and fixture policy
are part of the identity; version strings alone are insufficient. L24 denotes
links/monitors, server waits, selective receive, toplevel waits, local naming and
copying/isolation. Toplevel waits now use the later B25 close-out; creation and
child-spec validation use S24.

L24 per-run provenance: [links/monitors](reports/2026-10-24-links-monitors/provenance.json),
[server waits](reports/2026-10-24-server-waits/provenance.json),
[selective receive](reports/2026-10-24-selective-receive/provenance.json),
[toplevel waits](reports/2026-10-24-toplevel-waits/provenance.json),
[naming](reports/2026-10-24-local-naming/provenance.json),
[copying/isolation](reports/2026-10-24-copying-isolation/provenance.json).
S24 validation provenance: [creation](reports/2026-10-24-swi-spawn-source-creation-validation/provenance.json)
and [child specs](reports/2026-10-24-swi-spawn-source-child-specs/provenance.json).

## Baseline local and server selections

| Pack | Native SWI | Native Trealla | GNU ISOBASE | WASM Worker | WASM main | Evidence |
|---|---|---|---|---|---|---|
| ISOBASE HTTP | [10/10 pass](reports/2026-10-23-receive-handoff-acceptance/swi-isobase-http.json) | [10/10 pass](reports/2026-10-23-receive-handoff-acceptance/trealla-isobase-http.json) | [10/10 pass](reports/2026-10-21-gnu-request-framing/gnu-isobase-http.json) | not applicable | not applicable | B23 / G21 |
| ACTOR language | [7/7 pass](reports/2026-10-23-receive-handoff-acceptance/swi-language-actor.json) | [7/7 pass](reports/2026-10-23-receive-handoff-acceptance/trealla-language-actor.json) | outside profile | [7/7 pass](reports/2026-10-21-gnu-request-framing/swi-wasm-worker-language-actor.json) | [7/7 pass](reports/2026-10-21-gnu-request-framing/swi-wasm-main-language-actor.json) | B23 / G21 |
| Server wire capabilities | [3/3 pass](reports/2026-10-23-receive-handoff-acceptance/swi-wire-capabilities.json) | [3/3 pass](reports/2026-10-23-receive-handoff-acceptance/trealla-wire-capabilities.json) | outside profile | not applicable | not applicable | B23 |

The seven WASM language cases are actual engine runs with coordinator plumbing.
They do not cover browser network calls, terminal UI, Worker scheduling or the
new native-only local packs. GNU's ten HTTP cases are a subset of its separate
ISOBASE contract, not a complete ISO audit.

## HTTP interoperability

Rows are callers; columns are HTTP destinations. Each cell covers HC-001 paging
and HC-002 promise template sharing/caller independence. Native-only cells use
U25, later than B23; every direction involving GNU retains G21 evidence and its
older peer implementations. No GNU-to-current-native compatibility is inferred.

| Caller → peer | SWI | Trealla | GNU |
|---|---|---|---|
| swi | [2/2 pass](reports/2026-10-25-uri-closeout/checks/shared/swi-interop-http-0.1-to-swi.json) | [2/2 pass](reports/2026-10-25-uri-closeout/checks/shared/swi-interop-http-0.1-to-trealla.json) | [2/2 pass](reports/2026-10-21-gnu-request-framing/swi-interop-http-to-gnu.json) |
| trealla | [2/2 pass](reports/2026-10-25-uri-closeout/checks/shared/trealla-interop-http-0.1-to-swi.json) | [2/2 pass](reports/2026-10-25-uri-closeout/checks/shared/trealla-interop-http-0.1-to-trealla.json) | [2/2 pass](reports/2026-10-21-gnu-request-framing/trealla-interop-http-to-gnu.json) |
| gnu | [2/2 pass](reports/2026-10-21-gnu-request-framing/gnu-interop-http-to-swi.json) | [2/2 pass](reports/2026-10-21-gnu-request-framing/gnu-interop-http-to-trealla.json) | [2/2 pass](reports/2026-10-21-gnu-request-framing/gnu-interop-http-to-gnu.json) |

## ACTOR interoperability

B23 covers IX-001–003 in each direction: remote source/synchronous paging,
canonical asynchronous answers and unrelated monitor/message preservation.
Public-query delegated lineages require explicit fixture peer trust; an open
execution endpoint alone grants no internal-transport authority. GNU ACTOR is
outside its profile; WASM real-network interoperability is unmeasured here.

| Caller → peer | SWI | Trealla |
|---|---|---|
| swi | [3/3 pass](reports/2026-10-23-receive-handoff-acceptance/swi-interop-actor-to-swi.json) | [3/3 pass](reports/2026-10-23-receive-handoff-acceptance/swi-interop-actor-to-trealla.json) |
| trealla | [3/3 pass](reports/2026-10-23-receive-handoff-acceptance/trealla-interop-actor-to-swi.json) | [3/3 pass](reports/2026-10-23-receive-handoff-acceptance/trealla-interop-actor-to-trealla.json) |

## Supporting native ACTOR contracts

These separately versioned draft packs do not amend baseline 0.1. GNU ACTOR is
outside profile; neither WASM mode has a shared-pack result for these rows.

| Pack | SWI | Trealla | Evidence |
|---|---|---|---|
| actor-core 0.1 | [7/7 pass](reports/2026-10-23-receive-handoff-acceptance/swi-actor-core.json) | [7/7 pass](reports/2026-10-23-receive-handoff-acceptance/trealla-actor-core.json) | B23 |
| actor-workers 0.1 | [8/8 pass](reports/2026-10-23-receive-handoff-acceptance/swi-actor-workers.json) | [8/8 pass](reports/2026-10-23-receive-handoff-acceptance/trealla-actor-workers.json) | B23 |
| actor-behaviours 0.1 | [10/10 pass](reports/2026-10-23-receive-handoff-acceptance/swi-actor-behaviours.json) | [10/10 pass](reports/2026-10-23-receive-handoff-acceptance/trealla-actor-behaviours.json) | B23 |
| actor-supervisors 0.1 | [8/8 pass](reports/2026-10-23-receive-handoff-acceptance/swi-actor-supervisors.json) | [8/8 pass](reports/2026-10-23-receive-handoff-acceptance/trealla-actor-supervisors.json) | B23 |
| links-monitors 0.1 | [6/6 pass](reports/2026-10-24-links-monitors/swi-links-monitors.json) | [6/6 pass](reports/2026-10-24-links-monitors/trealla-links-monitors.json) | L24 |
| server-waits 0.1 | [6/6 pass](reports/2026-10-24-server-waits/swi-server-waits.json) | [6/6 pass](reports/2026-10-24-server-waits/trealla-server-waits.json) | L24 |
| selective-receive 0.1 | [6/6 pass](reports/2026-10-24-selective-receive/swi-selective-receive.json) | [6/6 pass](reports/2026-10-24-selective-receive/trealla-selective-receive.json) | L24 |
| toplevel-waits 0.1 | [6/6 pass](reports/2026-10-25-boolean-closeout/checks/shared/swi-toplevel-waits-0.1.json) | [6/6 pass](reports/2026-10-25-boolean-closeout/checks/shared/trealla-toplevel-waits-0.1.json) | B25 |
| local-naming 0.1 | [6/6 pass](reports/2026-10-24-local-naming/swi-local-naming.json) | [6/6 pass](reports/2026-10-24-local-naming/trealla-local-naming.json) | L24 |
| copying-isolation 0.1 | [6/6 pass](reports/2026-10-24-copying-isolation/swi-copying-isolation.json) | [6/6 pass](reports/2026-10-24-copying-isolation/trealla-copying-isolation.json) | L24 |
| creation-validation 0.1 | [6/6 pass](reports/2026-10-24-swi-spawn-source-creation-validation/swi-creation-validation.json) | [6/6 pass](reports/2026-10-24-swi-spawn-source-creation-validation/trealla-creation-validation.json) | S24 |
| child-specs 0.1 | [6/6 pass](reports/2026-10-24-swi-spawn-source-child-specs/swi-child-specs.json) | [6/6 pass](reports/2026-10-24-swi-spawn-source-child-specs/trealla-child-specs.json) | S24 |

The local packs each select six assertions per runtime. Creation-validation
intentionally supplies option values at runtime, after admission; its green
result does not settle literal-option admission semantics. Child-specs covers
initial/nested validation and dynamic rejection/retry, not all restart/shutdown
interleavings. Naming passes do not establish matching namespace scope:
SWI ordinary names are client-scoped, Trealla ordinary names are node-wide.

## Promise and yield

U25 runs the same six PY assertions in four ACTOR-caller/HTTP-peer directions.
All **24/24** pass; the earlier actor-send callback failures are superseded only
for those selections. The eight HC assertions reused by that run are already
represented in the HTTP table, not eight additional unique cases.

| Caller → HTTP peer | SWI | Trealla |
|---|---|---|
| swi | [6/6 pass](reports/2026-10-25-uri-closeout/checks/shared/swi-promise-yield-0.1-to-swi.json) | [6/6 pass](reports/2026-10-25-uri-closeout/checks/shared/swi-promise-yield-0.1-to-trealla.json) |
| trealla | [6/6 pass](reports/2026-10-25-uri-closeout/checks/shared/trealla-promise-yield-0.1-to-swi.json) | [6/6 pass](reports/2026-10-25-uri-closeout/checks/shared/trealla-promise-yield-0.1-to-trealla.json) |

GNU promise use through HC-002 is covered above; the six-case PY contract has not
been run for GNU. WASM promise network behavior is unmeasured by this shared pack.

## Diagnostic and experimental observations

These counts stay outside required/supporting totals. B23 is the latest committed
rerun of the older supervisor/worker/ISOBASE diagnostic packs; S24 is the later
admission comparison. A later related repair cannot silently turn an unchanged
older diagnostic into a passing result.

| Pack | SWI | Trealla | GNU | Evidence |
|---|---|---|---|---|
| isobase-diagnostics | [6 observed](reports/2026-10-23-receive-handoff-acceptance/swi-isobase-diagnostics.json) | [5 observed, 1 diagnostic_error](reports/2026-10-23-receive-handoff-acceptance/trealla-isobase-diagnostics.json) | [6 observed](reports/2026-10-21-gnu-request-framing/gnu-isobase-diagnostics.json) | B23 / G21 |
| supervisor-diagnostics | [4 pass, 1 fail](reports/2026-10-23-receive-handoff-acceptance/swi-supervisor-diagnostics.json) | [5 pass](reports/2026-10-23-receive-handoff-acceptance/trealla-supervisor-diagnostics.json) | outside selected scope | B23 |
| worker-diagnostics | [1 pass](reports/2026-10-23-receive-handoff-acceptance/swi-worker-diagnostics.json) | [1 pass](reports/2026-10-23-receive-handoff-acceptance/trealla-worker-diagnostics.json) | outside selected scope | B23 |
| portable-text 0.1 (retained history) | [7 fail](reports/2026-10-23-receive-handoff-acceptance/swi-portable-text.json) | [7 pass](reports/2026-10-23-receive-handoff-acceptance/trealla-portable-text.json) | outside selected scope | B23 |
| portable-text 0.2 (experimental caller/peer pairs) | [4 pass, 22 fail](reports/2026-10-25-portable-text-0.2/swi-portable-text.json), Trealla peer | [20 pass, 6 fail](reports/2026-10-25-portable-text-0.2/trealla-portable-text.json), SWI peer | unmeasured | E25 |
| admission-paths | [10 observed](reports/2026-10-24-swi-spawn-source-admission-probes/swi-admission-paths.json) | [10 observed](reports/2026-10-24-swi-spawn-source-admission-probes/trealla-admission-paths.json) | outside selected scope | S24 |

Portable Text is an experimental character-list contract. Draft 0.2 clarifies
Unicode scalar values and constructed `src_list/1` terms. Its new observations
include separate Unicode-reader, admission and DCG-sandbox blocks; the
[report](reports/2026-10-25-portable-text-0.2/REPORT.md) explains why peer failures
and blocked boundaries do not establish a local text defect. Neither native
configuration passes the full experiment. GNU and both browser engines are
unmeasured for 0.2. Historical 0.1 results remain available and are not added to
0.2 totals. Experimental failures are not required ACTOR failures. Six
ISOBASE observations likewise do not mean six normative passes: they record
zero-limit, numeric, text, malformed-input and framing boundaries.

| Finding | Latest evidence and current qualification |
|---|---|
| Literal versus runtime validation | [S24 admission matrix](reports/2026-10-24-swi-spawn-source-admission-probes/DIAGNOSTICS.md): SWI AP-003/AP-009 fail before entry; Trealla enters and catches the validation errors. Both catch corresponding runtime errors. This observable difference remains explicit. |
| Boolean types | [B24 compatibility](reports/2026-10-24-boolean-toplevel-waits/REPORT.md) and [B25 close-out](reports/2026-10-25-boolean-closeout/REPORT.md) remain 12/12; it adds no shared cases. Separate native/browser regressions reject numeric/string once values before dispatch; isolated GNU regressions also reject pending values and invalid later duplicates. Necessary HTTP/JSON decoding remains transport-only. The native development ownership failure remains separate. |
| URI fetch before invalid options | The source-fetch ordering part is repaired: AP-009 now reports spawn_option rather than a source socket error. SWI's [34 focused checks and full T4](../swi-prolog-node/docs/verification/spawn-source-validation-2026-10-24/REPORT.md) also check zero source requests, sharing and sandbox preservation. These are implementation regressions, not extra shared passes or a pin update. |
| Runtime child-spec admission and binding | SV-001–006 now pass on both runtimes; AP-002/AP-004/AP-006/AP-008 enter as expected. These supersede the corresponding failed child-spec and admission selections. The exact older nested-supervisor SCD-001 probe was not rerun in S24: its B23 SWI failure remains recorded, with current-head status unverified. |
| Earlier literal creation probes | [Initial CV diagnostics](reports/2026-10-24-creation-validation-initial/REPORT.md) retain outer-list/value errors and Trealla logical failure. AP-009 and native regressions address the source-order subfinding; the complete original literal manifest has not been rerun unchanged. Runtime CV passes are not a waiver. |
| Trealla operator framing | B23 IBD-006 still times out: incomplete observation. GNU parenthesized request framing and passing HC-002 do not establish a repair of Trealla's unparenthesized-input behavior. |
| Incidental sandbox and reply formats | [Naming report](reports/2026-10-24-local-naming/REPORT.md): Trealla rejected format(atom(...),...) in the initial fixture; supervisor_count_children/2 formats differ. Final naming assertions avoid these incidental assumptions; no runtime alignment is claimed. |
| Older output diagnostics | [SVD-002](reports/2026-10-24-child-spec-diagnostics/REPORT.md) timed out on Trealla. The later self-message entry probes complete, but the old output probe is not rerun or relabelled as a pass. [Four entry-marker controls](reports/2026-10-24-admission-marker-controls/REPORT.md) support the later method within their stated scope. |
| Promise callback controls | P24 PYD-001–003 complete in all four directions: 12 observations, no diagnostic errors. This supports the bounded callback repair, not arbitrary callbacks or lifecycle completion. See [controls](reports/2026-10-24-promise-callback-context/COVERAGE.md). |
| Intermittent lifecycle observations | B23 worker stress and SCD-002–005 pass only for their attempts. The old creation_race, parser log during statechart invocation, and SWI intermittent T3 replacement-cleanup failure retain their own evidence; no race-freedom claim follows. The [spawn follow-up](reports/2026-10-24-swi-spawn-source-admission-probes/REPORT.md) leaves T3 and whitelist supervisor startup separate. |
| Earlier cascade fixture timeout | The [exact-notification fixture repair](../trealla-port/reproducers/cascade-wait-repair-2026-10-24/REPORT.md) passes 48/48 fixed comparison processes across the original and callback-repaired source commits. This is a test-only wait-strategy correction, separate from PY conformance, not a runtime lifecycle repair. |

## Areas without a consolidated shared result

| Area | Coverage boundary |
|---|---|
| Current deployed n3/n5 and current repository heads | No fresh combined run in this consolidation. Narrow patched-candidate results are not deployment attestations. |
| GNU beyond the selected ISOBASE surface | Full ISO modes, its broader draft contract and historical audit were not rerun. ACTOR tests do not apply to its advertised ISOBASE profile. |
| Browser network and UI | Only G21 local language cases are selected here. Native transport tests and historical manual UI checks do not cover either browser runtime end to end. |
| RELATION and complete ISOTOPE HTTP sessions | No complete shared profile suite in this selection. ACTOR toplevel waits cover a narrower public surface. |
| Authentication and security containment | No general hostile-input, TLS, credential-isolation or complete whitelist certification. Blacklist remains a prototype policy. Interoperability used explicit fixture trust. |
| Remote lifecycle and naming | Remote server waits, namespace teardown/ownership transfer, multi-hop delegated cleanup, general remote cancellation and concurrent alias races are outside the new local packs. |
| Resources and paging policies | Selected paging assertions pass; exhaustive memory/response-byte accounting, cache expiry/eviction under load, arbitrary network fetch policy and deadline accuracy under traffic are not established. |
| Full statechart semantics and shutdown races | Runtime tests and some older interoperability checks exist, but no complete shared statechart contract or exhaustive interruption/shutdown schedule is represented here. |
| Portable strings and general module semantics | Experimental text results remain separate. No portable string decision or general module-qualification conformance is inferred. |

## Historical progression and maintenance

Historical reports remain immutable evidence, including failed and initial runs.
The latest relevant results above supersede only the exact selected cases, not
unrelated diagnostics, different policy modes or older versions by assumption.

| Earlier evidence | Latest relevant follow-up |
|---|---|
| [Initial baseline](reports/2026-10-21-baseline-0.1/COVERAGE.md), HTTP source/client failures | [Source loading](reports/2026-10-21-http-source-loading/COVERAGE.md), [client context](reports/2026-10-21-http-client-context/COVERAGE.md), [GNU framing](reports/2026-10-21-gnu-request-framing/COVERAGE.md); then B23 native and P24 HTTP results above |
| [Focused native comparison](reports/2026-10-20-focused-comparison.md), worker routing/cleanup and supervisor failures | [Worker routing](reports/2026-10-20-worker-routing-repair.md), [zero polling](reports/2026-10-20-zero-poll-repair.md), [native checkpoint](reports/2026-10-21-native-checkpoint/COVERAGE.md), then B23 |
| [ACTOR parser/source capture](reports/2026-10-21-trealla-source-capture/COVERAGE.md) | B23 required packs pass; older incidental parser diagnostic is not declared resolved |
| [3.14.8 acceptance](reports/2026-10-23-upstream-3.14.8-acceptance/COVERAGE.md) | B23 receive-handoff candidate checkpoint; later 3.14.10 narrow-pack evidence does not replace a broad rerun |
| [Promise/yield initial 22/24](reports/2026-10-24-promise-yield/COVERAGE.md) | [P24 callback context 24/24](reports/2026-10-24-promise-callback-context/COVERAGE.md) |
| [Child-spec initial 6/12](reports/2026-10-24-child-specs/COVERAGE.md) | [Trealla nonbinding 7/12](reports/2026-10-24-trealla-nonbinding-child-specs/COVERAGE.md), [SWI runtime specs 12/12](reports/2026-10-24-swi-runtime-specs-child-specs/COVERAGE.md), [S24 12/12](reports/2026-10-24-swi-spawn-source-child-specs/COVERAGE.md) |
| [Initial admission matrix](reports/2026-10-24-admission-paths/DIAGNOSTICS.md) | [Trealla nonbinding](reports/2026-10-24-trealla-nonbinding-admission-probes/DIAGNOSTICS.md), [SWI runtime specs](reports/2026-10-24-swi-runtime-specs-admission-probes/DIAGNOSTICS.md), [S24 source-order matrix](reports/2026-10-24-swi-spawn-source-admission-probes/DIAGNOSTICS.md) |

For an update, select reports by exact pack/case IDs and candidate configuration,
verify raw counts and provenance, and replace only the corresponding current
cells. A newer date on an unrelated run is insufficient. Keep an explicit
"not rerun" qualification when a repair is supported by different assertions.
A release-wide statement requires a fresh full run of the intended exact sources
and engines. [Runner instructions](docs/BASELINE_RUNNER.md) and the
[baseline difference register](docs/BASELINE_DIFFERENCES.md) retain their scopes.

## Experimental SWI portable-text configuration follow-up (25 October)

The [isolated configuration matrix](reports/2026-10-25-swi-portable-text-final-r2/COVERAGE.md)
adds **26/26 text cases per direction** with a separate Trealla JSON candidate,
and **90/90 shared ACTOR/interoperability selections**. The ordinary-reader
control remains 4/26 (SWI) and 25/26 (Trealla with that SWI peer); an unmodified
Trealla v3.14.10 control retains four supplementary-Unicode failures. All are
explicit disposable working-source configurations, not new deployed-head claims.
The native report keeps four old string/code-list expectations and separate
T3 diagnostics explicit. GNU/browser migration, native-string extension fidelity,
invalid encodings and performance remain unmeasured. Earlier E25 observations
and all historical reports above are preserved rather than replaced.

### Experimental migration-test follow-up

The [native SWI migration checkpoint](reports/2026-10-25-portable-text-migration/COVERAGE.md)
preserves four exact default contracts and adds four separate character-list
counterparts. Full T4 passes 1529 parameter selections per mode; TEXT passes
40 per mode and the read-only example checks pass 10 per mode. These overlapping
native tests do not add to shared cross-runtime totals. Model/Jev native-string
service guards remain migration work; T3 diagnostics, GNU/browser adoption,
invalid encodings and performance remain outside this checkpoint.
