# Source-capture repair: evidence and limits

The earlier [GNU framing report](../2026-10-21-gnu-request-framing/trealla-actor-behaviours.json)
retains a BH-007 shell-startup failure with `syntax_error(read_term)`. Its fresh
repeat passed. Before this repair, assessment also passed 200 sequential
source-shell starts and 30 complete behaviour packs without reproducing that
specific failure. Those observations do not establish that the source was valid
under every concurrent interleaving.

A separate forced-interleaving test demonstrates shared output-capture
contamination in the pinned engine: expected `actual(beta,alphaomega)`, observed
`actual(betaomega,alpha)`. SWI 10.1.17 returns the expected result. Concurrent
calls to the real bootstrap generator returned 40,951 and 299 characters instead
of two identical 20,829-character sources. The workaround removes shared output
capture from bootstrap generation and the HTTP/WebSocket display serializers.
It does not repair public `with_output_to/2` in the engine.

Before/after full and minimal bootstrap files were compared byte-for-byte for
module `probe`; both were unchanged. The new concurrency regression fails with
`mismatch(concurrent_snapshot)` against a temporary copy of the pre-repair
runtime files, and passes after the repair. Ten repeated post-repair runs each
checked 100 snapshots in each of two concurrent threads, plus surrounding-output
capture and quoting/sharing assertions. A final run also checks parsing of a
bootstrap whose module name contains an apostrophe and backslash.

Additional checks passed: HTTP private-source/cache regression, toplevel group,
source declarations and canonical answers. The recorded legacy isolation and
sandbox groups exit 0 but print respectively `missing arg` and `start of rule
expected` parser messages. Their raw outputs are retained in the adjacent
`*-regression.txt` files; these are unclassified diagnostics, not claimed fixed
or silently discarded. The public ACTOR rerun has no source-parsing failure.

The original intermittent failure's attribution to shared capture is strongly
supported, not conclusive. The separate prepared upstream report and standalone
reproducer are in the Trealla repository at
`reproducers/bug-026-concurrent-output-capture.{md,pl}`. They have not been
submitted and do not claim a current-upstream reproduction.

To rerun the public packs, start a disposable Trealla node from `trealla-port`
with its matching `TPL_LIBRARY_PATH` and the following goal (substitute PORT):

```prolog
consult('distribution.pl'),
web_prolog:web_prolog_node(PORT,[bind_address('127.0.0.1'),
    node_url('http://127.0.0.1:PORT'),profile(actor),
    sandbox(blacklist),auth(open)]),
thread_get_message(stop)
```

Use `runner/baseline.py --url ws://127.0.0.1:PORT/ws --candidate trealla
--profile actor` for `cases/language-actor-0.1.json` and
`cases/wire-capabilities-0.1.json`. Use `runner/run.py --ws-url
ws://127.0.0.1:PORT/ws --candidate trealla --timeout 8` for the other seven suites
listed in COVERAGE.md. Pass each manifest with `--manifest` and retain a fresh
JSON output using `--report`. Stop only that disposable node afterwards.
