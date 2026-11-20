# Canonical node identity and context qualification — 20 November 2026

Native SWI `254ae3a` and Trealla `d451596` pass **44/44** URI, source and client-context assertions on macOS and Linux. The previous committed sources record **32 pass / 12 fail** against the same version 0.2 case goals. This is a local qualification, **not a deployment or a new full live sweep**. The existing 207 unresolved failed observations remain open pending live verification or individually reviewed contract classification.

| Check | macOS | Linux |
|---|---:|---:|
| Version 0.2 URI/context assertions | 44/44 | 44/44 |
| Complete SWI tiers | 8/8 plus Origin/visitor checks | 8/8 plus Origin/visitor checks |
| Complete Trealla unit groups | 112/112 | 112/112 |
| Trealla interoperability groups | 71/71 | 71/71 |
| Conformance runner tests | 123/123, Node 22 | — |

The engines are SWI-Prolog 11.0.0 and Trealla 3.14.20. Every Trealla check retains its 30-second watchdog. [Raw qualification checks](qualification-checks.json) and platform logs preserve the completed phases and setup failures separately.

## Agreed behavior

The author explicitly selected canonical identity and peer configuration together. Only an empty root path is normalized: `https://node/` and `https://node` share the node key used by addresses, routing, credentials and owner dial mappings. Schemes, authorities, explicit ports, non-root paths (including their trailing slash), queries and fragments stay distinct. Duplicate canonical credential keys and conflicting endpoint mappings are rejected. Credential values are absent from validation errors.

An implicit local spawn retains the client's context. An explicit node URL creates work in a receiving transport context, even when it points back to the originating server. Returning to that URL does not restore the earlier client namespace. Ordinary names remain client-context scoped; published services provide node-wide discovery. These address and context rules are separate assertions in version 0.2. Browser, ECLiPSe/N7 and GNU/N6 adoption are not established by this native qualification.

## Repairs and tests

Both native implementations normalize root aliases before constructing returned actor/toplevel addresses, selecting credentials, applying owner topology and routing later controls. Tests cover character and code lists, IPv6 roots, distinct authorities/schemes/ports/paths, duplicate keys and conflicting mappings. Trealla's qualified-local sends and exit ownership checks now resolve the canonical address without granting authority to another client. Toplevel halt waits match the private monitor reference, allowing equivalent URI representations without losing the ownership or monitor check.

Trealla previously pooled outgoing connections across hosted clients. Root alias coalescing must not expose one client's ordinary names to another through a legacy peer with one namespace per connection. Its cache now keys by client context and canonical node, retaining the global pool for unscoped standalone use. Context retirement removes its routes and closes its connections outside the registry lock and manager loop. Closed contexts cannot reconnect. Internal manager commands carry a process-private key; raw public messages and variable-key forgeries cannot retire another context. A terminal reader-loss path also closes the owned socket.

The two real-peer lifecycle controls use an independent connection to observe actual remote actor termination. They check alias reuse within one context, separate sockets between clients, reclamation after retirement, surviving delivery for the other client, rejection of reconnect after closure, repeated retirement and forged control messages. They do not infer peer reclamation from a local connection-loss event.

## Contract and fixture history

Version 0.1 remains unchanged. An explicit replay on the final candidate records **20 pass / 6 fail**: exactly NU-001/002/004 in each engine. The six mixed visibility assertions are retained as failures, rather than claimed as repaired runtime behavior. NU-001/002/004 in version 0.2 remove only the mixed-in caller-namespace visibility assertion; address, source, monitor and baseline checks remain. NU-014–017 assert local visibility, explicit-URL isolation, retained-toplevel behavior and ordinary-name separation independently. NU-018/019 cover URI-text halt and foreign exit denial. NU-020 verifies alias lookup by delivery through the returned handle. NU-021/022 run fresh anonymous and equal-credential clients against the same canonical peer node, checking independent names, delivery, foreign control denial and baseline restoration.

The maintained adapter installs real owner credentials in each disposable runtime and normally configures each canonical node once. The old-source control uses its compatibility option to authorize both literal spellings, avoiding the already documented credential precondition. Thus it compares the same case goals, with the credential fixture appropriate to each implementation. It is not an identical deployment configuration. NU-011 already passes on this baseline because it includes the earlier Trealla reflection repair.

Initial diagnostic failures are retained separately. An exported remote handle can be a connection-scoped alias; strict equality with the peer's internal PID is not a portable delivery assertion. The corrected checks prove delivery with distinct markers. A lifecycle draft incorrectly installed a monitor in one retained-toplevel query and awaited it in a later query: Trealla's fresh query workers have separate mailboxes. The final check monitors and receives in one live query. Neither diagnostic error is counted as a runtime regression. The first complete Trealla unit run also reached an old fixture that passed `unused` as the socket to connection-loss cleanup. That fixture now supplies a stream, as the explicit-close control already did; production close behavior was not weakened.

The Linux lab completed all 112 unit groups, then its combined command stopped at the interoperability prerequisite guard because `nc` was absent. Installing `netcat-openbsd` in that disposable lab allowed the unchanged interoperability phase to run separately. No test watchdog or assertion was relaxed.

## Release boundary

The production selection guard passes unchanged. No dependency pin, live image, engine, admission limit or access mode changed. Candidate results do not retire the live NU observations. The next release step is to build exact images, run the ACTOR and demonstrator integration/OPEN-exercise gates against those images, update pins, deploy and replay the applicable live URI/context cases. A subsequent full sweep should be recorded separately.

[Outcome summary](SUMMARY.json) · [source revisions](source-commits.json) · [artifact hashes](files-sha256.json).
