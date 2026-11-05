# Public successor repair release — 5 November 2026

**Committed, pushed and deployed to N5.** The backend runs consumer image source
`a44c23d`, pinned to Trealla port `5741bd7`. Its engine source remains the pinned
Trealla 3.14.20 revision; native SWI, GNU and browser pins are unchanged. Eleven
other runtime/asset services retain their previous image identities.

The shared successor implementation validates supplied integer arguments before
choosing a direction. Client and owner-off calls, callbacks, receive code and
private/copied source agree on the documented formal errors. No manuscript or
admission-policy change was needed. The [development qualification](../2026-11-05-trealla-succ-repair/README.md)
retains the original failures, the incomplete guarded-path attempt and the final
full native unit/interoperability result.

## Qualification and rollout

- All 38 [consumer CI groups](consumer-ci/results.json) pass in one invocation,
  including the complete WASM group; no qualification rerun was needed.
- Two images were built from the committed consumer archive. The actual Linux
  N5 image passes 311 individual/nested/batched library controls and the focused
  callback/receive/copied-source/owner-off regression.
- [Rollout](rollout-results.json) preserves N5's exact environment fingerprint,
  user, entrypoint, resource/security controls and state/log/credential mounts.
  [Rollback image and prior service identities](before-services.json) remain.
- [Installed runtime pins](running-runtime-pins.json) match every running target;
  all [123 root Prolog files](running-n5-source.json) match committed Trealla
  `5741bd7`. N5 is healthy, and all eleven other images are unchanged.
- The N3–N5 source/spawn policy is unchanged. N5's self-route peer credential
  survives restart, remains scoped and active, and is owner-only (UID 10001,
  mode 0400) in the existing read-only volume. No secrets are stored here.

## Public verification

**268 selected public assertions pass**, without failures or policy exclusions:

| Selection | Passes |
|---|---:|
| All shared library cases on public N5 | 146 |
| Source-free public successor error terms | 2 |
| Native retained contexts on N3/N4/N5, all four routes and returns | 51 |
| External source/spawn denial and session recovery controls | 6 |
| N5–N4 tutorial and inline ping-pong controls | 3 |
| Public readiness, exact browser bytes and cross-node RPC/promise smoke checks | 60 |

Each selection has its own JSON observations. All temporary execute-only test
credentials were revoked in the wrapper's finally block; the owner peer
credential remains configured. This public selection is separate from the
1,024 development observations and the 311 Linux candidate controls; their
counts are not added to the live total.

The ledger remains at 28 covered library obligations and 15 requiring additional
tests. Full Appendix B and external ISO certification are not claimed. The
historical intermittent context timeout and browser CI failure remain recorded
in their earlier reports; this release neither reproduced nor diagnosed them.

Only N5 required deployment for this repair. The consumer documentation follow-up
and conformance release commit do not change the deployed image source `a44c23d`.
