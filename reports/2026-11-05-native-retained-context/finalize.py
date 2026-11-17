from pathlib import Path
import json,hashlib,shutil,subprocess,datetime,platform,re,os
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
inputs={'core':'/tmp/native-context-canonical-core','repeat':'/tmp/native-context-canonical-repeat','trealla-route':'/tmp/native-context-canonical-trealla','mixed-routes':'/tmp/native-context-canonical-mixed'}
rows={};reports={}
for label,base in inputs.items():
 base=Path(base);data=json.loads((base/'results.json').read_text());assert data['counts']['error']==0,(label,data['counts']);reports[label]=data
 shutil.copy(base/'results.json',O/(label+'.json'));shutil.copy(str(base)+'.txt',O/(label+'.txt'))
 for row in data['results']:
  key=(row['candidate'],row['id'])
  if key in rows:assert rows[key]['status']==row['status'],key
  else:rows[key]=row
assert reports['core']['counts']==reports['repeat']['counts']=={'pass':23,'fail':7,'blocked':0,'error':0}
assert len({v['adapter_sha256'] for v in reports.values()})==1
merged=dict(reports['core']);merged.update(scope='Scoped native audit: retained WSS, explicit retained SWI HTTP sessions, fresh HTTP request separation and four directed native route pairs. Canonical node URLs; duplicate controls agree; blocked probes are not passes.',routes=['swi-a:swi-b','swi-a:trealla-b','trealla-a:swi-b','trealla-a:trealla-b'],results=list(rows.values()),counts={s:sum(r['status']==s for r in rows.values()) for s in ['pass','fail','blocked','error']},runs={k:dict(report=k+'.json',counts=v['counts']) for k,v in reports.items()})
assert merged['counts']=={'pass':31,'fail':9,'blocked':11,'error':0};(O/'results.json').write_text(json.dumps(merged,indent=2)+'\n')
adapter=R/'adapters/local_retained_context.py';assert hashlib.sha256(adapter.read_bytes()).hexdigest()==merged['adapter_sha256'];shutil.copy(adapter,O/'adapter-source.py')
shutil.copy('/tmp/native-context-existing-controls.txt',O/'existing-swi-controls.txt')
log=(O/'existing-swi-controls.txt').read_text();passed=re.findall(r'^% \[(\d+)(?:-\d+)?/35\].*passed',log,re.M);assert len(set(passed))==35 and len(passed)==47
engines={}
for name,exe in [('swi','/usr/local/bin/swipl'),('trealla','/Users/lager/trinity-demonstrator/.trinity/trealla-engine/tpl')]:
 args=[exe,'--version'] if name=='swi' else [exe,'-g','current_prolog_flag(version_data,V),writeq(V),nl,halt'];env=dict(os.environ)
 if name=='trealla':env['TPL_LIBRARY_PATH']=str(Path(exe).parent/'library')
 engines[name]=dict(path=exe,sha256=hashlib.sha256(Path(exe).read_bytes()).hexdigest(),version=subprocess.check_output(args,text=True,env=env).strip())
 if name=='trealla':
  lib=Path(exe).parent/'library';engines[name]['library_tree_sha256']=hashlib.sha256(''.join(str(p.relative_to(lib))+':'+hashlib.sha256(p.read_bytes()).hexdigest()+'\n' for p in sorted(lib.rglob('*')) if p.is_file()).encode()).hexdigest()
for name,repo in [('swi','swi-prolog-node'),('trealla','trealla-port')]:
 root=Path('/Users/lager')/repo;assert not subprocess.check_output(['git','status','--porcelain'],cwd=root)
 pin=json.loads((Path('/Users/lager/trinity-demonstrator/dependencies')/(repo+'.json')).read_text());assert pin['revision']==merged['sources'][name]['revision'];engines[name]['matches_consumer_source_pin']=True
 for f,h in merged['sources'][name]['files_sha256'].items():assert hashlib.sha256((root/f).read_bytes()).hexdigest()==h,(name,f)
ledger=json.loads((R/'requirements/appendix-b-0.1.json').read_text());rev=ledger['source']['revision'];manual=subprocess.check_output(['git','show',rev+':author/appendix-B-current-manual.tex'],cwd='/Users/lager/boken/author');assert hashlib.sha256(manual).hexdigest()==ledger['source']['sha256'];(O/'pinned-manuscript.tex').write_bytes(manual)
environment=dict(date=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='audit complete; observed failures and blocked coverage; no runtime repair or deployment',host=platform.platform(),engines=engines,counts=merged['counts'],core_repeat=dict(runs=2,cases_per_run=30,pass_per_run=23,fail_per_run=7,status_agreement=True),existing_swi_named_tests=35,existing_swi_parameterized_executions=47,pinned_manuscript=ledger['source'],notes=['Each native node is addressed by its canonical URL; URI aliasing is not part of these findings.','SWI fixture hosts three HTTP listeners in one isolated SWI process; Trealla listeners use separate isolated processes. All communication is localhost.','Source/goal-export-blocked probes are not classified as ownership failures.','The uncommitted library-documentation draft remains outside this audit. Runtime sources, installed engines, dependency pins and public services are unchanged.'])
(O/'environment.json').write_text(json.dumps(environment,indent=2)+'\n')
files={str(p.relative_to(O)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(O.rglob('*')) if p.is_file() and p.name!='verification.json'}
record=dict(recorded_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='audit complete; failures recorded; repairs not implemented',distinct_probe_counts=merged['counts'],core_repeated_identically=True,existing_swi_named_tests_pass=35,existing_swi_parameterized_executions_pass=47,ledger_unit_tests_pass=7,public_services_changed=False,runtime_sources_changed=False,artifacts_sha256=files)
(O/'verification.json').write_text(json.dumps(record,indent=2)+'\n');print('PASS audit evidence: 51 distinct probes; core repeated; 35 named existing tests / 47 executions; exact source pins and hashes')
