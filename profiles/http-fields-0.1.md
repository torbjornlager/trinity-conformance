# Native HTTP fields

This supporting selection checks Appendix B's request-field contract for
`rpc/3` and `promise/4`. It does not change execution or transport deadlines.
Run `cases/http-fields-0.1.json` with `adapters/local_runtime_contracts.py`
against both native candidates in blacklist, whitelist and owner-off modes.
The negative cases require caught formal errors and preserve caller variables.

Run the wire qualification separately:

```sh
python3 adapters/native_http_fields.py \
  --swi-root /path/to/swi-prolog-node \
  --trealla-root /path/to/trealla-port \
  --tpl /path/to/tpl --output /path/to/results
```

The disposable peer binds only to loopback. It inspects first-field precedence
across all three option forms, character lists, bearer credentials, UTF-8 field
bytes and UTF-8 Basic credentials. RPC pagination checks every execution request;
promises check the complete collected answer and cleanup. Execution fields must
not appear on source fetches. Every rejected wire case is followed by a valid
request in the same process; request counts distinguish recovery from rejected
source fetching or execution. Only synthetic tokens are used and recorded;
random runtime query-owner capabilities are excluded from the report.

A separate fresh trusted process loads `http_field_order.pl`. The fixture replaces
the URI resolver with a sentinel and checks both public entry points reject an
invalid shadowed field before reaching it, preserving goal/reference variables
and promise-state inventory. A valid request must reach the sentinel as a positive
control. Because resolution precedes source/DNS activity and promise allocation,
this checks earlier ordering independently of the HTTP counters. The fixture is
never loaded into public nodes or submitted as user source.

The runtimes share the field schema but keep their HTTP-library adaptation private:
SWI needs UTF-8 byte atoms for field serialization; Trealla's HTTP library already
writes UTF-8. These cases do not qualify GNU/WASM, TLS, redirect policy or the
separate whole-request timeout work.
