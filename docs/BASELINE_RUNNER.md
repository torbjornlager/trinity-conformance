# Running the scoped baseline

The runners connect only to explicitly configured candidates. The local matrix
adapter starts disposable loopback nodes and grants GNU outbound access only
to their exact origins/IPs. It does not replace installed engines, restart N3/N5,
modify owner policy files, or repair runtime code. Use trusted local fixtures;
`auth(open)` is not a recommended public deployment configuration.

## One pack / external nodes

```sh
python3 runner/baseline.py --manifest cases/isobase-http-0.1.json \
  --url http://127.0.0.1:8081 --candidate gnu --profile isobase \
  --report reports/gnu-http.json

python3 runner/baseline.py --manifest cases/interop-actor-0.1.json \
  --url ws://127.0.0.1:3053/ws --peer http://127.0.0.1:3060 \
  --candidate swi --profile actor --report reports/swi-to-trealla.json
```

Other manifests have the same flags. `interop-http` requires an HTTP candidate
URL and a peer URL. `language-actor` and `wire-capabilities` require WebSocket
URLs. Node base-path and credential-policy edge cases are outside this scoped
local matrix. `--token-env NAME` reads an existing bearer token without placing
it in command arguments; do not put secrets in saved URLs or reports.

## Browser engines

```sh
node adapters/wasm.cjs /path/to/trinity-demonstrator worker \
  cases/language-actor-0.1.json reports/wasm-worker.json
node adapters/wasm.cjs /path/to/trinity-demonstrator main \
  cases/language-actor-0.1.json reports/wasm-main.json
```

The adapter imports only test harness setup from the runtime repository. The
manifest owns the goals; all four ACTOR engine configurations execute the same
assertions. A test coordinator emulates browser actor plumbing around the real
SWI-WASM engine. This is not UI or real-browser network testing. Native engines
are exercised through their public server/sandbox paths; the Node adapter does
not establish browser sandbox-admission parity.

## Reproduce the complete recorded matrix

Build GNU's ordinary `isobase-node`, `query-supervisor`, and `query-worker` first
using its existing build instructions. Use a Trealla binary with the matching
adjacent `library/` directory. The matrix records hashes instead of claiming
that a binary necessarily matches an arbitrary working-tree source snapshot.

```sh
python3 adapters/local_baseline.py \
  --swipl /path/to/swipl --tpl /path/to/tpl --node /path/to/node \
  --swi-root /path/to/trinity-demonstrator \
  --trealla-root /path/to/trealla-port --gnu-root /path/to/gprolog-port \
  --output /path/to/trinity-conformance/reports/my-baseline-run
python3 runner/coverage.py reports/my-baseline-run
python3 runner/validate_reports.py reports/my-baseline-run
```

Existing ACTOR packs run with `runner/run.py` and schema 1. New packs and browser
reports use schema 2. The generated matrix labels required packs, supporting
contracts and exploratory/experimental diagnostics separately. Existing
Portable Text assertions are not promoted into baseline requirements.

The launcher completes the matrix even when cases fail, recording subprocess
exit status and missing reports. It returns nonzero for required/supporting
failures or missing evidence; semantic differences in diagnostic-only suites
are recorded without becoming required failures. A diagnostic transport error
is explicitly incomplete evidence. The matrix is the verdict; inspect it rather
than treating successful process startup as conformance.

The selected calls do not exhaust GNU's contract 0.2.0, hostile-input security,
resource bounds, general lifecycle cleanup, remote cancellation, source fetching,
all text/numeric modes, browser transport or RELATION/complete ISOTOPE sessions.

## Result interpretation

- `pass`: the required assertion was observed.
- `fail`: a selected required assertion failed; it remains a failure when its
  cause is also discussed in the difference register.
- `unsupported`: the explicitly declared candidate profile is lower than the
  requirement; not a way to excuse an advertised required operation.
- `observed`: diagnostic response retained without a normative pass claim.
- `diagnostic_error`: no diagnostic response was obtained (for example timeout).
- Matrix `not applicable` and `not measured` cells are explicit scope decisions,
  not pass counts.

New tests use finite fixtures and compare formal outcomes, aliases and binding
identity. They do not equate every exception with success, normalize all errors
to a string, or wrap nondeterministic assertions in `once/1`.
