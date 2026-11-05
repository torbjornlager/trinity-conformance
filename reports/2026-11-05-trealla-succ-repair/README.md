# Trealla successor development repair — 5 November 2026

The same 146-case shared library manifest now passes in all five modes. The
[final native report](native/results.json) has 730 passing observations across
SWI/Trealla fresh HTTP and retained sessions plus GNU HTTP. The [real Chrome
report](browser.json) has 294 passes (146 per mode plus two existing child
controls). There are no failures in this selected repair evidence. This is
working-tree source qualification, not a public deployment certificate.

## Repair

The port supplies one [integer relation](integer_relations.pl), imported by node
execution, sandbox primitive dispatch, actor receive execution and private actor
bootstraps. The public actor API re-exports it for standalone use. Supplied values
are checked as nonnegative integers before direction selection. Valid forward,
backward and bound-pair modes retain their meaning; zero has no predecessor;
two variables raise an instantiation error; invalid values preserve the original
culprit and do not bind output variables.

The installed engine's native library permits a float in its preliminary
nonnegative check, then reports an instantiation error (or fails for a supplied
pair). The new shared relation corrects Web Prolog execution without editing the
installed engine/library. Their binary/library hashes match the original failing
run. Consumer pins and public nodes remain unchanged.

[The patch](working-tree.patch), [regression source](upstream-path-tests.pl),
[upstream runner](upstream-library-runner.py) and exact manifest accompany the
recorded source-file/executable hashes. The base Trealla commit remains `62e93c3`
with the identified working-tree changes; this report does not describe that
unchanged commit as containing the repair.

## Regression boundaries

The upstream library fixture now matches the common 146-case manifest byte for
byte. Its runner covers all cases and nested variants under blacklist mode,
selected permitted library/succ calls under whitelist mode, and source-bearing
and source-free succ calls under owner sandbox-off mode. It passes 334 controls.
The dedicated successor regression additionally exercises callbacks, computed
calls where permitted, named private predicates, receive guards/bodies, public
source export/copy, more invalid types, valid pairs/zero and variable preservation
under all three policies. Sandbox permissions are unchanged.

The full unit/interoperability gate passes on the final shared implementation:
[complete log](full-suite.txt) and [qualification record](verification.json).
All runtime source-file hashes still match the shared-run snapshots. The exact
command is:

```sh
TPL=/path/to/tpl SWIPL=/path/to/swipl TEST_TIMEOUT=180 \
TEST_STARTUP_DELAY=1 tools/test.sh all
```

All 80 conformance runner self-tests pass. The ledger records 28 covered library
obligations and 15 still requiring tests. The succ paragraph is verified on the
repaired Trealla sources; the general error paragraph returns to unverified,
since fixing these two observations does not prove every API's error contract.
New signatures and remaining generation/callback obligations are not promoted.

## Preserved earlier evidence

The [original finite-case report](../2026-11-05-library-finite-cases/README.md)
retains both failing succ cases through fresh HTTP and retained sessions, with
raw error terms. The [upstream before check](upstream-before.txt) also fails on
STDLIB-134 before the repair.

The first guarded-path implementation passed the shared selection and full
native regression gate but missed source-free owner sandbox-off HTTP calls.
Its [observations and patch](initial-guard-repair/) remain archived, including
that concrete missing path. The final shared implementation replaces those
special guards and covers owner calls too; the full gate is run again on the
final implementation.

An initial whitelist test expansion also tried newly added nth0/4 calls which
existing whitelist policy rejects. Its permission error is retained separately
in `invalid-initial-whitelist-selection.txt`. Positive whitelist controls were
limited to the permitted succ family; the full shared manifest remains unchanged
and still runs in the ordinary native conformance fixtures. No allowlist was
broadened or error expectation weakened to qualify the repair.
