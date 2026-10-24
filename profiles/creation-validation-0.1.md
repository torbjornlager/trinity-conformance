# Local creation-option validation 0.1 — separate draft pack

This draft selects local creation predicates' runtime option-validation contract
from the shared manual. It does not amend baseline 0.1 or create an advertised
profile. Required means required within this pack. Both native ACTOR nodes execute
identical [public-interface assertions](../cases/creation-validation-0.1.json).

| Case | Selected observation |
| --- | --- |
| CV-001 | An unknown spawn option raises domain_error(spawn_option,Option). |
| CV-002 | An unbound list, improper list and unbound option entry raise the selected instantiation/list errors without publishing a pid. |
| CV-003 | Invalid link, monitor and node values raise the selected boolean/atom_or_string type errors. |
| CV-004 | Invalid later duplicates are rejected in spawn, toplevel and supervisor options. |
| CV-005 | Plain spawn rejects session/strategy options; their wrappers accept valid settings. First session(false) wins over later session(true), yielding a terminating one-shot toplevel. |
| CV-006 | An unknown option is rejected before a missing source URI is fetched or the goal is activated; valid creation still succeeds afterward. |

Option lists are delivered as ordinary self-messages before calling creation
predicates. This makes validation occur at execution rather than allowing static
query admission to reject/transform literal spawn options first. Unbound lists
remain unbound; every captured exception is explicitly required to be nonvar
before its formal term is matched. Context text is not compared. The listed
formal errors are the selected common subset, not a claim that all error names
are identical across implementations.

The staging also delivers literal receive/wrapper option lists as ordinary data;
those values and callbacks are unchanged. Readiness waits explicitly throw on
timeout. No sleeps, runtime imports, private registries or native threads are
used. Normal successful fixtures consume expected monitor notifications. The
runner requires final success with More=false without an outer once/1.

The initial literal-option run is retained separately. Its admission/source
preparation differences and Trealla logical failure are unresolved diagnostics,
not passes of this runtime-validation contract. This pack does not certify that
all malformed literal options can be caught inside a submitted query.

Child specifications, statecharts, HTTP options, remote creation, concurrency,
source policy and exhaustive quotas are excluded. The zero-time unwanted-start
polls are bounded public observations, not proof against arbitrary delayed
activation. Disposable session/node teardown bounds failures. Runtime repairs
require a separate batch; installed engines and n3/n5 are not changed.
