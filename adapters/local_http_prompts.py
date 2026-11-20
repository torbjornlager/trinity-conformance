"""Run the prompt pack on disposable SWI/Trealla nodes with explicit routes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runner'))
from run import prolog_quote_atom


def free_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1',0))
        return sock.getsockname()[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--swipl',required=True)
    parser.add_argument('--tpl',required=True)
    parser.add_argument('--swi-root',type=Path,required=True)
    parser.add_argument('--trealla-root',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    args.swi_root=args.swi_root.resolve(strict=True)
    args.trealla_root=args.trealla_root.resolve(strict=True)
    args.output.mkdir(parents=True,exist_ok=False)
    nodes=[];logs=[];urls={};provenance={}
    try:
        for engine,root,binary in [('swi',args.swi_root,args.swipl),('trealla',args.trealla_root,args.tpl)]:
            port=free_port();base=f'http://127.0.0.1:{port}';urls[engine]=base
            options='profile(actor),auth(open),max_call_requests_per_window(100000),max_session_spawns_per_window(100000)'
            env=dict(os.environ)
            for key in ['WP_CONFIG_FILE','SWI_HOME_DIR','SWIPL_HOME_DIR','WP_NATIVE_MODE','WP_NATIVE_STATE']:
                env.pop(key,None)
            if engine=='swi':
                goal=f'use_module({prolog_quote_atom(str(root/"prolog/web_prolog.pl"))}),node({port},[{options}]),thread_get_message(stop)'
                command=[binary,'-f','none','-q','-g',goal]
            else:
                # Retained HTTP routes are opt-in on standalone Trealla.
                options+=f',http_sessions(true),node_url({prolog_quote_atom(base)}),bind_address(\'127.0.0.1\')'
                command=[binary,'-g',f'use_module(distribution),web_prolog:web_prolog_node({port},[{options}])']
                env['TPL_LIBRARY_PATH']=str(Path(binary).parent/'library')
            log=(args.output/(engine+'.log')).open('w');logs.append(log)
            proc=subprocess.Popen(command,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT);nodes.append(proc)
            for _ in range(200):
                if proc.poll() is not None:raise RuntimeError(engine+' fixture startup failed')
                try:
                    with socket.create_connection(('127.0.0.1',port),timeout=.1):break
                except OSError:time.sleep(.03)
            else:raise TimeoutError(engine+' fixture startup')
            provenance[engine]=dict(revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
                diff_sha256=hashlib.sha256(subprocess.check_output(['git','diff','HEAD'],cwd=root)).hexdigest(),
                retained_http_enabled=True)
        with (args.output/'runner.txt').open('w') as log:
            result=subprocess.run([sys.executable,str(ROOT/'runner/prompt_http.py'),'--swi',urls['swi'],
                                   '--trealla',urls['trealla'],'--output',str(args.output/'results.json')],
                                  stdout=log,stderr=subprocess.STDOUT,timeout=600)
        report=json.loads((args.output/'results.json').read_text())
        assert len(report['results'])==38
        assert all(row['status']=='pass' for row in report['preconditions'])
        for engine,root in [('swi',args.swi_root),('trealla',args.trealla_root)]:
            assert provenance[engine]['diff_sha256']==hashlib.sha256(subprocess.check_output(['git','diff','HEAD'],cwd=root)).hexdigest()
        (args.output/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
        return result.returncode
    finally:
        for proc in reversed(nodes):
            proc.terminate()
            try:proc.wait(timeout=3)
            except subprocess.TimeoutExpired:proc.kill();proc.wait()
        for log in logs:log.close()


if __name__=='__main__':raise SystemExit(main())
