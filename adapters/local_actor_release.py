#!/usr/bin/env python3
"""Launch two disposable private loopback candidates and run the ACTOR release gate.

Sources must be explicit archived checkouts in swi/ and trealla/. No installed
service is changed. Execute with the intended engines (e.g. inside a test image).
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import signal
import socket
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def atom(s): return "'"+str(s).replace("'","''")+"'"
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--sources',type=Path,required=True)
 p.add_argument('--output',type=Path,required=True)
 p.add_argument('--engine',choices=['swi','trealla','both'],default='both')
 a=p.parse_args();a.sources=a.sources.resolve();a.output=a.output.resolve();a.output.mkdir(parents=True,exist_ok=False)
 records=[]
 for engine in (['swi','trealla'] if a.engine=='both' else [a.engine]):
  with tempfile.TemporaryDirectory(prefix='actor-release-') as temporary:
   t=Path(temporary)
   with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
   owner=secrets.token_hex(24);observer=secrets.token_hex(24)
   options="profile(actor),sandbox(blacklist),auth(private)"
   if engine=='swi':
    exe=os.environ.get('SWIPL','/usr/bin/swipl');creds=t/'credentials.json'
    source=(f":- consult({atom(a.sources/'swi/load.pl')}).\n:- use_module(library(http/json)).\n"
      f"main :- set_setting(http:public_host,'127.0.0.1'),set_setting(http:public_port,{port}),set_setting(http:public_scheme,http),"
      f"use_module(library(socket)),tcp_socket(S),tcp_bind(S,ip(127,0,0,1):{port}),tcp_listen(S,128),node:node({port},[tcp_socket(S),{options}]),"
      "node_tokens:issue_token(release_owner,[execute],[],A),node_tokens:issue_token(release_observer,[execute],[],B),"
      f"open({atom(creds)},write,O),json_write_dict(O,_{{owner:A,observer:B}}),close(O),thread_get_message(stop).\n")
   else:
    exe=os.environ.get('TPL','/opt/trealla/tpl')
    source=(f":- asserta(user:file_search_path(library,{atom(a.sources/'trealla')})).\n:- use_module({atom(a.sources/'trealla/web_prolog.pl')}).\n"
      f"main :- web_prolog:web_prolog_node({port},[bind_address('127.0.0.1'),node_url('http://127.0.0.1:{port}'),{options},"
      f"bearer_token(release_owner,{atom(owner)},[execute]),bearer_token(release_observer,{atom(observer)},[execute])]),thread_get_message(stop).\n")
   script=t/'fixture.pl';script.write_text(source)
   cmd=[exe,'-f','none','-q','-s',str(script),'-g','main','-t','halt'] if engine=='swi' else [exe,'-q','-f',str(script),'-g','main']
   env=dict(os.environ);env.setdefault('TPL_LIBRARY_PATH','/opt/trealla/library')
   log=(a.output/f'{engine}-node.log').open('w');proc=subprocess.Popen(cmd,cwd=a.sources/engine,env=env,stdout=log,stderr=log,start_new_session=True)
   try:
    for _ in range(200):
     if proc.poll() is not None:raise RuntimeError(f'{engine} node startup failed; see log')
     try:
      if engine=='swi':c=json.loads(creds.read_text());owner=c['owner'];observer=c['observer']
      with socket.create_connection(('127.0.0.1',port),timeout=.1):pass
      break
     except (OSError,json.JSONDecodeError):time.sleep(.05)
    else:raise TimeoutError(f'{engine} node startup')
    env.update(RELEASE_OWNER_TOKEN=owner,RELEASE_OBSERVER_TOKEN=observer)
    gate=[sys.executable,str(ROOT/'runner/release.py'),'--ws-url',f'ws://127.0.0.1:{port}/ws','--candidate',engine,'--token-env','RELEASE_OWNER_TOKEN','--observer-token-env','RELEASE_OBSERVER_TOKEN','--disposable-fixture','--output',str(a.output/engine)]
    with (a.output/f'{engine}-release.log').open('w') as f:
     run=subprocess.run(gate,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=240)
    vcmd=[exe,'--version'] if engine=='swi' else [exe,'-g','current_prolog_flag(version_data,V),writeq(V),nl,halt']
    v=subprocess.run(vcmd,env=env,text=True,capture_output=True,timeout=10)
    records.append(dict(engine=engine,returncode=run.returncode,version=(v.stdout+v.stderr).strip(),executable_sha256=sha(exe),source_hashes={str(f.relative_to(a.sources/engine)):sha(f) for f in (a.sources/engine).rglob('*.pl')},fixture='Disposable private loopback ACTOR; two distinct execution-only principals; secrets excluded'))
    print(engine,'release gate',run.returncode,flush=True)
   finally:
    if proc.poll() is None:os.killpg(proc.pid,signal.SIGTERM)
    try:proc.wait(timeout=5)
    except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
    log.close()
    (a.output/'provenance.json').write_text(json.dumps(dict(engines=records,runner_sha256=sha(ROOT/'runner/release.py'),profile=json.loads((ROOT/'profiles/actor-release-0.1.json').read_text()),inputs={str(f.relative_to(ROOT)):sha(f) for d in ['runner','profiles','cases'] for f in (ROOT/d).rglob('*') if f.is_file() and '__pycache__' not in str(f)}),indent=2)+'\n')
 return int(any(x['returncode']!=0 for x in records))
if __name__=='__main__':raise SystemExit(main())
