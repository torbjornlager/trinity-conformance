# Trinity conformance tests

This repository is the future implementation-neutral conformance suite for
Web Prolog nodes. Its purpose is to test observable behaviour, independently
of whether a candidate node is implemented in SWI-Prolog, Trealla Prolog, or
another runtime.

## Current consolidated results

The [current coverage matrix](CURRENT_COVERAGE.md) brings together the latest
committed results for each shared pack, including GNU ISOBASE and both WASM
language modes. It records tested revisions/dates, unresolved diagnostics and
unmeasured surfaces. This is an evidence roll-up, not a fresh combined runtime
run. The dated sections below retain the historical sequence of repairs.

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

## Supervisor child-specification validation draft conformance

The separate [Child specifications 0.1 pack](profiles/child-specs-0.1.md) selects
missing starts, duplicate ids, malformed lists, invalid later duplicate options,
nested early rejection and dynamic rejection/retry with sibling preservation.
Identical public-interface goals run on disposable SWI and Trealla ACTOR nodes.
The [24 October matrix](reports/2026-10-24-child-specs/COVERAGE.md) records **6/12
passes: SWI 1/6, Trealla 5/6**. Required failures remain visible: SWI blocks
runtime-bound initial lists during admission; Trealla misses the dynamic case's
input message, with source inspection pointing to admission-time variable binding.
Initial and diagnostic runs are retained separately. Runtime code, installed
runtimes and n3/n5 remain unchanged.

```sh
python3 adapters/local_promises.py \
  --local-manifest cases/child-specs-0.1.json \
  --swipl /path/to/verified/swipl --tpl /path/to/separate/trealla/tpl \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --demonstrator-root /path/to/trinity-demonstrator \
  --output /fresh/path/child-spec-results
python3 runner/validate_reports.py /fresh/path/child-spec-results
python3 runner/links_coverage.py --suite child-specs /fresh/path/child-spec-results
```

Select `cases/child-spec-diagnostics-0.1.json` with a fresh output directory to run
the separate probes. Their admission errors/output-probe timeout are not required
coverage passes. Remote supervision, concurrency, exhaustive child options,
restart policies and shutdown timing remain outside this pack. Historical
matrices and runner defaults are unchanged.

## Admission-path diagnostic comparisons

The separate [Admission paths scope](profiles/admission-paths-0.1.md) compares
literal and runtime-supplied supervisor specifications and creation options.
The [diagnostic matrix](reports/2026-10-24-admission-paths/DIAGNOSTICS.md) records
**20 completed observations, no diagnostic errors**, not conformance passes.
Four separate entry-marker controls also complete. Existing required failures
and coverage matrices remain unchanged.

The results locate SWI's rejection of opaque initial child lists before execution,
Trealla's admission-time binding of a dynamic child receive variable, and SWI's
literal-source preparation before an unknown-option error. Exact command/response
objects and qualifications are retained in the reports. Runtime code, installed
runtimes and n3/n5 remain unchanged.

```sh
python3 adapters/local_promises.py \
  --local-manifest cases/admission-paths-0.1.json \
  --swipl /path/to/verified/swipl --tpl /path/to/separate/trealla/tpl \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --demonstrator-root /path/to/trinity-demonstrator \
  --output /fresh/path/admission-results
python3 runner/validate_reports.py /fresh/path/admission-results
python3 runner/admission_coverage.py /fresh/path/admission-results
```

Select `cases/admission-marker-controls-0.1.json` with another fresh output path
to reproduce the ordinary exception/failure controls. The capture transport is
restricted to diagnostic scope; observation of an error is never a required pass.
No output markers or sleeps are used. Remote, browser/GNU, whitelist-policy and
concurrency behavior are unmeasured; no runtime repair or engine report is implied.

## Trealla nonbinding admission repair checkpoint

The Trealla adapter repair was checked with the unchanged shared manifests on
new disposable nodes. [Child-specification coverage](reports/2026-10-24-trealla-nonbinding-child-specs/COVERAGE.md)
is now **7/12: Trealla 6/6 and SWI 1/6**. SWI's five required admission failures
remain visible. [Admission diagnostics](reports/2026-10-24-trealla-nonbinding-admission-probes/DIAGNOSTICS.md)
record Trealla's runtime child variable staying unbound and both messages matching;
all 20 observations complete. [Creation validation](reports/2026-10-24-trealla-nonbinding-creation-validation/COVERAGE.md)
remains **12/12**. Historical matrices and all manifests are unchanged.

Use the existing local adapter/reproduction commands with the patched Trealla
checkout, exact pinned SWI source, separate verified engines and fresh output
paths. Reports identify the uncommitted patch through source hashes as well as
its base commit. This is a source repair checkpoint, not an installed-runtime
upgrade; installed executables and n3/n5 remain unchanged. Broader lifecycle,
SWI admission/source-order findings and unrelated diagnostics remain separate.

