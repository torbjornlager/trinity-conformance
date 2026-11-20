# Node identity, copied I/O and client contexts — version 0.2

The author-directed contract treats `https://node/` and `https://node` as one
canonical node identity for actor routing, peer credentials and owner topology.
Only an empty root path is normalized. Schemes, authorities, explicit ports,
non-root paths, queries and fragments remain distinct. Duplicate canonical
credential entries and conflicting endpoint mappings are rejected.

An implicit local spawn retains the caller's client context. An explicit node
URL uses a receiving transport context, including a URL back to the same server.
Ordinary names remain client-context scoped; published services are node-wide.
An equivalent address does not restore an earlier caller namespace.

[cases/node-uri-io-0.2.json](../cases/node-uri-io-0.2.json) retains the original
source fixture and versions the mixed address/visibility assertions in
NU-001/002/004. NU-014–019 check visibility, ordinary names, retained-toplevel
halt and foreign control independently. NU-020 proves alias lookup by actual
delivery through the returned handle, without assuming the handle equals the
peer's internal PID. NU-021/022 check fresh anonymous and equal-credential
clients addressing the same canonical peer: independent ordinary names,
delivery to both actors, foreign exit denial, termination and baseline recovery.
The two clients need not share a socket.

Every ordinary case uses a fresh retained ACTOR toplevel; the client isolation
cases use two fresh connections. Output is acknowledged, expected messages have
throwing deadlines and a fresh query must succeed afterward. Disposable peers
use real owner-installed transport credentials, configured once per canonical
node. The adapter records source, adapter and manifest hashes, and tears down
its fixtures. No production settings are changed.

```sh
python3 adapters/node_uri_io.py \
  --swipl /path/to/swipl --tpl /path/to/tpl \
  --output /tmp/node-uri-io-v02-results
```

The adapter defaults to this manifest. To replay the old contract explicitly,
pass `--manifest cases/node-uri-io-0.1.json`. When testing older runtimes with
literal credential keys, add `--literal-peer-credentials` to authorize both
spellings; canonical-key runtimes reject those duplicate entries. The old case
file, profile and reports remain historical evidence.

The [native qualification](../reports/2026-11-20-canonical-uri-qualification/REPORT.md)
is local candidate evidence. It does not establish live adoption or browser,
ECLiPSe or GNU conformance to this selection.
