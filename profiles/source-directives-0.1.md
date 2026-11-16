# Source directives 0.1 — separate draft pack

This draft selects the rule decided on 15 November 2026: a directive in actor
or session source that fails, or that the engine does not carry out, makes
creation raise `error(directive_failed(Directive), _)`. No actor is created.
It does not amend baseline 0.1 or create an advertised profile. Required means
required within this pack. All engines run the same
[public-interface assertions](../cases/source-directives-0.1.json).

| Case | Selected observation |
| --- | --- |
| SD-001 | `src_text(':- fail.')` makes `spawn/3` raise `directive_failed(fail)`; no pid is bound and the goal never runs. |
| SD-002 | A failing goal directive after earlier clauses is reported as the plain goal, without module qualification. |
| SD-003 | When several directives fail, the first is reported. |
| SD-004 | `dynamic/1` and ordinary clauses still create a working actor. |
| SD-005 | `toplevel_spawn/2` with a failing directive raises the same term. |
| SD-006 | A directive calling a goal the sandbox forbids in queries (`open/3`) is refused by `spawn/3` with `permission_error(execute, sandboxed_directive, _)` and never runs. |
| SD-007 | The same for `toplevel_spawn/2`. |

In SD-006 and SD-007 an engine that executes no goal directives at all (ECLiPSe/N7 runs only `dynamic/1`) may refuse with `directive_failed(Directive)` instead; the requirement is that the directive never runs and no actor is created.

In SD-001, SD-002, SD-003 and SD-005 a node whose sandbox admits no goal
directives may instead refuse the directive before it runs, with
`error(permission_error(execute, sandboxed_directive, _), _)`. Either way no
actor is created; silent success and a hanging creator both fail the case.
Trealla's public sandbox admits only `dynamic/1` and `discontiguous/1`.
Visitors cannot use `link(false)`, so the cases leave it out.

Option lists are delivered as ordinary self-messages before calling creation
predicates, as in the creation-validation pack, so that static query admission
does not inspect the literal source first. Context arguments are not compared.

SD-006 and SD-007 were added on 16 November 2026 after the diagnostic in
that day's review showed the directive running on native SWI (both paths) and
on Trealla (`toplevel_spawn/2`) before the fixes.

Directives that raise an exception are outside this pack: engines currently
differ on whether the original exception or a warning reaches the creator.
ECLiPSe rejects directives other than `dynamic/1` and reports them with the same
term; a case for an unsupported directive is left to a later pack because the
set of supported directives differs per engine. `src_uri`, `src_list`,
statechart support source and remote creation are excluded.

Before this rule, native SWI-Prolog and SWI-WASM printed a warning and created
the actor, and Trealla could hang the creator indefinitely (handover §11.1).
