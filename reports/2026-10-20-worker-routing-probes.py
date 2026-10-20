#!/usr/bin/env python3
"""Check public worker routing on an already-running disposable ACTOR node.

Uses the shared external WebSocket harness. This is a focused regression probe,
not a new formal conformance profile. It does not start or stop the node.
"""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runner'))
import run as cr
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--port',type=int,required=True)
parser.add_argument('--report',type=Path,required=True)
args=parser.parse_args()

results=[]
for name,port in [('trealla',args.port)]:
 c=cr.Candidate(f'ws://127.0.0.1:{port}/ws','actor',5,None,None,False,())
 for sources in [False,True]:
  tests=[('parallel bindings','parallel([X=one,Y=two]),X==one,Y==two'),
    ('first_solution/2','first_solution(X,[X=fast,(sleep(0.1),X=slow)]),X==fast'),
    ('first_solution/3 continue','first_solution(X,[exit(killed),(sleep(0.1),X=ok)],[on_error(continue)]),X==ok'),
    ('caught worker exit','catch(parallel([exit(killed)]),E,true),nonvar(E),E=worker_exit(_,killed)'),
    ('compound and unrelated mailbox','self(Self),Self!down(other,unrelated,normal),parallel([X=one]),X==one,receive({down(other,unrelated,normal)->true})'),
    ('worker actor primitives','parallel([(self(Me),Me!hello,receive({hello->true}))])')]
  if sources:tests.append(('private worker source','parallel([probe(X)]),X==ok,first_solution(Y,[probe(Y)]),Y==ok'))
  if name=='trealla':tests.extend([('parallel sandbox denial',"parallel([shell('true')])"),('first_solution sandbox denial',"first_solution(_,[shell('true')])")])
  for title,goal in tests:
   item=dict(candidate=name,supplied_source=sources,case=title)
   try:
    with cr.Harness(c) as h:
     opts="[session(true),src_text('probe(ok).')]" if sources else '[session(true)]'
     h.spawn_shell(opts);h.call(goal,'[limit(1)]')
     e=None
     for i in range(32):
      e=h.recv()
      if e.get('type')=='down':continue
      break
     if 'sandbox denial' in title:
      assert e['type']=='error' and ('permission' in str(e) or 'sandbox' in str(e)),e
     else:
      assert e['type']=='success',e
      if e.get('more') is True:
       h.next()
       for i in range(32):
        end=h.recv()
        if end.get('type')=='down':continue
        assert end['type']=='failure',end;break
       item['tail']='empty final response after More=true'
     h.halt()
    item['status']='pass'
   except Exception as ex:item.update(status='fail',error=str(ex))
   results.append(item);print(item,flush=True)

args.report.write_text(json.dumps(results,indent=2)+'\n')
sys.exit(any(x['status']!='pass' for x in results))
