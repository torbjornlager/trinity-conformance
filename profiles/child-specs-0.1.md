# Supervisor child-specification validation 0.1 — separate draft pack

This separately versioned draft selects runtime child-specification validation
from the shared language manual. It does not amend baseline 0.1 or advertise a
new node profile. Required means required within this pack. Both native ACTOR
candidates run identical [public-interface assertions](../cases/child-specs-0.1.json).

| Case | Selected observation |
| --- | --- |
| SV-001 | A missing start raises missing_start_option(Id), leaving the supervisor output unbound. |
| SV-002 | Duplicate initial ids raise permission_error(duplicate,supervisor_child_id,Id). |
| SV-003 | Improper outer child lists and improper child-option lists raise list type errors. |
| SV-004 | Later invalid restart and shutdown settings are rejected despite earlier valid values. |
| SV-005 | An invalid nested child is rejected before a preceding valid initial child starts; the public actor snapshot is unchanged. |
| SV-006 | Invalid dynamic addition preserves an exact sibling snapshot and its ability to reply; valid retry appends a live child under the rejected id. |

Invalid specifications arrive as ordinary self-messages before constructors are
called; SV-006 uses literal valid specifications for its positive controls.
The intended selection is execution-time validation. Actual admission barriers
remain required failures in the matrix; they are not converted to passes or
unsupported outcomes. Existing supervisor/admission diagnostics remain separate
and are not cleared by this pack. All expected exceptions must be nonvar before
matching formal error terms. Context text is not compared.

For restart(bad), the selected semantic rejection explicitly permits either
SWI's type_error(oneof([permanent,transient,temporary]),bad) or Trealla's
domain_error(supervisor_child_restart,bad). This finite documented error-name
allowance is part of the shared test, not a candidate-specific goal or permission
to accept arbitrary errors. Other selected formal errors are matched directly.

No fixed sleeps, private registries, runtime imports or native threads are used.
Every expected receive has an explicit failure/exception callback. SV-005 compares
public actors/1 snapshots around validation and polls for an unwanted startup
message; this bounded observation cannot exclude an arbitrarily short-lived
provisional actor. SV-006 waits for startup acknowledgements, tests sibling
liveness before/after rejection and consumes explicit child monitors plus the
supervisor's spawn-time monitor after halt. Shutdown reasons/timing are not
asserted. The runner requires final success with More=false without an outer
once/1. Successful fixtures halt; disposable session/node teardown bounds failures.

This is not exhaustive validation: cyclic terms, every child option, server
callbacks, general directives, source inheritance and policy, static admission,
remote supervision, concurrent additions, restart behavior and shutdown timing
are outside scope. Public results do not prove private resource reclamation.
Runtime changes require separate authorization; installed engines and n3/n5 are
not modified.

The 24 October final run records 6/12 passes: SWI 1/6 and Trealla 5/6.
See the report for admission barriers, the initial run and bounded diagnostics.
