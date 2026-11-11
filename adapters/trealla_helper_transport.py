#!/usr/bin/env python3
"""Real WebSocket helper admission, ownership and source-fetch boundaries."""
import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import threading
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runner'))
from run import Candidate,Harness,prolog_quote_atom,row_value
from local_runtime_contracts import free_port as port

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tpl',required=True)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=False)
    requests=[]
    class Source(BaseHTTPRequestHandler):
        def do_GET(self):
            requests.append(self.path)
            text=('ha_uri_child(To):-current_prolog_flag(bounded,_),To!ha_uri_ok.'
                  if self.path=='/forbidden.pl' else 'ha_uri_child(To):-To!ha_uri_ok.')
            raw=text.encode()
            self.send_response(200)
            self.send_header('Content-Length',str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Source)
    thread=threading.Thread(target=server.serve_forever,daemon=True)
    thread.start()
    origin=f'http://127.0.0.1:{server.server_port}'
    n=port()
    url=f'http://127.0.0.1:{n}'
    env=dict(os.environ,TPL_LIBRARY_PATH=str(Path(args.tpl).parent/'library'))
    command=[args.tpl,'-g',f"use_module(distribution),web_prolog:web_prolog_node({n},[bind_address('127.0.0.1'),profile(actor),sandbox(whitelist),auth(open),max_ws_commands_per_window(1000),load_uri_allowed_origins(['{origin}']),load_uri_allowed_ip_ranges(['127.0.0.0/8'])])"]
    rows=[]
    def check(case_id,title,operation):
        before=len(requests)
        row=dict(candidate='trealla',id=case_id,title=title)
        try:row.update(status='pass',observation=operation())
        except Exception as error:row.update(status='fail',detail=str(error))
        row['source_requests']=requests[before:]
        rows.append(row)
        print(case_id,row['status'],flush=True)
    def harness():
        return Harness(Candidate(f'ws://127.0.0.1:{n}/ws','actor',8,None,url,False,()))
    def query(h,goal,options='[limit(1)]'):
        h.call('('+goal+'),HelperCheck=passed',options)
        event=h.recv()
        if event.get('type')!='success' or event.get('more') is not False or row_value(event,'HelperCheck')!='passed':
            raise AssertionError(event)
        return event
    def denied(h,goal,error_name,options='[limit(1)]'):
        before=len(requests)
        h.call(goal,options)
        event=h.recv()
        if event.get('type')!='error' or error_name not in str(event):raise AssertionError(event)
        if len(requests)!=before:raise AssertionError('Admission fetched source before rejecting the call')
        return event
    try:
      with (args.output/'node.log').open('w+') as log:
        node=subprocess.Popen(command,cwd=args.root,env=env,stdout=log,stderr=subprocess.STDOUT)
        try:
          for _ in range(200):
            if node.poll() is not None:
                log.seek(0)
                raise RuntimeError(log.read())
            try:
                with socket.create_connection(('127.0.0.1',n),timeout=.1):break
            except OSError:time.sleep(.03)
          else:raise TimeoutError('node startup')
          with harness() as h:
            original=h.spawn_shell("[session(true),src_text('ha_parent(a). ha_parent(b). ha_parent(c).')]")
            def pagination():
                h.call('ha_parent(V)','[limit(2)]')
                first=h.recv()
                if first.get('type')!='success' or first.get('data')!=[{'V':'a'},{'V':'b'}] or first.get('more') is not True:raise AssertionError(first)
                h.next()
                last=h.recv()
                if last.get('type')!='success' or last.get('data')!=[{'V':'c'}] or last.get('more') is not False:raise AssertionError(last)
                return [first,last]
            check('HT-001','Retained private helper paginates without binding caller state',pagination)
            for i,option in enumerate(["src_text('ha_forged.')",'src_list([ha_forged])','src_predicates([ha_forged/0])',f"src_uri('{origin}/allowed.pl')"],2):
                check(f'HT-{i:03}','Call options cannot confer private helper membership',lambda o=option:denied(h,'ha_forged','domain_error(toplevel_call_option','['+o+']'))
            check('HT-006','Unknown helpers remain denied',lambda:denied(h,'ha_unknown','not_whitelisted'))
            check('HT-007','Runtime/bootstrap definitions are not public helper names',lambda:denied(h,"'$actor_source_pi'(_)",'permission_error'))
            check('HT-008','Explicit module qualification cannot enter node internals',lambda:denied(h,'isolation:actor_application_predicates(any,_)','module_qualification'))
            check('HT-009','A known forbidden child operation is denied before URI fetching',lambda:denied(h,f"spawn(current_prolog_flag(bounded,_),_,[src_uri('{origin}/allowed.pl')])",'permission_error'))
            def uri_child():
                before=len(requests)
                result=query(h,f"self(Me),spawn(ha_uri_child(Me),P,[src_uri('{origin}/allowed.pl'),monitor(true)]),receive({{ha_uri_ok->true}},[timeout(2),on_timeout(throw(helper_transport_message_missing))]),receive({{down(P,P,true)->true}},[timeout(2),on_timeout(throw(helper_transport_message_missing))])")
                if requests[before:]!=['/allowed.pl']:raise AssertionError(requests[before:])
                return result
            check('HT-010','Caller fetches a URI child source once and validates its helper',uri_child)
            def forbidden_body():
                before=len(requests)
                h.call(f"spawn(ha_uri_child(_),_,[src_uri('{origin}/forbidden.pl')])",'[limit(1)]')
                event=h.recv()
                if event.get('type')!='error' or 'permission_error' not in str(event):raise AssertionError(event)
                if requests[before:]!=['/forbidden.pl']:raise AssertionError(requests[before:])
                return event
            check('HT-011','Fetched helper bodies are still validated before child execution',forbidden_body)
            check('HT-012','Session remains usable after rejected helper calls',lambda:query(h,'ha_parent(a)'))
            h.spawn_shell('[session(true)]')
            check('HT-013','Another session on the same connection cannot inherit helper names',lambda:denied(h,'ha_parent(a)','not_whitelisted'))
            with harness() as other:
                other.spawn_shell('[session(true)]')
                def foreign():
                    before=len(requests)
                    other.send(dict(command='toplevel_call',pid=original,goal='ha_parent(V)',options=f"[src_uri('{origin}/allowed.pl')]"))
                    event=other.recv()
                    if event.get('type')!='error' or 'permission_error(access,web_prolog_actor' not in str(event):raise AssertionError(event)
                    if len(requests)!=before:raise AssertionError('Foreign request fetched source')
                    return event
                check('HT-014','Foreign session ownership is checked before private lookup or source work',foreign)
            h.shell=original
            check('HT-015','The original session retains its own helper definitions',lambda:query(h,'ha_parent(c)'))
        finally:
            node.terminate()
            try:node.wait(timeout=5)
            except subprocess.TimeoutExpired:node.kill();node.wait()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
    report=dict(suite='trealla-helper-transport-0.1',adapter_sha256=sha(__file__),helpers_sha256={f:sha(ROOT/f) for f in ['runner/run.py','adapters/local_runtime_contracts.py']},
                sources=dict(root=str(args.root.resolve()),
                             executable_sha256=sha(args.tpl),files_sha256={str(p.relative_to(args.root)):sha(p) for p in sorted(args.root.glob('*.pl'))+sorted((args.root/'fixtures/source').glob('*.pl'))}),
                results=rows,counts={s:sum(r['status']==s for r in rows) for s in ['pass','fail']})
    (args.output/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    return int(any(r['status']=='fail' for r in rows))


if __name__=='__main__':raise SystemExit(main())
