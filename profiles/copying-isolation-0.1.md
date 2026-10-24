# Actor copying and private-source isolation 0.1 — separate draft pack

This separately versioned draft selects observable local actor copying and
private-source behavior from the shared language manual. It does not amend
baseline 0.1 or advertise a new node profile. Required means required within this
pack. Both native ACTOR candidates execute identical
[public-interface goals and source](../cases/copying-isolation-0.1.json).

| Case | Selected observation |
| --- | --- |
| CI-001 | The spawn output variable inside the goal denotes the child's exact self pid. |
| CI-002 | A child binding leaves the parent variable unbound; later parent binding leaves the child value unchanged. |
| CI-003 | Repeated goal variables retain sharing, distinct variables remain distinct, and a delivered message has independent variables with the same sharing structure. |
| CI-004 | src_text supplies a two-clause child predicate, enumerated in source order. |
| CI-005 | src_list preserves two-clause order, repeated variable sharing within a clause and distinct variables across the returned terms; original source variables remain unbound. |
| CI-006 | Two siblings define the same predicate differently. Mutation of one private database leaves the sibling and the parent's supplied predicate unchanged. |

CI-003 binds a variable in the delivered message, then asks the child to confirm
that its corresponding variables remain unbound. CI-006 releases a sibling read
only after the other actor reports its completed mutation. These are explicit
message barriers, not guessed sleeps. Every expected receive has a failure/
exception timeout callback, and exact pid/reference/normal-reason notifications
are consumed. Successful fixtures terminate normally; disposable session/node
teardown bounds failures.

Goals use public predicates only: no runtime imports, private module names,
registry inspection or native threads. CI-006 uses minimal dynamic/1 declarations
solely to support the selected retractall/assertz mutation; directive behavior in
general is not under test. The runner requires one final success with More=false
without an outer once/1 hiding residual alternatives.

URI loading, source directive policy beyond this dynamic declaration, implicit
source inheritance, src_predicates, general module qualification, remote spawning,
browser runtimes, GNU ACTOR, interruption, quotas and exhaustive sandbox policies
are outside this finite selection. Ordinary variable identity and clause order
are checked inside Prolog, not inferred from serialized variable names or pid
formatting. Passing this pack does not prove resource reclamation or a complete
security boundary. Failures remain visible; runtime repairs require a separate
batch.
