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

## Browser evidence and remaining tests

The maintained real-Chrome promise selection exercises both modes: parent/child
and sibling access, creator exit, collector interruption, replacement queries,
foreign contexts with equal numeric references, harmless foreign cleanup,
closure cancellation/wakeup, rejected late creation and surviving actors. The
new completion barrier resolves a request after closure has committed and checks
that neither state nor a claim reappears.

That evidence does not yet close these complete source units:

- B-004: directly combine ordinary-name isolation, retained shell replacement,
  and remote descendant return with browser/native transports. Establish which
  return paths are possible under the advertised inbound-connectivity capability.
- B-354: the [browser name-closure repair](../reports/2026-11-05-browser-name-closure/README.md) now qualifies ordinary-name retirement, pending
  startup rollback, late publication/commit denial, committed-actor survival,
  isolation, late URI-source completion without child leaks, and synchronous disposal admission. Browser/native context
  attachment and closure propagation still need direct transport controls;
  coordinator-only barriers do not certify those remote paths.
- B-296: qualify browser/native reference forwarding in both directions and the
  remote authentication boundary. Two local runtime instances and a simple HTTP
  answer fixture do not establish every remote context-admission rule.

Both browser whole-unit statuses remain unverified. The ordinary-name lifecycle
gap found in this audit is repaired; the remaining transport items are concrete
missing evidence, not observed implementation failures.

## GNU ISOBASE evidence and remaining tests

GNU provides outgoing promises within an ISOBASE worker. Its actor/session APIs
are outside its profile; native ACTOR test results cannot certify its request
boundaries. These three common units remain unverified pending direct tests of:

- authenticated and anonymous fresh HTTP requests attempting to collect and
  dispose of a reference from another request;
- worker/request retirement while an outgoing promise is pending, followed by
  a forced late completion and confirmation that resources remain reclaimed;
- standalone root ownership and forwarding an originating reference to another
  GNU/native node without granting access.

No new manuscript rule is needed for these findings. Appendix B already separates
context closure from actor termination and requires ownership to survive engine
placement and permitted transport changes.
