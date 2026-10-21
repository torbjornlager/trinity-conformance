# Trealla HTTP source-loading follow-up

This run uses the unchanged baseline 0.1 manifests and assertions on disposable
loopback nodes. It tests the Trealla working-tree repair identified in
[repair-inputs.json](repair-inputs.json); the installed engine and live N3/N5
were not changed. See [coverage](COVERAGE.md), [provenance](provenance.json) and
the [initial run](../2026-10-21-baseline-0.1/COVERAGE.md).

- Trealla IB-006 and IB-010 now pass: submitted HTTP source executes and remains
  private. All three native HTTP destinations pass 10/10 selected ISOBASE cases.
- Required selections: 87/94 pass, up from 85/94. The seven remaining failures
  are the existing six Trealla HTTP-context RPC/promise cases and GNU-to-Trealla
  promise case. They remain failures, without waivers or assertion changes.
- Supporting native ACTOR contracts remain 66/66. Both real SWI-WASM engine
  adapters retain 7/7 local language cases. Diagnostic and experimental results
  remain separate; the matrix command exits nonzero for the outstanding cases.
- The shared fixture still parenthesizes goal/template fields uniformly.
  Unparenthesized operator parsing remains a separate Trealla diagnostic.

The repair reads inline source, admits it through the existing profile/sandbox
and source-size checks, and loads it into the page producer's private namespace.
Source and admission policy participate in continuation identity. Final/error
source producers wait for the existing owner scope to stop them: this prevents
natural private-module destruction from racing monitored scope termination.
Source-free execution and public request/reply formats are unchanged.

The Trealla-specific `http_source_tests.pl` suite covers both sandbox modes,
ISOBASE admission, source/policy cache separation, continuation reuse,
`once(true)`, shared variables, private mutation, size/syntax/unsafe-source
rejection, runtime guards, failure/error/deadline cleanup, public HTTP paging,
JSON bindings, and source-bearing RPC/promise clients. Six consecutive complete
runs passed after the repair (an earlier source-only version passed ten runs).
The test client imports RPC before the node, using its complete client module;
this does not repair or waive the separately failing HTTP callable context.

The existing HTTP paging cleanup, whole-page deadline, FIFO eviction, paging
offset and server-side once regression suites also passed after the repair.
All 39 conformance reports pass schema/accounting validation.

Runtime regressions and conformance evidence concern selected observable paths,
not a general guarantee of sandbox completeness or arbitrary concurrency safety.
