#!/usr/bin/env python3
"""Run current shared ISOBASE/HTTP packs on disposable SWI and GNU fixtures.

The older GNU ISOBASE 0.2 draft is a separate, retained comparison target;
its code-list and host-extension expectations do not define today's manual.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import select
import signal
import socket
import subprocess
import sys
import tempfile
import time
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def atom(s):return "'"+str(s).replace("'","''")+"'"
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--swipl',default=os.environ.get('SWIPL','swipl'))
 p.add_argument('--demonstrator-root',type=Path,default=ROOT.parent/'trinity-demonstrator')
 p.add_argument('--gnu-root',type=Path,default=ROOT.parent/'gprolog-port')
 p.add_argument('--output',type=Path,required=True)
 a=p.parse_args();a.output=a.output.resolve();a.output.mkdir(parents=True,exist_ok=False)
 demo=a.demonstrator_root.resolve();gnu=a.gnu_root.resolve();runs=[];procs=[];logs=[]
 env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
 setup=json.loads(subprocess.check_output([sys.executable,str(demo/'tools/setup_swi.py'),'--validate'],env=env,text=True))
 inputs=[ROOT/'cases/isobase-http-0.1.json',ROOT/'cases/interop-http-0.1.json',ROOT/'runner/baseline.py',Path(__file__),demo/'web/manual.html']
 provenance={'selection':'current manual; scoped shared ISOBASE and HTTP interoperability',
  'not_selected':'historical GNU ISOBASE 0.2 draft; no ISO certification claim',
  'started_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'runs':runs,
  'setup':setup,'inputs':{str(f):sha(f) for f in inputs},'nodes':{}}
 try:
  with tempfile.TemporaryDirectory(prefix='current-isobase-') as temporary:
   t=Path(temporary);policy=t/'outbound.policy';policy.touch(mode=0o600)
   with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
   goal=(f"consult({atom(demo/'load.pl')}),set_setting(http:public_host,'127.0.0.1'),set_setting(http:public_port,{port}),set_setting(http:public_scheme,http),"
    f"node:node({port},[profile(isobase),sandbox(blacklist),auth(open),max_call_requests_per_window(1000),ip('127.0.0.1')]),thread_get_message(stop)")
   log=(a.output/'swi-node.log').open('w');logs.append(log)
   proc=subprocess.Popen([a.swipl,'-f','none','-q','-g',goal],cwd=demo,env=env,stdout=log,stderr=log,start_new_session=True);procs.append(proc)
   for _ in range(200):
    if proc.poll() is not None:raise RuntimeError('SWI fixture startup failed')
    try:
     with socket.create_connection(('127.0.0.1',port),.1):break
    except OSError:time.sleep(.025)
   else:raise TimeoutError('SWI fixture startup')
   node=gnu/'isobase/isobase-node';log=(a.output/'gnu-node.log').open('w');logs.append(log)
   proc=subprocess.Popen([str(node),'--auth','open','--port','0','--time-ms','5000','--outbound-policy',str(policy)],cwd=gnu/'isobase',env=env,stdout=subprocess.PIPE,stderr=log,text=True,start_new_session=True);procs.append(proc)
   if not select.select([proc.stdout],[],[],10)[0]:raise TimeoutError('GNU fixture startup')
   gp=json.loads(proc.stdout.readline())['port'];nodes={'swi':f'http://127.0.0.1:{port}','gnu':f'http://127.0.0.1:{gp}'}
   policy.write_text(''.join(f'http 127.0.0.1 {u.rsplit(":",1)[1]} 127.0.0.1\n' for u in nodes.values()));policy.chmod(0o600)
   provenance['nodes']=nodes;provenance['gnu_binary_sha256']=sha(node)
   for name,url in nodes.items():
    for suite,peer in [('isobase-http',None),*[('interop-http',other) for other in nodes]]:
     label=name+'-'+suite+('-to-'+peer if peer else '');report=label+'.json'
     cmd=[sys.executable,str(ROOT/'runner/baseline.py'),'--manifest',str(ROOT/'cases'/(suite+'-0.1.json')),'--url',url,'--candidate',name,'--profile','isobase','--report',str(a.output/report)]
     if peer:cmd+=['--peer',nodes[peer]]
     with (a.output/(label+'.log')).open('w') as f:r=subprocess.run(cmd,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=120)
     runs.append({'label':label,'exit_code':r.returncode,'report':report if (a.output/report).exists() else None});print(label,r.returncode,flush=True)
 finally:
  for proc in reversed(procs):
   if proc.poll() is None:os.killpg(proc.pid,signal.SIGTERM)
   try:proc.wait(3)
   except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
  for log in logs:log.close()
  (a.output/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
 passed=bool(runs) and len(runs)==6 and all(row['exit_code']==0 and row['report'] for row in runs)
 total={key:0 for key in ['pass','fail','unsupported','observed','diagnostic_error']}
 for row in runs:
  if row['report']:
   report=json.loads((a.output/row['report']).read_text())
   for key,value in report['counts'].items():total[key]+=value
   passed=passed and report['counts']['fail']==0 and report['counts']['unsupported']==0
 (a.output/'summary.json').write_text(json.dumps({'passed':passed,'counts':total,'scope':provenance['selection']},indent=2)+'\n')
 return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
