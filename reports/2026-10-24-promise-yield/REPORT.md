# Promise/yield conformance batch — 24 October 2026

## Outcome

The new separately versioned draft pack passes 22/24 assertions. All six pass
with native SWI as caller against both peers. Trealla as caller passes five of
six against either peer; PY-002 fails with
`error(existence_error(procedure,(!)/2),(!)/2)`. These remain required failures
within the draft pack. The existing HC-001/HC-002 pack passes 8/8 selections;
HC-002 is reused for sharing/caller independence without duplicating its goal.
See [COVERAGE.md](COVERAGE.md) and the raw schema-2 reports.

Three separate controls pass their assertions in all four caller/peer directions
(12 observations): ordinary actor sending outside a callback, a unification-only
timeout callback, and a callback exception followed by successful retry. This
narrows the observed failure to the actor-send callback path. It does not prove
the precise module-resolution mechanism, general callback failure, or an engine
bug. No runtime repair is made or proposed as already verified here. A follow-up
can trace the callback's execution context while preserving these failures.

## Method

`adapters/local_promises.py` validates the demonstrator manifest pin before
starting disposable loopback nodes. Native SWI source is exactly
`f316e65503bff863dfbd2e182f7487988c91480c`, loaded from `swi-prolog-node` rather
than the retained demonstrator sources. Trealla uses its committed Web Prolog
source with the exact separate unmodified v3.14.10 engine and matching library.
Source commits/status, commands, versions and binary hashes are in
[provenance.json](provenance.json). SWI uses the preserved separate verified
10.1.18 build with core `09b6299` and the HTTP shutdown candidate; the version
string alone does not identify that build.

The existing implementation-neutral runner sends identical manifest goals to
every public ACTOR WebSocket caller. Each promise calls the selected HTTP peer.
All four combinations, including same-runtime peers, use disposable nodes; none
uses live n3/n5. Native layer/runtime internals are not imported into assertions.
No once/1 is added around the assertions: accidental query continuations remain
failures. Returned literal errors are distinguished from transport/query errors.

Six PY goals cover timeout/retry, one timeout callback plus unrelated-message
preservation, first-slice once behaviour, logical failure and literal remote
exceptions, unknown/collected references, and invalid wait-option preservation.
The error-answer test deliberately uses a public remote throw; internal worker
crashes, malformed replies and stream failures are not fault-injected. Timed
fixtures sleep 0.5 seconds remotely with zero-time first waits and five-second
retry bounds. A severely delayed caller could miss that scheduling interval;
this is explicit in the profile, and no observed failure is retried into a pass.
No assertion or runtime timeout was weakened after seeing results.

The first adapter execution returned nonzero because the two PY-002 assertions
failed. After reading those reports, a diagnostics-only switch and separate
manifest were added to the same adapter. The initial pack was not rerun or
rewritten; its recorded adapter/profile input hashes therefore identify the
pre-diagnostic version. New manifests and current adapter are committed together
with this evidence. The original baseline, case IDs and historical reports are
unchanged. Diagnostics appear under their own directory and provenance.

## Validation and preservation

- All eight primary reports and four diagnostic reports pass schema and count
  accounting validation (`schema-validation.log`).
- All 13 runner regressions pass, including a new matrix test ensuring successful
  diagnostics cannot erase a required failure. An initial renderer quoting error
  was caught by that test and fixed; its failed development log is retained as
  `runner-regressions-initial.log`. This was not a candidate runtime trial.
- Both before/after fixture comparisons preserve native Prolog sources, Trealla
  source files, selected engine executables and the matching Trealla library.
- Installed SWI/Trealla executable hashes and alias targets match the preceding
  preservation record (`installed-preservation.json`). No installation or
  launcher operation was performed.
- n3/n5 process identities, start times and commands are unchanged; all four
  disposable node processes from the two runs were stopped.
- `git diff --check` passes. No runtime repository or baseline runner was edited.

## Limits and next step

GNU and SWI-WASM real-network execution are unmeasured, not unsupported or passing.
This does not establish expiry, reclamation timing, concurrent collection,
ownership transfer, resource limits, remote cancellation or arbitrary scheduling
safety. Blacklist fixtures are trusted local tests, not a security certification.
No GUI, TLS, full native suite or old diagnostic suite was rerun.

The next bounded investigation is the Trealla timeout callback's actor-predicate
resolution, starting from PY-002 and its successful controls. Fixing that is a
separate runtime batch. The draft retains the failing result until repaired and
verified; it does not narrow the language contract to the implementation.
