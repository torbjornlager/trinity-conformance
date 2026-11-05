#!/usr/bin/env python3
"""Disposable native peers for real-Chrome browser context transport checks."""
import argparse,hashlib,json,os,socket,subprocess,tempfile,time,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runner'))
from context_release import validate
def port():
    with socket.socket() as s:s.bind(('127.0.0.1',0));return s.getsockname()[1]
def atom(s):return "'"+str(s).replace("'","''")+"'"
def main():
    p=argparse.ArgumentParser(description=__doc__)
    for f in ['swipl','tpl','swi-root','trealla-root','runtime-root','node']:p.add_argument('--'+f,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    ports={n:port() for n in ['swi','trealla','browser']};origin='http://127.0.0.1:'+str(ports['browser'])
    urls={n:('http://localhost:' if n=='swi' else 'http://127.0.0.1:')+str(ports[n]) for n in ['swi','trealla']};children=[];logs=[]
    env=dict(os.environ)
    for key in ['WP_CONFIG_FILE','SWI_HOME_DIR','SWIPL_HOME_DIR','WP_NATIVE_STATE','WP_NATIVE_MODE']:env.pop(key,None)
    driver=ROOT/'adapters/browser_native_context.cjs'
    inputs={str(driver):hashlib.sha256(driver.read_bytes()).hexdigest()}
    for root in [Path(a.swi_root),Path(a.trealla_root)]:
      files=(root/'prolog').rglob('*.pl') if root==Path(a.swi_root) else root.glob('*.pl')
      inputs.update({str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in files})
    try:
      with tempfile.TemporaryDirectory(prefix='browser-context-peers-') as tmp:
        tmp=Path(tmp);credentials=tmp/'credentials.json';swi=tmp/'swi.pl'
        options=f"profile(actor),auth(open),ws_allowed_origins([{atom(origin)}]),max_ws_actors_per_principal(256),max_principal_actors(256),max_call_requests_per_window(1000),peer_transport_tokens([{','.join(atom(u)+'-Peer' for u in urls.values())}])"
        swi.write_text(f":- use_module({atom(Path(a.swi_root)/'prolog/web_prolog.pl')}).\n:- use_module(library(http/json)).\n:- initialization(main,main).\nmain:-node_tokens:issue_token(\"node:browser-context\",[execute,internal_transport],[],PeerString),atom_string(Peer,PeerString),open({atom(credentials)},write,S),json_write_dict(S,_{{peer:Peer}}),close(S),node({ports['swi']},[{options}]),thread_get_message(stop).\n")
        def start(name,command,cwd,extra=None):
          log=(a.output/(name+'.txt')).open('w');logs.append(log)
          child=subprocess.Popen(command,cwd=cwd,env=dict(env,**(extra or {})),stdout=log,stderr=subprocess.STDOUT);children.append(child)
          for _ in range(200):
            if child.poll() is not None:raise RuntimeError(name+' fixture exited')
            try:
              with socket.create_connection(('127.0.0.1',ports[name]),timeout=.1):return
            except OSError:time.sleep(.03)
          raise TimeoutError(name+' readiness')
        start('swi',[a.swipl,'-f','none','-q',str(swi)],a.swi_root)
        peer=json.loads(credentials.read_text())['peer'];tpl=tmp/'trealla.pl'
        tpl.write_text(f":- use_module(distribution).\nmain:-web_prolog:web_prolog_node({ports['trealla']},[ws_allowed_origins([{atom(origin)}]),max_call_requests_per_window(1000),peer_transport_tokens([{','.join(atom(u)+'-'+atom(peer) for u in urls.values())}]),bearer_token('node:browser-context',{atom(peer)},[execute,internal_transport])]).\n")
        start('trealla',[a.tpl,'-g',f'consult({atom(tpl)}),main'],a.trealla_root,{'TPL_LIBRARY_PATH':str(Path(a.tpl).parent/'library')})
        driver=ROOT/'adapters/browser_native_context.cjs';e=dict(env,BROWSER_CONTEXT_PEERS=json.dumps(urls),BROWSER_CONTEXT_PORT=str(ports['browser']),LIBRARY_RUNTIME_ROOT=a.runtime_root,LIBRARY_REPORT=str(a.output/'results.json'))
        with (a.output/'browser.txt').open('w') as log:r=subprocess.run([a.node,str(driver)],cwd=ROOT,env=e,stdout=log,stderr=subprocess.STDOUT,timeout=240)
        provenance={'driver_sha256':hashlib.sha256(driver.read_bytes()).hexdigest(),'runtime_manifest':json.loads((Path(a.runtime_root)/'manifest.json').read_text()),'native_sources':{}}
        for mode,root in [('swi',Path(a.swi_root)),('trealla',Path(a.trealla_root))]:
          provenance['native_sources'][mode]={'revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'files_sha256':{str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted((root/'prolog').rglob('*.pl') if mode=='swi' else root.glob('*.pl'))}}
        unchanged=all(hashlib.sha256(Path(f).read_bytes()).hexdigest()==sha for f,sha in inputs.items())
        provenance['inputs_unchanged_during_run']=unchanged
        expected=[dict(candidate='swi-wasm-'+mode,id=f'BN-{number:03}-'+peer) for mode in ['worker','main'] for peer in ['swi','trealla'] for number in range(1,12)]
        try:
          validate(json.loads((a.output/'results.json').read_text()),expected)
          if r.returncode:raise ValueError('browser adapter exited nonzero')
          provenance['selection_status']='pass'
        except (OSError,ValueError,KeyError) as error:
          provenance['selection_status']='fail';provenance['selection_error']=str(error)
        if not unchanged:provenance['invalidated']='source or driver changed during active fixture execution'
        (a.output/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n');return (0 if provenance['selection_status']=='pass' else 1) if unchanged else 2
    finally:
      for c in reversed(children):
        c.terminate()
        try:c.wait(timeout=5)
        except subprocess.TimeoutExpired:c.kill();c.wait()
      for log in logs:log.close()
if __name__=='__main__':raise SystemExit(main())
