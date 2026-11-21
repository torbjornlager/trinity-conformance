from pathlib import Path
import json,hashlib,re,collections
R=Path('/private/tmp/claude-502/-Users-lager-trinity-demonstrator/58219eb7-1e68-4089-a2dd-25c3117837f6/scratchpad/tc');D=R/'reports/2026-11-21-post-release-conformance';O=Path(__file__).resolve().parents[1]
hashes=json.loads((D/'files-sha256.json').read_text())
assert set(hashes)=={str(p.relative_to(D)) for p in D.rglob('*') if p.is_file() and p.name!='files-sha256.json'}
assert all(hashlib.sha256((D/n).read_bytes()).hexdigest()==h for n,h in hashes.items())
for p in D.rglob('*.json'):json.loads(p.read_text())
v=json.loads((D/'verification.json').read_text());assert v['manifest_count']==81 and v['main_case_rows']==2081
assert not any(p['unaccounted_case_indexes'] for p in v['coverage'])
assert sum(len(p['not_executed_case_indexes']) for p in v['coverage'])==4
for pack in v['coverage']:
 for case in pack['cases']:
  for evidence in case['evidence']:assert (D/evidence['file']).is_file()
for p in [D/'REPORT.md',R/'README.md',R/'CURRENT_COVERAGE.md']:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if not target.startswith(('http:','https:','#')):assert (p.parent/target).exists(),(p,target)
secrets=set()
for p in (O/'orchestration/isolated').rglob('*.private.pl'):
 secrets.update(re.findall(r"bearer_token\([^,]+,'([^']+)'",p.read_text()))
assert len(secrets)==2,'Expected both execution-only fixture credentials'
for p in D.rglob('*'):
 if p.is_file():
  content=p.read_text()
  assert not any(value and value in content for value in secrets), 'Fixture credential exported'
print(json.dumps(dict(status='pass',hashed_artifacts=len(hashes),manifests=81,main_rows=2081,blocked_return_rows=4,links_and_json_valid=True,fixture_credentials_absent=True)))
