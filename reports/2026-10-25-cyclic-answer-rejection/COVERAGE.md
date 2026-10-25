# Computed-answer cycle repair matrix

Exact inputs and limits: [REPORT.md](REPORT.md), [provenance](results/provenance.json).
This matrix describes explicit native working-source candidates. It does not
replace historical or cumulative baseline conformance totals.

| Native public boundary | SWI | Trealla |
|---|---|---|
| HTTP cyclic answer | finite cyclic-term representation error | same |
| WebSocket cyclic answer | finite cyclic-term representation error | same |
| HTTP shared variables | preserved | preserved |
| Internal cycle with finite returned template | accepted | accepted |
| Ordinary HTTP exception | unchanged | unchanged |
| HTTP cyclic exception | finite cyclic-term representation error | **separate engine diagnostic: request closes** |

| Caller → peer | RPC shared / cycle rejection | Promise shared / cycle rejection | Callback and retry |
|---|---|---|---|
| SWI → SWI | pass / pass | pass / pass | pass |
| SWI → Trealla | pass / pass | pass / pass | pass |
| Trealla → SWI | pass / pass | pass / pass | pass |
| Trealla → Trealla | pass / pass | pass / pass | pass |

**31/31 required repair selections pass; one separate diagnostic remains.**
Every post-observation HTTP health query succeeds. The native suites additionally
exercise finite-prefix errors and later-page/session recovery; Trealla's new
regressions exercise later-page/session recovery and producer cleanup. Native
T2/T4 and five selected existing Trealla groups pass. No GNU, browser, deployed
node or full Trealla-suite result is inferred.

Earlier actor-message and remote shared-variable diagnostics were not repaired
or rerun by this answer-boundary batch. Trealla's exception-copying reproducer
and logs remain separate from passing counts. See [validation](validation.json).