## SWI runtime-bound supervisor admission checkpoint

The native SWI working-tree repair closes its runtime-bound initial child-list
barrier on the unchanged shared pack:
[child specifications](reports/2026-10-24-swi-runtime-specs-child-specs/COVERAGE.md)
now pass **12/12**, and [creation validation](reports/2026-10-24-swi-runtime-specs-creation-validation/COVERAGE.md)
remains **12/12**. [Admission diagnostics](reports/2026-10-24-swi-runtime-specs-admission-probes/DIAGNOSTICS.md)
record all 20 observations complete, including SWI's runtime list executing and
its missing-start error becoming catchable. Historical matrices remain unchanged.

The fixture adapter's default still requires the clean exact dependency pin.
`--swi-source-candidate` explicitly permits a working-tree patch over that same
pinned base, records source/pin hashes and verifies the pin remains unchanged.
It does not modify or invoke a production launcher. Example:

```sh
python3 adapters/local_promises.py --swi-source-candidate \
  --local-manifest cases/child-specs-0.1.json \
  --swipl /path/to/verified/swipl --tpl /path/to/separate/trealla/tpl \
  --swi-root /path/to/pinned-base-native-working-tree \
  --trealla-root /path/to/trealla-port \
  --demonstrator-root /path/to/trinity-demonstrator \
  --output /fresh/path/swi-candidate-results
```

The native verification report retains one unresolved full behaviour-tier cleanup
failure and a pre-existing whitelist framework-startup restriction. SWI's literal
URI ordering finding also remains separate. These green ACTOR/blacklist cells do
not erase those limits. The dependency pin, installed runtimes and n3/n5 are
unchanged; promotion/deployment is a separate step.

## SWI spawn source-validation checkpoint

The plain SWI `spawn/3` candidate now rejects ground invalid options before URI
preparation. The [admission matrix](reports/2026-10-24-swi-spawn-source-admission-probes/DIAGNOSTICS.md)
records **20 completed diagnostic observations**: AP-009 gives a spawn-option
error before entry rather than a source socket error. It remains an admission
error; AP-010 retains catchable runtime validation. Separate
[creation validation](reports/2026-10-24-swi-spawn-source-creation-validation/COVERAGE.md)
and [child specifications](reports/2026-10-24-swi-spawn-source-child-specs/COVERAGE.md)
each pass **12/12**. Historical matrices and manifests remain unchanged.

To evaluate a later committed native base without updating the demonstrator pin,
explicit candidate mode now accepts `--swi-candidate-revision FULL_COMMIT_SHA`.
The checkout must have exactly that HEAD, and it must descend from the unchanged
pin. A full immutable 40-character SHA is required. Omitting this option keeps
the previous pinned-base candidate rule; omitting candidate mode keeps the strict
clean-pin checker. Working-tree hashes, selected base, unchanged pin and fixture
preservation checks are recorded. This is test-only selection, not a pin update.

## Boolean option compatibility checkpoint

The [Boolean candidate follow-up](reports/2026-10-24-boolean-toplevel-waits/COVERAGE.md)
retains 12/12 unchanged toplevel-wait assertions on disposable SWI/Trealla nodes.
Its [report](reports/2026-10-24-boolean-toplevel-waits/REPORT.md) links the separate
native, browser and GNU Boolean regressions and keeps the intermittent native
ownership finding separate. The [current matrix](CURRENT_COVERAGE.md) records
the candidate scope; the dependency pin and installed/live runtimes are unchanged.

The [Boolean-only close-out](reports/2026-10-25-boolean-closeout/REPORT.md)
reruns the focused native/browser/GNU checks and the same 12 shared assertions
over the current source bases, preserving the separate URI work.

## URI representation compatibility checkpoint

The [URI candidate matrix](reports/2026-10-24-uri-promise-http/COVERAGE.md) retains
24/24 promise/yield and 8/8 HTTP interoperability selections across native SWI
and Trealla. Those historical candidates also include the then-pending Boolean repair. Separate
implementation regressions exercise canonical atom output, supported text forms,
checked Host:Port shorthand, early errors, no-fetch guarantees and sharing.
The [report](reports/2026-10-24-uri-promise-http/REPORT.md) records scope and
preservation. GNU shared baseline and browser real-network coverage are not
inferred from those implementation tests. Historical reports remain unchanged.

The [URI close-out](reports/2026-10-25-uri-closeout/REPORT.md) repeats the focused
checks and 24+8 shared assertions over separately committed Boolean sources,
reconciles Appendix B and the web manual, and preserves deployed runtimes.

## Portable-text experimental expansion

