# Committed local adoption checkpoint — 25 October 2026

This checkpoint adopts verified local implementations. It does not change shared
baseline requirements, pack totals or the experimental status of portable-text
specification work. Historical results and diagnostics are preserved.

| Selected implementation | Revision |
| --- | --- |
| SWI | `abbc56f3d5104bd6d40d2ed5f99fe6199d75c4a8` |
| Trealla | `e7c51dc101cd8002dea9548f8154fc4d2bf6707d` |
| Demonstrator | `5b4deb3aeee6e3b9bc66592d0554e4e1e65535ad` |

| Checkpoint coverage | Result |
| --- | --- |
| Native SWI tiers and integration/origin gates | Pass |
| SWI TEXT both modes; full native T4 in chars | Pass |
| Trealla full unit driver | Pass |
| Model/Jev default and character-list regressions | Pass |
| Full WASM tier at the final selected demonstrator commit | Pass |
| Commit/clean-input startup guards | 4/4 |
| Public post-restart interoperability smoke checks | 29/29 |
| Unicode/private source/application boundary smoke checks | 10/10 |
| Actual n3 text and n5 ping-pong UI checks | Pass |

The first browser attempts exposed a missing Node.js PATH entry and a stale
structural greeting assertion. The bundled Node.js and a separate test-only
alignment resolved them; the final complete browser tier passes. No runtime
assertion or deadline was weakened. Original failed attempts are retained.

[Full report and evidence](../../../trinity-demonstrator/docs/verification/committed-adoption-2026-10-25/REPORT.md)
record commands, source selections, launcher guards, rollback and unchanged
engines. Regular local n3 explicitly selects character-list reading; n5 retains
its character-list reader. Browser/GNU text configurations are unchanged.

Trealla cyclic-exception copying, supplementary Unicode JSON surrogate escapes,
broader portable-text diagnostics and ISO-mode assessment findings remain
separate. They are not passing conformance cases. This batch does not rerun every
historical shared pack or promote untested capabilities to supported ones.
