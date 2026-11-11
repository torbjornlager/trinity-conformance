# Successor validation on admitted native surfaces

Native SWI is the design reference for Appendix B's non-negative integer succ/2
relation. Trealla 3.14.20 can report an instantiation error or failure for supplied
floats. The port's small shared integer relation repairs that engine constraint
without replacing the engine, widening sandbox admission or exposing runtime
guards in copied source.

The selection checks directions, zero, determinism, invalid types and domains,
both-variable errors, original culprits and unbound peer arguments. Identical
assertions cover HTTP and actor queries, static higher-order calls, private
source, receive guards/bodies and source copied to a child actor. All expected
receives have throwing deadlines.

```sh
python3 adapters/local_runtime_contracts.py \
  --manifest cases/successor-validation-0.1.json \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --swipl /path/to/swipl --tpl /path/to/released/tpl \
  --mode blacklist --output /tmp/successor-validation
```

Repeat with whitelist and owner sandbox-off modes. The adapter uses disposable
loopback nodes and records observations and a manifest digest. The native Trealla
fix must land before requiring this selection on main.

The prerequisite maplist callback case requires separate whitelist library
admission work. It remains with that batch and is not silently counted as a pass
or used to justify widening this extraction's permissions.

The runner reports two explicitly deferred rows per runtime in whitelist mode:
SU-019 and SU-HTTP-019 (literal call/N admission). They remain active in blacklist
and owner-off modes. SU-020 now runs in every mode with validated private-helper
session admission. These cases are checked on both runtimes with the same
selection; deferrals are not counted as passing successor semantics. Maplist
remains with the pending library-admission batch.

`cases/interop-successor-0.1.json` runs the valid relation, float validation,
and private-source contract across both native peer directions. Use the standard
`runner/baseline.py` with `--profile actor --url ws://localhost:PORT/ws` and
`--peer http://localhost:PEER_PORT`, then reverse the two nodes. These three
cases run in blacklist, whitelist, and owner-off modes without deferrals.
