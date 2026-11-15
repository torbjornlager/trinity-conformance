# Deployed and isolated conformance refresh — 15 November 2026

The selection completed with **623 passes and 24 failed assertions as written
across 647 case executions**. This is a scoped refresh, not full language or
security certification. Failures are preserved and classified below. Controls
are separate observations, never replacements for the original failed rows.

The conformance inputs are frozen from `34557d322518941ba13a3e4486736e3d41d73c81`.
No implementation source, manifest expectation, service configuration, quota,
server deadline, credential, release or preview/snapshot ref was changed.
Only this repository's reports and current coverage documentation are updated.

## Results by boundary

| Boundary | Result | Scope |
|---|---|---|
| Isolated SWI image used by N1/N3/N4, native `8af3669` | **45/45** | Current actor-release-0.2, disposable private node, two execution-only principals |
| Isolated SWI N2 image, native `6fb82d5` | **45/45** | Same gate; fixture advertises ACTOR to exercise its runtime, not a claim that live N2 advertises ACTOR |
| Isolated Trealla N5 image, port `09dd226` | **45/45** | Same gate after full WebSocket readiness; cold-start attempt retained |
| Public N3 | **97/98** | Anonymous WSS, release gate's41 non-ownership cases plus selected behaviours/workers/language/callback/prompt packs |
| Public N4 | **97/98** | Same selection |
| Public N5 | **96/98** | Same selection, now public rather than the old SSO/backend-only route |
| Public N7 | **89/98** | Same selection; four admission and four unnegotiated-prompt observations have separate passing controls |
| HTTP ISOBASE subset on N1–N7 | **70/70** |10 cases per endpoint; inherited subset on higher profiles, not complete ISOTOPE/ACTOR certification |
| SWI-WASM Worker / main | **7/7 each** | Shared language manifest with real packaged engines under Node and mock actor coordinator; no fresh browser UI claim |
| ACTOR toplevel interoperability | **25/36** |3 cases ×12 directed pairs among N3/N4/N5/N7 |
| Runner self-tests | **55 pass** | Tooling checks, excluded from conformance execution totals |

The current release profile resolves to 45 case IDs because source-copying now
contains six cases, including `SCOPY-006`. The 1 November report's 44-case gate had
five source-copying cases. The profile label alone does not establish identical
inputs; [suite-inputs.json](suite-inputs.json) records the actual hashes.

The full machine-readable result is [SUMMARY.json](SUMMARY.json). Case files are
under [observations](observations), with controls under [diagnostics](diagnostics).

## Findings requiring follow-up

### N5 RC-009: callback context under receive enumeration

The unchanged assertion is:

```prolog
self(S), send(S,rc_probe),
findall(X,
    receive({rc_probe -> runtime_property(persistent(true)), member(X,[a,b])},
            [timeout(0),on_timeout(throw(receive_body_missing))]),
    Xs),
Xs == [a,b]
```

Public N5 returns `error(existence_error(procedure,runtime_property/1),runtime_property/1)`.
Three fresh exact-case repetitions fail the same way. Four controls pass:
ordinary `runtime_property/1`; that predicate in a plain `findall`; the predicate
in a non-enumerated receive body; and receive enumeration without that predicate.
This narrows the problem to the combined construct rather than a generally
missing capability. The precise implementation cause was not repaired here.
N3, N4 and N7 pass the original RC-009.

Evidence: [exact reproductions](diagnostics/N5-RC009-reproduction.json),
[controls](diagnostics/N5-receive-controls.json), and the original
[N5 callback pack](observations/public/N5/receive-callback-context-0.1.json).

### Inbound remote toplevel commands are unavailable on N7

`IX-001`, `IX-002`, `IX-003` fail for each of N3→N7, N4→N7 and N5→N7 with
`Unsupported peer actor command`. The source guard in
`eclipse-node/experiments/eclipse-clp/n7_actor_ws.py:586` permits peer commands
`transport_hello`, `spawn`, `send`, `exit`; it rejects `toplevel_spawn` and the
other toplevel commands.

This is a concrete peer capability gap. Bare remote actor spawn/output/reply/
prompt checks from the preceding tutorial audit remain valid, but do not prove
remote toplevel support. A repair needs ownership, source admission, reply
correlation, monitor and cleanup qualification; simply disabling the peer guard
would be insufficient.

### N7→N5 synchronous toplevel answers are not delivered through the expected path

`IX-001` and `IX-003` return failure; `IX-002` asynchronous variable-sharing
passes in that direction. Separate step controls successfully create the remote
Trealla toplevel and later halt it/receive its down notification. However,
`toplevel_call_synch` and `toplevel_next_synch` complete their waits with their
answer variables still unbound (`var(A)` / `var(B)` explicitly verified).
This localizes the observation to synchronous answer delivery/correlation,
rather than general peer authorization or inability to create the toplevel.
The exact implementation cause is unproven; no timeout was extended.

Evidence: [peer matrix](observations/interop-actor.json),
[step controls](diagnostics/N7-N5-controls.json), and
[variable checks](diagnostics/N7-N5-controls-vars.json).

### SC-001 assumes the former asynchronous initial-supervisor failure contract

All four public ACTOR nodes fail the old SC-001. The test expects
`supervisor_spawn` to return a supervisor PID and then receives an exception down
notification. The shared manual's current `supervisor_spawn/2-3` entry instead
requires initial startup to complete before return and raises
`error(supervisor_start_failed(Pid,Reason),Context)` on initial failure.
All four nodes return that synchronous error.

Treat this as a test/contract reconciliation issue. A future test update should
catch the documented exception and retain checks that provisional children are
reclaimed and the blocker survives. This run changed neither expectation nor
runtime, and retains all four failed rows. Passing the current 45-case release
gate does not cover this separate supervisor pack case.

