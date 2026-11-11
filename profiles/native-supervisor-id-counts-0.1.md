# Native supervisor IDs and active counts

The `Id` in `child(Id, Options)` is an atom label used by supervisor management
APIs. It is distinct from the child PID returned by inspection or respawn.
Run `cases/native-supervisor-id-counts-0.1.json` through the local runtime
contract adapter on native SWI and Trealla in blacklist, whitelist and off.
Both paired runtime ID/count fixes and the supervisor lifecycle foundations
are prerequisites.

The cases cover integers, floats, lists, ground and nonground compound terms,
and unbound IDs at initial/dynamic creation and terminate/delete/respawn.
Caught errors must be nonvar; tests must not manufacture an expected error
by binding a variable after an accepted invalid call. Dynamic rejections leave
child records unchanged, and invalid initial specifications leave the supervisor
output unbound and its name unpublished. Native reservation/queue tests cover
validation before child effects and startup cleanup.

Count assertions cover live, stopped, respawned and deleted workers and nested
supervisors, in source-free and private contexts. Retained specs may remain after
a child stops; only active records contribute to supervisors/workers, so those
counts stay nonnegative. IDs do not change actor PID semantics. This is native
qualification; no deployed-node or WASM coverage is claimed.
