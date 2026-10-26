# Four-mode character-list checkpoint — 26 October 2026

The normal language paths agree on character-list reading in the selected
native SWI, Trealla and both SWI-WASM implementations. This checkpoint is **not
all green**: the default WebSocket JSON encoding exposes Trealla's supplementary
Unicode decoding problem; browser URI policy and CORS prevent three selected
browser paths; and a separate public term-reader control differs in native SWI.
No runtime repair or profile promotion is included.

## Tested versions

These are the selected, committed deployment sources, not today's repository
heads: native SWI `abbc56f3d5104bd6d40d2ed5f99fe6199d75c4a8`, Trealla
`e7c51dc101cd8002dea9548f8154fc4d2bf6707d`, browser assets
`b9ea7c557a61faf5ef9524fb97500bbe1ff89015`. Native engines are the selected
SWI 10.1.18 separate build (core receive fix, PCRE and HTTP shutdown candidate)
and unmodified Trealla 3.14.10 with matching libraries. Binary hashes, source
identities and input hashes are in [native provenance](native/provenance.json)
and [browser provenance](browser-provenance.json).

The initial native run archived committed source into temporary directories.
A second pair of temporary loopback nodes loaded the same clean, frozen source
copies read-only for browser peers and controls. The temporary SWI node served
the unchanged browser assets and a private fixture examples directory. No test
query went to live n3/n5. Both temporary peer processes and the browser tab were
closed. Process identities, launchers, selected binaries/libraries, source files,
asset configuration and dependency pin were preserved; see
[preservation](preservation.json), [native preservation](native/preservation.json)
and [final source comparison](final-source-preservation.json).

## Results

See the [per-case matrix](COVERAGE.md). Do not sum overlapping controls.

| Selection | Result |
|---|---|
| Existing 26-case portable-text pack, native SWI | 26 pass |
| Same pack, Trealla, runner's normal escaped JSON | 22 pass; 4 fail |
| Same pack, Trealla, literal UTF-8 JSON control | 26 pass |
| Browser Worker, 26 mapped assertions | 23 pass; 3 blocked/diagnostic |
| Browser main thread, same 26 mapped assertions | 23 pass; 3 blocked/diagnostic |
| Nine additional browser controls per mode | 9 pass in each |
| Native output, scalar construction and promise-template controls | Pass in both |
| Additional native `atom_to_term/3` reader control | SWI fails character-list assertion; Trealla passes |

Both browser modes visibly print `[a,b,c]` before the answer to
`write("abc").`; [Worker evidence](worker-output.ax.txt),
[main-thread evidence](main-output.ax.txt), and the two UI screenshots retain
that observation. The native output controls also receive exactly `[a,b,c]`.
Promise controls preserve the character-list template, repeated-variable
structure, and the caller's unbound variable.

## Procedure and limits

The [existing experimental manifest](../../cases/portable-text-0.2.json) supplies
the assertions. Native tests use the public WebSocket session API and HTTP peers;
`runner/portable_text.py` resubmits serialized bindings and exercises public
input replies. The normal runner intentionally keeps its existing JSON encoding.
The separate UTF-8 control changes only client JSON spelling, without changing
any Prolog goal, expected answer or engine.

Browser tests use the public portal terminal through CUA, with runtime identity
confirmed by `runtime_property/1` and the visible mode footer. Source cases load
an ordinary monitored actor using `src_text/1`, `src_list/1` or `src_uri/1` and
assert the same source result plus exact child termination. The copied-source
case also checks a nested copied helper. These are explicitly mapped procedures,
not a claim that browser terminal access is the native WebSocket harness.
The three loaded-source native session cases additionally cover that entry path.
Browser input is supplied through its real terminal prompt. Four separate
round-trip controls copy the **displayed** text binding and resubmit that exact
spelling for equality; the initial mapped assertions alone do not establish a
serialization round trip.

