from pathlib import Path
import json,urllib.request,urllib.parse,secrets,time,hashlib
O=Path(__file__).resolve().parent
raw=(O.parents[1]/'cases/standard-library-0.1.json').read_bytes();pack=json.loads(raw);rows=[]
for n in range(1,7):
 for offset in range(0,len(pack['cases']),8):
  cases=pack['cases'][offset:offset+8]
  # findall gives each shared assertion its original independent variable scope.
  goal=','.join('findall(passed,('+c['goal']+'),[passed])' for c in cases)+',LibraryCheck=passed'
  params=dict(goal=goal,src_text=pack['source'],template='LibraryCheck',format='prolog',limit=1)
  req=urllib.request.Request(f'https://n{n}.elfenbenstornet.se/call?'+urllib.parse.urlencode(params),headers={'X-Web-Prolog-Query-Owner':secrets.token_hex(32)})
  time.sleep(1.5)
  try:
   with urllib.request.urlopen(req,timeout=30) as response:body=response.read().decode()
   assert ''.join(body.split())=='success([passed],false).',body
   for c in cases:rows.append(dict(node=n,id=c['id'],status='pass'))
  except Exception as e:
   for c in cases:rows.append(dict(node=n,id=c['id'],status='fail',detail=str(e)))
  (O/'public-library.json').write_text(json.dumps(dict(scope='All shared library assertions on public N1-N6, with private source; batches use independent findall scopes',manifest_sha256=hashlib.sha256(raw).hexdigest(),results=rows,counts={s:sum(r['status']==s for r in rows) for s in ['pass','fail']}),indent=2)+'\n')
  print('N'+str(n),[c['id'] for c in cases],rows[-1]['status'],flush=True)
raise SystemExit(any(r['status']=='fail' for r in rows))
