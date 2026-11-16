# Deployed and isolated conformance refresh — 16 November 2026

The selection completed with **681 passes and 29 failed assertions as written
across 710 case executions**. It repeats the [15 November selection](../2026-11-15-deployed-conformance/REPORT.md)
against the nodes and images deployed earlier on 16 November, and adds the
draft [source-directives-0.1](../../profiles/source-directives-0.1.md) pack
(SD-001 to SD-007) to every configuration. This is a scoped refresh, not full
language or security certification. Failures are kept as failures, and controls
are recorded separately.

Suite inputs are frozen at `e3285ec` ([suite-inputs.json](suite-inputs.json)).
No implementation source, manifest expectation, service configuration, quota,
deadline, credential or release was changed for this run.

## What was tested

The deployed coordinated release `sandbox-20261116-b29a5ad-r2` pins native SWI
`swi-prolog-node` 74022a6, Trealla `trealla-port` 3d876ef, SWI-WASM
`swi-wasm-node` 82aac08 and N7 package manifest `cc060af1…`. It contains the
`directive_failed` rule and the sandbox fix that walks goal directives in
visitor source through the goal policy.

## Results by boundary

| Boundary | Result | Scope |
|---|---|---|
| Isolated SWI image used by N1/N3/N4 (`b877ac1c…`) | **45/45 + 7/7** | actor-release-0.2 gate + source-directives, disposable private node, two execution-only principals |
| Isolated SWI N2 image (`8fca5459…`) | **45/45 + 7/7** | Same; the fixture advertises ACTOR to exercise the runtime, not a claim about live N2 |
| Isolated Trealla N5 image (`5e2e4169…`) | **45/45 + 7/7** | Same, started after full WebSocket readiness |
| Public N3 | **104/105** | Anonymous WSS: 15 November's 98 cases + 7 source-directives |
| Public N4 | **104/105** | Same selection |
| Public N5 | **103/105** | Same selection |
| Public N7 | **95/105** | Same selection; five admission and four prompt rows pass in separate controls |
| HTTP ISOBASE subset on N1–N7 | **70/70** | 10 cases per endpoint |
| SWI-WASM Worker / main | **12/14 each** | language-actor 7/7; source-directives 5/7 (SD-006/SD-007, see below) |
| ACTOR toplevel interoperability | **25/36** | 3 cases × 12 directed pairs among N3/N4/N5/N7 |
| Runner self-tests | **55 pass** | Tooling checks, not counted in the totals |

Source-directives passes **7/7 on all seven sandboxed configurations**: the three
isolated images and public N3, N4, N5 and N7. Compared with 15 November, the
primary selection grows from 647 to 710 executions. The failure count goes from 24
to 29: one more N7 admission row (WC-008) and SD-006/SD-007 in both SWI-WASM modes.

The full machine-readable result is [SUMMARY.json](SUMMARY.json). Per-pack
results are under [observations](observations), and controls are under [diagnostics](diagnostics).

## New findings

### SD-006/SD-007 do not apply to an engine without a sandbox

Both SWI-WASM modes fail SD-006 and SD-007. The worker reports
`failure(@(1234567890,localhost))`; main reports `expected one solution, observed 0`.
The packaged browser engine announces `sandbox(off)` (swi-wasm-node
`docs/runtime.md`): there is no goal policy, so `open/3` on `/dev/null`
succeeds, the directive runs, and creation succeeds. This is consistent with
the engine's documented configuration. The cases require a refusal that only a
sandboxed node can give.

This is a pack applicability question, not a runtime defect. The pack should
state that SD-006/SD-007 apply only to nodes whose sandbox forbids the goal (or
choose a goal forbidden everywhere). The four failed rows are kept as written.
SD-001 to SD-005, which test the `directive_failed` rule itself, pass in both
modes.

### N7 WC-008 also hit the admission limit

On 15 November four worker cases (WC-003/004/005/007) received HTTP 429 during the
WebSocket upgrade; this run adds WC-008. These cases open several sessions each,
so the 5-second spacing of case starts does not bound every engine start under N7's
public limit of 20 engine starts per client per minute. The unchanged control
waits 61 s and spaces every WebSocket session at least 4 s apart; **all five then
pass**. The original 95/105 is not rewritten.

## Findings carried forward unchanged

Each was observed again with the same symptom. See the 15 November report for
the analysis.

- **SC-001 on N3, N4, N5 and N7**: the test expects the former asynchronous
  initial-supervisor failure; all four nodes raise the documented synchronous
  `supervisor_start_failed` error. The test and the manual need reconciling.
- **N5 RC-009**: `existence_error(procedure,runtime_property/1)` in the combined
  receive-body plus `findall` construct.
- **Inbound remote toplevels on N7**: IX-001/002/003 from N3, N4 and N5 fail with
  `Unsupported peer actor command` (9 rows).
- **N7→N5 synchronous toplevels**: IX-001/003 fail; asynchronous IX-002 passes (2 rows).
- **N7 default prompt mode**: PW-001 to PW-004 fail without negotiation and pass
  unchanged with explicit `prompt_correlation:true` (control repeated today).

## Failure accounting (29)

| Group | Rows |
|---|---|
| SC-001 test/manual contract | 4 |
| N5 RC-009 | 1 |
| N7 worker admission (429), passing paced | 5 |
| N7 unnegotiated prompts, passing negotiated | 4 |
| Interop: inbound N7 toplevel commands | 9 |
| Interop: N7→N5 synchronous toplevel answers | 2 |
| SWI-WASM SD-006/SD-007 applicability | 4 |

## Reproduction and provenance

- [orchestration](orchestration) archives the exact scripts: `isolated.py`,
  `public.py`, `interop.py`, `browser.py` and `N7-controls.py`. They are the 15 November
  scripts with the image IDs updated and the source-directives pack added. In the isolated
  fixtures the SD pack runs with the owner execution token, after the gate. They resolve
  their artifact root from `__file__` and keep machine-specific paths.
- The private artifact directory is recorded in SUMMARY. Fixture source files, node
  logs and fixture tokens were not copied into this report. The copied files were
  checked for token-like strings. Disposable containers and networks were removed
  (`cleanup_complete` in [orchestration-results](orchestration-results/isolated-summary.json)).
- Public per-pack files use `direct-runner-observations-v1`; the isolated gate files
  are canonical `release.py` reports. The SWI-WASM results come from the
  conformance `adapters/wasm.cjs` with the packaged 82aac08 runtime and its test
  shared database ([provenance](observations/browser/provenance.json)).

## Coverage limits

N0 has metadata only. HTTP ISOBASE tests on N2 do not certify complete ISOTOPE
session behaviour. No two-principal 45-case release gate was run against N7 or the
browser. N6 (GNU Prolog) is covered here only by the HTTP subset. Its own test
suites were rerun the same day outside this report (status, local and RPC suites
pass; `rpc_tests.py` needs the locked SWI 10.1.3 comparison peer and was not run).
Its loader executes no goal directives, so the source-directives pack, which tests
creation predicates, does not apply to it. Native-specific helper/admission packs,
experimental text, resource saturation and hostile security probes were not rerun.
Nothing unexecuted is counted as passing.
