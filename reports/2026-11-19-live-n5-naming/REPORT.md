# Live N5 naming deployment — 19 November 2026

N5 now runs Trealla port **6041ea3** and image
`sha256:f6773633b01d2f8f0a337b4de15c09e85aedee4a9c46206692beaa7c3dbaa26e`.
Ordinary names are client-context scoped; published services remain node-wide.
The Trealla engine remains 3.14.20.

The live [eight naming checks](live-naming.json) pass **8/8**. All eight deployment
smoke groups pass: 36 versioned case executions across naming, HTTP, local
naming, ACTOR core and N5→N3 interoperability; three Linda checks; and N5→N1
source loading plus N5→N2→N4 nested RPC. All 34 local consumer integration groups
and both [upgrade CI jobs](https://github.com/torbjornlager/trinity-demonstrator/actions/runs/44543224917)
passed for consumer commit `33ca0d9`. The separately committed SWI cleanup fix
`dc93b05` is not deployed by this release.

The [deployment record](https://github.com/torbjornlager/trinity-demonstrator/blob/6320ae3298c21ac168a899c3c8a087a80a9826fa/docs/verification/n5-client-naming-2026-11-19/verification.json)
contains source/image identities, preservation checks and recovery details.
The first cutover automatically restored its predecessor after a smoke script
sent the legacy actor-core pack to the wrong runner. No actor-core assertion
ran in that failed step. The corrected runner passed 7/7 on the isolated exact
image before the separately sealed second attempt reran every live check.
All failed/setup attempts remain private and intact.

Credentials, volumes, peer files, network identity, limits, health configuration
and Caddy were preserved. Other persistent services retained their container
and image identities. Predecessor→candidate→rollback was rehearsed using an
owned state volume, with its marker preserved across all three phases. No live
writable state was used by that rehearsal. The selected model and guarded
recovery procedure are named in the shared deployment record.

This is a targeted deployment verification. The full retained-context suite's
HTTP-principal, remote ownership and round-trip findings remain open; this
record does not claim a complete rerun or a green full context gate. The
[full run](../2026-11-19-deployed-conformance/REPORT.md),
[first repair batch](../2026-11-19-conformance-repairs/REPORT.md) and
[pre-deployment naming qualification](../2026-11-19-client-naming/REPORT.md)
remain unchanged historical evidence.
