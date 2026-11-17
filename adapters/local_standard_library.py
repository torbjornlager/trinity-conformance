#!/usr/bin/env python3
"""Shared Appendix B library checks on disposable native nodes; no live changes."""
import argparse,hashlib,json,os,socket,subprocess,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runner'))
from baseline import http_case
from run import Candidate,Harness,prolog_quote_atom
from library_prefix import http_prefix,session_prefix

def port():
    with socket.socket() as s:s.bind(('127.0.0.1',0));return s.getsockname()[1]
def atom(s):return "'"+str(s).replace("'","''")+"'"
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--swipl',required=True);p.add_argument('--tpl',required=True)
    p.add_argument('--swi-root',type=Path,required=True);p.add_argument('--trealla-root',type=Path,required=True)
    p.add_argument('--gnu-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--manifest',type=Path,default=ROOT/'cases/standard-library-0.1.json')
    p.add_argument('--only',nargs='+',choices=['swi','trealla','gnu'],default=['swi','trealla','gnu'])
    a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    pack=json.loads(a.manifest.read_text());rows=[];sources={}
    for name in a.only:
      root=getattr(a,name+'_root');n=port();url=f'http://127.0.0.1:{n}';env=os.environ.copy()
      for key in ['WP_CONFIG_FILE','SWI_HOME_DIR','SWIPL_HOME_DIR','WP_NATIVE_STATE','WP_NATIVE_MODE']:env.pop(key,None)
      if name=='swi':cmd=[a.swipl,'-f','none','-q','-g',f"use_module({atom(root/'prolog/web_prolog.pl')}),node({n},[profile(actor),auth(open),max_call_requests_per_window(1000)]),thread_get_message(stop)"]
      elif name=='trealla':
        env['TPL_LIBRARY_PATH']=str(Path(a.tpl).parent/'library')
        cmd=[a.tpl,'-g',f'use_module(distribution),web_prolog:web_prolog_node({n},[max_call_requests_per_window(1000)])']
      else:cmd=[str(root/'isobase/isobase-node'),'--auth','open','--port',str(n),'--time-ms','3000']
      sources[name]=dict(revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),diff_sha256=hashlib.sha256(subprocess.check_output(['git','diff'],cwd=root)).hexdigest(),executable=cmd[0],executable_sha256=sha(cmd[0]))
      scope=root/'prolog' if name=='swi' else root/'isobase' if name=='gnu' else root
      files=scope.rglob('*.pl') if name=='swi' else scope.glob('*')
      sources[name]['files_sha256']={str(f.relative_to(root)):sha(f) for f in sorted(files) if f.is_file() and f.suffix in ('.pl','.c','.h')}
      if name=='gnu':sources[name]['worker_binaries_sha256']={f:sha(scope/f) for f in ['query-worker','query-supervisor']}
      if name=='trealla':
        libs=Path(a.tpl).parent/'library'
        sources[name]['engine_library_sha256']=hashlib.sha256(''.join(str(f.relative_to(libs))+':'+sha(f)+'\n' for f in sorted(libs.rglob('*')) if f.is_file()).encode()).hexdigest()
      with (a.output/(name+'.log')).open('w+') as log:
        node=subprocess.Popen(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
        try:
          for _ in range(150):
            if node.poll() is not None:log.seek(0);raise RuntimeError(log.read())
            try:
              with socket.create_connection(('127.0.0.1',n),timeout=.1):break
            except OSError:time.sleep(.03)
          else:raise TimeoutError(name+' startup')
          for case in pack['cases']:
            row=dict(candidate=name,id=case['id'],title=case['title'])
            wire=dict(requests=[dict(params=dict(goal='('+case['goal']+'),LibraryCheck=passed',template='LibraryCheck',format='prolog',limit=1,src_text=pack['source']),expect_prolog='success([passed],false).')])
            try:row.update(status='pass',observation=http_prefix(case,pack['source'],url) if case.get('bounded_prefix') else http_case(wire,url,8,None,False))
            except Exception as e:row.update(status='fail',detail=str(e))
            rows.append(row);print(name,case['id'],row['status'],flush=True)
          if name != 'gnu':
            with Harness(Candidate(f'ws://127.0.0.1:{n}/ws','actor',8,None,url,False,())) as h:
              h.spawn_shell('[session(true),src_text('+prolog_quote_atom(pack['source'])+')]')
              for case in pack['cases']:
                row=dict(candidate=name+'-session',id=case['id'],title=case['title'])
                try:
                  if case.get('bounded_prefix'):
                    row.update(status='pass',observation=session_prefix(case,h))
                    rows.append(row);print(name+'-session',case['id'],row['status'],flush=True)
                    continue
                  h.call('('+case['goal']+'),LibraryCheck=passed','[limit(1)]')
                  event=h.recv()
                  if event.get('type')!='success' or event.get('more') is not False:raise AssertionError(event)
                  row.update(status='pass',observation=event)
                except Exception as e:row.update(status='fail',detail=str(e))
                rows.append(row);print(name+'-session',case['id'],row['status'],flush=True)
        finally:
          node.terminate()
          try:node.wait(timeout=5)
          except subprocess.TimeoutExpired:node.kill();node.wait()
    report=dict(suite=pack['suite'],scope='Shared source and goals through fresh native HTTP workers; development source snapshots',manifest_sha256=sha(a.manifest),adapter_sha256=sha(__file__),prefix_helper_sha256=sha(ROOT/'runner/library_prefix.py'),sources=sources,results=rows,counts={s:sum(r['status']==s for r in rows) for s in ['pass','fail']})
    (a.output/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    return int(report['counts']['fail']>0)
if __name__=='__main__':raise SystemExit(main())
