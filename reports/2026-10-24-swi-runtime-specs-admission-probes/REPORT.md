# SWI runtime-bound specification repair — admission observations

All **20 diagnostic observations completed**, without probe errors/timeouts.
DIAGNOSTICS.md describes actual responses and entry markers; these are not
conformance passes. Exact sent commands and decoded response transcripts remain
in the raw reports.

SWI AP-002 now enters and creates the runtime-supplied initial child list; AP-004
now enters and catches missing_start_option(probe). Static valid/invalid controls
continue to work. SWI AP-009 still produces its literal URI preparation error
before entry; that separate ordering finding remains unresolved. Trealla's
committed nonbinding behavior is unchanged.

The exact committed manifest/capture code and all timeouts are unchanged. Native
SWI was selected explicitly with --swi-source-candidate over the unchanged pinned
base, never by weakening the production pin checker. Source snapshots, commands,
base revisions, pin bytes and engine identities are in provenance/preservation.
Both fixture nodes stopped and every preservation check passed. Installed
executables, Trealla, the dependency pin and live n3/n5 remain unchanged.

See ../2026-10-24-swi-runtime-specs-child-specs/REPORT.md and the sibling native
verification report for patch details and the separate broad T3/whitelist findings.
The diagnostic footer identifies the patch under test; raw observations are intact.
Reproduce with the local adapter's explicit candidate flag and
cases/admission-paths-0.1.json, then validate and run runner/admission_coverage.py.
No complete whitelist, lifecycle, remote, browser/GNU or security claim is made.
