# SWI character-list term-output follow-up

25 October 2026. Current native SWI working-source candidate; default strings and
opt-in `portable-text-0.2` configuration on disposable n3-like nodes. Deployed
native Trealla is the cross-runtime peer. No regular node reader is switched.

| Check | Default SWI | Chars SWI |
|---|---|---|
| Public reader/source/shared-DB/transport/output controls | 16/16 pass | 16/16 pass |
| `write([a,b,c])` / `writeln([a,b,c])` | list syntax | list syntax |
| `write("abc")` | `abc` (native string) | `[a,b,c]` (list), matching Trealla |
| TEXT/library boundaries | 56 selections pass | 56 pass |
| T1_NATIVE | 98 selections pass | 98 pass |
| T2 | 145 selections pass | 145 pass |
| T4_NATIVE | 1529 selections pass | 1529 pass |
| Read-only example checks | 10 pass | 10 pass |

The three output mismatches from the preceding checkpoint are resolved. Proper
character lists are rendered before entering the text-output bridge in both
prelude forms. Atoms, strings, numeric code lists, other structured payloads,
variable sharing, partial lists, prompts and formatted text retain their existing
behavior. The internal helper is hidden from private listings. No tests were
relaxed to accept the previous output mismatch.

The model/Jev native-string guards remain migration work. The example suite's
passing results include intentional guard rejection; they do not certify those
services as character-list ready. No provider calls or service/example edits ran.
Full portable-text profiles, GNU/WASM, supplementary-Unicode interoperability
and all tutorial/book examples are not newly certified here.

Detailed candidate hashes, commands, evidence and preservation records are in:

```
swi-prolog-node/docs/verification/portable-term-output-2026-10-25/
```

Regular n3/n5, their reading modes and processes, installed engines/libraries and
the dependency pin are unchanged. All temporary nodes are stopped. Counts overlap
and are not added to cumulative shared baseline totals. Earlier reports and
unresolved diagnostics remain available.
