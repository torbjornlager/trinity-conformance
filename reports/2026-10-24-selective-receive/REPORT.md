# Selective-receive conformance — 24 October 2026

## Outcome

All six identical public assertions pass on both disposable native ACTOR nodes:
**12/12 selections**, no failed, unsupported or diagnostic outcomes. Both raw
schema-2 reports and their accounting validate. All 16 runner regressions pass,
including failure-preserving rendering for selective receive and the previous
local packs. See [COVERAGE.md](COVERAGE.md) and the raw reports/logs.

The pack is a separate draft, not a change to baseline 0.1 or complete receive
certification. No failed candidate trial was retried or repaired. No runtime
code, existing manifest, assertion or historical report was changed.

## Public observations

- SR-001 sends a term with a shared variable, rejects a ground pattern that
  would bind it, then accepts a general pattern and checks sharing. It also
  rejects a repeated-variable pattern against two distinct message variables,
  then confirms the received variables remain distinct. Original sender
  variables remain unbound after receiver-side binding.
- SR-002 selects a later target, then checks the exact relative order of earlier
  deferred messages and a following native-queue message using general patterns.
- SR-003 checks that guard failure and an ordinary literal guard exception retain
  the candidate, roll back tentative pattern/guard bindings and do not duplicate
  the message. Its guards have no external side effects.
- SR-004 deliberately enumerates any receive alternatives and requires exactly
  one first-solution guard/body pair. A second guard solution cannot leak out.
- SR-005 distinguishes selected-body logical failure and an ordinary exception
  from timeout, confirms both messages were consumed, and recovers unrelated data.
- SR-006 deliberately enumerates caller alternatives and tests an enclosing
  disjunction. A body cut must not prune either caller control scope.

All goals use only public interfaces, self-sent ordinary Prolog terms and zero-time
polls. No sleep, private mailbox inspection, implementation-specific source or
runtime import is used. Candidates receive the identical goal strings. Query
execution checks one final success with More=false; no outer once/1 hides extra
alternatives. The findall observations in SR-004/SR-006 are the assertions under
test, not normalizations of failed/nondeterministic results.

Each case has a fresh session and consumes its expected messages. Existing
session and disposable-node teardown bound failure cleanup. This is a finite
contract selection, not a mailbox stress test or reclamation proof.

## Revisions, reproduction and evidence

The unchanged local-pack adapter runs one manifest selection per candidate
without a peer. Native SWI loads from the exact demonstrator dependency pin
f316e65503bff863dfbd2e182f7487988c91480c. Exact Trealla source and conformance base
commits/status are in provenance.json. Trealla uses the separate unmodified
v3.14.10 engine and adjacent library. SWI uses the separate previously verified
10.1.18 candidate with core 09b6299 and the HTTP shutdown patch; its version string
alone does not identify those prerequisites.

provenance.json records source revisions/status, launch/runner commands, node
configuration, executable hashes and executed input hashes. The local manifest
still matches its launch hash. Inherited promise input hashes in shared-adapter
metadata do not imply those packs were rerun. profile-input.json records the
contract document after execution. New conformance inputs were uncommitted when
run and are identified by the eventual commit containing this record.

The local coverage renderer gains a selective-receive selector; its previous
paths/defaults remain tested. The baseline runner and runtime repositories are
unchanged. README contains the reproduction commands.

## Preservation and limits

preservation.json confirms unchanged native SWI/Trealla source files, selected
engines and Trealla library, plus live n3/n5 identities. Both temporary nodes were
stopped. installed-preservation.json confirms installed executable targets/hashes
match the preceding preservation record. No engine installation, launcher,
repository access or running-node change occurred.

Interruption/handoff races, abort/termination/enforced-limit control exceptions,
timeout accuracy under traffic, exhaustive clause priority, arbitrary mailbox
load, remote delivery, browser execution and GNU ACTOR are unmeasured. No GUI,
TLS, security, full native-suite or general lifecycle certification is claimed.
