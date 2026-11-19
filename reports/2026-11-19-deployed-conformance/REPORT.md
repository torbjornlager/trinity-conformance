# Full conformance run after the SWI-Prolog 11 upgrade — 19 November 2026

**The run is not all-green.** All **76 case manifests (1,973 main case rows)**
were exercised through the public nodes, disposable native fixtures, GNU's
ISOBASE API, embedded SWI-WASM and real Chrome sessions. Every main case ID has
execution evidence. Auxiliary attachment and browser/native return-barrier
controls could not start because their instrumentation no longer matches the
native source. This is therefore an incomplete qualification, not a release
certification or a language-conformance percentage.

The suite was frozen at `3c5315ca9e621ee97b6cc717c06fad87857d0fd0`.
[Input hashes](suite-inputs.json), the [per-file result index](SUMMARY.json) and
[case inventory verification](verification.json) make the selection reviewable.
Older library pack versions and repeated routes were deliberately included;
1,973 rows do not mean 1,973 independent features. Failures were retained as
written. No runtime source, assertions, live service settings or quotas were
changed to obtain passing results.

## Public and exact-image results

| Boundary | Fresh result | Limits |
|---|---|---|
| N0 RELATION | 1/1 error-admission case | Not full RELATION certification |
| N1, N2, N6 HTTP | 12/12 each | ISOBASE subset; does not qualify all ISOTOPE features on N2 |
| N6 error admission | 1/1 | Separate profile refusal check |
| N3 SWI ACTOR | 118/118 | 106 ACTOR + 12 HTTP |
| N4 SWI ACTOR | 118/118 | Same |
| N5 Trealla ACTOR | 118/118 | Same |
| N7 ECLiPSe ACTOR, first attempt | 106/118 | Twelve HTTP 429 upgrade refusals |
| N7 paced controls | 12/12 | Same assertions after 61 seconds quiet, 5 seconds between session starts; first failures remain |
| Directed public ACTOR interoperability | 36/36 | 3 cases × 12 directed pairs among N3/N4/N5/N7 |
| Additional public packs | 72/72 | 18 per ACTOR node: supervisor/worker diagnostics, terminal newline, text and wire capabilities; diagnostics are observations, not language qualification |
| Demonstrator tutorial | 1/1 on N3 | DEMO-019 |
| Exact deployed SWI N1/N3/N4 image, private fixture | 45/45 + 7/7 | actor-release-0.2 + source-directives |
| Exact deployed SWI N2 image, private fixture | 45/45 + 7/7 | Same runtime gate; fixture advertises ACTOR, unlike live N2 |
| Exact deployed Trealla N5 image, private fixture | 45/45 + 7/7 | Same; transport readiness checked |
| Runner unit tests | 111 passed | Tooling tests, outside case counts |

The private release fixtures use two independent execution-only principals and
are distinct from anonymous public transport tests. All three were removed,
along with their temporary network. Public primary files are under
[observations/observations](observations/observations); additional cases and paced
controls are under [public-extra](observations/public-extra). Exact-image gates
are under [isolated](observations/orchestration/isolated).

SC-001 now passes its current synchronous-startup expectation. The N5 callback
case RC-009, public prompt cases, and all directed interoperability cases pass
this selection. The [16 November report](../2026-11-16-deployed-conformance/REPORT.md)
remains unchanged: both suite expectations and deployed software have changed,
so this is not a controlled attribution of each difference to SWI 11.

## Native and browser results

All four standard-library pack versions were run across seven modes: SWI and
Trealla HTTP/WSS, GNU HTTP, SWI-WASM Worker and SWI-WASM main in Chrome.

| Selection | Native modes | Real Chrome Worker/main |
|---|---|---|
| standard-library-0.1, 112 cases | 560/560 | 224/224 + 2 child controls |
| standard-library-0.2, 146 cases | 730/730 | 292/292 + 2 child controls |
| standard-library-0.3, 289 cases | 1,445/1,445 | 578/578 + 2 child controls |
| standard-library-0.4, 295 cases | 1,475/1,475 | 590/590 + 2 child controls |
| Receive guard controls | 16/16 | 16/16 |
| Bounded library noncompletion | Trealla/GNU pass; SWI fails entry control | Both pass |
| Maintained monitor shared cases | 94 pass / 4 fail | 94 pass / 4 fail |
| Native monitor withdrawal barriers | 2/2 | Not a browser claim |
| Source directives, embedded WASM | Not applicable to this column | 5 pass / 2 unsupported per mode |

The complete native and embedded selections include boolean validation,
creation and policy boundaries, source/callback context, naming, selective
receive, node settings, errors, partial pages, URI handling, RPC deadlines,
HTTP fields, statechart documents, promises, text, interoperation and diagnostics.
Use [SUMMARY.json](SUMMARY.json) for every file's raw status counts instead of
summing repeated and auxiliary runs into one denominator.

The browser package is `0363b38b3d4939a53f62a57b23fbc4e73997e79f`.
Its engine remains **SWI-Prolog 10.1.19**, swipl-wasm 8.2.5; the SWI 11 upgrade
was native. Tests used Linux Node 22.23.4 and Chromium 156.0.8078.79.
Embedded observations use the adapter's coordinator, while real Chrome tests
use the packaged session API. Neither alone certifies the public browser UI.
SD-006/007 now require `goal_sandbox`; their unsupported WASM status follows the
current manifest, rather than converting the earlier failed observations.

## Findings requiring follow-up

