# Library requirement test gaps

Pinned Appendix B: `3edc3698774258f71b11bf9998955d273ee26220`. The expanded prose is mapped into **43 testable obligations**: **42 covered** within existing evidence and **1 needing additional tests**, and **0 with an observed failure**. These are clause counts, not a conformance percentage.

The 295-case shared manifest supplies recorded native SWI, Trealla, GNU and both browser-mode observations. This audit checks every cited case against all five recorded targets. It does not certify current public deployments. A partial row can contain passing cases while still needing tests; a known failure is recorded separately.

[Source-unit matrix](APPENDIX_B_COVERAGE.md) · [Machine-readable clause inventory](../requirements/library-obligations-0.1.json) · [Shared test goals](../cases/standard-library-0.4.json)

## Observed failures

| ID / source unit | Assertion | Failing target and cases |
|---|---|---|

No failures in the current selected development evidence. The [earlier Trealla failures](../reports/2026-11-05-library-finite-cases/README.md) and [repair qualification](../reports/2026-11-05-trealla-succ-repair/README.md) remain separate records; this is not a public deployment claim.


## Additional tests

| ID / source unit | Family | Existing cases | Tests still needed |
|---|---|---|---|
| LIB-035 / B-381 | `countall/2` | None for this clause | Use a bounded cancellable fixture to observe noncompletion and then stop it; do not run an unbounded test process. |

## Covered clauses within the recorded selection

