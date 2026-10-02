# Portable text portability survey

Status: **investigation note**  
Date: 2026-10-02

This note assesses how readily selected Prolog systems could implement the
draft [`portable-text-0.1`](../profiles/portable-text-0.1.md) rule that a
double-quoted sequence denotes a list of one-character atoms. It is a reader
capability survey, not a node-conformance result: none of SICStus, Ciao, or XSB
was tested here through a Web Prolog node.

## Summary

| System | Default double-quote meaning | Character-list mode | Initial assessment |
|---|---|---|---|
| Trealla | character atoms | native/default | Direct fit; executable Web Prolog suite passes 7/7 |
| Scryer | character atoms | native/default and recommended | Direct fit |
| SWI | native string object | `double_quotes(chars)`, module-local | Feasible, but every public reader and generated source module must be controlled |
| SICStus 4.10 | character codes | configurable, global, volatile `double_quotes=chars` flag | Feasible, but invasive: unlike SWI, modules cannot isolate the setting, and the manual warns that most SICStus code assumes `codes` |
| GNU Prolog | configurable; commonly codes | `double_quotes=chars` | Feasible through its global startup flag |
| Ciao 1.25 | character-code/byte list in the tested reader | No verified character-atom mode | Requires a Web Prolog reader or source transformation; the reported ISO flag is misleading |
| XSB 5.0 manual | character codes | No: `double_quotes` is fixed to `codes` | Requires a Web Prolog reader or source transformation |

“Feasible” in this table concerns literal syntax only. A port must additionally
verify DCGs, formatting, source loading, term writing, Unicode, sandbox policy,
and all generated/private module contexts covered by the executable suite.

## SICStus Prolog

The SICStus 4.10.1 manual documents three values for the volatile ISO
`double_quotes` flag: `codes` (the default), `chars`, and `atom`. With `chars`,
`"SICStus"` reads as a list of one-character atoms. This is exactly the draft's
term semantics. The same manual explicitly says that all SICStus Prolog flags
are global rather than local to a module or Prolog text. This differs from
SWI-Prolog, where `double_quotes` is maintained per module.

There are two qualifications:

1. SICStus says that most code assumes the default `codes` setting and advises
   against changing it. A node-wide switch could therefore affect libraries
   outside the Web Prolog boundary.
2. The documented `read_term/[2,3]` options do not include a per-read
   double-quote override. A SICStus port would need either a carefully isolated
   node runtime or a reader/source boundary that safely changes and restores
   the volatile global flag. Module separation alone cannot protect SICStus
   libraries that expect code lists.

This assessment is documentation-based; SICStus was not installed locally.

Primary references:

- [SICStus 4.10.1 documentation index](https://sicstus.sics.se/documentation.html)
- [SICStus Prolog flags are global](https://sicstus.sics.se/sicstus/docs/latest/html/sicstus/ref_002dlps_002dflg.html)
- [SICStus strings as lists](https://sicstus.sics.se/sicstus/docs/4.8.0/html/sicstus/ref_002dsyn_002dcpt_002dsli.html)
- [SICStus `read_term/[2,3]`](https://sicstus.sics.se/sicstus/docs/4.3.4/html/sicstus/mpg_002dref_002dread_005fterm.html)

## Ciao Prolog

Ciao 1.25.0-m1 was available locally and was probed through `ciaosh`. The
installed runtime reports:

```prolog
?- current_prolog_flag(double_quotes, X).
X = chars
```

But the reader's observable results are code/byte lists:

```prolog
?- X = "abc".
X = [97,98,99]

?- X = "å".
X = [195,165]
```

The second result is the UTF-8 byte sequence rather than either `[229]` or
`['å']`. The installed Ciao source also defines its ordinary `string/1` as a
list of character codes, and its optional `read_string_data_type` flag chooses
between such a list and Ciao's distinct string wrapper; it does not provide a
verified one-character-atom mode.

Consequently, the reported ISO `double_quotes=chars` value must not be accepted
as evidence of draft conformance. For this purpose it behaves inconsistently
with the usual meaning of `chars`. A Ciao node would initially need its own
Web Prolog source reader/token transformation, followed by Unicode-specific
tests. This may also merit a narrowly scoped Ciao issue independently of any
Web Prolog port.

Primary references:

- [Ciao 1.25 manual](https://ciao-lang.org/ciao/build/doc/ciao.html/)
- [Ciao term input and `read_string_data_type`](https://ciao-lang.org/ciao/build/doc/ciao.html/read.html)
- [Ciao term output and `write_strings`](https://ciao-lang.org/ciao/build/doc/ciao.html/write.html)

## XSB Prolog

The current XSB manual (describing version 5.0) is unambiguous: double-quoted
terms are lists of character codes, `double_quotes` is always `codes`, and the
flag is not settable. XSB's version 4 release notes mention an option for
reading double-quoted text as an atom, but that does not supply the required
character-atom-list mode.

An XSB port therefore cannot obtain the proposed semantics through normal flag
configuration. It would need a Web Prolog-specific reader or a token-preserving
source transformation. A transformation performed only after ordinary parsing
is insufficient because the resulting code list no longer records whether the
author wrote `"abc"` or `[97,98,99]`.

This assessment is documentation-based; XSB was not installed locally.

Primary references:

- [XSB manual, `double_quotes` flag](https://xsb.sourceforge.net/manual1/manual1.pdf)
- [XSB version 4 release notes](https://xsb.sourceforge.net/downloads/changelog.html)

## Consequences for the draft

The proposal remains coherent, but it is not merely a choice all candidate
runtimes can enable. The systems divide into three implementation classes:

1. **Native fit:** Trealla and Scryer.
2. **Configurable fit:** SWI, SICStus, and GNU Prolog, with different flag
   scopes and compatibility risks.
3. **Reader adaptation required:** Ciao and XSB.

This does not by itself argue for code lists instead. Requiring code lists
would reverse some of the same difficulty for systems centered on character
atoms, and would not solve the larger need for a precisely specified Unicode
model. It does show that source notation and the portable text data model are
two separable design decisions.

Before promoting Portable Text 0.1 out of draft, Web Prolog should decide
explicitly between these alternatives:

- **Strong source rule:** every Web Prolog reader gives double quotes
  character-list semantics. Ciao and XSB adapters must implement a specialized
  reader or lexical transformation.
- **Portable data model only:** protocol text is represented as character
  lists, while source files must use explicit lists where host double-quote
  syntax differs. This is easier to port but makes tutorial source less
  portable and weakens the current profile substantially.
- **Negotiated text syntax:** nodes advertise `chars`, `codes`, or native
  strings. This reflects existing systems but fragments source portability and
  is therefore the least attractive option for a shared Web Prolog language.

The current draft deliberately retains the strong source rule while this
decision is reviewed. Conformance results must be based on behaviour, not only
on a runtime's reported `double_quotes` flag.
