# Admission paths 0.1 — diagnostic comparisons

This pack investigates existing conformance failures; it does not add required
language behavior, modify baseline 0.1 or classify observed errors as passes.
The [ten probes](../cases/admission-paths-0.1.json) run identically on disposable
native SWI and Trealla ACTOR nodes under their existing blacklist configurations.

| Group | Literal/runtime comparison |
| --- | --- |
| Valid initial children | Valid one-child supervisor creation with an explicit blocking child and monitored halt. |
| Missing start | The same missing-start specification supplied directly or through an ordinary message. |
| Dynamic child | Both valid and missing-start additions, with literal terms or a receive-bound term. Runtime probes report whether admission already bound the receive variable. |
| Validation order | Unknown spawn option following a missing file URI, supplied literally or at runtime. |

The diagnostic capture runner records all sent command objects and decoded JSON
responses from transport negotiation through halt. The selected goal is prefixed
with self-message admission_probe_entered. After its terminal success/failure/error,
a follow-up query on the same persistent shell consumes that marker or reports
its absence with a zero-time poll. This avoids output callbacks, sleeps and private
runtime inspection. It is an observation of entry, not a timing measurement.

[Two separate controls](../cases/admission-marker-controls-0.1.json) throw an
ordinary exception or fail after the prefix; they check whether the marker is
retained across those execution outcomes. Each capture keeps unexpected transport
errors/incomplete follow-ups visible. The admission transport is allowed only in
diagnostic-scope manifests; ordinary conformance query behavior is unchanged.

In the runtime dynamic probes, PatternState reports the variable before data is
sent. If no message matches, the request is explicitly not dispatched. A resulting
successful query is merely an observation of that state, not successful child
creation. Invalid literal terms are caught where execution reaches their catch.

The generated diagnostic matrix is separate from required coverage. It retains
incomplete/missing cells, caught errors and undispatched requests explicitly.
Existing admission findings and required failures remain unchanged. This finite
run does not settle intended sandbox policy, prove complete isolation, exhaust
source handling or establish an engine bug. Only read-only source inspection is
used to explain observations. Any repair requires separate authorization.
