# Browser context-wide promise ownership

Development repair, 5 November 2026. Release pins and public nodes are unchanged.

Each browser runtime instance is a client context with one coordinator-owned
registry. Main, shell and child Workers share it. Separate runtime instances
remain isolated even with equal reference numbers. Worker code cannot select
another registry through a context key.

Creator exit and retained shell replacement preserve pending and ready answers.
Collector interruption/death releases only that actor's claims. Ordered Worker
messages keep setup, release and explicit cleanup non-suspending; creation,
waiting and commit await the coordinator. Context closure disposes entries,
wakes waiters, cancels local transports and closes admission without itself
terminating surviving actors. Reference history prevents revival. Local transport
cancellation does not guarantee remote computation cancellation.

The original parent/child diagnostic now passes unchanged (`worker.json`). The
upstream real-browser suite exercises both main/Worker directions, sibling access,
creator exit, competing collectors, killing collectors, query interruption,
shell replacement, timeout/retry, output mismatch, variable sharing, remote
failure/error answers, foreign contexts with equal references, access-time expiry,
late HTTP completion, context closure and further-admission denial. It uses
real Chrome engines, public session/Prolog APIs and a real local HTTP fixture;
expiry advances an entry deadline to check access-time expiry without waiting
five minutes. Closure additionally inspects the registry's wake/cancel effects.

`package-manifest.json` identifies all tested development inputs. The recorded
runtime diff includes the preceding uncommitted introspection repair. The final
suite passes all six groups, including **102 semantic scenarios**,
**13 new coordinator assertions**, **59 new browser ownership checks** and
**81 existing browser session checks**. `verification.json` records results and hashes.
The consumer smoke explicitly selects the development package; consumer release
pins and source-validation guards are unchanged.

Earlier diagnostic attempts are retained separately. The first regression run
found a fixture missing the newly required release method and one supervisor
startup assertion that passed on rerun. An unused-context disposal attempt found
that closing an unused registry must not instantiate the factory; the repair
now marks it closed and creates a closed store only if later accessed.
These earlier attempts do not qualify the final source package.

The [coverage ledger](../../docs/APPENDIX_B_COVERAGE.md) removes the previous
browser ownership failure/missing annotations. Its grouped ownership paragraph
remains unverified as a whole: these browser controls do not certify all remote
admission/authentication paths or native retained-context propagation.
