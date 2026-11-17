from pathlib import Path
import sys,re,html,json,time
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O.parents[1]/'runner'))
from run import Candidate,Harness,prolog_quote_atom
source=html.unescape(re.search(r'<pre id="cpw-remote-pingpong-source">(.*?)</pre>',Path('/Users/lager/trinity-demonstrator/web/actor-profile-tutorial.html').read_text(),re.S)[1]).replace('{{actor_peer_host}}','https://n4.elfenbenstornet.se')
rows=[]
for name,loaded,goal,expected in [
 ('tutorial',True,'ping_pong_remote',['Pong received ping.']*3+['Ping received pong.']*3+['Ping finished.','Pong finished.']),
 ('inline-loaded',True,"spawn(format('remote_inline(~w)~n',[ok]),P,[node('https://n4.elfenbenstornet.se'),monitor(true)]),receive({down(P,_,R)->(R==true->true;throw(remote_failed(R)))},[timeout(6),on_timeout(throw(no_down))])",['remote_inline(ok)']),
 ('inline-sourceless',False,"spawn(format('remote_inline(~w)~n',[ok]),P,[node('https://n4.elfenbenstornet.se'),monitor(true)]),receive({down(P,_,R)->(R==true->true;throw(remote_failed(R)))},[timeout(6),on_timeout(throw(no_down))])",['remote_inline(ok)'])]:
 events=[];started=time.monotonic()
 with Harness(Candidate('wss://n5.elfenbenstornet.se/ws','actor',10,None,'https://n5.elfenbenstornet.se',False,())) as h:
  h.spawn_shell('[session(true),src_text('+prolog_quote_atom(source)+')]' if loaded else '[]');h.call(goal,'[limit(1)]')
  for _ in range(24):
   e=h.recv();events.append(e);h.acknowledge_output(e)
   if e.get('type') in ('success','failure','error'):break
 assert events[-1]['type']=='success',events
 outputs=[e['event']['data'] for e in events if e.get('type')=='io_request']
 assert sorted(outputs)==sorted(expected),outputs
 rows.append(dict(case=name,status='pass',seconds=round(time.monotonic()-started,2),events=events));print(name,'PASS',flush=True)
 (O/'public-pingpong.json').write_text(json.dumps(dict(results=rows,counts=dict(pass_count=len(rows),fail_count=0)),indent=2)+'\n')
