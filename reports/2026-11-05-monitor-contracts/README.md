# Monitor contract qualification

The complete [maintained gate](final/results.json) passes on committed runtime
sources: **196 shared language observations**, **64 browser/native transport
observations**, and **two native implementation barrier selections**. This closes
the scoped monitor source-unit audit B-048–B-055 across native SWI, native Trealla,
SWI-WASM Worker and SWI-WASM main execution. GNU ISOBASE does not advertise these
ACTOR APIs. This report is a development-source qualification; public nodes,
consumer pins and the manuscript are unchanged.

## Behavior and repairs

The [49-case manifest](../../cases/monitor-contracts-0.1.json) tests registered
local names, fresh opaque references, exact termination notifications, immediate
spawn completion versus explicit monitoring of a dead target, both demonitor
arities and determinism, ownership/idempotence, finite option errors, and private
wait cleanup. The [clause/test mapping](../../profiles/monitor-contracts-0.1.md)
identifies the assertions for every source unit. The [remote selection](final/remote/results.json)
retains actual connection loss, late frames, no automatic monitor restoration,
confirmed withdrawal, timeout/retry, foreign-owner isolation and reference
independence against both native peers. The [native barriers](final/barriers/results.json)
retain selected-down/withdrawal orderings and serialized writer acknowledgement.

All runtimes now validate the complete demonitor option list before withdrawing
an observation or flushing. Only the atom `flush` is accepted; repeats are
validated and accepted. Variables/partial lists raise instantiation errors,
wrong list types raise `type_error(list, Value)`, and unrecognised options or
wrong arities raise `domain_error(demonitor_option, Option)`. The diagnostic
Context is not compared. Required uninstantiated references are rejected.
Invalid calls leave both the real active monitor and queued notifications
available, including when the invalid option follows a valid `flush`.

Native monitor entry points reject uninstantiated targets before registry lookup.
Trealla resolves a registered name once rather than recursively treating an
undefined name as another lookup. It validates the atom-valued node component
before reference allocation or routing. Its host diagnostics can abbreviate long
culprits; the monitor URI check and demonitor list-error boundary now preserve
the complete original value in the formal error. No engine installation was
modified.

The browser preserves an immediate child's recorded completion only for the
spawn monitor, whose reference is that pid. A fresh explicit monitor on the dead
target delivers `no_process`, regardless of retained completion information.
These changes preserve the existing remote observation-owner confirmation,
connection-loss and cancellation behavior.

## Private observations and source review

MC-019–024 exercise real toplevel call/next and server request/yield through
success, timeout, callback failure/exception, result mismatch, target death and
cleanup. MC-025 exercises supervisor control, child observation, termination,
deletion and halt. Independent spawn/explicit notifications must remain, and
unexpected private notifications are rejected. These are direct public-API
observations, without private registry inspection.

The full runtime suites complement them with implementation controls for private
monitor records, setup/send errors, interruptions, supervisor timeout/halt
ordering, child shutdown and server upgrade. SWI's `server_promise_cleanup`,
`server_upgrade_lifecycle`, `supervisor_request_cleanup`, `toplevel_synch` and
worker ownership selections check these paths. Trealla's server promise cleanup,
server actor, synchronous toplevel and supervisor halt selections check the
corresponding paths. Browser semantic scenarios cover worker interruption,
private observation-table cleanup, supervisor request/halt timeouts and shutdown;
the shared real-Chrome cases exercise both browser modes.

Source review ties these assertions to the common mechanisms: SWI removes the
calling watcher's matching reference under its monitor-lifecycle mutex; Trealla
uses the same owned-reference table for all private waits and serializes remote
withdrawal through its writer; the browser coordinator filters by watcher and
reference. Generic wait implementations use cleanup scopes around these private
references. Target retirement discharges all remaining references, while
withdrawal selects only the caller's reference. The reviewed identity allocators
reserve fresh references for the process/coordinator lifetime; the tests compare
references for identity only and make no width or representation assertion.

These observations support B-049 target resolution/freshness/correlation/loss,
B-050 independent references and private waits, B-051 immediate/dead monitoring,
B-052 determinism and B-053 ownership/options/validation. B-048's documented
monitor mode is checked by collecting all solutions in MC-001. B-054/B-055 retain
the earlier barrier/loss evidence and pass again with the repaired runtimes.
The scope is the documented language modes and the recorded local/remote routes,
not a proof of every possible scheduling interleaving or an endpoint certificate.

## Validation

[Native shared results](final/native/results.json), [real-Chrome shared results](final/browser.json),
[remote provenance](final/remote/provenance.json), and [gate fingerprints](final/results.json)
record exact cases, clean runtime revisions, package identities and unchanged
inputs. The maintained runner rejects missing, duplicate, unexpected and
nonpassing observations; it also rejects changed runtime/driver inputs.

The [full SWI suite](swi-full.txt), [full Trealla unit/interoperability suite](trealla-full.txt),
[all eleven browser groups](browser-regressions/results.json), and
[104 runner tests](runner-tests.txt) pass. The browser full suite ran the
development package; [package comparison](browser-code-equivalence.json) confirms
that its runtime and test files are identical to the final clean package. Only
`docs/runtime.md` changed. This avoids treating metadata or documentation as an
additional runtime repair or silently relabelling the original full-suite run.
[Qualification inputs](inputs.json) record commands, executables and revisions.

## Preserved diagnostics

The initial 36-case baseline is reconstructed exactly in
[manifest-baseline.json](manifest-baseline.json), whose SHA-256 matches both
[native](native-baseline/results.json) and [browser](browser-baseline.json) reports.
The native run exposes absent preflight checks; in one case the type error occurs
after the real monitor was already withdrawn. The browser run also exposes the
wrong post-termination reason.

The old LM-003 assertion could succeed on receive timeout and therefore did not
establish that `no_process` arrived. Its initial browser pass is invalid as
positive evidence. The strengthened [42-case diagnostic](manifest-diagnostic.json)
and [browser diagnostic results](browser-diagnostic.json) explicitly fail on
missing expected messages and expose that regression in both modes. Expected
receives in the reused links/server/toplevel manifests are now strict; intentional
timeout cases retain their original semantics.

The [expanded native](native-expanded/results.json) and [browser](browser-expanded.json)
runs expose a fixture issue in comparing copied exception variables by identity.
The matcher now requires an actual exception and compares the formal term by
variant, with separate no-binding and sharing assertions. The expanded native
run also exposes Trealla's shortened URI culprit; the
[complete-culprit diagnostic](native-complete-culprit-diagnostic/results.json)
then exposes its shortened long-list error. The preserved node-type diagnostics
include an initial reflection query rejected by the normal sandbox, followed by
ordinary value/exception comparisons that demonstrate the actual culprit loss.
No reflection policy was relaxed.

Final review additionally hardened the remaining deadline-delivery and positive
server-reply assertions. The [first gate](first-gate/results.json) is retained
as intermediate evidence; the final gate runs the strengthened manifest without
a further runtime change.

The [native development](native-development/results.json) and
[browser development](browser-development.json) selections pass all 49 cases per
mode before the final clean gate. Earlier 42-case successes are retained in
`native-first` and `browser-first.json`. Archived text logs have trailing whitespace
normalised; JSON observations and input/package hashes are unchanged.
