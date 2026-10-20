# Native SWI supervisor request monitor cleanup

Ordinary supervisor requests now scope their private monitor across sending and
waiting with `setup_call_cleanup/3`. Finalization removes and flushes that monitor
on success, output mismatch, exception or interruption. Public request/reply terms,
supervisor-down errors and the ten-second timeout after sending are unchanged.
The operation is not cancelled and a late reply remains in the mailbox.
`supervisor_halt/1` is unchanged.

Seven regressions exercise success, reply mismatch, original send exception,
missing-name errors with a queued private down, interrupted waiting, supervisor
death with a separate application monitor, and the real ten-second timeout
followed by late reply delivery. Three selected leak regressions fail against
the prior implementation and pass with the repair. The new suite passes both
standalone and under node composition, and passes the T3 empty-mailbox check.

Additional validation:

- Existing supervisor suite: all 19 entries pass, including halt ordering.
- Supervisor child-spec suite: all 26 entries pass and mailbox check passes.
- Node-composed cleanup, worker-ownership and lifetime-authority suites: all
  44 entries pass, including parameterized cases.
- Source and documentation diff whitespace checks pass.

The existing supervisor suite's final empty-mailbox check fails with
`down(actor(70),actor(70),kill)` after its assertions. The exact same residue
occurs against the prior supervisor implementation; it is a separate existing
suite/lifecycle diagnostic and was not hidden by draining unrelated messages.
The combined targeted T3 run therefore does not have an entirely green exit.

The shared HTML manual and Appendix B TeX source now state the common cleanup
contract once; implementation mechanics are in the native runtime README.
No PDF rebuild, deployment, live node restart, commit or push was performed.
