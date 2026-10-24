# Synchronous toplevel waits 0.1 — separate draft conformance pack

This draft selects the shared manual's synchronous toplevel wait contract.
It does not amend baseline 0.1 or advertise a new node profile. Required means
required within this pack. Both native ACTOR candidates execute identical
[public-interface goals](../cases/toplevel-waits-0.1.json).

| Case | Selected observation |
| --- | --- |
| TW-001 | Explicit caller targeting succeeds; conflicting targeting raises the documented domain error. Query/template variables remain independent. |
| TW-002 | Default timeout leaves the answer unbound. Timeout callbacks preserve bindings, logical failure and exceptions, and commit to their first solution. |
| TW-003 | Late call and next answers cannot satisfy subsequent synchronous waits. Timeout does not cancel the gated computation. |
| TW-004 | A conflicting output fails after selecting its call/next slice; later paging returns exactly the remaining answers. |
| TW-005 | Committed exit during a synchronous call raises toplevel_down(Reason); spawn-time and independent monitors still deliver that exact reason. |
| TW-006 | Synchronous selection preserves ordinary asynchronous answers, unrelated application messages and both public monitors. |

Gates are self-contained query terms, not inherited helper assumptions. They
announce readiness and await explicit release messages. Every readiness and
notification wait has a failure/exception timeout callback; a default timeout
cannot silently stand in for readiness. Sequential query processing establishes
that the old answer has been emitted before a subsequent reply. There are no
fixed sleeps, private correlation envelopes, runtime imports or registry access.

TW-002 intentionally collects callback results with findall/3 and requires exactly
one value, testing the documented commitment. The runner also requires a final
success with More=false; no outer once/1 hides residual alternatives. TW-004
advances beyond each mismatched slice rather than expecting a reply to next after
an already completed query. Pids and monitor references remain opaque, and
implementation-specific error contexts are not compared.

Each case owns fresh session fixtures, halts its toplevel on success and consumes
expected public notifications. Disposable-session/node teardown bounds failures.
This finite selection does not prove private monitor reclamation, arbitrary
interleavings or deadline accuracy under traffic. Remote transport, browser
execution, GNU ACTOR, terminal I/O, concurrent clients, cancellation and general
lifecycle stress are outside this batch. Failures remain visible; runtime repairs
require a separate batch.