[Draft 0.2](profiles/portable-text-0.2.md) defines characters as Unicode scalar
values, preserves normalization distinctions, and clarifies that `src_list/1`
preserves constructed terms rather than rereading or converting their data.
Its [26 cases](cases/portable-text-0.2.json) extend 0.1 to option/input readers,
private/copied/DCG/URI source, Unicode round trips and HTTP peer assertions.
The draft remains opt-in; it adds no requirement to existing node profiles.
Version 0.1 and all historical reports are retained.

Run against explicitly selected test fixtures, with unchanged reader defaults:

```sh
python3 runner/run.py --manifest cases/portable-text-0.2.json \
  --candidate candidate --ws-url ws://127.0.0.1:PORT/ws \
  --advertised-profile actor --peer http://127.0.0.1:PEER_PORT \
  --source-base http://127.0.0.1:SOURCE_PORT --report /fresh/path/text.json
```

The source server must serve `fixtures/portable-text/portable-text.pl` at
`SOURCE_BASE/portable-text.pl`, and its origin/address must be allowed by the
disposable nodes' source policy. These permissions are fixture configuration,
not production changes. `adapters/local_portable_text.py` automates disposable
native fixtures from each source repository's committed HEAD using the same
`--swipl`, `--tpl`, `--swi-root`, `--trealla-root`, `--demonstrator-root` and
`--output` arguments as the promise adapter. It excludes pending runtime edits,
records exact archived sources and preservation checks, and stops its fixtures.
It changes no reader flags. Use `--case TXT-001` (repeatable) with `runner/run.py`
for a local selection that does not need URI or peer fixtures.

Runner regressions run with `python3 -m unittest discover -s runner -p 'test_*.py'`.
Native observations and remaining untested surfaces are recorded in the
[0.2 coverage matrix](reports/2026-10-25-portable-text-0.2/COVERAGE.md).

## Isolated SWI portable-text candidate

The [configured experiment](reports/2026-10-25-swi-portable-text-final-r2/COVERAGE.md)
passes all 26 text cases in each direction with the separate Trealla Unicode
candidate, plus 90 shared actor/interoperability selections. Ordinary-reader
and unmodified-Trealla controls remain separate. The broader experimental SWI
native suites retain explicit native-string/code-list expectations and separate
T3 diagnostics; this is not a deployment or language-profile adoption claim.

`adapters/local_portable_text.py` defaults to archived committed sources and
unchanged readers. Explicit `--swi-working-tree-candidate --swi-portable-text`
flags overlay only SWI `prolog/` working files in the disposable archive and
select the configuration only in that owned SWI process. `--shared-checks`
adds existing actor/interoperability packs; `--trusted-loopback-transport`
configures the disposable Trealla peer's explicit loopback trust boundary.
Source hashes, commands and preservation are recorded. These flags never update
installed engines, n3/n5 or the demonstrator's dependency pin.

The separate [portable-text migration checkpoint](reports/2026-10-25-portable-text-migration/COVERAGE.md)
records mode-specific native SWI tests, explicit native-library conversion checks
and an unedited example audit. Both modes pass full T4 and the focused checks;
model/Jev string guards remain application migration work. This test-only batch
does not add to the shared conformance totals or change deployed runtimes.

## Cyclic-term boundary diagnostics

The [25 October assessment](reports/2026-10-25-cyclic-term-boundaries/REPORT.md)
keeps local rational-tree behavior separate from message/answer portability.
Its [diagnostic matrix](reports/2026-10-25-cyclic-term-boundaries/COVERAGE.md)
records time-resource errors, lossy cycle copies and separate finite remote-actor
control failures. These observations add no normative cyclic-term requirement or
conformance pass totals; runtime code and deployed nodes are unchanged.

The [computed-answer repair follow-up](reports/2026-10-25-cyclic-answer-rejection/REPORT.md)
records 31/31 disposable-node repair selections passing with early cycle guards
in the two native working-source candidates. Trealla's cyclic exception-copying
limitation remains a separate diagnostic; actor-message findings are unchanged.

The [actor write/1 follow-up](reports/2026-10-25-write-output/COVERAGE.md) records
shared native output assertions, copied-helper delivery and retained Trealla
stream denials. Character-list-reading migration remains separate.

The [current character-list adoption checkpoint](reports/2026-10-25-portable-text-current-checkpoint/COVERAGE.md)
keeps passing reader/round-trip checks separate from term-output and model/Jev
migration blockers. Regular n3's reader remains unchanged.

The [character-list term-output repair](reports/2026-10-25-portable-term-output/COVERAGE.md)
resolves the SWI write/writeln text-presentation mismatch on disposable nodes.
Model/Jev service boundaries still precede adoption on regular n3.

The [25 October committed local adoption checkpoint](reports/2026-10-25-committed-adoption/COVERAGE.md)
links exact implementation revisions to post-restart evidence. It records local
configuration adoption without changing shared pack totals or reclassifying
unresolved diagnostics.
