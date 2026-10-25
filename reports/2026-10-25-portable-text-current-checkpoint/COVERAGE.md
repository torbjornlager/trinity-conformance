# Current native character-list checkpoint — 25 October 2026

This focused assessment uses the current repaired native SWI sources with default
and opt-in `portable-text-0.2` reading on temporary n3-like nodes. The current
Trealla n5 is the cross-runtime reference. No deployed reader or runtime is
changed, and no full portable-text/shared ACTOR pack is claimed to have rerun.

| Concern | Default SWI | Character-list SWI |
|---|---|---|
| Goal, Unicode, private-source and shared-DB readers | pass | pass |
| Constructed actor source | pass | pass |
| RPC and promise callback/retry/sharing, both directions | pass | pass |
| Current computed-cycle guard | pass | pass |
| Required public controls | 16/16 pass | 13/13 pass |
| Term-output alignment diagnostics | matches explicit-list Trealla controls | 3 mismatches |
| Existing TEXT/library tier | 40 selections pass | 40 selections pass |
| Read-only example checks | 10 pass | 10 pass |
| Model/Jev reader-input validators | accept native strings | reject character lists |

The three diagnostic mismatches are `write("abc")`, `write([a,b,c])` and
`writeln([a,b,c])`: the experimental SWI text bridge prints `abc`, while Trealla
prints `[a,b,c]`. The character-list reader itself has produced the correct term;
term writing is being passed through text/prompt conversion. Current live n3/n5
controls confirm the unchanged ordinary-reader behavior.

The passing example checks explicitly include known character-list rejections.
They do not make the model/Jev application boundary migration-ready. Pure
validators only were called; no provider request or chargeable inference ran.
The next repairs are term-writing versus text-output separation, then explicit
portable/native text conversion at application boundaries with mocked providers.

The full report, runner, source hashes, process/engine preservation evidence,
raw observations and pure service probe are retained in:

```
swi-prolog-node/docs/verification/portable-text-current-checkpoint-2026-10-25/
```

The source base is native SWI `b61270d` plus the current cycle repair; engines
remain the verified SWI 10.1.18 prefix and unmodified Trealla v3.14.10. All temporary
nodes are stopped. n3's regular reader, n5, its frontend, the auxiliary node and
the dependency pin are unchanged. These counts overlap earlier checkpoints and
are not added to cumulative conformance totals. GNU/WASM and a full T2/T4 rerun
are outside this batch. Historical matrices remain unchanged.
