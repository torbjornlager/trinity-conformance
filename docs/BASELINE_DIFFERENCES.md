# Baseline 0.1: unresolved and excluded differences

This register records decisions that the small baseline does **not** make.
A failing selected requirement stays a failure even if its cause also has an
entry here. Runtime repairs are outside the consolidation batch.

| Area | Existing authority / observation | Treatment |
|---|---|---|
| GNU ISOBASE inventory | GNU draft 0.2.0 contains 97 required predicate/arities, explicit boundary decisions and incomplete mode coverage. | Baseline HTTP smoke tests are a subset, not a substitute for that audit. Historical 39-probe/broad-comparison totals are not rerun claims. |
| Zero page limit | GNU D01/K01 remains open; native clients reject zero while historical GNU tests accept it. | IBD-001 records current behavior; required paging fixtures use positive limits. |
| Numeric semantics | GNU B01 requires ISO float result for `**`; SWI has an integer-result extension. Other conversion/domain questions remain. | IBD-002/005 retain observations and GNU obligation links. No resolution or numeric repair here. |
| Portable text | `portable-text-0.1` is experimental; native string conventions differ. | IBD-003 and the separate experimental pack do not become requirements of `actor`. |
| Address/options/deadlines | GNU contract B24–42 and K01/K06 specify obligations beyond these selected fixtures. | Preserve that contract and its evidence; do not infer compatibility from HTTP success alone. |
| Malformed goals and HTTP framing | Error/status presentation and unparenthesized operator fragments can differ. | IBD-004/006 record them. Baseline sends parenthesized goal/template fields uniformly; no per-runtime rewriting. |
| Nested supervisor admission | SCD-001 is an existing static-vs-runtime-bound admission difference. | Existing diagnostic remains separate. No input-policy repair or new waiver. |
| Worker/supervisor races | Diagnostic passes only mean no occurrence in those attempts. | Preserve IDs and reports; do not promote a stress pass into a universal cleanup guarantee. |
| Legacy transport | Untagged errors cannot reliably identify the command that caused them. | Modern capability and legacy fallback are distinct contracts. Tests do not infer spawn correlation from query correlation. |
| Delegated lineage/cancellation | Trealla lacks `lineage_close`; remote effects may survive contact loss. | No blanket no-orphan or cancellation claim. Existing ownership, monitoring and cleanup qualifications stand. |
| Browser/network surface | SWI-WASM executes inside a browser; it is not a GNU-style HTTP server. | Local language fixtures use real engines under Node. HTTP-server/wire-server cells are not applicable; browser network and UI cells are untested here. |

The current matrix adds concrete failures observed in this run. If a shared
manual statement and a draft test disagree, record the conflict and obtain a
semantic decision before modifying either to match an implementation.
