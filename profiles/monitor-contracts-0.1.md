# Monitor contracts 0.1

The [49-case shared selection](../cases/monitor-contracts-0.1.json) exercises native
SWI, native Trealla, SWI-WASM Worker and SWI-WASM main execution. GNU ISOBASE does
not advertise the ACTOR monitor APIs. This is an Appendix B development-source
qualification; it does not change deployment policy or certify all endpoints.

| Source unit | Shared assertions and complementary controls |
|---|---|
| B-048/B-049 | MC-001 resolves a registered local name to its actual pid, requires exactly one monitor result, compares fresh references before/after discharge without interpreting their representation, and consumes exact notifications once. MC-002 demonstrates that a down-shaped application message is correlation data, not sender authentication, and does not discharge the runtime's observation. MC-005/027–029 check required targets and atom-valued node components. BN-015 checks actual remote socket loss, `connection_closed`, late-frame rejection and absence of automatic restoration. |
| B-050 | LM-002/006 and MC-004 prove spawn/explicit/foreign-owner independence. MC-019–021 cover toplevel call/next, success, timeout, callback failure/exception, target death and cleanup. MC-022–024 cover synchronous and monitored asynchronous server waits with the same outcomes, plus output mismatch. MC-025 covers supervisor control, independent child observations, termination/deletion and halt. Each new wait case consumes the public references and rejects unexpected private notifications. Full implementation suites additionally check private tables, send/setup exceptions, interruptions, supervisor timeout/halt ordering and server upgrade. |
| B-051 | LM-001 requires immediate success, failure, exception and explicit-exit reasons from spawn-time monitors. LM-003 and MC-001 require a fresh explicit monitor after observed termination to deliver `no_process`, rather than replay the old reason. |
| B-052 | MC-003 collects all solutions from both demonitor arities, including unknown/already removed references and duplicate `flush`; each returns exactly once. |
| B-053 | MC-003/004 cover idempotence and ownership; MC-006–018/026/030/031 cover required references, proper lists, uninstantiated lists/elements/tails, wrong arity, unknown options, every later duplicate and complete formal-error culprits. Invalid option lists must leave both a real live observation and queued notification intact. |
| B-054/B-055 | LM-006 and the earlier BN-014–016/native barrier selection are retained regression controls for flush, confirmed withdrawal, timeout/retry and declared loss. |

Expected receives have explicit failing/throwing timeout callbacks. The language
allows `receive/2` to succeed on timeout by default; a successful query alone
therefore cannot establish that its expected message arrived. This selection
strengthens the links/server-wait expected receives and reuses the toplevel-wait
manifest. Expected deadline deliveries and server replies also have explicit
failing timeout callbacks.
Intentional timeout scenarios retain their original semantics.

Error assertions require an actual exception and compare its formal term by
variant, because throwing copies variables. They separately check that input
variables remain unbound and that option sharing/structure is preserved. The
portable contract excludes diagnostic `Context` text. URI tests use the supplied
node term as written in each host's text mode; no conversion to an accepted atom
is performed by the monitor call.

A retired pid and its recorded spawn completion are distinct cases. The browser
may retain completion information to honor spawn-time monitoring when its
installation follows a fast child exit. A new explicit reference must observe
`no_process`. Tests use no pid-width, numeric-reference or engine-format rules.

Run the complete maintained gate from this repository:

```sh
NODE_PATH=/path/to/playwright/node_modules python3 runner/monitor_release.py \
  --swipl /path/to/swipl --tpl /path/to/tpl \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --runtime-root /path/to/packaged-browser-runtime --node /path/to/node \
  --output /fresh/report
```

The gate requires 196 shared observations, 64 real browser/native transport
observations and both native monitor barrier groups. It rejects missing,
duplicate, unexpected and nonpassing rows, and invalidates a run if source or
driver fingerprints change. Run each runtime's full suite as well when repairing
implementation behavior. Supporting suite passes still require clause review
before changing the source-unit ledger.
