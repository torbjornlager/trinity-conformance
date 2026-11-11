# Native prompt reply regressions

Appendix B places `respond/3` in ACTOR. ISOBASE and ISOTOPE clients cannot use
it, including through a computed call. The transport's own `toplevel_respond`
command remains available for answering ISOTOPE input; it is a runtime bridge.

`runner/prompt_boundaries.py` tests the public `/call`, HTTP session and ACTOR
WebSocket paths. Each engine needs one disposable ACTOR node and one disposable
ISOTOPE node. Enable HTTP sessions on Trealla. The five PB cases check direct
and computed rejection in ISOBASE and ISOTOPE, followed by an actual ACTOR
self-reply round trip.

```sh
python3 runner/prompt_boundaries.py \
  --trealla-actor http://127.0.0.1:29090 \
  --trealla-isotope http://127.0.0.1:29091 \
  --swi-actor http://127.0.0.1:29092 \
  --swi-isotope http://127.0.0.1:29093 \
  --output /tmp/prompt-boundaries.json
```

The shared WebSocket selection checks that prompt metadata stays separate from
literal prompt data (PW-001), stale and missing references do not answer a later
prompt (PW-002), malformed input leaves the reference usable but dispatch
consumes it (PW-003), and dispatch consumes the reference even if the actor's
input pattern rejects the value (PW-004). Abort must recover that waiting actor.
`responded` acknowledges routing, rather than acceptance by the input pattern.

```sh
python3 runner/run.py --ws-url ws://127.0.0.1:29090/ws \
  --manifest cases/prompt-ws-0.1.json --report /tmp/trealla-prompt-ws.json
python3 runner/run.py --ws-url ws://127.0.0.1:29092/ws \
  --manifest cases/prompt-ws-0.1.json --report /tmp/swi-prompt-ws.json
```

Run the existing HTTP races as well. The HTTP client preserves visitor cookies
per endpoint; enable anonymous visitor identity on SWI when requesting the
ownership check. Native SWI and Trealla require prompt references by default,
including when an older client requests `prompt_correlation: false`.

```sh
python3 runner/prompt_http.py --trealla http://127.0.0.1:29090 \
  --swi http://127.0.0.1:29092 --visitor-ownership --output /tmp/prompt-http.json
```

Before the fixes, PW-003 failed on both native implementations. The four lower
profile PB cases also failed on Trealla. Passing SWI profile checks did not
excuse its separate replay defect. These cases use the same public assertions
for both implementations and do not depend on their internal predicates.
