# OPEN exercises and HTTP context repair — 19 November 2026

**All 34 visible drawer entries now pass all 136 checks in anonymous OPEN mode.**
This includes the intended Prolog failure/error examples, every fridge recovery
follow-up, and all fourteen statechart sequences. Fresh HTTP requests remain
isolated even with matching credentials; sharing across queries uses an explicit
retained WebSocket or HTTP session. No login requirement was added to OPEN.

## Cause and repair

The ten timeouts in the [previous checkpoint](../2026-11-19-open-http-contract/REPORT.md)
shared a native runtime defect. The fixture hosts two node listeners in one
SWI process. An actor's start-goal node context unwound before its thread's
`at_exit` callback ran. Retirement then canonicalized its PID using the last
registered listener instead of its creating node. Name withdrawal and monitor
lookup used the wrong identity, so waiting programs never received their
termination messages.

The actor layer now supplies a caller-side `hook_stop_context/2` boundary for its
retirement callback. Node composition captures the creating port and reinstalls
that context during retirement. Registry cleanup, monitor delivery and lifecycle
hooks therefore operate on the correct node without upward imports in the
standalone actor layer.

Correct retirement also exposed a race where a remote child's ownership record
could disappear between removing its parent link and requesting its termination.
Internal dependency teardown now follows the recorded parent edge directly.
Explicit public `exit/2` still performs its admission checks. A regression proves
that a public exit-policy rejection does not prevent runtime dependency cleanup.

The inherited-terminal test now keeps its linked parent alive until the remote
writer receives the browser acknowledgement. It still requires the actual
acknowledged output; it no longer relies on a child surviving parent retirement.

The parallel combinator and fridge teaching algorithms did not need changes.
Their missing monitor notifications, and the statechart halt timeouts, disappear
when the runtime retires actors under the correct node context.

## Verification

| Check | Result |
|---|---|
| Visible drawer, without credentials | **34 entries / 136 checks pass**, exact inventory and query count checked |
| Fresh requests and local contexts | **23/23 pass** |
| Retained HTTP sessions, anonymous and equal credentials | **6 executions pass** |
| Retirement regression | **4 executions pass**: success, failure, exception, protected public exit versus runtime dependency cleanup |
| Controlled negative: remove only retirement context | All **3 context variants fail**; the dependency-cleanup control still passes |
| Native LINT, T0, T1_NATIVE, T2, T3_NATIVE, T4_NATIVE, T5 | Pass; T4 has **1,097 named tests**, plus origins/visitor controls |
| Exact consumer integration and service selections | All nine selected tiers pass |
| Conformance runner unit tests | **114 pass**, Node 22.23.4 |
| Empty exercise inventory control | Correctly rejected; no empty selection can qualify |

The [drawer observations](open-exercises.json) contain the exact anonymous query
sequences, expected terminal types, source hashes and observed events. Every
visible source is fetched through the public asset route. The checker reads the
current drawer curation, rejects missing/duplicate/empty inventories and checks
the total number of executed queries. Intentional failure/error examples count
only when their documented result is observed. The extra links control proves
an unlinked child survives its immediate parent inside its retained client.

HTTP observations are [anonymous sessions](http-open.json),
[authenticated sessions](http-authenticated.json) and
[local contexts](local-contexts.json). They retain producer-arrival/release,
foreign-yield/cleanup and owner-collection controls. No timeout was enlarged.

The [retirement positive log](retirement-positive.log),
[controlled negative log](retirement-controlled-negative.log) and
[negative patch](negative-without-retirement-context.patch) establish the cause.
The negative modifies only a disposable worktree; it is not a portable language
pass or a change to the installed engine. Earlier failed records remain intact.

The final [native log](native-final.log) and [consumer log](consumer-final.log)
record the broad checks. Consumer selections are T1_INTEGRATION,
T3_INTEGRATION, T4_INTEGRATION, DEMONSTRATOR, SERVICE_TEXT, LINDA, MODEL,
MODEL_SXML and JEV. Service/inference tests use owned fake backends. The currently
hidden entries are outside the 34-entry drawer selection; these service suites
provide additional coverage, not an exhaustive live-provider claim.

## Published changes and adoption boundary

- Native retirement repair: `47e640f`, on `codex/welcome-release-20261113`.
- Native HTTP ownership and retained-client unlinking: `a2ff186`, same branch.
- Trealla HTTP-session namespaces: `3a5b761`, on `main`.
- Demonstrator OPEN checker and compatibility notes: `2c4283e`, on `main`.

The consumer qualification used clean, exact private candidate pins. The native
runtime and test files are byte-identical to the published native source.
Browser schema provenance required a private metadata package, whose engine,
worker, runtime and schema hashes match the original browser package.
[Candidate identifiers](private-candidates.json) and [summary](SUMMARY.json)
record that distinction.

Production dependency pins still select native `26e1ce7`, browser `0363b38` and
Trealla `6041ea3`. No live node, installed engine, deployment configuration,
principal quota or trust setting changed. Adopting the published runtime
commits and deploying them remains a separate release step. Demonstrator CI
checks its current production pins; candidate runtime qualification is the
explicit local evidence above.

## Reproduction

```sh
python3 tools/test_open_exercises.py --swipl /path/to/swipl \
  --native-root /path/to/swi-prolog-node \
  --runner /path/to/trinity-conformance/runner/run.py --output /fresh/report
```

The checker starts two owned listeners bound to loopback in one process,
preserving the regression condition. External example URLs are mapped to owned
local node/source fixtures. Queries use a fixed 15-second deadline, including
WebSocket ping/pong frames. See the
[HTTP session profile](../../profiles/http-session-context-0.1.md) for anonymous
and authenticated session commands.

SWI 11.0.0 and Trealla 3.14.20 with its matching library supplied the native
checks; the browser engine remains 10.1.19. Private worktrees, initial attempts
and fixtures are retained under
`trinity-demonstrator/.trinity/open-http-20261119/exercise-repair`.
[Export hashes](files-sha256.json) cover this record. The owned mixed-runtime
Docker lab is removed after exporting its results.
