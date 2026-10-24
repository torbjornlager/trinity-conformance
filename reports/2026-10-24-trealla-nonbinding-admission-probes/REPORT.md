# Trealla nonbinding repair — admission observations

All **20 diagnostic observations completed**, without diagnostic errors or probe
timeouts. These are not conformance passes. See DIAGNOSTICS.md and the exact
command/decoded-response transcripts in the two raw reports.

Trealla AP-006/008 now report PatternState=unbound and Matched=yes. The valid
runtime addition returns ok and one child; the invalid one catches
missing_start_option(probe), with an empty child list. Literal controls continue
to work, and initial runtime lists still work on Trealla. This replaces the
pre-repair bound(child(_,[start(server(_,_))|_])) / not_dispatched observation.

SWI AP-002/004 still return instantiation errors before query entry, and AP-009
still reaches literal URI preparation before the later unknown-option error.
These observations are not claimed fixed. The historical diagnostic matrix,
entry-marker controls and required conformance failures are not rewritten.

The manifest/capture runner and all timeouts are unchanged from the committed
investigation. The existing adapter ran on disposable loopback ACTOR/blacklist
fixtures. Exact source commits/status, changed-file hashes, engine identities and
commands are in provenance.json and preservation.json. The separate engine builds
are unchanged; the Trealla source repair is loaded from its working tree.
All source/binary/library/live-node preservation checks pass and both nodes stop.
Installed executable targets/hashes and n3/n5 remain unchanged. The generated
matrix footer was clarified to identify the patched source under test; raw
transcripts were not modified.

See ../2026-10-24-trealla-nonbinding-child-specs/REPORT.md and the sibling Trealla
verification report for repair/regression details and qualifications. Reproduce
with the same local adapter and cases/admission-paths-0.1.json, validate the raw
reports, then run runner/admission_coverage.py on a fresh output directory.
This is a finite blacklist diagnostic, not whitelist expansion, full security,
remote transport, browser/GNU or lifecycle certification.
