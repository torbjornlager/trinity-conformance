# Request isolation with OPEN exercises — 19 November 2026

The candidate isolates fresh HTTP computations even when credentials match,
while retaining sharing inside an explicit WebSocket or HTTP session. Its HTTP
and normal integration checks pass without adding a login requirement to OPEN.
**The stricter condition that every visible teaching query finishes remains
unmet:** the exercise run retains ten timeouts, all reproduced on unchanged
OPEN source. The candidate remains uncommitted and unpublished pending the
exercise-condition choice. No running node or production dependency pin changed.

## Candidate behavior

SWI now gives each stateless HTTP computation a fresh internal lineage and
uses that lineage for its promise owner key. It keeps the principal's existing
resource-account identity, so equal credentials still aggregate quotas. Local
descendants inherit the computation context; separate requests cannot collect
or dispose of its references. Retained WebSocket and HTTP-session namespaces
continue to take precedence. The Trealla HTTP-session repair from the
[preceding investigation](../2026-11-19-http-context/REPORT.md) remains selected
in this candidate.

The links exercise exposed an existing owner-only restriction on `link(false)`.
The SWI candidate permits declining a parent link inside a live retained client
namespace, while preserving client ownership and quota accounting. It grants
no node-owner authority. Stateless HTTP and public execution without an open
retained namespace still cannot use it to leave unlinked work behind. Tests
cover real actor ownership and rejection after namespace closure; the actual
anonymous links sequence and a parent-termination survivor control pass.

Example 19 already collects its timeout retry in one query. Its source comment
now describes explicit retained sessions for sharing across queries. That is a
comment-only update after execution; the exercised program is unchanged.

## Passing checks

- [Fresh-request/local context selection](fresh-requests.json): **23/23 pass**.
  The [old SWI control](old-swi-http-control.json) retains 22 pass / 1 fail,
  including the original authenticated-request sharing result.
- The exact three-case HTTP-session selection passes with both
  [anonymous clients](http-anonymous.json) and
  [equal execution credentials](http-authenticated.json): **6 executions pass**.
  Anonymous clients retain individual visitor cookies where required; they send
  no authorization header. The producer-arrival/release and foreign-cleanup
  controls remain active.
- Native LINT, T0, T1_NATIVE, T2, T3_NATIVE and T5 pass. The final T4_NATIVE run
  passes all **1,095 named tests**, plus the origin and HTTP visitor controls.
  The initial broad run retained one obsolete authenticated-sharing expectation;
  its test was deliberately revised for the accepted candidate contract and
  T4 was rerun. Both logs remain available.
- The demonstrator's normal test wrapper passes T1_INTEGRATION,
  T3_INTEGRATION, T4_INTEGRATION, DEMONSTRATOR, SERVICE_TEXT, LINDA, MODEL,
  MODEL_SXML and JEV. Service tests use owned fake backends, including public
  OPEN WebSocket flows; no live provider credentials are required.
- All **114 conformance runner unit tests pass** with Node 22.23.4.

The consumer tests use private verification worktrees and exact candidate pins.
Browser schema provenance requires matching native revision metadata, so a
private browser metadata commit/package was generated as well. Its engine and
all runtime/schema file hashes match the original package. Normal dependency
validation remained enabled. Public pins and the default setup still select
native `26e1ce7` and browser `0363b38`.

## Strict OPEN exercise result

The new consumer tool fetches the real catalogue and source anonymously, applies
the drawer's current curation, and executes its actual query sequences on owned
OPEN loopback nodes. Public node/source URLs are mapped to local fixtures.
Documented deliberate failure/error examples retain those expected outcomes.
Whole-query deadlines also cover WebSocket ping/pong frames.

The checks visited **20 visible Prolog entries and 14 visible statechart entries**.
Across **131 observations**, 121 pass and ten time out. Five later fridge
queries were not executed after the recovery step failed; this is not a claim
that every query was completed.

| Flow | Candidate timeout | Unchanged OPEN control |
|---|---|---|
| Parallel example 13 | Queries 1, 2 and 3 | Same three; the source explicitly documents its flawed mailbox/cleanup algorithm |
| Fridge example 16 | Query 6, crash/restart | Same query |
| Statechart examples 01, 02, 08, 09, 11 and 12 | Their final `statechart_halt/3` query | Same six queries |

The public observations are [Prolog entries](open-actor-exercises.json),
[statecharts](open-statechart-exercises.json),
[parallel baseline](parallel-baseline.json),
[fridge baseline](fridge-baseline.json) and
[statechart baseline](statechart-baseline.json). The failure signatures match by
source path, query number and terminal timeout type. This establishes that the
new HTTP contract did not introduce those failures; it does not diagnose their
exact runtime cause or relabel them as passes.

The first driver attempts exposed two fixture problems: an arbitrary event-count
limit rejected ordinary philosopher output, and placeholder substitution scanned
inside quoted XML comments. The driver now uses a 15-second wall deadline and
substitutes query placeholders before inserting XML source. Those attempts stay
private. The Prolog export is the actor subset of the earlier mixed run, which
stopped at the XML fixture issue; the corrected separate statechart run covers
all fourteen chart entries. Baseline controls use the corrected reader.

The five currently hidden Prolog entries and six hidden statecharts are outside
this drawer selection. Their service/inference boundaries receive additional
coverage in the normal consumer suites; this report does not claim exhaustive
interactive completion of hidden entries or real model-provider behavior.

## Reproduction and next decision

Run against the recorded candidate inputs:

```sh
python3 tools/test_open_exercises.py --swipl /path/to/swipl \
  --native-root /path/to/native-candidate \
  --runner /path/to/trinity-conformance/runner/run.py --output /fresh/open-report
```

Use `--only 'actors/13 parallel.pl'`, `--only 'actors/16 fridge_server.pl'` or
`--only statecharts/` for the unchanged-source controls. The tool starts and
stops its own loopback fixtures; it has no live-endpoint option.

For HTTP sessions, add `--anonymous-http-sessions` to the command in
[the session profile](../../profiles/http-session-context-0.1.md). Omitting
remote routes from the original context adapter runs the 23-observation local
selection. It is not a rerun of the full retained-context release gate.

The remaining choice is whether the user's OPEN condition requires fixing the
existing exercise failures before publication, or preserving anonymous access
while tracking them separately. No unrelated failure is being silently excluded
from a green all-exercises claim. The raw records and candidate patches are
ready for review before that choice.

[Summary and input hashes](SUMMARY.json), [private candidate identifiers](private-candidates.json),
[native patch](native.patch), [Trealla patch](trealla.patch),
[consumer patch](consumer.patch), [adapter patch](conformance.patch) and
[export hashes](files-sha256.json) identify this checkpoint. Private worktrees,
initial attempts and fixture logs remain under
`trinity-demonstrator/.trinity/open-http-20261119`. Runtime versions are SWI 11.0.0
and Trealla 3.14.20 with its matching library; browser engine 10.1.19 is unchanged.
The network-isolated mixed-runtime Docker lab is removed after export.
