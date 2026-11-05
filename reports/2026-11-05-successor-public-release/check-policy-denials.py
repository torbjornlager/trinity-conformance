"""Verify the three peer additions did not permit arbitrary external origins."""
from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'runner'))
from run import Candidate,Harness
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--credentials-file',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
credentials=json.loads(a.credentials_file.read_text());rows=[]
def terminal(h):
 for _ in range(24):
  e=h.recv();h.acknowledge_output(e)
  if e.get('type') in ['success','failure','error']:return e
 raise RuntimeError('missing terminal result')
for name,n in [('swi-a',3),('swi-b',4),('trealla-a',5)]:
 url=f'https://n{n}.elfenbenstornet.se'
 with Harness(Candidate(url.replace('https:','wss:')+'/ws','actor',10,credentials[name],url,False,())) as h:
  h.spawn_shell('[session(true)]')
  for label,goal,options in [('spawn',"spawn(true,_,[node('https://external.invalid')])",'[limit(1)]'),('source',"rpc(localhost,true,[src_uri('https://external.invalid/probe.pl')])",'[limit(1)]')]:
   h.call(goal,options);event=terminal(h);detail=json.dumps(event)
   ok=event.get('type')=='error' and ('permission_error' in detail or 'No permission' in detail) and 'external.invalid' in detail
   h.call('true','[limit(1)]');recovery=terminal(h);ok=ok and recovery.get('type')=='success'
   rows.append(dict(node=n,id='EXTERNAL-'+label.upper(),status='pass' if ok else 'fail',denial=event,recovery=recovery));print('N'+str(n),label,'pass' if ok else 'FAIL',flush=True)
   a.output.write_text(json.dumps(dict(scope='External spawn/source denial and session recovery on N3-N5 after peer allowlist expansion',results=rows,counts={s:sum(x['status']==s for x in rows) for s in ['pass','fail']}),indent=2)+'\n')
assert len(rows)==6 and all(x['status']=='pass' for x in rows)
