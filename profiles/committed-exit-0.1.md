# Committed exit 0.1

An actor's explicit exit or accepted termination signal commits its termination
reason. Catching an exception cannot revoke that decision and resume mailbox
operations, including a nonblocking receive's timeout callback. An ordinary
caught exception permits further execution.

The four query cases in `cases/committed-exit-0.1.json` exercise these boundaries
without naming an engine's private unwind token. Each observation uses an
explicit failure callback on a missed deadline. They do not claim that an
arbitrary computation without runtime safe points can be forcibly interrupted.

This pack extends the scoped gate to **actor-release-0.2**, 44 cases per engine.
The previous 40-case `actor-release-0.1` manifest remains available through the
release runner and local adapter's `--profile` option. Run only on disposable
private loopback fixtures; see `adapters/local_actor_release.py --help`.
