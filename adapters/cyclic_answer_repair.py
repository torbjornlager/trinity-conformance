#!/usr/bin/env python3
"""Verify explicitly selected working-source answer guards on disposable nodes."""
import json,sys,time
from pathlib import Path
import cyclic_boundaries as c
OUT=c.ROOT/'reports/2026-10-25-cyclic-answer-rejection/results'

def main():
    OUT.mkdir(parents=True,exist_ok=False);c.OUT=OUT
    before=c.preservation(c.NATIVE,c.TREALLA,c.SWI,c.TPL)
    rows=[];nodes=[];roots=dict(swi=c.NATIVE,trealla=c.TREALLA)
    source_input={kind:dict(commit=c.git(root,'rev-parse','HEAD'),status=c.git(root,'status','--short'),runtime_hashes=(before['native_prolog'] if kind=='swi' else before['trealla_sources'])) for kind,root in roots.items()}
    cases=[]
    for caller in roots:
        for name,goal,template in [
          ('http_shared','X=pair(A,A),X=pair(U,V),var(U),U==V,Outcome=shared_ok','Outcome'),
          ('http_cycle','X=f(X)','X'),
          ('http_cyclic_exception','X=f(X),throw(error(probe(X),ctx))','X'),
          ('http_finite_after_local_cycle','X=f(X),\\+acyclic_term(X),Outcome=ok','Outcome'),
          ('http_plain_error','throw(ordinary_error)','X')]:
            cases.append((name,caller,None,goal,template))
        cases.append(('ws_cycle',caller,None,'X=f(X),Outcome=X',None))
        for peer in roots:
            for family in ['rpc','promise']:
                for cyclic in [False,True]:cases.append((family+('_cycle' if cyclic else '_shared'),caller,peer,cyclic,None))
            cases.append(('promise_retry',caller,peer,None,None))
    try:
        for index,(name,caller,peer,value,template) in enumerate(cases):
            label=f'{index:02}-{caller}-{name}'+(f'-{peer}' if peer else '')
            row=dict(case=name,caller=caller,peer=peer);active=[]
            # catch/3 loses a cyclic exception in this unchanged Trealla engine.
            row['kind']='engine_diagnostic' if name=='http_cyclic_exception' and caller=='trealla' else 'required_regression'
            try:
                x=c.Node(caller,label+'-caller',roots);active.append(x);nodes.append(x.record)
                p=None
                if peer:p=c.Node(peer,label+'-peer',roots);active.append(p);nodes.append(p.record)
                if name.startswith('http_'):result=c.http(x,value,template)
                else:
                    if name.startswith('rpc_'):goal=c.rpc_goal(p.url,value)
                    elif name.startswith('promise_') and name!='promise_retry':goal=c.promise_goal(p.url,value)
                    elif name=='promise_retry':
                        goal=f"promise({c.quote(p.url)},(sleep(0.15),X=pair(Y,Y)),Ref,[template(X),limit(1),once(true)]),yield(Ref,Early,[timeout(0),on_timeout(Early=waiting)]),Early==waiting,yield(Ref,success([pair(A,B)],false),[timeout(2)]),var(A),A==B,Outcome=retry_ok"
                    else:goal=value
                    row['goal']=goal;result=c.ws(x,goal)
                row['result']=result
                text=json.dumps(result)
                if row['kind']=='engine_diagnostic':row['passed']=None
                elif ('cycle' in name or name=='http_cyclic_exception') and name!='http_finite_after_local_cycle':row['passed']='representation_error' in text and 'cyclic_term' in text
                elif name.endswith('shared'):row['passed']='shared_ok' in text
                elif name=='promise_retry':row['passed']='retry_ok' in text
                elif name=='http_plain_error':row['passed']='error(ordinary_error)' in text
                else:row['passed']='success([ok],false)' in text
                row['health_after']=c.http(x,'Outcome=healthy','Outcome')
                row['healthy']='success([healthy],false)' in row['health_after'].get('body','')
            except Exception as e:row.update(exception=type(e).__name__,message=str(e),passed=False)
            finally:
                for n in reversed(active):n.stop()
                rows.append(row);(OUT/'observations.json').write_text(json.dumps(rows,indent=2)+'\n')
                print(label,row.get('passed'),json.dumps(row.get('result',row.get('exception'))),flush=True)
    finally:
        after=c.preservation(c.NATIVE,c.TREALLA,c.SWI,c.TPL)
        checks={k:before[k]==after[k] for k in before}
        (OUT/'preservation.json').write_text(json.dumps(dict(checks=checks,before=before,after=after),indent=2)+'\n')
        (OUT/'provenance.json').write_text(json.dumps(dict(sources=source_input,nodes=nodes,engines=before['engines'],runner_sha256=c.sha(Path(__file__)),fixture_sha256=c.sha(Path(c.__file__)),sources_are='explicit working-tree candidates, not committed/deployed claims'),indent=2)+'\n')
    return int(any(r.get('passed') is False for r in rows) or not all(checks.values()))
if __name__=='__main__':raise SystemExit(main())
