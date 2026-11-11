# Monitor preflight

This focused Appendix B selection keeps MC-001–018 and MC-026–031 from the
prerequisite monitor audit. It checks registered-name resolution, independent
references, queued application data, idempotence, foreign ownership, required
arguments, atom-valued node components, malformed option lists and full error
culprits. Failed validation must leave bindings, observations and mailbox data
unchanged. Every expected receive has a throwing timeout.

The assertions are literal public goals with no private source helpers or opaque
meta-call admission requirement. An originally unbound options argument is checked
with var/1 before and after the call; compound inputs use fresh structural copies.
This avoids relying on a separate unbound snapshot across Trealla exception
unwinding while still requiring unchanged API inputs and fresh output variables.
Runtime guards do not appear in the submitted source.

Run the same cases against both native implementations in both sandbox modes:

```sh
python3 adapters/local_runtime_contracts.py \
  --manifest cases/monitor-preflight-0.1.json \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --swipl /path/to/swipl --tpl /path/to/released/tpl \
  --mode blacklist --output /tmp/monitor-preflight
```

Repeat with `--mode whitelist`. The adapter starts and stops disposable loopback
nodes and records all observations and the manifest digest. It does not modify
public nodes. The broader wait/context audit and browser qualification remain
separate. Native barrier tests additionally cover remote down-selection races
and timeout/retry of confirmed withdrawal.
