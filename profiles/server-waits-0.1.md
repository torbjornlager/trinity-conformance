# Generic-server waits 0.1 — separate draft conformance pack

This separately versioned draft selects the shared language manual's
[server_yield/2-4 contract](https://github.com/torbjornlager/trinity-demonstrator/blob/main/web/manual.html#server_yield/2-4).
It is not a baseline 0.1 amendment, new advertised node profile or complete server
lifecycle certification. Required means required within this selected pack.
Both candidates run identical public ACTOR goals and supplied callback source
from the [manifest](../cases/server-waits-0.1.json).

| Case | Selected observation |
| --- | --- |
| SW-001 | Request references distinguish replies; collect the second before the first. |
| SW-002 | A pre-bound conflicting output fails after consuming that selected reply; another reply remains available. |
| SW-003 | A zero-time wait invokes its callback, then the same reference collects the released reply. |
| SW-004 | Unmonitored yield timeout callbacks retain bindings, logical failure, the original exception and exactly the supplied alternatives. |
| SW-005 | server_request/4 and monitored server_yield/4 report server_down(sw_death); an independent monitor still delivers. |
| SW-006 | Monitored wait completion through timeout, mismatch or callback exception cleans its private monitor while preserving unrelated data, spawn monitoring, an explicit monitor and later reply collection. |

There are no sleeps or private runtime imports. A blocking callback announces
that it has accepted the request, then waits for a release/crash message. This
makes timeout tests deterministic without a guessed delay. A barrier request
establishes that earlier server replies were emitted before mismatch/poll checks.
Pids/references remain opaque, and no host-specific error context is compared.
The runner requires one final success with no residual query continuation.

SW-004 intentionally enumerates the alternatives of the timeout callback and
checks the exact result list. That enumeration is part of the contract, not an
outer once/1 hiding unexpected query alternatives. Alternatives under the
monitored four-argument form, cut/interruption cleanup and competing waiters are
not selected here. SW-006's absence checks are zero-time mailbox observations
after observed server termination; they do not certify arbitrary in-flight
remote notification races or use private registry counts to infer reclamation.

Each case has a fresh session with owned server fixtures. Expected responses and
notifications are consumed, explicit monitors retired, and servers halted on
success; existing linked-session and disposable-node teardown bound failed
fixtures. Unknown-reference validation, transport faults, remote servers, browser
execution, GNU ACTOR, quotas and general shutdown stress remain outside this
batch. A failing selected assertion remains a failure rather than a diagnostic
waiver. Runtime repairs require a separate batch.
