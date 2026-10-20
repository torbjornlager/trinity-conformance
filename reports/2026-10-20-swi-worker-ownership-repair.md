# Native SWI worker-cleanup ownership repair

The pre-retirement node stop hook removed actor ownership before the actor core
retired the pid-to-thread mapping. A concurrent worker cleanup could therefore
see a resolvable actor without the ownership record needed to authorize exit.
The former WC-004 failure and repeated-call ownership diagnostic exercised this
window.

The repair retains ownership until the existing registry/monitor retirement
transaction has completed. A pre-retirement hook still samples final CPU usage;
a new post-retirement hook removes owner, mailbox and CPU records and reclaims
unused lineage outside the actor locks. The exit authorization predicate is
unchanged. This avoids suppressing permission errors or adding network work
inside the retirement locks. No public protocol or book example changed.

A controlled regression pauses an actor in the pre-retirement stop hook after
the node's work, checks that its owner can still stop it, and checks that an
outsider is denied. It verifies metadata reclamation after the post-retirement
hook and harmless repeated exit after retirement. A second regression preserves
the original exception through worker-scope cleanup. The controlled test fails
against the previous runtime with the original exit permission error and passes
with the repair.

Validation:

- Standalone actor tier: 86 test entries passed (including parameterized cases).
- Targeted node suites: 51 entries passed across worker ownership cleanup,
  lifetime authority, worker scopes and generic actor API.
- Identical public ACTOR Workers 0.1 assertions: SWI 8/8, Trealla 8/8.
- Separate repeated-call diagnostic: passed on both candidates for the tested
  eight iterations with and without supplied source. This is a finite diagnostic,
  not a claim that all possible lifecycle races are absent.

Public runs used fresh SWI 10.1.17 and Trealla 3.13.10 processes on ports 39860
and 39861, with the same configuration as the original worker batch. Reports
are named `2026-10-20-ownership-fixed-{swi,trealla}-{actor-workers-0.1,worker-diagnostics-0.1}.json`.
Earlier failure reports are retained. Disposable processes were stopped; n3 and
n5 were unchanged. Runtime documentation is in the native README; the shared
language contract already requires this cleanup behaviour.
