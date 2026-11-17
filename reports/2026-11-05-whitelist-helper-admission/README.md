# Whitelist private-helper admission repair

Trealla now admits private helpers in retained sessions and child source under
whitelist mode. No manuscript, public node, deployment pin, SWI runtime or
browser runtime changed.

Session admission now follows ownership resolution in the relay. It obtains
predicate indicators from that target's installed private source, excluding
imported/bootstrap predicates and shared owner definitions. Private source
that shadows a shared definition retains its own whitelist membership. Goal
checking and rewriting still use the configured policy and the executing
actor's private context. One session cannot supply another's helper names.

`toplevel_call/3` does not install source. Source options on a WebSocket session
call now raise `domain_error(toplevel_call_option, Option)` before source work;
they cannot fabricate whitelist membership. Source-free/private actors and
ordinary public built-ins continue through the existing dispatch.

Child preflight now derives names from literal text and clause lists, as well
as copied predicate indicators. It inspects copies, leaving application
variables and source sharing untouched. Constructed text and URI source defer
source-dependent membership checks to the existing runtime spawn guard. URI
preflight performs no fetch. Known forbidden operations are still rejected
before fetching, and actual source bodies are validated by the caller before
child creation.

## Execution evidence

All **401 final runtime observations pass**:

| Selection | Pass | Fail |
|---|---:|---:|
| Twelve shared cases, native SWI/Trealla, whitelist | 24 | 0 |
| Same selection, blacklist | 24 | 0 |
| Same selection, off | 24 | 0 |
| Settings profile/sandbox/context matrix | 314 | 0 |
| Whitelist transport and fetch-boundary controls | 15 | 0 |

The [shared manifest](../../cases/private-helper-admission-0.1.json) covers
retained helpers, alternatives and sharing, literal/mixed/constructed/copied
child source, guards, timeout callbacks, rollback, library closures and checked
dynamic updates. Native results are recorded for
[whitelist](shared-whitelist/results.json),
[blacklist](shared-blacklist/results.json) and [off](shared-off/results.json).
[The first whitelist run](shared-first/results.json) is also retained. These
shared tests use fresh sessions with real source loading and child actors.

The [transport controls](transport-final/results.json) exercise real
WebSockets and a local HTTP source server. They verify pagination, invalid call
sources, unavailable helpers, protected runtime/module boundaries, one caller
fetch for URI source, forbidden fetched bodies, post-error session reuse,
same-connection target isolation, and cross-connection ownership before source
lookup or fetching. A forbidden child operation paired with a source URI
produces zero HTTP source requests. A valid child fetches exactly once; a
forbidden body is fetched once and rejected without running the child helper.

The maintained native `whitelist_helper_tests.pl` additionally checks that
shared owner code and bootstrap/imported predicates do not confer private
membership, private shadows remain callable, preparation does not bind caller
variables, and call-source rejection applies across sandbox modes. The
extended `src_list_admission_tests.pl` proves that forbidden literal helper
bodies are rejected with the child pid still unbound. Both are included in
the [full unit/interoperability run](regressions.txt).

## Before and after

The previous source-qualified settings report had 312 passes and two failures:
`actor-whitelist-source-child-sourceless` and
`actor-whitelist-source-child-private`. The previous
[clean-source diagnostics](../2026-11-05-node-settings-trealla/existing-helper-baseline.json)
also reproduced retained-session helper rejection without `node_setting/2`.
Their qualified source maps to pre-repair commit
`c989f0e917c7e5662d93911100a0b4d7a5cc5a02`.

The [first repaired settings run](settings-first/results.json) uses exactly
the previous manifest and adapter hashes: all 314 cases pass. The
[final settings run](settings-final/results.json) strengthens private-session
rows to call `ns_read/2`, a source helper wrapping `node_setting/2`; those rows
also pass in every sandbox mode. The earlier failures remain in their dated
report; no case was waived or removed to achieve this result.

The current ledger moves the existing Trealla node-setting evidence to these
passing private-helper routes. New source/toplevel cases are listed as
candidate evidence. They do not establish every atom/string representation,
URI/file/remote route, option error or lifecycle obligation, so their whole
source/toplevel units remain unverified. B-346's RELATION endpoint mapping is
still pending. GNU and browser node-setting gaps remain separate.

[Verification metadata](verification.json) records the final source/adapter
hashes, committed runtime revision, test commands and outcomes. Runtime source
files were frozen during final qualification. The full native unit and SWI/Trealla
interoperability suite and all 104 conformance-runner tests pass. No public
deployment is certified by these disposable development fixtures.

## Reproduction

Use fresh output directories from the conformance checkout:

```sh
python3 adapters/local_actor_cases.py --swipl /usr/local/bin/swipl \
  --tpl /Users/lager/trinity-demonstrator/.trinity/trealla-engine/tpl \
  --swi-root /Users/lager/swi-prolog-node --trealla-root /Users/lager/trealla-port \
  --manifest cases/private-helper-admission-0.1.json --sandbox whitelist \
  --output /tmp/helper-admission-shared-new
python3 adapters/trealla_helper_transport.py \
  --tpl /Users/lager/trinity-demonstrator/.trinity/trealla-engine/tpl \
  --root /Users/lager/trealla-port --output /tmp/helper-admission-transport-new
python3 adapters/trealla_node_settings.py \
  --tpl /Users/lager/trinity-demonstrator/.trinity/trealla-engine/tpl \
  --root /Users/lager/trealla-port --output /tmp/helper-admission-settings-new
```

Repeat the shared command with `--sandbox blacklist` and `--sandbox off` for
the control modes. From the Trealla checkout:

```sh
TPL=/Users/lager/trinity-demonstrator/.trinity/trealla-engine/tpl \
SWIPL=/usr/local/bin/swipl TEST_TIMEOUT=120 TEST_STARTUP_DELAY=1 \
TEST_PORT_BASE=25760 tools/test.sh all
```
