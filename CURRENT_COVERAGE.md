# Current Web Prolog conformance coverage

Updated **19 November 2026**, after deploying native SWI-Prolog 11.0.0.
The full run exercised **76 manifests / 1,973 main case rows** at suite revision
`3c5315c`. **It is not all-green.** Every main case ID has execution evidence,
but failures remain and auxiliary instrumentation blocks complete qualification.
Repeated library versions, routes, diagnostics and controls are not independent
features and must not be converted into a language-conformance percentage.

Read the [full report](reports/2026-11-19-deployed-conformance/REPORT.md),
[per-file results](reports/2026-11-19-deployed-conformance/SUMMARY.json),
[verified inventory](reports/2026-11-19-deployed-conformance/verification.json)
and [exact inputs](reports/2026-11-19-deployed-conformance/suite-inputs.json).
Historical reports remain unchanged.

The [first repair follow-up](reports/2026-11-19-conformance-repairs/REPORT.md)
records candidate source-loading, entry-fixture and public cleanup API fixes.
These are **not deployed**. The targeted controlled context rerun records
42 pass / 15 fail / 4 blocked, and all three native noncompletion probes pass.
The tables below remain the original full-run observations.

The subsequent [naming alignment](reports/2026-11-19-client-naming/REPORT.md)
implements client-context ordinary names in candidate Trealla code. The shared
pack passes 8/8 on SWI, patched Trealla and live ECLiPSe N7, and 7/7 applicable
checks in browser Worker/main (one unsupported multi-toplevel API operation per
mode). Trealla `6041ea3` is now [deployed on N5](reports/2026-11-19-live-n5-naming/REPORT.md),
with a fresh 8/8 live naming result and eight passing smoke groups. Node-wide published services remain
a separate registry; HTTP-session naming is outside this measured selection.

The [connection-cleanup follow-up](reports/2026-11-19-connection-cleanup/REPORT.md)
resolves the naming report's missed-notification probe as delayed test-client
cleanup. Both close modes pass direct independent-monitor checks for roots,
unlinked children and toplevels, with positive survivor controls. All 69
interoperability groups pass. This is a harness repair; no runtime or deployed
inputs changed, and original full-run totals below remain unchanged.

The [HTTP context follow-up](reports/2026-11-19-http-context/REPORT.md) adds
candidate Trealla retained-session namespaces. Its versioned selection passes
3/3, with 69 passing interoperability groups and one retained baseline unit
timeout. Stateless authenticated HTTP sharing and remote resumption are
unchanged; the [remote design](profiles/remote-client-context-design.md) separates
outbound client isolation from return-context restoration. No deployment changed.

The [OPEN contract candidate](reports/2026-11-19-open-http-contract/REPORT.md)
passes the 23 local context checks and six authenticated/anonymous HTTP-session
executions. All normal native and selected consumer tiers pass. The separate
34-entry drawer check retains ten baseline timeouts, so there is no green
all-exercises claim or live adoption at this checkpoint.

The [published OPEN repair](reports/2026-11-19-open-exercise-repair/REPORT.md)
now passes the full 34-entry, 136-check visible drawer sequence. The earlier ten
baseline timeouts were a retirement-context defect, now covered by positive and
controlled-negative regressions. HTTP isolation/session checks and broad native
and consumer gates pass. Deployment pins remain unchanged.

## Current deployed observations

| Node | Surface | Fresh selection |
|---|---|---|
| N0 | Public RELATION, SWI 11.0.0 | 1/1 error admission; not full RELATION |
| N1 | Public ISOBASE, SWI 11.0.0 / native 26e1ce7 | 12/12 HTTP |
| N2 | Public ISOTOPE, SWI 11.0.0 / native 26e1ce7 | 12/12 HTTP subset; not full ISOTOPE |
| N3 | Public ACTOR, SWI 11.0.0 / native 26e1ce7 | 106/106 ACTOR + 12/12 HTTP |
| N4 | Public ACTOR, SWI 11.0.0 / native 26e1ce7 | 106/106 ACTOR + 12/12 HTTP |
| N5 | Public ACTOR, deployed Trealla image | 106/106 ACTOR + 12/12 HTTP |
| N6 | Public contained ISOBASE, GNU | 12/12 HTTP + 1/1 error admission |
| N7 | Public isolated ACTOR, ECLiPSe 7.2.13 | 94/106 ACTOR + 12/12 HTTP initially; twelve 429 refusals pass paced controls |

