# Native SWI sandbox validation source identities

The shared validation loader used synthetic source-file names such as
`sandbox_source` and `sandbox_source_1` in every temporary validation module.
SWI tracks these as source identities independently of destination modules.
Overlapping validations therefore attempted to load one non-module source into
two live modules, raising `permission_error(load,source,Label)`. This explains
the previously intermittent BH-009 nested-supervisor source-loading failures.

The common loading helper now prefixes each logical source label with the unique
temporary module identity. Both unnumbered goal/source validation and numbered
source options use this path. Logical labels remain stable within one module,
so reloading that source retains its previous replacement semantics. The stream
handling, source prechecks, whitelist load options, materialization order and
module cleanup paths are unchanged. No global validation lock was added.

Regression evidence:

- The overlap regression keeps two temporary modules live at once, loading the
  same label with different facts. All four combinations of blacklist/whitelist
  and numbered/unnumbered labels fail on the old loader with the original
  permission error, and pass with the repair. No sleeps or scheduler timing are
  needed to reproduce the conflict.
- Five new test entries exercise twelve variants, covering module/content
  isolation, same-module reload, numbered source-option order and retained
  non-source options, forbidden directives, and module/predicate reclamation
  after success and exceptions.
- All 70 selected entries pass across the new suite, the existing public-goal
  guard suite and forty existing sandbox preparation/checking cases.
- Fresh public WebSocket conformance runs pass all seven core and ten behaviour
  cases on both SWI 10.1.17 and Trealla 3.13.10. BH-009 also passes five additional
  consecutive SWI attempts. Raw reports use the `2026-10-20-source-names-fixed-`
  prefix. These finite runs supplement the deterministic overlap regression.
- Diff whitespace checks pass. The language manual and Appendix B source hashes
  are unchanged from the start of this batch; book examples were not edited.

Implementation notes were added only to the native runtime README. Disposable
nodes on ports 39860/39861 were stopped. Running n3/n5 were unchanged. No commit,
push, deployment or book build was performed.
