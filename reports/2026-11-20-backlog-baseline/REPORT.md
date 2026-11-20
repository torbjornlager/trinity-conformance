# First conformance backlog batch — 20 November 2026

**A current issue inventory is available, the URI contract drift is corrected in source/tests, and two local runtime preflight repairs cover six failing timeout cases. Production is unchanged. Complete Trealla unit qualification remains blocked.**

[Current issue inventory](../../CURRENT_ISSUES.md) · [summary](SUMMARY.json) · [source patches](candidate-source.json).

## What the current inventory says

The frozen full sweep contributes 416 applicable failed observations and 387 blocked projections after explicit profile/harness exclusions. The reviewed dispositions distinguish 121 N6 capacity observations with passing expiry controls, 32 repeated stale monitor expectations, 19 missing-route fixture failures, two observations of the deployed SWI retirement repair, and one passing N6 replay whose original cause is still open. **241 failed observations remain unresolved.** These are repeated observations across cases, versions, routes and nodes; they are not 241 independent defects. Candidate fixes remain open in the production column.

The 387 blocked projections are separate from the four versioned input rows with no completed execution anywhere in the full sweep. Those four retained-context return assertions remain incomplete. The generator preserves each source file, JSON pointer, candidate, classification and outcome. Reviewed decisions require matching proof; historical hashes are checked and the old reports are not edited.

## URI contract and monitor version correction

The shared HTML manual still contained the atom-only proposal. The demonstrator's dated 17 November author-directed decision explicitly supersedes that proposal: URI atoms, string objects and proper character/code lists are accepted, including monitor targets; Host:Port compounds are rejected. [Contract provenance](contract-review.json) retains the conflicting wording and the governing decision.

The runtime monitor implementation is preserved. The manual source and stale README text are corrected to the recorded decision. No URI runtime semantics or live assets are changed in this batch.

`monitor-contracts-0.2` and `monitor-preflight-0.2` replace the two stale rejection assertions with positive checks that URI text and the atom address monitor the same actor, produce independent references and deliver the expected down notification. An additional case covers character lists. All other case bodies and helper source remain identical; the old 0.1 files remain unchanged. The maintained monitor release runner now selects 0.2. [Version hashes](manifest-versions.json).

Both complete packs pass on disposable SWI and Trealla nodes: [100/100](monitor-contracts-v2.json) and [50/50](monitor-preflight-v2.json). The three representation checks also pass on live N3/N4/N5/N7 ([12/12](live-monitor-text.json)) and in real Chrome Worker/main modes ([6/6](browser-monitor-text.json)). This supports the version correction; it does not close unrelated monitor or URI-transport findings.

## Numeric RPC/promise timeout validation

The unchanged 20-case timeout pack reproduces four SWI failures and two Trealla failures: [before evidence](validation-before.json). SWI accepted explicitly supplied variable/none execution timeouts through an internal omitted-value normalizer. Trealla's public request validator accepted the atom infinite. The common manual requires numeric values and validation before source loading or dispatch.

The SWI candidate validates supplied values numerically while retaining the internal default used for omission. The Trealla candidate requires numbers for request timeout options; its separate yield behavior is unchanged. Successful unit vectors use numeric request timeouts, and explicit invalid-value regression checks cover failure before source/resource side effects. No existing conformance timeout assertion is relaxed.

The unchanged timeout pack now passes **20/20 on each runtime**. The combined final selection, including six revised URI-monitor observations, passes [46/46](validation-candidate.json). Final SWI LINT, TEXT and T4_NATIVE pass, including 1,098 node-tier tests, WebSocket origins and HTTP visitor ownership. Focused Trealla RPC option tests pass. The source candidates are [reviewable patches](candidate-source.json), not dependency pin updates or deployed changes. This is a preflight repair, not proof that Trealla's legacy destination/transport timeout projection fully implements the common contract; that remains queued.

## HTTP prompt fixture correction

The 19 historical Trealla HTTP 404s came from a standalone fixture without retained HTTP routes. `adapters/local_http_prompts.py` explicitly enables http_sessions(true) and owns/cleans up its disposable nodes. Both correctly configured fixtures pass the unchanged [38 prompt assertions](http-prompts.json), with [source provenance](http-prompts-provenance.json).

The maintained runner now probes spawn/halt once before asserting prompt behavior. A real disabled-route control returns a failing run with one setup error and [19 blocked cases](prompt-disabled.json). Missing routes are never counted as passes. Preflight unit tests also check cleanup, non-execution of blocked assertions and preservation of ordinary assertion failures. All **123 runner unit tests pass**.

## Qualification blockers retained

The broad macOS Trealla unit run stops at the sandbox/cascade group's unchanged 30-second watchdog after t144. An unmodified 2d5042b archive reproduces that outcome. [Both observations](qualification-limitations.json) and the original/retry logs are retained. Eight subsequent governance/resource/source-policy groups pass separately; this does not turn the complete suite green.

An isolated Linux qualification uses byte-identical live N5 engine/library files. Its complete unit run stops at the HTTP cache-eviction group's 30-second watchdog after four successful checks. The exact unmodified-source group control reproduces the timeout. [Linux qualification](trealla-linux-qualification.json), [baseline control](trealla-linux-baseline-cache.json), and [both outcomes](linux-qualification-limitations.json) remain explicit. These are pre-existing qualification blockers with unproven causes, not evidence that the numeric-timeout patch introduced them. No timeout was increased and no failing assertion was deleted.

Production services, pins and recovery selections remain unchanged. Owned probe processes/containers are removed. The next release step requires resolving or properly qualifying these cleanup blockers; the current inventory keeps the other runtime and fixture findings open. Exported artifacts are covered by [SHA-256 hashes](files-sha256.json).
