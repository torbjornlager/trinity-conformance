from pathlib import Path
import argparse,hashlib,json,sys
O=Path(__file__).resolve().parent;ROOT=O.parents[1];sys.path.insert(0,str(ROOT/'runner'))
from baseline import query_case
p=argparse.ArgumentParser();p.add_argument('--credentials-file',type=Path,required=True);a=p.parse_args()
tokens=json.loads(a.credentials_file.read_text());raw=(ROOT/'cases/monitor-contracts-0.1.json').read_bytes();pack=json.loads(raw);rows=[]
for n,account in [(3,'swi-a'),(4,'swi-b'),(5,'trealla-a')]:
 for c in pack['cases']:
  row=dict(node=n,id=c['id'])
  try:row.update(status='pass',observation=query_case(dict(c,source=pack['source']+'\n'+c.get('source','')),f'wss://n{n}.elfenbenstornet.se/ws',12,tokens[account]))
  except Exception as e:row.update(status='fail',detail=str(e))
  rows.append(row);(O/'public-monitors.json').write_text(json.dumps(dict(scope='All 49 shared monitor assertions on public N3/N4/N5 ACTOR WSS sessions, fresh session per case with temporary execute-only credentials',manifest_sha256=hashlib.sha256(raw).hexdigest(),results=rows),indent=2)+'\n');print('N'+str(n),c['id'],row['status'],flush=True)
assert len(rows)==147 and all(r['status']=='pass' for r in rows)
