# Generic-server wait conformance — 24 October 2026

## Outcome

All six identical public-interface cases pass on both disposable native
candidates: **12/12 selections**, with no failed, unsupported or diagnostic
outcomes. Both raw schema-2 reports and their accounting validate. All 15 runner
regressions pass, including failure-preserving coverage rendering for each local
pack. See [COVERAGE.md](COVERAGE.md) and the raw reports/logs.

This separately versioned draft does not amend baseline 0.1 or change an existing
profile. No failed candidate trial was retried, normalized away or repaired.
Runtime code and prior manifests/reports remain unchanged.

## Public assertions

SW-001 collects replies by reference in reverse request order. SW-002 collects
a later barrier reply to establish that earlier replies are available, then
requires a conflicting output to consume only its selected reply. Another
reference must still collect normally; a second attempt on the consumed reply
must time out rather than return it again.

SW-003 gates the server callback on an explicit release message. Its acceptance
handshake proves a zero-time yield occurs while the request is blocked; release
then permits collection of the same reference. SW-004 repeats this gated setup
while checking callback bindings, logical failure, a literal exception and an
exact [one,two] alternative list, followed by successful reply collection.

SW-005 checks server_down(sw_death) through both server_request/4 and monitored
server_yield/4, preserving an independent termination notification. SW-006
checks the monitored wait's timeout, mismatch and callback-exception cleanup,
late replies, unrelated application data, spawn-time monitoring and a separately
installed monitor. Zero-time checks after observed server termination find no
private wait-reference notifications remaining. Those checks are public mailbox
observations, not private registry/resource counts or a guarantee about arbitrary
future remote in-flight events.

The manifest submits the same sw_probe/4 source and goal strings to each public
ACTOR session. Callbacks announce request acceptance and wait for release/crash
messages. There are no sleep/1 calls, private runtime imports or per-runtime goal
rewrites. A barrier relies on the server's sequential handling of requests from
one caller, rather than a guessed time delay. Literal payloads and exact reference
matches are asserted; host-specific error contexts and pid formatting are not.

Existing runner query checks require one final success with no continuation.
SW-004 deliberately enumerates and asserts callback alternatives; this is not an
outer once/1 concealing extra query results. Each case has a fresh owning session,
consumes its expected notifications, retires explicit monitors and halts its
servers on success. Existing linked-session and disposable-node cleanup bound
failed fixtures. No cancellation or leak-free arbitrary-interleaving claim follows.

## Reproduction and provenance

The existing local-manifest fixture adapter starts two disposable loopback nodes
and runs one manifest selection per candidate, without an outbound peer. Native
SWI is loaded from the exact demonstrator dependency pin
f316e65503bff863dfbd2e182f7487988c91480c. Trealla uses the committed runtime recorded
in provenance.json, the separate unmodified v3.14.10 engine and matching library.
SWI uses the existing separate verified 10.1.18 candidate containing core 09b6299
and the HTTP shutdown patch; the version string alone is not its identity.

provenance.json identifies exact source revisions/status, executable hashes,
fixture/runner commands, profiles, sandbox settings and executed input hashes.
The new executed manifest matches its launch hash. Shared adapter metadata also
contains inherited promise-manifest hashes; they do not imply those cases were
rerun. profile-input.json records the separate contract document hash after the
run. New conformance inputs were uncommitted at execution and are identified by
the eventual commit containing this evidence.

The existing coverage renderer now takes an optional suite selector; its default
links-and-monitors path is preserved and unit-tested. Baseline execution code
and runtime repositories are unchanged. README provides the exact invocation.

## Preservation and limits

preservation.json confirms unchanged native SWI/Trealla sources, selected
engines/matching library and live n3/n5 process identities. Both temporary nodes
were stopped. installed-preservation.json confirms installed executable targets
and hashes still match the preceding preservation record. No installation,
launcher, repository access or live-node change occurred.

Remote servers, browser execution, GNU ACTOR, invalid-reference policy, transport
fault injection, monitored-callback alternative cleanup, cut/interruption,
competing collectors and wider lifecycle stress are unmeasured. No full native
unit suite, GUI, TLS, security or general lifecycle certification is claimed.
