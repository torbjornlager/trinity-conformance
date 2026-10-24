# SWI runtime-bound specification repair — shared checkpoint

## Outcome

The unchanged child-specification manifest now passes **12/12 required assertions**:
SWI 6/6 and Trealla 6/6. See COVERAGE.md and raw reports. The five previously blocked
SWI initial-specification cases now reach their intended validation assertions.
Dynamic sibling preservation/retry also remains passing. No shared assertion,
error allowance, input, callback or timeout was changed. Historical matrices and
raw failures are retained at their original paths.

Companion admission probes record 20 complete observations without timeouts; SWI
AP-002/004 now enter execution rather than producing an outer instantiation error.
Creation-option runtime validation remains 12/12. All schema/accounting checks and
29 conformance-runner regressions pass.

## Repair and separate findings

SWI admission now treats unknown specifications as data, with nonbinding inspection
of known starts. A registered node guard checks actual normalised child goals
before initial/nested startup or dynamic dispatch. Existing profile, source and
per-child checks remain active. Source context and shared variables are retained.

The sibling swi-prolog-node repository's verification report under
 docs/verification/runtime-supervisor-admission-2026-10-24 records focused tests,
archived-source controls, patch hashes and regression logs. Its 28 focused checks,
full T4_NATIVE and layering lint pass. Its full T3_NATIVE has one unresolved
provisional-replacement cleanup test failure. Three isolated archived-source and
three candidate controls pass, which neither reproduces nor clears that full-tier
failure. Whitelist startup still has an internal-framework restriction reproduced
on both archived and candidate sources. Those findings remain separate; this green
blacklist conformance matrix does not certify all native behavior or whitelist.
SWI's literal URI preparation ordering finding also remains unchanged.

## Explicit candidate evaluation and unchanged pin

The strict adapter initially refused the modified pinned checkout before creating
fixtures. The new --swi-source-candidate flag is explicit test-only selection: it
requires the same exact pinned base revision and records working-tree source
hashes. Without that flag the existing strict checker is still called. Three
unit regressions cover the default, candidate metadata and changed-base rejection.
The dependency pin and production launcher are not modified. Its byte hash is
recorded and compared before/after every fixture run.

Provenance identifies the native base f316e65503bff863dfbd2e182f7487988c91480c plus
uncommitted source status/hashes; a base commit alone does not identify the patch.
Trealla source remains committed 7220bb5. Engines are the separate verified SWI
10.1.18 candidate (core 09b6299 plus HTTP shutdown patch) and unmodified Trealla
v3.14.10 4ef56e3bbbcc6ca44085a4aa5eae0e6848c70294 with its matching library.
All executed manifest/tool and final native .pl hashes match recorded inputs.
New candidate code was uncommitted while run and is identified by its eventual
containing commit plus native patch-inputs.json.

All preservation checks are true and both disposable nodes stop. Native candidate
files, Trealla, selected engines/library, pin bytes and live n3/n5 identities stayed
stable during fixtures. Installed binary targets/hashes match the prior reference.
No installed runtime, launcher, restart/reload, access setting or dependency pin
changed. The coverage footer identifies the patched candidate; raw reports and
provenance were not rewritten.

## Reproduction and limits

Use adapters/local_promises.py with --swi-source-candidate and
--local-manifest cases/child-specs-0.1.json, the same pinned-base native working-tree
patch, separate engine paths, committed Trealla source and a fresh output path.
Validate with runner/validate_reports.py and render with runner/links_coverage.py
--suite child-specs. README and provenance give full command forms.

This finite ACTOR/blacklist run excludes full whitelist operation, remote
supervision, concurrency, engine installation, browser/GNU and general lifecycle
or security certification. The old failures remain historical evidence, not a
replacement for the separate unresolved findings described above.
