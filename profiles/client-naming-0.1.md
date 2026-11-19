# Client-context naming 0.1

Ordinary actor names have one common ACTOR contract across implementations.
`register/2`, `whereis/2`, `unregister/1`, named sends, named monitors and
`name/1` startup reservations use the caller's client-context namespace.
The [manifest](../cases/client-naming-0.1.json) adds multi-client checks to the
existing single-client [local naming pack](local-naming-0.1.md).

A retained WebSocket connection defines a client context. Its toplevels and
local descendants share names. Independent connections remain separate even
when they use the same principal or anonymous visitor identity. In the browser
session API, a page/coordinator owns the context shared by its local actors;
independent page sessions are tested separately. Supported retained HTTP session
APIs must use their session context; this pack currently measures WebSocket and
browser-page boundaries, not HTTP session naming.

A name identifies at most one PID within its context. The same atom can name
different actors in independent contexts; one PID's ordinary-name uniqueness is
also checked within the caller's context. Registering, unregistering, reserving
or retiring a name in one context cannot remove or block an independent
context's binding/reservation. Local descendants inherit the context.
Unregistering a name does not terminate its actor. Actual PID retirement removes
its aliases wherever that exact PID is registered; a same-named binding to a
different PID survives. Client teardown withdraws only that context's ordinary
bindings and startup reservations and rejects late publication into it.

Explicitly published services use an independent node-wide service registry.
They support intentional discovery across client contexts. Ordinary name
registration does not publish a service or grant remote service-addressing
rights. Publication and removal retain the node's owner/administrative policy;
this contract does not grant public clients service-management authority.
Native regression checks cover the separate service registry; the common
black-box pack does not provision node-wide services on public endpoints.

| Case | Required observation |
|---|---|
| CN-001 | Another client cannot look up an ordinary registration. |
| CN-002 | Two clients can use the same name and each sees its own actor. |
| CN-003 | Foreign unregister preserves the owner's name. |
| CN-004 | Named messages reach the caller's context. |
| CN-005 | Named monitors resolve in the caller's context; retirement preserves another context's same-named actor. |
| CN-006 | Local descendants share the parent's namespace. |
| CN-007 | Multiple toplevels on one retained connection share names. |
| CN-008 | Disconnecting one client preserves another client's same-named binding. |

CN-007 requires a transport API that exposes multiple toplevels on one retained
connection. Native SWI/Trealla and ECLiPSe WebSocket adapters run it. The browser
session API does not expose that operation; its unsupported row remains explicit
and cannot be counted as a pass. Browser page-to-page checks are not a claim that
one browser coordinator hosts multiple network clients.

## Running the selection

Use Python 3.11+ for the shared WebSocket harness and Node 22 with Playwright and
Chromium for browser sessions. The native driver starts and stops owned loopback
nodes and needs the verified engines paired with their libraries.

```sh
python3 adapters/local_client_naming.py \
  --swipl /path/to/swipl --tpl /path/to/tpl \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --output /fresh/native-results

python3 adapters/client_naming.py \
  --ws-url wss://authorized-test-node/ws --candidate candidate-name \
  --session-interval 5 --output /fresh/client-naming.json

LIBRARY_RUNTIME_ROOT=/path/to/browser-package \
LIBRARY_REPORT=/fresh/browser-naming.json \
CHROME_PATH=/path/to/chromium \
node adapters/wasm_client_naming.cjs
```

The pack uses the same ordered goal/action steps on every boundary, with fresh
contexts and unique name atoms per case. Both clients use equal credentials.
There are no automatic retries or changes to public limits. Failures and
unsupported operations remain visible. Pending reservations, concurrent closure
and service discovery require the additional native implementation regressions.
The older retained-context results and their naming failures remain historical
evidence; this selection does not change promise ownership or remote round-trip
context semantics.
