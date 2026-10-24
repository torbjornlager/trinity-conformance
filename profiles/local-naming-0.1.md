# Local naming and registration 0.1 — separate draft conformance pack

This separately versioned draft selects the shared language manual's ordinary
registration and local named-creation contracts. It is not an amendment to
baseline 0.1 or a new advertised node profile. Required means required within
this pack. Both native ACTOR candidates execute the identical
[public-interface goals](../cases/local-naming-0.1.json).

| Case | Selected observation |
| --- | --- |
| LN-001 | Register a live actor, look up its exact pid, and route a request through the ordinary name. |
| LN-002 | Occupied names and a second name for an already named pid raise the documented native errors, preserving the original registration. |
| LN-003 | Unregister twice; lookup becomes undefined and the actor still acknowledges a direct request. |
| LN-004 | After exact normal termination, the name disappears and can name a different live actor. |
| LN-005 | An observed dead local pid is rejected with existence_error(process,Pid), leaving the name available for a live actor. |
| LN-006 | Occupied named supervisor creation is rejected; failed source setup releases its reservation; retry publishes a usable empty supervisor. |

Names are distinct fixed atoms per case on disposable nodes serving only this
run; no cross-client name generation assumption is made. Actors acknowledge ping requests and
wait for explicit stop messages; exact pid/reference/reason notifications precede
cleanup and reuse assertions. Lookup results are received into fresh variables
and checked by identity, avoiding an accidental success through output matching.
Every expected receive has an explicit failure/exception timeout callback. No
fixed sleeps, runtime imports, native threads or private registries are used.
The runner requires one final success with More=false and does not insert once/1.

LN-006 deliberately supplies a nonexistent file URI as a source-setup failure.
The platform-dependent error context is not compared. A subsequent successful
creation under the same name checks release through public interfaces. Its
zero-time check for an unwanted child startup message is a bounded observation,
not proof against arbitrary delayed activation races.

Ordinary namespace differences remain explicit: native SWI names belong to the
caller's client namespace; native Trealla names are node-wide. These tests stay
inside one client and do not assert cross-client isolation or merge namespaces.
Service registrations, remote aliases, concurrent name races, publication during
startup, interruption, namespace teardown, browsers and GNU ACTOR are outside
this pack. Public lifecycle observations do not certify resource reclamation.
Successful fixtures are stopped and monitored notifications consumed; disposable
session/node teardown bounds failures. Required failures remain visible and any
runtime repair requires separate authorization.
