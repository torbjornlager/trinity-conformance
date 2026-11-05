# Node-setting conformance audit

This is an audit of development sources, not a deployment or a completed
five-mode repair. No runtime code, manuscript text, dependency pin or public
node changed.

The [nine shared cases](../../cases/node-settings-0.1.json) check finite,
nonempty enumeration; unique keys; bound-key and bound-value lookup; unknown
and structurally invalid keys; the privacy allowlist; repeatable reads; public
profile names; and absence of settings for unavailable API families. Requiring
a profile and a nonempty enumeration prevents an empty implementation from
passing. These are ordinary public queries, without privileged introspection.

| Execution boundary | Pass | Fail |
|---|---:|---:|
| SWI HTTP | 9 | 0 |
| SWI retained session | 9 | 0 |
| Trealla HTTP | 0 | 9 |
| Trealla retained session | 0 | 9 |
| GNU HTTP | 0 | 9 |
| WASM Worker | 0 | 9 |
| WASM main | 0 | 9 |
| SWI configured-node/context probes | 8 | 0 |

[Native results](native/results.json), [real-Chrome results](browser.json),
and [configured-node results](configuration-final/results.json) contain the
observations and source hashes. There are **26 passing and 45 failing final
observations**. The shared core selection is nine cases across five language
modes; retained sessions and configured-node probes add execution boundaries.
The failures repeatedly expose one missing facility in each affected mode;
they do not represent 45 distinct runtime bugs.

The configuration adapter starts ISOBASE, ISOTOPE and ACTOR listeners in one
SWI process, with distinct nondefault timeout, rate, size and capacity values.
It asserts the complete visible key/value relation for each profile. It then
repeats each HTTP assertion with a Host header naming another live listener.
An ACTOR retained session and its linked child must see that node's exact
settings. The owner-only `dev_principal` fixture remains private. Open and
development authentication configurations are both exercised.

SWI passes those checks. B-339 through B-345 receive scoped passing evidence.
B-346 remains unverified because changing the owner's built-in family policy
has not been exercised; default profile visibility and repeated reads pass.
The HTTP semi-stateful session interface, custom family policies, relation-only
profiles and live public deployments are outside this qualification.

## Missing implementations

Trealla returns `existence_error(procedure,node_setting/2)` in fresh HTTP
workers and retained sessions. Source inspection finds no public relation in
`actor_api.pl`, `isolation.pl`, `node.pl`, or the source-free dispatch surface.
Its real configuration already resides in node, resource, governance and
source policy modules. A repair must export and admit the relation through all
private/source-free contexts and enumerate an explicit public allowlist.

GNU rejects the predicate with `permission_error(execute,isobase,node_setting/2)`.
The ISOBASE policy, prologue and worker contain no public implementation.
The HTTP owner's configuration must reach the separate query worker through
trusted metadata before the relation can report actual serving-node values.
Standalone workers must fail for unavailable settings. Merely admitting the
name in the policy would not implement the contract.

Both generated browser Prolog surfaces lack the relation and produce
`existence_error(procedure,node_setting/2)` in real Chrome. The asset server's
address is not evidence of an inbound execution-node URL. HTTP authentication,
admission ceilings and rate settings must not be invented for these hosts.
Appendix B already permits unavailable keys to fail; a repair must distinguish
actual execution-host settings from settings of a remote peer or asset server.

Source pins are SWI `80e3e799a40c2c39d87efccb5a6e1ba4d9a8fe1e`, Trealla
`d92364caaef3b23efdce07d388aa221e20a83b00`, GNU
`4a3e587f0b53fb38a11006bb1abc9cc10376ebc5`, and browser package
`deb11db4ff58c27b4565f7125d29b0deec6627f7`. All were clean when tested.
Native reports hash runtime Prolog/C sources and executables; browser reports
hash both generated surfaces, bundle and package manifest.

B-339/B-340 are marked failing for these four modes, based on execution.
B-341 through B-346 are marked missing based on inspected absence of the
facility, with the failing queries retained as candidate evidence. No profile
waiver or unavailable-setting exception conceals an undefined predicate.

## Fixture corrections

The [initial manifest](initial-manifest.json) omitted a lexical space between
`->` and `\+` in NS-009. Its [native](native-baseline/results.json) and
[browser](initial-browser-fixture.json) runs are diagnostics, not qualification.
The final selection corrects that syntax and reruns all cases unchanged in
scope. The [first configuration run](configuration/results.json) used a
detached child; node policy correctly rejected that request. The
[corrected run](configuration-corrected/results.json) uses the normal linked
child and passes. The final run pins the final adapter and its helpers.
No runtime policy was relaxed.

## Reproduction

From the conformance checkout, use fresh output directories:

```sh
python3 adapters/local_standard_library.py \
  --swipl /usr/local/bin/swipl \
  --tpl /Users/lager/trinity-demonstrator/.trinity/trealla-engine/tpl \
  --swi-root /Users/lager/swi-prolog-node \
  --trealla-root /Users/lager/trealla-port \
  --gnu-root /Users/lager/gprolog-port \
  --manifest cases/node-settings-0.1.json --output /tmp/node-settings-native-new
python3 adapters/local_node_settings.py --swipl /usr/local/bin/swipl \
  --swi-root /Users/lager/swi-prolog-node --output /tmp/node-settings-config-new
```

Package the clean browser checkout with its `tools/package_runtime.py`, then:

```sh
NODE_PATH=/tmp/promise-context-browser-tools/node_modules \
LIBRARY_RUNTIME_ROOT=/tmp/node-settings-audit-package \
LIBRARY_MANIFEST=/Users/lager/trinity-conformance/cases/node-settings-0.1.json \
LIBRARY_REPORT=/tmp/node-settings-browser-new.json \
/Users/lager/.nvm/versions/node/v22.23.4/bin/node adapters/wasm_actor_cases.cjs
```

The native and browser baseline commands intentionally exit nonzero while the
missing relation remains unrepaired. [Verification metadata](verification.json)
records final counts and hashes. The next implementation step is Trealla's
public relation and context dispatch, followed by GNU's trusted owner-to-worker
metadata and the two browser host surfaces. The manuscript's existing
unavailable-key and privacy rules require no change on this evidence.
