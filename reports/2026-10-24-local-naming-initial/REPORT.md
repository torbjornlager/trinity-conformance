# Initial local naming test construction run

This run is retained for transparency, **not as final naming coverage**.
executed-manifest.json records its exact inputs. SWI reported 5 passes and one
failure; Trealla reported six errors before the naming assertions executed.

Trealla's sandbox rejected format(atom(...),...) used for incidental name
construction as stream I/O. This existing policy difference is a separate
observation, not evidence about registration correctness. The final tests use
case-specific fixed atoms on isolated disposable nodes instead; runtime sandbox
policy is unchanged.

SWI LN-006 expected Trealla's counts(0,0) supervisor response. SWI uses a count
property list instead. The corrected query checks the common public
supervisor_which_children/2 empty list to establish that the retry is usable.
The named creation, registration and cleanup assertions and timeouts are retained.

See ../2026-10-24-local-naming/REPORT.md for the final corrected selection and
coverage. Both initial disposable nodes stopped and all preservation checks passed.
