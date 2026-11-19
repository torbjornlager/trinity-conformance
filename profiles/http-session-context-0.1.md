# Retained HTTP client contexts 0.1

This selection tests explicit retained HTTP sessions on disposable SWI and
Trealla fixtures with equal execution-only credentials. The same selection also
runs without client credentials using `--anonymous-http-sessions`; each session
retains its own visitor cookies where the runtime requires them. It does not change the
older retained-context manifest, its case inventory or historical observations.

| Case | Candidate | Required observation |
|---|---|---|
| HCTX-001 | SWI, Trealla | An unrelated session cannot yield a pending promise or dispose of it. The owner still sees it pending, then collects after explicit producer release. |
| HCTX-002 | Trealla | Equal ordinary names coexist in different HTTP session namespaces; lookup and withdrawal remain local to a session. |

The promise test acknowledges HTTP request arrival, holds the answer producer,
checks foreign yield/cleanup and owner retry, releases the answer, then requires
successful owner collection. Exactly one producer request is allowed. Every
language query must finish with `more:false`. Two independently spawned sessions
use the same credential, so authentication does not substitute for context.

SWI's HTTP route has an ISOTOPE ceiling and rejects actor naming operations;
HCTX-002 therefore targets Trealla's HTTP ACTOR extension only. The shared ACTOR
naming contract remains tested on WebSockets by `client-naming-0.1`. Passing
HCTX-001 does not establish common stateless HTTP ownership semantics.

```sh
python3 adapters/local_retained_context.py \
  --swipl /path/to/swipl --tpl /path/to/tpl \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --http-session-context-only --output /fresh/report/directory
```

This explicit mode enables Trealla's optional HTTP session routes only on its
owned fixture, runs exactly the three observations in the
[manifest](../cases/http-session-context-0.1.json), and tears down all fixture
processes. Any failure, blocked observation or error gives a nonzero exit.
Default retained-context behavior and inventory remain unchanged. Report
selection and case inventory must match before claiming qualification.

The accepted candidate contract isolates fresh HTTP requests even with equal
credentials; sharing across queries requires an explicit retained session.
SWI previously shared by authenticated principal. OPEN exercise compatibility
is measured separately from these three session observations.
No credential, route setting or runtime is changed by this adapter on live nodes.
