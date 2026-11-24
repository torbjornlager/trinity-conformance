# Full live conformance after the third-party send releases — 24 November 2026

Fresh execution of **82 manifests / 2,085 input rows** at suite `8e3408072321cfd1f6c4911a448bca45a62ef7bb`, against the live nodes after the 24 November releases (N7 relay robustness and third-party sends, N5 third-party sends and follow-up). Every result was executed for this run; nothing was copied from earlier runs. Repeated cases, versions, transports and nodes are separate observations, not independent defects or a conformance percentage.

[Per-file outcomes](SUMMARY.json) · [case inventory](verification.json) · [comparison with 21 November](COMPARISON.json) · [frozen inputs](suite-inputs.json) · [provenance](execution/provenance.json) · [preservation](preservation.json) · [orchestration changes](execution/orchestration-changes.json)

## Runtime selection and conditions

N0–N4 and admin: native SWI `67f0b17` / SWI-Prolog 11.0.0, demonstrator `c5ebc76`, browser `1d6ee0d`. N5: Trealla `47b9e1d` / 3.14.20. N6: gprolog-port `8eeb3f8` with the N6 adapter. N7: eclipse-node `44b3900` adapter and worker. Owned native fixtures use snapshots of these deployed images.

The orchestration is the 21 November sweep's, with only paths, dates and pins changed. The other changes are listed in [orchestration-changes.json](execution/orchestration-changes.json) and [fixture-setup-corrections.json](execution/fixture-setup-corrections.json): the browser lab base image was rebuilt, and a controller was added for the new `cross-node-actor-0.1` manifest. Admission budgets and pacing are unchanged. No runtime, setting or quota changed during the run.

Suite changes since 21 November (`a7a4a7b` → `8e34080`): one added manifest, `cross-node-actor-0.1`, and its runner. Runner self-tests: 126 pass.

**N5 restarted during the sweep.** At 20:06 UTC its Trealla process was killed at the container's 1 GiB memory limit (log: `Killed`) during the live standard-library phase, and Docker restarted the container. After the sweep N5 was back at about 1 GiB while idle and was restarted in a controlled way. The fix belongs in trealla-port; the 23 November flood incident showed the same retention.

## Primary public selections

| Node | Profile | Fresh result |
|---|---|---|
| N0 | RELATION | 1 pass |
| N1 | ISOBASE | 12 pass |
| N2 | ISOTOPE | 12 pass |
| N3 | ACTOR | 118 pass |
| N4 | ACTOR | 118 pass |
| N5 | ACTOR | 118 pass |
| N6 | ISOBASE | 12 pass |
| N7 | ACTOR | 118 pass |

## Cross-node actors

`cross-node-actor-0.1` over N3, N4, N5 and N7 from every caller: XN-001 pass, XN-002 pass, XN-003 pass, XN-004 pass (148 combinations, all passing). On 24 November before the releases, XN-001..003 failed 96 of 144 pair combinations.

The generic per-node runner also met this manifest and recorded 16 rows for N3, N4, N5 and N7 as failures ("No public handler"): it has no handler for pair-topology cases. They are classified `invalid_harness_pair_topology_requires_cross_node_runner` and left out of the counts below.

## Comparison with 21 November

Rows are matched by file, case, candidate and occurrence ([COMPARISON.json](COMPARISON.json)). **6 rows changed from fail to pass, 52 from pass to fail, and 133 still fail** (harness rows excluded).

| Node / fixture | Failed 21 Nov | Failed 24 Nov | Fixed | New failures |
|---|---|---|---|---|
| n1 | 4 | 4 | 0 | 0 |
| n2 | 4 | 4 | 0 | 0 |
| n3 | 13 | 13 | 0 | 0 |
| n4 | 13 | 13 | 0 | 0 |
| n5 | 13 | 60 | 0 | 47 |
| n6 | 6 | 6 | 0 | 0 |
| n7 | 22 | 22 | 0 | 0 |
| fixture:gnu-direct-api | 2 | 2 | 0 | 0 |
| fixture:swi | 27 | 27 | 0 | 0 |
| fixture:swi-wasm-main | 1 | 1 | 0 | 0 |
| fixture:swi-wasm-worker | 1 | 1 | 0 | 0 |
| fixture:trealla | 29 | 30 | 6 | 3 |
| fixture:trealla-to-swi | 0 | 2 | 0 | 2 |

