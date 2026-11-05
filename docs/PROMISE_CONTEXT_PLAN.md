# Context-wide promise ownership repair

Implemented in development sources on 5 November 2026. Appendix B makes the
key `(node, client context, reference)`, independently of engine placement.
Each browser runtime instance now owns one coordinator registry shared by its
main engine, shell Workers and spawned actors. Separate runtime instances are
separate client contexts, including when numeric references coincide.

The original opt-in parent/child diagnostic now passes. Upstream regression
scenarios and a real Chrome suite cover cross-engine collection/disposal,
creator exit, collector interruption, retained shell replacement, expiry, late
completion, equal references in foreign contexts, and closure/admission rules.
The browser suite uses a real local HTTP fixture. These changes are not deployed.

## Ownership design

- The page coordinator must establish the trusted client-context identity from
  actor/session lineage. Query code must not select a context by supplying a key.
- Keep one registry per context at the browser node. Creating and collecting
  engines are clients of that registry. A reference's meaning cannot depend on
  which engine happens to receive it.
- Preserve separate-context denial. A reference from another context is missing;
  matching numbers in different contexts do not confer access. Existing isolated
  engine fixtures remain useful negative controls for distinct root contexts.
- Allocate references without reviving old references within a live context.
  Check active entries and retain sufficient retired-reference history. A page-
  global store without context authorization would violate the same contract.
- Claims are owned by collecting actors, not creating engines. Only one claim
  exists at a time. Interruption or engine death releases that actor's claim
  without consuming a ready answer or destroying a context-owned promise.
- Commit selection before output matching. Cleanup/expiry winning first wakes
  collectors with a missing-reference error. Late completion cannot recreate
  a disposed entry. Preserve the existing timeout callback and answer semantics.
- Closing a context retires all its entries and transports. Finishing an actor
  or one toplevel in a retained context must not close the context. Ending an
  engine must release its waits; surviving context members retain their entries.
- Disposal may abort local transport resources. It does not promise remote
  cancellation or terminate surviving actors.

## Acceptance coverage

Use the same public Prolog assertions wherever possible: parent creates/child
collects; child creates and exits/parent collects; siblings collect and dispose;
foreign context cannot collect or dispose; context closure wakes collectors;
creator engine exits while the context stays open; collector interruption and
replacement; expiry/disposal/result races; no reference collision or revival;
and main-to-Worker/Worker-to-main transitions. Include pending and ready answers,
variable sharing, failure, exceptions and supplied output-pattern mismatch.

Coordinator claim/release messages must handle teardown without awaiting during
Prolog cleanup. Keep the existing cleanup guarantees while adding cross-engine
access. The upstream browser suite repeats these ownership/lifetime controls through
the public session API in real Chrome, including both main/Worker directions.
This qualifies development sources; release pins and public rollout are separate.

Native context propagation and retained HTTP contexts need their own reviewed
case mapping; this browser design does not certify those implementations.
