# Strict Boolean options — close-out, 25 October 2026

This closes the previously tested Boolean batch separately from pending URI
work. The Boolean-only candidate was projected over the current committed heads
and exported into disposable source fixtures. Runtime and test bodies match the
historical Boolean patch hashes; later SWI DCG and Trealla src_list work remains
in the bases. README and Trealla test-integration hashes differ where those
later committed additions must be preserved; see the projection audit.

Fresh focused checks pass for native SWI and retained legacy Boolean/synchronous
units, Trealla Boolean and synchronous-wrapper groups, both actual SWI-WASM
engines under Node, and a separately compiled GNU worker. GNU reports 41 Boolean,
zero-request, precedence, paging and sharing assertions, plus six framing checks.
The two unchanged shared toplevel-wait selections pass 6/6 each, total 12/12.
These compatibility assertions are not new Boolean shared-profile cases.

The shared web manual states atom-only Boolean values, validation of every
asynchronous once option and the HTTP/JSON transport-decoding boundary. Appendix
B now states the same rule. Existing first-setting precedence and callback,
variable-sharing and timeout contracts are unchanged. Runtime-specific details
remain in READMEs. Historical reports are retained unedited.

This is a focused close-out, not a rerun of full acceptance or browser UI checks.
The historical intermittent native supervisor ownership finding remains separate;
no supervisor assertions, timeouts or runtime behaviour were adjusted here.

`checks/checks.json` records all fresh commands and exits; `checks/shared` records
source hashes, engine hashes, loopback endpoints, commands, raw results and node
cleanup. `candidate-bases.json` identifies the committed bases; actual projected
runtime hashes in the shared provenance identify the tested source, not merely a
version string. Original per-runtime verification directories retain the larger
24 October regressions and archived controls.

Only disposable fixtures and a temporary GNU worker were used. The installed
engines, launchers, existing GNU worker, dependency pin and n3/n5 are unchanged.
URI code remains separate for its own close-out and commit. No unrelated pending
Trealla acceptance staging material is included.

The reconciled Appendix B compiles in a temporary full-book build (both planned
convention additions present). The changed page was rendered and inspected;
`book-check.json` records the build. No published book.pdf was overwritten. The
first invocation needed an absolute path to the existing index style because
makeindex ran in the temporary output directory; source/configuration were not
changed to address that invocation issue.
