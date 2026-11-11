# Public serving-node settings

The fourteen actor cases run unchanged against native SWI and Trealla in
blacklist, whitelist and owner-off using `local_runtime_contracts.py`. They
cover enumeration, bound values, privacy, source helpers, receive callbacks
and copied children. The Trealla public-settings runtime fix is required.

`native_node_settings.py` adds direct HTTP checks for all four public profiles
and all three sandbox modes on both hosts. RELATION uses only direct
node_setting/2 calls; it does not assume general Prolog goal admission. Values
are compared with configured enforced settings, URL identity is compared with
the node's own metadata even with a spoofed Host header, and private/invalid or
unavailable family keys must fail. Hosts may omit unsupported settings; this
selection does not claim HTTP session implementation or GNU/browser support.

Run both drivers with `--swi-root`, `--trealla-root`, the released `--tpl` and
an output directory. The generic driver additionally takes `--manifest
cases/node-settings-0.1.json --mode MODE`. The node-settings fixture uses a fresh
output directory and loopback listeners, and never contacts deployed nodes.
