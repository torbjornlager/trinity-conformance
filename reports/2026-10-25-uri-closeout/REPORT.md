# Canonical URI inputs — close-out, 25 October 2026

This closes the previously tested URI batch over the separately committed strict
Boolean changes. `preceding-boolean-commits.json` records those commits. Disposable
fixtures use those heads plus the URI source changes; their exact runtime hashes,
engine identities and commands are in `checks/shared/provenance.json`.

The historical URI runtime/test hashes still match. README additions, the
Trealla test runner's later committed src_list integration, and the reconciled
web manual explain the remaining documentation/integration differences recorded
in `historical-evidence-audit.json`. Existing Boolean checks remain integrated.
No URI runtime repair was expanded during this close-out.

## Fresh checks

- Native SWI and retained legacy URI/Boolean/synchronous units pass.
- Trealla URI, existing RPC-option and source-policy groups pass. Its live URI
  text-form/Host:Port RPC/promise check passes against a disposable SWI peer.
- Both actual SWI-WASM engines under Node pass URI normalization, early-error,
  no-operation and result-sharing scenarios. This is not a browser UI/network run.
- A separately compiled GNU worker passes 22 URI assertions, 41 Boolean assertions
  and six request-framing/sharing assertions. The existing worker is unchanged.
- The unchanged shared promise/yield pack passes 24/24 assertions and the HTTP
  interoperability selections pass 8/8 in all four native caller/peer directions.
  These compatibility results do not add new shared URI case counts.

## Manual reconciliation

The shared web manual and Appendix B now document canonical URI atoms, each
runtime's supported boundary text forms, checked/nonbinding Host:Port shorthand,
GNU source-URI shorthand, early representation errors and unchanged fetch/URI
policies. Double-quoted text does not establish a common portable string type.
Both recommend atoms for portable source text, preserving each runtime's extra
boundary forms. Appendix B identifies GNU's ISOBASE scope. The web manual's
native implementation link now points to swi-prolog-node and includes a GNU
guide link; runtime implementation detail stays in READMEs.

The temporary full-book compilation passes, and the changed Appendix B page was
rendered and inspected (`book-check.json`). No published `book.pdf` was replaced.
An initial makeindex invocation could not locate its relative existing style in
the temporary output directory; the final command supplies that style's absolute
path. No source/configuration change was needed for that invocation issue.

## Boundaries

Historical reports are unchanged. The older supervisor-ownership development
failure, admission diagnostics, experimental portable text/DCG findings and
unrelated Trealla acceptance staging remain separate. Full suites, deployment
acceptance, GNU shared baseline and browser real-network checks are not claimed
by this focused close-out.

All disposable nodes stop after the checks. Installed engines/launchers, the
existing GNU worker, matching libraries, dependency pin and n3/n5 identities
remain unchanged. Source fixes are committed; no pin promotion or deployment is
included. Shared schemas/accounting and preservation checks pass.

`source-commits.json` maps the separately committed Boolean and URI changes
across the native, browser/legacy, GNU and book repositories. Staged runtime/test
bytes were checked against the disposable fixtures before committing.
