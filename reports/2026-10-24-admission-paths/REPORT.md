# Admission-path investigation — 24 October 2026

## Outcome

All **20 main observations** completed: ten identical public-interface probes on
each disposable runtime, with no probe errors or timeouts. This is diagnostic
completion, **not 20 conformance passes**. The [DIAGNOSTICS.md](DIAGNOSTICS.md)
matrix retains successes, errors before entry, caught errors and requests that
were never dispatched. Existing required coverage matrices are unchanged.

Four additional [entry-marker controls](../2026-10-24-admission-marker-controls/REPORT.md)
also completed, showing that ordinary query exceptions and logical failure retain
the marker on both runtimes. All raw schema-2 reports/accounting validate, and all
26 runner regression tests pass.

## Findings

### SWI rejects opaque initial child lists before execution

AP-001 creates and halts a valid literal one-child supervisor on both runtimes.
AP-002 supplies the same list through a self-message. Trealla executes it, but
SWI returns error(instantiation_error,_) and the entry marker is absent. AP-003/004
repeat this contrast with a missing-start specification: literal calls reach the
submitted catch on both runtimes; SWI's runtime-bound initial list is rejected
before that catch, while Trealla catches missing_start_option(probe).

Read-only inspection of native node_sandbox.pl identifies the path:
reject_supervisor_child_specs/3 calls supervisor_child_meta_calls/3, then
supervisor_child_specs_calls/3. An unbound whole child list is exposed as a meta
call [Module:ChildSpecs], so admission checks an opaque variable goal. This is a
sandbox-adapter restriction, not evidence of an SWI engine fault. Whether dynamic
initial lists should be admitted requires a guarded runtime-check design; simply
omitting the sandbox check would not be an acceptable repair.

### Trealla admission changes a dynamic child's receive variable

Literal valid and invalid additions (AP-005/007) execute on both runtimes. Valid
addition returns ok and one child; invalid addition is caught as missing_start.

For runtime-bound additions (AP-006/008), SWI reports PatternState=unbound, matches
the message, and respectively adds the child or catches the missing-start error.
Trealla reports this value **before sending the message**:

    bound(child(_,[start(server(_,_))|_]))

Its receive cannot match either supplied specification; Matched=no and
Reply=not_dispatched, with no child added. These observations directly explain the
prior dynamic test's missing input message; it was not waiting for a supervisor
reply, and no runtime request had been dispatched.

The source path is Trealla's Web Prolog sandbox_policy.pl, not an engine primitive:
meta_goal_parts(supervisor_spawn_child(...)) invokes supervisor_spec_goals([Spec],...).
The child-shaped clause unifies an unbound Spec, memberchk(start(Start),Options)
constructs an option list, and the first supervisor_start_goals(server(_,_),[])
head binds Start to server(_,_). The resulting term matches the captured value.
Admission should inspect without changing application data. The smallest repair
candidate is nonbinding shape analysis with existing runtime goal checks retained,
plus regressions for both valid and unsafe runtime additions. No repair was made.

### SWI literal source preparation precedes the unknown-option error

AP-009 contains a missing file URI followed by unknown(admission_probe). Trealla
enters the query and catches domain_error(spawn_option,unknown(admission_probe)).
SWI returns a socket name-resolution error before query entry; the submitted catch
cannot intercept it. AP-010 supplies the same list at runtime: both enter and
catch the spawn-option error before source loading.

Native node_sandbox.pl's reject_nested_spawn_goal/4 selects source preparation for
known literal source options. prepare_source_options/6 processes options in order;
materialize_source_option/4 reaches uri_to_source_limited/3 for src_uri before the
later unknown option is rejected by the creation API. The result establishes the
ordering difference in this fixture, not the complete semantics of file URI
handling or proof that a network connection was made. The exact socket error is
retained. Validation-before-materialization is a separate bounded repair candidate.

## Entry evidence and raw transcripts

Each fresh session receives a goal prefixed with a self-message. After the first
terminal response, the runner sends a second query on the same shell to consume
the marker, then halts the shell. The marker is present after both ordinary
exception and logical-failure controls. In the main run it is absent only for
SWI AP-002, AP-004 and AP-009, consistent with errors during admission.

Raw reports preserve every sent command and decoded response object, including
negotiation, spawn, exact query text/options, primary result, follow-up and halt.
This is decoded JSON capture, not a TCP/WebSocket-byte trace. No terminal-output
marker, fixed sleep, runtime import or private registry is used. Captured errors
are observations, not expected-success assertions. Marker replies must be one
final yes/no success; incomplete protocol/cleanup remains diagnostic_error.

The four proposed comparison groups yield ten variants because dynamic additions
have valid and invalid controls. No probes were retried to green or thresholds
changed. The output-probe timeout from the earlier investigation was not rerun or
claimed fixed; these non-output observations make it unnecessary for this trace.

## Tools, revisions and reproduction

A diagnostic-only admission transport delegates from runner/baseline.py to
runner/admission_probe.py. Existing query/wire/HTTP paths remain unchanged. A
required-scope manifest cannot use this transport: a regression checks that it
fails without running the probe. The local fixture adapter now hashes this extra
module when used. runner/admission_coverage.py generates a separate matrix and
keeps incomplete and missing results visible. No runtime repository was edited.

Native source remains the exact demonstrator dependency pin
f316e65503bff863dfbd2e182f7487988c91480c. Trealla source is d4e96a3 and uses the
separate unmodified v3.14.10 engine 4ef56e3bbbcc6ca44085a4aa5eae0e6848c70294
with its adjacent library. SWI uses the separate verified 10.1.18 build with core
09b6299 and the HTTP shutdown candidate; version alone is insufficient.

provenance.json records source commits/status, commands, configuration, engine and
input hashes, including the new capture module. Both executed manifests and
capture inputs match their launch hashes. profile-input.json records the scope
document after execution. New conformance files were uncommitted during the run
and are identified by the eventual containing commit. Inherited promise hashes
in adapter metadata do not mean those suites were rerun. README has commands.

## Preservation and limits

Main and control runs have all preservation checks true and both fixture pairs
stopped. Runtime source trees, selected engines/library and live n3/n5 identities
remain unchanged. installed-preservation.json confirms installed binary targets
and hashes match the preceding preservation record. No installation, launcher,
repository access or running-node change occurred.

This finite blacklist-mode comparison does not establish whitelist behavior,
production policy intent, concurrency safety, exhaustive source semantics, remote
transport, browser/GNU behavior, resource reclamation or complete sandbox security.
The new findings concern Web Prolog adapters; an upstream engine report is not
warranted by these results alone. Recommended first repair discussion: Trealla's
nonbinding specification inspection, followed separately by SWI admission support
and source-validation order. Existing required failures remain untouched.
