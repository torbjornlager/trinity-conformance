from pathlib import Path
import json,shutil,time,subprocess
O=Path(__file__).resolve().parent;initial=O/'consumer-ci-initial';rerun=Path('/tmp/cluster-policy-wasm-gate-rerun');replays=Path('/tmp/cluster-policy-wasm-replays');started=time.monotonic()
while not (rerun/'result.json').exists():
 if time.monotonic()-started>600:raise TimeoutError('WASM rerun did not complete')
 time.sleep(1)
r=json.loads((rerun/'result.json').read_text());assert r['exit_code']==0,r
trials=json.loads((replays/'results.json').read_text());assert len(trials)==3 and all(x['exit_code']==0 for x in trials)
rows=json.loads((initial/'results.json').read_text());assert len(rows)==38 and [(x['label'],x['exit_code']) for x in rows if x['exit_code']] == [('WASM',1)]
out=O/'consumer-ci';out.mkdir(exist_ok=False)
for f in initial.iterdir():
 if f.is_file() and f.name not in ['results.json','WASM.log']:shutil.copy2(f,out/f.name)
shutil.copy2(rerun/'WASM.log',out/'WASM.log');shutil.copytree(replays,O/'wasm-focused-replays');shutil.copytree(rerun,O/'wasm-gate-rerun')
rows=[r if x['label']=='WASM' else x for x in rows]
(out/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
note={'initial':{'groups':38,'passed':37,'failed':['WASM: supervisor_request_wait_worker interruption cleanup assertions']},'focused_replays':{'runs':3,'failures':0},'wasm_group_rerun_exit_code':0,'product_or_test_changes_for_rerun':False,'browser_pin_unchanged':True,'note':'Initial failure is retained, not converted to a pass. Qualification combines the unchanged 37 passing groups with the complete passing WASM rerun. The failure did not reproduce in three focused runs; no browser fix is claimed.'}
(O/'ci-rerun-note.json').write_text(json.dumps(note,indent=2)+'\n');print('PASS 38 qualified consumer groups; initial intermittent WASM failure retained',flush=True)
