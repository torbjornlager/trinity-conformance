#!/usr/bin/env python3
"""Supplemental public-interface probes. Start disposable ACTOR nodes first.

Example: python3 reports/2026-10-20-focused-probes.py --swi-port 39860 --trealla-port 39861 --report /tmp/recent.json
These are focused diagnostics, not a versioned conformance profile.
"""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runner'))
import run as cr
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--swi-port',type=int,required=True)
parser.add_argument('--trealla-port',type=int,required=True)
parser.add_argument('--report',type=Path,required=True)
args=parser.parse_args()

def public_success(candidate,goal):
 with cr.Harness(candidate) as h:
  h.spawn_shell();h.call(goal,'[limit(1)]')
  events=[]
  for i in range(32):
   e=h.recv()
   if e.get('type')=='down':events.append(e);continue
   cr.require(e.get('type')=='success',f"expected success, got {e!r}")
   cr.require(e.get('more') is False,'unexpected nondeterminism')
   h.halt();return
  raise AssertionError('no answer after child notifications')
extra=[]
def record(name,title,fn):
 try:fn();item=dict(candidate=name,case=title,status='pass')
 except Exception as e:item=dict(candidate=name,case=title,status='fail',error=str(e))
 extra.append(item);print(item,flush=True)
def candidate(port):return cr.Candidate(f'ws://127.0.0.1:{port}/ws','actor',5,None,None,False,())
def http_page(port,params):
 import urllib.request,urllib.parse
 url=f'http://127.0.0.1:{port}/call?'+urllib.parse.urlencode(dict(format='prolog',**params))
 with urllib.request.urlopen(url,timeout=8) as r:return r.read().decode().strip()
for name,port in [('swi',args.swi_port),('trealla',args.trealla_port)]:
 c=candidate(port)
 def http_large():
  first=http_page(port,dict(goal='between(1,1005,X)',template='X',limit=1002));assert first.startswith('success([1,2,3,'),first[:200];assert first.endswith('1001,1002],true).'),first[-100:]
  final=http_page(port,dict(goal='between(1,1005,X)',template='X',limit=1002,offset=1002));assert final=='success([1003,1004,1005],false).',final
  all_=http_page(port,dict(goal='between(1,1005,X)',template='X'));assert all_.endswith('1004,1005],false).'),all_[-100:]
 record(name,'HTTP requested/omitted size and continuation above 1000',http_large)
 record(name,'promise timeout/retry callback and reference consumption',lambda:public_success(c,f"promise('http://127.0.0.1:{port}',(sleep(0.15),X=ok),Ref,[template(X)]),yield(Ref,Early,[timeout(0),on_timeout(Early=waiting)]),Early==waiting,yield(Ref,Answer),Answer==success([ok],false),catch(yield(Ref,_),E,true),nonvar(E),E=error(existence_error(promise,Ref),_)"))
 record(name,'parallel unexpected worker exit',lambda:public_success(c,"catch(parallel([exit(killed)]),Error,true),nonvar(Error),Error=worker_exit(_,killed)"))
 record(name,'first_solution unexpected worker exit with continue',lambda:public_success(c,"first_solution(X,[exit(killed),(sleep(0.1),X=ok)],[on_error(continue)]),X==ok"))
 record(name,'promise failure answer and invalid reference',lambda:public_success(c,f"promise('http://127.0.0.1:{port}',fail,Ref),yield(Ref,Answer),Answer==failure,catch(yield(42,_),E,true),nonvar(E),E=error(existence_error(promise,42),_)"))
 def server_setup():
  source="echo(Request,State,Request,State)."
  goal="server_spawn(echo,[],P),self(Self),monitor(P,Other),catch(server_promise(P,unused,0,_),E,true),var(E),demonitor(Other,[flush]),server_promise(P,hello,Ref,Mon),server_yield(Ref,Mon,Reply,[]),Reply==hello,server_halt(P,_)"
  # Failure of setup is semidet; explicitly require failure before continuing.
  goal=goal.replace('catch(server_promise(P,unused,0,_),E,true),var(E)','\\+server_promise(P,unused,0,_)')
  cr.require_source_goal_success(c,source,goal)
 record(name,'server promise failed setup followed by successful monitored request',server_setup)
 def ptcp_large():
  with cr.Harness(c) as h:
   h.spawn_shell();h.call('between(1,2005,X)','[limit(1002)]');a=h.recv('success');assert len(a['data'])==1002 and a['more'] is True
   h.send({'command':'toplevel_next','pid':h.shell,'limit':1001});b=h.recv('success');assert len(b['data'])==1001 and b['data'][0]['X']=='1003' and b['more'] is True,('second page',len(b['data']),b.get('more'))
   h.next();d=h.recv('success');assert [x['X'] for x in d['data']]==['2004','2005'] and d['more'] is False,('last page',len(d['data']),d.get('more'))
   h.halt()
 record(name,'WebSocket PTCP initial and changed next sizes above 1000',ptcp_large)
args.report.write_text(json.dumps(extra,indent=2)+'\n')
