from pathlib import Path
import json,time,urllib.request,urllib.parse,secrets
O=Path(__file__).resolve().parent
pack=json.loads((O.parents[1]/'cases/local-node-rpc-0.1.json').read_text());rows=[]
def check(n,id,params):
 time.sleep(1.5)
 req=urllib.request.Request(f'https://n{n}.elfenbenstornet.se/call?'+urllib.parse.urlencode(params),headers={'X-Web-Prolog-Query-Owner':secrets.token_hex(32)})
 row=dict(node=n,id=id)
 try:
  with urllib.request.urlopen(req,timeout=15) as response:body=response.read().decode();assert response.status==200
  assert ''.join(body.split())=='success([passed],false).',body
  row.update(status='pass',body=body)
 except Exception as e:row.update(status='fail',detail=str(e))
 rows.append(row);print(n,id,row['status'],flush=True)
 (O/'public-localhost.json').write_text(json.dumps(dict(results=rows,counts={s:sum(r['status']==s for r in rows) for s in ['pass','fail']}),indent=2)+'\n')
for n in range(1,7):
 for case in pack['cases'][:5]:check(n,case['id'],case['requests'][0]['params'])
for n in [5,6]:
 for id,goal in [('RPC-SOURCE',"findall(pair(X,Y),rpc(localhost,ancestor_descendant(X,Y),[src_uri('https://n2.elfenbenstornet.se')]),Rows),length(Rows,6)"),('PROMISE-SOURCE',"promise(localhost,ancestor_descendant(X,Y),R,[src_uri('https://n2.elfenbenstornet.se'),template(pair(X,Y))]),yield(R,success(Rows,false)),length(Rows,6),var(X),var(Y)")]:
  check(n,id,dict(goal='('+goal+'),ReleaseCheck=passed',template='ReleaseCheck',format='prolog',limit=1))
raise SystemExit(any(r['status']=='fail' for r in rows))
