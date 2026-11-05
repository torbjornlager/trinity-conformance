# GNU public node settings

GNU ISOBASE now implements `node_setting/2` using serving-controller metadata.
The HTTP controller passes a validated port/capacity/authentication tuple
through its private supervisor/worker arguments. The worker installs its
public context before loading shared or private source. This works without
inheriting additional environment variables or passing credentials, source
paths or principal policies as node settings.

Six settings are available: `url`, `profile`, `sandbox`, `auth`,
`max_inflight_calls` and `max_load_text_bytes`. The URL is the actual bound
loopback endpoint, profile is `isobase`, sandbox is the enforced `whitelist`,
authentication is the controller's actual open/private mode, capacity comes
from `--max-queries`, and the source ceiling comes from the worker's shared
loader constant. Other keys fail as unavailable; unrelated combined-request
and execution-time limits are not assigned different public setting names.
Standalone workers without a serving context enumerate no settings.

The query policy admits only the public relation. Its initializer and storage
remain inaccessible, and private/compiled source cannot redefine its name.
Malformed or duplicate bootstrap metadata is rejected before query execution.
Startup shared-source validation runs before a port is bound, with no serving
context. Metadata survives ordinary retained query pages and remains specific
to the controller serving them.

## Qualification

The [same ten shared cases](shared-first/results.json) all pass. An immutable
archive of pre-repair GNU commit `4a3e587f0b53fb38a11006bb1abc9cc10376ebc5`, built
with the current installed compiler, [fails all ten](baseline-final/results.json)
because the relation is rejected by the old policy. This is a source baseline,
not a claim to reproduce the old release binary byte for byte.

The [maintained GNU groups](native-final-qualified/results.json) pass **14/14**:
standalone absence, trusted worker and supervisor bootstrap, 28 malformed or
duplicate argument rejections, open/authenticated HTTP configurations, private
and shared helpers, unavailable/private keys, mismatched values, protected
metadata, independent controllers, unknown HTTP parameters and continuation
pages. Fixtures include private controller credentials and per-owner/budget
quotas; their values are not exposed. Forged ambient metadata has no effect.
The earlier [13-group run](native-first.json) and
[first recorded 14-group run](native-final/results.json) are retained too.
The final adapter also accepts relative repository paths; the baseline and
maintained-group reports above use that same final adapter hash.

The [full local suite](regressions-final.txt) passes, including source,
execution policy, standard library, numeric, RPC/local routing, supervisor,
memory, credentials, HTTP, eviction, ownership, request parsing, shared source
and distributed proof-tree tests. [Status reconciliation](status-check.txt)
passes without changing its versioned historical contract. All
[104 conformance-runner tests](runner-tests.txt) and both ledger validators
pass.

The [compiled suite](compiled-native-candidate.txt) passes. New assertions read
metadata through shared predicates in both interpreted and compiled nodes;
the suite also retains its 51 paired cases, native RPC, source, credentials,
security and memory checks. The compiled bundle manifest now hashes the new
bootstrap header. The controller, supervisor and worker are rebuilt together.

## Retained failures and comparison inputs

The [initial local run](initial-regressions.txt) timed out in an existing shell
supervisor fixture: a 0.6-second delay did not return its first response within
the one-second cumulative budget. That fixture passes no node metadata.
The [unchanged rerun](supervisor-rerun.txt) and the subsequent full local suite
pass. No timeout or runtime limit was relaxed.

The first compiled run correctly refused the newer demonstrator checkout
against its historical comparison lock; that
[refusal](compiled-historical-refusal.txt) is retained. An explicit candidate
run then [refused the consumer's stale native SWI pin](compiled-consumer-pin-refusal.txt).
The successful run explicitly selects clean native SWI revision
`1c25f34972e5d403e9b556ae12328c07966d4a24`, its native entry/RPC files and
SWI 10.1.19. Candidate mode identifies demonstrator revision
`7071a22861547daff1ac306a9128417d4c3548f6`; the recorded historical lock remains
unchanged. [Harness provenance](compiled-candidate-provenance.json) and
[verification metadata](verification.json) retain actual inputs and overrides.
This does not certify the demonstrator's configured dependency set or claim a
strict historical-baseline comparison. Neither dependency checks nor pins were
disabled or changed.

All execution here is native macOS development qualification. The Linux
query-jail path preserves the same validated argument protocol, but was not
executed in this batch. No public presenter, canonical reverse-proxy identity
or deployment is certified. Public nodes, release pins, browser code and the
manuscript are unchanged.

## Ledger and reproduction

B-339–B-346 now have scoped GNU ISOBASE evidence: six available keys and the
required failure behavior for unavailable/private values and disabled API
families. GNU has 31 verified source units; SWI and Trealla retain 42 each.
These are source-unit counts, not percentages of language conformance. Both
browser modes still lack `node_setting/2`.

From the conformance checkout, use a fresh output directory:

```sh
python3 adapters/gnu_node_settings.py --gnu-root /Users/lager/gprolog-port \
  --output /tmp/gnu-node-settings-new
```

Add `--baseline-revision 4a3e587f0b53fb38a11006bb1abc9cc10376ebc5` for the old
source selection, which deliberately exits nonzero with ten failing cases.
From the GNU `isobase` directory:

```sh
make all local-test status-check
COMPARISON_MODE=candidate \
COMPARISON_TRINITY_REVISION=7071a22861547daff1ac306a9128417d4c3548f6 \
COMPARISON_SWI_VERSION=10.1.19 SWIPL=/usr/local/bin/swipl \
SWI_NODE_FILE=/Users/lager/swi-prolog-node/prolog/web_prolog.pl \
SWI_RPC_FILE=/Users/lager/swi-prolog-node/prolog/web_prolog/rpc.pl \
make compiled-test
```
