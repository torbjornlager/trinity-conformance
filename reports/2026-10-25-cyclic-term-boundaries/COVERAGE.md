# Cyclic-term diagnostics matrix

Exact inputs, limits and interpretation: [REPORT.md](REPORT.md).
These are observations outside baseline 0.1 cyclic-term coverage, not required
pass/fail selections. Finite shared-variable controls retain their exact checks.

| Public path | SWI | Trealla |
|---|---|---|
| Raw HTTP shared-variable control | shared identity preserved | shared identity preserved |
| Raw HTTP finite summary of constructed cycle | reports cyclic | reports cyclic |
| Raw HTTP cyclic answer | time resource error | acyclic approximation returned |
| Raw HTTP cyclic exception | time resource error | request closes without response |
| Local actor shared-variable echo | shared identity preserved | shared identity preserved |
| Local actor cyclic echo | term-depth resource error | acyclic approximation returned |

For RPC and promise rows, the column identifies the peer computing the result:

| Caller | Peer | `rpc/3` shared control | `rpc/3` cycle | Promise shared control | Promise cycle |
|---|---|---|---|---|---|
| SWI | SWI | preserved | time resource error | preserved | time resource error |
| SWI | Trealla | preserved | acyclic approximation | preserved | acyclic approximation |
| Trealla | SWI | preserved | time resource error | preserved | time resource error |
| Trealla | Trealla | preserved | acyclic approximation | preserved | acyclic approximation |

| Actor sender | Peer | Shared-variable echo | Cycle send/echo |
|---|---|---|---|
| SWI | SWI | preserved | sender term-depth rejection |
| SWI | Trealla | delivery timeout; separate diagnostic | sender term-depth rejection |
| Trealla | SWI | preserved | client socket timeout; operation unisolated |
| Trealla | Trealla | delivery timeout; separate diagnostic | client socket timeout; finite control also fails |

The two failing actor shared-variable controls are **not** classified as cyclic
term failures. Supporting ground echo controls succeed in both directions.

| Standalone operation | SWI | Trealla v3.14.10 |
|---|---|---|
| Create `X=f(X)` | cyclic | cyclic |
| Copy with `copy_term/2` | cyclic | cyclic |
| Occurs check creating cycle | fails | fails |
| Occurs check on existing cycle, same term | succeeds | succeeds |
| Store/retrieve with `nb_setval/2` | cyclic | acyclic |
| Thread queue round trip | cyclic | acyclic |
| `findall/3` on cyclic template | cyclic | printed acyclic-term error; process exit 0 |
| Bounded-depth writer | finishes | finishes |

Four additional SWI reductions (`term_attvars/2`, `findnsols/4`, internal
`portable_answer/2` and `answer/5`) finish and retain the cycle where applicable.
Thus the HTTP time-resource outcome has not been reduced to an engine collection
bug. The eight initial engine observations, 36 public observations and 14
supporting observations remain separate from cumulative conformance totals.

No GNU or browser coverage is claimed. No full ACTOR/interoperability suite,
portable-text matrix or ISO assessment was rerun. See [validation](validation.json),
[public/engine observations](results/observations.json),
[supporting observations](followup-results/observations.json), and
[SWI reductions](swi-reduction-results.json).
