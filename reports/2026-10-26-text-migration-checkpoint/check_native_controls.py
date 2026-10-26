#!/usr/bin/env python3
"""Public-interface controls; connect only to explicitly supplied disposable nodes."""
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'runner'),str(ROOT/'adapters')]
import run as wire
import portable_text

def query(url,goal):
 candidate=wire.Candidate(url.replace('http:','ws:')+'/ws','actor',5,None,None,False,())
 with wire.Harness(candidate) as h:
  h.spawn_shell(); events=[]; outputs=[]
  try:
   h.call('once(('+goal+')),Checkpoint=pass','[template(Checkpoint),format(prolog),limit(1)]')
   for _ in range(32):
    e=h.recv();events.append(e)
    if e.get('type')=='io_request':
     if e.get('event',{}).get('type')=='output':outputs.append(e['event']['data'])
     h.send(dict(command='browser_io_reply',request_id=e['request_id'],status='ok'))
    elif e.get('type')=='output':outputs.append(e.get('data'))
    elif e.get('type') in ['success','failure','error']:return dict(passed=e.get('data')==['pass'],outputs=outputs,events=events)
   raise RuntimeError('No terminal response')
  finally:h.halt()

def main():
 p=argparse.ArgumentParser();p.add_argument('--swi',required=True);p.add_argument('--trealla',required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 if a.output.exists():p.error('Output exists; choose a fresh file')
 out=Path(__file__).parent;rows=[]
 original=wire.WebSocket.send_json
 for name,url in [('swi',a.swi),('trealla',a.trealla)]:
  for ident,goal in [('OUT-001','write("abc")'),('CONTROL-SCALAR','char_code(C,128512),atom_chars(A,[C]),atom_length(A,1)'),('CONTROL-ROUNDTRIP','atom_to_term(\'"ab"\',T,[]),T==[a,b]'),('PROMISE-001','promise('+wire.prolog_quote_atom(a.swi)+',X="ab",R,[template(X-X)]),yield(R,A),A==success([[a,b]-[a,b]],false),var(X)')]:
   try:r=query(url,goal)
   except Exception as e:r=dict(passed=False,error=repr(e))
   rows.append(dict(candidate=name,id=ident,goal=goal,**r))
  candidate=wire.Candidate(url.replace('http:','ws:')+'/ws','actor',5,None,None,False,())
  for encoding in ['escaped_surrogates','literal_utf8']:
   wire.WebSocket.send_json=original if encoding=='escaped_surrogates' else lambda self,v:self._send_frame(1,json.dumps(v,ensure_ascii=False,separators=(',',':')).encode('utf-8'))
   for case in json.loads((ROOT/'cases/portable-text-0.2.json').read_text())['cases']:
    if case['id'] not in ['TXT-008','TXT-020','TXT-025','TXT-026']:continue
    try:portable_text.execute(candidate,case);r=dict(passed=True)
    except Exception as e:r=dict(passed=False,error=repr(e))
    rows.append(dict(candidate=name,id=case['id'],encoding=encoding,**r))
  wire.WebSocket.send_json=original
 a.output.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 for r in rows:print(r['candidate'],r['id'],r.get('encoding',''),r['passed'],r.get('error',''))
if __name__=='__main__':main()
