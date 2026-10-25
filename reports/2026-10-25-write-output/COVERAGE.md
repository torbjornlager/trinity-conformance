# Actor write/1 repair checks — 25 October 2026

Identical public WebSocket goals and expected output are applied to disposable
native SWI and Trealla nodes. This is a focused repair checkpoint, not a new
baseline pack or a rerun of all cumulative conformance tests.

| Shared assertion | SWI | Trealla |
|---|---|---|
| Atom output | pass | pass |
| Explicit character-list output | pass | pass |
| Unicode atom output | pass | pass |
| Compound output | pass | pass |
| `call(write(abc))` | pass | pass |
| Computed complete goal through `call/1` | pass | pass |
| Helper in private source | pass | pass |
| Helper copied to child actor | pass | pass |
| Output survives goal backtracking | pass | pass |

**18/18 shared selections pass.** Two separate Trealla checks confirm direct and
runtime-computed `write/2` remain forbidden without producing output. Unit checks
cover blacklist/whitelist admission, inherited terminal delivery and variable
sharing. Existing Trealla sandbox, isolation and toplevel groups pass.

The candidate change rewrites `write(Term)` to the existing actor terminal bridge
used by `writeln/1`, admits only `write/1`, and retains the `write/2` deny-list
entry. No stream capability is introduced and no other I/O predicate is admitted.
General partial-closure `call/N` admission is unchanged; these tests exercise
complete goals through `call/1`, not every higher-order form.

[Observations](results/observations.json) and [provenance](results/provenance.json)
record working-source hashes, commands, selected separate engine hashes and
before/after preservation checks. Selected engines are the verified separate SWI
10.1.18 build with prior fixes and unmodified Trealla v3.14.10 with matching
libraries. Default text reading is used. Explicit `[a,b,c]` is therefore the
shared fixture; this does not claim that `"abc"` currently denotes the same term
on both runtimes. No GNU, WASM or experimental character-list SWI result is inferred.

After disposable checks passed, n5's backend was restarted with a new frozen
snapshot containing only this additional policy repair. All 11 Trealla public
checks passed again through `http://localhost:3060`. The actual UI visibly prints
`abc` for `write(abc)` and `[a,b,c]` for `write("abc")`. Deployment commands, logs,
screenshot and rollback details are in
`trealla-port/docs/verification/write-output-2026-10-25/`.

The n3 process, n5 frontend, auxiliary 3061 process, installed engine and dependency
pin are unchanged. Book examples and earlier historical reports are unchanged.
