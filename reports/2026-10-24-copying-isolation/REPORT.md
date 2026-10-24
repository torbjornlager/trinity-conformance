# Actor copying and private-source isolation — 24 October 2026

## Outcome

All six identical public-interface assertions pass on both disposable native
ACTOR nodes: **12/12 selections**, no failed, unsupported or diagnostic outcomes.
Raw schema-2 reports and accounting validate. All 19 runner regression tests
pass, including failure/missing-cell rendering for this suite and previous packs.
See [COVERAGE.md](COVERAGE.md) and the raw reports/logs.

The first candidate run passed without corrections or retries. This separate
draft does not amend baseline 0.1 or claim general lifecycle/security coverage.
No runtime code, existing public contract or historical report was changed.

## Selected observations

- CI-001 sends both the embedded spawn output and the child's self pid back to
  the parent, then compares both by identity to the actual spawn result.
- CI-002 binds the child's variable, confirms that the parent variable is still
  unbound, binds the parent to a different atom, then asks the child to confirm
  that its value is unchanged before normal termination.
- CI-003 binds a repeated child-goal variable and observes both occurrences in
  its message. Distinct unbound child variables arrive as distinct variables.
  After binding one received variable, the parent asks the child to verify that
  both original child variables are still unbound and distinct. Parent goal
  variables also remain unbound.
- CI-004 enumerates two clauses loaded through src_text and requires the exact
  [alpha,beta] order in the child's message.
- CI-005 loads a two-clause src_list, enumerates it and checks exact clause order,
  repeated unbound-variable identity, distinct variables in the second clause,
  independence across clauses, and unchanged original source-term variables.
- CI-006 supplies the same predicate name independently to the parent and two
  children. The first child reads [left], replaces it with [changed], and reports
  completion. Only then does the parent request the sibling's read, which must
  still be [right]; the parent's source must still yield [parent].

All synchronization is through explicit messages and normal actor termination.
Every expected receive has an explicit failure/exception timeout callback and
exact pid/reference/reason termination notifications are consumed. No sleeps,
runtime imports, private module names or native threads are used. The runner
requires final success with More=false and inserts no outer once/1. CI-006 uses
minimal dynamic/1 declarations to enable database mutation; general directive
policy is not selected. Each case has a fresh session. Successful fixtures exit
normally; disposable session/node teardown bounds failed fixtures.

## Revisions, reproduction and evidence

The unchanged local adapter ran one manifest selection per candidate, without
remote peers. SWI source is the demonstrator's external native dependency pin
f316e65503bff863dfbd2e182f7487988c91480c. Trealla source is d4e96a3 and uses the
separate unmodified v3.14.10 engine 4ef56e3bbbcc6ca44085a4aa5eae0e6848c70294
with its matching adjacent library. SWI uses the separate verified 10.1.18 build
with core 09b6299 and the HTTP shutdown candidate; its version string alone does
not identify those prerequisites.

provenance.json records exact source commits/status, executable hashes, commands,
node configuration and executed input hashes. The current manifest still matches
its launch hash. profile-input.json records the contract document after execution.
Inherited promise hashes in shared-adapter metadata do not mean those packs were
rerun. New conformance files were uncommitted during execution and are identified
by the eventual commit containing this report. README supplies reproduction.

The existing coverage renderer gains an optional copying-isolation selector and
a regression asserting that failures and missing cells stay visible. Previous
defaults and report paths remain tested. The baseline executor, runtime sources
and historical matrices are unchanged.

## Preservation and limits

All preservation.json checks are true: native SWI/Trealla source files, selected
engines, Trealla library and live n3/n5 identities remain unchanged. Both temporary
nodes stopped. installed-preservation.json confirms installed executable targets
and hashes match the preceding preservation record. No engine installation,
launcher, repository access or running-node change occurred.

URI loading, general directive handling, implicit source inheritance,
src_predicates, outer module qualification, remote spawning, browser runtimes,
GNU ACTOR, interruption, quotas and exhaustive sandbox policies are unmeasured.
Variable identity is tested inside Prolog rather than inferred from printed
names. This finite selection does not prove memory reclamation or a complete
security boundary and does not clear existing separate diagnostics.
