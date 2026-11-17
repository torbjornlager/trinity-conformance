from pathlib import Path
import json,time,urllib.request,urllib.parse,secrets
O=Path(__file__).resolve().parent;pack=json.loads((O.parents[1]/'cases/runtime-introspection-0.1.json').read_text());rows=[]
for n in range(1,7):
 for case in pack['cases']:
  time.sleep(1.5)
  query=urllib.parse.urlencode(dict(goal='('+case['goal']+'),ReleaseCheck=passed',template='ReleaseCheck',format='prolog',limit=1))
  req=urllib.request.Request(f'https://n{n}.elfenbenstornet.se/call?'+query,headers={'X-Web-Prolog-Query-Owner':secrets.token_hex(32)})
  row=dict(candidate=f'N{n}',id=case['id'],title=case['title'])
  try:
   with urllib.request.urlopen(req,timeout=15) as response:body=response.read().decode();assert response.status==200
   assert ''.join(body.split())=='success([passed],false).',body
   row.update(status='pass',body=body)
  except Exception as e:row.update(status='fail',detail=str(e))
  rows.append(row);print(n,case['id'],row['status'],flush=True)
  (O/'public-capabilities.json').write_text(json.dumps(dict(scope='shared capability assertions through live N1-N6 HTTP admission',results=rows,counts={s:sum(r['status']==s for r in rows) for s in ['pass','fail']}),indent=2)+'\n')
raise SystemExit(any(r['status']=='fail' for r in rows))
