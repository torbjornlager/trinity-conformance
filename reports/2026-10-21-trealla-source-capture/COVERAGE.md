# Trealla ACTOR rerun — source-capture repair

2026-10-21. Scope: one disposable Trealla ACTOR node on loopback, pinned engine
v3.13.10 with its matching library. No live N3/N5 restart or engine replacement.

| Suite | Classification | Result |
|---|---|---|
| language-actor | required baseline selection | [7/7](trealla-language-actor.json) |
| wire-capabilities | required baseline selection | [3/3](trealla-wire-capabilities.json) |
| actor-core | supporting ACTOR contract | [7/7](trealla-actor-core.json) |
| actor-workers | supporting ACTOR contract | [8/8](trealla-actor-workers.json) |
| actor-behaviours | supporting ACTOR contract | [10/10](trealla-actor-behaviours.json) |
| actor-supervisors | supporting ACTOR contract | [8/8](trealla-actor-supervisors.json) |
| supervisor-diagnostics | separate diagnostic | [5/5](trealla-supervisor-diagnostics.json) |
| worker-diagnostics | separate diagnostic | [1/1](trealla-worker-diagnostics.json) |
| portable-text | experimental text | [7/7](trealla-portable-text.json) |

All 56 executed checks passed: 10 required local/capability selections,
33 supporting ACTOR checks, seven experimental text checks and six separate
diagnostics. These are scoped observations, not full interoperability or
language certification. HTTP interoperability, GNU, SWI and browser modes
were not rerun in this batch. No failures were reclassified or waived.

[NOTES.md](NOTES.md) records regressions and limitations.
[provenance.json](provenance.json) records source revisions, dirty paths,
executable/input hashes, fixture configuration and subprocess exits.
