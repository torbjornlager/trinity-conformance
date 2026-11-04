# Common RPC HTTP fields — 4 November 2026

Appendix B and the development runtimes now share the closed HTTP option schema:
`request_header(Name=Value)`, `authorization(basic(User,Password))`,
`authorization(bearer(Token))`, and `user_agent(Agent)`. Values accept atoms,
strings and character-list strings, including empty and Unicode values. Names
are ASCII HTTP tokens. Text fields use UTF-8 bytes; Basic credentials use UTF-8
then Base64. All occurrences are validated before source work. First-field
precedence is case-insensitive and crosses authorization/user-agent aliases.
Fields apply to each RPC page and promise request, never to source downloads.

Reserved proxy identity fields remain protected. The GNU allowlist retains its
pinned Host field and operator-bound credential precedence. Its worker/broker
protocol adds an optional headers field; the updated broker independently
validates it. An older broker rejects custom fields explicitly. Deploy a matching
pair before relying on this feature in contained workers.

## Verification

- **361 HTTP field checks pass:** 295 identical validation assertions across
  five execution modes, plus 66 captured HTTP requests/scenarios across the
  three native engines.
- **141 timeout regression checks pass:** 60 shared assertions and 81 live
  checks, including the rebuilt GNU HTTP controller.
- Native LINT, TEXT, T0, T1_NATIVE, T2, T3_NATIVE and T4_NATIVE pass; T4 has 1053
  cases. Final focused native and Trealla field checks pass.
- Trealla full unit and SWI/Trealla interoperability suites pass. The retained
  interop runner increases only fixture waits to 1 second for the released x86
  Trealla executable.
- Final packaged WASM statechart, schema, mailbox, standalone and all **99**
  selected semantic scenarios pass. Native integration is covered separately;
  the package's native schema pin is retained.
- GNU HTTP/supervisor, URI, Boolean, source, wire, TLS, policy and credential
  regressions pass. Broker handler and TLS verification checks pass locally.
- The full book builds successfully in a temporary output directory.

[verification.json](verification.json) records source and evidence hashes,
counts and qualifications. Initial failures and stale test fixtures are retained
in [diagnostics](diagnostics/). Broad native/Trealla runs precede the last
representation-edge fix; the final shared/live and focused checks cover that fix.
Browser HTTP checks use real WASM APIs with mocked Fetch. Linux containment,
a deployed worker/broker pair, dependency promotion and full Appendix B
conformance remain outside this verification. No live deployment or pin changed.

The Worker promise parser also now reads a fresh term before matching a supplied
answer pattern, matching main-thread behavior. A misplaced GNU HTTP-controller
timeout flag from the preceding batch was fixed and its live regressions rerun.
