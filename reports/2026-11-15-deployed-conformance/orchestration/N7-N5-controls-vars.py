from pathlib import Path
import sys,json
O=Path(__file__).parent;sys.path.insert(0,str(O/'conformance/runner'));import run as actor
rows=[];c=actor.Candidate('wss://n7.elfenbenstornet.se/ws','actor',8,None,None,False,())
with actor.Harness(c) as h:
 h.spawn_shell()
 def call(label,goal):
  h.call(goal,'[limit(1)]');seen=[]
  for _ in range(50):
   e=h.recv();seen.append(e)
   if e.get('type') in ['success','failure','error']:break
   if e.get('type')=='io_request':h.acknowledge_output(e)
  rows.append(dict(step=label,goal=goal,events=seen));(O/'N7-N5-controls-vars.json').write_text(json.dumps(rows,indent=2)+'\n');return e
 spawn=call('spawn',"toplevel_spawn(P,[node('https://n5.elfenbenstornet.se'),session(true),monitor(true),src_text('baseline_remote(a). baseline_remote(b).')])")
 if spawn['type']=='success':
  p=actor.row_value(spawn,'P')
  call('sync-call',f'toplevel_call_synch({p},baseline_remote(X),A,[template(X),limit(1),timeout(3)]),(A==success({p},[a],true)->Match=yes;Match=no),(var(A)->AnswerUnbound=yes;AnswerUnbound=no)')
  call('sync-next',f'toplevel_next_synch({p},B,[timeout(3)]),(B==success({p},[b],false)->Match=yes;Match=no),(var(B)->AnswerUnbound=yes;AnswerUnbound=no)')
  call('halt-and-monitor',f'toplevel_halt({p}),receive({{down({p},{p},Reason)->Down=received}},[timeout(3),on_timeout(Down=timeout)])')
 h.halt()
print('N7->N5 step control captured')
