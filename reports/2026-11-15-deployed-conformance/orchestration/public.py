from pathlib import Path
import os,sys,json,time,traceback,subprocess
from datetime import datetime,timezone
from urllib.request import urlopen
os.umask(0o077);O=Path(__file__).parent;R=O/'conformance';sys.path.insert(0,str(R/'runner'));import run as actor,baseline
P=O/'public';P.mkdir();gate=json.loads((R/'profiles/actor-release-0.2.json').read_text());packs=[x['suite'] for x in gate['packs'] if x['suite']!='ownership-lifecycle-0.1']+['actor-behaviours-0.1','actor-supervisors-0.1','actor-workers-0.1','language-actor-0.1','server-waits-0.1','receive-callback-context-0.1','receive-wait-options-0.1','prompt-ws-0.1'];summary=[]
for n in range(8):
 try:
  info=json.load(urlopen(f'https://n{n}.elfenbenstornet.se/node_info',timeout=12));(P/f'N{n}-metadata.json').write_text(json.dumps(info,indent=2)+'\n')
  if n==0:continue
  report=P/f'N{n}-isobase-http.json'
  with (P/f'N{n}-http.log').open('wb') as f:p=subprocess.run([sys.executable,str(R/'runner/baseline.py'),'--manifest',str(R/'cases/isobase-http-0.1.json'),'--url',f'https://n{n}.elfenbenstornet.se','--candidate',f'N{n}-public','--profile',info['profile'],'--report',str(report)],stdout=f,stderr=f,timeout=180)
  summary.append(dict(node=n,selection='isobase-http-0.1',exit_code=p.returncode,report=str(report)));print('HTTP N'+str(n),p.returncode,flush=True)
 except Exception as e:summary.append(dict(node=n,selection='HTTP/metadata',error=repr(e)));print('HTTP N'+str(n),repr(e),flush=True)
(O/'public-http-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
for n in [3,4,5,7]:
 F=P/f'N{n}-actor';F.mkdir();url=f'wss://n{n}.elfenbenstornet.se/ws';candidate=actor.Candidate(url,'actor',5,None,f'https://n{n}.elfenbenstornet.se',False,());last=0
 for suite in packs:
  manifest=json.loads((R/'cases'/(suite+'.json')).read_text());rows=[];start=datetime.now(timezone.utc).isoformat()
  for case in manifest['cases']:
   if n==7:
    delay=5-(time.monotonic()-last)
    if delay>0:time.sleep(delay)
   last=time.monotonic();t=time.monotonic();row=dict(id=case['id'],title=case['title'])
   try:
    if 'goal' in case:result=baseline.query_case(case,url,8,None)
    else:result=actor.CASE_FUNCTIONS[case['id']](candidate)
    row.update(status='pass',observation=result)
   except Exception as e:row.update(status='fail',detail=type(e).__name__+': '+str(e))
   row['duration_ms']=round((time.monotonic()-t)*1000);rows.append(row);counts={k:sum(x['status']==k for x in rows) for k in ['pass','fail','unsupported','observed','diagnostic_error']};report=dict(schema_version=2,baseline=manifest.get('baseline',suite),suite=suite,scope=manifest.get('scope','required'),candidate=f'N{n}-public',advertised_profile='actor',endpoint=url,peer=None,started_at=start,counts=counts,results=rows,execution_note='Public anonymous sessions; ordinary actor-owned work; no ownership-lifecycle release gate on live services; N7 case starts paced at least five seconds apart; unmodified assertions/timeouts (core5s/query8s)')
   (F/(suite+'.json')).write_text(json.dumps(report,indent=2)+'\n');print('N'+str(n),suite,case['id'],row['status'],row.get('detail','')[:170],flush=True)
 print('N'+str(n),'ACTOR selection complete',flush=True)