| ID / source unit | Assertion | Cases passing on all five recorded targets |
|---|---|---|
| LIB-001 / B-359 | `member/2` — Enumerate supplied-list positions left to right, including duplicate values and variable sharing | STDLIB-001, STDLIB-002 |
| LIB-002 / B-359 | `member/2` — Generate lists when List is uninstantiated | STDLIB-290, STDLIB-291, STDLIB-292 |
| LIB-003 / B-361 | `memberchk/2` — Commit to the first unifying position, preserve bindings, fail on no match and ignore an unused improper tail | STDLIB-001, STDLIB-003, STDLIB-004, STDLIB-005, STDLIB-060 |
| LIB-004 / B-363 | `append/3` — Construct concatenations and enumerate every split from the empty prefix in order | STDLIB-007, STDLIB-008 |
| LIB-005 / B-363 | `append/3` — Remove a supplied prefix in the bound-prefix mode | STDLIB-007, STDLIB-113 |
| LIB-006 / B-365 | `length/2` — Measure a proper list and construct a supplied length | STDLIB-009, STDLIB-010 |
| LIB-007 / B-365 | `length/2` — Every constructed unknown position is a distinct fresh variable | STDLIB-009, STDLIB-114 |
| LIB-008 / B-365 | `length/2` — Enumerate proper completions of partial lists and fresh lists in increasing length | STDLIB-293, STDLIB-294, STDLIB-295 |
| LIB-009 / B-367 | `select/3` — Enumerate removals in position order and preserve the remainder | STDLIB-011 |
| LIB-010 / B-367 | `select/3` — Insert into a supplied remainder in successive positions | STDLIB-115, STDLIB-116 |
| LIB-011 / B-369 | `nth0/3-4, nth1/3-4` — Enumerate zero- and one-based three-argument positions | STDLIB-012, STDLIB-013 |
| LIB-012 / B-369 | `nth0/3-4, nth1/3-4` — Remove and construct through the four-argument forms | STDLIB-014, STDLIB-015, STDLIB-016, STDLIB-117, STDLIB-118 |
| LIB-013 / B-369 | `nth0/3-4, nth1/3-4` — A supplied index beyond a finite list fails | STDLIB-119, STDLIB-120, STDLIB-121, STDLIB-122 |
| LIB-014 / B-371 | `between/3` — Enumerate inclusive bounds in order and test interval membership | STDLIB-017, STDLIB-018 |
| LIB-015 / B-371 | `between/3` — A reversed interval has no answers | STDLIB-123 |
| LIB-016 / B-371 | `between/3` — Bounds are instantiated integers under the common validation rules | STDLIB-124, STDLIB-125, STDLIB-126, STDLIB-127, STDLIB-128, STDLIB-129 |
| LIB-017 / B-373 | `succ/2` — Compute in both integer directions | STDLIB-019 |
| LIB-018 / B-373 | `succ/2` — Check supplied pairs and reject a predecessor of zero | STDLIB-130, STDLIB-131 |
| LIB-019 / B-373 | `succ/2` — At least one nonnegative integer argument is supplied | STDLIB-132, STDLIB-133, STDLIB-134, STDLIB-135, STDLIB-136, STDLIB-137, STDLIB-138 |
| LIB-020 / B-375 | `maplist/2-8` — Every arity calls private callbacks with list arguments in the documented order | STDLIB-020, STDLIB-022, STDLIB-024, STDLIB-026, STDLIB-028, STDLIB-030, STDLIB-032 |
| LIB-021 / B-375 | `maplist/2-8` — Preserve callback alternatives and partial application | STDLIB-034, STDLIB-035, STDLIB-147, STDLIB-148, STDLIB-151, STDLIB-152, STDLIB-157, STDLIB-158, STDLIB-167, STDLIB-168, STDLIB-179, STDLIB-180, STDLIB-193, STDLIB-194, STDLIB-209, STDLIB-210 |
| LIB-022 / B-375 | `maplist/2-8` — Traverse positions left to right and bind unknown lists from known lists | STDLIB-020, STDLIB-022, STDLIB-024, STDLIB-026, STDLIB-028, STDLIB-030, STDLIB-032, STDLIB-034, STDLIB-035, STDLIB-149, STDLIB-153, STDLIB-154, STDLIB-155, STDLIB-159, STDLIB-160, STDLIB-161, STDLIB-162, STDLIB-169, STDLIB-170, STDLIB-171, STDLIB-172, STDLIB-173, STDLIB-181, STDLIB-182, STDLIB-183, STDLIB-184, STDLIB-185, STDLIB-186, STDLIB-195, STDLIB-196, STDLIB-197, STDLIB-198, STDLIB-199, STDLIB-200, STDLIB-201, STDLIB-211, STDLIB-212, STDLIB-213, STDLIB-214, STDLIB-215, STDLIB-216, STDLIB-217, STDLIB-218 |
| LIB-023 / B-375 | `maplist/2-8` — Successful lists have equal length; mismatches fail | STDLIB-036, STDLIB-163, STDLIB-164, STDLIB-165, STDLIB-174, STDLIB-175, STDLIB-176, STDLIB-177, STDLIB-187, STDLIB-188, STDLIB-189, STDLIB-190, STDLIB-191, STDLIB-202, STDLIB-203, STDLIB-204, STDLIB-205, STDLIB-206, STDLIB-207, STDLIB-219, STDLIB-220, STDLIB-221, STDLIB-222, STDLIB-223, STDLIB-224, STDLIB-225, STDLIB-261 |
| LIB-024 / B-375 | `maplist/2-8` — Empty inputs succeed without invoking invalid closures | STDLIB-021, STDLIB-023, STDLIB-025, STDLIB-027, STDLIB-029, STDLIB-031, STDLIB-033, STDLIB-058, STDLIB-059, STDLIB-069, STDLIB-073, STDLIB-077, STDLIB-081, STDLIB-085, STDLIB-089, STDLIB-093 |
| LIB-025 / B-377 | `foldl/4-6` — Thread ordered elements and incoming/outgoing accumulators at every arity | STDLIB-039, STDLIB-040, STDLIB-041 |
| LIB-026 / B-377 | `foldl/4-6` — Preserve callback alternatives and empty accumulator identity | STDLIB-042, STDLIB-043, STDLIB-062, STDLIB-097, STDLIB-101, STDLIB-105, STDLIB-228, STDLIB-229, STDLIB-233, STDLIB-234, STDLIB-240, STDLIB-241 |
| LIB-027 / B-377 | `foldl/4-6` — All supplied lists have the same length on success | STDLIB-235, STDLIB-236, STDLIB-242, STDLIB-243, STDLIB-244 |
| LIB-028 / B-377 | `foldl/4-6` — Callbacks append arguments after pre-applied closure arguments | STDLIB-227, STDLIB-232, STDLIB-239 |
| LIB-029 / B-379 | `call_nth/2` — Number duplicate answers from one and select one bound position or fail past the end | STDLIB-044, STDLIB-045, STDLIB-046 |
| LIB-030 / B-379 | `call_nth/2` — Reject zero, negative and non-integer positions with the documented errors | STDLIB-047, STDLIB-139, STDLIB-140, STDLIB-141, STDLIB-142, STDLIB-143 |
| LIB-031 / B-379 | `call_nth/2` — Bound selection does not enumerate later alternatives on backtracking | STDLIB-045, STDLIB-144 |
| LIB-032 / B-381 | `countall/2` — Count duplicates, failure and one final result; check prebound outputs | STDLIB-048, STDLIB-049, STDLIB-050, STDLIB-051 |
| LIB-033 / B-381 | `countall/2` — Discard generator bindings/cuts and preserve independent nested counters | STDLIB-048, STDLIB-052, STDLIB-053, STDLIB-063 |
| LIB-034 / B-381 | `countall/2` — Shared Goal/Count variables receive only final-count unification | STDLIB-145, STDLIB-146 |
| LIB-036 / B-383 | `forall/2` — Fail on a counterexample, export no generator/test bindings and handle vacuous generators | STDLIB-054, STDLIB-055, STDLIB-056, STDLIB-057, STDLIB-061, STDLIB-110 |
| LIB-037 / B-383 | `forall/2` — One successful nondeterministic test alternative is enough for each generator answer | STDLIB-247 |
| LIB-038 / B-383 | `forall/2` — Preserve double-negation behavior inside other meta-predicates | STDLIB-054, STDLIB-055, STDLIB-061, STDLIB-248, STDLIB-249, STDLIB-250 |
| LIB-039 / B-334, B-357 | `common callbacks` — Non-callable invoked callbacks have exact callable type errors and original culprits | STDLIB-064, STDLIB-065, STDLIB-066, STDLIB-067, STDLIB-070, STDLIB-071, STDLIB-074, STDLIB-075, STDLIB-078, STDLIB-079, STDLIB-082, STDLIB-083, STDLIB-086, STDLIB-087, STDLIB-090, STDLIB-091, STDLIB-094, STDLIB-095, STDLIB-098, STDLIB-099, STDLIB-102, STDLIB-103, STDLIB-106, STDLIB-107, STDLIB-108, STDLIB-109, STDLIB-112 |
| LIB-040 / B-334, B-357 | `common callbacks` — Uninstantiated invoked callbacks raise instantiation_error without binding them | STDLIB-038, STDLIB-068, STDLIB-072, STDLIB-076, STDLIB-080, STDLIB-084, STDLIB-088, STDLIB-092, STDLIB-096, STDLIB-100, STDLIB-104, STDLIB-251, STDLIB-252, STDLIB-253, STDLIB-254 |
| LIB-041 / B-334, B-357 | `common callbacks` — Unused callback variables remain untouched | STDLIB-058, STDLIB-062, STDLIB-150, STDLIB-156, STDLIB-166, STDLIB-178, STDLIB-192, STDLIB-208, STDLIB-226, STDLIB-229, STDLIB-234, STDLIB-241, STDLIB-255, STDLIB-280, STDLIB-281, STDLIB-282, STDLIB-283, STDLIB-284, STDLIB-285, STDLIB-286, STDLIB-287, STDLIB-288, STDLIB-289 |
| LIB-042 / B-334, B-357 | `common callbacks` — Application exceptions retain their original terms | STDLIB-037, STDLIB-052, STDLIB-057, STDLIB-111, STDLIB-230, STDLIB-231, STDLIB-237, STDLIB-238, STDLIB-245, STDLIB-246, STDLIB-256, STDLIB-257, STDLIB-262, STDLIB-263, STDLIB-264, STDLIB-265, STDLIB-266, STDLIB-267, STDLIB-268, STDLIB-269, STDLIB-270, STDLIB-271, STDLIB-272, STDLIB-273, STDLIB-274, STDLIB-275, STDLIB-276, STDLIB-277, STDLIB-278, STDLIB-279 |
| LIB-043 / B-334, B-357 | `common callbacks` — Callbacks retain the caller source context | STDLIB-020, STDLIB-022, STDLIB-024, STDLIB-026, STDLIB-028, STDLIB-030, STDLIB-032, STDLIB-039, STDLIB-040, STDLIB-041, STDLIB-250, STDLIB-258, STDLIB-259, STDLIB-260 |

## Separate decisions and limits

- Do not import Neumerkel draft expectations for call_nth(true,0), invalid countall outputs or malformed length lists as new Web Prolog requirements. The committed manual and common error contract remain authoritative.
- External ISO mode/error combinations, cyclic terms and occurs-check-dependent or freeze-dependent comparisons require a separate inventory and explicit applicability.

The nineteen manuscript examples checked on native SWI do not supply five-target evidence. Shared nested forall controls and externally bounded member/length generation now pass in all five recorded modes. Generation evidence checks six-answer prefixes, followed by continuation stop and recovery on retained sessions; it is not a proof of every infinite enumeration. Infinite countall still requires its own bounded noncompletion fixture and cleanup, never an unbounded conformance process.

New source-unit signatures remain unverified pending full supported-mode mapping. Finite callback assertions pass, but the common paragraph incorporates the broader ISO call/N contract, which remains unexpanded; it is not promoted wholesale. Unverified does not mean an implementation has failed.
