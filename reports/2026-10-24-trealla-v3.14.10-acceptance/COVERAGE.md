# Trealla v3.14.10 acceptance conformance — 24 October 2026

All **60 required selections and 66 supporting ACTOR assertions pass** on the disposable native SWI/Trealla fixtures. GNU and SWI-WASM were not rerun. Separate diagnostics are retained below.

Trealla engine: exact unmodified v3.14.10 `4ef56e3bbbcc6ca44085a4aa5eae0e6848c70294`, matching library, with the Web Prolog receive adapter using public `sig_atomic/1`. SWI engine: separate PCRE-enabled `09b6299f696574c9230f23e53b1ab041a942b6f3` build. Source revisions and hashes are in [provenance](provenance.json). Test cases and assertions are unchanged. Installed engines and N3/N5 were not restarted. This checkpoint is acceptance evidence, not an installed-runtime upgrade.

## Native selections

| Pack | SWI | Trealla |
|---|---|---|
| isobase-http | [10 pass](swi-isobase-http.json) | [10 pass](trealla-isobase-http.json) |
| language-actor | [7 pass](swi-language-actor.json) | [7 pass](trealla-language-actor.json) |
| wire-capabilities | [3 pass](swi-wire-capabilities.json) | [3 pass](trealla-wire-capabilities.json) |
| actor-core | [7 pass](swi-actor-core.json) | [7 pass](trealla-actor-core.json) |
| actor-workers | [8 pass](swi-actor-workers.json) | [8 pass](trealla-actor-workers.json) |
| actor-behaviours | [10 pass](swi-actor-behaviours.json) | [10 pass](trealla-actor-behaviours.json) |
| actor-supervisors | [8 pass](swi-actor-supervisors.json) | [8 pass](trealla-actor-supervisors.json) |

## HTTP interoperability

| Caller → peer | SWI | Trealla |
|---|---|---|
| swi | [2 pass](swi-interop-http-to-swi.json) | [2 pass](swi-interop-http-to-trealla.json) |
| trealla | [2 pass](trealla-interop-http-to-swi.json) | [2 pass](trealla-interop-http-to-trealla.json) |

## ACTOR interoperability

| Caller → peer | SWI | Trealla |
|---|---|---|
| swi | [3 pass](swi-interop-actor-to-swi.json) | [3 pass](swi-interop-actor-to-trealla.json) |
| trealla | [3 pass](trealla-interop-actor-to-swi.json) | [3 pass](trealla-interop-actor-to-trealla.json) |

## Separate diagnostics

| Pack | SWI | Trealla |
|---|---|---|
| isobase-diagnostics | [6 observed](swi-isobase-diagnostics.json) | [5 observed, 1 diagnostic_error](trealla-isobase-diagnostics.json) |
| supervisor-diagnostics | [4 pass, 1 fail](swi-supervisor-diagnostics.json) | [5 pass](trealla-supervisor-diagnostics.json) |
| worker-diagnostics | [1 pass](swi-worker-diagnostics.json) | [1 pass](trealla-worker-diagnostics.json) |
| portable-text | [7 fail](swi-portable-text.json) | [7 pass](trealla-portable-text.json) |

These reproduce the previous checkpoint differences: SWI SCD-001 nested runtime-bound child admission fails with instantiation_error; Trealla IBD-006 unparenthesized HTTP operator goal times out (incomplete evidence); experimental character-list Portable Text fails 7/7 on SWI and passes 7/7 on Trealla. None is relabelled as a required pass.

Peer trust uses the endpoint-specific [fixture](peer_transport_fixture.pl) with a public test token granting execute/internal_transport on the disposable Trealla peer. Open execution alone grants no lineage authority. See the recorded launch commands.

## Reproduction and limits

Exact per-run commands and exit statuses for all thirty reports are recorded in [provenance](provenance.json). The original orchestration script is not included; its exit 0 was not an all-packs-pass claim. All thirty reports passed runner/validate_reports.py schema/accounting validation. The runtime tracked-tree hashes and engine hashes match before and after.

These selected assertions do not certify full language compliance, hostile-input security, TLS, arbitrary policies, browser runtime behaviour or lifecycle race freedom. Separate full-suite and real-UI evidence lives in trealla-port/reproducers/receive-handoff-acceptance-2026-10-23/REPORT.md.

