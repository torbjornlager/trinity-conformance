# Portable runtime capabilities

Appendix B defines exactly five runtime_property/1 capabilities: persistent/1,
inbound_addressable/1, dom/1, actor_isolation/1 and hard_termination/1. Isolation
is independent or cooperative; the other values are boolean. Implementation
identity belongs to diagnostic tools, not this relation. Unknown or nonmatching
properties fail without binding inputs.

The five prerequisite RT assertions run unchanged through actor queries, with
five matching HTTP cases. They check exact finite enumeration, uniqueness,
positive and negative bound lookups, malformed properties and variable
preservation. Each native implementation runs both surfaces in blacklist and
whitelist modes.

```sh
python3 adapters/local_runtime_contracts.py \
  --manifest cases/runtime-introspection-0.1.json \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --swipl /path/to/swipl --tpl /path/to/released/tpl \
  --mode blacklist --output /tmp/runtime-introspection
```

Repeat with `--mode whitelist`. The adapter binds disposable nodes to loopback,
closes each successful actor session, stops the nodes in cleanup, and records
observations and the manifest digest. No public deployment is modified. The
native capability fixes should land before enabling this selection on main.
