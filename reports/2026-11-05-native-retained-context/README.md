# Native retained-context audit — 5 November 2026

**Audit complete; repairs remain.** The audit found three context defects and
two adjacent API/transport defects in the currently pinned native sources.
Runtime code, installed engines, consumer pins and public services were not
changed. The deferred prologue/library semantic choices were not revisited.

The four scoped runs cover **51 distinct candidate/case pairs**: **31 pass,
nine fail and 11 remain blocked**. Duplicate controls agree across runs. The
30-probe core was repeated unchanged on fresh fixtures, with **23 passes and
seven failures each time**, and no fixture errors. These are selected contract
probes, not a full conformance certificate.

## Confirmed context defects

| Defect | Observed result | Evidence |
|---|---|---|
| SWI uses an authentication principal as the context of fresh HTTP requests. | One request creates a promise; a new request with the same bearer credential collects `success([mark],false)` without a retained session or context handle. Anonymous requests remain separated. | `swi / CTX-010`, positive separation control `CTX-011`. |
| SWI does not rejoin the original context on a remote round trip. | A retained client at A registers an ordinary name and creates a promise. Descendants routed A → B → A see `undefined` for the name and `existence_error(promise,Ref)` for the promise. A name lookup also fails to rejoin A through a Trealla B. | `swi / CTX-016-swi-b`, `CTX-017-swi-b`, `CTX-016-trealla-b`. |
| Trealla ordinary names do not isolate clients. | A second WSS connection with equal credentials sees the first client's pid, cannot independently use the same name, and can unregister the first client's association. | `trealla / CTX-006`, `CTX-007`, `CTX-008`. |

These contradict the committed Appendix B client-context, ordinary-name and
promise ownership rules (B-004, B-058, B-062, B-064, B-296 as applicable).

## Adjacent defects and blocked coverage

- Native SWI does not expose `promise_cleanup/1` through the public actor API:
  the call raises `existence_error(procedure,promise_cleanup/1)`. The underlying
  RPC module implements it. The foreign cleanup probe consequently cannot
  exercise the public disposal boundary, although the owner still collects its
  promise. This contradicts B-305/B-306 (`swi / CTX-003`).
- A Trealla-origin inline `catch/3` sent to SWI contains private
  `sandbox_policy:sandbox_control_catch(...)` code. The receiver rejects it;
  the simple remote-message control succeeds (`trealla / CTX-018-swi-b` versus
  `CTX-012-swi-b`). This is a portable-goal export defect, not an ownership result.
- All ten Trealla-origin remote promise/round-trip probes, and the SWI → Trealla
  → SWI promise probe, are blocked before a context result is observable.
  Source helpers containing guarded `yield`, `catch` or nested `spawn` can
  encounter private-helper rejection or a missing callback reply. The report
  records those outcomes as **blocked**, rather than declaring their ownership
  checks passed or failed. Trealla remote promise isolation remains unverified.

## What is working

Both native runtimes preserve promise sharing with local children, isolate
separate retained WSS clients with equal credentials, and preserve promises
across toplevel replacement on one WSS connection. Native SWI also preserves
references across requests to an explicit retained HTTP session and isolates
another such session with equal credentials (`CTX-020`).

SWI-origin remote siblings share promises at both SWI and Trealla destinations.
Different originating clients remain isolated there, and an unsuccessful
foreign collection attempt leaves the owner's answer available (`CTX-013`–015).
The defect appears when descendants return to the originating node.

The existing SWI `promise_ownership` and `namespace_teardown` groups pass all
**35 named tests (47 parameterized executions)**. They cover namespace closure, resource disposal, admission and
surviving actors. However, one existing test explicitly requires authenticated
HTTP requests to share by principal; that expectation conflicts with the current
Appendix B contract. Passing that suite is not evidence that the account/context
boundary is correct.

## Source trace