Fixed: receive-guard controls RG-001..003 and RG-005..007 in the owned Trealla fixture, the 21 November regression, repaired by the N5 rg-fix release on 23 November.

## New failures

- **N5 standard library (41 rows):** the rows that ran while N5 was killed and restarting; the same cases pass on every other node and in the owned Trealla fixture.
- **IX-001 and IX-003 on N5 and in the owned Trealla-to-SWI fixture:** a real regression from trealla-port `fd0907a` (24 November). A synchronous remote toplevel call sent its reply route, `target(Self)`, as a qualified pid, so the peer replied over another connection instead of the one where the call waits. Reproduced locally (`2924726` passes, `fd0907a` fails); fixed on trealla-port branch `sync-reply-route`, not yet released.
- **Retained-context Trealla-to-Trealla rows in the owned fixture** (CTX-012, CTX-018 and CP-001 to `trealla-b`, with dependent CTX-013..019 now blocked or failing): since `fd0907a`, a Trealla node with a public URL sends its pids as `Id@URL`. A Trealla node that holds no peer credential for it cannot then reply over a new connection, while earlier per-connection return handles allowed a reply on the same connection. The live nodes hold peer credentials and pass the cross-node cases. Whether unpeered nodes should be able to reply is a node-to-node trust question (see the distribution agenda in trinity-demonstrator), not yet decided.

## Remaining failures by category

Rows that do not match a recorded category are left unclassified rather than guessed.

| Category | Rows | Packs |
|---|---|---|
| Superseded 0.1 assertions (the 0.2 pack passes on the same node/fixture) | 47 | monitor-contracts-0.1, monitor-preflight-0.1, node-uri-io-0.1 |
| N5 was killed at its memory limit during this phase (20:06 UTC) and restarted | 41 | standard-library-0.1 |
| Unclassified: unchanged since 21 November, needs triage | 32 | (aggregate adapter), browser-local-compatibility-0.1, isobase-diagnostics-0.1, isobase-error-admission-0.1, node-uri-io-0.2, partial-page-errors-0.1, retained-context-0.1, statechart-document-0.1 |
| Out-of-scope rows (profile or environment exclusion) | 24 | browser-local-compatibility-0.1, isobase-error-admission-0.1, relation-error-admission-0.1 |
| Live prerequisite missing: needs a peer serving local_node_loaded/1 | 14 | local-node-rpc-0.1 |
| Regression: Trealla fd0907a sends the synchronous reply route as a qualified pid (fix on trealla-port sync-reply-route) | 8 | (aggregate adapter), interop-actor-0.1 |
| Changed: Trealla nodes without peer credentials cannot reply to each other's qualified pids (policy question) | 7 | retained-context-0.1 |
| GNU classification and NUL representation (expected to remain) | 5 | (aggregate adapter), error-contract-0.1, http-fields-0.1 |
| Sandbox-only rows on N7 (should be not applicable with sandbox off) | 4 | native-supervisor-lifecycle-0.1 |
| N7 design gap: one peer connection per spawn | 2 | node-uri-io-0.2 |
| N7 defect: explicit limit plus timeout returns a truncated page | 1 | partial-page-errors-0.1 |

## Live standard library

842 rows per transport, original source and assertions.

| Node | Stateless HTTP | Retained WSS |
|---|---|---|
| N1 | 842 pass | not exposed |
| N2 | 842 pass | not exposed |
| N3 | 842 pass | 842 pass |
| N4 | 842 pass | 842 pass |
| N5 | 842 pass | 801 pass, 41 fail |
| N6 | 842 pass | not exposed |
| N7 | 842 pass | 842 pass |

## Finite admission

980 fresh finite HTTP probes, 140 per node on N1–N7, 0.6 s apart after all other endpoint work; outside manifest row counts. Overall: pass.

| Node | Probe result | Admission policy unchanged |
|---|---|---|
| N1 | pass | True |
| N2 | pass | True |
| N3 | pass | True |
| N4 | pass | True |
| N5 | pass | True |
| N6 | pass | True |
| N7 | pass | True |

Blocked, unsupported and inapplicable rows are accounted for without being called passes; every unexecuted row keeps its reason in verification.json. Persistent service container and image IDs match the pre-run snapshot, and all owned fixture containers were removed.

[Completion checks](execution/completion-verification.json) · [runtime restarts](execution/runtime-restarts.json) · [artifact hashes](files-sha256.json)
