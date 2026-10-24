# SWI runtime-bound specification repair — option-validation checkpoint

The unchanged runtime-supplied creation-option manifest passes **12/12** assertions
on disposable SWI/Trealla ACTOR nodes. See COVERAGE.md. No case, formal error,
callback or receive timeout changed. Original literal-admission diagnostics remain
separate and are not cleared by this checkpoint.

This rerun checks that SWI's supervisor guard and nonbinding data inspection retain
existing creation-option behavior. See ../2026-10-24-swi-runtime-specs-child-specs/REPORT.md
for repair, explicit working-tree candidate selection and broader test limits.
Its separate full T3 failure, existing whitelist startup restriction and literal
URI ordering finding remain documented; this pack does not waive them.

The exact pinned base and patch hashes, committed Trealla revision, separate
engine identities and commands are in provenance.json/preservation.json. The
--swi-source-candidate flag was explicit; the dependency pin and strict default
checker remain unchanged. All input hashes/preservation checks pass and both
fixture nodes stop. Installed executables and n3/n5 remain unchanged. The coverage
footer identifies the patched candidate; raw reports were not modified.

Reproduce with the existing adapter plus --swi-source-candidate and
cases/creation-validation-0.1.json, validate reports, then use the local coverage
renderer with --suite creation-validation. This is a finite blacklist checkpoint,
not general whitelist, remote, lifecycle, browser/GNU or security certification.
