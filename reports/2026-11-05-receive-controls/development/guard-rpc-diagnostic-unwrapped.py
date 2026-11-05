import sys,subprocess,socket,os,time
sys.path[:0]=['adapters','runner']
from receive_control_peer import GuardPeer
from run import Harness,Candidate,prolog_quote_atom
with GuardPeer() as peer:
 peer.release.set()
 with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
 goal="use_module(distribution),web_prolog:web_prolog_node("+str(port)+",[])"
 env=dict(os.environ,TPL_LIBRARY_PATH='/Users/lager/trinity-demonstrator/.trinity/trealla-engine/library')
 with open('/tmp/guard-rpc-diagnostic-node.txt','w') as log:
  p=subprocess.Popen(['/Users/lager/trinity-demonstrator/.trinity/trealla-engine/tpl','-g',goal],cwd='/Users/lager/trealla-port',env=env,stdout=log,stderr=log)
  try:
   for _ in range(100):
    try:
     with socket.create_connection(('127.0.0.1',port),timeout=.1):break
    except OSError:time.sleep(.03)
   with Harness(Candidate(f'ws://127.0.0.1:{port}/ws','actor',5,None,None,False,())) as h:
    h.spawn_shell('[session(true)]')
    rpc='rpc(LibraryEntryURI,true,[http_timeout(2)])'
    diagnostic='LibraryEntryURI='+prolog_quote_atom(peer.url)+',self(S),S!rg_before,S!rg_target(pair(V,V)),S!rg_after,receive({rg_target(pair(X,Y)) if (X=tentative,GuardBinding=dirty,('+rpc+'))->Outcome=guard},[timeout(0)]),receive({diagnostic(D)->true},[timeout(0)])'
    h.call(diagnostic,'[limit(1)]');print(h.recv());h.halt()
   print('Entry requests',peer.requests)
  finally:
   p.terminate()
   try:p.wait(timeout=2)
   except subprocess.TimeoutExpired:p.kill();p.wait()
