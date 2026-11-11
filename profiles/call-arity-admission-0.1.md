# Completed call/N arity

Ten positive cases run unchanged on native SWI and Trealla in blacklist,
whitelist and owner-off modes. They cover builtin and private closures, prefix
arguments, all appended arities 1–7, sharing and rollback. Four additional
policy checks require a specific formal error class and a successful
follow-up query on the same session. Unknown and variable callbacks are checked in whitelist; forbidden and
nested qualified callbacks are checked in blacklist and whitelist. These rows
are `not_applicable` in other modes, not deferred semantic tests. Owner-off never executes their halt goal.

Use `adapters/local_runtime_contracts.py --manifest cases/call-arity-admission-0.1.json`
with both native roots and the released Trealla engine. The Trealla completed
arity repair must land first. The successor pack now requires SU-019 and
SU-HTTP-019 in whitelist too, with no remaining deferrals. ISO call/N errors
remain separate from the pending library callback-validation work.
