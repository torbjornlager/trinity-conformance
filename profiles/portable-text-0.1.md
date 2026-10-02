# Portable Text 0.1

Status: **draft experimental profile**  
Test transport: ACTOR WebSocket protocol version `1`

This document defines the portable source-level meaning of double-quoted text
in Web Prolog. It is deliberately separate from the cumulative node profiles:
the semantic requirement is intended to apply wherever Web Prolog source is
accepted, while the initial executable tests use an ACTOR session as their
implementation-neutral black-box transport.

No deployed node is required to claim this draft merely because it advertises
`relation`, `isobase`, `isotope`, or `actor`.

## Normative semantics

1. A double-quoted sequence must read as a proper list of one-character atoms.
   Thus, `"abc"` is observationally equivalent to `[a,b,c]`, and `""` is
   equivalent to `[]`.
2. A character means one Unicode character represented by a one-character
   atom. It does not mean one byte of the character's UTF-8 encoding.
3. The rule must apply consistently to:
   - submitted goals;
   - source supplied through `src_text`, `src_list`, or `src_uri`;
   - generated or private modules in which supplied source is compiled; and
   - Prolog terms serialized for later submission to a node.
4. Character lists must retain ordinary list behaviour, including unification,
   list decomposition, DCG terminals, and list predicates.
5. Single-quoted text remains an atom. Double-quoted text must not silently
   become an atom or a distinct opaque string value in portable code.
6. The contract is observational. An implementation may use a packed internal
   representation if all portable Prolog operations have the required list
   semantics.

## Boundaries

JSON fields in the wire protocol remain JSON strings. This profile governs the
Prolog text represented by those fields, not the JSON data model itself.

Native string types and implementation-specific string predicates are outside
this profile. Implementations may offer them as extensions, but portable Web
Prolog source must not depend on them. Normal source-size, term-depth, and
resource limits still apply.

## Rationale

Character lists avoid relying on a native string type that many Prolog systems
do not have. They also avoid representing arbitrary text as a single atom,
which is undesirable on systems without atom garbage collection or with atom
length limits.

Trealla Prolog and Scryer Prolog already expose double-quoted text with
character-list semantics. Scryer may store such lists in a packed form while
preserving their observable list behaviour. SWI-Prolog can select the same
syntax with the module-local `double_quotes` flag. These facts motivate the
draft, but the normative requirement is the observable contract above rather
than any one implementation's representation.

## References

- [SWI-Prolog flags: `double_quotes`](https://www.swi-prolog.org/pldoc/man?section=flags)
- [SWI-Prolog strings and character lists](https://www.swi-prolog.org/pldoc/man?section=string)
- [Scryer Prolog README: default `double_quotes=chars`](https://github.com/mthom/scryer-prolog)
- [Scryer Prolog `format/2` documentation](https://www.scryer.pl/format)
- [Trealla Prolog](https://github.com/trealla-prolog/trealla)

## Conformance

The normative executable metadata is in
[`cases/portable-text-0.1.json`](../cases/portable-text-0.1.json). A candidate
conforms only when every case passes in the same configuration. Because this
is an opt-in draft, a baseline failure is evidence that the candidate does not
yet implement the draft; it does not retroactively invalidate another profile
the node currently advertises.
