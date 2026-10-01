# Source test inventory

This is a static inventory of `test/1` and `test/2` declarations in the
SWI-Prolog reference implementation at the time this repository was created.
Parameterized PlUnit declarations may execute more than once, so these are
source declaration counts rather than a count of runtime test instances.

| Tier | Subject | Declarations |
|---|---|---:|
| T0 | Core actors | 68 |
| T1 | Isolation and source preparation | 45 |
| T2 | Toplevel actors | 45 |
| T3 | Server, supervisor, parallel, and statechart behaviours | 170 |
| T4 | Distribution, node, profiles, policy, and operations | 558 |
| T5 | Wire-level interoperability | 20 |
| **Total** | | **906** |

These 906 declarations are not automatically 906 conformance requirements.
Most T4 cases, and portions of every lower tier, inspect SWI-specific modules,
thread behaviour, administrative facilities, or internal helper predicates.

## Extraction rule

A source test belongs in this repository only when it can be stated as an
observable requirement of an advertised profile. Extraction should:

1. assign a stable conformance case identifier;
2. identify the minimum profile required by the case;
3. name the original repository, file, suite, and test;
4. state inputs and expected observable outputs without naming internals;
5. run against a candidate through a public API or a documented thin adapter;
6. specify required isolation and cleanup.

The T5 wire tests are the best first source because they already exercise
HTTP and WebSocket behaviour across process and implementation boundaries.
The T0 and T2 suites are the next source for portable local API scenarios.
