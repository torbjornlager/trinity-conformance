# Trealla public node settings

The Trealla development source now implements `node_setting/2`. No public node,
deployment pin, manuscript text, GNU runtime or browser runtime changed.

The relation exposes an explicit public allowlist. Listener identity is
registered and retired with the server, follows the connection into retained
sessions and descendants, and is not inferred from Host headers. Limits and
source policies are read from the current enforced process-wide configuration.
The development profile is reported by its public profile, `actor`.

Two Appendix B keys are unavailable in this host: `timeout` and
`max_sessions_per_principal`. Neither has a separate node configuration here,
so both fail. The public `max_load_text_bytes` reports the actual
`max_source_text_bytes/1` ceiling. Source-origin values are canonical URI atoms
with explicit ports, sorted without duplicates. Shared source, credentials and
principal policies are never enumerated. Settings are unavailable outside a
serving context.

The implementation imports and routes the predicate through source-free HTTP
workers, retained toplevels, generated private modules, child actors and
receive callbacks. The ordinary sandbox safe-predicate list admits it; source
definitions and guarded dynamic updates cannot replace it. It is admitted as
a read-only relation in the RELATION profile too.

## Evidence and remaining gap

The [shared final run](shared-final/results.json) passes **20/20** assertions:
ten shared cases through HTTP and the same ten through a retained session.
The added NS-010 checks bound-value filtering and failure for a mismatching
value representation. A [SWI control](shared-swi-control/results.json) passes
the same 20 assertions without runtime changes.

The [profile/sandbox/context matrix](matrix-final/results.json) has **312 passes
and two failures**. It uses real disposable ISOBASE, ISOTOPE and ACTOR nodes
under blacklist, whitelist and off sandbox modes. It checks the complete
configured relation, public URLs independent of Host headers, nondefault
limits, unavailable/private keys, source helpers over HTTP, retained sessions
with and without private source, child actors, receive guards, and rejected
source definitions/dynamic updates. Configuration fixtures include fictional
private principal and credential sentinels.

The two failures are `actor-whitelist-source-child-sourceless` and
`actor-whitelist-source-child-private`. Whitelist WebSocket admission rejects
the child helper's name before the child runs. A separate existing restriction
also rejects direct calls to a retained session's named private helper.
[Clean pre-repair diagnostics](existing-helper-baseline.json) reproduce both
restrictions at `d92364caaef3b23efdce07d388aa221e20a83b00`, using `ns_probe/1`
and no `node_setting/2` call. The blacklist control passes. Source inspection
finds that nested admission collects copied predicate indicators but not those
defined by literal child source; session command admission also lacks retained
application predicate indicators. These remain unresolved admission gaps,
not passing cases or profile waivers. The matrix command still exits nonzero.

Direct calls to `node_setting/2` pass in all tested private/source-free
sessions and children, including whitelist. Named private helpers calling it
pass through HTTP in every tested sandbox mode and through WebSocket child
programs in blacklist/off modes. This qualification does not certify arbitrary
private-helper admission, all transport/lifetime semantics or public releases.

The maintained `node_settings_tests.pl` also checks unavailable settings
outside a context, nested context and exception restoration, linked-child
inheritance and cleanup, current policy changes, RELATION visibility, origin
normalization and bound-value mismatches against policy defaults. Policy
getters are called with fresh output variables before matching the caller's
value, preventing an active-value mismatch from accidentally selecting a
getter's default-policy fallback.

[Final broad regressions](regressions-final.txt) run Trealla's full unit and
SWI/Trealla interoperability selection, including the new context tests.
[Verification metadata](verification.json) records the final source hashes,
commands and outcomes. The ledger maps B-339 through B-345 to scoped passing
Trealla evidence. B-346 remains unverified: default profile/read-only probes
pass, but RELATION endpoint coverage is still unit-only. GNU and both browser
modes retain their earlier missing-facility findings. No book change is needed
to express the existing unavailable-key rule.

## Retained diagnostics

The [first shared run](shared-first/results.json) exposed missing imports for
meta-call contexts; [the corrected nine-case run](shared-second/results.json)
passes before NS-010 was added. The [first matrix](matrix-first/results.json)
retains origin representation failures, a fixture that expected a sandbox
error where the stateless profile correctly denied mutation first, and the
existing whitelist helper-admission failures. The fixture now distinguishes
stateless profile rejection from actual ACTOR mutation rejection. Private
session probes call the public relation directly; separate helper/child probes
and clean baseline diagnostics retain the unresolved admission failures.

The [earlier broad run](broad-before-final-projection.txt) passed before the
final URI projection and bound-value corrections; its
[source hashes](broad-before-final-projection-sources.json) are retained.
The final broad run checks the corrected source. No runtime admission policy
was relaxed to turn these failures into passes.

## Reproduction

Use fresh output directories from the conformance checkout:

```sh
python3 adapters/local_standard_library.py \
  --swipl /usr/local/bin/swipl \
  --tpl /Users/lager/trinity-demonstrator/.trinity/trealla-engine/tpl \
  --swi-root /Users/lager/swi-prolog-node \
  --trealla-root /Users/lager/trealla-port --gnu-root /Users/lager/gprolog-port \
  --manifest cases/node-settings-0.1.json --only trealla \
  --output /tmp/node-settings-trealla-shared-new
python3 adapters/trealla_node_settings.py \
  --tpl /Users/lager/trinity-demonstrator/.trinity/trealla-engine/tpl \
  --root /Users/lager/trealla-port --output /tmp/node-settings-trealla-matrix-new
```

The first command passes. The second preserves the two existing admission
failures. From the Trealla checkout, run the maintained full regression suite:

```sh
TPL=/Users/lager/trinity-demonstrator/.trinity/trealla-engine/tpl \
SWIPL=/usr/local/bin/swipl TEST_TIMEOUT=120 TEST_STARTUP_DELAY=1 \
TEST_PORT_BASE=24760 tools/test.sh all
```
