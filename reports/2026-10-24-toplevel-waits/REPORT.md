# Synchronous toplevel wait conformance — 24 October 2026

## Outcome

The corrected six-case pack passes identically on both disposable native ACTOR
nodes: **12/12 selected assertions**, no failed, unsupported or diagnostic
outcomes. Raw schema-2 reports and accounting validate. All 17 runner regressions
pass, including failure-preserving rendering for this new pack and prior packs.
See [COVERAGE.md](COVERAGE.md) and the raw reports/logs.

This is a separate draft selection, not a baseline 0.1 amendment or general
lifecycle certification. Runtime code and existing public contracts are unchanged.

## Observations

- TW-001 checks the exact conflicting-target domain error, accepts explicit caller
  targeting and confirms that returned template values do not bind query variables.
- TW-002 holds each query behind a release gate. Default timeout leaves Answer
  unbound; callbacks retain bindings, failure and their exception. Enumerating
  the binding callback produces exactly its first solution. Every blocked query
  is released and a subsequent synchronous barrier confirms completion.
- TW-003 checks stale correlation for both call and next. The old answer must
  precede the later response because the toplevel processes commands sequentially.
  The next scenario times out on gated b, releases it, then requires c. Neither
  timed-out query is cancelled, and neither late answer can satisfy the next wait.
- TW-004 deliberately mismatches the call slice a and next slice b, then requires
  exactly [c,d] with More=false. Both outputs are selected before unification;
  failure cannot leave an earlier slice for the next synchronous request.
- TW-005 commits an actor exit during the query and requires
  toplevel_down(tw_death), plus both exact public termination notifications.
- TW-006 leaves a normal asynchronous answer and ordinary application data queued
  while collecting a synchronous response. Both survive, as do spawn-time and
  independent monitors through subsequent normal termination.

All gates are inline public query terms. Readiness/notification waits have explicit
failure/exception callbacks. No sleeps, private envelopes, registry access or
runtime imports are used. The runner requires one final success with More=false;
there is no outer once/1 hiding residual alternatives. Callback enumeration is
itself an assertion of the documented commitment. Each case has a fresh session,
halts successful fixtures and consumes expected messages. Session/node teardown
bounds failed fixtures; this does not prove private monitor resource reclamation.

## Initial test correction

The [initial run](../2026-10-24-toplevel-waits-initial/REPORT.md) is retained with
its executed manifest, failed raw reports, logs and preservation evidence. It had
four reported passes and two failures per candidate, but is not coverage evidence:
its gate helper was not supplied to the child toplevel, readiness waits could
silently time out, and TW-004 expected a failure answer from next after completion.
TW-003's apparent pass therefore did not establish its intended gated execution.

The corrected manifest embeds gates, makes readiness waits fail explicitly,
advances past both mismatched slices while a continuation exists, and additionally
checks next-timeout correlation. The second run used these corrected assertions
on both candidates. No runtime repair or timeout increase was made, and no failed
runtime selection was retried unchanged to obtain a green result.

## Revisions, reproduction and evidence

The existing local adapter ran one final manifest selection per candidate.
SWI source is the demonstrator's exact external-native dependency pin
f316e65503bff863dfbd2e182f7487988c91480c. Trealla source is d4e96a3 and uses the
separate unmodified v3.14.10 engine (4ef56e3bbbcc6ca44085a4aa5eae0e6848c70294)
with its adjacent matching library. SWI uses the verified separate 10.1.18 build
with core 09b6299 and the HTTP shutdown candidate, not just a generic version match.

provenance.json identifies exact commits/status, executable hashes, configuration,
commands and executed input hashes. The current manifest matches its launch hash.
profile-input.json records the contract document after execution. Inherited
promise hashes in the shared adapter metadata do not imply promise tests were
rerun. New conformance files were uncommitted during execution; the eventual
commit containing this record identifies them. README supplies reproduction.

The existing coverage renderer has a new optional toplevel-waits selector; its
previous defaults and paths remain tested. The baseline executor is unchanged.
Historical matrices are not regenerated.

## Preservation and limits

Both runs' preservation.json checks are all true: native/Trealla source files,
selected engines, Trealla library and live node identities remain unchanged.
Both pairs of disposable nodes were stopped. installed-preservation.json confirms
installed executable targets and hashes match the preceding preservation record.
No installation, launcher, repository access or n3/n5 change occurred.

Remote transport, browser runtimes, GNU ACTOR, terminal I/O, concurrent controlling
clients, deadline accuracy under traffic, cancellation, exhaustive option checks,
private monitor reclamation and general lifecycle stress remain unmeasured.
Existing unresolved diagnostics remain separate; this run does not clear them.
