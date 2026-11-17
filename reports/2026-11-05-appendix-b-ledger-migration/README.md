# Appendix B ledger migration — 5 November 2026

This record describes the initial migration, before the [finite test extension](../2026-11-05-library-finite-cases/README.md) added new observations.

The ledger now pins book commit `364ee0bd73095a1e9e42610c52eab926ab796272`.
The [byte-exact manuscript](pinned-manuscript.tex), [previous ledger](previous-ledger.json)
and [migration map](migration.json) retain provenance. Inventory version is 0.2;
the established `requirements/appendix-b-0.1.json` path stays stable for callers.

All 353 old IDs remain. 350 original spans are byte-identical after relocation;
B-004 (context association), B-016 (source ordering/document exception) and
B-334 (callback paragraph) have reviewed replacements. Thirty new IDs,
B-354–B-383, cover context closure, the promise example, remote permissions,
library mode conventions, and thirteen library signature/prose pairs. IDs are
ordered by source location without renumbering earlier requirements. Examples
and bibliography prose are not counted as independent requirements; forall's
normative double-negation definition is part of its prose unit.

## Evidence and status changes

Existing target statuses/evidence are unchanged for every old ID except B-334.
The old broad paragraph's verified annotation is returned to unverified after
clause-level review: the common callback rule is not fully exercised for every
callback family. Its positive execution evidence remains as candidates, and its
original exact annotation is preserved in the archived ledger.

The new memberchk prose unit B-361 is verified against five existing passing
cases on each of the five recorded targets: first-match commitment, bindings,
failed match, unused improper tail, and member enumeration. This is a review of
dated execution evidence, not a new runtime run. Other new signatures and prose
remain unverified; their relevant case evidence is retained as candidates.
Whole-unit verified counts therefore remain eleven per target, with 372
unverified per native/browser target and 128 unverified plus 244 profile
exclusions for GNU. Counts are source units, not a language percentage.

## Library test inventory

The [archived clause inventory](library-obligations-at-migration.json)
and [archived test gap document](LIBRARY_TEST_GAPS-at-migration.md) assess 43 obligations:
16 covered within existing dated five-mode evidence, 27 needing further common
tests. Partial rows retain existing positive cases alongside concrete missing
assertions. All cited cases are checked against native and browser reports,
including exact candidate identity and manifest hash. The shared 112-case
manifest is unchanged, preserving correspondence with historical reports.

The next useful batch is finite mode/error coverage: reversed between intervals,
succ pair/zero cases, call_nth negative/noninteger indices, select/nth insertion,
and countall shared output variables. Bounded fresh/partial-list generation,
meta-callback combinations and cancellable infinite-generator checks follow.
Neumerkel's differing draft expectations are recorded as separate decisions,
not silently imported as Web Prolog requirements. Native-only example checks
and implementation-specific nested controls do not become five-target passes.

## Validation

All [78 runner tests](runner-tests.txt) pass. Both generated matrices validate:

```sh
python3 runner/appendix_coverage.py \
  --manual reports/2026-11-05-appendix-b-ledger-migration/pinned-manuscript-current.tex --check
python3 runner/library_coverage.py --check
python3 -m unittest discover -s runner
```

The first command also passes against the current clean book checkout.
Five new library-audit tests reject mismatched source/manifest/target evidence,
missing or duplicate/failed observations, unknown requirements/cases, and an
attempt to mark an open or unsupported clause covered. No runtime, public node,
deployment policy or manuscript is modified by this migration.

The initial migrated ledger is retained in `ledger-at-migration.json`; later finite-test status changes are recorded separately.

A subsequent [layout-only refresh](layout-refresh.json) pins `3edc369`; the normalized manuscript text, IDs and evidence are unchanged. Its snapshot is retained separately as `pinned-manuscript-current.tex`.
