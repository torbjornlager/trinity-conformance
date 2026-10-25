# Cyclic-term boundary assessment — 25 October 2026

This is a test-only diagnostic assessment, not a new conformance requirement.
Baseline 0.1 excludes cyclic terms from its portable fixtures; it does not yet
prescribe every rejection outcome. Local rational-tree semantics remain separate
from what may cross a Web Prolog message or answer boundary.

## Conclusion

Keep local unification unchanged. The useful next repair would reject cyclic
payloads and solution templates **before** copying, nonbacktrackable storage or
wire serialization can lose their structure or loop. Acyclic non-ground terms
must continue to work and preserve repeated-variable identity. A cyclic error
culprit also needs a finite error envelope; merely throwing an exception that
contains the original cycle can move the problem to error delivery.

The assessment found real gaps, not a reason to introduce a general cyclic-term
library. No runtime changes or upstream reports were made in this batch.

## Exact inputs and bounds

- Native SWI source: `b61270d11c55b4a98166365c793e97e4a721acbb`.
- Trealla source: `9b7c9402b8653d79d34f86f2482c758cdaee71d7`.
- SWI 10.1.18 separate verified build, including the previously tested core/HTTP
  patches; this is not an unmodified upstream SWI comparison.
- Unmodified separate Trealla v3.14.10 build, with its matching library directory.
- Default text semantics and ISO settings; no portable-text or ISO-mode activation.
- Public fixtures use fresh source archives of those commits, disposable loopback
  ACTOR nodes, blacklist sandbox, open authentication, and explicit loopback
  peer trust on Trealla. These are not public deployment security settings.

[Provenance](results/provenance.json) records full commands, binary hashes,
source status, PIDs, ports and adapter hash. Each public case gets a fresh caller
and, where needed, a distinct peer process. A valid HTTP readiness request avoids
an abandoned partial-request fixture. The final actor fixture uses a plain echo
worker without extra monitor setup/cleanup; the owning disposable process is
always stopped after the case.

WebSocket reads and HTTP bodies are capped at 16 KiB, client socket waits at four
seconds, actor receives at one second and promise collection waits at three
seconds. Disposable processes also have a 20-second CPU cap and 1 MiB log-file
cap. These diagnostic safeguards are not changes to node resource policy.

## Observations

There are 36 public diagnostics, eight initial standalone engine observations,
and 14 supporting reductions. They are not summed into shared conformance totals.
The [matrix](COVERAGE.md) and [raw observations](results/observations.json) retain
all outcomes, including failed finite controls.

Both engines create and copy `X=f(X)`, reject creation with
`unify_with_occurs_check(X,f(X))`, and accept
`X=f(X), unify_with_occurs_check(X,X)`. This small sample does not establish
complete rational-tree compatibility.

SWI's local actor send rejects the cycle as `resource_error(term_depth)` in the
configured Web Prolog node; its raw thread queue preserves a cycle. Sending from
SWI to either peer gives the same sender-side rejection. These outcomes must not
be described as uniform native-engine behavior.

With a SWI HTTP peer, a query that constructs a cyclic answer reaches the node's
existing time limit and returns `resource_error(time)` to either caller runtime.
A three-second promise wait receives that same error. A cyclic exception also
returns a time resource error over raw HTTP. A finite summary of the cycle
returns immediately, so constructing it alone is not the problem. Supporting
native calls to `findnsols/4`, `term_attvars/2`, `portable_answer/2` and `answer/5`
complete with the cycle intact. The precise later HTTP-path traversal responsible
for the time-limit outcome remains untraced; this report does not attribute it
to `findnsols/4` or claim an upstream SWI engine bug.

