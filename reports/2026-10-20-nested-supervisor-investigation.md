# Native SWI nested-supervisor investigation

The earlier BH-009 timeout was **not evidence of a stalled restart**. The native
SWI candidate rejects the submitted query before executing it. The runner's
`recv_type('success')` discarded the immediate error and kept waiting for success,
turning that rejection into a misleading socket timeout.

## Actual runtime difference

The original query uses an earlier conjunction to bind `Inner`, then passes that
variable inside `start(start_sub_supervisor(Inner, Options))`. At admission time
the nested list is still unbound. SWI's static sandbox walker exposes such a list
as an unknown executable meta-call and rejects it with `instantiation_error`.
Trealla accepts the variable-bound form. This remains a compatibility limitation;
no sandbox check was weakened or skipped during this investigation.

The exact original form was rerun after correcting error reporting. SWI's error
arrived in about 15 ms; Trealla completed it in about 333 ms. See
`2026-10-20-nested-runtime-bound-diagnostic.json`.

## Real replacement path

Using the same two inner workers, outer sibling, restart policies and shutdown
settings, with the nested child list explicit in the specification:

1. SWI creates the outer supervisor and starts its nested supervisor and sibling.
2. Killing the nested supervisor causes one-for-one replacement.
3. The replacement has a new pid; the outer sibling retains its pid.
4. Subsequent child inspection and supervisor halt respond successfully.

A staged public WebSocket diagnostic and supervisor debug messages confirmed
these phases. No supervisor lifecycle code was changed.

## Harness and test corrections

- `Harness.recv_type('success')` now raises immediately on terminal `error` or
  `failure`, retaining preceding event context. It continues to allow child
  `down` notifications before success. Other wait types keep their selective
  behaviour.
- Four runner regressions check immediate admission errors, failure after a
  child notification, success after a child notification, and unchanged halt
  waits.
- BH-009 now spells the nested list explicitly, isolating its advertised
  subtree-replacement requirement from runtime-bound-data admission. The
  original variable-bound form remains in the separate diagnostic report;
  its difference is not counted as repaired.
- The shared manual, Appendix B and SWI runtime README document the admission
  limitation. Book examples and runtime execution code are unchanged.

Both candidates pass ACTOR Core 0.1 (7/7) and ACTOR Behaviours 0.1 (10/10) after
these corrections. Raw reports have prefix `2026-10-20-nested-recheck-`.
SWI's earlier generic-server timeout did not recur in this run; intermittent
worker-cleanup ownership errors remain separate observations.

## Next possible batch

Supporting runtime-bound nested specifications on native SWI requires checking
the resolved child starts at execution time, before their execution or creation.
That is a separate sandbox-integration batch, with negative tests proving that
runtime-bound forbidden child goals remain rejected. The result here does not
justify weakening static validation or adding supervisor lifecycle machinery.

All nodes used here were disposable loopback processes. They were stopped;
running n3 and n5 were not changed. Investigation changes and reports are
uncommitted.
