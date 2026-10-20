# first_solution continue-policy determinism

Follow-up to the public worker-routing repair. The previous observation of
`More=true` followed by terminal `failure` was caused by local solver-list
bookkeeping, not HTTP `length/2` or offset arithmetic.

Both `handle_first_failure/6` and `handle_first_error/7` used `select/3` to remove
a known worker pid before recursively waiting for another solver. Trealla's
`select/3` retains an alternative to search for another occurrence when the
removed pid precedes other elements. Worker pids in this list are unique, so
that alternative can never succeed. It nevertheless survives a later winner,
prevents immediate determinism detection and delays scope finalization until
backtracking or commitment.

The repair replaces those two calls with `selectchk/3`, which commits only the
unique pid removal. It adds no cut to the worker query, result collector, user
goal or toplevel pager. Policies, winner selection and exception propagation
are unchanged. HTTP offset calculations are untouched.

`first_solution_determinism_tests.pl` first demonstrates the `select/3` choice
point, then uses a separate monitored gate actor to permit failure/exception/
exit before releasing a winner. The original implementation fails with
`leftover_choicepoint(failure)`. With the repair, all three cases return
successfully without an outstanding choice point, preserving unrelated down
notifications. Existing unexpected-worker-exit, worker-scope and public-routing
regressions also pass. Public-routing regressions now require final pages.

Six disposable public WebSocket checks (three rejection kinds, with and without
supplied source) return the winning value with `More=false`. Their results are
in `2026-10-20-first-solution-determinism-fixed.json`.

This supersedes the earlier note that the routing repair deliberately retained
an empty continuation. The common manual already declares first_solution
semidet and single-result; this repair restores that existing contract rather
than defining new paging semantics. The runtime README and regression runner
are updated. Source changes remain uncommitted; the running n5 is unchanged.