With a Trealla HTTP peer, the cyclic result becomes an **acyclic** answer, for
example `success([f(f(_))],false)`, rather than an explicit rejection. Both `rpc/3`
and `promise/4` observe the changed structure. The same node can report
`acyclic_term(X)` false before the answer leaves the query. A standalone reduction
shows that `nb_setval/2` followed by retrieval already turns the cycle acyclic;
the page collector uses this storage before canonical answer serialization.
Consequently a check only at final serialization can miss the original cycle.
The result identifies a concrete early boundary to protect; it does not prove
this is the only lossy copying operation.

Trealla's raw thread queue also returns an acyclic copy of this cyclic input.
The local Web Prolog actor echo similarly returns an acyclic `f/1` term. Trealla's
remote cyclic actor probes reach the four-second client wait without a terminal
answer. Their exact blocking operation is not isolated here. The caller process
is still running when stopped; a timeout is not evidence of a process crash.
Trealla's cyclic HTTP exception closes the request without an HTTP answer; the
caller remains healthy on a fresh finite HTTP request.

## Finite controls and separate diagnostics

14 of 16 shared-variable controls succeed, including every HTTP, RPC, promise,
and local actor control. They check `pair(A,A)` by inspecting both variablehood
and identity after transfer, rather than relying on printed variable names.

The remote actor echoes SWI→Trealla and Trealla→Trealla time out even for this
finite non-ground payload. Plain ground `pair(a,b)` controls succeed in those
same directions in a supporting run. The remaining finding concerns non-ground
remote actor delivery or matching, not demonstrated cycle rejection. It needs
its own bounded trace; do not count the associated cycle timeout as an isolated
cycle-specific failure or silently weaken the sharing assertion. Trealla→SWI
and SWI→SWI shared-variable actor echoes succeed.

No disposable node exits before controlled shutdown. Every executed fresh HTTP
health check after a completed public observation succeeds. The two WebSocket
exception/timeout rows do not execute that health step, so health is not claimed
for those rows. All disposable node processes are stopped. Preservation checks
cover native and Trealla runtime sources, selected engine/library hashes,
dependency pin and n3/n5 process identities. Installed launcher targets and
hashes also match the preceding ISO assessment. Its uncommitted documents and
README change remain untouched.

## Recommended next bounded batch

1. Add early cycle rejection to computed answer and exception boundaries in both
   native runtimes, with finite, portable error envelopes. Check each solution
   before collection storage; check exception payloads before storing/sending them.
2. Protect Trealla message copying/serialization before a cycle can become an
   acyclic approximation or stall a sender. Preserve finite shared variables.
3. Keep the two non-ground remote actor control failures as a separate diagnostic
   investigation. Do not change general unification or globally enable occurs
   checking as a workaround.

The exact public error category should be agreed before adding normative negative
cases. Browser and GNU runtimes, cyclic source/options, attributed terms, deeper
mutually recursive cycles, alternate HTTP formats, remote toplevel answer
protocols, and repeated stress/performance runs were not assessed here.

## Reproduction and evidence

The runner is [adapters/cyclic_boundaries.py](../../adapters/cyclic_boundaries.py).
It deliberately refuses to overwrite its output directory. For a repeat run,
select a new directory without touching the recorded results:

```sh
python3 - <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, 'adapters')
import cyclic_boundaries as probe
probe.OUT = Path('/tmp/trinity-cyclic-boundaries-repeat')
probe.main()
PY
```

Its default binary/source paths identify this Mac's separate builds; edit those
inputs in a copied runner when reproducing elsewhere. Do not resolve the SWI
launcher to its underlying executable, since its runtime-home lookup depends on
the launcher layout. Run from the conformance repository.

[followup.py](followup.py) records eight supporting engine operations and the two
ground remote actor controls. [swi-reduction.py](swi-reduction.py) records four
supporting native internal operations. These supporting scripts use unchanged
working-tree runtime sources, which match the preservation hashes; they are not
additional public-interface conformance cases. Their output directories likewise
must be fresh. Early exploratory fixture runs were discarded after the final
bounded run; existing historical reports are unchanged.
