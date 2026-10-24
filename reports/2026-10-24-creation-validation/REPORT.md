# Local creation-option validation — 24 October 2026

## Outcome and scope

All six runtime-supplied-option cases pass identically on both disposable native
ACTOR nodes: **12/12 selections**, no failed, unsupported or diagnostic outcomes
within that final selection. Raw schema-2 reports and accounting validate. All
20 runner regression tests pass, including failure/missing-cell rendering for
this suite and prior packs. See [COVERAGE.md](COVERAGE.md).

This is a separate draft of runtime validation, not baseline 0.1 amendment or
complete query-admission certification. The initial literal-option run had five
failures, retained as [separate diagnostics](../2026-10-24-creation-validation-initial/REPORT.md).
Those paths are unresolved, not waived or cleared by the final matrix. No runtime
code or public contract was changed.

## Public assertions

- CV-001 rejects unknown(creation_probe) with domain_error(spawn_option,...),
  leaving the spawn output unbound.
- CV-002 rejects unbound options, an improper list and an unbound list entry with
  the selected instantiation/list errors. Input variables and outputs remain
  unbound where appropriate.
- CV-003 rejects link(maybe), monitor(1) and node(42) with the selected formal type
  errors. Every rejected creation output remains unbound.
- CV-004 checks every occurrence: later invalid link/session/period values cannot
  be ignored because an earlier valid setting exists. Spawn, toplevel and empty
  supervisor construction all reject them.
- CV-005 checks that plain spawn rejects session/strategy options while the
  corresponding constructors accept them. session(false) preceding session(true)
  yields one answer then normal monitored termination, demonstrating first-value
  precedence. An empty supervisor accepts the documented strategy, zero intensity
  and fractional period, returns an empty child list and halts normally.
- CV-006 places a nonexistent file URI before an unknown option. Runtime validation
  must reject the unknown option before source loading and application activation.
  Its output remains unbound, no unwanted message is observed, and a subsequent
  valid actor announces startup and terminates on an explicit stop message.

Lists are self-sent as ordinary terms, received into fresh option variables, and
then passed to creation predicates. This includes literal receive/wrapper option
lists; their original values and timeout callbacks are preserved. The deliberately
unbound list stays unbound. Each caught error must be nonvar before matching its
formal term; implementation-specific contexts are not compared. Pids/references
are opaque, and exact normal termination notifications are consumed where normal
termination is selected (supervisor halt reason is not standardized by this pack).

No fixed sleeps, runtime imports, private registries or native threads are used.
Every expected receive has an explicit failure/exception callback. Zero-time
unwanted-start polls are bounded observations, not proof against arbitrary delayed
activation. The runner requires final success with More=false without inserting
once/1. Successful fixtures terminate; disposable session/node teardown bounds
failures. Public observations do not prove private resource reclamation.

## Initial literal-option observations

The initial run used literal option lists. SWI reported 3 passes/3 failures;
Trealla reported 4 passes/2 failures. Some errors arose before execution could
enter the submitted catch/3: improper-list admission, node-option sandbox policy,
source preparation and a Trealla text-type error. Trealla CV-002 returned logical
failure; its exact contributing step is not reduced. The raw observations and
executed manifest are retained, with no runtime repairs or timeout increases.

The final manifest selects runtime validation through message-delivered lists.
The same invalid values and expected formal errors are retained, and captured
errors are additionally required to be nonvar. Both candidates execute identical
input. This change isolates a different execution surface; it is not evidence
that the initial admission failures are fixed. Future investigation can reduce
those paths independently, without changing this pack's runtime assertions.

## Revisions and reproduction

The unchanged local-pack adapter ran one final manifest selection per candidate,
without peers. SWI source is the demonstrator's external native dependency pin
f316e65503bff863dfbd2e182f7487988c91480c. Trealla source is d4e96a3 and uses the
separate unmodified v3.14.10 engine 4ef56e3bbbcc6ca44085a4aa5eae0e6848c70294
with its adjacent matching library. SWI uses the separate verified 10.1.18 build
with core 09b6299 and the HTTP shutdown candidate; version alone is insufficient.

provenance.json identifies exact source commits/status, engine hashes, commands,
node configuration and executed input hashes. The final manifest matches its
launch hash. profile-input.json records the contract document after execution.
Inherited promise hashes in adapter metadata do not imply those suites were rerun.
New conformance files were uncommitted during execution and are identified by the
eventual commit containing this report. README supplies reproduction commands.
The existing coverage renderer gains an optional creation-validation selector;
prior defaults and report paths remain tested. The baseline executor, runtime
repositories and historical matrices are unchanged.

## Preservation and limits

Both runs have all preservation checks true: native SWI/Trealla sources, selected
engines, Trealla library and live n3/n5 identities. Both disposable fixture pairs
stopped. installed-preservation.json confirms installed executable targets and
hashes match the preceding preservation record. No engine installation, launcher,
repository access or running-node change occurred.

Static query admission, child-spec validation, statecharts, HTTP options, remote
creation, concurrent startup, exhaustive quotas, general source/sandbox policy,
browsers and GNU ACTOR are outside the final required selection. Initial
admission findings and all existing unrelated diagnostics remain separate.
