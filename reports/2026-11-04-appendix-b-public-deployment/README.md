# Appendix B public-node deployment — 4 November 2026

**Committed, pushed and deployed to N0–N6.** Twelve runtime/asset services now
use the new pinned images. Admission proxies, resource limits, operator
credentials and persistent volumes retain their existing configuration.

The images were built from clean committed consumer source
`b3f06c597e6bf189449687ebca4540ba9b749139`. Consumer qualification at
`c74f815a00d0c022676c7177d083d922b24ad2da` changes only test fixtures; it
has identical deployed runtime files and dependency pins. The browser package
is a clean release with matching native schema provenance.

## Verification

- **354/354** shared HTTP-field assertions pass on public N1–N6.
- **42/42** creation/supervisor assertions pass on public N3–N5.
- **60/60** readiness, exact browser/Worker asset, cross-node HTTP field,
  promise and pinned-Host checks pass, including all 35 permitted RPC directions.
- All **34** pinned consumer CI groups pass with the retained full WASM follow-up;
  that final run covers **107** selected runtime/consumer scenarios.
- Candidate N5 saturation, Linda and URI source policies pass. Candidate N6's
  actual contained worker/broker custom fields and Linux containment checks pass.
  Live N6 public-contract and N5 statechart/source-policy checks also pass.

The initial consumer tests still matched obsolete private signatures and
Boolean errors; their corrections are committed and the full browser tier was
rerun. The initial SC-001 fixture expected an asynchronous failure notification;
it now checks the specified wrapped caller exception, unbound output and rollback.
An overlapping public test batch hit N1's existing rate cap. The successful
rerun paces HTTP assertions at 1.5 seconds; limits were retained. Earlier failures
remain in the evidence and diagnostics.

[verification.json](verification.json) records pins, scope and evidence hashes;
[rollout-results.json](rollout-results.json) records image identities;
[rollback-images.json](rollback-images.json) retains restoration tags.
[pinned-ci-followup.json](pinned-ci-followup.json) reconciles the original
CI run with its successful full WASM rerun. This is a scoped deployment
qualification, not complete Appendix B conformance.
