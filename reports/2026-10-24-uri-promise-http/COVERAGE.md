# URI candidate compatibility checkpoint

24 October 2026. Identical unchanged public-interface assertions on disposable
native SWI/Trealla fixtures. The URI candidates include the preceding Boolean
source patches; installed/live engines and the dependency pin are unchanged.

## Promise and yield

| Caller → HTTP peer | SWI | Trealla |
|---|---|---|
| swi | [6/6 pass](swi-promise-yield-to-swi.json) | [6/6 pass](swi-promise-yield-to-trealla.json) |
| trealla | [6/6 pass](trealla-promise-yield-to-swi.json) | [6/6 pass](trealla-promise-yield-to-trealla.json) |

**24/24 selections pass.**

## HTTP interoperability

| Caller → HTTP peer | SWI | Trealla |
|---|---|---|
| swi | [2/2 pass](swi-interop-http-to-swi.json) | [2/2 pass](swi-interop-http-to-trealla.json) |
| trealla | [2/2 pass](trealla-interop-http-to-swi.json) | [2/2 pass](trealla-interop-http-to-trealla.json) |

**8/8 selections pass.**

## Scope and evidence

The eight raw reports pass schema/count validation. New implementation URI
tests cover text forms, canonical atoms, early errors, shorthand and sharing;
they do not add shared case counts. Diagnostic packs, GNU shared baseline and
browser real-network interoperability were not rerun here. No older failed
observation is waived or silently replaced by this finite checkpoint.

[Provenance](provenance.json) records source revisions, working-tree hashes,
engine/library identities and exact commands. Both native candidates are
explicitly selected working trees: SWI base 786737f and Trealla base 7220bb5.
The SWI base remains a descendant of unchanged pin f316e65. All preservation
checks are true and fixtures stopped. See [REPORT.md](REPORT.md) for the audit.
