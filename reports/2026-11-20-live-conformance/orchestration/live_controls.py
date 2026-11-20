from pathlib import Path
import sys,json,time,subprocess,collections,hashlib
P=Path(__file__).resolve().parents[1];R=P/'suite-snapshot';sys.path[:0]=[str(R/'runner'),str(R/'adapters')]
import run as actor,local_page_errors as pages
F=P/'live-controls';F.mkdir(exist_ok=True)
for node in ['n3','n4','n5']:
 while not (P/'logs'/('more-'+node+'.done')).exists():time.sleep(2)
 # The extended driver loaded before the HTTPS-to-WSS call-site correction.
 # These retain the unmodified maintained toplevel assertions with a correct WSS base.
 actor.set_session_interval(2.1);rows=[];path=R/'cases/partial-page-errors-0.1.json';pack=json.loads(path.read_text())
 for c in pack['cases']:
  if c['transport']!='toplevel':continue
  row=dict(id=c['id'],title=c['title'])
  try:row.update(status='pass',observation=pages.toplevel_case(c,'wss://'+node+'.elfenbenstornet.se'))
  except Exception as e:row.update(status='fail',detail=type(e).__name__+': '+str(e))
  rows.append(row)
 (F/('partial-page-errors-'+node+'.json')).write_text(json.dumps(dict(suite=pack['suite'],candidate=node,manifest_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),scope='Controlled unchanged assertion rerun with correct WSS URL base; original orchestration outcomes preserved',results=rows,counts=dict(collections.Counter(r['status'] for r in rows))),indent=2)+'\n')
 print(node,'page controls complete',flush=True)
# Prompt checks start only after the other endpoint phases, so race assertions
# are not serialized or distorted by artificial request throttling.
for node in ['n2','n3','n4','n5']:
 while not (P/'logs'/('library-'+node+'.done')).exists():time.sleep(2)
 with (P/'logs'/('prompt-http-'+node+'.log')).open('w') as out:
  cmd=['python3',str(R/'runner/prompt_http.py'),'--'+('trealla' if node=='n5' else 'swi'),'https://'+node+'.elfenbenstornet.se','--output',str(F/('prompt-http-'+node+'.json'))]
  result=subprocess.run(cmd,stdout=out,stderr=subprocess.STDOUT)
 print(node,'prompt HTTP',result.returncode,flush=True)
