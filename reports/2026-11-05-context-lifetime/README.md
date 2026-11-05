# Context lifetime clause audit

The [clause-level audit](../../docs/CONTEXT_LIFETIME_AUDIT.md) maps every clause of
B-004, B-354 and B-296 to native evidence and identifies remaining browser and
GNU tests. Native SWI and Trealla now have scoped whole-source-unit evidence for
all three entries. Their runtime implementations did not change: this work adds
tests, a maintained closure selection, and reviewed evidence mapping.

## Added checks

- Four `CTX-019-*` public-API cases, one per directed native route, forward an
  originating reference to a remote descendant. Destination collection is
  denied, destination cleanup is harmless, and the origin still collects.
- Native late-completion assertions deliver a response after scope retirement
  committed. SWI exercises WebSocket and HTTP-session namespaces; Trealla checks
  the surviving owner actor. State and queues stay retired.
- Both real-Chrome modes resolve a pending completion after promise-context
  closure and verify the reference cannot reappear or be claimed.

The [expanded maintained gate](native-forwarding/results.json) passes **61
public-API observations**, four attachment-order checks plus two required unsafe
negative controls, and **six native closure regression selections**. The closure
adapter runs the existing name/ownership/lifecycle assertions, including late
name publication, admitted creation racing with teardown, surviving actors,
collector wakeup, foreign isolation and standalone ownership. These aggregate
selections are not six additional portable language cases. Their source files,
hashes and exact commands are recorded in [closure results](native-forwarding/closure/results.json).

The [browser package selection](browser/results.json) passes all eight selected
JavaScript/Chrome groups, including **61 promise-context checks** across both
modes. Runtime, engine and schema bytes are unchanged. The clean committed
package has exactly the same packaged file hashes as the tested development
package; [verification](verification.json) records both manifests and the native
test-only commits. Schema/native integration and consumer deployment tests were
not selected. All [104 runner tests](runner-tests.txt) pass.

## Retained diagnostic history

The first native invocation used `/usr/local/bin/tpl`, an older unqualified
system engine. Trealla listeners failed before observations and its attachment
fixtures failed: [original gate](diagnostics/system-trealla/results.json).
The [correct-engine run](first-contexts/results.json), selecting the existing
project engine, passes all 57 original observations and the attachment controls.
No runtime or deadline adjustment was needed.

A direct SWI invocation loaded individual components without the node composition
hooks: [original output](diagnostics/swi-without-composition.txt). The
[full-loader invocation](native-combined.txt) passes all 51 test declarations,
including their generated schedules. The new adapter uses that full loader and
rejects load errors even if SWI exits zero. The
[first closure selection](first-closure/results.json) and
[first integrated gate](native/results.json) also pass; the final gate expands
these with the four forwarding cases rather than retrying a failing assertion.

## Limits and next tests

Browser and GNU whole-unit statuses remain unverified. The audit names the exact
remaining boundaries: browser/native context return and reference forwarding,
browser ordinary-name closure/publication during startup, and GNU request/root
ownership and retirement while a completion is pending. A promise-only browser
close hook does not establish ordinary-name closure. Browser confinement is not
used as evidence for remote authentication policy.

Appendix B already states the required distinctions; no manuscript revision was
needed. Historical public timeout/interruption evidence is unchanged. Public
nodes, credentials, consumer dependency pins and release policy were not changed.
