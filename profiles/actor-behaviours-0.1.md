# ACTOR Behaviours 0.1

Status: **draft executable profile**  
Required advertised node profile: `actor`  
Wire protocol version: `1`

This opt-in profile defines observable semantics for the generic-server and
supervisor behaviours shared by the SWI-Prolog and Trealla Prolog nodes. It is
separate from ACTOR Core so behaviour evolution does not retroactively change
the meaning of ACTOR Core 0.1.

## Generic servers

1. `server_spawn/3-4` must start a server using the supplied callback and
   initial state.
2. `server_request/3-4` must return the callback reply and thread the returned
   state into the next request.
3. `server_promise/3-4` and `server_yield/2-4` must correlate asynchronous
   replies without losing the server's state transitions.
4. `server_upgrade/2-3` must replace the callback while preserving server
   state. Source supplied with the upgrade must be available to the server.
5. `server_halt/1-2` must terminate the server and report its normal reply.

## Supervisors

1. A supervisor must start each valid child specification and report distinct
   live child PIDs through `supervisor_which_children/2`.
2. `supervisor_count_children/2` must report specification, active, worker,
   and supervisor counts consistently with child enumeration.
3. Dynamic child start, terminate, restart, and delete operations must update
   enumeration and return the documented result terms.
4. `one_for_one` must replace only a failed child. `one_for_all` must replace
   all children. Nested supervision must restart the failed subtree without
   replacing an unaffected outer sibling.
5. A `temporary` child must not restart. A `transient` child that exits
   normally must remain present as an inactive specification.
6. A `server(...)` child must retain generic-server request semantics and
   terminate normally when its supervisor performs a timed shutdown.

## Executable cases

The normative metadata is in
[`cases/actor-behaviours-0.1.json`](../cases/actor-behaviours-0.1.json).
The cases use only the public WebSocket session protocol and submitted Prolog
source; they do not import either implementation.

Timing is used only to wait for deliberately delayed child termination. A
candidate may complete earlier, but must satisfy the same observable state by
the end of the stated test interval.
