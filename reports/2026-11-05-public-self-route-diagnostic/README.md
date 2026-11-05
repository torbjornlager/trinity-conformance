# N5 public self-route diagnostic — 5 November 2026

**20/20 attempts pass** on the actual N5 public HTTPS and actor self-route.
Ten use the original `promise(URL,true,R,[template(mark)])` shape. Ten replace
the HTTP goal/template with `get_time(T)`/`mark(T)` to record producer execution.
All use separate owner/foreign retained contexts with the same execute-only
credential. Foreign collection remains denied; the owner receives its answer
within the original two-second wait. The collector's four-second reply deadline
is also unchanged. Explicit toplevel halt bounds the live diagnostic footprint.

[Raw observations](observations/results.json), [analysis](analysis.json),
[exact adapter](adapter-source.py) and [service identities](services.json) are
retained. A temporary execute-only token was minted for this diagnostic and
[revoked](credential-cleanup.json) in the wrapper's finally block. No bearer or
administrator secrets are stored. No deployment settings or runtime code changed.

## What the timestamps show

In the ten timestamped attempts, producer execution began 51.9–59.7 ms after
promise creation began. Producer execution to owner collection was 122.4–149.6 ms,
including the intervening foreign probe and actor transport. Each of the twenty
owner `yield` calls itself took under 0.2 ms at the server. This is consistent
with answers being ready by collection in this run. It does not measure the
instant the HTTP response reached the promise worker or was installed locally.
The producer and collectors run on the same node; these are wall-clock samples,
not latency guarantees or a proof about every scheduling interleaving.

The source timestamps and diagnostic control change the workload somewhat;
these attempts are evidence about this recorded selection, not exact replays
of the entire earlier 51-case run or its surrounding load/connection history.

## Failure preservation and limits

An initial owner timeout would remain a failed attempt. A subsequent diagnostic
retry would be recorded separately and could not turn it into a pass. The
analysis tests enforce that distinction and retain attempts lacking timings.
All [73 runner self-tests](runner-tests.txt) pass.

The historical `CTX-015-trealla-b` timeout did not reproduce in these twenty
attempts. Its cause remains undiagnosed; no ownership defect, transport defect
or performance fix is claimed. The [original observation](../2026-11-05-cluster-peer-policy/public-contexts-repeat-timeout/results.json)
remains unchanged. More repetitions alone would not explain it. If it recurs,
these phase observations can distinguish delayed producer execution from delay
after execution; exact response-arrival and answer-installation timing would
require separate runtime diagnostic instrumentation.

The [controlled local extension](../2026-11-05-controlled-promise-suite-qualified/README.md)
continues to cover deterministic pending timeout, ownership and retry. Public
repetitions are a diagnostic selection, not additional language features or a
replacement for that conformance gate.
