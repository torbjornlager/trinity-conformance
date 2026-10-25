#!/usr/bin/env python3
"""Identical public actor-output assertions, plus separate Trealla denials."""
from pathlib import Path
import json,sys
import cyclic_boundaries as c
import run as wire
OUT=c.ROOT/'reports/2026-10-25-write-output/results'
CASES=[
 ('atom','write(abc),Outcome=ok',{},['abc']),
 ('chars','write([a,b,c]),Outcome=ok',{},['[a,b,c]']),
 ('unicode',"write('räksmörgås'),Outcome=ok",{},['räksmörgås']),
 ('compound','write(pair(a,a)),Outcome=ok',{},['pair(a,a)']),
 ('call','call(write(abc)),Outcome=ok',{},['abc']),
 ('computed_call','G=write(abc),call(G),Outcome=ok',{},['abc']),
 ('private_source','writer(abc),Outcome=ok',{'source':'writer(X) :- write(X).'},['abc']),
 ('copied_helper','spawn(writer(copied),C,[src_predicates([writer/1]),monitor(true)]),receive({down(C,C,true)->Outcome=ok},[timeout(2),on_timeout(fail)])',{'source':'writer(X) :- write(X).'},['copied']),
 ('backtracking','((write(a),fail);write(b)),Outcome=ok',{},['a','b']),
]
def query(url,goal,source=None):
 cand=wire.Candidate(url.replace('http:','ws:')+'/ws','actor',5,None,None,False,())
 with wire.Harness(cand) as h:
  options='[session(true)'+(',src_text('+c.quote(source)+')' if source else '')+']'
  h.spawn_shell(options);outputs=[];events=[]
  try:
   h.call(goal,'[template(Outcome),format(prolog),limit(1)]')
   for _ in range(24):
    e=h.recv();events.append(e)
    if e.get('type')=='io_request':
     nested=e.get('event',{})
     if nested.get('type')=='output':outputs.append(nested.get('data'))
     h.send(dict(command='browser_io_reply',request_id=e['request_id'],status='ok'))
    elif e.get('type')=='output':outputs.append(e.get('data'))
    elif e.get('type') in ['success','error','failure']:return dict(outputs=outputs,answer=e,events=events)
   raise RuntimeError('missing terminal result')
  finally:h.halt()
def checks(url,kind):
 rows=[]
 for name,goal,options,expected in CASES:
  result=query(url,goal,**options);passed=result['outputs']==expected and result['answer'].get('data')==['ok']
  rows.append(dict(case=name,kind='shared',candidate=kind,passed=passed,goal=goal,options=options,result=result))
  print(kind,name,passed,flush=True)
 if kind=='trealla':
  for name,goal in [('stream_direct','write(user_output,abc),Outcome=unexpected'),('stream_computed','G=write(user_output,abc),call(G),Outcome=unexpected')]:
   result=query(url,goal);passed=not result['outputs'] and result['answer'].get('type')=='error' and 'permission_error' in json.dumps(result['answer'])
   rows.append(dict(case=name,kind='trealla_stream_denial',candidate=kind,passed=passed,goal=goal,result=result));print(kind,name,passed,flush=True)
 return rows
def main():
 OUT.mkdir(parents=True,exist_ok=False);c.OUT=OUT
 before=c.preservation(c.NATIVE,c.TREALLA,c.SWI,c.TPL);nodes=[];rows=[]
 try:
  for kind in ['swi','trealla']:
   node=c.Node(kind,kind,dict(swi=c.NATIVE,trealla=c.TREALLA));nodes.append(node)
   rows.extend(checks(node.url,kind))
 finally:
  for node in reversed(nodes):node.stop()
  after=c.preservation(c.NATIVE,c.TREALLA,c.SWI,c.TPL)
  (OUT/'observations.json').write_text(json.dumps(rows,indent=2)+'\n')
  (OUT/'provenance.json').write_text(json.dumps(dict(nodes=[x.record for x in nodes],runtime_sources=dict(swi=before['native_prolog'],trealla=before['trealla_sources']),engines=before['engines'],preservation={k:before[k]==after[k] for k in before},runner_sha256=c.sha(Path(__file__))),indent=2)+'\n')
 assert len(rows)==20 and all(x['passed'] for x in rows),[(x['candidate'],x['case'],x['result']) for x in rows if not x['passed']]
if __name__=='__main__':main()
