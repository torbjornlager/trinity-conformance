from pathlib import Path
import argparse,json,time,urllib.request,urllib.error,urllib.parse,secrets
p=argparse.ArgumentParser();p.add_argument('--url',required=True);p.add_argument('--host');p.add_argument('--output',type=Path,required=True);p.add_argument('--node',required=True);p.add_argument('--interval',type=float,default=0);a=p.parse_args()
pack=json.loads(Path('/Users/lager/trinity-conformance/cases/http-transport-options-0.1.json').read_text());rows=[]
headers={'X-Web-Prolog-Query-Owner':secrets.token_hex(32)}
if a.host:headers['Host']=a.host
for case in pack['cases']:
 if a.interval:time.sleep(a.interval)
 start=time.monotonic();goal='('+case['goal']+'),ReleaseCheck=passed'
 url=a.url+'/call?'+urllib.parse.urlencode(dict(goal=goal,template='ReleaseCheck',format='prolog',limit=1))
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=15) as response:status=response.status;body=response.read().decode()
  ok=status==200 and ''.join(body.split())=='success([passed],false).'
  row=dict(id=case['id'],status='pass' if ok else 'fail',http_status=status,body=body)
 except Exception as e:row=dict(id=case['id'],status='fail',error=str(e))
 row['duration_ms']=round((time.monotonic()-start)*1000);rows.append(row)
 print(a.node,case['id'],row['status'],flush=True)
report=dict(suite=pack['suite'],candidate=a.node,endpoint=a.url,host=a.host,scope='supporting shared HTTP field assertions through public HTTP admission',counts={s:sum(r['status']==s for r in rows) for s in ['pass','fail']},results=rows)
a.output.write_text(json.dumps(report,indent=2)+'\n');print(report['counts']);raise SystemExit(bool(report['counts']['fail']))
