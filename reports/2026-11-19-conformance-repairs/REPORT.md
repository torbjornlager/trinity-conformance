# First conformance repair batch — 19 November 2026

Four candidate fixes are implemented and verified locally. They are **uncommitted
and not deployed**. This targeted follow-up does not replace the
[full run](../2026-11-19-deployed-conformance/REPORT.md) or qualify the remaining
context requirements. No manifest assertions or runtime isolation contracts
were changed.

## Changes and evidence

| Change | Verification |
|---|---|
| Merge native common and per-case helper source instead of overwriting per-case source | Both native engines now execute all helper-dependent monitor cases; 94 pass / 4 fail across 98 observations. Remaining failures are MC-028/029 on both engines, unchanged URI expectations. |
| Load source-dependent WASM packs through the maintained real Chrome session adapter | Node-settings passes 14/14 in Worker and 14/14 in main, including the formerly missing `ns_read/2` helpers. Source-free cases retain independent embedded processes. |
| Correlate noncompletion entry by dedicated listener instead of URL path | SWI, Trealla and GNU pass 3/3. Each warmup/probe/recovery has its own loopback endpoint. Entry, bounded observation, forced termination and recovery requirements are unchanged. |
| Expose SWI's existing `promise_cleanup/1` through the actor API, RPC family policy and sandbox allowlist | CTX-003 and all CTX-019 routes pass. New ownership regressions exercise the public import/admission chain: foreign cleanup preserves the promise, owner cleanup disposes it, and repeated cleanup is harmless. |

The entry fixture failed because SWI RPC replaces a base URI path with `/call`.
The old peer counted the request under the wrong key; its zero-entry result was
not evidence about countall. The new fixture keeps each phase on a separate
listener and retains exact-one-request assertions, without changing deadlines.

The WASM routing fix changes the execution boundary for source-dependent packs:
those results are real browser session observations, not embedded coordinator
observations. The adapter preserves successful rows when another assertion fails,
and rejects a nonzero subprocess exit that supplies only passing rows.
Regression tests cover source composition, selected mode, process isolation and
exit-status handling.

Native SWI's cleanup implementation and ownership checks were already present.
The missing public export and admission entries caused `Unknown procedure` in
public client execution. The fix exposes that implementation through the existing
RPC family; it adds no owner override or new internal disposal primitive.

## Verification

- **114 runner tests pass**, using explicit Node 22.23.4.
- SWI **LINT, TEXT, T0, T1_NATIVE, T2, T3_NATIVE, T4_NATIVE and T5 pass** on
  verified SWI-Prolog 11.0.0. T4_NATIVE includes the WebSocket origin and HTTP
  visitor ownership checks. After adding the focused API regressions, the
  **27-test promise-ownership suite passes**.
- The complete 61-row controlled context selection records **42 pass / 15 fail /
  4 blocked / 0 error**, compared with 39/18/4/0 in the full run. The three
  improved rows are SWI CTX-003 and CTX-019-swi-b from SWI and Trealla.
- No live service was restarted or reconfigured. Baseline Compose container IDs
  and image IDs remain unchanged. The owned repair lab was removed after export.

Initial host attempts encountered an unsuitable local Trealla configuration and
an unsupported default Node 10.16.3. Their artifacts are retained privately;
primary cross-engine observations above use the pinned Linux lab and Node 22.
No installed engine or host default was changed.

Results are under [observations](observations), source hashes and environment
information under [provenance.json](provenance.json), and the service comparison
under [preservation.json](preservation.json). Test log hashes are recorded in
[verification.json](verification.json); full logs and initial attempts remain
in the private artifact directory named in provenance. This is a focused rerun,
not a rerun of all 76 manifests. The full run's original files remain unchanged.

## Decision needed before the next context batch

Current runtime contracts conflict with several older conformance assumptions:

- SWI's `docs/WEB_PROLOG_BUILTINS.md` explicitly permits authenticated stateless
  HTTP requests from one principal to share promises. CTX-010 requires the
  opposite. Anonymous requests remain isolated and their check passes.
- Trealla's README explicitly makes ordinary-name lookup and uniqueness
  node-wide. CTX-006/007/008 require separate client name visibility,
  uniqueness and withdrawal rules.
- Current transport lineage is scoped to its accepted connection. Trealla
  explicitly documents receiver-side support without downstream delegation.
  The old round-trip scope and last-attachment controls depend on functions
  removed by that design. Replacing a source-patch needle cannot restore the
  semantics those controls measure.

The pending choice is whether to preserve these documented contracts and version
the conflicting tests, or undertake a deliberate runtime semantics change.
The recommendation is to preserve the contracts and version the tests, retaining
all old failures. Until that choice is settled, attachment/return-barrier controls
remain incomplete and the context gate remains red. No old expectation was
weakened or relabeled as passing in this batch. Browser callback/naming and the
remaining transport/document failures also remain open.
