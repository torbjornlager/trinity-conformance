# Retained context 0.1 — maintained native conformance selection

This draft promotes the 51 native retained-context audit probes and adds six
controlled producer cases in a strict,
repeatable selection. It is not a new advertised node profile or complete
Appendix B certification. Case IDs and requirement mappings are preserved in
[the manifest](../cases/retained-context-0.1.json).

The same black-box operations run against both native runtimes. Five disposable
listeners provide independent retained WebSocket clients, fresh HTTP calls,
explicit retained HTTP sessions, and four directed native route combinations:
SWI→SWI, SWI→Trealla, Trealla→SWI and Trealla→Trealla. Trealla's two endpoints
are separate local nodes; the public N5 self-route remains a separate deployment
check. Execute-only clients share credentials intentionally; peer credentials
are separately provisioned for the disposable fixtures.

| Cases | Required observable behavior |
|---|---|
| CTX-001–005 | Local descendants and replacement toplevels share retained promises; unrelated clients cannot collect or dispose of them. |
| CTX-006–009 | Ordinary names isolate clients, propagate to descendants, and survive foreign unregister attempts. |
| CTX-010–011 | Equal credentials and anonymous fresh HTTP requests do not retain promise ownership between requests. |
| CTX-020 | An explicit retained HTTP session preserves ownership between requests and isolates another session. This transport fixture currently runs on SWI only. |
| CTX-012–015, CTX-018 per route | Remote transport and public goal export work; remote siblings share destination context while other clients remain isolated; foreign collection leaves the owner's promise intact. |
| CTX-016–017 per route | Returning descendants rejoin the origin's name and promise scopes. |

## Routine gate

```sh
python3 runner/context_release.py \
  --swipl /path/to/swipl --tpl /path/to/tpl \
  --swi-root /path/to/swi-prolog-node --trealla-root /path/to/trealla-port \
  --output /fresh/report/directory
```

This command runs all 57 cases and the existing attachment regression adapter
once each. It checks the exact candidate/case inventory and all four routes.
Missing, duplicate, unexpected, blocked, excluded and failed observations cannot
qualify. A nonzero adapter exit cannot qualify even if its report contains only
passing rows. Both groups run so an early failure does not hide the other group's
observations. There is no automatic retry, deadline enlargement or failure masking.
Historical release packs remain unchanged.

The attachment group supplies four deterministic positive observations and two
negative controls on disposable source copies. Both orderings of reattachment
and retirement are checked. Each negative control must reproduce unsafe closure
when retirement is deliberately moved outside the decision lock. These are
implementation regression controls, reported separately from the 57 black-box
language observations; they are not six additional portable language cases.

Run the gate's own inventory/rejection tests with the routine runner checks:

```sh
python3 -m unittest discover -s runner
```

## Limits and unresolved evidence

The original remote collector retains its two-second wait and four-second reply
deadline. Six `CP-001-*` cases add explicit HTTP request-arrival and release
barriers, across all four native route combinations and one transport self-route
per runtime. Each case checks foreign denial while pending, an owner timeout
before release, foreign denial after release, successful owner retry, and a
missing reference after consumption. It also requires exactly one HTTP request.
The producer records arrival and response-flush times alongside each client phase.
A response flushed by the server is not asserted to be installed in the runtime;
owner retry retains the existing two-second deadline for delivery and collection.

The controlled peer replaces the promise's HTTP callee with a local fixture.
Self-routes exercise remote actor creation at the originating node, not the
public HTTPS proxy or the original N5 HTTP self-call. The
[public intermediate timeout](../reports/2026-11-05-cluster-peer-policy/public-contexts-repeat-timeout/results.json)
remains unresolved; no automatic retry, deadline change or runtime fix is claimed.
The [first extended run](../reports/2026-11-05-controlled-promise-suite/README.md)
records two SWI fixture admission failures. The corrected disposable SWI launchers
set both actor ceilings to 256 to accommodate the larger selection under the
shared test principal. Public settings are unchanged. The
[qualified run](../reports/2026-11-05-controlled-promise-suite-qualified/README.md)
retains the corrected configuration and all observations.
Native attachment instrumentation does not certify every context closure or
late-completion schedule. The browser interruption failure remains separate.

GNU ISOBASE and browser execution are outside this native selection. Source
policy denial controls, source-fetch counters, statechart documents, and browser
interrupted-wait controls retain their separate suites and evidence; this gate
does not claim to expand those contracts. Full lifetime/transport clause mapping
and additional deterministic schedules remain work to do.