## Execution accounting

| Invocation | Scope | Exit | Evidence |
|---|---|---|---|
| trealla-isobase-http | required | 0 | [report](trealla-isobase-http.json), [log](trealla-isobase-http.log) |
| trealla-isobase-diagnostics | diagnostic | 1 | [report](trealla-isobase-diagnostics.json), [log](trealla-isobase-diagnostics.log) |
| trealla-language-actor | required | 0 | [report](trealla-language-actor.json), [log](trealla-language-actor.log) |
| trealla-wire-capabilities | required | 0 | [report](trealla-wire-capabilities.json), [log](trealla-wire-capabilities.log) |
| trealla-actor-core | supporting | 0 | [report](trealla-actor-core.json), [log](trealla-actor-core.log) |
| trealla-actor-workers | supporting | 0 | [report](trealla-actor-workers.json), [log](trealla-actor-workers.log) |
| trealla-actor-behaviours | supporting | 0 | [report](trealla-actor-behaviours.json), [log](trealla-actor-behaviours.log) |
| trealla-actor-supervisors | supporting | 0 | [report](trealla-actor-supervisors.json), [log](trealla-actor-supervisors.log) |
| trealla-supervisor-diagnostics | diagnostic | 0 | [report](trealla-supervisor-diagnostics.json), [log](trealla-supervisor-diagnostics.log) |
| trealla-worker-diagnostics | diagnostic | 0 | [report](trealla-worker-diagnostics.json), [log](trealla-worker-diagnostics.log) |
| trealla-portable-text | experimental | 0 | [report](trealla-portable-text.json), [log](trealla-portable-text.log) |
| swi-isobase-http | required | 0 | [report](swi-isobase-http.json), [log](swi-isobase-http.log) |
| swi-isobase-diagnostics | diagnostic | 0 | [report](swi-isobase-diagnostics.json), [log](swi-isobase-diagnostics.log) |
| swi-language-actor | required | 0 | [report](swi-language-actor.json), [log](swi-language-actor.log) |
| swi-wire-capabilities | required | 0 | [report](swi-wire-capabilities.json), [log](swi-wire-capabilities.log) |
| swi-actor-core | supporting | 0 | [report](swi-actor-core.json), [log](swi-actor-core.log) |
| swi-actor-workers | supporting | 0 | [report](swi-actor-workers.json), [log](swi-actor-workers.log) |
| swi-actor-behaviours | supporting | 0 | [report](swi-actor-behaviours.json), [log](swi-actor-behaviours.log) |
| swi-actor-supervisors | supporting | 0 | [report](swi-actor-supervisors.json), [log](swi-actor-supervisors.log) |
| swi-supervisor-diagnostics | diagnostic | 1 | [report](swi-supervisor-diagnostics.json), [log](swi-supervisor-diagnostics.log) |
| swi-worker-diagnostics | diagnostic | 0 | [report](swi-worker-diagnostics.json), [log](swi-worker-diagnostics.log) |
| swi-portable-text | experimental | 1 | [report](swi-portable-text.json), [log](swi-portable-text.log) |
| trealla-interop-http-to-trealla | required | 0 | [report](trealla-interop-http-to-trealla.json), [log](trealla-interop-http-to-trealla.log) |
| trealla-interop-actor-to-trealla | required | 0 | [report](trealla-interop-actor-to-trealla.json), [log](trealla-interop-actor-to-trealla.log) |
| trealla-interop-http-to-swi | required | 0 | [report](trealla-interop-http-to-swi.json), [log](trealla-interop-http-to-swi.log) |
| trealla-interop-actor-to-swi | required | 0 | [report](trealla-interop-actor-to-swi.json), [log](trealla-interop-actor-to-swi.log) |
| swi-interop-http-to-trealla | required | 0 | [report](swi-interop-http-to-trealla.json), [log](swi-interop-http-to-trealla.log) |
| swi-interop-actor-to-trealla | required | 0 | [report](swi-interop-actor-to-trealla.json), [log](swi-interop-actor-to-trealla.log) |
| swi-interop-http-to-swi | required | 0 | [report](swi-interop-http-to-swi.json), [log](swi-interop-http-to-swi.log) |
| swi-interop-actor-to-swi | required | 0 | [report](swi-interop-actor-to-swi.json), [log](swi-interop-actor-to-swi.log) |
