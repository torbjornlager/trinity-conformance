# Links and monitors draft conformance — 24 October 2026

## Outcome

All six identical public-interface assertions pass on both disposable native
candidates: **12/12 selections**, no failed, unsupported or diagnostic outcomes.
Both schema-2 reports and their accounting validate. All 14 runner regressions
pass, including a new coverage-renderer check that preserves a required failure
and labels an absent case unmeasured. See [COVERAGE.md](COVERAGE.md).

This is a separately versioned draft pack, not a change to baseline 0.1 or a
complete ACTOR certification. Historical profiles, manifests and results remain
unchanged. No runtime repair or upstream engine change was made in this batch.

## Tests and method

The same six manifest goals run through public sandboxed ACTOR WebSocket sessions:

1. Spawn-time monitoring observes immediate true, false, literal exception and
   explicit-exit reasons, each with its exact pid/spawn reference.
2. Explicit and spawn-time monitoring deliver independently, using distinct
   opaque references, while unrelated application data remains available.
3. Monitoring after a known termination reports no_process with its own reference.
4. A linked parent remains responsive after its child's normal termination.
5. A readiness-synchronized three-generation tree cascades root/die to child/kill
   and grandchild/kill, with all exact notifications under one two-second deadline.
6. Demonitor withdrawal and idempotent scoped flush preserve unrelated references,
   pending application data and a retained monitor's genuine termination delivery.

No fixed sleep, actor enumeration, private registry access or runtime-specific
helper appears in a goal. Handshake messages and observed notifications establish
readiness/completion. Independent notification order is not asserted. Fixtures
are linked to their fresh controlling sessions; expected events are consumed and
explicit monitors retired on success. Normal session and disposable-node teardown
bound failed fixtures. No once/1 wrapper hides query alternatives; the existing
runner checks for a single final result with More=false.

The flush subcase intentionally sends controlled down-shaped application terms
for real owned references. This guarantees pending queue data without depending
on when a real termination notification happens to arrive. It checks removal of
two matching terms and preservation of another reference's term/application data,
then verifies that the other monitor still delivers its real termination event.
It is not a claim about down-term authenticity or remote transport ordering.

adapters/local_promises.py gains an optional local-manifest mode using its
existing disposable fixture launch, pin checks and preservation machinery. It
runs one local pack per native candidate, without adding an outbound peer. The
promise-mode default selections remain unchanged. Baseline runner execution,
public goals in earlier packs and runtime implementations are untouched.

## Revisions and preservation

Native SWI source is exactly the demonstrator manifest pin
f316e65503bff863dfbd2e182f7487988c91480c, loaded from swi-prolog-node. Trealla source
is d4e96a3846577f0ebd4660aac4e81505702356e1 as identified in provenance.json; its recent cascade change is test-only. SWI uses the existing
separate verified 10.1.18 candidate with core 09b6299 and the HTTP shutdown patch.
Trealla uses the existing separate unmodified v3.14.10 engine and its matching
library. No version-string-only inference identifies the SWI prerequisite.

provenance.json records exact source/base revisions, working status, launch and
runner commands, node configuration, engine hashes and executed input hashes.
The shared adapter's inherited promise-manifest hashes are metadata, not claims
that promise cases were rerun in this local-pack batch. The executed local
manifest matches its launch hash; profile-input.json separately records the
profile document. New conformance code was uncommitted at execution, and is
identified by the eventual commit containing this evidence.

preservation.json confirms unchanged native Prolog sources, Trealla source/test
files, selected executable/library hashes and live n3/n5 identities. Both
fixture nodes were stopped after the run. installed-preservation.json confirms
installed executable targets/hashes still match the preceding preservation record.
No installed runtime, launcher, repository access setting or n3/n5 process changed.

## Limits

One six-case run per candidate is not stress/race certification. Remote monitors
and links, browser execution, GNU ACTOR, GUI, TLS, cross-client ownership, hostile
input, resource bounds and arbitrary shutdown races remain unmeasured. The
existing cascade investigation is independent historical evidence; the new pack
uses notification readiness rather than its former fixed-delay snapshot strategy.
No full runtime unit suite or prior diagnostic pack was rerun.
