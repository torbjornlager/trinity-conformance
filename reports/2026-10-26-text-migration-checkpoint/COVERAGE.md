# Text checkpoint coverage — 26 October 2026

Scope and interpretation: [report](REPORT.md). Historical baseline results are unchanged.
`P` = assertion passed; `J` = JSON surrogate-pair diagnostic; `U` = URI policy blocked;
`C` = cross-origin fetch blocked. A diagnostic is not a pass.

Native default reports use escaped JSON. The UTF-8 column repeats all 26 Trealla
cases with literal UTF-8 JSON, preserving goals and assertions. Browser source
procedures and exact displayed-binding round trips are explained in the report.

| Case | Assertion | SWI native | Trealla default | Trealla UTF-8 control | Worker UI | Main UI |
|---|---|---|---|---|---|---|
| TXT-001 | A double-quoted literal is a list of one-character atoms | P | P | P | P | P |
| TXT-002 | The empty double-quoted literal is the empty list | P | P | P | P | P |
| TXT-003 | A non-ASCII literal contains one Unicode character atom rather than UTF-8 bytes | P | P | P | P | P |
| TXT-004 | Double-quoted terminals retain DCG list semantics | P | P | P | P | P |
| TXT-005 | Source loaded into a session uses character-list semantics | P | P | P | P | P |
| TXT-006 | A serialized text binding can be resubmitted with the same list meaning | P | P | P | P | P |
| TXT-007 | Double-quoted text supports ordinary relational list operations | P | P | P | P | P |
| TXT-008 | A supplementary Unicode scalar is one character atom | P | J | P | P | P |
| TXT-009 | Combining marks are separate character atoms | P | P | P | P | P |
| TXT-010 | Reading preserves normalization distinctions | P | P | P | P | P |
| TXT-011 | Single-quoted text remains an atom | P | P | P | P | P |
| TXT-012 | Quoted text escapes preserve quotes and backslashes | P | P | P | P | P |
| TXT-013 | Quoted clauses in spawn options use the option reader semantics | P | P | P | P | P |
| TXT-014 | Constructed src_list terms preserve numeric lists and variable sharing | P | P | P | P | P |
| TXT-015 | Supplied DCG source compiles character terminals | P | P | P | P | P |
| TXT-016 | A private actor source module reads double quotes consistently | P | P | P | P | P |
| TXT-017 | Copied predicates preserve text through generated source | P | P | P | P | P |
| TXT-018 | URI-supplied source uses the same literal semantics | P | P | P | U | U |
| TXT-019 | Toplevel input replies use character-list literal semantics | P | P | P | P | P |
| TXT-020 | Unicode text survives serialized answer resubmission | P | J | P | P | P |
| TXT-021 | Empty text survives serialized answer resubmission | P | P | P | P | P |
| TXT-022 | Quotes and backslashes survive serialized answer resubmission | P | P | P | P | P |
| TXT-023 | A remote HTTP peer reads its supplied source consistently | P | P | P | C | C |
| TXT-024 | Remote answers preserve text code lists and variable sharing | P | P | P | C | C |
| TXT-025 | A joined emoji consists of scalar values rather than one grapheme | P | J | P | P | P |
| TXT-026 | Unicode input replies retain supplementary scalar characters | P | J | P | P | P |

| Selection | SWI native | Trealla native | Worker UI | Main UI |
|---|---|---|---|---|
| Actual `write("abc")` output `[a,b,c]` | P | P | P | P |
| Promise text template, sharing and caller isolation | P | P | P | P |
| ASCII-only supplementary scalar construction | P | P | Not run | Not run |
| `atom_to_term/3` character-list reader control | Diagnostic: native string | P | P | P |
| Same-origin HTTP source + sharing controls | See native opposite-peer pack | See native opposite-peer pack | 2 P | 2 P |
| Displayed bindings resubmitted (ASCII, Unicode, empty, escaped) | 4 P in original pack | 3 P default; 4 P UTF-8 | 4 P | 4 P |

Each browser has 26 mapped cases (23 P, 3 diagnostics) and nine additional
controls (9 P): **32 passed, 3 diagnostics per mode**. Controls overlap the
original pack and must not be added as independent language coverage.

No GNU rerun, full library audit, dedicated shared-DB text assertion, deployed-node
test queries, new profile obligation or claim of browser-to-Trealla cross-origin
success is included. All temporary fixtures were stopped.
