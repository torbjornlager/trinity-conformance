# Ownership and lifecycle 0.1 (draft)

This ACTOR pack tests public language-level termination authority and monitor
observations across independently authenticated client connections. It was
extracted from the paper's K7/K8 findings. It is a scoped draft, not full
security, distributed-reclamation or runtime-thread certification.

Use a **disposable private node**, configured with two distinct authenticated
principals, each with `execute` capability only. Do not use an administrator
as either principal: that would test a different authority contract. Tokens
must be provisioned by the fixture operator; the runner does not mint tokens,
contact deployed nodes, or infer principals from token text. Different token
strings alone do not establish distinct principals; provisioning is an explicit
fixture precondition. Distinct connections have distinct client lifetimes.

```sh
python3 runner/run.py --ws-url ws://127.0.0.1:3060/ws \
  --manifest cases/ownership-lifecycle-0.1.json \
  --token-env OWNER_TEST_TOKEN --observer-token-env OBSERVER_TEST_TOKEN \
  --candidate candidate-name --report /tmp/ownership-lifecycle.json
```

The runner rejects missing or identical tokens before connecting. Secrets are
read from the environment and excluded from reports and command lines.

| Case | Required observation |
| --- | --- |
| OL-001 | A submitted foreign `exit/2` throws `permission_error(exit,actor,...)`. The target independently answers a probe after the attempt. Its owning client can then terminate it, and an independent monitor reports the supplied reason. |
| OL-002 | Explicit owner termination of a computing child delivers the already installed independent monitor exactly once; a later monitor reports `no_process`. |
| OL-003 | EOF on the owning TCP connection preserves the independent monitor for a ready computing child; the observer remains usable and a later monitor reports `no_process`. |
| OL-004 | The same EOF case covers a child and grandchild, both ready and computing, with independent monitors installed before closure. |

Readiness is established by messages; no sleep infers that computation has
stopped. The computing goals are pure Prolog `repeat, fail` loops. The observer
waits up to three seconds for each original notification and up to two seconds
for later absence. These are bounded test observations on the fixture, not
universal cancellation or notification deadlines. No public registry observation
is treated as proof that an underlying host thread has exited.

OL-001 records return versus throw before inspecting an exception, and probes
the target even if the denial will fail. A normally returning call cannot pass
by unifying an unbound variable with a fabricated permission-error term.
OL-002 is the matched explicit-termination control for the socket-close cases.
These tests do not use private actor tables or host-thread introspection.

Earlier links/monitors cases exercised explicit root termination within one
client execution. Earlier wire ownership tests rejected foreign WebSocket
commands. Neither exercised the combination of an admitted submitted `exit/2`
goal, a foreign client lifetime and independently installed observer monitors.
Historical manifests and failed reports remain unchanged.
