# Native Boolean option contract

Appendix B requires atom type and Boolean domain for language options `link`,
`monitor`, `session`, `trace` and `once`. Every occurrence is validated before
side effects; the first scalar setting wins. In particular, repeated valid
`trace/1` options are permitted and the first setting determines trace output.

`cases/boolean-options-0.1.json` contains 234 negative cases across raw creation,
server/supervisor/toplevel/chart wrappers, RPC/promise, asynchronous toplevel calls,
and local/remote synchronous calls. It covers integers, floats, strings, character
lists, empty lists, compounds, invalid atoms, variables and later duplicates.
Public query rejections require the exact formal error, including its culprit,
and a successful follow-up query on the same shell. This permits validation at
sandbox admission or runtime without treating either as an unrelated error.

Run the selection against both candidates in each sandbox mode:

```sh
python3 adapters/local_runtime_contracts.py \
  --manifest cases/boolean-options-0.1.json \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --tpl /path/to/tpl --mode blacklist --output /path/to/results
```

Repeat with `whitelist` and `off`. The disposable SWI fixture sizes its command
budget to the number of cases so rejection/recovery traffic does not exhaust the
production default. This changes only the fixture's startup options.

Two existing boundary limitations are explicitly separate from language results:
SWI whitelist analysis cannot derive the selected server-creation callback;
Trealla's owner-off submitted query path lacks the statechart alias. Corresponding
mode entries are deferred for both candidates to retain an identical selection.
They are not counted as language passes. The separate
`cases/boolean-boundary-diagnostics-0.1.json` records exact host-specific admission
and availability outcomes, plus recovery, for an opaque session setting under
whitelist and a chart call under owner-off. It does not waive the language errors
or weaken sandbox policy.

Run the complete native selection, including those deferred public cases:

```sh
python3 adapters/native_boolean_options.py \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --tpl /path/to/tpl --output /path/to/native-results
```

The adapter uses the same cases in fresh trusted processes with the public APIs
imported explicitly. Each negative call catches the exact error, preserves option
and output variables, compares actor/link/monitor/promise/queue inventories, and
preserves an unrelated mailbox message. Creation and RPC/promise options include
a loopback source URI before the invalid scalar: both source and dispatch request
counts must remain zero. Goals and callbacks must not execute.

Positive controls observe both orderings of actual link/monitor settings, trace
output from real valid charts, and synchronous `once/1` continuation flags. The
resource fixture is never installed in public nodes or submitted as user source.
The runtime validators remain private, rather than being copied into user clauses.
Trealla needs an explicit atom test because its `must_be(atom,...)` accepts strings
and its atom classification includes the empty list; this adaptation remains in
its runtime. No engine difference justifies different public errors.

Keep HTTP/JSON text-Boolean decoding, redirect/TLS options, URI/source semantics,
prompt protocols and timeout rewrites outside this selection. Existing native
transport-decoder tests and full interop remain required qualification controls.
