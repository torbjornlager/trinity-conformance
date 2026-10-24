# Trinity conformance tests

This repository is the future implementation-neutral conformance suite for
Web Prolog nodes. Its purpose is to test observable behaviour, independently
of whether a candidate node is implemented in SWI-Prolog, Trealla Prolog, or
another runtime.

## Scoped interoperability baseline

[Baseline 0.1](baselines/0.1.md) consolidates the existing nodes' selected
observable contracts. The [coverage matrix](reports/2026-10-21-baseline-0.1/COVERAGE.md)
includes GNU Prolog at ISOBASE level, native SWI/Trealla and local language
assertions in both SWI-WASM modes. Required failures, exploratory differences,
experimental text and unmeasured surfaces have separate accounting.
The [HTTP source-loading follow-up](reports/2026-10-21-http-source-loading/COVERAGE.md)
records the subsequent Trealla repair; the initial matrix remains historical evidence.
The [HTTP client-context follow-up](reports/2026-10-21-http-client-context/COVERAGE.md)
records the subsequent client availability repair, with the remaining failure explicit.
The [GNU framing follow-up](reports/2026-10-21-gnu-request-framing/COVERAGE.md)
records 94/94 required selections passing, with separate supporting failures retained.
The [native conformance checkpoint](reports/2026-10-21-native-checkpoint/COVERAGE.md)
reruns the committed SWI/Trealla implementations: 60/60 required selections and
66/66 supporting ACTOR assertions pass with explicit fixture peer authentication.
The native interoperability runner completes 69 invocation groups; parser,
admission, HTTP-framing and experimental-text observations remain separate.
GNU and browser engines were not rerun in that checkpoint.
See [reproduction](docs/BASELINE_RUNNER.md) and the
[difference register](docs/BASELINE_DIFFERENCES.md). This is a scoped draft,
not complete language, security or lifecycle certification.

## Status

The executable draft profiles are
[`actor-core-0.1`](profiles/actor-core-0.1.md),
[`actor-behaviours-0.1`](profiles/actor-behaviours-0.1.md),
[`actor-supervisors-0.1`](profiles/actor-supervisors-0.1.md),
[`portable-text-0.1`](profiles/portable-text-0.1.md), and
[`actor-workers-0.1`](profiles/actor-workers-0.1.md). The dependency-free
black-box runner contains cases exercised against both the SWI and Trealla
nodes. These remain drafts: passing one means only that a candidate passes its
explicitly listed cases.

## Profiles

The reference implementation currently recognizes these cumulative public
node profiles:

| Profile | Required public surface |
|---|---|
| `relation` | Restricted relational queries through `/call` |
| `isobase` | Stateless queries through `/call` |
| `isotope` | ISOBASE plus stateful `/toplevel_*` sessions |
| `actor` | ISOTOPE plus the Web Prolog WebSocket actor protocol |

`workbench` is also recognized by the reference implementation, but is an
unrestricted development mode rather than an initial portability target.

## Intended structure

- `cases/` — implementation-neutral case definitions and expected outcomes
- `adapters/` — thin process-launch and local-API adapters
- `docs/` — profile, provenance, and source-test inventories
- `reports/` — dated baseline and candidate-node reports
- `profiles/` — versioned observable contracts
- `runner/` — candidate-neutral external-node runner
- `schemas/` — machine-readable report formats

Implementation-specific unit tests remain in their implementation
repositories. In particular, SWI PlUnit internals and Trealla regression tests
do not belong here unless they are recast as an observable contract.

## Result vocabulary

An eventual runner should distinguish:

- `pass` — the advertised contract was observed
- `fail` — the candidate advertised the profile but violated the contract
- `unsupported` — the candidate does not advertise the required profile
- `not_applicable` — the case does not apply to this candidate configuration

Untested behaviour must never be counted as passing, and an unsupported
higher profile must not make a lower-profile implementation appear broken.

## Running ACTOR Core 0.1

The runner uses only the Python 3 standard library and connects to an already
running node. It never imports implementation code.

```sh
python3 runner/run.py \
  --ws-url ws://127.0.0.1:3060/ws \
  --advertised-profile actor \
  --candidate trealla-local \
  --report reports/trealla-local.json
```

For a private node, keep the secret out of the command line:

```sh
export TRINITY_TEST_TOKEN='...'
python3 runner/run.py \
  --ws-url wss://node.example/ws \
  --token-env TRINITY_TEST_TOKEN \
  --candidate node-name
```

Use `--case AC-004` to select one case. Failure classifications can be added
with `--classifications path/to/classifications.json`; see
[`docs/FAILURE_CLASSIFICATION.md`](docs/FAILURE_CLASSIFICATION.md).

To test the opt-in portable-text draft without changing the node:

