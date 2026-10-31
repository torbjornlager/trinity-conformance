# Ownership and lifecycle repairs — 31 October 2026

The two paper findings are repaired in separately committed SWI and Trealla
sources. The original failed paper record is unchanged. The unchanged full
paper harness now passes **54/54** scenario executions (nine scenarios, three
repetitions per engine). The new shared pack passes **24/24** executions
(four scenarios, three repetitions per engine). The normal conformance CLI
passes all four cases on each engine as a separate integration check.

## Causes and repairs

- **Trealla:** wire commands checked connection ownership, but admitted
  submitted goals invoked the actor library's `exit/2` without that check.
  A core policy hook now checks inherited client scope before local signalling
  or distribution routing. Same-scope siblings, trusted local code and node
  owners retain their legitimate authority. Unknown routes are not authority.
- **SWI:** `ws_kill_actor/1` erased all monitors of a closing connection's
  owned actors. This removed monitors installed by surviving observers.
  Normal actor retirement now retains and delivers those notifications.
- A positive administrator control exposed a related **SWI owner-context
  lookup defect**: pre-bound patterns could skip the actual owner frame and
  select an outer/public fallback. Lookup now selects the frame before
  testing the caller's pattern. Two native tests cover both context sources.

## Why earlier coverage missed these

Earlier wire tests denied foreign commands at the protocol boundary. They
did not submit a foreign `exit/2` call through an already admitted goal.
Earlier links/monitors cases ran within one client execution and terminated
roots explicitly. They did not combine connection teardown with monitors
installed by a different surviving client. The new pack exercises exactly
those combinations, including computing children and grandchildren.

OL-001 also probes survival even if the denial assertion will fail. It never
constructs an expected exception by unifying an unbound error variable after
a normally returning call. A weak native SWI assertion was tightened likewise.

## Controls and outcomes

The new pack on the original snapshots reports **15 pass, 9 fail**: SWI
fails OL-003/004 in all repetitions; Trealla fails OL-001 in all repetitions.
Both original engines pass the matched explicit owner-termination control
(OL-002). These results are kept alongside the repaired observations.

Eight additional public controls pass: same-account separate connections
remain isolated, sibling termination succeeds, administrator submitted-goal
termination succeeds, and ISOBASE HTTP rejects actor exit before execution
for ordinary and administrator principals while leaving the target responsive.
The HTTP control is a profile-admission check, not an ownership measurement.

Trealla's complete existing unit runner passes. SWI's focused authority group
passes 37/37; LINT, T0 and T2 pass. The full T4_NATIVE run is **not green**:
five supervisor assertions fail. A matched unmodified-source control also
has five supervisor failures, with varying strategies/assertion identities.
Those records remain separate; this repair does not claim to resolve them.
The first native run's 256-process limit also caused resource exhaustion;
its output is retained and the final native runs use 1024 processes/2 GiB.

The conformance runner's existing 50 Python unit tests pass. Missing fixture
tokens are rejected before any connection is made.

## Provenance and replay

`repaired-commits.json` identifies both runtime commits; `base-pins.json`
records their original revisions. `final-source-hashes.json` identifies the
executable sources used by final validation. The two repair patches and all
raw results/logs accompany this report. `SUMMARY.json` states exact scope.

Use the normal invocation in `profiles/ownership-lifecycle-0.1.md` on a
disposable private node with two separately provisioned execution-only
principals. The dated fixture scripts preserve the container orchestration,
with `/work` bound to the repair workspace, `/sources` to the chosen source
set (swi/trealla/conformance), and `/results` to a fresh writable directory.
The fixture source archives must match the recorded pins and hashes.
Lifecycle fixture `case-inputs.json` files contain inherited, unused paper
inputs; the actual OL manifest and runner module are the versioned sources.

No deployed node, installed engine, production credential or external service
was changed. No observer registry check is treated as proof of host-thread
termination, and bounded notification waits are not universal deadlines.
