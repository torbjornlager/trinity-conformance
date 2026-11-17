from pathlib import Path
import json
O=Path(__file__).resolve().parent;R=O.parents[1]
assert json.loads((O/'verification.json').read_text())['status']=='deployed'
p=R/'CURRENT_COVERAGE.md';s=p.read_text();a=s.index('The [latest 5 November runtime repair release]');b=s.index('The [preceding promise release]',a)
s=s[:a]+'''The [latest standard-library release](reports/2026-11-05-standard-library-release/README.md)
is committed, pushed and deployed to N0–N6. All twelve services have exact checked
pins. Its 112-case shared selection passes 786 committed-source observations;
all 36 pinned consumer CI groups and 2,379 selected public checks pass.

The required library forms and described semantics work across all five runtime
modes. Library callback errors require exact callable types and original culprits
at invocation, with lazy unused callbacks and unchanged application exceptions.
The final Trealla repair also preserves this behaviour inside nested meta-calls.
The report retains the initial failed nested probe and the repeated final gates.
Full external ISO mode/error coverage and native retained-context propagation
remain open; these checks do not certify the complete language.

The [preceding runtime repair release](reports/2026-11-05-public-runtime-repair-release/README.md)
records the earlier localhost, remote output and N5–N4 ping-pong fixes. The
[standard-library development snapshot](reports/2026-11-05-standard-library/README.md)
retains the original 57-case baseline and 65-case qualification, with its own
historical manifests and scope.

'''+s[b:]
s=s.replace('resolved; the required GNU library forms are repaired in development, while','resolved; the required GNU library forms are deployed, while');p.write_text(s)
for name in ['cases/README.md','adapters/README.md']:
 p=R/name;s=p.read_text().replace('supplies 65 common goals','supplies 112 common goals');s=s.replace('[The development repair](../reports/2026-11-05-standard-library/README.md) records\nscoped before/after evidence and qualification limits.','[The development repair](../reports/2026-11-05-standard-library/README.md) retains\nthe earlier baseline. [The public release](../reports/2026-11-05-standard-library-release/README.md)\nrecords exact callback errors, the nested Trealla follow-up and deployed pins.');p.write_text(s)
p=R/'runner/appendix_coverage.py';s=p.read_text();s=s.replace('the required forms and described binding/solution semantics now pass the shared development selection across all five runtime modes. Complete external ISO mode/error coverage, exact error refinements and public promotion remain separate; see the standard-library repair record.','the required forms, described binding/solution semantics and exact callback errors are deployed across all five runtime modes. Complete the remaining external ISO mode/error inventory; see the standard-library release record.');s=s.replace('[Current public release](../reports/2026-11-05-public-runtime-repair-release/README.md)','[Current public release](../reports/2026-11-05-standard-library-release/README.md)');p.write_text(s)
