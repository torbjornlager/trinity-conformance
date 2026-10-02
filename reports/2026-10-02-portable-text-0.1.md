# Portable Text 0.1 draft baseline — 2026-10-02

This report records the first execution of the opt-in `portable-text-0.1`
suite. Neither deployed node was changed. The result is a baseline for the
proposed text semantics, not a regression in the existing ACTOR profile.

## Candidates

| Candidate | Runtime/configuration | Result |
|---|---|---:|
| Trealla port | Trealla Prolog 3.12.6, local source checkout, `profile(actor)`, open authentication, blacklist sandbox | 7/7 pass |
| SWI reference node | Local source checkout, default SWI double-quote semantics, `profile(actor)`, open authentication, blacklist sandbox | 0/7 pass |

Both candidates ran as fresh processes. The same dependency-free runner used
a fresh WebSocket connection for every case and imported no implementation
module.

## Covered cases

- `TXT-001` double-quoted ASCII text is a list of one-character atoms
- `TXT-002` empty double-quoted text is the empty list
- `TXT-003` non-ASCII text contains a Unicode character atom, not UTF-8 bytes
- `TXT-004` double-quoted DCG terminals have list semantics
- `TXT-005` source loaded with `src_text` uses the same semantics
- `TXT-006` a returned text term can be parsed again with the same meaning
- `TXT-007` double-quoted text participates in relational list operations

## Interpretation

Trealla's current observable behaviour already satisfies this draft. The SWI
node reads double-quoted literals as SWI string objects in all seven tested
contexts, which is SWI's documented default. For example, the DCG case reports
that a list was expected but a string was found.

The SWI result is therefore an expected implementation/configuration gap, not
evidence of an SWI runtime defect and not a failure of the separately versioned
ACTOR Core 0.1 profile. A later SWI implementation change must arrange
`double_quotes(chars)` consistently in the public goal reader, supplied-source
modules, generated/private modules, and term serialization contexts. Merely
changing one calling module would not establish conformance because SWI
maintains this flag per module.

## Test-design findings

The initial draft used explicit `=/2` in several submitted goals. Trealla's
current public-goal policy rejected those calls, confounding text semantics
with sandbox policy. The final cases express the same observations through
`member/2` and `append/3` instead. An initial emoji example was also replaced
by `å`: the profile still requires Unicode-character semantics, while support
for every possible Unicode scalar is a distinct portability question.

## Next decision

The profile should remain opt-in until its wording and cases have been reviewed.
If accepted, the next implementation step is to adapt an undeployed SWI test
configuration and rerun both this suite and ACTOR Core 0.1 before changing any
running node.
