"""Fresh N7 retained-HTTP prompt coverage, using the maintained ECLiPSe branch."""
from pathlib import Path
import sys,time,threading,json
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'suite-snapshot/runner'));import prompt_http as prompt
while not (P/'logs/endpoint-n7.done').exists():time.sleep(3)
print('N7 prompts:61-second quiet period',flush=True);time.sleep(61)
original=prompt.post_response;lock=threading.Lock();last=0

def paced(base,command,fields,**kwargs):
 global last
 if command!='spawn':return original(base,command,fields,**kwargs)
 with lock:
  delay=4-(time.monotonic()-last)
  if delay>0:time.sleep(delay)
  try:return original(base,command,fields,**kwargs)
  finally:last=time.monotonic()
prompt.post_response=paced
output=P/'live-controls/paused-prompt-http-n7.json';sys.argv=['prompt_http.py','--eclipse','https://n7.elfenbenstornet.se','--output',str(output)]
code=prompt.main();data=json.loads(output.read_text());data.update(minimum_pause_between_session_spawns_seconds=4,race_submissions_unchanged=True,coverage_note='Additional live N7 coverage; not included in preceding full sweep prompt matrix');output.write_text(json.dumps(data,indent=2)+'\n');(P/'n7-prompt-job.json').write_text(json.dumps(dict(exit_code=code,case_count=len(data['results'])),indent=2)+'\n');(P/'n7-prompts.complete').write_text('complete\n');print('N7 prompt pack finished, exit',code,flush=True)
