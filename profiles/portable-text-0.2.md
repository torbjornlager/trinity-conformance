# Portable Text 0.2

Status: **experimental, opt-in draft**. This expands
[0.1](portable-text-0.1.md), which remains available with its historical results.
It changes neither cumulative node-profile requirements nor deployed defaults.
ACTOR WebSocket version 1 is the test harness, not a claim that every ACTOR node
already implements these semantics. Adoption and runtime migration are separate
decisions.

## Proposed contract

1. A double-quoted literal denotes a proper list of one-character atoms:
   `"abc"` has the meaning `[a,b,c]`, and `""` has the meaning `[]`.
   These are ordinary relational lists, including in DCG terminals.
2. Here **character means Unicode scalar value**: U+0000–U+D7FF or
   U+E000–U+10FFFF. It does not mean a UTF-8 byte, UTF-16 code unit or displayed
   grapheme. Thus `"😀"` contains one element, `"é"` contains two (U+0065,
   U+0301), and `"👩‍💻"` contains three (U+1F469, U+200D, U+1F4BB).
   A surrogate is not a character under this contract.
3. Reading and serialization must preserve scalar sequences without implicit
   Unicode normalization. Precomposed `"é"` (U+00E9) and decomposed `"é"`
   (U+0065, U+0301) are distinct lists, despite often looking identical.
4. Single-quoted text remains an atom. There is no implicit conversion of
   arbitrary atoms, numeric lists or existing opaque native strings into
   character lists. Implementations may provide native string extensions;
   portable code cannot depend on their representation or predicates.
5. The requirement is observational. Packed storage is permissible if it
   preserves list operations, unification and variable sharing.

Source and protocol text must be decoded without replacing invalid sequences
with other characters. The exact error contract for malformed encodings,
surrogate escapes and prohibited source characters is still to be specified;
this draft does not claim executable coverage of those rejection paths.
Ordinary source-character, escape and resource rules continue to apply.

## Readers and supplied source

The same literal semantics must apply to submitted goals, Prolog option fields,
term input replies, and source compiled from `src_text/1` or `src_uri/1`.
Private and generated modules must preserve those semantics, as must copied
predicates and remotely supplied source. The receiving node reads remotely
supplied source under its own selected portable-text configuration.

`src_list/1` is different: its argument is **already constructed Prolog terms**,
not a character sequence to read again. For example:

```prolog
Clauses = [codes([97,98]), chars([a,b]), same(X,X)]
```

Passing these clauses through `src_list(Clauses)` must preserve the numeric
list, the character list and the repeated-variable relationship in `same/2`.
Ordinary actor copying and clause-variable scope still apply: preserving sharing
does not make the caller's variables shared mutable state with the child.
There must be no recursive numeric-list-to-character-list conversion.

If `src_list([p("ab")])` occurs inside a textual goal or option field, the
enclosing reader first constructs `p([a,b])`. The source loader subsequently
receives that term. Conversely, `src_list([p([97,98])])` keeps its numeric data.
This distinction also applies to clauses constructed at run time.

## Serialization and native boundaries

A serialized portable term must read back with the same data and sharing.
Writers may use explicit character lists or equivalent double-quoted literals;
the spelling need not be identical. Empty text, non-ASCII scalars, quotes and
backslashes must survive the round trip. A successful wire round trip alone
does not establish the semantics of the peer's source reader: tests must also
assert the list meaning on the peer before serialization.

JSON fields remain JSON strings. This draft governs the Prolog text carried
inside them, not the JSON data model. URI identifiers remain canonically atoms;
this draft does not redefine URI or Boolean types. Public APIs that accept
additional text representations need explicit boundary conversions under any
future portable-text configuration. Native libraries may retain their own
string conventions behind those conversions.

## Executable scope

[The 26-case manifest](../cases/portable-text-0.2.json) and
[runner](../runner/portable_text.py) exercise the following boundaries:

| Cases | Boundary |
|---|---|
| TXT-001–007 | Original literal, list, DCG, source and round-trip requirements |
| TXT-008–012, TXT-025 | Supplementary scalars, combining marks, normalization distinctions, atoms, escapes and graphemes |
| TXT-013–014 | Option-field reading and constructed `src_list/1` data/sharing |
| TXT-015–018 | Supplied DCGs, private actor source, copied predicates and URI source |
| TXT-019, TXT-026 | ASCII and Unicode toplevel input replies |
| TXT-020–022 | Unicode, empty and escaped answer round trips |
| TXT-023–024 | HTTP peer source semantics and answer data/sharing |

The first seven IDs retain their original metadata; 0.2 strengthens runner
checks and adds boundary cases. Results must identify the suite version rather
than combining 0.1 and 0.2 counts. The full run needs a caller, an HTTP peer and
an explicitly allowed HTTP source fixture. It must not silently skip missing
fixtures. The runner neither changes reader flags nor rewrites runtime sources.

A candidate claim requires all cases in one consistently selected configuration.
Failure against this experiment is not failure of an existing ACTOR obligation.
Passing the finite pack does not prove all Unicode values or all reader paths.
In particular, other input APIs, every option reader, direct remote ACTOR source
transport, invalid encodings, native-library conversions, memory costs and
performance remain unmeasured. GNU and browser results require separate runs;
native results cannot stand in for them.

## Migration gate

Before adopting the contract, implement an isolated test configuration covering
all public readers and supplied/private/generated source, audit string-dependent
examples and native API boundaries, and run this draft alongside actor and
interoperability suites. Include explicit numeric-list and variable-sharing
controls so migration cannot accidentally reinterpret existing data. A global
flag change or a reader-flag value alone is not implementation evidence.
