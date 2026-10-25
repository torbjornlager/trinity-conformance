#!/usr/bin/env python3
"""Supporting reductions; separate from the public boundary matrix."""
import json, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'adapters')]
import cyclic_boundaries as c
OUT=Path(__file__).resolve().parent/'followup-results'
c.OUT=OUT
OUT.mkdir(exist_ok=False)
rows=[];nodes=[]
before=c.preservation(c.NATIVE,c.TREALLA,c.SWI,c.TPL)
try:
    probes=[
      ('nb_store','X=f(X),nb_setval(cycle_probe,X),nb_getval(cycle_probe,Y),(acyclic_term(Y)->write(acyclic);write(cyclic))'),
      ('findall','findall(X,X=f(X),[Y]),(acyclic_term(Y)->write(acyclic);write(cyclic))'),
      ('writer','X=f(X),write_term(X,[quoted(true),max_depth(8)])'),
      ('thread_message','thread_self(Me),X=f(X),thread_send_message(Me,X),thread_get_message(Y),(acyclic_term(Y)->write(acyclic);write(cyclic))')]
    for kind,exe in [('swi',c.SWI),('trealla',c.TPL)]:
      for name,goal in probes:
        cmd=[str(exe)]+(['-f','none','-q'] if kind=='swi' else [])+['-g',goal+',nl,halt']
        row=dict(case=name,engine=kind,command=cmd)
        try:
          r=subprocess.run(cmd,env=c.ENV,capture_output=True,text=True,timeout=3,preexec_fn=c.child_limits,start_new_session=True)
          row.update(exit_code=r.returncode,stdout=r.stdout[:16384],stderr=r.stderr[:16384])
        except subprocess.TimeoutExpired as e:row.update(exception='TimeoutExpired',stdout=str(e.stdout or '')[:16384],stderr=str(e.stderr or '')[:16384])
        rows.append(row)
    for caller,peer in [('swi','trealla'),('trealla','trealla')]:
      active=[];label=caller+'-to-'+peer
      try:
        x=c.Node(caller,label+'-caller',dict(swi=c.NATIVE,trealla=c.TREALLA));active.append(x);nodes.append(x.record)
        p=c.Node(peer,label+'-peer',dict(swi=c.NATIVE,trealla=c.TREALLA));active.append(p);nodes.append(p.record)
        # A plain finite round trip separates general return routing from cycle handling.
        src="probe :- receive({inspect(V,Parent) -> Parent ! observed(V)})."
        goal=f"catch((self(Self),spawn(probe,Pid,[node({c.quote(p.url)}),src_text({c.quote(src)})]),Pid ! inspect(pair(a,b),Self),receive({{observed(V)->Outcome=observed(V)}},[timeout(1),on_timeout(Outcome=delivery_timeout)])),E,(acyclic_term(E)->Outcome=exception(E);Outcome=cyclic_exception))"
        row=dict(case='plain_remote_control',caller=caller,peer=peer,goal=goal)
        try:row['result']=c.ws(x,goal)
        except Exception as e:row.update(exception=type(e).__name__,message=str(e))
        rows.append(row)
      finally:
        for n in reversed(active):n.stop()
finally:
    after=c.preservation(c.NATIVE,c.TREALLA,c.SWI,c.TPL)
    (OUT/'preservation.json').write_text(json.dumps(dict(checks={k:before[k]==after[k] for k in before}),indent=2)+'\n')
    (OUT/'observations.json').write_text(json.dumps(rows,indent=2)+'\n')
    (OUT/'nodes.json').write_text(json.dumps(nodes,indent=2)+'\n')
for row in rows:print(json.dumps(row))
