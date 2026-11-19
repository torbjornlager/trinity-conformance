# Public admission controls 0.1

Admission budgets belong to the operator. A query cannot raise its own budget.
Applicable budgets must be configurable, and public metadata must describe the
values actually enforced. Changing a request rate does not raise concurrency,
actor, memory, CPU, process or execution-time ceilings.

Server runtimes expose an `admission` object in `/node_info`. Only applicable
public controls appear. Existing `node_setting/2` keys retain their meanings;
this object also describes limits enforced outside the Prolog engine.

| Field | Meaning |
|---|---|
| `rate_identity` | `principal` or proxy-verified `client_ip`; never a caller-supplied identity |
| `window_policy` | `fixed`, `rolling` or `leaky_bucket` |
| `rate_window_seconds` | Window length, or the time unit for the advertised refill rate |
| `max_call_requests_per_window` | Requests charged to the call budget per identity/window; native SWI includes `/call`, `/toplevel_call` and `/toplevel_next` |
| `max_session_spawns_per_window` | Session creations admitted per identity in a fixed/rolling window |
| `max_engine_starts_per_window` | Shared fresh-engine budget across HTTP calls, HTTP-session creation and WebSocket connections |
| `requests_per_minute`, `burst` | Leaky-bucket refill rate and additional burst allowance; not a strict rolling-minute maximum |
| Concurrency fields | Separate bounds, such as `max_inflight_calls`, `max_sessions_per_principal`, `max_ws_actors_per_principal`, `max_public_engines` and `max_public_engines_per_client` |

SWI and Trealla retain their existing principal and window contracts. N7's
public ECLiPSe adapter counts fresh engines by client IP in a rolling window.
Public GNU N6 uses its trusted ingress's leaky bucket. These are different
accounting units; an engine-start ceiling must not be advertised as a separate
120-call allowance plus a separate 120-session allowance. Reusing a retained
N7 session consumes no further fresh-engine allowance.

Anonymous execution remains available in OPEN mode. The budget identity is
independent of the ordinary-name/promise ownership context. In particular,
sharing an IP budget does not permit clients to share ordinary names.

The browser execution host has no public HTTP listener or server admission
budget. Its missing rate-related `node_setting/2` keys remain inapplicable.
Calls to a remote server consume that server's applicable budget.

The selected public deployment preset is 120 call entries and 120 session
creations per 60 seconds on SWI/Trealla, 120 shared engine starts per 60 seconds
on N7, and a 120-request/minute ingress refill rate on GNU. Existing concurrency
and resource bounds remain in place. This preset is not a throughput guarantee.

`runner/admission.py` checks finite answer equality over a sustained interval.
A 429, another HTTP error, or an error inside an HTTP 200 body is a failure,
never a passing language assertion. Its count and pacing are explicit. Run
exhaustion and configuration-boundary controls in owned fixtures; do not consume
an entire public node's capacity merely to discover its limits. HTTP 429 replies
should include `Retry-After`; a concurrency retry delay is advisory, whereas a
rolling-window rate delay can be calculated from the oldest charged admission.

Historical conformance observations remain immutable. New budgets and passing
paced controls do not erase earlier admission refusals.

The live native SWI HTTP-IP layer also charges retained query/page commands to
the call budget. Session-creation capacity is not an allowance for unlimited
queries inside those sessions. The maintained prompt stress pack uses paced
session creation without delaying its reply/abort/halt races. A refused case
remains a refusal in its original attempt, even if a paced control later passes.
