# Initial supervisor child-specification run

This run is preserved with executed-manifest.json, raw reports/logs and exact
provenance. SWI passed 0/6; Trealla passed 5/6. Required failures remain in these
raw reports and are not replaced by the subsequent run.

SWI rejected all submitted queries with an outer instantiation error. Trealla
passed SV-001–005 but SV-006 threw missing_child_spec_observation. A separate
stage-labelled diagnostic located that wait at the second self-message receive,
before supervisor creation or a dynamic request.

The final SV-006 stages only the invalid child specification, with literal valid
initial/retry controls. It preserves rejection, exact sibling snapshots, liveness,
valid retry and cleanup assertions and all timeouts. Trealla still fails at the
invalid-data receive; SWI passes that revised dynamic case. SV-001–005 are unchanged.
See ../2026-10-24-child-specs/REPORT.md for final matrix and source-based analysis.
All preservation checks passed and both initial disposable nodes stopped.
