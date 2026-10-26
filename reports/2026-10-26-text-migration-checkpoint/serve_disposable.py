import sys,os,json,subprocess,tempfile,time,socket,signal,argparse
from pathlib import Path
sys.path.insert(0,'adapters')
from local_promises import free_port,quote
root=Path('/Users/torbjorn.lager/.local/share/trinity-local-nodes/committed-adoption-2026-10-25')
parser=argparse.ArgumentParser(description='Disposable text-checkpoint UI and peer fixtures; run from conformance root.')
parser.add_argument('--output',type=Path,required=True,help='New evidence directory; never overwrite historical results')
args=parser.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=False);pids=[]
with tempfile.TemporaryDirectory(prefix='text-ui-') as t:
 p=Path(t); (p/'examples').mkdir()
 for n in ['web','img']:(p/n).symlink_to(root/'demonstrator'/n,target_is_directory=True)
 (p/'examples/portable-text.pl').write_text('pt_uri("ab").\n')
 ports={n:free_port() for n in ['swi','trealla']};urls={n:'http://127.0.0.1:'+str(v) for n,v in ports.items()}
 env=dict(os.environ,TPL_LIBRARY_PATH='/Users/torbjorn.lager/Documents/GitHub/trealla-port/.build/trealla-current/library')
 for k in ['SWI_HOME_DIR','SWIPL_HOME_DIR','WP_CONFIG_FILE','WP_ASSET_ROOT','WP_WASM_SOURCE_DIR','WP_NATIVE_STATE','WP_NATIVE_MODE','WP_EXPERIMENTAL_TEXT']:env.pop(k,None)
 try:
  for name in ports:
   if name=='swi':
    goal=f"use_module(library(sgml)),use_module(library(option)),consult({quote(root/'native/load.pl')}),set_setting(node_assets:root,{quote(p)}),set_setting(node_assets:wasm_directory,{quote(root/'demonstrator/.trinity/browser-prolog-38d86f5c618da3af')}),set_setting(http:public_host,'127.0.0.1'),set_setting(http:public_port,{ports[name]}),set_setting(http:public_scheme,http),use_module(library(socket)),tcp_socket(S),tcp_bind(S,ip(127,0,0,1):{ports[name]}),tcp_listen(S,128),node:node({ports[name]},[tcp_socket(S),profile(actor),sandbox(blacklist),auth(open),load_uri_allowed_origins([{quote(urls['swi'])}])]),thread_get_message(stop)"
    cmd=['/Users/torbjorn.lager/.local/share/trinity-runtimes/swi-current/bin/swipl','-f','none','-q','-g',goal];e=dict(env,WP_EXPERIMENTAL_TEXT='portable-text-0.2')
   else:
    goal=f"use_module(web_prolog),use_module(distribution),web_prolog:web_prolog_node({ports[name]},[bind_address('127.0.0.1'),node_url({quote(urls[name])}),profile(actor),sandbox(blacklist),auth(open),trusted_proxy_ranges(['127.0.0.1']),load_uri_allowed_origins([{quote(urls['swi'])}]),load_uri_allowed_ip_ranges(['127.0.0.1'])]),thread_get_message(stop)"
    cmd=['/Users/torbjorn.lager/Documents/GitHub/trealla-port/.build/trealla-current/tpl','-g',goal];e=env
   log=(out/(name+'-ui-node.log')).open('w');proc=subprocess.Popen(cmd,cwd=root/('native' if name=='swi' else 'trealla'),env=e,stdout=log,stderr=log,start_new_session=True);pids.append(proc)
   for _ in range(150):
    if proc.poll() is not None:raise RuntimeError(name+' failed')
    try:
     with socket.create_connection(('127.0.0.1',ports[name]),timeout=.1):break
    except OSError:time.sleep(.05)
   else:raise TimeoutError(name)
  (out/'ui-fixture.json').write_text(json.dumps(dict(urls=urls,pids=[p.pid for p in pids],asset_root=str(p)),indent=2));print(urls,flush=True)
  while not (out/'STOP').exists():time.sleep(.5)
 finally:
  for proc in reversed(pids):
   if proc.poll() is None:
    os.killpg(proc.pid,signal.SIGTERM)
    try:proc.wait(timeout=5)
    except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
