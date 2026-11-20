from pathlib import Path
import json,subprocess,hashlib,datetime
P=Path(__file__).resolve().parent;R=Path('/Users/lager/trinity-conformance');A=R/'reports/2026-11-19-upgraded-live-conformance';B=R/'reports/2026-11-20-live-conformance'
status={'pass','fail','blocked','error','observed','unsupported','diagnostic_error','not_applicable','deferred'}
def rows(x):
 if isinstance(x,dict):
  if x.get('status') in status and any(k in x for k in ['id','case_id','case','label']):yield x;return
  for k,v in x.items():
   if k not in ['observation','transcript','sources','source','inputs','requests','events','trace']:yield from rows(v)
 elif isinstance(x,list):
  for v in x:yield from rows(v)
def key(r):return (r.get('id',r.get('case_id',r.get('case',r.get('label')))),r.get('candidate',r.get('engine')),r.get('route'),r.get('peer'))
a={r['file']:r for r in json.loads((A/'SUMMARY.json').read_text())['files']};b={r['file']:r for r in json.loads((B/'SUMMARY.json').read_text())['files']};changes=[]
for f in sorted(a.keys()&b.keys()):
 if any(w in a[f]['classification']+b[f]['classification'] for w in ['out_of_scope','invalid_','overlapping','superseded','first_']):continue
 old={key(r):r for r in rows(json.loads((A/f).read_text()))};new={key(r):r for r in rows(json.loads((B/f).read_text()))}
 for k in old.keys()&new.keys():
  if old[k]['status']=='pass' and new[k]['status'] in ['fail','error']:changes.append(dict(file=f,id=k[0],candidate=k[1],route=k[2],peer=k[3],detail=new[k].get('detail','')))
(P/'comparison.json').write_text(json.dumps(dict(previous=str(A.relative_to(R)),current=str(B.relative_to(R)),changes=changes),indent=2)+'\n')
targets=[r for r in changes if '/live-more/n6/' in r['file']];assert len(targets)==56;assert sum('query_limit_exceeded' in r['detail'] for r in targets)==55
(P/'n6-targets.json').write_text(json.dumps(targets,indent=2)+'\n')
for name in ['logs','n6','swi','sources']:(P/name).mkdir(exist_ok=True)
files={str(f.relative_to(R)):hashlib.sha256(f.read_bytes()).hexdigest() for folder in ['cases','runner','adapters','fixtures','profiles'] for f in (R/folder).rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.suffix!='.pyc'}
(P/'inputs.json').write_text(json.dumps(dict(revision=subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD'],text=True).strip(),files=files),indent=2)+'\n')
names=['deployment-wp_n3-1','deployment-wp_n4-1','trinity-n6-host-wp_n6-1','trinity-n6-host-n6_admission-1'];before=json.loads(subprocess.check_output(['docker','inspect',*names]));(P/'preservation-before.json').write_text(json.dumps([dict(name=d['Name'],id=d['Id'],image=d['Image']) for d in before],indent=2)+'\n')
(P/'STATE.json').write_text(json.dumps(dict(status='running',task='N6 clean56replays and NU003 repeated old/current controlled reproduction',started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),root=str(P),runtime_changes=False,original_reports_immutable=True),indent=2)+'\n');print('Prepared56N6targets and124matchedpass-to-failobservations')
