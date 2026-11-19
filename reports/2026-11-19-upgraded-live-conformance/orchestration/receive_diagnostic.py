from pathlib import Path
import sys,json
P=Path(__file__).resolve().parents[1];R=P/'suite-snapshot';sys.path[:0]=[str(R/'runner')];import run as actor,baseline
pack=json.loads((R/'cases/selective-receive-0.2.json').read_text());case=next(c for c in pack['cases'] if c['id']=='SR-015');goal=case['goal'];suffix=',Xs==[one-a,two-a]';assert goal.endswith(suffix)
projection=goal[:-len(suffix)];actor.set_session_interval(2.1);rows=[]
for timeout in ['0','0.05','0.2']:
 row=dict(label='receive_observation_timeout_'+timeout,status='observed',variant='diagnostic projection only; no conformance pass is inferred',goal=projection.replace('timeout(0)','timeout('+timeout+')'))
 try:row['observation']=baseline.query_case(dict(goal=row['goal']),'wss://n5.elfenbenstornet.se/ws',10,None)
 except Exception as e:row.update(status='diagnostic_error',detail=type(e).__name__+': '+str(e))
 rows.append(row)
(P/'live-controls/trealla-sr015-diagnostics.json').write_text(json.dumps(dict(scope='Supplementary projection/timing observations. The original SR-015 failure and unchanged repeats are separate.',results=rows),indent=2)+'\n')
