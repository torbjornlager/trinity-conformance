# Public promise and capability release — 5 November 2026

**Committed, pushed and deployed to N0–N6.** Twelve runtime/asset services use
images built from clean consumer commit `080c7068893c2e0113237dcb76f253c394f070a1`.
The four runtime dependencies are exact commits; the browser package is clean
and its native schema provenance matches the consumer pin.

- All **34 consumer CI groups** pass, including **109 runtime/consumer scenarios**.
- The clean browser package passes all six qualification groups, including
  **102 semantic scenarios**, **59 ownership checks** in real Chrome/HTTP and
  **81 existing browser session checks**.
- All **132 selected live assertions** pass: 60 readiness/asset/RPC/transport
  checks, 30 shared runtime capability checks on N1–N6, and 42 browser checks
  loading the deployed assets from every N0–N6 hostname in both execution modes.
- The live browser checks use real N1 HTTPS calls. Same-context children collect
  parent promises; another browser context cannot collect or dispose of them;
  the owning context still collects after the foreign cleanup attempt.
- A disposable N6 passes its public contract, 59 HTTP-field assertions, actual
  contained worker/broker transport checks, and Linux containment controls.

Every replaced service preserves its environment fingerprint, runtime user,
resource/security controls and persistent mounts. Admission proxies and operator
credentials retain their existing configuration. Twelve rollback tags remain
available in `rollback-images.json`. Candidate containers were removed.

An initial N6 test harness ran from the wrong working directory. The corrected
candidate run passes; the original harness failure remains in `diagnostics`. The
initial live browser harness targeted the optional minimal-host download route.
The corrected run uses the supported public demonstrator page; its initial
diagnostics are also retained.

[verification.json](verification.json) records exact pins, source commits,
qualification scopes and evidence hashes. [rollout-results.json](rollout-results.json)
records image identities; [public-browser.json](public-browser.json) records the
live browser assertions. This release does not certify all Appendix B clauses.