Each successful browser assertion has an exact, unique `Checkpoint` binding.
Full accessibility states are compressed in [browser evidence](browser-evidence.json.gz);
[compact results](browser-results.json) retain executed goals. Mode attribution
comes from each observed footer, and marker checking uses exact identifiers,
so `txt023swi` cannot satisfy `txt023`. Delayed source completions are checked
against later captured states from the same mode. No browser runtime state was
read or modified using JavaScript evaluation.

This is a finite functional checkpoint, not concurrency stress, complete Unicode
validation, DCG standards certification or a full library-boundary audit. GNU
ISOBASE and unrelated actor/lifecycle suites were not rerun. Shared database
reading was exercised during browser boot but has no new dedicated assertion in
this selection. Existing reader-migration evidence remains historical.

## Separate diagnostics

1. **Trealla JSON surrogate pairs.** TXT-008/020/025/026 fail with
   `representation_error(character)` when supplementary scalars are represented
   by JSON `\uDxxx\uDxxx` pairs. All four pass with the identical payload encoded
   as literal UTF-8; the full 26-case UTF-8 rerun passes. The ASCII-only scalar
   construction control also passes. This distinguishes the known JSON-library
   decoding issue from general character-list/Unicode support. The installed
   library was not patched. See [encoding controls](native-controls.json).

2. **Browser source policy.** TXT-018 rejects the temporary loopback fixture
   origin with `src_uri origin is not allowed in SWI-WASM`. The source file is
   served successfully over HTTP, but the browser actor URI loader allows only
   its configured public node origins. This checkpoint preserves that policy;
   it does not establish a browser URI-source text failure after admission.

3. **Browser-to-Trealla CORS.** TXT-023/024 fail at fetch against the separate
   temporary Trealla origin, whose HTTP response omits CORS authorization. The
   same assertions pass against the same-origin temporary SWI peer in both
   browser modes. Native opposite-runtime HTTP tests pass. Cross-origin browser
   compatibility with Trealla remains unverified here; no CORS setting changed.

4. **Native SWI public term-reader boundary.**
   `atom_to_term('"ab"',T,[])` returns `"ab"` on native SWI and `[a,b]` on Trealla;
   both browser modes satisfy `T==[a,b]`. See the explicit
   [reader result](atom-reader-diagnostic.json). Ordinary native goal, input,
   source and serialization tests pass. This is a remaining built-in reader
   boundary, not evidence that the shell's character-list reader reverted.
   The next bounded assessment should decide which public term-reading
   predicates the language promises to align before implementing a repair.

The temporary UI fixture deliberately supplies only the text example, so its
examples-index request logs a 500 for missing normal example directories. That
fixture limitation does not affect the terminal assertions and is not counted
as a runtime regression.

## Reproduction

Run `adapters/local_portable_text.py --help` for the unchanged native runner;
its exact invocation is in the recorded provenance. Use the source and engine
paths above, `--swi-portable-text` and `--trusted-loopback-transport`, and a fresh
output directory. Expected normal results are 26/26 SWI and 22/26 Trealla.

From the conformance root, `python3 <this-directory>/serve_disposable.py --output
/tmp/text-checkpoint-fresh` starts separate UI/peer fixtures and records their
URLs. The launcher intentionally requires a new evidence directory. It uses the
local frozen source/engine paths recorded above; adapt these paths on another
machine. Open its SWI `/portal?node=swi-wasm`, run the saved goals and input
procedures, switch execution modes in Settings, and observe exact results. Use
its SWI origin for the source fixture and same-origin HTTP controls. Finish by
creating `STOP` in that fresh evidence directory; the launcher stops only its
own processes and removes its temporary asset root.

`check_native_controls.py --swi <temporary-url> --trealla <temporary-url>
--output <fresh-json-file>` repeats the output/promise/reader and two JSON
encoding controls. `verify_results.py` audits the saved evidence and matrix
counts without starting any runtime. Historical reports are untouched.
