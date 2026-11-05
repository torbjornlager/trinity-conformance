# Required standard-library repair — 5 November 2026

**Development sources only.** No commits, consumer pins, installed engines or
public services were changed for this repair. The public runtime-repair release
retains its separately recorded inputs.

The required forms and described binding/solution semantics in Appendix B's
four library source units (B-331–B-334) pass on SWI, Trealla, GNU and both browser
execution modes. The source-unit ledger now maps those clauses to exact shared
case IDs. This does not certify the complete external ISO mode/error inventory.

## Repairs

- Native SWI and both browser modes supply `maplist/6-8` and `countall/2` without
  explicit imports. Meta-predicate declarations retain private callback scope.
- GNU supplies guarded `memberchk/2`, `forall/2`, `countall/2` and the higher
  `maplist` forms. Its new counter is private and constant-space; callbacks stay
  in the ordinary local/shared execution policy. Submitted source cannot replace
  these entry points. Invalid count generators raise catchable execution errors.
- Trealla guards library callbacks under the current profile and sandbox,
  including computed closures. Its private-source runner preserves generator
  cut scope. `call_nth/2` rejects nonpositive ordinals with the common domain
  error. Copied source and remote spawn restore the public library calls.

The initial **57-case selection** produced **57 failures in 285 observations**:
12 on SWI, one on Trealla, 20 on GNU, and 12 in each browser mode. Its exact
manifest and raw reports are retained. The selection was subsequently expanded
and strengthened; these are not identical before/after test inventories.

The final **65-case selection** checks every listed predicate and arity,
positional list/accumulator order, nondeterminism, partial application, empty
closures, variable sharing, binding isolation, cuts, exceptions and selected
formal errors. All mirrored upstream fixtures are byte-identical.

- **325/325 shared checks:** 65 cases in each of five runtime modes.
- **130/130 retained-session checks:** the same cases on SWI and Trealla WSS
  sessions with private source.
- **2/2 browser child controls:** spawned actors use the required library with
  an explicitly copied private callback.
- **457/457 observations pass**, with no failing or unsupported results.

## Wider qualification

Native SWI's LINT, TEXT, T0, T2, T5, T1_NATIVE, T3_NATIVE and T4_NATIVE selection,
plus HTTP visitor ownership, pass. The new lower-layer test checks private actor
callbacks; the node tests check both sandbox modes through real HTTP.

Trealla passes **89 unit and 71 interoperability groups**, including 80 focused
library/sandbox controls and copied/inline library calls to a real native SWI
peer. The temporary runner uses one-second fixture startup waits for the released
x86 engine; no installed engine was modified.

GNU's complete `local-test`, including 65 mirrored cases, five callback controls
and five source-redefinition controls, passes. Its inventory/status checks pass.
The historical comparison lock and its separate certification scope are unchanged.

All **seven browser-package groups** pass: statechart unit, schema equivalence,
worker mailbox, standalone host, semantic contracts, real-browser standard
library and existing session/promise controls. The package is explicitly dirty
and cannot be used as a consumer release pin. Its runtime-file hashes match the
qualified working sources. An initial browser fixture omitted UTF-8 declarations;
that fixture-only failure is retained separately from the corrected baseline.

## Qualification boundary

The reference does not expand every external ISO mode and error into this
inventory. In particular, the invalid-closure case checks `type_error` and the
original culprit without claiming identical `atom` versus `callable` refinements
across all higher-order paths. B-014's grouped error contract and the broad ISO
requirements remain unverified; these passes must not be read as their certificate.
The native retained-context and multi-hop ownership audit also remains separate.

[verification.json](verification.json) records counts, scope and evidence hashes.
[native.json](native.json) records runtime source/binary fingerprints; [browser.json](browser.json)
records real public-session results and exact runtime/package fingerprints. Runtime
file hashes were rechecked after qualification; later documentation edits do not
alter those qualified inputs. The source diffs and new-file snapshots retain the
uncommitted implementation and test changes for review.
