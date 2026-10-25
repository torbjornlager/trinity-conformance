# Portable-text migration checkpoint — 25 October 2026

**Experimental SWI testing, not a deployment or a new shared-profile requirement.**
Runtime modules remain byte-identical to native SWI commit `c347b11`; only tests
and reports change. Installed runtimes, dependency pin and n3/n5 are unchanged.

| Selection | Default strings | Experimental character lists |
|---|---|---|
| Representation-specific migration contracts | 4/4 original contracts pass | 4/4 distinct counterparts pass |
| Full SWI T4_NATIVE | 1041 active named tests; **1529/1529 parameter selections pass** | 1041 active named tests; **1529/1529 pass** |
| TEXT tier, including explicit native-library conversions | 30 named tests; **40/40 selections pass** | 30 named tests; **40/40 pass** |
| Read-only example checks | **10/10 pass** | **10/10 pass** |

Rows overlap; their totals must not be added into a conformance score. The four
original default test bodies and expected values are preserved. Each process
selects its own exact representation contract, rather than accepting either
representation in one weakened assertion.

The example checks include five unchanged tutorial queries, the word-list
grammar, common/actor/n3 shared source, and pure checks confirming the model/Jev
native-string mismatch. Passing a diagnostic check that confirms rejection is
**not** a claim that those application services already accept portable text.
No external model/Jev service was called. All audited example hashes match.

## Audit findings and remaining work

The read-only inventory covers ten tutorial pages (500 preformatted blocks),
44 parsed Prolog sources and 21 XML statecharts. It is not full execution of all
examples. Core shared clauses and checked format/source examples work unchanged;
model-actor 21, model-statechart 19 and model/Jev service guards still require
native strings. Jev request/reply JSON boundaries and displayed reply expectations
also need an explicit migration batch with mocked providers.

Opaque native-string identity is still outside the portable character-list wire
claim. Earlier T3 supervisor/SGML diagnostics remain separate and were not rerun
or repaired. Browser/GNU migration, invalid encodings, performance and book
example migration remain untested. Shared cross-runtime packs were not rerun in
this test-only batch; their previous committed results are preserved unchanged.

## Evidence

The native repository contains the full report, raw logs, query inputs, static
inventory, original-body hashes and engine/example preservation checks:

[`swi-prolog-node/docs/verification/portable-text-migration-2026-10-25/REPORT.md`](https://github.com/torbjornlager/swi-prolog-node/blob/main/docs/verification/portable-text-migration-2026-10-25/REPORT.md)

The [local summary](results.json) records test-file hashes and the native working
candidate base. Earlier matrices, including the original four representation
failures, remain historical evidence rather than being edited into passes.
