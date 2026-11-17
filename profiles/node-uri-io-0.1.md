# Node URI identity and copied I/O

Native SWI is the design reference for shared behavior; Appendix B remains the
contract. Engine-specific adaptations must stay private and must preserve the
same observable behavior. A concrete engine constraint is required before
choosing a different solution.

The shared selection in `cases/node-uri-io-0.1.json` and
`fixtures/node-uri-io/program.pl` runs unchanged in both native directions.
It covers own-node URIs with and without a trailing slash, qualified local sends,
toplevel URI aliases, copied `write/1`, `writeln/1` and `format/1`, variable sharing
in the visible source body, and a second source transfer back to the origin.
Source-less remote actors cover direct and meta-called `writeln/1` as well.
The ping-pong case includes the reported `writeln(Self)` and trailing-slash URI.

Explicit node URIs retain their existing transport semantics. Normalization
precedes credential lookup, connection caching and public PID construction;
source/document URI paths are not rewritten. The `localhost` designator retains
its local-dispatch meaning.

Each case gets a fresh ACTOR session. Expected receives have throwing deadlines,
both child terminations are observed, public actors must return to their baseline,
output events are collected and acknowledged, and a fresh query must work afterward.
The adapter starts disposable loopback nodes with test-only peer authentication.
It records the source files and manifest hashes and closes the nodes afterward.

```sh
python3 adapters/node_uri_io.py \
  --swi-root /path/to/swi-prolog-node \
  --trealla-root /path/to/trealla-port \
  --swipl /path/to/swipl --tpl /path/to/tpl \
  --output /tmp/node-uri-io-results
```

Use a released Trealla engine supported by the port. The adapter pairs it with
the library directory beside the executable. `--case NU-009` selects the reported
ping-pong pattern; `--timeout` controls the external socket bound.

Trealla installs `writeln/1` in its private actor prelude, following SWI. Its
reader carries an earlier builtin binding, so the compiler first rebuilds the
public call to let the actor's local definition resolve it. Trealla 3.14.20 rejects
redefining `write/1` after actor imports; that operation retains a small
`sandbox_write/1` adapter, restored to public `write/1` before transfer. The shared
tests assert output, source visibility and lifecycle behavior rather than private
helper names.
