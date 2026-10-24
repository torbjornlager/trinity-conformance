# SWI spawn source-validation candidate — 24 October 2026

This run evaluates a working-tree plain spawn/3 repair over native commit
8c90a4dedcee7e6c590a5745fed02fc6b986dcbf, alongside committed Trealla 7220bb5.
The demonstrator dependency pin remains f316e65503bff863dfbd2e182f7487988c91480c.
The fixture explicitly selects the exact descendant base, checks ancestry and
records all source hashes; its strict default still requires the clean pin.

The admission pack records 20 complete observations with no diagnostic errors.
AP-009 now fails with a spawn_option domain error before query entry rather than
a URI socket error. AP-010 still catches the runtime error. The admission errors
remain diagnostics, not conformance passes. The required creation-validation and
child-specs packs each pass 12/12. See the matrices in the three sibling
2026-10-24-swi-spawn-source-* directories and each raw report for exact commands
and replies. No manifest, assertion or timeout was changed.

The new native loopback regression fixture additionally counts source HTTP
requests: invalid ground options and still-invalid runtime options make none;
pending values are not bound during admission, and runtime source order, sharing,
sandbox, origin and size checks remain active. The native final T4_NATIVE and
focused checks pass. Detailed implementation and native test evidence are in
swi-prolog-node/docs/verification/spawn-source-validation-2026-10-24/REPORT.md.
The previous T3 failure and whitelist supervisor startup restriction remain
separate; neither is claimed fixed here.

provenance.json records commands, source identities, engines, libraries and
input hashes. preservation.json shows all checks true; disposable nodes stopped.
Only the intended patched SWI source was evaluated, stable during each final run.
Installed executable targets/hashes were checked separately. The dependency pin,
installed runtimes, live n3/n5 and Trealla sources remain unchanged. README edits
after the runs document the results and do not change tested Prolog inputs.
The shared runner has 32 passing unit tests, including exact candidate selection
and diagnostic error rendering. Previous coverage reports remain intact.
