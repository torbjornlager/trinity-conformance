# Native retained-context release — 5 November 2026

**Committed, pushed and deployed to N0–N6.** All twelve runtime and asset services
run images built from consumer `3c8702ade852837ed8ac9d8895e33110a418862e`.
Exact installed pins match native SWI `c826111`, Trealla `62e93c3`, and browser
package `f5fbafb`. GNU retains its previously qualified runtime pin.

The native context repairs now run publicly: fresh authenticated HTTP requests
have distinct promise owners; native descendants retain their context on remote
return; Trealla ordinary names isolate clients; and last-attachment retirement
is atomic. SWI publicly exposes promise cleanup and Trealla exports public goals
without private sandbox wrappers. The [source qualification](../2026-11-05-native-context-attachment-repair/README.md)
records 51 passing context probes, four deterministic attachment checks and two
negative controls, 38 consumer CI groups, full native/Trealla suites and seven
browser package groups.

## Deployment and credentials

Six clean images were built from the committed consumer archive. The Linux N5
candidate passed 238 library controls. The N6 candidate passed the public
contract, 59 HTTP-field assertions, actual worker/broker checks and Linux
containment. [Rollout](rollout-results.json) records all twelve service updates;
[installed pins](running-runtime-pins.json) and [rollback images](rollback-images.json)
are retained.

Every service retains its runtime user, resource/security controls, admission
settings and existing state/log volumes. N5 additionally receives the qualified
read-only owner peer volume. Its self-route credential was issued through the
private owner administration API, persisted in the existing N5 token store,
mounted as UID 10001 mode 0400, and verified in use after restart. No bearer or
administrator secret is stored in this report. N5 → N3/N4 keeps the pre-existing
owner-configured private-Docker trust boundary; no admission allowlist was widened.

## Public verification

**2,421 selected public checks pass**, with zero failures in permitted operations:

- 42 native context checks on N3/N4/N5, repeated successfully: fresh HTTP and
  retained sessions, name and promise isolation, remote sibling sharing,
  native remote return and N5's authenticated public self-route.
- 672 required-library assertions on public N1–N6.
- 1,568 required-library assertions in real Chrome on N0–N6, in worker and main modes.
- 60 readiness, exact-asset, cross-node HTTP-field and promise checks; 34 localhost
  and caller-fetched-source checks; three N5–N4 ping-pong/inline checks; and
  42 browser promise ownership/transport checks.

**Nine context cases are excluded by existing deployment policy.** N3/N4 do not
allow spawning at N5, and N5 does not allow spawning at N3. The final context run
uses N3 → N4, N3 → N5, N5 → N4 and N5's public self-route: N3 → N5's seven cases
are excluded, as are the two N5 → N4 → N5 return-spawn cases. The unchanged
[running spawn policy](public-spawn-policy.json) is recorded. Permitted remote
returns are verified on N3 → N4 → N3 and N5 → N5 → N5. These are explicit
coverage boundaries, not passing assertions for forbidden routes.

The initial probe selected some forbidden directions and recorded their actual
permission errors; [that attempt](public-contexts-initial-policy-attempt/results.json)
is preserved. The final [context results](public-contexts/results.json) report
42 passes, nine policy exclusions, zero failures and zero fixture errors. An
[independent permitted-route run](public-contexts-first-permitted-run/results.json)
agrees. Temporary execute-only test credentials were revoked after verification;
the owner self-route credential remains configured.

The complete language contract and external ISO mode/error inventory remain
outside this selected release certificate. Existing source-unit verification
counts are not promoted merely because these probes pass.
