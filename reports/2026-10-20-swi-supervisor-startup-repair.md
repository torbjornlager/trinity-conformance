# Native SWI initial-startup and dynamic-addition rollback

Native SWI now journals provisional children for one initial startup or one
`supervisor_spawn_child/3` attempt. Local admission records pids before activation;
acknowledged remote creation records its returned pid during a protected handoff.
The journal holds cleanup copies without replacing live specifications or their
variable sharing. Successful admission commits the journal. Failure rolls back
in reverse start order using child shutdown policies and private cleanup monitors.
Only the supervisor's recorded monitor references and its private cleanup
references are removed or flushed; application monitors and messages survive.
Cleanup continues after ordinary cleanup errors while preserving the original
startup outcome. Reserved runtime control transfers propagate. A committed actor
exit retains normal parent-link containment and does not wait on a dying mailbox.

Initial ordinary failure retains `init_failed`, and initial exceptions retain
their original term. Dynamic ordinary failure replies `error(start_failed)`;
dynamic exceptions reply `error(Error)` without replacing existing state or
terminating siblings. Creation timing, restart policy, defaults and precedence
are unchanged. A child goal subsequently failing is a normal child termination.
`infinity` may make rollback wait indefinitely.

A required node-layer integration retains ownership when a local spawn throws
after activation, allowing the creating scope to reclaim that pid. Ownership is
removed by normal pid retirement. Never-activated reservations are still removed
immediately. Public exit authority checks are unchanged. A focused regression
failed before this integration (the provisional plain actor remained live) and
passes with it. The never-activated case also has a regression.

Validation:

- 63 supervisor, startup, request-cleanup and child-spec test entries pass,
  including parameterized variants and the final empty-mailbox check.
- 75 node-composed startup, ownership, authority, naming and request-cleanup
  test entries pass, including parameterized variants.
- Startup regressions cover partial startup, ordinary failure, preparation
  exceptions, pre-admission monitor failure, post-activation spawn failure,
  reverse rollback order, numeric/infinite/brutal shutdown policies, forced
  shutdown of a blocked server, original-error preservation after cleanup faults,
  variable sharing, dynamic retry, unrelated monitors/messages and committed exit.
- Whitespace checks pass for runtime, test and manual sources.

Public compatibility checks ran on fresh SWI 10.1.17 and Trealla 3.13.10 nodes
on test ports 39860/39861. Core cases pass 7/7 on both. Behaviour cases pass
10/10 on Trealla; the first SWI run passes 9/10, with BH-009 exposing an intermittent
`permission_error(load,source,sandbox_source_1)`. A comparison reproduces that
same category against the previous supervisor implementation (two failures and
one pass), while three subsequent scoped-startup attempts pass. This remains a
separate source-loading diagnostic; the mixed public run is not represented as
fully passing. Raw reports use the `2026-10-20-startup-` prefix.

The shared HTML manual and Appendix B TeX source describe common startup rollback
once, with explicit remaining runtime differences. Internal details are in the
native runtime README. No PDF build was requested for this batch.

Explicit respawn, automatic restart failures, intensity exhaustion, general spawn
lifecycle, unknown remote outcomes and remote cancellation remain separate.
Disposable nodes were stopped. Running n3/n5, book examples and other runtimes
were unchanged. Changes are uncommitted.
