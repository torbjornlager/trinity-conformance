# Local naming and registration conformance — 24 October 2026

## Outcome

All six corrected public-interface assertions pass on both disposable native
ACTOR nodes: **12/12 selections**, no failed, unsupported or diagnostic outcomes
in the final selection. Raw schema-2 reports and accounting validate. All 18
runner regression tests pass, including failure/missing-cell rendering for this
new suite and prior packs. See [COVERAGE.md](COVERAGE.md) and the raw reports/logs.

This separately versioned draft does not amend baseline 0.1 or claim complete
naming/lifecycle certification. No runtime code or public contract was changed.

## Selected observations

- LN-001 registers a live actor, checks lookup identity and routes ping through
  its name. The actor responds before normal termination and name withdrawal.
- LN-002 checks exact native name_is_in_use(Name) and
  process_already_has_a_name(Pid) errors. Neither conflict changes the original
  registration or creates the rejected second name; named routing still works.
- LN-003 unregisters twice, checks undefined lookup and confirms the original
  actor remains able to answer a direct ping before it is explicitly stopped.
- LN-004 consumes the exact normal termination notification before checking
  withdrawal and reusing the same name for a different live actor.
- LN-005 attempts registration only after observing the actor's exact termination.
  It requires existence_error(process,Pid), no published name and successful reuse
  for a live actor. Implementation-specific error contexts are not compared.
- LN-006 rejects occupied supervisor creation with the original registration
  intact and its output unbound. An existing actor still responds through the
  name. After stopping that actor, a nonexistent file URI forces source-setup
  failure. That output remains unbound, lookup is undefined, and retry publishes
  a usable empty supervisor. The common which_children result is exactly [].

Each case uses a distinct fixed atom on nodes serving only this run. Namespace
isolation is not inferred from this setup. Gates wait for explicit stop messages;
expected replies and exact pid/reference/reason notifications have explicit
failure/exception callbacks. Lookup outputs are fresh variables checked by
identity. No guessed sleeps, runtime imports, host threads or private registries
are used. The runner requires a final success with More=false, without an outer
once/1. Successful fixtures stop and consume expected notifications; disposable
session/node teardown bounds failures.

The source-failure exception in LN-006 is required to exist, but its file- and
platform-dependent shape is not standardized here. Its unwanted-startup poll is
a bounded zero-time observation, not a proof against arbitrary delayed activation.
Public results do not prove memory reclamation or reservation internals.

## Initial construction run and separate observations

The [initial run](../2026-10-24-local-naming-initial/REPORT.md) is preserved with
its executed manifest, raw reports/logs and preservation evidence. It reported
5 passes and 7 failures, but is not the final naming coverage selection.

All six initial Trealla queries were rejected before naming assertions because
its sandbox classifies format(atom(...),...) as stream I/O. This existing sandbox
policy difference remains a separate observation; it was not repaired or waived
as a naming failure. Fixed distinct names remove incidental formatting from the
contract under test. SWI's LN-006 assumed Trealla's counts(0,0) reply; native SWI
instead returns a list of count properties. The corrected test uses the common
public supervisor_which_children/2 result [] to establish a usable empty supervisor.

No naming assertion, receive timeout or runtime implementation was weakened to
obtain passes. The final run executes the corrected input identically on both
candidates. Initial errors remain visible and no unchanged failing selection was
retried to obtain a green result. Existing unrelated diagnostics are not cleared.

## Revisions, reproduction and evidence

The existing local-pack adapter runs one final manifest per candidate without a
peer. SWI source is the demonstrator's exact external native dependency pin
f316e65503bff863dfbd2e182f7487988c91480c. Trealla source is d4e96a3 and uses the
separate unmodified v3.14.10 engine 4ef56e3bbbcc6ca44085a4aa5eae0e6848c70294
and matching adjacent library. SWI uses the separate verified 10.1.18 build with
core 09b6299 and the HTTP shutdown candidate; version alone is insufficient.

provenance.json records source commits/status, engine hashes, node configuration,
commands and executed input hashes. The current manifest matches its launch hash.
profile-input.json records the draft document after execution. Inherited promise
input hashes in the shared adapter metadata do not mean promise suites were rerun.
New conformance inputs were uncommitted at execution and are identified by the
eventual commit containing this report. README supplies reproduction commands.

Only the existing coverage renderer and its regression tests gain a local-naming
selector. Prior defaults and report paths remain tested. The baseline executor,
runtime repositories and historical matrices are unchanged.

## Preservation and limits

Both runs have all preservation checks true: native SWI/Trealla source files,
selected engines, Trealla library and live n3/n5 identities. Both fixture pairs
were stopped. installed-preservation.json confirms installed executable targets
and hashes match the preceding preservation record. No engine installation,
launcher, repository access or running-node change occurred.

SWI ordinary names belong to a client namespace; Trealla ordinary names are
node-wide. Cross-client isolation, service names, remote aliases, concurrent name
races, publication during startup, interruption and namespace teardown remain
unmeasured. Browsers and GNU ACTOR were not run. This finite selection is not
GUI, transport, resource-reclamation, security or general lifecycle certification.
