# GNU request-framing follow-up

The unchanged baseline 0.1 cases were run against all three native runtimes,
plus the existing native ACTOR and local SWI-WASM selections. See
[coverage](COVERAGE.md), [provenance](provenance.json), [repair source hashes](repair-inputs.json),
and the [previous HTTP client-context run](../2026-10-21-http-client-context/COVERAGE.md).

**94/94 required baseline selections pass**, up from 93/94. In particular,
GNU-to-Trealla HC-002 now completes with the expected promise answer instead
of the worker deadline error. All nine HTTP caller/destination pairs pass both
selected interoperability assertions. These are scoped requirements, not full
ISO conformance, security certification or general lifecycle guarantees.

## Repair

GNU previously emitted bare `goal=V0=ok` and `template=V0-V0` text. Trealla's
current combined parser cannot recover the intended pair from those fragments.
The shared GNU RPC/promise serializer now emits `(V0=ok)` and `(V0-V0)`.
Parentheses are added after serialization with the existing shared variable
names and quoted UTF-8 printer, before unchanged URL encoding. Source options,
request limits, paging, deadlines, transport policy and promise semantics are
unchanged. No Trealla parser or runtime file was changed.

## Focused regressions

The new GNU `rpc_framing_tests.py` suite passed six captured-wire assertions
and twelve live checks per native peer (SWI, Trealla and GNU): 42 assertions.
[Live evidence](gnu-framing-live.txt) records the peer order and results.
The suite uses portable operator goals and templates, quoted apostrophes,
backslashes/Unicode, repeated and distinct variables, caller independence,
paging and once. Replies are collected before asserting their contents, so a
protocol error is not hidden by GNU's pre-existing output-pattern wait behaviour.
Existing GNU source failure/order/slot-recovery (11 checks) and address,
no-I/O, path/source-resource (56 checks) regressions also pass. The broad pinned
RPC/comparison suites are not claimed as rerun; their existing zero-limit and
other audit qualifications remain in the GNU status documentation.

## Separately retained observations

The initial complete run recorded one supporting ACTOR failure: Trealla BH-007
returned `error(syntax_error(read_term),read_term/3)` during spawn. Thus the
initial supporting native ACTOR packs total 65/66, despite all 94 required
baseline selections passing. The original [failure report](trealla-actor-behaviours.json)
is retained unchanged. A [fresh-node repeat](trealla-actor-behaviours-repeat.json)
passed all ten behaviour cases; it does not erase the initial failure or establish
its cause. No ACTOR implementation, assertion or waiver was changed.

The bare/unparenthesized operator-fragment diagnostic remains a separate
Trealla parser issue. Experimental text, other semantic diagnostics and the
previous immediate-disposal mutex observation remain outside this repair.
The complete runner's nonzero exit reflects those retained observations; it
must not be reported as an entirely green broader run.
