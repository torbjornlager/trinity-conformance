# Early computed-answer cycle rejection — 25 October 2026

The native SWI and Trealla working-source candidates now reject computed cyclic
answer templates with `error(representation_error(cyclic_term),_)`. Native SWI
also replaces escaping cyclic exceptions with a finite error before retaining
or delivering it. Local unification and locally caught exceptions are unchanged.

Trealla exception preservation remains a separate engine issue, as agreed during
this batch: changing every user `throw/1` would affect locally caught exceptions,
so it is not used as a workaround. The original diagnostic assessment and its
actor-message findings remain [historical evidence](../2026-10-25-cyclic-term-boundaries/REPORT.md).

## Implementation

SWI checks the template on each successful goal evaluation, before
`findall/findnsols` collection. An invalid solution enters the existing goal-error
path, preserving its finite-prefix/pending-error paging behavior. Escaping cyclic
exceptions are converted before `nb_setarg/3` stores the pending error. Ordinary
errors and their repeated-variable identity retain their existing representation.
The outer collection-error normalization defensively handles any still-cyclic
exception as well.

Trealla checks a PTCP solution before `copy_term/2` and page `nb_setval/2`, and an
HTTP producer's template before receive-clause preparation or its message
handoff. Those are earlier than final canonical serialization, where the engine
may already have lost the cycle. One small `answer_terms.pl` helper serves both
paths. Defensive exception checks handle a cycle if it reaches the handler intact;
they cannot infer one that the engine has already changed.

Checks inspect terms without binding variables. A cyclic value used only during
local computation is permitted when the returned template is finite. The native
SWI regression also checks a locally caught cyclic exception returning a finite
answer. This is not global occurs checking. Application actor messages, remote
non-ground actor diagnostics, browser runtimes and GNU were not repaired here.

## Verification

[32 live observations](results/observations.json) comprise **31/31 required repair
regressions** and one separate Trealla cyclic-exception diagnostic. All four
caller/peer combinations use distinct disposable native SWI/Trealla processes.
The selected checks cover:

- HTTP and WebSocket rejection of computed cycles in both runtimes;
- finite HTTP error delivery for native SWI cyclic exceptions;
- RPC and promise cycle-error delivery with either peer;
- finite shared-variable identity through HTTP, RPC and promise paths;
- timeout callback followed by successful promise retry in all four pairings;
- finite returned templates after internal cyclic computation, ordinary errors,
  and a fresh HTTP health query following every observation.

Native T2 passes, including cyclic bare/formal/context exceptions, finite prefix
preservation, later-page rejection, session reuse, local catches and variable
sharing. Full native T4 passes **1529 parameter selections**. Trealla's new
`cyclic_answer_tests` passes, including HTTP producer-scope cleanup, later-page
rejection and session reuse. Five unchanged related groups also pass: synchronous
toplevel wrappers, promise/yield correctness, HTTP once cleanup, whole-page
deadlines and HTTP paging cleanup. These overlapping native results are not
added to the shared baseline totals.

Raw native logs are in `swi-prolog-node/docs/verification/cyclic-answer-rejection-2026-10-25/`;
Trealla logs and the related-check commands are in the corresponding
`trealla-port/docs/verification/` directory. [Validation](validation.json) records
preservation and health checks. [Provenance](results/provenance.json) records the
exact runtime-source hashes and working-tree status, binary hashes, process
commands, PIDs, ports, and runner hashes. These are explicit working-source
candidates over SWI `b61270d11c55b4a98166365c793e97e4a721acbb` and Trealla
`9b7c9402b8653d79d34f86f2482c758cdaee71d7`, not deployed or committed-head claims.

The selected engines are the separate verified SWI 10.1.18 build with the prior
core/HTTP fixes and unmodified Trealla v3.14.10 with its matching libraries. No
engine patch or installation occurred. The fixture policy and socket/process
bounds are inherited from [the diagnostic runner](../../adapters/cyclic_boundaries.py).

## Separate Trealla engine diagnostic

The standalone `trealla-port/reproducers/port-cyclic-exception-copy.pl` imports no
Web Prolog code. On unmodified Trealla v3.14.10 it reports:

```text
before_throw-cyclic
after_catch-acyclic
```

On the selected SWI engine, both stages report `cyclic`. This demonstrates why
post-catch checking cannot guarantee equivalent exception rejection in Trealla.
The live Trealla HTTP cyclic-exception probe still closes the request without a
response, while the next finite HTTP health query succeeds. It is recorded as a
diagnostic, not a passing repair regression or a process crash. The adapter does
not attempt to turn an already acyclic exception back into a cycle, infer its
history, or rewrite user catches/throws. No upstream report was submitted here.

## Scope and reproduction

The shared manual documents the new native answer behavior and the remaining
Trealla exception qualification. Runtime READMEs describe the check placement.
Book examples, dependency pin, installed runtime targets/binaries and n3/n5 are
unchanged; all 52 disposable node processes are stopped. Existing uncommitted
ISO assessment files and earlier reports are preserved.

From the conformance checkout, with the recorded candidate runtime files present:

```sh
python3 - <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, 'adapters')
import cyclic_answer_repair as repair
repair.OUT = Path('/tmp/trinity-cyclic-answer-repair-repeat')
raise SystemExit(repair.main())
PY
```

The output path must be new. The adapter deliberately selects working-source
roots; use its recorded hashes to reproduce these inputs. It is not a baseline
manifest or a new claim of complete cycle portability. Broader cycle shapes,
offset-skipped cyclic values, formats beyond the selected Prolog HTTP and
WebSocket routes, performance, and the full Trealla unit/interop suite were not
rerun. The two earlier non-ground remote actor failures remain separate.