- **Retained context:** the 61-row matrix (55 manifest rows plus six controlled
  promise rows) records **39 pass, 18 fail, 4 blocked**. Failures include foreign
  cleanup, cross-context handling, remote return and controlled promise paths.
  The six closure controls pass. The six attachment controls did not execute:
  `local_attachment_race.py` raises `instrumentation boundary changed` before
  producing results. The overall context gate stays red.
- **Monitor contract drift:** MC-028/029 fail on SWI, Trealla and both WASM modes.
  These older cases require rejecting string/list node URIs, whereas the current
  URI pack accepts text representations. Source-aware native reruns reproduce
  the four native failures; shared real Chrome execution reproduces four more.
  The strict remote monitor group also stops before execution because
  `return_barriers.py` cannot find its source instrumentation needle. Passing
  native barriers do not compensate for this missing group. A supplementary
  uninstrumented browser/native context run completes with **27 pass / 33 fail**
  across 60 observations. It excludes the four BN-013 return-barrier cases and
  does not satisfy the strict 64-observation selection.
- **Browser API differences:** source-aware Chrome reruns retain ER-008
  (unregistered-name error), LN-002/005, B-SV-006 and ten of twelve receive
  callback cases per mode. Copying isolation, node settings, server waits and
  source copying pass after their helper source is loaded. Separate preflight
  sessions additionally fail MC-005. Embedded receive-wait and delayed-send
  failures remain evidence about that adapter boundary, including missing
  coordinator hooks; they are not automatically runtime defects.
- **Boolean boundary:** the 234 direct `native_goal` assertions selected from the
  boolean pack produce **202 pass / 32 fail per embedded WASM mode**.
  The derived manifest selects the original `native_goal` field as `goal`;
  its exported bytes are distinct from the hashed source manifest. This is
  distinct from query-rejection wire validation. Native resource-preservation
  controls pass; diagnostics remain separate from normative validation.
- **Native URI, deadline and HTTP differences:** native node-URI I/O records
  12 pass / 14 fail, including missing replies and transport-lineage refusals.
  The seven-case local-node RPC pack passes on SWI/GNU and fails all seven on
  Trealla. Generic native RPC-timeout cases record 34 pass / 6 fail; HTTP options
  record 112 pass / 6 fail. A standalone API rerun records 299 pass / 24 fail
  across its selected packs. These boundaries have different admission and
  fixture contexts; the observations do not isolate every failure to the engine.
- **Supporting transport/document fixtures:** HTTP field forwarding passes
  66/66. RPC timeout fixtures record 61 pass / 20 fail; statechart document
  fixtures record 1 pass / 9 fail, including missing relative document fetches.
  Portable-text 0.2 records 24 pass / 2 fail on each native engine, with
  `invalid_prompt_ref` on TXT-019/026. HTTP prompt tests pass 19/19 on SWI;
  Trealla returns HTTP 404 on all 19 selected cases. GNU direct API comparisons
  retain six URI failures and two HTTP zero-timeout controls.
- **SWI noncompletion evidence is invalid for its target:** the warmup passes,
  but `entry_count` is zero rather than one. This is a failed entry control,
  not proof that countall terminates or fails to terminate. The externally
  bounded Trealla/GNU and Chrome observations pass their controls.

Diagnostic JSON parse errors in the generic ISOBASE diagnostic adapter are
retained as diagnostic failures, not counted as language validation failures.
Required, supporting, diagnostic and browser-specific packs must be interpreted
in their own declared scope. The report does not treat a browser compatibility
expectation run on native engines as a native ACTOR obligation.

## Fixture corrections and incomplete controls

Initial native monitor execution overwrote per-case helper source with common
pack source. Its 22 failed rows remain archived; the existing source-aware
adapter reduces this to the four URI expectation failures. Initial embedded
browser execution ignored per-case source. These attempts remain indexed and
were followed by source-aware real Chrome runs without changing assertions.
Receive callback failures persist in the source-aware runs.

Initial promise setup hit Git's dubious-ownership check in the copied suite.
After allowing that owned snapshot directory, the maintained promise selection
and diagnostics ran successfully. Fixture setup repair is not an implementation
change. The strict attachment and return-barrier instrumentation failures were
not repaired by weakening the gate; they remain explicitly incomplete.

## Provenance, preservation and reproduction

Native SWI source is `26e1ce7d712afafe440e3f87388baec4490232ec`, on
SWI-Prolog **11.0.0**. The demonstrator upgrade is `dc66d8c…`; deployment notes
are `b14feb3`. [provenance.json](provenance.json) records exact deployed and lab
image IDs, browser payload hashes, engine versions and synthetic snapshot IDs.
Trealla/GNU sources in the labs came from the deployed images. Their Git
repositories were initialized solely for adapter provenance; those synthetic
IDs are not upstream commits.

Because Docker Desktop did not permit these host bind mounts, frozen suite and
runtime files were copied into owned Docker labs. Broad tests ran with network
`none` and loopback fixtures; the private release gates used an owned temporary
network. No production service was restarted, rebuilt or reconfigured.
[Preservation checks](preservation.json) confirm all baseline Compose container
IDs and image IDs stayed unchanged. This checks identity/images, not every
mutable value inside a service.

[Orchestration scripts](orchestration) and [execution plans](execution) preserve
commands, routes and timeouts. They contain machine-specific paths and require
the named private images/runtime package; they are a record, not a turnkey
public CI job. The original private run artifacts remain at
`trinity-demonstrator/.trinity/conformance-full-20261119`. Exported observations
omit credential files, private fixture programs and verbose node logs;
authorization/query-owner header values and fixture tokens are redacted.
Assertions and input hashes remain unchanged. The [file hash index](files-sha256.json)
protects the exported record. Historical reports retain their original scope.
