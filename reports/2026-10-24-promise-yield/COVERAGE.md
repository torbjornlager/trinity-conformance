# Promise/yield draft 0.1 — 24 October 2026

Identical public-interface goals were run on disposable native SWI/Trealla nodes.
This separately versioned pack does not change baseline 0.1. GNU and SWI-WASM
network behaviour are **not measured**. No runtime code or installed engine was changed.

## Promise/yield selections

| Caller → HTTP peer | SWI | Trealla |
| --- | --- | --- |
| swi | [6 pass, 0 fail](swi-promise-yield-to-swi.json) | [6 pass, 0 fail](swi-promise-yield-to-trealla.json) |
| trealla | [5 pass, 1 fail](trealla-promise-yield-to-swi.json) | [5 pass, 1 fail](trealla-promise-yield-to-trealla.json) |

**22/24 assertions pass; 2 failures remain.**
Failures within this draft pack are not waived by separate diagnostic controls.

## Existing HTTP interoperability selection

HC-002 is reused for sharing/caller independence; HC-001 retains its paging
assertion. **8/8 selections pass**.

| Caller → HTTP peer | SWI | Trealla |
| --- | --- | --- |
| swi | [2 pass, 0 fail](swi-interop-http-to-swi.json) | [2 pass, 0 fail](swi-interop-http-to-trealla.json) |
| trealla | [2 pass, 0 fail](trealla-interop-http-to-swi.json) | [2 pass, 0 fail](trealla-interop-http-to-trealla.json) |

## Separate diagnostics

PYD-001 (ordinary actor send), PYD-002 (unification-only timeout callback) and
PYD-003 (throwing callback followed by retry) all complete their assertions in
the four directions. Individual outcomes are listed below; they do not waive
required failures or establish an exact implementation cause.

- [swi → swi](diagnostics/swi-promise-diagnostics-to-swi.json): 3 observed, 0 diagnostic errors.
- [swi → trealla](diagnostics/swi-promise-diagnostics-to-trealla.json): 3 observed, 0 diagnostic errors.
- [trealla → swi](diagnostics/trealla-promise-diagnostics-to-swi.json): 3 observed, 0 diagnostic errors.
- [trealla → trealla](diagnostics/trealla-promise-diagnostics-to-trealla.json): 3 observed, 0 diagnostic errors.

## Required failures

- **PY-002 — trealla → swi**: ConformanceFailure: expected success, got {'type': 'error', 'pid': 1456735128, 'data': 'error(existence_error(procedure,(!)/2),(!)/2)'}; preceding events were [] [report](trealla-promise-yield-to-swi.json).
- **PY-002 — trealla → trealla**: ConformanceFailure: expected success, got {'type': 'error', 'pid': 1476557048, 'data': 'error(existence_error(procedure,(!)/2),(!)/2)'}; preceding events were [] [report](trealla-promise-yield-to-trealla.json).

## Provenance and limits

Native SWI source is the demonstrator manifest pin
`f316e65503bff863dfbd2e182f7487988c91480c`; Trealla uses the separately built
unmodified v3.14.10 engine and matching libraries. Exact Web Prolog source
revisions, commands, binary hashes and fixture configuration are in
[provenance.json](provenance.json). Both fixture pairs were stopped after use.
Read [REPORT.md](REPORT.md) for method, schema/accounting checks, preservation
and the timing-fixture qualifications. No full-suite, GUI, GNU, browser-network,
TLS, cancellation or general lifecycle certification is claimed.
