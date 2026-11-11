# Native library callback contract

Run `cases/native-library-callbacks-0.1.json` with
`adapters/local_runtime_contracts.py` against the native SWI and Trealla roots,
using `--mode blacklist`, `--mode whitelist` and `--mode off`.

The selection covers maplist/2–8, foldl/4–6, countall/2, call_nth/2 and forall/2:
private closures, prefix arguments, ordered alternatives, state threading,
original scalar culprits, unused callbacks, rollback and propagated exceptions.
It also exercises nested and copied private source, sandboxed clause reflection,
HTTP queries, and denial of forbidden/qualified callbacks and private guard entry
points. HA-011 in the private-helper selection is active alongside these cases.

Both native runtime changes must land before requiring this selection on main.
Appendix B controls callback behavior; SWI is the design reference, including
where its current host behavior needs repair. Trealla's native forall checks both
arguments before running its generator, so the runtime defers invocation and
restores the public goal when source is exported.

Invoked-variable probes use blacklist and owner-off: whitelist can reject opaque
closures at admission, before execution. Forbidden operations and private guard
entry points are checked only in sandbox modes and never executed in owner-off.
Clause reflection is qualified in sandbox modes, where the runtime promises
application-source restoration; owner-off source export is verified by native
unit tests and copied-child execution. These exclusions are not semantic
failures or deferrals. No browser, WASM, deployed-node or complete standard-library
certification is claimed.

Fold helpers use equivalent structured facts. SWI 10.1.19's clause inspector can
return a variable body for a clause whose sole unification is optimized into its
head; that separate engine issue can make whitelist analysis reject such a
source clause. This fixture avoids depending on that decompiler behavior while
still testing fold argument order and state threading. It is not a runtime fix
or a claim that the source-inspection issue is resolved.
