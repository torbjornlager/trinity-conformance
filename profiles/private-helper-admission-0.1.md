# Validated private helpers

The twelve portable cases run unchanged against native SWI and Trealla in
blacklist, whitelist and owner-off modes via `adapters/local_runtime_contracts.py`.
They cover alternatives, sharing, ordered/constructed/copied source, receive
callbacks, binding rollback and scoped dynamic updates. Expected messages have
throwing deadlines. HA-011 checks a maplist closure in the validated private
source context.

The Trealla runtime admission fix is required before enabling this selection.
SU-020 in the successor pack is checked in whitelist too. Completed call/N
arity admission also enables SU-019 and SU-HTTP-019 there; no successor rows
remain deferred. The native library callback fixes are required for HA-011.

`adapters/trealla_helper_transport.py --tpl /path/to/tpl --root /path/to/trealla-port
--output /tmp/helper-transport` additionally checks the actual Trealla WebSocket
boundary in whitelist. Its loopback source server records fetches: ownership,
call-option rejection, unknown/bootstrap helpers and unsafe child goals must be
checked before source work; fetched bodies remain validated. The report hashes
all local runtime Prolog sources and the engine, so exported test copies work
without a Git checkout. These are port-specific transport checks alongside the
shared semantic cases, not a claim of cross-runtime error-text equivalence.
