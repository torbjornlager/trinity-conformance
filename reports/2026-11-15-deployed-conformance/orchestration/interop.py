from pathlib import Path
import sys,json,time
O=Path(__file__).parent;R=O/'conformance';sys.path.insert(0,str(R/'runner'));import baseline
pack=json.loads((R/'cases/interop-actor-0.1.json').read_text());rows=[]
for source in [3,4,5,7]:
 if source==7:
  while True:
   try:count=sum(len(json.loads(p.read_text())['results']) for p in (O/'public/N7-actor').glob('*.json'))
   except Exception:count=0
   if count==98:break
   time.sleep(1)
 for target in [n for n in [3,4,5,7] if n!=source]:
  for case0 in pack['cases']:
   if source==7:time.sleep(5)
   case=json.loads(json.dumps(case0).replace('__PEER__',f'https://n{target}.elfenbenstornet.se'));t=time.monotonic();row=dict(source=source,target=target,id=case['id'],title=case['title'])
   try:row.update(status='pass',observation=baseline.query_case(case,f'wss://n{source}.elfenbenstornet.se/ws',8,None))
   except Exception as e:row.update(status='fail',detail=type(e).__name__+': '+str(e))
   row['duration_ms']=round((time.monotonic()-t)*1000);rows.append(row);(O/'interop-actor.json').write_text(json.dumps(dict(format='direct-runner-observations-v1',suite=pack['suite'],scope=pack['scope'],results=rows),indent=2)+'\n');print(source,target,case['id'],row['status'],row.get('detail','')[:150],flush=True)
