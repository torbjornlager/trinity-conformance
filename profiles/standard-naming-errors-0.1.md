# Standard registry and required-option errors

Appendix B.9 uses `error(Formal,Context)`. Ordinary-name conflicts now use
`permission_error(register,actor_name,Name)`; a pid already ordinarily named uses
`permission_error(register,process,Pid)`. The same forms apply to pending name
reservations, named creation and publication, including remote publication.
The context is implementation-defined. Rejection preserves the existing name,
output variables, pending ownership, and the ability to retry after cleanup.

Missing child starts use `existence_error(option,start(Id))`, where `start(Id)`
identifies the required start option of child `Id`. Missing named synchronous
toplevel targets use `existence_error(actor_name,Name)` on both native hosts.

Run `cases/standard-naming-errors-0.1.json` and `cases/local-naming-0.1.json`
through `adapters/local_runtime_contracts.py` on both native candidates in
blacklist, whitelist and owner-off. Run the updated child-spec selection too;
its existing whitelist admission limitations must be reported independently of
formal-error checks. Native naming/reservation/race/remote-publication tests and
full interop qualify the producer changes beyond these public query examples.

The new selection also verifies that explicit application exceptions retain
legacy-shaped terms and their own contexts. No blanket boundary conversion is
permitted. Normal `down/3`, timeout results and library reply codes are unchanged.
Lifecycle, transport-loss and wait-timeout exception families remain a separate
contract review: this change does not relabel connection loss as process death.
