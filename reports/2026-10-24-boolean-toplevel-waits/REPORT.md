# Boolean repair compatibility checkpoint — 24 October 2026

All 12 selected toplevel-waits assertions pass on disposable SWI/Trealla ACTOR
nodes with the bounded Boolean candidate patches. No shared case, assertion or
timeout was changed. GNU ACTOR and browser/network behavior are not measured by
this pack. The new Boolean regression counts belong to implementation suites.

SWI candidate base is 786737f, selected explicitly as an unchanged-pin descendant;
Trealla candidate base is 7220bb5. Both are working-tree candidates identified by
provenance source hashes. Separate SWI 10.1.18 core/HTTP candidate and exact
unmodified Trealla 3.14.10 engines were used with matching libraries.

See the native and demonstrator docs/verification/boolean-options-2026-10-24/
reports, Trealla's reproducers/boolean-options-2026-10-24/, and GNU's
isobase/verification/boolean-options-2026-10-24/ for the audit and focused checks.
An intermittent native supervisor-ownership failure in a development T4 run is
retained separately; this compatibility result does not waive or resolve it.

Both fixture nodes stopped and all preservation flags are true. The patched
Prolog source stayed stable during execution. Installed engines, n3/n5 and the
demonstrator dependency pin were not changed. The schema/count validator passes.
