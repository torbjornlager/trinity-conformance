# N7 HTTP conformance fixes

The disposable ECLiPSe CLP 7.2.13 candidate passed every assertion that
failed in the [previous checkpoint](../2026-11-08-n7-packaged-conformance/README.md).
The candidate ran with the N7 execution limits and no engine container network.

| Selection | Result | Evidence |
| --- | --- | --- |
| Required stateless HTTP | 10 passed | [IB-001 through IB-010](isobase-http.json) |
| Required cross-node HTTP | 2 passed | [HC-001 and HC-002](interop-http.json) |
| Supporting local RPC and promises | 7 passed | [LOCAL-001 through LOCAL-007](local-node-rpc.json) |
| Opt-in HTTP prompt and interruption | 17 passed | [PT-004 through PT-020](prompt-http.json) |
| Exploratory stateless diagnostics | 6 observations | [Diagnostic responses](isobase-diagnostics.json) |
| ACTOR Core | 7 unsupported at the advertised ISOTOPE profile | [ACTOR Core](actor-core.json) |

The stateless pack covers request-local `src_text`, source isolation and JSON
bindings. Local RPC uses a fresh engine module for each request. Cross-node
RPC and source fetches went through the host adapter with two exact loopback
origins on its allowlist. The policy checks exercised a reachable but
unlisted hostname and a redirect from an allowlisted source origin. The
source fixture also rejected any forwarded owner credentials. A separate
run confirmed that the [default allowlist blocks outbound access](egress-policy.txt).

The [HTTPS fixture](https-fixture.txt) exercised metadata, anonymous and
wrong-account denial, stateless JSON with request source, paging and prompt
replies. The [pilot limits probe](pilot-limits.txt) exercised admission, session
limits, timeouts and the engine watchdog. [Image and fixture fingerprints](provenance.json)

## Reproduce

Build the candidate under a local tag using the N7 deployment instructions.
From the conformance repository, run the existing checkpoint launcher with
its disposable peers enabled.

```sh
python3 reports/2026-11-08-n7-packaged-conformance/run.py \
  --demonstrator /path/to/trinity-demonstrator \
  --swi-load /path/to/swi-prolog-node/load.pl \
  --image trinity-eclipse-n7:conformance --allow-fixture-peers \
  --output /tmp/n7-conformance
python3 runner/validate_reports.py /tmp/n7-conformance
```