Directed public ACTOR interoperability passes **36/36** across twelve ordered
pairs among N3/N4/N5/N7. Additional public selections record 18 successful rows
per ACTOR node, including diagnostics; DEMO-019 passes on N3. First-attempt N7
failures remain in the record alongside unchanged paced controls. No live
service was restarted or reconfigured during this conformance run; baseline
Compose container IDs and image IDs were preserved.

## Isolated native and browser coverage

| Selection | Fresh observation |
|---|---|
| Exact deployed SWI N1/N3/N4 image, private ACTOR | 45/45 release + 7/7 source-directives |
| Exact deployed SWI N2 image, private ACTOR | 45/45 + 7/7; not live N2 ACTOR certification |
| Exact deployed Trealla N5 image, private ACTOR | 45/45 + 7/7 |
| Library versions 0.1–0.4, seven modes | All pass; latest pack 295 × 7 = 2,065 case executions |
| Native and Chrome receive guard controls | 16/16 native + 16/16 browser |
| Native retained-context matrix | 39 pass / 18 fail / 4 blocked; closure 6/6; attachment controls did not execute |
| Shared monitor matrix | 94 pass / 4 fail native; 94 pass / 4 fail browser; native barriers 2/2; strict remote group blocked by instrumentation |
| Library noncompletion | Trealla/GNU and Chrome pass; SWI fails entry control, so its target operation was not measured |
| Embedded WASM source directives | 5 pass / 2 unsupported per mode, per current `goal_sandbox` applicability |
| Runner unit tests | 111 pass, outside conformance case counts |

Seven library modes means SWI HTTP/WSS, Trealla HTTP/WSS, GNU HTTP and real
Chrome Worker/main. Browser runtime package `0363b38b…` still contains SWI
10.1.19 / swipl-wasm 8.2.5. The engine payload was not upgraded to SWI 11.
Embedded Node assertions, browser session API tests and public UI tests are
different boundaries; this run does not certify the whole browser UI.

## Current findings and limits

Retained-context failures and blocked controls keep its gate red. Monitor
MC-028/029 conflict with newer URI text acceptance; their failures remain as
written. Source-aware Chrome tests retain callback-context, local naming and
unregistered-name error differences. Native URI I/O, RPC deadlines, Trealla
local-node RPC and HTTP options, statechart document fixtures, prompt HTTP and
portable-text 0.2 have unresolved failures. The dated report links observations,
source-aware reruns, original invalid fixture attempts and applicability notes.

Every main manifest was exercised, including older library packs and native
supporting/diagnostic packs. This does not establish complete ISO coverage,
complete RELATION/ISOTOPE semantics, all runtime/configuration combinations,
hostile security qualification, or passing auxiliary attachment and strict
return-barrier controls. Nothing unexecuted is counted as passing.

The [Appendix B source-unit matrix](docs/APPENDIX_B_COVERAGE.md) and
[library clause gaps](docs/LIBRARY_TEST_GAPS.md) retain obligation-level limits.
The [16 November report](reports/2026-11-16-deployed-conformance/REPORT.md),
[15 November report](reports/2026-11-15-deployed-conformance/REPORT.md) and
[older 1 November matrix](https://github.com/torbjornlager/trinity-conformance/blob/34557d322518941ba13a3e4486736e3d41d73c81/CURRENT_COVERAGE.md)
remain evidence for their original sources and configurations. Current passes
must not silently rewrite their failures; both software and suite inputs changed.
