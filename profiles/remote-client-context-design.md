# Remote client context follow-up design

Status: investigation and proposed implementation order, 19 November 2026.
This document changes no runtime contract or conformance expectation.

The common ACTOR rule is client-scoped ordinary names, with a separate registry
for explicitly published services. Equal credentials, a known actor PID or a
forwarded promise reference do not themselves establish a shared client scope.

## Current evidence

The fresh disposable native context run is linked from the
[HTTP context follow-up](../reports/2026-11-19-http-context/REPORT.md).
SWI-origin return probes successfully deliver their answers: ordinary names are
`undefined`, and promise collection reports `existence_error`. This directly
shows that those returning descendants do not rejoin the origin namespace.

Trealla-origin remote sibling checks expose a different defect: another client
can collect the remote owner's promise; the owner's later collection then
fails. Trealla currently sends no per-client delegated lineage on its outgoing
transport. Its README explicitly limits delegated lineage to receiver support.
This must be fixed before claiming remote client isolation.

Trealla-origin return probes time out before an answer, and remain blocked.
Those timeouts do not prove a particular source-export failure or establish the
returning actor's scope. The old adapter uses a broad blocker classification;
its raw observations must be read with this limitation.

SWI's receiver uses `ws_lineage(Connection, Token)`; the connection is part of
identity. Receiving an equal token on a different connection does not authorize
restoration of an earlier browser, HTTP-session or delegated namespace.

## Proposed separate changes

1. Give Trealla outgoing commands a per-client delegated lineage. Keep transport
   credentials, account quotas and ordinary-name scope separate. Record the
   remote route before awaiting spawn acknowledgement. Test two local clients
   using the same physical peer connection and credential on both destinations:
   SWI and Trealla. Foreign yield/cleanup must preserve the owner's reference.
   Include toplevel spawn, named children, disconnect and late-reply controls.
2. Replace ambiguous return probes with explicit public-language phase messages:
   bridge started, return spawn acknowledged, return actor entered, lookup or
   collection result. Each phase must have a bounded deadline and a unique
   correlation reference. Copy complete helper source and preserve terminal
   errors; absence of a reply must not be labeled as a proven exporter defect.
3. Retain the documented connection-scoped return boundary unless an explicit
   context-resumption feature is chosen. Test that a fresh returning context
   cannot collect or dispose of the origin's promise and leaves its names
   hidden, while an explicit message back to an existing origin actor works.
   Preserve the older CTX-016/017 failures in their versioned report. Do not
   silently reinterpret them as passes for a different requirement.
4. If transparent rejoining is wanted, design and review it as an explicit
   origin-issued capability. Bind it to the origin context and trusted peer,
   reject it after context closure, and distinguish it from account identity
   and the existing connection-scoped lineage token. Test forged, expired,
   replayed and cross-client use before enabling it. Matching token text alone
   must never select the origin's namespace.

The recommendation is to finish per-client outbound delegation first and keep
implicit round-trip restoration out of that patch. Applications can send to an
existing origin actor explicitly; that actor can use its own names and promises.
The earlier connection-cleanup repair supplies real termination observations
for current receiver lifetimes. Restoring removed attachment instrumentation
would not implement a resumption contract.

## Completion criteria

The four directed native routes need observed phase controls and isolated owner
collection, with equal-credential foreign controls. Test socket closure using
independent monitor references and a still-live unrelated context. Preserve
source/executable hashes, failed attempts and exact case inventory. No live
engine, deployment pin, quota or peer trust setting should change merely to
make these tests pass.
