# Trealla HTTP client-context follow-up

The unchanged baseline 0.1 fixtures run on disposable loopback nodes against
the working-tree repair identified by [source hashes](repair-inputs.json).
The installed engine and live N3/N5 are unchanged. See [coverage](COVERAGE.md),
[provenance](provenance.json), and the [preceding source-loading run](../2026-10-21-http-source-loading/COVERAGE.md).

Required selections now pass **93/94**, up from 87/94. All six Trealla HTTP
client cases (RPC paging and promise sharing against SWI, Trealla and GNU)
pass. The GNU-to-Trealla promise case remains a failure without a waiver.
The unparenthesized operator-fragment diagnostic is unchanged. The runner
therefore still exits nonzero; this is not an all-green certification claim.
All 39 reports pass schema/accounting validation. Supporting native ACTOR
contracts remain 66/66 and both real SWI-WASM local adapters retain 7/7.

## Repair and regression scope

The HTTP node loads the full RPC module before extending its ownership hook.
On Trealla 3.13.10, creating the hook first can leave the module incomplete.
Source-free sandbox guards use an internal HTTP context: execution resolves
through `node`, while database guards keep their existing `user` scope. Thus
RPC/promise/yield also resolve inside `catch/3` and guarded calls without
moving clause inspection or mutation into node bookkeeping.
Private-source guards retain their actor context. Client implementations,
option validation, sandbox admission, ownership and public protocols are unchanged.

Source-free producers now use the terminal wait already used for private-source
producers. The existing request scope owns teardown after final/error replies;
normal actor exit no longer races that monitored stop. This is a local HTTP
producer integration change, with no general actor lifecycle or cancellation repair.

`tools/test-http-client-context.py` starts fresh processes through both `node.pl`
and `distribution.pl` in blacklist and whitelist modes, without preloading RPC.
It checks 80 public HTTP assertions covering nested RPC, promise templates and
sharing, callbacks/retry, errors, disposal, ownership, private sources and
sandbox/module-qualification denial, database isolation and profile boundaries.
The final 80-case matrix passed three complete runs.
Existing promise correctness, lifecycle, ownership, client-option, source-loading,
HTTP paging cleanup/deadline, sandbox and profile regressions also passed.

## Separate exploratory observation

An exploratory immediate-disposal request produced this error once:

```
error(permission_error(mutex_unlock,not_locked_by_me,'$rpc_promise_lifecycle'),mutex_unlock/1)
```

The probe was `promise(Peer,true,R),promise_cleanup(R),catch(yield(R,_),E,true)`
inside a whitelist HTTP request with the RPC module available. Its cause has not
been established. The client-context regression allows completion before explicit
disposal; existing lifecycle regressions still exercise pending-worker disposal
and pass. This observation is retained as a separate concurrency diagnostic,
not silently treated as repaired by client availability or attributed upstream.
No promise-locking implementation was changed in this batch.
