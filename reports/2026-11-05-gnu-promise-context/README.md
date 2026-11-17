# GNU request/root promise ownership and retirement

All **six maintained groups pass** on clean GNU commit recorded in
[verification](verification.json). No runtime code changed. The tests run in
`make -C isobase promise-context-test` and the normal `local-test` selection.
The [full local suite](local-suite.txt) passes with the new selection included.

| Case | Checked behavior |
|---|---|
| GCTX-001 | Anonymous fresh HTTP requests cannot collect/dispose an explicitly retained query's promise; the origin resumes and collects. |
| GCTX-002 | The same checks with equal bearer authentication show that authentication alone does not retain execution ownership. |
| GCTX-003 | Idle retirement reaps the execution processes and closes pending transport before a controlled producer attempts its late response; fresh collection is denied and capacity recovers. |
| GCTX-004 | Stopping a standalone root query closes its pending connection before late completion. |
| GCTX-005 | Explicit root cleanup preserves a later promise and leaves the old transport closed before late completion. |
| GCTX-006 | Actual GNU-to-GNU RPC forwarding grants no collection or cleanup authority at the other node; the originating retained query still collects. |

[Final results](final.json) record request/continuation responses, references,
producer counts and retirement observations. Request-arrival and release barriers
control ordering. A producer observes socket EOF before its forced late response;
retired execution processes stay absent. These are bounded deterministic
schedules, not an exhaustive proof for every possible race.

The isolation cases also create a foreign worker's own promise and collect its
own answer. This candidate emits equal numeric references in the independent
workers, demonstrating why equality does not grant cross-context authority. The
tests do not require future implementations to choose equal reference numbers.
Explicit retention uses the query-owner capability and the next paging offset;
it does not turn an arbitrary new HTTP query into the old execution context.

The [first run](first.json) passes retirement/root checks but fails two fixture
end-state checks. Its origin retry skipped an offset, correctly starting a fresh
query rather than resuming the cached continuation. The fixture now resumes the
next offset and checks exactly one originating producer request. The
[second run](second.json) passes all six cases; the clean final invocation repeats
them without retries or deadline changes.

The ledger now maps B-296 within GNU's ISOBASE/standalone/retained-page boundaries.
These tests do not certify all promise/yield mode or formal-error requirements,
GNU ACTOR features, or Linux jail/public transport behavior. B-004/B-354 retain
partial evidence pending the remaining profile-conditioned clause mapping and
retirement/continuation attachment race controls.

Binary/source/compiler hashes and the unchanged engine revision are recorded in
verification. Public nodes, owner policy, credentials and consumer pins were not
changed. Text logs have trailing whitespace normalized; JSON is unchanged.
