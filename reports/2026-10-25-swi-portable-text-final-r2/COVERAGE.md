# Experimental SWI portable-text configuration — coverage

25 October 2026. Explicit SWI working-source overlay, separate SWI build and
separate Trealla v3.14.10 JSON Unicode candidate. **Not installed/deployed.**
Trealla retains its character-list defaults. SWI alone selects the experimental
configuration. Source hashes are in [provenance.json](provenance.json).

| Pack | SWI caller | Trealla caller |
|---|---|---|
| portable-text | [26/26 pass](swi-portable-text.json) | [26/26 pass](trealla-portable-text.json) |
| actor-core-0.1 | [7/7 pass](swi-actor-core-0.1.json) | [7/7 pass](trealla-actor-core-0.1.json) |
| language-actor-0.1 | [7/7 pass](swi-language-actor-0.1.json) | [7/7 pass](trealla-language-actor-0.1.json) |
| copying-isolation-0.1 | [6/6 pass](swi-copying-isolation-0.1.json) | [6/6 pass](trealla-copying-isolation-0.1.json) |
| actor-workers-0.1 | [8/8 pass](swi-actor-workers-0.1.json) | [8/8 pass](trealla-actor-workers-0.1.json) |
| promise-yield-0.1 | [6/6 pass](swi-promise-yield-0.1.json) | [6/6 pass](trealla-promise-yield-0.1.json) |
| toplevel-waits-0.1 | [6/6 pass](swi-toplevel-waits-0.1.json) | [6/6 pass](trealla-toplevel-waits-0.1.json) |
| interop-actor-0.1 | [3/3 pass](swi-interop-actor-0.1.json) | [3/3 pass](trealla-interop-actor-0.1.json) |
| interop-http-0.1 | [2/2 pass](swi-interop-http-0.1.json) | [2/2 pass](trealla-interop-http-0.1.json) |

**Portable text: 52/52. Required shared selections: 90/90.**
Where a peer is used it is the opposite implementation. These finite packs
are separate from broader native-suite diagnostics.

| Control | SWI text | Trealla text | Required shared checks |
|---|---|---|---|
| [Ordinary SWI readers, same JSON candidate](../2026-10-25-swi-portable-text-default-r2/provenance.json) | 4/26 | 25/26 | 90/90 |
| [Configured SWI, unmodified v3.14.10](../2026-10-25-swi-portable-text-unmodified-trealla/provenance.json) | 26/26 | 22/26 | Not rerun |

The unmodified-engine control retains four supplementary-Unicode JSON failures.
The ordinary-reader control retains SWI native-string differences and one
Trealla caller assertion about the SWI peer source convention.

## Separate diagnostics and untested areas

The final experimental T4 native run retains four assertions requiring native
strings or code-list literal terminals. T3 produced intermittent supervisor
fixture failures and a one-off SGML import diagnostic. Its fixed focused
comparison passes 3/3 processes per reader mode, but does not erase those
full-tier findings. The entire experimental native suite is **not green**.
See the native repository’s `docs/verification/portable-text-configuration-2026-10-25/DIAGNOSTICS.md`.

GNU/browser portable-text configurations, invalid encodings, performance,
opaque native-string extension fidelity and example migration remain outside
coverage. No deployment, dependency-pin update or language-profile adoption
is implied. Historical portable-text matrices remain unchanged.

[Preservation checks](preservation.json) cover source snapshots during this
definitive run, engine binaries/libraries, pin and live n3/n5 process identities.
