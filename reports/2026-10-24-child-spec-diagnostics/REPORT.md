# Bounded child-specification diagnostics

This diagnostic-only pack is separate from required child-specification coverage.
It ran once per candidate with identical public queries; it cannot turn a required
failure into a pass.

| Probe | SWI | Trealla |
| --- | --- | --- |
| SVD-001 initial dynamic case with labelled waits | Outer instantiation error | sv_missing_stage(2) |
| SVD-002 runtime-bound initial list with execution output marker | Outer instantiation error | Runner timeout |

SVD-001's second wait receives sv_invalid(Invalid), before supervisor creation.
It establishes that the first dynamic-case failure does not occur while waiting
for a supervisor request reply. The final required case simplifies this setup and
retains a corresponding input-wait failure on Trealla.

SVD-002 is inconclusive on Trealla: the diagnostic output probe timed out. It is
not evidence that validation succeeded, that output was delivered, or that a
runtime bug was fixed. Its timeout is kept separate and is not investigated here.
The required pack contains no output marker.

Read-only sandbox inspection and qualifications are in the final required report.
No runtime change was made. Both diagnostic fixture nodes stopped and all source,
engine/library and live-node preservation checks passed. Raw reports validate.
