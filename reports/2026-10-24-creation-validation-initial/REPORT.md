# Literal-option admission diagnostics — 24 October 2026

The initial six-case run reported SWI 3/6 and Trealla 4/6 passes: **7/12**, five
failures. All raw reports, logs and the exact executed-manifest.json are retained.
These failures remain unresolved admission-path diagnostics. They are not counted
as passes or discarded by the final runtime-supplied-options selection.

| Candidate/case | Actual observation |
| --- | --- |
| SWI CV-002 | Improper literal option list rejected as an outer query error, rather than caught by the submitted catch/3. |
| SWI CV-003 | node(42) rejected as permission_error(option,sandboxed,node(42)) during admission, rather than the selected runtime type error. |
| SWI CV-006 | Socket name-resolution error before the intended unknown-option assertion; literal URI source preparation was reached. |
| Trealla CV-002 | Submitted query returned logical failure. The exact contributing assertion/admission transformation has not been reduced. |
| Trealla CV-003 | Outer query error type_error(text,42) with src_text/1 context, rather than the selected node type error. |

Literal creation calls can be inspected/transformed before query execution, so a
catch/3 in that query cannot catch all admission errors. These observations do
not establish which runtime validator is defective; no runtime repair was made.

The final pack delivers the same option values as ordinary self-messages, then
calls creation predicates with the received lists. This deliberately selects
runtime validation after admission. It also explicitly requires captured errors
to be nonvar. The node value, improper list, unknown option, callbacks and receive
timeouts were not relaxed. The unresolved literal paths remain separate.

Both initial disposable nodes stopped and all preservation checks passed.
See ../2026-10-24-creation-validation/REPORT.md for final scope and reproduction.
