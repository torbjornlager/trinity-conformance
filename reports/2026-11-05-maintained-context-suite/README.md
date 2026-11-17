# Maintained context selection — 5 November 2026

The first invocation of `runner/context_release.py` passes on unchanged native
SWI `c826111` and Trealla `62e93c3` source checkouts. No live services, runtime
implementations, pins or policy are changed by this work.

- [51 context observations](contexts/results.json): all pass across the full
  four-route matrix, without blocked cases, errors or exclusions.
- [Attachment controls](attachments/results.json): four positive observations
  and two successful negative controls on disposable source copies.
- [69 runner self-tests](runner-tests.txt): all pass, including five new gate
  rejection tests for missing/duplicate/unexpected cases, nonpassing statuses,
  policy exclusions, route omissions and negative-control identity.
- [Strict gate result](results.json): both groups pass on their first invocation.

The [manifest](../../cases/retained-context-0.1.json) preserves the audit IDs and
requirement associations. The [profile](../../profiles/retained-context-0.1.md)
defines this supporting selection, its reproduction command and limits. This
promotion adds a durable strict gate, not 51 newly discovered semantic assertions.
The six implementation race observations remain separate from black-box cases.

Appendix B was clarified in the author's existing working manuscript: retained
context lifetime/closure and remote return; the exactly-one-document exception
to additive source loading; an ownership example; and separate source, destination
and admission permissions. Existing manuscript work was preserved. The PDF rebuild succeeded and the
five affected pages were rendered and visually checked; [validation](book-validation.json)
records file hashes. The ledger
continues to validate against its pinned manuscript snapshot; these edits do not
silently migrate its source-unit hashes or promote whole-unit verification.

The public N5 timeout and browser CI interruption failure in the
[preceding release](../2026-11-05-cluster-peer-policy/README.md) remain unresolved.
No deadline, retry policy or runtime code was changed to qualify this gate.
Additional controlled producer, closure/late-completion and interruption schedules
remain future tests, as distinguished in the profile.