- SWI `node_glue.pl:283` gives namespaces priority for promises but falls back
  to `http_client(Scope,Id)` for HTTP execution, where `Id` is the principal.
  `node_lifetime.pl:73` explicitly preserves an authenticated account across
  carriers. Resource accounts need that sharing; client contexts do not.
- SWI `node_lifetime.pl:246` propagates lineage and account fields, but
  `with_wire_context/4` constructs `ws_lineage(Queue,Token)` on the receiving
  connection. Returning to the origin consequently selects another ordinary
  registry and promise owner instead of the original `ws_client(...)` context.
- Trealla `actors.pl:762`, `:844`, `:854` keep ordinary-name uniqueness,
  unregistration and lookup node-wide. Namespace bookkeeping currently controls
  retirement rather than all name access. `namespace_tests.pl` even asserts
  node-wide visibility and uniqueness; those expectations need correcting.
- Trealla `receiver_lineage.pl` explicitly implements receiver-side,
  connection-scoped delegation only. Its outbound distribution manager pools
  nodes by URL, and outgoing messages lack an independent retained-context field.
  That needs a full propagation audit after the source-export blockers are fixed;
  source inspection alone is not a measured remote promise-isolation failure.
- SWI `actor_api.pl` exports promise/yield but omits `promise_cleanup/1`.
  Trealla `isolation:restore_actor_goal/2` restores library and format wrappers
  but does not generally restore the private catch/yield/spawn wrappers seen
  by the blocked transport probes.

## Recommended repair order

1. Separate the client-context key from authentication/resource accounts and
   transport carriers. Fresh HTTP requests get separate contexts; explicit
   retained sessions keep their context. Keep per-principal quotas intact.
2. Scope every Trealla ordinary-name operation, including uniqueness,
   lookup, unregistration, reservations and publication, to that context.
3. Propagate a server-issued, authenticated delegation of the context across
   native transports. Returning descendants must resolve the original context;
   a transport connection is an attachment to it. Preserve closure/revocation
   and prevent clients or unrelated peers from choosing another context.
4. Expose native SWI cleanup and restore portable Trealla goal/source terms,
   then rerun the blocked matrix before declaring remote ownership repaired.

Do not solve this by accepting caller-selected context ids or by making all
connections with the same credentials share a namespace. The first failing
regressions should replace the existing principal-wide HTTP and node-wide name
expectations before implementation changes.

## Reproduction and limits

Run `adapters/local_retained_context.py` with explicit `--swipl`, `--tpl`,
`--swi-root`, `--trealla-root` and a fresh `--output` directory. The default
selects the 30-probe core. Additional route selections are:

```text
--routes trealla-a:trealla-b
--routes swi-a:trealla-b trealla-a:swi-b
```

The fixture uses canonical node URLs, avoiding URI-alias questions. It runs
three SWI HTTP listeners in one isolated process and two
separate Trealla processes, on dynamically allocated localhost ports. The
actual engines are SWI 10.1.19 and released Trealla 3.14.20. Runtime source,
engine and adapter fingerprints are retained. Credentials are synthetic,
fixture-local and removed at teardown. All fixture processes are stopped.
This does not cover separate-machine/network failures, all admission modes,
all expiry/disconnect races, or GNU's contained HTTP worker/broker boundary.
GNU does not advertise retained ACTOR sessions, and has not been recertified here.

The contract pin is the preceding committed manuscript in
[pinned-manuscript.tex](pinned-manuscript.tex). The uncommitted library-documentation
expansion is separate and is not promoted by this audit. Native failure cells
are updated in the source-unit ledger; passing controls do not verify whole
paragraphs whose other obligations remain untested.

[results.json](results.json) contains the deduplicated observations;
[core.json](core.json), [repeat.json](repeat.json), [mixed-routes.json](mixed-routes.json)
and [trealla-route.json](trealla-route.json) retain each complete run.
[environment.json](environment.json) identifies the inputs, and
[existing-swi-controls.txt](existing-swi-controls.txt) retains the existing suite.