Authority inspected: shared `web/manual.html`, `#supervisor_spawn/2-3`, and native
`supervisor_actor.pl` startup-error path. The earlier working hypothesis of only
an error-name mismatch was narrowed to synchronous versus asynchronous startup.

### N7 default prompt mode differs from the native prompt regression pack

The four PW cases assume prompt references without an explicit capability flag.
Native SWI/Trealla pass. N7's handshake defaults `prompt_correlation` to false,
so its unnegotiated prompt envelopes omit `prompt_ref` and all four fail.
The same four assertions pass when the client explicitly sends
`prompt_correlation:true` in `transport_hello`.

The actual browser/tutorial client negotiates correlation, consistent with its
previous passing checks. The conformance pack is documented as native prompt
regressions but requires ACTOR in its manifest. Decide the intended shared default
and applicability explicitly; do not waive the failed rows or silently add a
flag while claiming the original pack passed.

### N7 worker admission observations, successfully controlled

Four WC cases originally received HTTP429 during upgrade. These cases create
multiple session variants internally, so spacing only outer case starts by five
seconds did not bound every engine start. N7's public admission retains 20 engine
starts/client/minute, two client engines and four total engine entries. The
particular original sub-counter was not instrumented.

After a quiet interval, pacing **every** WebSocket session at least four seconds
apart passes WC-003/004/005/007 with unchanged goals and deadlines. These are
separate controls. The original 89/98 N7 result is retained; it is not rewritten
to 93/98. No public limit, retry mechanism or implementation was changed.

Evidence: [controls](diagnostics/N7-controls.json).

## Reproduction and provenance

- Exact isolated images and accepted reports appear in SUMMARY and
  `observations/isolated/*/release-summary.json`.
- Each isolated release invocation uses the unchanged `runner/release.py`,
  default `profiles/actor-release-0.2.json`, original default timeouts and two
  independent execution-only principals. No administrator principal is used.
- Public selection reuses unchanged `CASE_FUNCTIONS` and `baseline.query_case`.
  Core/wire functions retain 5-second transport timeouts; query packs retain the
  baseline's 8-second timeout. Ordinary created actors/sessions are closed.
- Public per-pack files use `direct-runner-observations-v1`, not canonical CLI
  report schema2. They retain each manifest's scope (including supporting packs)
  and per-assertion measured duration. Full case-ID and count accounting is
  checked separately. Canonical CLI reports retain their original schemas.
- The peer selection performs only the runner's documented `__PEER__` URL
  substitution, with the same three goals in all 12 directions.
- SWI-WASM qualification uses the verified 539a01c package with its assembled SXML
  schema and its own test `shared_db.pl`, matching packaged runtime test setup.
  Bare source trees are not equivalent packaged inputs.
- [orchestration](orchestration) archives exact helper scripts. They resolve their
  artifact root from `__file__`; copy them into a fresh private artifact root and
  reconstruct `conformance/` from the recorded commit before reuse. They retain
  machine-specific paths/image IDs and are not a general installed CLI.
- The private original artifact directory is recorded in SUMMARY. It contains
  frozen source, bounded logs and original attempts. Generated fixture token
  files and raw private state were not copied into this report.

## Initial fixture attempts are retained

[attempts](attempts) records unsuccessful preparation and early observations:

1. Host loopback ports were unreachable using the first Docker internal bridge;
   no case verdict was available. Ordinary separate bridge networking fixed the
   fixture's host access; it never joined the production network.
2. A private Trealla run began after TCP readiness and failed 19 upgrades before
   later cases passed. In a fresh fixture, three readiness probes failed before
   a complete transport welcome. Starting the unchanged gate only after that
   welcome yielded 45/45. This demonstrates a cold-start readiness window;
   it does not erase the first failed upgrade observations or prove all startup
   schedules safe. Future cutover health should include transport readiness.
3. Initial SWI-WASM adapter invocations used an unpackaged source layout or lacked
   the test shared database. One worker produced no report; main reported setup
   path errors. A zero exit without a report is incomplete evidence. The verified
   package plus explicitly supplied fixture database subsequently passed 7/7 per
   mode. No engine or assertion was changed to obtain those results.

## Coverage limits

The active ECLiPSe worktree was already at `cfb418fc909172091c30f6ddea3e092ee9e5c85a`
before the test baseline (`Report unsupported source directives with the shared
directive_failed error`). Its existing untracked `.git-claude.bundle` predates
the run and was left untouched. This selection tests the **deployed N7 sealed
package**, not that newer local development commit. It neither builds nor
qualifies/deploys that candidate. The inspected peer-command handler was checked
byte-for-byte against the selected package before using it to explain the live
rejection.


N0 has metadata only: no dedicated RELATION suite is claimed. HTTP ISOBASE tests
on N2 do not certify complete ISOTOPE session behaviour. The isolated N2 image
was deliberately configured as a private ACTOR fixture to test its runtime;
live N2 remained ISOTOPE. No two-execution-principal 45-case release gate was run
against N7 or the browser. Worker/main Node tests do not certify browser UI,
public networking or sandbox-admission parity. Native-specific helper/library/
admission packs, full experimental text matrices, resource saturation, hostile
security probes and GNU's complete predicate/mode audit were not rerun.

The earlier tutorial audit reported no unexpected failures **within its visible
example scope**. These additional conformance cases test other combinations,
remote toplevels and protocol defaults. Preserve both reports with their scopes.

## Preservation

See `preservation.json` for the final check. Live persistent services, N7
LaunchAgent/process, proxy selection, all 27 existing N7 package inventories,
all 11 coordinated groups, refs/stashes/previews/snapshots and other source
checkouts are preserved. Disposable containers/networks were removed. Current
source report edits are left uncommitted; no push or deployment was performed.
