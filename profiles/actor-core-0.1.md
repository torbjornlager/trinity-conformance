# ACTOR Core 0.1

Status: **draft executable profile**  
Required advertised node profile: `actor`  
Wire protocol version: `1`

This document freezes the first implementation-neutral behavioural contract
for an ACTOR node. It specifies observable results, not implementation
mechanisms. Passing this profile does not imply conformance to unrestricted
`workbench` behaviour or to every predicate provided by SWI-Prolog.

## Conformance language

The words **must**, **must not**, **should**, and **may** are normative. A
candidate conforms only when every required case passes in the same supported
configuration. Skipped and untested behaviour does not count as passing.

## Transport

1. The node must accept a WebSocket connection at its documented endpoint.
2. `transport_hello` with protocol version 1 must produce one
   `transport_welcome` event advertising version 1. A node may include its
   profile in this event; the candidate configuration remains authoritative
   when version 1 omits it.
3. Browser PID and acknowledged terminal-I/O negotiation must be reported
   explicitly.
4. A session created by `toplevel_spawn` must be owned by the connection that
   created it and must be reclaimable when that connection closes.

## Public identifiers

Actor PIDs and opaque references exposed by this profile are ten-digit
integers. A locally displayed PID may additionally carry a node suffix using
`Pid@Node`. Repeated enumeration of a deterministic operation must not expose
an artificial final failure answer.

## Toplevel sessions

1. A session must accept `toplevel_call`, `toplevel_next`, `toplevel_stop`,
   `toplevel_abort`, `toplevel_halt`, and `toplevel_respond` as applicable.
2. A successful page is reported as `success(Pid, Rows, More)` on the Prolog
   surface and as a `success` event on the wire.
3. `More=true` means another page may be requested. The final page must report
   `More=false` without evaluating an additional solution for presentation
   purposes.
4. Bindings in answer templates must preserve the names and sharing of the
   submitted query variables.
5. A session created with `session(true)` must return to its idle state after
   a completed, failed, stopped, or recoverably erroneous call.

## Actors and selective receive

1. `self/1` must deterministically return the current public actor PID.
2. Sending to self and then receiving the message must work within one
   toplevel call.
3. Receive clauses are tested from left to right against messages in arrival
   order. Messages that do not currently match must remain available to a
   later receive.
4. A guarded clause `Pattern if Guard -> Body` matches only when the pattern
   matches and the guard succeeds. Guard failure must not consume the message.
5. Built-ins used by a receive guard must have the same observable meaning as
   when used in an ordinary submitted goal.

## Terminal output

1. Non-stream `writeln/1`, `format/1`, and `format/2` output from public actor
   code must be delivered to the inherited terminal endpoint.
2. When acknowledged browser I/O is negotiated, an output event must remain
   pending until the client sends `browser_io_reply`.
3. One Prolog line-ending request must produce one terminal line ending.

## Input and response

1. Direct browser-session input must produce a `prompt` event and suspend the
   goal until `toplevel_respond` supplies an answer.
2. Input executed in a nested toplevel belongs to that toplevel's protocol
   caller. The caller must receive `prompt(Pid, Prompt)` as an actor message
   and may complete the operation with `respond(Pid, Answer)`.
3. A nested prompt must not be silently diverted to the caller's inherited
   browser terminal.

## Initial executable cases

The normative case metadata is in
[`cases/actor-core-0.1.json`](../cases/actor-core-0.1.json). Version 0.1 covers
transport negotiation, public identity, paging, selective receive, guarded
receive, direct browser input, and nested toplevel input. Monitoring,
distribution, source transfer, connection cleanup, and resource governance
remain part of the ACTOR roadmap but are not certified by this first tranche.

## Compatibility rule

SWI-Prolog is the first reference implementation, but incidental SWI
behaviour is not automatically normative. A disputed result must be resolved
by clarifying this document and versioning the profile when the observable
contract changes.
