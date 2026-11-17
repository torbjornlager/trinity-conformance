# Actual controls during receive guards — 5 November 2026

**All 32 observations pass:** eight cases each on native SWI, Trealla, real Chrome
Worker and real Chrome main. [Native results](native/results.json) and
[browser results](browser.json) each record 16 passes. The [manifest](manifest.json)
covers abort, configured execution limit, termination and ordinary RPC error,
each with no submitted source and with private source containing named guard/body
helpers. [104 runner checks](runner-tests.txt) pass.

Trealla repair `d92364c` and browser maintained-test commit `deb11db` are committed
and pushed. The browser runtime code and installed engines are unchanged by this
batch. The book already states these rules. Public consumer pins and services
are unchanged. [Verification](verification.json) records exact inputs and source
commits; committed runtime files match the executed source hashes.

## Barriers and assertions

Each probe first queues an earlier message, a target containing two references
to one variable, and a later message. The guard tentatively binds the target
variable and a separate guard variable, then calls a read-only local RPC peer.
The peer records entry and withholds its response. Controls are requested only
after exactly one request has arrived. The guard cannot complete normally while
the peer is held; its selected body throws if unexpectedly reached.

- **Abort:** interrupt the primary session through its actual control API.
  Require the abort acknowledgement, then call receive on that same surviving
  session. Check earlier/target/later order, the target's original unbound shared
  variable, no duplicate messages and a healthy subsequent call.
- **Execution limit:** start a retained child toplevel with a 0.6-second running
  limit. Its parent matches `error(Target,error(resource_error(time),_))` as a
  Prolog term, then submits the mailbox recovery goal to that same target and
  requires its success. Display diagnostics are not used to classify the error.
- **Termination:** request `exit(Target,guard_terminated)` for a monitored child
  and require its matching down notification while the peer is still held.
  The parent remains healthy. The destroyed target's mailbox is not inspected.
- **Ordinary exception:** release the peer with `error(guard_ordinary)`. Require
  a non-match, rolled-back pattern/guard bindings and the full original mailbox.
  This contrast control exercises the exception class receive must discard.

Private-source variants also call named predicates in their guard and recovery
body. Patterns and message payloads remain data throughout preparation.

Browser execution boundaries:
**main-session abort runs on the main engine itself**, and Worker-session abort
runs on its primary Worker. Configured public PTCP time limits and actor
termination use Worker children under either coordinator. The report does not
infer a main-engine time-limit or hard-termination API from those child tests.
Native child cases use each native runtime's normal actors/toplevels.

The entry deadline is five seconds. Host response deadlines are five seconds;
child protocol receives use three seconds. Guard waits/RPC client limits are
longer (12/15 seconds), so normal timeout completion cannot satisfy the control
checks. Peer response release follows control and recovery, except in the
ordinary-error case. Owned sessions, nodes, browsers and held handlers are closed.
The browser has an external 120-second watchdog. No public policy is widened.

## Trealla repair

An unwrapped RPC in a submitted receive guard was resolved as an undefined
procedure. Receive correctly treated that ordinary error as a non-match, hiding
the callback dispatch gap and preventing the entry barrier from being reached.

The final repair is confined to `isolation.pl`: submitted source-less receive
callbacks now pass through the same public API dispatcher as the surrounding
goal; the minimal actor bootstrap prepares application goals too. Private guard
leaves use the existing actor-query dispatcher. Message patterns are not
rewritten. The core `actors.pl` receive selector is byte-identical to its parent
commit. Compiled native callbacks keep their original context and cut scope.

`receive_caller_tests.pl` maintains executable checks for submitted guard, body
and timeout API calls and a message pattern whose functor resembles an API call.
The shared controlled fixture supplies the real RPC/control and private-source
coverage. The browser package now maintains the eight-case control selection in
its normal real-browser test plan.

## Regression results

The original 29-case receive selection passes all **58 native observations**
again in [the regression report](selective-receive-regression/results.json).
Every Trealla unit group passes in the [combined unit/initial interop run](trealla-unit-and-initial-interop.txt).
That command then failed its interop stage with connection refusal at a one-shot
listener's default 0.2-second startup wait. The unchanged-code
[interop rerun](trealla-interop.txt), using fresh fixture ports and the runner's
one-second startup margin, passes every interop group. No runtime assertion or
protocol deadline was relaxed. The per-process test watchdog was 120 seconds.

All seven [packaged browser groups](browser-regressions/results.json) pass:
mailbox, standalone, semantic contracts, standard library, session API, the
29-case receive selection and the new eight-case control matrix. This batch
changes browser tests only. Existing engine/schema pins remain unchanged.

## Coverage and preserved unsuccessful work

B-104 is verified within the primary-session/child-lifecycle boundaries above.
ACTOR targets now have **34 verified Appendix B source units** each; GNU ISOBASE
remains at 23, with ACTOR outside its profile. The 43 mapped library obligations
remain covered. These are source-unit/selected-obligation counts, not a full
language conformance percentage. The [previous ledger](previous-ledger.json) is
retained.

`development/` preserves failed entry probes, diagnostic wrappers and rejected
repairs. Initially all Trealla probes lacked entry because callback lookup failed;
adding fixture source-origin allowances did not fix it and was removed. A broader
attempt to change core receive module qualification broke cyclic-answer and
first-solution regressions. Those attempts were rejected; the final change leaves
the selector untouched. An extra host-compiled private-module experiment also
failed against unchanged original sources; it is retained separately, not used
as an accepted Web/API conformance probe. Earlier browser ordinary-error fixture
framing was corrected to compute Content-Length from the actual released body.
Intermediate results are not added to the final 32 observations.

## Reproduction

```sh
python3 adapters/local_receive_controls.py \
  --swipl /path/to/swipl --tpl /path/to/tpl \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --output /fresh/native-output

LIBRARY_RUNTIME_ROOT=/absolute/path/to/swi-wasm-node \
LIBRARY_REPORT=/fresh/browser.json NODE_PATH=/path/to/playwright/node_modules \
node adapters/wasm_receive_controls.cjs

python3 runner/receive_controls.py --manifest cases/receive-control-0.1.json \
  --native /fresh/native-output/results.json --browser /fresh/browser.json
```