```sh
python3 runner/run.py \
  --manifest cases/portable-text-0.1.json \
  --ws-url ws://127.0.0.1:3060/ws \
  --advertised-profile actor \
  --candidate candidate-name
```

The `actor` argument in this invocation describes the transport surface used
by the current runner. It does not claim that portable-text semantics are part
of the deployed ACTOR profile.

The cross-runtime implications for SICStus, Ciao, XSB, and the systems already
considered are recorded in
[`docs/PORTABLE_TEXT_PORTABILITY.md`](docs/PORTABLE_TEXT_PORTABILITY.md).

To test the shared generic-server and supervisor behaviour contract:

```sh
python3 runner/run.py \
  --manifest cases/actor-behaviours-0.1.json \
  --ws-url ws://127.0.0.1:3060/ws \
  --advertised-profile actor \
  --candidate candidate-name
```

To test worker bindings, policies, determinism, supplied source and completed-call
cleanup through public interfaces:

```sh
python3 runner/run.py \
  --manifest cases/actor-workers-0.1.json \
  --ws-url ws://127.0.0.1:3060/ws \
  --candidate candidate-name --report reports/worker-result.json
```

The separate `cases/worker-diagnostics-0.1.json` manifest probes an unresolved
worker-cleanup ownership race. Diagnostic results do not count toward the worker
profile; a passing stress run does not establish that the race is fixed.

The demonstrator-specific tutorial regressions are deliberately separate
from the ACTOR profile because they may call named nodes in the deployed
Trinity topology. For example, tutorial 19 loads source through a browser
WebSocket session on the candidate and resolves promises through N3 and N4:

```sh
python3 runner/run.py \
  --manifest cases/demonstrator-tutorials-0.1.json \
  --ws-url ws://127.0.0.1:13060/ws \
  --advertised-profile actor \
  --candidate trealla-n5
```

Private deployments reached through a trusted local proxy can add its
verified identity header with `--header 'X-Web-Prolog-User: owner@example.test'`.

## Provenance and license

The initial inventory was derived from `trinity-demonstrator` and
`trealla-port`. See [NOTICE.md](NOTICE.md). This repository is distributed
under the [MIT License](LICENSE).

## Supervisor cleanup conformance and diagnostics

Run the identical public-interface cleanup cases against each isolated native
node using `--manifest cases/actor-supervisors-0.1.json`. They exercise startup
rollback, dynamic-addition and explicit-respawn retry, restart-budget exhaustion
under all three strategies, shutdown policies and monitor/message preservation. See the [profile](profiles/actor-supervisors-0.1.md) for coverage
limits; runtime regression tests still cover never-published provisional pids.

Run `--manifest cases/supervisor-diagnostics-0.1.json` separately. The runtime-bound
nested-specification admission difference remains unresolved. The historical
repeated-cleanup and replacement-name-conflict cases now pass with native SWI's
zero-time polling repair; they retain their diagnostic identifiers and remain
outside the shared profile's pass count. See the
[repair results](reports/2026-10-20-zero-poll-repair.md).

## Promise/yield draft conformance

The separate [Promise/yield 0.1 pack](profiles/promise-yield-0.1.md) adds six public
ACTOR-caller/HTTP-peer assertions without changing baseline 0.1. It covers local
wait timeout/retry, callbacks, once, failure/error answers, reference collection
and option-validation preservation. Existing HC-002 supplies sharing coverage.

The [24 October matrix](reports/2026-10-24-promise-yield/COVERAGE.md) records
22/24 new selections passing and 8/8 existing HTTP selections passing. Trealla's
actor-send timeout callback fails against both peers; successful diagnostic
controls remain separate and do not waive these required draft-pack failures.
GNU and SWI-WASM network execution are unmeasured in this batch.

```sh
python3 adapters/local_promises.py \
  --swipl /path/to/verified/swipl --tpl /path/to/separate/trealla/tpl \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --demonstrator-root /path/to/trinity-demonstrator \
  --output /fresh/path/promise-results
python3 adapters/local_promises.py --diagnostics-only \
  --swipl /path/to/verified/swipl --tpl /path/to/separate/trealla/tpl \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --demonstrator-root /path/to/trinity-demonstrator \
  --output /fresh/path/promise-results/diagnostics
python3 runner/validate_reports.py /fresh/path/promise-results
python3 runner/validate_reports.py /fresh/path/promise-results/diagnostics
python3 runner/promise_coverage.py /fresh/path/promise-results
```

The adapter checks the demonstrator's native dependency pin, uses matching
Trealla libraries and disposable loopback ACTOR nodes, and stops its fixtures.
It does not install engines or use n3/n5. Add `--diagnostics-only` with a different
fresh output directory for the separate controls. If used outside the recorded
nested report layout, link those diagnostics separately in the resulting report.
The coverage renderer expects the main report directory to contain a
`diagnostics/` result directory as in the published run.

