# Conformance cases

[`actor-core-0.1.json`](actor-core-0.1.json) is the first executable case
manifest. Each entry has a stable ID, an observable requirement category, and
source-test provenance. `runner/run.py` maps those IDs to black-box protocol
procedures.

[`portable-text-0.1.json`](portable-text-0.1.json) is an independent opt-in
draft. Its `TXT-*` cases specify double-quoted text as a list of one-character
atoms in submitted goals, loaded source, DCGs, list operations, Unicode text,
and serialized-term round trips. The initial runner reaches those semantics
through an ACTOR session; this does not make the draft an implicit requirement
of every node already advertising `actor`.

The remaining extraction backlog is grouped by the minimum advertised
profile.

[`actor-behaviours-0.1.json`](actor-behaviours-0.1.json) is an opt-in,
black-box generic-server and supervisor suite. Its cases consolidate portable
semantics from the implementation-specific SWI and Trealla unit suites while
leaving runtime internals and implementation workarounds in their home
repositories.

## RELATION

- accepted advertised relation
- conjunction of advertised relations
- rejection of an unadvertised relation
- rejection of source loading and non-relational goals

## ISOBASE

- successful `/call` with template bindings
- multiple solutions and finite paging
- `once=true`
- logical failure
- goal exception
- malformed goal text
- Prolog and JSON response formats
- stable public `/node_info` profile metadata

## ISOTOPE

- session spawn and ownership
- call, next, and final-page signalling
- stop followed by session reuse
- abort of a running goal
- halt and lifecycle notification
- output delivery
- prompt/respond input round trip
- source loading and persistence across calls

## ACTOR

- remote spawn and normal completion notification
- one-way send driving a remote receive
- explicit exit reason propagation
- monitor and demonitor semantics
- bidirectional actor-message routing
- links and multiple monitors
- inherited terminal output and acknowledged delivery
- inherited prompt/respond input
- connection loss, cleanup, and reconnect behaviour

Before implementation, each remaining item must receive a stable ID and an
exact wire or API contract. Existing implementation tests are evidence for
defining the contract, not the contract itself.
