# Packaged N7 conformance checkpoint

Measured **ECLiPSe CLP 7.2.13**, advertised as a private **ISOTOPE** pilot.
Both runs used disposable copies of the N7 adapter and its Linux ARM64
engine image, with the production execution limits and container networking
disabled. The runners supplied synthetic owner headers directly to the
loopback adapter. [Image and fixture fingerprints](provenance.json)

| Selection | Outcome | Evidence |
| --- | --- | --- |
| Opt-in semi-stateful HTTP prompt pack | 17 passed, 0 failed | [PT-004 through PT-020](prompt-http.json) |
| Required stateless HTTP baseline | 7 passed, 3 failed | [ISOBASE HTTP](isobase-http.json) |
| Required cross-node HTTP baseline | 0 passed, 2 failed | [HTTP interop](interop-http.json) |
| Supporting localhost RPC and promises | 0 passed, 7 failed | [Local node RPC](local-node-rpc.json) |
| Exploratory stateless HTTP diagnostics | 6 observations | [Diagnostic responses](isobase-diagnostics.json) |
| ACTOR Core | 7 unsupported for the advertised profile | [ACTOR Core](actor-core.json) |

## Failed assertions

- **IB-006** sends `src_text` with a stateless call. N7 returned HTTP 400
  with “Unsupported stateless query parameter.”
- **IB-009** requests JSON bindings from `/call`. N7 returned HTTP 400
  with “Expected format=prolog.”
- **IB-010** tests request source isolation. Its setup request was rejected
  with HTTP 400 for `src_text`, so the source isolation assertion could
  not be reached. Its second request also expects JSON.
- **HC-001–002** and **LOCAL-001–007** returned `error(abort).` instead of
  the expected RPC or promise result. The disposable peer and source
  fixture were checked from the host before the run. The two cross-node
  cases and the URI-source cases also depend on outbound connectivity,
  which the packaged engine's network policy blocks. The localhost cases
  without a URI source failed as well.

The ACTOR Core runner classified its cases from the advertised profile.
The remote actor prompt pack and other WebSocket suites were outside this
checkpoint. The opt-in prompt pack covers stale, malformed, missing and
wrong-session replies, along with session recovery and retirement during
Abort and Halt races.

The [separate HTTPS fixture](https-fixture.txt) passed with real Caddy and
OAuth2 Proxy using a mock GitHub provider. It covered public metadata,
anonymous and wrong-account denial, owner answer paging and owner prompt
replies. The conformance checkpoint used local fixtures throughout.

## Reproduce

With the N7 engine image built and SWI-Prolog on PATH, run from the
conformance repository root.

```sh
python3 reports/2026-11-08-n7-packaged-conformance/run.py \
  --demonstrator /path/to/trinity-demonstrator \
  --swi-load /path/to/swi-prolog-node/load.pl \
  --output /tmp/n7-conformance
python3 runner/validate_reports.py /tmp/n7-conformance
```

The launcher returns a nonzero status when any measured assertion fails.
It uses the existing baseline and prompt assertions and records the
ACTOR Core runner's profile classification. The validator covers the
required and diagnostic baseline reports and ACTOR Core. The prompt pack
uses its own result format, and the local RPC report retains its
`supporting` scope, which the baseline schema cannot represent.

Run `python3 tools/test_n7_https.py` from the demonstrator repository to
reproduce the HTTPS fixture.
