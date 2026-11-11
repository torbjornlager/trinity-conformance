# Opaque reference creation and admission

The selection strengthens the existing LC-001 reference assertion with explicit
determinism, freshness across repeated calls and message round-trip identity.
It assumes no numeric width or host representation. Public ACTOR queries must
admit make_ref/1; stateless HTTP must reject it and remain usable afterward.

The same four profile-policy assertions run in both native implementations:
RELATION, ISOBASE and ISOTOPE reject the primitive, ACTOR admits it, and admission
does not bind its output. The adapter supplies only the native policy module.
These rows are labeled policy checks in the report. Trealla main has no HTTP
ISOTOPE session routes yet, so this selection does not claim wire-level ISOTOPE
session qualification or pull in the pending session implementation.

```sh
python3 adapters/local_runtime_contracts.py \
  --manifest cases/reference-contracts-0.1.json \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --swipl /path/to/swipl --tpl /path/to/released/tpl \
  --mode blacklist --output /tmp/reference-contracts
```

Repeat with `--mode whitelist`. All cases run unchanged against both native
implementations on disposable loopback nodes. The native SWI and Trealla admission fixes should
land before this selection becomes a required main gate.
