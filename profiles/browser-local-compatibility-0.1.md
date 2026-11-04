# Browser local compatibility 0.1

This supporting selection preserves the documented browser API while testing the
same registration and dynamic-child behavior as LN-002, LN-006 and SV-006.
It is separate from the native manifests and does not waive their exact outcomes.

Browser registration collisions use `permission_error(register,actor_name,Name)`.
Browser supervisor listings contain `child(Id,Pid,OriginalSpec)`, rather than the
native `info(Id,Pid,Type,Restart)`. Specs cross messages as copies, so comparison
uses variant equivalence to preserve structure and variable-sharing relationships.
The goals still require collision rejection before startup, preservation of the
original actor and siblings, successful retry, message routing and monitor cleanup.

Run `adapters/wasm.cjs PACKAGE worker|main cases/browser-local-compatibility-0.1.json REPORT`.
Each case runs in a fresh process; manifest source is loaded before the assertion.
The Node coordinator is a transport fixture, not a browser/network attestation.
