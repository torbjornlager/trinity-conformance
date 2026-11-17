# Standard-library release — 5 November 2026

**Committed, pushed and deployed to N0–N6.** All twelve runtime and asset services
run clean images built from consumer commit `1b04f278f12b2572a2071dc9d3ba163aa23736ff`.

Appendix B's required library forms and callback semantics now work consistently
across native SWI, Trealla, GNU and both browser modes. Missing higher `maplist`
forms and `countall` are supplied automatically; GNU also supplies the required
`memberchk` and `forall`. Trealla retains private callback scope, cut scope and
remote source export while applying the current sandbox policy.

Library callbacks validate when invoked: uninstantiated values raise
`instantiation_error`; invalid values raise `type_error(callable, Value)` with
the original culprit. Empty iteration and vacuous `forall` tests do not invoke
unused callbacks. Application exceptions propagate unchanged. ISO `call/N`
retains its existing runtime-specific error refinement; its shared control checks
only the accepted category and culprit, while library cases require exact callable errors.

- **112 shared cases** cover every required predicate and arity, positional
  callback arguments, relational modes, binding isolation, cuts, exceptions,
  lazy callbacks and exact callable errors.
- **786/786 committed-source observations** pass: 560 checks in five runtime
  modes, 224 retained-session checks and two browser child controls.
- Native SWI and GNU full regression suites pass. Trealla passed **89 unit and 71 interoperability groups** before the nested
  follow-up; the final repair reruns all 89 unit groups and adds **239 library
  and sandbox controls**. The Linux N5 candidate passes **238 individual, nested
  and batch controls**. The clean browser package passes **seven groups**.
- All **36 pinned consumer CI groups** pass. The clean N6 image passes its public
  contract, 59 HTTP-field assertions, worker/broker checks and Linux containment.
- **2,379/2,379 public checks** pass: 672 shared assertions on N1–N6, 1,568 in
  real Chrome on N0–N6 across both modes, and 139 previous transport, localhost,
  ownership, asset and N5–N4 ping-pong regressions.

All services retain their environment fingerprint, runtime user, resource and
security controls, and persistent mounts. Existing admission configuration is
retained. Exact running pins were checked in all twelve services. Rollback images
are recorded in [rollback-images.json](rollback-images.json).

An initial public probe exposed premature `forall/2` test validation on N5
inside nested meta-calls. The final pinned repair guards both callbacks at
invocation and retains public source export. The failed probe and initial
deployment evidence remain in [initial-attempt](initial-attempt/); the final
release repeats image builds, pinned consumer CI, candidate gates and live checks.

The source-unit ledger remains at 11 verified units per runtime: this repair
strengthens the four required-library units rather than certifying the full ISO
mode/error inventory. Native retained-context propagation remains a separate audit.
The [earlier development report](../2026-11-05-standard-library/README.md) retains
the original 57-case baseline and subsequent 65-case qualification; its manifests
are historical and have not been replaced by the 112-case release selection.

[verification.json](verification.json) records pins, counts and evidence hashes.
