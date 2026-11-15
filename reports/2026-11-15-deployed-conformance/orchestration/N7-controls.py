from pathlib import Path
import sys,json,time
O=Path(__file__).parent;sys.path.insert(0,str(O/'conformance/runner'));import run as actor
while True:
 try:done=len(json.loads((O/'interop-actor.json').read_text())['results'])==36
 except Exception:done=False
 if done:break
 time.sleep(1)
print('Waiting61s for public engine-start sliding window',flush=True);time.sleep(61)
original_enter=actor.Harness.__enter__;original_send=actor.Harness.send;last=0;correlated=False
def paced_enter(h):
 global last
 delay=4-(time.monotonic()-last)
 if delay>0:time.sleep(delay)
 last=time.monotonic();return original_enter(h)
def send(h,request):
 if correlated and request.get('command')=='transport_hello':request={**request,'prompt_correlation':True}
 return original_send(h,request)
actor.Harness.__enter__=paced_enter;actor.Harness.send=send;candidate=actor.Candidate('wss://n7.elfenbenstornet.se/ws','actor',5,None,'https://n7.elfenbenstornet.se',False,());rows=[]
for variant,ids in [('paced-original-worker',['WC-003','WC-004','WC-005','WC-007']),('explicit-correlated-prompt',['PW-001','PW-002','PW-003','PW-004'])]:
 correlated=variant=='explicit-correlated-prompt'
 for case_id in ids:
  start=time.monotonic();row=dict(variant=variant,id=case_id)
  try:actor.CASE_FUNCTIONS[case_id](candidate);row['status']='pass'
  except Exception as e:row.update(status='fail',detail=type(e).__name__+': '+str(e))
  row['duration_ms']=round((time.monotonic()-start)*1000);rows.append(row);(O/'N7-controls.json').write_text(json.dumps(dict(results=rows,fixture_policy='All worker assertions and transport deadlines unchanged; wait61s then >=4s between every WebSocket session, below existing20engine-starts/minute. PW control explicitly negotiates prompt_correlation:true; original unnegotiated failures remain separate.'),indent=2)+'\n');print(variant,case_id,row['status'],row.get('detail','')[:200],flush=True)
