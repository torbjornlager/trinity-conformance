from pathlib import Path
import hashlib,json,re,secrets,time,urllib.parse,urllib.request
O=Path(__file__).resolve().parent;ROOT=O.parents[1]
pack=json.loads((ROOT/'cases/monitor-contracts-0.1.json').read_text());chosen=['MC-001','MC-003','MC-004','MC-006','MC-015','MC-016','MC-028','MC-031','MC-019','MC-025','LM-001','LM-003'];rows=[]
for n in [3,4,5]:
 for id in chosen:
  c=next(c for c in pack['cases'] if c['id']==id)
  source=(pack['source'] if re.search(r'\bmc_(error|invalid)\(',c['goal']) else '')+'\n'+c.get('source','')
  params=dict(goal='('+c['goal']+'),ReleaseCheck=passed',template='ReleaseCheck',format='prolog',limit=1)
  if source.strip():params['src_text']=source
  url=f'https://n{n}.elfenbenstornet.se/call?'+urllib.parse.urlencode(params)
  row=dict(node=n,id=id)
  time.sleep(1.5)
  try:
   request=urllib.request.Request(url,headers={'X-Web-Prolog-Query-Owner':secrets.token_hex(32)})
   with urllib.request.urlopen(request,timeout=20) as response:body=response.read().decode()
   assert ''.join(body.split())=='success([passed],false).',body
   row.update(status='pass',observation=body)
  except Exception as e:row.update(status='fail',detail=str(e))
  rows.append(row);(O/'public-monitors.json').write_text(json.dumps(dict(scope='Fresh public HTTP requests on N3/N4/N5: selected shared monitor/lifecycle/preflight assertions with necessary private helper source only',manifest_sha256=hashlib.sha256((ROOT/'cases/monitor-contracts-0.1.json').read_bytes()).hexdigest(),results=rows),indent=2)+'\n');print('N'+str(n),id,row['status'],flush=True)
assert len(rows)==36 and all(r['status']=='pass' for r in rows)
