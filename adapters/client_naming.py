#!/usr/bin/env python3
"""Shared multi-client naming assertions. Endpoints must be disposable or authorized test nodes."""
import argparse,hashlib,json,os,secrets,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runner'))
from run import Candidate,Harness,row_value,set_session_interval
MANIFEST=ROOT/'cases/client-naming-0.1.json'
class Session:
    def __init__(self,url,token):
        self.h=Harness(Candidate(url,'actor',8,token,None,False,()))
        self.closed=False
        try:self.h.__enter__();self.new_toplevel()
        except Exception:self.close();raise
    def new_toplevel(self):self.h.spawn_shell('[session(true)]')
    def query(self,goal):
        self.h.call('('+goal+'),ScopeCheck=passed','[limit(1)]')
        for _ in range(64):
            event=self.h.recv()
            if event.get('type') in ['success','failure','error'] and event.get('pid',self.h.shell)==self.h.shell:
                if event.get('type')!='success' or event.get('more') is not False or row_value(event,'ScopeCheck')!='passed':raise AssertionError(repr(event))
                return event
            self.h.acknowledge_output(event)
        raise AssertionError('missing terminal query answer')
    def close(self):
        if not self.closed:
            self.closed=True
            self.h.__exit__(None,None,None)
def execute(case,create):
    clients={};trace=[]
    try:
        for name in ['a','b']:clients[name]=create()
        unique='cn_'+secrets.token_hex(10)
        for s in case['steps']:
            client=clients[s['client']]
            if s.get('action')=='close':client.close();observed={'closed':True}
            elif s.get('action')=='new_toplevel':client.new_toplevel();observed={'new_toplevel':True}
            else:observed=client.query(s['goal'].replace('__NAME__',unique))
            trace.append(dict(step=s,observation=observed))
        return dict(status='pass',trace=trace)
    except Exception as e:return dict(status='fail',detail=type(e).__name__+': '+str(e),trace=trace)
    finally:
        for client in clients.values():client.close()
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--ws-url',required=True);p.add_argument('--candidate',required=True);p.add_argument('--token-env');p.add_argument('--session-interval',type=float,default=0);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    set_session_interval(a.session_interval);pack=json.loads(MANIFEST.read_text());rows=[];a.output.parent.mkdir(parents=True,exist_ok=True)
    for c in pack['cases']:
        row=dict(candidate=a.candidate,id=c['id'],title=c['title'],**execute(c,lambda:Session(a.ws_url,os.environ[a.token_env] if a.token_env else None)))
        rows.append(row);a.output.write_text(json.dumps(dict(suite=pack['suite'],manifest_sha256=hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),endpoint=a.ws_url,session_interval_seconds=a.session_interval,results=rows,counts={s:sum(r['status']==s for r in rows) for s in ['pass','fail']}),indent=2)+'\n');print(a.candidate,c['id'],row['status'],flush=True)
    return int(any(r['status']!='pass' for r in rows))
if __name__=='__main__':raise SystemExit(main())
