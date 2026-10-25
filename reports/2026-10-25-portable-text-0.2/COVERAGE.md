# Portable-text 0.2 experimental observations — 25 October 2026

This is an opt-in specification/test expansion, not a deployment or a change to
ACTOR requirements. All 26 cases ran once per caller with unchanged reader
defaults. The two HTTP peer cases use the other implementation. Consequently,
results describe each tested **caller/peer configuration**, not a standalone
conformance claim for either implementation.

| Caller | HTTP peer | Pass | Fail | Unsupported |
|---|---|---:|---:|---:|
| Native SWI | Trealla | 4 | 22 | 0 |
| Native Trealla | SWI | 20 | 6 | 0 |

Raw reports: [SWI](swi-portable-text.json), [Trealla](trealla-portable-text.json).
The [report](REPORT.md) distinguishes semantic differences, admission blocks
and unmeasured paths. Historical 0.1 results remain unchanged.

| Case | Requirement | SWI → Trealla configuration | Trealla → SWI configuration |
|---|---|---|---|
| TXT-001 | A double-quoted literal is a list of one-character atoms | fail | pass |
| TXT-002 | The empty double-quoted literal is the empty list | fail | pass |
| TXT-003 | A non-ASCII literal contains one Unicode character atom rather than UTF-8 bytes | fail | pass |
| TXT-004 | Double-quoted terminals retain DCG list semantics | fail | pass |
| TXT-005 | Source loaded into a session uses character-list semantics | fail | pass |
| TXT-006 | A serialized text binding can be resubmitted with the same list meaning | fail | pass |
| TXT-007 | Double-quoted text supports ordinary relational list operations | fail | pass |
| TXT-008 | A supplementary Unicode scalar is one character atom | fail | fail |
| TXT-009 | Combining marks are separate character atoms | fail | pass |
| TXT-010 | Reading preserves normalization distinctions | fail | pass |
| TXT-011 | Single-quoted text remains an atom | pass | pass |
| TXT-012 | Quoted text escapes preserve quotes and backslashes | fail | pass |
| TXT-013 | Quoted clauses in spawn options use the option reader semantics | fail | pass |
| TXT-014 | Constructed src_list terms preserve numeric lists and variable sharing | pass | fail |
| TXT-015 | Supplied DCG source compiles character terminals | fail | pass |
| TXT-016 | A private actor source module reads double quotes consistently | fail | pass |
| TXT-017 | Copied predicates preserve text through generated source | fail | pass |
| TXT-018 | URI-supplied source uses the same literal semantics | fail | pass |
| TXT-019 | Toplevel input replies use character-list literal semantics | fail | pass |
| TXT-020 | Unicode text survives serialized answer resubmission | fail | fail |
| TXT-021 | Empty text survives serialized answer resubmission | fail | pass |
| TXT-022 | Quotes and backslashes survive serialized answer resubmission | fail | pass |
| TXT-023 | A remote HTTP peer reads its supplied source consistently | pass | fail |
| TXT-024 | Remote answers preserve text code lists and variable sharing | pass | pass |
| TXT-025 | A joined emoji consists of scalar values rather than one grapheme | fail | fail |
| TXT-026 | Unicode input replies retain supplementary scalar characters | fail | fail |

Both source URI requests returned HTTP 200. No cases were waived or reclassified
as passing. GNU and both browser engines are **unmeasured in 0.2**. The native
7-case results previously recorded for 0.1 cannot substitute for this pack.

The runner's **47 unit tests pass**, including 15 new procedure/manifest tests.
These are test-harness checks, not additional language conformance cases.
