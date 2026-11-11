# Finite pages and exceptions

Appendix B requires a finite page's ordinary solutions to precede a pending
exception. The following `next` delivers the exception; `stop` discards it.
HTTP `once(true)` delivers only the first slice and retains no continuation.
An exception before the first answer is immediate. Owner running-time exhaustion
is an error rather than a truncated success.

`cases/partial-page-errors-0.1.json` contains shared HTTP and WebSocket protocol
assertions. It checks short and exact full pages, nonzero offsets, offset skipping,
once, stop and subsequent session recovery. Omitted limits keep all-solutions
exception semantics, while even a very large explicit integer remains finite. The WebSocket cases control the
toplevel directly so that executing a test coordinator inside a submitted goal
does not introduce unrelated source or whitelist admission requirements.

The adapter also runs the existing ER-011–013 zero-divisor cases and ER-014–016,
which use computed denominators and require an unbound result and subsequent
successful arithmetic. All assertions run unchanged against native SWI and
Trealla. Both nodes are disposable loopback fixtures with a one-second owner
execution limit; the deadline case tests that owner limit, not request-specific
timeout tightening.

```sh
python3 adapters/local_page_errors.py \
  --swi-root /path/to/swi-prolog-node \
  --trealla-root /path/to/trealla-port \
  --swipl /path/to/swipl --tpl /path/to/released/tpl \
  --mode blacklist --output /tmp/native-page-errors
```

Repeat with `--mode whitelist`. The adapter uses public protocol replies,
checks the responding PID and page order, halts each successful session, and
stops both node processes in cleanup. It writes observations and manifest hashes
to the output directory. A negative-control run may select an unfixed Trealla
checkout without changing its files.