The [callback-context repair follow-up](reports/2026-10-24-promise-callback-context/COVERAGE.md)
passes all 24 unchanged PY and eight HC selections on disposable native fixtures.
The earlier failing matrix remains historical evidence. The broader runtime
sandbox fixture's intermittent cascade timeout is recorded separately, not as a
promise-pack failure or a resolved lifecycle issue.

## Links and monitors draft conformance

The separate [Links and monitors 0.1 pack](profiles/links-monitors-0.1.md) covers
local monitoring, exact exit reasons, independent references, one-way links,
a readiness-synchronized cascade and scoped demonitor/flush behaviour. It uses
identical public goals with no fixed sleeps or private runtime imports.
The [24 October coverage matrix](reports/2026-10-24-links-monitors/COVERAGE.md)
records **12/12 selections passing** on disposable SWI/Trealla ACTOR nodes.
Remote monitoring and GNU/browser execution are not measured by this batch.

The existing disposable fixture adapter also accepts a local ACTOR manifest:

```sh
python3 adapters/local_promises.py \
  --local-manifest cases/links-monitors-0.1.json \
  --swipl /path/to/verified/swipl --tpl /path/to/separate/trealla/tpl \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --demonstrator-root /path/to/trinity-demonstrator \
  --output /fresh/path/links-results
python3 runner/validate_reports.py /fresh/path/links-results
python3 runner/links_coverage.py /fresh/path/links-results
```

The local-manifest mode runs once per candidate without an outbound peer. The
promise mode and its existing manifests remain available. Pin validation,
matching libraries, bounded subprocesses and preservation checks are shared;
no installed engine or live n3/n5 process is used as a fixture.

## Generic-server wait draft conformance

The [Generic-server waits 0.1 pack](profiles/server-waits-0.1.md) selects public
reply correlation, mismatch consumption, timeout/retry, callback outcomes,
server-down reporting and scoped wait cleanup. Identical goals and callback
source execute on disposable native ACTOR nodes using acceptance/release
handshakes instead of sleeps. It does not amend baseline 0.1.

The [24 October matrix](reports/2026-10-24-server-waits/COVERAGE.md) records
**12/12 selections passing**. Remote servers, browser execution and unknown
reference policy remain outside this batch; no runtime repair was made.

```sh
python3 adapters/local_promises.py \
  --local-manifest cases/server-waits-0.1.json \
  --swipl /path/to/verified/swipl --tpl /path/to/separate/trealla/tpl \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --demonstrator-root /path/to/trinity-demonstrator \
  --output /fresh/path/server-waits-results
python3 runner/validate_reports.py /fresh/path/server-waits-results
python3 runner/links_coverage.py --suite server-waits /fresh/path/server-waits-results
```

The existing matrix renderer's default remains the links-and-monitors pack;
`--suite server-waits` selects the new report filenames and scope text. Both
rendering paths preserve required failures and missing-case observations.

## Selective-receive draft conformance

The separate [Selective receive 0.1 pack](profiles/selective-receive-0.1.md)
selects one-sided matching and variable sharing, deferred order, failed/throwing
guards, first-solution guard bindings, body consumption and cut scope. Identical
public goals run on disposable native ACTOR nodes without sleeps, private mailbox
inspection or runtime imports. Existing baseline/profile definitions are unchanged.

The [24 October matrix](reports/2026-10-24-selective-receive/COVERAGE.md) records
**12/12 selections passing**. Interruption/handoff stress, remote delivery and
browser execution remain unmeasured; no runtime repair was made.

```sh
python3 adapters/local_promises.py \
  --local-manifest cases/selective-receive-0.1.json \
  --swipl /path/to/verified/swipl --tpl /path/to/separate/trealla/tpl \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --demonstrator-root /path/to/trinity-demonstrator \
  --output /fresh/path/receive-results
python3 runner/validate_reports.py /fresh/path/receive-results
python3 runner/links_coverage.py --suite selective-receive /fresh/path/receive-results
```

The shared local-pack fixture adapter and coverage renderer retain their prior
defaults. The selective-receive renderer preserves required failures/missing
observations; existing report files are not regenerated by this extension.

## Synchronous toplevel wait draft conformance

The separate [Toplevel waits 0.1 pack](profiles/toplevel-waits-0.1.md) selects
caller targeting, timeout outcomes/callbacks, stale call/next correlation, output
mismatch, termination and preservation of asynchronous replies and public monitors.
Identical public-interface assertions execute on disposable native ACTOR nodes.
The [24 October matrix](reports/2026-10-24-toplevel-waits/COVERAGE.md) records
**12/12 selections passing**. Initial test-construction errors and their raw
reports are retained separately and do not count as coverage. Runtime code,
installed runtimes and n3/n5 remain unchanged.

