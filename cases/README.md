# Candidate conformance cases

No cases in this directory are normative or executable yet. The following is
the initial extraction backlog, grouped by the minimum advertised profile.

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

Before implementation, each item must receive a stable ID and an exact wire
or API contract. Existing implementation tests are evidence for defining the
contract, not the contract itself.
