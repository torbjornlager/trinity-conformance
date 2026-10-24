# Supervisor child-specification validation — 24 October 2026

## Outcome

**6/12 selected assertions pass: SWI 1/6, Trealla 5/6.** Six required failures
remain visible in [COVERAGE.md](COVERAGE.md), rather than being waived or reclassified
as unsupported. Raw schema-2 reports and accounting validate. All 21 runner
regression tests pass, including failure/missing-cell rendering for this pack.

The test/report batch is complete; runtime interoperability is not established
for the failing paths. Runtime code and existing contracts were not changed.
This separate draft does not amend baseline 0.1.

| Case | SWI | Trealla |
| --- | --- | --- |
| SV-001 missing start | Admission instantiation error | Pass |
| SV-002 duplicate initial ids | Admission instantiation error | Pass |
| SV-003 improper outer/option lists | Admission instantiation error | Pass |
| SV-004 invalid later restart/shutdown | Admission instantiation error | Pass |
| SV-005 invalid nested specification, no startup | Admission instantiation error | Pass |
| SV-006 dynamic rejection, sibling preservation, retry | Pass | Missing runtime specification message |

## Assertions and method

The manifest contains identical public-interface goals for both candidates.
Invalid specifications are delivered as ordinary self-messages and then passed
to creation predicates. SV-006's valid initial/retry specifications are literal
positive controls. Each captured error must be nonvar before its formal term is
matched; implementation-specific context text is not compared.

The shared restart(bad) assertion explicitly accepts either SWI's
 type_error(oneof([permanent,transient,temporary]),bad) or Trealla's
 domain_error(supervisor_child_restart,bad). This finite documented formal-name
variation is not a relaxation to accept arbitrary exceptions. Shutdown(-1) must
raise domain_error(supervisor_child_shutdown,-1). Missing start and duplicate id
errors are matched directly. Rejected outputs must remain unbound.

SV-005 compares public actor snapshots around rejection and polls for an unwanted
startup message. SV-006 checks exact sibling lists and request acknowledgements
before/after rejection, then requires a successful addition and exact appended
child list. Public child monitors and the supervisor spawn monitor must survive
and deliver after halt. Shutdown reasons/timing are outside its assertions.

There are no sleeps, private registries, runtime imports or native threads in the
required pack. Expected waits throw on timeout. Snapshot equality and zero-time
polls are bounded observations, not proofs against short-lived provisional actors.
The runner requires final success with More=false without an outer once/1.
Disposable sessions/nodes bound cleanup after failures.

## Admission barrier and bounded diagnosis

SWI fails before query assertions can run for SV-001–005. Read-only inspection
of node_sandbox.pl explains the barrier: supervisor_child_meta_calls/3 delegates
to supervisor_child_specs_calls/3; an unbound whole child list is exposed as a
meta-call. The sandbox consequently rejects it with instantiation_error during
admission, before the submitted catch can execute. SV-006 has a literal outer
list and reaches its dynamic validation assertion successfully. Passing that
case does not establish support for runtime-bound initial lists.

Trealla's final SV-006 throws missing_invalid_spec_data before supervisor creation.
The staged diagnostic of the first variant also stopped while receiving that
invalid specification, before any dynamic request. Read-only inspection of
sandbox_policy.pl identifies a strong explanation: supervisor_spawn_child's
meta_goal_parts/2 examines [Spec]; supervisor_spec_goals/2 matches a child term
and memberchk(start(Start),Options) without guarding an unbound Spec/Options.
That traversal can bind the future receive-pattern variable during admission,
so the actual child(retry,[]) message no longer matches. This is a source-based
explanation supported by the stage observations, not an independently reduced
engine reproducer. No runtime fix or workaround was installed.

The separate [diagnostic run](../2026-10-24-child-spec-diagnostics/REPORT.md)
retains stage labels and an execution-entry-output probe. The latter timed out on
Trealla, so it supplies no additional validation conclusion. Its cause is not
investigated in this batch. Existing admission findings remain separate.

## Initial run and test setup simplification

The [initial run](../2026-10-24-child-specs-initial/REPORT.md) is retained with its
executed manifest and raw evidence: SWI 0/6, Trealla 5/6. Its SV-006 staged three
messages containing initial, invalid and retry terms. A separate diagnostic
identified the second data receive as the missing step. The final SV-006 stages
only the invalid specification, and uses literal positive-control specifications.
Its rejection, sibling-state, liveness, retry and cleanup assertions and all
receive timeouts are preserved. No unchanged failing run was retried to green.
The final Trealla failure remains, now with a specific input-wait label.

## Revisions, reproduction and preservation

The unchanged local adapter runs the selected pack per candidate on separate
loopback fixtures, without peers. Native SWI source is the demonstrator dependency
pin f316e65503bff863dfbd2e182f7487988c91480c. Trealla source is d4e96a3 with the
separate unmodified v3.14.10 engine 4ef56e3bbbcc6ca44085a4aa5eae0e6848c70294
and matching library. SWI uses the verified separate 10.1.18 build with core
09b6299 and the HTTP shutdown candidate; its version alone is insufficient.

provenance.json records exact source revisions/status, executable hashes,
configuration, commands and executed inputs. Final required and diagnostic
manifests match their launch hashes. profile-input.json records the contract
document after execution. Inherited promise hashes in shared adapter metadata
do not mean promise tests were rerun. New conformance inputs were uncommitted
during execution; the eventual containing commit identifies them. README gives
reproduction commands. Only the coverage renderer and its tests gain a selector;
the baseline executor and historical matrices are unchanged.

All three fixture runs have all preservation checks true and temporary nodes
stopped. Runtime source trees, selected engines/library and live n3/n5 identities
are unchanged. installed-preservation.json confirms installed executable targets
and hashes match the earlier preservation record. No installation, launcher,
repository access or live-node change occurred.

Cyclic terms, exhaustive child options, server callbacks, source policy, general
module qualification, remote supervision, concurrent additions, restart behavior,
shutdown timing, browsers and GNU ACTOR remain outside scope. These results do
not prove resource reclamation or clear existing diagnostics. The next bounded
runtime investigation would address admission of runtime-bound specifications and
Trealla's apparent variable binding before extending this pack further.
