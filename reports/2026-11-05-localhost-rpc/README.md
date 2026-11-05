# Localhost RPC and promise repair — 5 November 2026

This records the development-stage qualification before promotion. The repair
was subsequently committed, pinned and deployed in the [public runtime repair
release](../2026-11-05-public-runtime-repair-release/README.md).

Appendix B retains the atom `localhost` as the current node for `rpc` and
`promise`. Native SWI already resolves it. Trealla now obtains its own listener
from private node-layer metadata, independently of its advertised public URL.
User source cannot replace that metadata. GNU obtains its listener from trusted
controller metadata; ordinary workers retain normal outbound-policy checks.

Contained GNU workers use a reserved broker route to the fixed local stateless
`/call` endpoint. They gain no arbitrary loopback access, source endpoint or
administration route. Controller credentials remain in the broker. Root-owned
leases now carry both IP budget and client identity. Continuation owners are
derived from the trusted client identity and per-call nonce, preventing cache
reuse across clients sharing an IP budget. Controller and broker must be
promoted together because their lease protocol changed.

All **21 shared assertions** pass on disposable SWI, Trealla and GNU nodes.
They exercise local paging, temporary source isolation, promise variable sharing,
failure/error answers and caller-fetched URI sources. All **7 contained N6
assertions** pass with real Linux workers and the actual broker. Those include
the reported query, unchanged:

```prolog
rpc(localhost, ancestor_descendant(X,Y),
    [src_uri('https://n2.elfenbenstornet.se')]).
```

It returns six ancestor/descendant pairs. The matching promise form returns the
same six pairs and leaves the caller's goal variables unbound.

Trealla's full unit and interoperability suites pass. GNU's complete RPC suite
passes in explicit candidate comparison mode; credential/environment isolation,
four egress and eight adapter unit tests, real TLS checks, the contained N6
public contract and Linux containment checks pass. Egress and adapter regressions
are now included in the pinned consumer CI plan, whose runner tests also pass.
The complete consumer CI matrix has not been rerun for this development batch. The interop runner copy uses
one-second startup waits for the released x86 engine; its initial 0.2-second
startup race is retained. The historical GNU comparison lock correctly refuses
the newer consumer checkout; that attempt is retained separately from the
successful candidate qualification.

The Linux test images are explicitly developmental: the build overlays three
identified GNU source files and the changed consumer broker on committed bases.
They are not release artifacts and must not be used as dependency pins.
The tests preserve the rejection of `Host:Port` terms. URI source handling and
external peer egress restrictions are unchanged.

[verification.json](verification.json) records source hashes, development image
identities, qualification boundaries and evidence hashes. The exact development snapshots remain recorded here; the promotion report
identifies the committed sources and clean release images.
