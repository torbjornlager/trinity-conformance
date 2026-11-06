# Public node URI and actor I/O release — 6 November 2026

**Committed, pushed, deployed and verified.** Runtime/asset images use consumer
`88ad749`. Exact [pins and validation](verification.json), [image builds](build-results.json),
[rollout](rollout-results.json), [running services](running-services.json) and
[rollback inventory](rollback-inventory.json) identify the release. Ten services
were updated. All sixteen surveyed services retain their environment fingerprints,
users, commands, resource/security controls and persistent mount identities.
The two GNU runtime images, admission services and credentials are unchanged.

The [development repair](../2026-11-06-node-uri-io/README.md) qualified trailing-slash
node identity and public copied I/O source on both native engines. The committed
runtime sources then passed the private ACTOR release gate: **44 cases each** on
SWI and Trealla ([gate provenance](actor-release/provenance.json)). Consumer
LINT, DEMONSTRATOR, DISCOVERY and WASM pass in one invocation
([log](consumer-tests.log.gz)). The browser update changes dependency provenance
only: [equivalence](browser-equivalence.json) confirms unchanged runtime and schema bytes.

Linux candidate images pass all **32 selected native URI/lifecycle tests**
([log](native-image-focused.log.gz)) and four Trealla groups for I/O, source capture,
URI validation and private workers ([log](trealla-image-tests.log.gz)). An initial
native-image command selected an unpackaged consumer test script; it executed no
tests ([diagnostic](native-image-tests.log.gz)). The corrected command uses the
upstream tests installed in the actual image. These results supplement the
prior full native and Trealla qualification; those tiers were not all repeated.

## Published UI results

- [N3/N4/N5 editor checks](ui-node-uri-io-final.json): **12 pass**. The actual
  `06 ping-pong.pl` Queries menu works; the reported local-ponger/remote-pinger
  variant prints the remote PID with its URI through copied `writeln(Self)`.
  Both slash spellings complete, actors return to their baseline, copied
  `write/1` works and a fresh query succeeds on every node.
- Native published tutorial ping-pong passes twice on each node, including cached
  connection reuse and baseline restoration: [N3](ui-native-tutorial-n3.json),
  [N4](ui-native-tutorial-n4.json), [N5](ui-native-tutorial-n5.json).
- [Browser tutorial checks](ui-browser-tutorials.json): **six pass** across the
  ACTOR, SWI-WASM and general tutorial documents in Worker and main modes,
  using the published N4 peer. Replies, terminal output and fresh queries pass.
- [Public HTTP/asset/RPC checks](public-verification.json): **45 pass, zero failures**
  across N0–N6, with exact asset hashes and the existing GNU presenter bootstrap.

The first new editor-variant harness used a transient tutorial load while the
editor still contained the original example. Its next query correctly reloaded
that original source, so the fixture predicate was absent. That
[initial harness result](ui-node-uri-io-initial-harness.json) is retained.
The corrected test edits and loads through the editor path. Test revision
`17d4f19` differs from the deployed consumer source only in that test file;
tests are excluded from the production image. The successful run uses the real
published pages without frontend or transport substitution.

This release checks the affected examples and selected release contracts. It is
not a complete tutorial catalogue rerun or full Appendix B certification. No
production policy, deadline or credential relaxation was needed. The
[drivers](rollout.py) preserve rollback tags and stop on invariant/readiness
failure; [evidence hashes](evidence-sha256.json) identify the retained inputs.
