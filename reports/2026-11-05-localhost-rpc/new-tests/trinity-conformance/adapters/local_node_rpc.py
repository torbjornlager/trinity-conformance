#!/usr/bin/env python3
"""Run shared localhost assertions on disposable nodes, never live services."""
import argparse,hashlib,http.server,json,os,socket,subprocess,sys,tempfile,threading,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runner'))
from baseline import http_case

def atom(x):return "'"+str(x).replace("'","''")+"'"
def port():
    with socket.socket() as s:s.bind(('127.0.0.1',0));return s.getsockname()[1]
class Source(http.server.BaseHTTPRequestHandler):
    def log_message(self,*a):pass
    def do_GET(self):
        self.send_response(200);self.end_headers();self.wfile.write(b'local_node_loaded(one). local_node_loaded(two).')
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--swi-root',type=Path,required=True);p.add_argument('--trealla-root',type=Path,required=True)
    p.add_argument('--gnu-node',type=Path,required=True);p.add_argument('--tpl',required=True);p.add_argument('--swipl',required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():p.error('output must be a new file')
    source=http.server.ThreadingHTTPServer(('127.0.0.1',0),Source);thread=threading.Thread(target=source.serve_forever);thread.start()
    peer=f'http://127.0.0.1:{source.server_port}';pack=json.loads((ROOT/'cases/local-node-rpc-0.1.json').read_text().replace('__PEER__',peer))
    rows=[];sources={}
    try:
      with tempfile.TemporaryDirectory(prefix='localhost-contract-') as d:
        for name in ['swi','trealla','gnu']:
          n=port();url=f'http://127.0.0.1:{n}';env=os.environ.copy()
          if name=='swi':
            root=a.swi_root;goal=f"use_module({atom(root/'prolog/web_prolog.pl')}),node({n},[profile(actor),auth(open),load_uri_allowed_origins([{atom(peer)}]),load_uri_allowed_ip_ranges(['127.0.0.0/8'])]),thread_get_message(stop)"
            cmd=[a.swipl,'-f','none','-q','-g',goal]
          elif name=='trealla':
            root=a.trealla_root;env['TPL_LIBRARY_PATH']=str(Path(a.tpl).parent/'library')
            cmd=[a.tpl,'-g',f"use_module(web_prolog),web_prolog_node({n},[node_url('https://advertised.invalid'),load_uri_allowed_origins([{atom(peer)}]),load_uri_allowed_ip_ranges(['127.0.0.0/8'])])"]
          else:
            root=a.gnu_node.parent.parent;policy=Path(d)/'policy';policy.write_text(f'http 127.0.0.1 {n} 127.0.0.1\nhttp 127.0.0.1 {source.server_port} 127.0.0.1\n');policy.chmod(0o600)
            env['ISO_OUTBOUND_POLICY']=str(policy);cmd=[str(a.gnu_node),'--auth','open','--port',str(n),'--time-ms','2000']
          sources[name]={'root':str(root),'revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'diff_sha256':hashlib.sha256(subprocess.check_output(['git','diff'],cwd=root)).hexdigest(),'executable':cmd[0],'executable_sha256':hashlib.sha256(Path(cmd[0]).read_bytes()).hexdigest()}
          changed=subprocess.check_output(['git','ls-files','-m','-o','--exclude-standard','-z'],cwd=root).split(b'\0')
          sources[name]['changed_files']={os.fsdecode(n):hashlib.sha256((root/os.fsdecode(n)).read_bytes()).hexdigest() for n in changed if n and (root/os.fsdecode(n)).is_file()}
          with open(Path(d)/(name+'.txt'),'w+') as log:
            node=subprocess.Popen(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
            try:
              for _ in range(100):
                if node.poll() is not None:log.seek(0);raise RuntimeError(log.read())
                try:
                  with socket.create_connection(('127.0.0.1',n),timeout=.1):break
                except OSError:time.sleep(.05)
              else:raise RuntimeError(name+' did not start')
              for case in pack['cases']:
                row={'candidate':name,'id':case['id'],'title':case['title']}
                try:row.update(status='pass',observation=http_case(case,url,8,None,False))
                except Exception as e:row.update(status='fail',detail=str(e))
                rows.append(row);print(name,case['id'],row['status'],flush=True)
            finally:node.terminate();node.wait(timeout=8)
    finally:source.shutdown();source.server_close();thread.join()
    report={'suite':pack['suite'],'scope':'shared assertions through disposable local HTTP nodes; explicit fixture-only loopback grants; development sources','sources':sources,'results':rows,'counts':{s:sum(r['status']==s for r in rows) for s in ['pass','fail']}}
    a.output.write_text(json.dumps(report,indent=2)+'\n');return int(report['counts']['fail']>0)
if __name__=='__main__':raise SystemExit(main())
