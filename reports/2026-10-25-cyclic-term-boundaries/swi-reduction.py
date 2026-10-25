#!/usr/bin/env python3
"""Bounded supporting reduction of the SWI HTTP time-limit observation."""
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'adapters'))
import cyclic_boundaries as c
prefix=f"use_module(library(time)),use_module(library(sgml)),use_module(library(option)),consult({c.quote(c.NATIVE/'load.pl')}),"
probes=[('attvars','X=f(X),term_attvars(X,V),write(V)'),('findnsols','findnsols(1,X,(X=f(X)),[Y]),(acyclic_term(Y)->write(acyclic);write(cyclic))'),('portable_answer','X=f(X),toplevel_actors:portable_answer(success([X],false),A),(acyclic_term(A)->write(acyclic);write(cyclic))'),('answer','toplevel_actors:answer((X=f(X)),X,0,1,A),(acyclic_term(A)->write(acyclic);write(cyclic))')]
rows=[]
for name,goal in probes:
    bounded="catch(call_with_time_limit(0.5,("+goal+")),E,(functor(E,N,A),write(exception(N,A)))),nl,halt"
    cmd=[str(c.SWI),'-f','none','-q','-g',prefix+bounded]
    row=dict(case=name,command=cmd)
    try:
        r=subprocess.run(cmd,env=c.ENV,cwd=c.NATIVE,capture_output=True,text=True,timeout=4,preexec_fn=c.child_limits,start_new_session=True)
        row.update(exit_code=r.returncode,stdout=r.stdout[:16384],stderr=r.stderr[:16384])
    except subprocess.TimeoutExpired:row['exception']='TimeoutExpired'
    rows.append(row)
    print(json.dumps(row),flush=True)
Path(__file__).with_name('swi-reduction-results.json').write_text(json.dumps(rows,indent=2)+'\n')
