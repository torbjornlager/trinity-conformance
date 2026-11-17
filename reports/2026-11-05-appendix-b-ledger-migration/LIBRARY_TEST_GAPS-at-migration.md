# Library requirement test gaps

Pinned Appendix B: `364ee0bd73095a1e9e42610c52eab926ab796272`. The expanded prose is mapped into **43 testable obligations**: **16 covered** within existing evidence and **27 needing additional tests**. These are clause counts, not a conformance percentage.

The 112-case shared manifest supplies dated native SWI, Trealla, GNU and both browser-mode observations. This audit checks every cited case against all five recorded targets. It performs no new runtime run and makes no claim about their current deployed versions. A partial row can contain passing cases while still needing tests.

[Source-unit matrix](APPENDIX_B_COVERAGE.md) · [Machine-readable clause inventory](../requirements/library-obligations-0.1.json) · [Shared test goals](../cases/standard-library-0.1.json)

## Additional tests

| ID / source unit | Family | Existing cases | Tests still needed |
|---|---|---|---|
| LIB-002 / B-359 | `member/2` | None for this clause | Collect a bounded prefix of fresh-list answers and check increasing occurrence positions and sharing. |
| LIB-005 / B-363 | `append/3` | STDLIB-007 | Call append([a],Tail,[a,b,c]) and check Tail=[b,c], plus a nonmatching-prefix failure. |
| LIB-007 / B-365 | `length/2` | STDLIB-009 | Check all pairwise inequalities, including first versus third, and freshness relative to supplied prefix variables. |
| LIB-008 / B-365 | `length/2` | None for this clause | Use bounded external answer collection for partial-tail and two-fresh-argument generation; check answer order without exhausting an infinite relation. |
| LIB-010 / B-367 | `select/3` | None for this clause | Enumerate select(x,List,[a,b]) and check all three ordered insertions, including shared variables. |
| LIB-012 / B-369 | `nth0/3-4, nth1/3-4` | STDLIB-014, STDLIB-015, STDLIB-016 | Add nth1/4 ordered removal/enumeration and nth0/4 insertion; existing cases exercise only the opposite mode in each family. |
| LIB-013 / B-369 | `nth0/3-4, nth1/3-4` | None for this clause | Cover out-of-range indices for both bases and both arities. |
| LIB-015 / B-371 | `between/3` | None for this clause | Check between(2,1,N) fails with N unbound and when a candidate is supplied. |
| LIB-016 / B-371 | `between/3` | None for this clause | Exercise uninstantiated and non-integer lower and upper bounds with exact common formal errors and unchanged variables. |
| LIB-018 / B-373 | `succ/2` | None for this clause | Test true and false supplied pairs and succ(_,0), including deterministic answer count. |
| LIB-019 / B-373 | `succ/2` | None for this clause | Test two variables and invalid type/domain inputs against the common error rules; check variables remain unbound. |
| LIB-021 / B-375 | `maplist/2-8` | STDLIB-034, STDLIB-035 | Extend nondeterministic and pre-applied-closure cases across the remaining arities. |
| LIB-022 / B-375 | `maplist/2-8` | STDLIB-020, STDLIB-022, STDLIB-024, STDLIB-026, STDLIB-028, STDLIB-030, STDLIB-032, STDLIB-034, STDLIB-035 | Observe effect order at every arity; use nonsymmetric data and generate unknown input/output lists where another list fixes length. |
| LIB-023 / B-375 | `maplist/2-8` | STDLIB-036 | Cover unequal lengths at arities 4 through 8, with each argument shorter in turn. |
| LIB-026 / B-377 | `foldl/4-6` | STDLIB-042, STDLIB-043, STDLIB-062, STDLIB-097, STDLIB-101, STDLIB-105 | Exercise alternatives for foldl/5-6 and variable/aliased accumulator identity for the two- and three-list empty forms. |
| LIB-027 / B-377 | `foldl/4-6` | None for this clause | Check unequal-length failure for foldl/5-6, with each list shorter in turn. |
| LIB-028 / B-377 | `foldl/4-6` | None for this clause | Add private partial-application closures to every foldl arity. |
| LIB-030 / B-379 | `call_nth/2` | STDLIB-047 | Test negative integers and non-integer Nth values, exact culprit, and validation before goal effects. |
| LIB-031 / B-379 | `call_nth/2` | STDLIB-045 | Put an observable effect or exception after the selected answer and prove it is not reached. |
| LIB-034 / B-381 | `countall/2` | None for this clause | Use a variable shared between Goal and Count; test both a final match and mismatch without exporting generator bindings. |
| LIB-035 / B-381 | `countall/2` | None for this clause | Use a bounded cancellable fixture to observe noncompletion and then stop it; do not run an unbounded test process. |
| LIB-037 / B-383 | `forall/2` | None for this clause | Use a failing first test alternative followed by success; check no duplicate overall answers and no exported bindings. |
| LIB-038 / B-383 | `forall/2` | STDLIB-054, STDLIB-055, STDLIB-061 | Promote the Trealla nested-meta regression into the common manifest for all five modes; include nested success, failure and binding isolation. |
| LIB-040 / B-334, B-357 | `common callbacks` | STDLIB-038, STDLIB-068, STDLIB-072, STDLIB-076, STDLIB-080, STDLIB-084, STDLIB-088, STDLIB-092, STDLIB-096, STDLIB-100, STDLIB-104 | Add invoked uninstantiated goals for countall, call_nth and both forall callback positions. |
| LIB-041 / B-334, B-357 | `common callbacks` | STDLIB-058, STDLIB-062 | Extend uninstantiated unused closures to maplist/3-8, foldl/5-6 and vacuous forall; current invalid-number controls do not assert variable preservation. |
| LIB-042 / B-334, B-357 | `common callbacks` | STDLIB-037, STDLIB-052, STDLIB-057, STDLIB-111 | Test application exceptions through foldl at every arity and call_nth, including nested forms. |
| LIB-043 / B-334, B-357 | `common callbacks` | STDLIB-020, STDLIB-022, STDLIB-024, STDLIB-026, STDLIB-028, STDLIB-030, STDLIB-032, STDLIB-039, STDLIB-040, STDLIB-041 | Use private named goals through call_nth, countall and both forall positions; existing private-source cases cover maplist and foldl. |

