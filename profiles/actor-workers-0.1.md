# ACTOR Workers 0.1

Status: **draft executable profile**  
Required advertised node profile: `actor`  
Wire protocol version: `1`

This opt-in profile specifies the observable worker-combinator contract shared
by native SWI and Trealla. It does not change ACTOR Core or ACTOR Behaviours 0.1.
Passing it means passing the listed cases, not all possible worker lifecycles.

## Contract and cases

| Case | Required observation |
|---|---|
| WC-001 | `parallel([])` succeeds; independent goals return their first bindings. |
| WC-002 | A failed parallel goal makes the call fail; a thrown term is propagated intact. |
| WC-003 | Both `first_solution` arities return one winner; an empty solver list fails. |
| WC-004 | Continuing after failure, exception or unexplained exit preserves the eventual winner and leaves no extra paging continuation for these single-result queries. |
| WC-005 | An unexplained exit is `worker_exit(Pid,Reason)`; stop policies fail or propagate the original exception as documented. |
| WC-006 | Worker goals resolve supplied predicates, and copying an answer preserves variable sharing. |
| WC-007 | A winning first_solution has removed its blocked loser from public actor enumeration before the caller proceeds, preserving unrelated mailbox contents and an application monitor. |
| WC-008 | Parallel error cleanup removes its blocked sibling before the caller proceeds, preserving unrelated mailbox contents and an application monitor. |

Each case uses the public WebSocket session API and public language predicates.
Except WC-006, which inherently requires source, cases exercise the same goals
both without source and with a harmless submitted private predicate. Worker
queries are not wrapped in `once/1`, which could hide nondeterminism. A successful
single-result test under `limit(1)` must report `more:false`; a terminal failure
must be delivered as failure rather than hidden by an answer wait.

The tests make no assumption about pid display formatting: they match pid terms
inside submitted Prolog and inspect ordinary returned bindings. Notifications
about child termination may precede the answer and are allowed by the runner.
Coordination actors are ordinary linked actors; no owner-only detached-creation
privilege is requested.

## Ordering and cleanup observations

The continue-policy cases use monitor/message barriers, not timing sleeps, to
force the rejected worker to terminate before releasing a winner. The blocked
loser cases arrange readiness before the other worker succeeds or throws. The
loser's public liveness and the unrelated witness are checked immediately after
the combinator returns, before waiting for the gate's termination notification.

These cases cover completed local calls. Partial startup failures, interrupted
callers, hard abort, remote cancellation and general namespace teardown are not
claimed by this batch. Implementation-specific fault-injection tests remain in
the runtime repositories.

## Separate diagnostics

`worker-diagnostics-0.1.json` is explicitly exploratory. WCD-001 repeats short
continue-policy calls with and without supplied source to investigate the SWI
worker-cleanup ownership error observed earlier. It uses the same assertions on
both candidates, but its pass/fail report is **not** part of ACTOR Workers 0.1.
A pass means the race did not occur in those attempts, not that it is fixed.

Other differences, including runtime-bound nested supervisor admission,
blacklist enforcement and resource-policy defaults, remain outside this worker
contract. Do not relax a core assertion to accommodate a candidate failure: a
failure of a listed worker requirement remains a conformance failure and should
be reported with its evidence.

## Invocation

```sh
python3 runner/run.py --manifest cases/actor-workers-0.1.json \
  --ws-url ws://127.0.0.1:3060/ws --advertised-profile actor \
  --candidate candidate-name --report reports/worker-result.json
```

Run the diagnostic separately by selecting
`--manifest cases/worker-diagnostics-0.1.json`. Authentication and timeout flags
are the same as for the other profiles. The runner does not start or stop nodes.
