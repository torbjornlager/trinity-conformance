from pathlib import Path
import sys,json,time
O=Path(__file__).parent;sys.path.insert(0,str(O/'conformance/runner'));import run as actor
cases=[('direct','runtime_property(persistent(true)),Control=direct'),('findall-outside-receive','findall(X,(runtime_property(persistent(true)),member(X,[a,b])),Xs),Xs==[a,b]'),('receive-body','self(S),send(S,body_probe),receive({body_probe->runtime_property(persistent(true))},[timeout(0),on_timeout(throw(missing))])'),('receive-enumeration-without-runtime-property','self(S),send(S,body_probe),findall(X,receive({body_probe->member(X,[a,b])},[timeout(0),on_timeout(throw(missing))]),Xs),Xs==[a,b]')];rows=[]
for label,goal in cases:
 try:
  with actor.Harness(actor.Candidate('wss://n5.elfenbenstornet.se/ws','actor',8,None,None,False,())) as h:
   h.spawn_shell();h.call(goal,'[limit(1)]');e=h.recv_type('success',limit=64);h.halt();r=dict(control=label,goal=goal,outcome='success',event=e)
 except Exception as e:r=dict(control=label,goal=goal,outcome='failed',detail=type(e).__name__+': '+str(e))
 rows.append(r);print(label,r['outcome'],flush=True)
(O/'N5-receive-controls.json').write_text(json.dumps(rows,indent=2)+'\n')
