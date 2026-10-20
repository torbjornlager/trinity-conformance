# Trealla public worker routing: bounded repair

Follow-up to the focused comparison earlier on 20 October 2026. The source
changes are uncommitted and have not been loaded into the running n5.

## Cause and change

Source-less PTCP queries run in `toplevel_actors`, which did not supply public
parallel entry points. Private-source execution already supplied its own
wrappers, and local tests imported `parallel` directly, so they missed this path.

Importing the predicates alone was insufficient: native meta-calls could lose
worker goal context. The final repair adds small source-less forwarding wrappers
that pass the current actor's private module to the existing worker combinators.
A focused preparer makes those entries explicit in ordinary controls and in the
sandbox's rewritten catch helper. A fixed non-meta execution entry preserves
control scope while passing a prepared query through the PTCP enumeration layer.
Structurally unchanged queries retain their original execution path. Existing
private-source routing, worker algorithms, startup/cleanup scopes and policies
are unchanged. No sandbox rule was relaxed.

This is an application integration defect; no independently reproduced Trealla
engine bug has been established for an upstream report.

## Validation

- `public_worker_routing_tests.pl`: ordinary and compound calls, both
  `first_solution` arities, unexpected worker exits, the continue policy,
  rewritten sandbox catch, variable sharing, actor operations inside workers,
  supplied predicates, native cuts and conditional scope. The original source
  without forwarding wrappers fails the first worker-call check.
- Existing toplevel, isolation, sandbox, unexpected-worker-exit and worker-scope
  suites pass. Expected diagnostics from intentionally malformed source tests
  remain present; the groups exit successfully.
- Disposable public ACTOR node: 17 worker-routing probes with/without supplied
  source, including four negative checks, pass. See
  `2026-10-20-trealla-worker-routing-fixed.json` and the reusable external-node
  probe script `2026-10-20-worker-routing-probes.py`.
- The ACTOR Core and Behaviours profiles were rerun on the repaired candidate;
  their JSON reports have prefix `2026-10-20-trealla-worker-fixed-`.

The continue-policy path can still expose an open paging choicepoint: a single
successful page may have `More=true`, followed by `failure` on `next`. The tests
consume that empty final response and verify that no additional solution is
produced. Changing this existing paging behaviour is outside this routing repair.

## Separate observations

The SWI worker-cleanup ownership error noted earlier occurred again in a
supplied-source `first_solution` continue-policy probe. It remains a separate
race investigation; this repair changes no SWI runtime code.

During exploratory blacklist-mode checks, the harmless `shell('true')` worker
was accepted by the disposable SWI candidate and rejected by Trealla. An earlier
`open` probe also had different outcomes. Those are recorded as policy/route
observations, not failures of a shared sandbox profile: the worker-routing
comparison does not establish equivalent blacklist enforcement. No security
policy was changed here; the book's blacklist qualification remains in place.

An intermediate preparer exposed a control-scope regression and was not kept.
The final fixed execution entry passes both the existing control tests and new
worker-control regressions. Intermediate `worker-routing-after-repair` and
diagnostic files are exploratory; use the final `trealla-worker-routing-fixed`
report for the completed repair.

## Subsequent determinism repair

The empty continuation described above was subsequently traced to `select/3`
in the continue handlers and removed with two `selectchk/3` replacements.
See `2026-10-20-first-solution-determinism.md` and its public test results.
