# Isolated SWI portable-text experiment

The [coverage matrix](COVERAGE.md) records the configured candidate, its ordinary
reader control and the unmodified-Trealla control separately. The native report
contains the reader changes, shared-database checks, library conversion audit,
native-tier results and separate diagnostics:

`/Users/torbjorn.lager/Documents/GitHub/swi-prolog-node/docs/verification/portable-text-configuration-2026-10-25/REPORT.md`

All public-interface assertions, manifests and timeouts are unchanged. The
adapter overlays only explicit SWI candidate sources, passes the experimental
selector only to its owned SWI process, trusts only loopback for the disposable
Trealla transport and tears down owned nodes. Installed runtimes and n3/n5 are
unchanged. Unrelated acceptance staging is untouched.

The provenance's older generic configuration prose says unchanged readers;
its explicit `experimental_swi_configuration: true`, commands and source overlay
identify the actual candidate. The adapter now describes the mode directly in
future records. Intermediate development runs are not added to pass counts.

[Shared input hashes](shared-inputs.json) additionally verify that every executed
public manifest and both existing assertion runners still match the committed
conformance revision. The adapter now includes these inputs directly when
`--shared-checks` is selected. These are provenance/accounting improvements;
the runtime checks above executed the same unchanged assertions.