```sh
python3 adapters/local_promises.py \
  --local-manifest cases/toplevel-waits-0.1.json \
  --swipl /path/to/verified/swipl --tpl /path/to/separate/trealla/tpl \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --demonstrator-root /path/to/trinity-demonstrator \
  --output /fresh/path/toplevel-waits-results
python3 runner/validate_reports.py /fresh/path/toplevel-waits-results
python3 runner/links_coverage.py --suite toplevel-waits /fresh/path/toplevel-waits-results
```

Existing runner/renderer defaults and historical baseline reports are unchanged.
Remote transport, browsers, terminal I/O, concurrent clients and deadline accuracy
under traffic are outside this finite contract selection.

## Local naming and registration draft conformance

The separate [Local naming 0.1 pack](profiles/local-naming-0.1.md) checks ordinary
registration/routing, conflicts, idempotent removal, termination cleanup, stale
local pids and named supervisor startup failure/retry. Identical public-interface
goals execute on disposable native ACTOR nodes. The
[24 October matrix](reports/2026-10-24-local-naming/COVERAGE.md) records **12/12
selections passing**. Initial setup errors and the incidental sandbox/count-format
differences are retained separately. Runtime code, installed runtimes and n3/n5
remain unchanged.

```sh
python3 adapters/local_promises.py \
  --local-manifest cases/local-naming-0.1.json \
  --swipl /path/to/verified/swipl --tpl /path/to/separate/trealla/tpl \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --demonstrator-root /path/to/trinity-demonstrator \
  --output /fresh/path/local-naming-results
python3 runner/validate_reports.py /fresh/path/local-naming-results
python3 runner/links_coverage.py --suite local-naming /fresh/path/local-naming-results
```

SWI's client namespaces and Trealla's node-wide ordinary names remain explicit.
Cross-client isolation, remote aliases, concurrent races, service names and
namespace teardown are outside this finite selection. Existing runner defaults
and historical reports are unchanged.

## Actor copying and private-source isolation draft conformance

The separate [Copying and isolation 0.1 pack](profiles/copying-isolation-0.1.md)
selects child pid substitution, independent parent/child bindings, preserved
sharing, src_text/src_list loading and sibling/parent database isolation.
Identical public-interface assertions execute on disposable native ACTOR nodes.
The [24 October matrix](reports/2026-10-24-copying-isolation/COVERAGE.md) records
**12/12 selections passing** on the first run. Runtime code, installed runtimes
and n3/n5 remain unchanged.

```sh
python3 adapters/local_promises.py \
  --local-manifest cases/copying-isolation-0.1.json \
  --swipl /path/to/verified/swipl --tpl /path/to/separate/trealla/tpl \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --demonstrator-root /path/to/trinity-demonstrator \
  --output /fresh/path/copying-isolation-results
python3 runner/validate_reports.py /fresh/path/copying-isolation-results
python3 runner/links_coverage.py --suite copying-isolation /fresh/path/copying-isolation-results
```

Minimal dynamic declarations support the selected private-database mutation;
general directives, URI loading, source inheritance, module qualification,
remote spawning and exhaustive sandbox-policy checks remain outside this pack.
Historical matrices and existing runner defaults remain unchanged.

## Local creation-option validation draft conformance

The separate [Creation validation 0.1 pack](profiles/creation-validation-0.1.md)
checks unknown options, list structure, invalid values, later duplicates, wrapper
boundaries, first-setting precedence and validation before source loading/startup.
Identical public-interface goals run on disposable native ACTOR nodes. The
[24 October matrix](reports/2026-10-24-creation-validation/COVERAGE.md) records
**12/12 runtime-supplied-option selections passing**. The initial literal-option
run's five admission-path failures remain separate unresolved diagnostics; they
are not covered by the final green matrix. Runtime code, installed runtimes and
n3/n5 remain unchanged.

```sh
python3 adapters/local_promises.py \
  --local-manifest cases/creation-validation-0.1.json \
  --swipl /path/to/verified/swipl --tpl /path/to/separate/trealla/tpl \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --demonstrator-root /path/to/trinity-demonstrator \
  --output /fresh/path/creation-validation-results
python3 runner/validate_reports.py /fresh/path/creation-validation-results
python3 runner/links_coverage.py --suite creation-validation /fresh/path/creation-validation-results
```

Lists are delivered through ordinary messages to test runtime validation after
query admission. Child specifications, statecharts, HTTP options, remote creation
and concurrent startup races are outside this pack. Historical reports and
existing runner defaults are unchanged.
