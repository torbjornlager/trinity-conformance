# Trealla nonbinding repair — child-specification checkpoint

## Outcome

Trealla passes **6/6** unchanged required cases. SWI passes **1/6** with its five
runtime-bound initial-list admission failures still visible: combined **7/12**.
See [COVERAGE.md](COVERAGE.md). The historical 6/12 matrix is not overwritten and
no required assertion, input manifest, receive timeout or diagnostic classification
was changed. The fixture adapter's exit 1 is expected from the retained SWI
failures; it is not interpreted as a successful combined pack.

SV-006 now receives its invalid dynamic specification, catches the missing-start
error, preserves the exact sibling list and its ability to respond, adds the
valid retry and collects its public termination notifications. Trealla's repair
therefore closes the previously failing dynamic case. It does not close SWI's
separate admission restrictions.

## Repair and regression evidence

Trealla's profile and sandbox checkers now share nonbinding child-specification
inspection. Opaque terms remain subject to conservative whitelist rejection;
blacklist-prepared supervisor calls recheck actual supplied goals before dispatch.
Private source and copied constructor helpers retain their receiving context.
No language manual, book example, engine installation or lifecycle policy changed.

The sibling Trealla repository records focused tests, eight final applicable
regression groups, an archived pre-repair binding control and exact patch hashes
under docs/verification/nonbinding-supervisor-admission-2026-10-24. One existing
behaviour test's prepared-term expectation now explicitly requires the new guard;
its profile and forbidden-goal assertions remain. A separate copied-timeout-options
fixture observation is qualified there and was not repaired. The final shared
manifests are unchanged.

The companion admission matrix is at
../2026-10-24-trealla-nonbinding-admission-probes/DIAGNOSTICS.md; creation validation
remains 12/12 at ../2026-10-24-trealla-nonbinding-creation-validation/COVERAGE.md.
All schema/accounting checks and all 26 conformance-runner regressions pass.

## Provenance and preservation

The existing adapter ran the exact cases/child-specs-0.1.json manifest against
separate loopback ACTOR/blacklist/open fixtures. SWI uses external source pin
f316e65503bff863dfbd2e182f7487988c91480c with the verified separate 10.1.18 candidate
(core 09b6299 plus HTTP shutdown patch). Trealla uses the separate unmodified
v3.14.10 engine 4ef56e3bbbcc6ca44085a4aa5eae0e6848c70294 and matching library,
loading the working-tree source repair over base d4e96a3. This is an adapter patch,
not an engine patch. Exact input/source/binary hashes and commands are in
provenance.json and preservation.json. Final .pl hashes match the final patch.
New code was uncommitted during execution; the eventual containing commit and
Trealla patch-inputs.json identify it without relying on base commit alone.

All preservation checks are true: native SWI files, patched Trealla sources,
selected engines/library and live n3/n5 identities stayed stable during fixtures.
Both nodes stopped. installed-preservation.json confirms installed executable
targets/hashes still match the earlier reference. No installed engine, launcher,
restart, reload or repository access changed. The coverage footer was clarified
to identify the patched candidate, rather than imply no runtime source repair.
The raw reports/provenance were not rewritten.

## Reproduction and limits

Use adapters/local_promises.py with --local-manifest cases/child-specs-0.1.json,
separate verified engine paths, the pinned native SWI checkout, the patched
Trealla checkout and a fresh output directory. Run runner/validate_reports.py and
runner/links_coverage.py --suite child-specs on that output. The top-level README
supplies the full command shape; provenance retains this run's exact arguments.

This finite checkpoint excludes whitelist expansion, exhaustive options,
concurrency, remote supervision, browser/GNU runtimes and general lifecycle or
security certification. Existing SWI failures and unrelated diagnostics remain.
