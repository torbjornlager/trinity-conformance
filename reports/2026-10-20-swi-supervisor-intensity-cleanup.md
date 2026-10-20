# Native SWI restart-intensity exhaustion cleanup — 2026-10-20

Exhaustion is now decided before replacement startup and before committing the supervisor exit. The triggering child is marked inactive. The existing reverse-order policy cleanup stops remaining recorded children using fresh private monitors, then the supervisor exits with `shutdown`. Ordinary cleanup errors do not replace this reason or prevent attempts for remaining children. Reserved runtime control transfers still propagate. An externally committed exit retains its original reason and containment path.

Restart timestamp collection, strict period boundary, pruning and the number of allowed restarts are preserved. The private intensity predicate now fails on exhaustion so its caller can perform cleanup. No replacement starts once the budget is exhausted.

## Verification

- New intensity unit: six test entries (eight parameterised instances) pass. Covers all three strategies at zero budget, exactly two permitted restarts, period pruning and strict boundary, numeric timeout escalation, graceful infinite-policy completion, brutal kill, cleanup send exceptions, and same-mailbox application/unrelated down-message preservation during a reserved cleanup control transfer.
- Broader behaviour run: 51 entries, including parameterised variants, pass across supervisor, intensity, restart failure, startup and request cleanup; final empty-mailbox check passes.
- Node/ownership run: 13 entries, including parameterised variants, pass. Tests exhaustion under ordinary owner authority for all three strategies alongside replacement/startup/worker ownership regressions.
- The public-interface zero-budget test fails for all three strategies against the pre-repair supervisor: remaining server children receive `kill` and do not observe graceful reverse stopping. It passes with the repair.
- Shared HTML manual, Appendix B source and native runtime README updated. No book examples, PDF, live n3/n5 processes, or broader lifecycle paths changed. No new live conformance run was needed for this local exhaustion path; focused public-interface regressions run through both behaviour and node harnesses.

This supersedes the intensity-exhaustion qualification retained in the earlier restart-failure repair report.
