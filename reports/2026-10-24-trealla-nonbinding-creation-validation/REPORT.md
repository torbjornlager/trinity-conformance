# Trealla nonbinding repair — creation-option regression checkpoint

The exact committed runtime-supplied-option manifest still passes **12/12**:
six identical public assertions per disposable native SWI/Trealla ACTOR node.
See COVERAGE.md. No case, formal-error allowance, callback, assertion or timeout
changed. The historical literal-option admission failures remain separate and
are not cleared by this checkpoint.

This rerun checks that the nonbinding supervisor traversal and its dispatch guard
preserve existing creation-option behavior. The companion child-specification
pack now passes Trealla 6/6 while retaining five SWI failures; the separate
admission probes record the corrected Trealla variable/message behavior.

See ../2026-10-24-trealla-nonbinding-child-specs/REPORT.md for exact revisions,
engine prerequisites, regression groups and limitations. This run's full
commands, input/source/binary hashes and source status are in provenance.json
and preservation.json. The patched Trealla .pl hashes match the final candidate;
selected engines and installed runtimes were not changed.

All preservation checks pass and both disposable nodes stop. Installed binary
targets/hashes and live n3/n5 identities remain unchanged. The coverage footer was
clarified for the patched candidate; raw results were not rewritten. Reproduce
through the existing local adapter with cases/creation-validation-0.1.json,
validate reports, then render using runner/links_coverage.py --suite creation-validation.
No complete security, remote, browser/GNU or lifecycle certification is claimed.
