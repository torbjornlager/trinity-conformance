#!/usr/bin/env python3
"""Run the common multi-client naming pack on owned native loopback fixtures."""
import argparse,hashlib,json,os,socket,subprocess,sys,time
from pathlib import Path
from urllib.request import urlopen
from client_naming import ROOT,MANIFEST,Session,execute

def port():
    with socket.socket() as s:s.bind(('127.0.0.1',0));return s.getsockname()[1]
def atom(x):return "'"+str(x).replace("'","''")+"'"
def main():
    p=argparse.ArgumentParser(description=__doc__)
    for f in ['swipl','tpl','swi-root','trealla-root']:p.add_argument('--'+f,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    pack=json.loads(MANIFEST.read_text());rows=[];sources={}
    def save():
        (a.output/'results.json').write_text(json.dumps(dict(suite=pack['suite'],manifest_sha256=hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),sources=sources,results=rows,counts={s:sum(r['status']==s for r in rows) for s in ['pass','fail']}),indent=2)+'\n')
    for name,path in [('swi',a.swi_root),('trealla',a.trealla_root)]:
        root=Path(path);n=port();url=f'ws://127.0.0.1:{n}/ws'
        exe=a.swipl if name=='swi' else a.tpl
        scope=(root/'prolog').rglob('*.pl') if name=='swi' else root.glob('*.pl')
        sources[name]=dict(revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),files_sha256={str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(scope)})
        cmd=[exe,'-q','-g',f"use_module({atom(root/'prolog/web_prolog.pl')}),node({n},[profile(actor),auth(open),max_ws_commands_per_window(10000)]),thread_get_message(stop)"] if name=='swi' else [exe,'-g',f"use_module(distribution),web_prolog:web_prolog_node({n},[bind_address('127.0.0.1'),profile(actor),auth(open)])"]
        env=dict(os.environ)
        if name=='trealla':env['TPL_LIBRARY_PATH']=str(Path(a.tpl).parent/'library')
        with (a.output/(name+'.log')).open('w') as log:
            proc=subprocess.Popen(cmd,cwd=root,env=env,stdout=log,stderr=log)
            try:
                for _ in range(200):
                    if proc.poll() is not None:raise RuntimeError(name+' fixture exited')
                    try:
                        with urlopen(f'http://127.0.0.1:{n}/node_info',timeout=.3):break
                    except OSError:time.sleep(.05)
                else:raise TimeoutError(name+' fixture readiness')
                for c in pack['cases']:
                    rows.append(dict(candidate=name,id=c['id'],title=c['title'],**execute(c,lambda:Session(url,None))))
                    save();print(name,c['id'],rows[-1]['status'],flush=True)
            finally:
                proc.terminate()
                try:proc.wait(timeout=5)
                except subprocess.TimeoutExpired:proc.kill();proc.wait()
    return int(any(r['status']!='pass' for r in rows))
if __name__=='__main__':raise SystemExit(main())
