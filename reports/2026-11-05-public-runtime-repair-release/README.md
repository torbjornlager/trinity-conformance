# Public runtime repair release — 5 November 2026

**Committed, pushed and deployed to N0–N6.** All twelve runtime/asset services
run clean images built from consumer commit `e00b4f95e131d21fd9213af648682f2394435276`. Later consumer changes
only update deployment documentation. The Trealla pin is
`197674e907955338458c23c3cecdc6f124e9448a`; GNU is
`626c350961e984fa2ab732ff75adc33f239cff57`. Native SWI and browser pins are unchanged.

The public N5–N4 ping-pong tutorial now completes, with all eight output messages
and normal actor completion. Inline remote output also passes with and without
loaded source. The private Trealla output helper stays out of exported code;
remote formatted SWI text renders normally.

`rpc(localhost, ...)` and `promise(localhost, ...)` now resolve the current node
on Trealla and contained GNU as well as native SWI. The exact reported N2-source
query returns six ancestor/descendant pairs on public N5 and N6. The GNU
controller and broker were deployed together with their matching lease protocol.

- All **36 pinned consumer CI groups** pass, including the runtime/consumer WASM
  scenarios and the new N6 broker/adapter regression groups.
- All **21 committed-source shared localhost assertions** pass on disposable
  SWI, Trealla and GNU listeners.
- The clean N6 image passes its public contract, **59 common HTTP-field checks**,
  five localhost cases, real worker/broker transport checks and Linux containment.
- All **139 selected public checks** pass: 60 readiness/asset/RPC checks,
  34 localhost RPC/promise/source checks, three N5–N4 output scenarios and
  42 real-Chrome ownership checks on all seven hosts in both execution modes.
- The upstream Trealla repair separately passed **88 unit groups and 71 interop
  groups**; its committed qualification includes output variable-sharing and
  supervisor admission controls.

Every updated service retains its environment fingerprint, runtime user,
resource/security controls and persistent mounts. Admission services and
operator credentials retain their existing configuration. Exact running pins
were checked in all twelve services. Rollback tags remain in
[rollback-images.json](rollback-images.json); disposable candidate containers
were removed.

[verification.json](verification.json) records exact revisions and evidence
hashes. [public-pingpong.json](public-pingpong.json) contains the observed tutorial
output; [public-localhost.json](public-localhost.json) records the retained local
node contract. These selected checks do not certify every Appendix B clause.