## Covered clauses within the recorded selection

| ID / source unit | Assertion | Cases passing on all five recorded targets |
|---|---|---|
| LIB-001 / B-359 | `member/2` — Enumerate supplied-list positions left to right, including duplicate values and variable sharing | STDLIB-001, STDLIB-002 |
| LIB-003 / B-361 | `memberchk/2` — Commit to the first unifying position, preserve bindings, fail on no match and ignore an unused improper tail | STDLIB-001, STDLIB-003, STDLIB-004, STDLIB-005, STDLIB-060 |
| LIB-004 / B-363 | `append/3` — Construct concatenations and enumerate every split from the empty prefix in order | STDLIB-007, STDLIB-008 |
| LIB-006 / B-365 | `length/2` — Measure a proper list and construct a supplied length | STDLIB-009, STDLIB-010 |
| LIB-009 / B-367 | `select/3` — Enumerate removals in position order and preserve the remainder | STDLIB-011 |
| LIB-011 / B-369 | `nth0/3-4, nth1/3-4` — Enumerate zero- and one-based three-argument positions | STDLIB-012, STDLIB-013 |
| LIB-014 / B-371 | `between/3` — Enumerate inclusive bounds in order and test interval membership | STDLIB-017, STDLIB-018 |
| LIB-017 / B-373 | `succ/2` — Compute in both integer directions | STDLIB-019 |
| LIB-020 / B-375 | `maplist/2-8` — Every arity calls private callbacks with list arguments in the documented order | STDLIB-020, STDLIB-022, STDLIB-024, STDLIB-026, STDLIB-028, STDLIB-030, STDLIB-032 |
| LIB-024 / B-375 | `maplist/2-8` — Empty inputs succeed without invoking invalid closures | STDLIB-021, STDLIB-023, STDLIB-025, STDLIB-027, STDLIB-029, STDLIB-031, STDLIB-033, STDLIB-058, STDLIB-059, STDLIB-069, STDLIB-073, STDLIB-077, STDLIB-081, STDLIB-085, STDLIB-089, STDLIB-093 |
| LIB-025 / B-377 | `foldl/4-6` — Thread ordered elements and incoming/outgoing accumulators at every arity | STDLIB-039, STDLIB-040, STDLIB-041 |
| LIB-029 / B-379 | `call_nth/2` — Number duplicate answers from one and select one bound position or fail past the end | STDLIB-044, STDLIB-045, STDLIB-046 |
| LIB-032 / B-381 | `countall/2` — Count duplicates, failure and one final result; check prebound outputs | STDLIB-048, STDLIB-049, STDLIB-050, STDLIB-051 |
| LIB-033 / B-381 | `countall/2` — Discard generator bindings/cuts and preserve independent nested counters | STDLIB-048, STDLIB-052, STDLIB-053, STDLIB-063 |
| LIB-036 / B-383 | `forall/2` — Fail on a counterexample, export no generator/test bindings and handle vacuous generators | STDLIB-054, STDLIB-055, STDLIB-056, STDLIB-057, STDLIB-061, STDLIB-110 |
| LIB-039 / B-334, B-357 | `common callbacks` — Non-callable invoked callbacks have exact callable type errors and original culprits | STDLIB-064, STDLIB-065, STDLIB-066, STDLIB-067, STDLIB-070, STDLIB-071, STDLIB-074, STDLIB-075, STDLIB-078, STDLIB-079, STDLIB-082, STDLIB-083, STDLIB-086, STDLIB-087, STDLIB-090, STDLIB-091, STDLIB-094, STDLIB-095, STDLIB-098, STDLIB-099, STDLIB-102, STDLIB-103, STDLIB-106, STDLIB-107, STDLIB-108, STDLIB-109, STDLIB-112 |

## Separate decisions and limits

- Do not import Neumerkel draft expectations for call_nth(true,0), invalid countall outputs or malformed length lists as new Web Prolog requirements. The committed manual and common error contract remain authoritative.
- External ISO mode/error combinations, cyclic terms and occurs-check-dependent or freeze-dependent comparisons require a separate inventory and explicit applicability.

The nineteen manuscript examples checked on native SWI do not supply five-target evidence. Existing nested Trealla regressions are useful supporting observations, but do not substitute for a common nested-meta case on every target. Infinite generators require bounded observation and cleanup, never an unbounded conformance process.

New source-unit signatures remain unverified pending full supported-mode mapping. The revised callback paragraph is also unverified because its general rule extends beyond the currently mapped callback cases. Unverified does not mean an implementation has failed.
