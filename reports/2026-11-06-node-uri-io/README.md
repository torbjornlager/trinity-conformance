# Node URI identity and copied I/O — 6 November 2026

**Development qualification captured before commit and deployment.** Appendix B remains the
contract and native SWI is the design reference. Trealla departures require a
concrete engine constraint and shared behavioral evidence. The Trealla repository
now records that rule in `AGENTS.md`.

The [shared selection](../../profiles/node-uri-io-0.1.md) runs 13 identical cases
against each native implementation, using the other as its peer: **26 pass,
zero failures**. [Results](shared/results.json) record the manifest, adapter,
fixture and runtime source fingerprints. This includes the reported local-ponger,
remote-pinger pattern with `writeln(Self)` and a trailing-slash destination.

Node identity is normalized before peer credential lookup, connection caching
and PID construction. Explicit node URIs retain transport dispatch, including
own-node URIs; `localhost` retains its local-dispatch meaning. Document/source
URI paths are preserved. Copied `write/1` and `writeln/1` retain public source,
including variable sharing, a second source transfer back to the origin, and
source-less direct and meta-called remote output. Output events are acknowledged;
actor baselines and subsequent queries are checked.

Trealla now resolves `writeln/1` through its private actor prelude, following SWI.
Its parser retains an earlier builtin binding, so fresh public call terms are
constructed before private compilation/dispatch. Trealla 3.14.20 disallows
redefining `write/1` after actor imports; its small private adapter is restored to
public `write/1` before source inspection or transfer. The tests assert observable
behavior rather than private helper names.

The complete Trealla run passes **98 unit groups and 73 interoperability
groups** ([log](trealla-all.log)); its runtime file hashes match the shared run
and remained unchanged afterward. [Verification](verification.json) records the
engines, command, source fingerprints and log hashes.

## Controls and limits

[Negative controls](negative-controls/results.json) use the previous native SWI
revision and the previous Trealla revision with only the already qualified
private-transport-worker repair applied. Seven of eight selected observations
fail as expected: noncanonical node identity/credential lookup, copied internal
I/O helper rejection, or the combined ping-pong case. Native SWI's copied
`writeln/1` case passes as the working design control. These are disposable
archived source fixtures, not public-node tests.

Native SWI passes all **1,077 T4 tests**, lint and the HTTP visitor ownership
check ([log](native-swi-t4.log)), plus the focused URI, own-node and cross-node
lifecycle selection ([log](native-swi-focused.log)).

The runtime fingerprints identify uncommitted working-tree sources. No consumer
pins, public endpoints or deployment configuration were changed. This report
qualifies the selected native behavior; it does not certify all Appendix B,
SWI-WASM, arbitrary URI equivalence or every network failure schedule.

The subsequent [committed revisions](committed-runtime-revisions.json) preserve
these qualified runtime sources. The [public rollout and UI evidence](../2026-11-06-node-uri-io-public-release/README.md)
records the subsequent deployment.
