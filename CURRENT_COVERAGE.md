# Current Web Prolog conformance coverage

Updated **15 November 2026**. The fresh selection is **not all-green**. It
records **623 passes / 24 failures as written across 647 case executions**, with
separate passing controls and classified contract/admission observations.
These are case executions across configurations, not 647 independent features.

Read the [full report](reports/2026-11-15-deployed-conformance/REPORT.md),
[machine-readable summary](reports/2026-11-15-deployed-conformance/SUMMARY.json)
and [preservation check](reports/2026-11-15-deployed-conformance/preservation.json).
Original older reports remain unchanged. Source inputs for this refresh are
`34557d322518941ba13a3e4486736e3d41d73c81`, identified by file hashes.

## Current deployed surfaces and fresh observations

| Node | Current surface | Fresh selection |
|---|---|---|
| N0 | Public RELATION registry/discovery | Metadata only; no RELATION conformance claim |
| N1 | Public ISOBASE, SWI native 8af3669 | 10/10 ISOBASE HTTP |
| N2 | Public ISOTOPE, SWI native 6fb82d5 | 10/10 ISOBASE HTTP; not complete ISOTOPE |
| N3 | Public ACTOR, SWI native 8af3669 | 97/98 public ACTOR; 10/10 HTTP |
| N4 | Public ACTOR, SWI native 8af3669 | 97/98 public ACTOR; 10/10 HTTP |
| N5 | **Public ACTOR**, Trealla 09dd226 / 3.14.20 | 96/98 public ACTOR; 10/10 HTTP |
| N6 | Public contained ISOBASE, GNU 1.6.0 | 10/10 ISOBASE HTTP |
| N7 | **Public isolated ACTOR**, ECLiPSe 7.2.13 | 89/98 public ACTOR; 10/10 HTTP; separate worker/prompt controls pass |

N5 is no longer the old SSO-only backend path. N7's UI is
[https://n7.elfenbenstornet.se/demonstrator](https://n7.elfenbenstornet.se/demonstrator).
Current safe metadata, image provenance and exact source selection are linked
from the dated report and the shared project handover. Image labels alone can
be inherited; native N1/N3/N4 source matches 8af3669, while N2 matches 6fb82d5.
No pin or deployed image was changed for this test run.

## Isolated release gate and browser scope

| Configuration | Fresh result |
|---|---|
| Deployed SWI N1/N3/N4 image, disposable private ACTOR | 45/45 |
| Deployed SWI N2 image, disposable private ACTOR | 45/45 |
| Deployed Trealla N5 image, transport-ready disposable private ACTOR | 45/45 |
| SWI-WASM Worker, packaged 539a01c under Node | 7/7 shared language cases |
| SWI-WASM main, same package under Node | 7/7 shared language cases |
| Conformance runner self-tests | 55 pass; separate from case totals |

The current `actor-release-0.2` resolves to 45 cases, including SCOPY-006.
The 1 November 44-case record remains accurate for its older input hashes.
The fresh native gate uses distinct execution-only principals and loopback
fixtures; it is not a public-proxy/security certification. The live public
selection excludes ownership-lifecycle and adds selected behaviour, supervisor,
worker, language, receive and prompt packs: 98 cases/node. No full 45-case gate is
claimed for ECLiPSe or the browser. Browser Node assertions are distinct from
browser UI/network tests and historical implementation CI results.

## Remaining findings

- **N5 RC-009:** missing `runtime_property/1` in the combined receive-body plus
  `findall` assertion; three exact fresh repetitions fail, while four narrower
  controls pass.
- **Inbound remote toplevels on N7:** IX001/2/3 fail from N3/N4/N5 because the
  trusted peer command handler omits `toplevel_*`. Nine failed executions.
- **N7→N5 synchronous toplevels:** IX001/3 fail; asynchronous IX002 passes.
  Diagnostic calls explicitly confirm unbound synchronous answer variables,
  while remote creation, halt and down notification work.
- **N7 default prompt mode:** the four native PW assertions fail without
  capability negotiation and pass unchanged with explicit
  `prompt_correlation:true`. Keep the default/applicability difference visible.
- **SC-001 on all four ACTOR nodes:** old asynchronous initial-supervisor
  failure expectation conflicts with the current manual's synchronous startup
  exception. All four failed rows remain; reconcile the test contract before
  proposing a runtime repair.
- **Four N7 worker admission failures:** original 429 rows are retained. All four
  pass when every inner WebSocket session is paced, without changed assertions,
  deadlines or public limits. Do not relabel the original 89/98 result.

The three-case ACTOR interoperability pack passes **25/36** across 12 directed
pairs. Inbound-N7 and N7→N5 failures above account for its 11 failed executions.
The earlier 36-check bare actor output/reply/prompt audit covers different
operations and remains valid within that scope.

## Evidence and accounting

See the dated report's `observations/` for canonical CLI reports and direct
runner observation files, `diagnostics/` for controls, `attempts/` for retained
fixture failures, `suite-inputs.json` for frozen hashes, and `verification.json`
for schema/case-ID/count checks. All raw public failures remain failures in the
primary 647-case selection. Repeated/negotiated/paced controls are separate.

This refresh does not run every draft/native-only manifest in the repository:
full native-specific helper/admission/library contracts, experimental text,
resource stress, GNU's broader ISO inventory/mode audit, complete RELATION and
ISOTOPE contracts, browser admission parity and hostile security qualifications
remain outside its scope. Nothing unexecuted is counted as passing.

The older [1 November matrix](https://github.com/torbjornlager/trinity-conformance/blob/34557d322518941ba13a3e4486736e3d41d73c81/CURRENT_COVERAGE.md)
retains its dated 88-case isolated and 132-case deployed selections, CI links and
broader historical index. Those source/configuration claims do not describe
today's public N5/N7 selection. The baseline remains a scoped draft, not complete
language/profile/security certification.
