# Client-context lifetime audit

This audit splits B-004, B-354 and B-296 of the pinned Appendix B manuscript into
individual obligations. It qualifies development sources, not public deployment
pins. The [qualification report](../reports/2026-11-05-context-lifetime/README.md)
records inputs, commands, original fixture failures and results.

The native evidence below uses **both** SWI and Trealla. `CTX` and `CP` identify
public-API cases in the [maintained manifest](../cases/retained-context-0.1.json).
`LIFE-NAMES`, `LIFE-OWNERSHIP` and `LIFE-LIFECYCLE` identify executed implementation
regression selections in that manifest. The SWI selections load the full node
composition. Native attachment tests use barriers at the retirement decision,
with deliberately unsafe negative controls in disposable source copies.

| Clause | Native evidence and assertions reviewed |
|---|---|
| B-004: the environment establishes an interaction's context | CTX-001–002, CTX-010–011: retained WebSocket clients and fresh authenticated/anonymous HTTP requests have the intended boundaries. LIFE-OWNERSHIP checks trusted standalone and HTTP owners. |
| B-004: local descendants retain the association | CTX-001, CTX-009: child promise collection and ordinary-name lookup. |
| B-004: remote descendants retain the association | CTX-013–015 on all four directed native routes: destination siblings share ownership; unrelated clients do not. |
| B-004: names and promises are scoped at each node | CTX-002–003, CTX-006–009, CTX-014–015; LIFE-OWNERSHIP checks identical namespace identities on distinct node scopes in SWI, and trusted/client isolation in both runtimes. |
| B-004: equal credentials do not merge contexts | CTX-002 and CTX-010; the independent retained clients deliberately share credentials. |
| B-004: cross-request reuse requires explicit retention | CTX-010–011 versus CTX-004–005. CTX-020 additionally exercises SWI's HTTP session interface; Trealla retention is exercised through WebSocket sessions. |
| B-004: one request ending or a toplevel replacement does not close a retained context | CTX-004–005; LIFE-NAMES and LIFE-OWNERSHIP check retained namespace and promise lifetimes independently of a toplevel. |
| B-004: returning descendants rejoin the origin despite transport/engine changes | CTX-016–017 on SWI→SWI, SWI→Trealla, Trealla→SWI and Trealla→Trealla; LIFE-NAMES checks connection replacement and origin reattachment. |
| B-354: closure ends ordinary-name admission | LIFE-NAMES: retired names disappear, late registration and named creation fail, and another client's names remain. |
| B-354: closure ends promise admission | LIFE-OWNERSHIP/LIFECYCLE: pending and ready state is retired, collectors wake with missing references, and creation from surviving actors is rejected. |
| B-354: late creation/publication cannot reopen scopes | LIFE-NAMES pauses source preparation before publication. LIFE-OWNERSHIP/LIFECYCLE explicitly deliver completion after committed closure; state and queues remain absent. SWI also pauses creation after admission checking. |
| B-354: concurrent attachment joins before retirement or is rejected after it | ATTACH-REJOIN-FIRST and ATTACH-ATOMIC in both runtimes. ATTACH-NEGATIVE must reproduce the unsafe ordering when retirement is moved outside the lock. |
| B-354: closed scopes alone do not terminate surviving actors | LIFE-NAMES and LIFE-OWNERSHIP/LIFECYCLE retain live actors and execute further commands after scope retirement. Transport shutdown may separately terminate actors; that is not treated as scope-only closure. |
| B-354: standalone execution has an environment-provided root | LIFE-OWNERSHIP: trusted standalone actors share promises, while public clients cannot borrow trusted ownership. LIFE-NAMES preserves trusted names when a client scope closes. |
| B-296: promises belong to their creating node and context | CTX-001–002, CTX-013–015, LIFE-OWNERSHIP; owner identity comes from execution context rather than a supplied reference. |
| B-296: references work independently of engine placement | CTX-001, CTX-004–005, CTX-017; parent, child, replacement shell and returning descendant collect from the original owning context. |
| B-296: same-context code may collect or dispose; another context cannot | CTX-001–003 and CTX-014–015; LIFE-OWNERSHIP checks foreign cleanup leaves the owner's result collectible, including trusted/client separation. |
| B-296: forwarding a reference does not confer access at another node | CTX-019 on all four routes directly forwards an origin reference to a destination descendant, checks collection denial and harmless cleanup there, then collects successfully at the origin. LIFE-OWNERSHIP additionally checks node scopes. The transport/source review confirms references carry no owner mutation; access is resolved against the executing node/context. A reference can independently identify that recipient's own promise; numeric equality is not authority. |
| B-296: authentication alone grants no access | CTX-002, CTX-010, CTX-014; CP-001 supplies pending/ready foreign denial and owner retry with equal client credentials. |
| B-296: across-request collection requires explicit retention | CTX-010–011 versus CTX-004–005, and SWI CTX-020. |
| B-296: ownership transfer is unsupported | Reviewed native creation/access paths derive ownership from execution context, with no public transfer operation. CTX-002–003 and CTX-014–015 show that sending a reference or attempting foreign cleanup does not transfer authority. |

These assertions support whole-source-unit verification for **native SWI and
Trealla within these execution boundaries**. Tests check selected deterministic
orderings; they do not prove absence of every possible concurrency defect.

## Browser/native transport qualification

