# Native context attachment repair — 5 November 2026

The last-attachment decision and retirement of context admission now share the
actor registry mutex on both native runtimes. A concurrent attachment either
joins before retirement and preserves the context, or arrives after retirement
and cannot acquire a context that cleanup is about to close. Route and actor
cleanup runs after the decision's mutex has been released.

## Regression evidence

The [barrier-controlled race suite](attachment-race/results.json) contains four
positive checks and two negative controls. Both runtimes pass both orderings:
reattachment before retirement preserves the original open context; retirement
before reattachment closes admission atomically. The negative controls move
retirement outside the decision mutex in disposable source copies. Both must
reproduce a successful attachment followed by closure of its namespace. The
adapter reports a control as passed only when that unsafe outcome is observed.

The test-only barrier is inserted at the actual retirement call. No installed
engine, source checkout or public node is changed by the adapter. Original and
instrumented module hashes, committed revisions, generated observations and the
[adapter source](local_attachment_race.py) are retained.

All **51 context probes pass** on the committed native revisions, including all
four directed native route combinations: [results](contexts/results.json).
The original failed audit and earlier repair reports remain historical evidence.
The Appendix B ledger retains unverified status for whole source units whose
remaining obligations have not yet been mapped.

## Release preparation

Trealla's deployment launcher now accepts `WP_PEER_TRANSPORT_TOKENS_FILE`, using
the same owner-only, destination-bound list format as the SWI launcher. It
rejects malformed files, trailing terms, non-HTTP destinations and header
newlines without printing secrets. All [eight launcher checks](trealla-peer-config.txt)
pass. Actual owner credentials remain outside Git.

The consumer adds separate N5 read-only bind/volume overlays, applied after the
public N5 overlay. [Three real Compose merge checks](n5-compose-tests.txt) verify
both mount variants retain public state/log volumes and demonstrate that the
wrong overlay order discards the credential mount. The existing N3/N4 credential
overlays are preserved. [Existing peer-file checks](consumer-peer-tests.txt) pass.

The native and Trealla revisions are pinned in the consumer. Browser executable
code is unchanged; its native schema provenance and package manifest are updated
to the new native commit. The standalone package passes all seven qualification
groups, including real Chrome standard-library and session API checks:
[browser results](browser-package-tests/results.json).

The full [38-group consumer CI](consumer-ci/results.json) passes, as does the
[full native suite](swi-full-suite.txt). Consumer CI ran the final working tree
before commit; its original provenance records that base HEAD. The environment
record identifies the commit of those unchanged tested files.

The clean [Trealla full unit-and-interoperability run](trealla-full-suite.txt)
passes in one invocation (`TEST_TIMEOUT=180 TEST_STARTUP_DELAY=1 tools/test.sh all`).
An earlier [invalidated run](trealla-invalidated-first-run.txt) reached the final
checks but failed shell parsing after the runner was edited while active. The
committed, frozen runner was rerun from the beginning; its complete exit result
is zero.

Public node images, credentials and services remain unchanged;
this is qualification for release, not a deployment certificate.