The [browser/native report](../reports/2026-11-05-browser-native-context/README.md)
adds 44 passing real-Chrome observations: eleven cases in each browser mode
against both native runtimes. BN-002/003/005 check forwarding in both directions,
same-context collection and foreign cleanup/closure isolation. BN-004 returns a
native request to an existing browser child, which resolves its original name
and collects its original context's promise in that engine. BN-008 exercises
actual native HTTP RPC/promise values and sharing through a fixture proxy.
BN-006/007/009/010/011 cover acknowledged scope closure, actor survival, raw late
creation, forged lineage, reconnect denial and delayed-handshake admission.

Together with the maintained local browser ownership selection, this maps every
B-296 clause within the named browser/native execution boundaries. The scope
close hook now confirms retirement at connected peers without terminating their
existing actors. Unsupported peers or connection loss reject confirmation.

Browsers have no advertised inbound node endpoint. A callback over an established
connection is tested; arbitrary native spawning of a new browser actor is not a
supported return path. The [extended qualification](../reports/2026-11-05-context-races-and-monitors/README.md)
adds BN-012 and BN-013 in all four browser/native combinations. BN-012 traverses
both native runtimes and returns to the original native scope before replying
to an existing browser child; each returning engine resolves its original name
and collects its original promise. BN-013 holds the real returning frame before
admission, commits origin closure, then checks rejection and absent state.

The complete browser B-004 mapping uses local child/name/promise ownership from
the maintained browser ownership selection, BN-002/003/004 for engine boundaries,
BN-005 for equal-authority client separation, the retained session API for
request/toplevel replacement, and BN-012 for native-to-native attachment/return.
B-354 uses BC-001–008 for local publication/admission barriers, BN-006/007/010/011
for acknowledged peer closure, surviving actors and delayed admission, and
BN-012/013 for return before versus after committed closure. The same native
admission locks have independent join-first/retire-first controls above. Browser
standalone initialization supplies its local root; no new inbound browser-node
facility is assumed. These assertions support scoped whole-unit verification
for B-004/B-354 in both browser modes.

## GNU ISOBASE request/root qualification

The [GNU report](../reports/2026-11-05-gnu-promise-context/README.md) adds six passing
maintained groups without a runtime change. Fresh anonymous requests and requests
sharing bearer authentication cannot collect/dispose a retained query's promise.
Only its explicit paging continuation resumes that worker's ownership. A separate
worker can collect its own answer even if reference numbers coincide. Actual
GNU-to-GNU RPC forwarding grants no access to the originating promise.

Idle retirement and standalone stop close pending transport before a forced late
response. Execution processes remain reaped, later fresh requests cannot collect
the old promise, and capacity recovers. Explicit root cleanup also permits a
later promise to complete. These assertions map B-296 within GNU's ISOBASE,
standalone and retained-page boundaries; they do not certify every promise/yield
mode or formal error.

The [GNU continuation controls](../reports/2026-11-05-context-races-and-monitors/gnu-races-final.json)
complete the applicable retirement ordering: continuation-first preserves the
original worker and pending producer; retirement-first closes the old producer
and a later request starts a new execution. The unsafe busy-guard mutation must
fail to preserve the active execution.

For B-004, GCTX-001/002/003 establish fresh anonymous/authenticated requests and
explicit retained-page ownership; GCTX-004 supplies independent-worker roots;
GCTX-006 verifies that RPC reference forwarding grants no origin ownership.
Only the explicit continuation resumes the original execution and promise state;
ending one page request leaves that retained execution open. For B-354,
GCTX-003/004/005 check idle/root retirement, late completion, absent old state,
transport teardown and resource recovery; the two GRACE orderings check that
continuation cannot reattach after committed retirement. Standalone cleanup
closes its promise root and later execution creates fresh state.

GNU advertises ISOBASE, so ACTOR child creation, ordinary-name registration and
surviving actor APIs are outside this target's public profile. Its HTTP RPC is a
new query interaction, not ACTOR descendant attachment. The mapping verifies
B-004/B-354 within GNU's request, retained-query and standalone execution model;
it does not certify an unadvertised ACTOR lineage facility. No new manuscript
rule was required: Appendix B already separates context closure, actor termination
and reference possession from ownership.


## Monitor observation ownership

The [monitor qualification](../reports/2026-11-05-context-races-and-monitors/README.md)
adds browser BN-014–016 and native deterministic controls. B-053 gains candidate evidence for owner-only
withdrawal, harmless foreign/unknown references and idempotence; its full
option/value/error mapping is still required. B-054 maps all
matching queued notifications, nonblocking flush and unrelated mailbox state.
B-055 maps the observation-owner confirmation barrier, queued-message retention
without flush, suppression after successful withdrawal, and declared connection
loss. Browser and Trealla timeout controls additionally require the exact formal
error, retained local record, no timeout flush and successful retry. The browser
control releases an old timed-out operation before retry and proves that it is
cancelled; it cannot erase the retained observation.

SWI's synchronous lifecycle mutex covers remote monitor selection, delivery and
withdrawal, so it has no asynchronous peer-confirmation timeout branch. Trealla
uses its serialized connection writer; the browser uses its coordinator's
observation filter and ordered engine channel. These are reviewed implementation
boundaries for the same public rule, not language exceptions. Remote loss and
additional/private-reference clauses B-049/B-050 gain candidate evidence, but
remain unverified until their complete clause inventories are mapped.
