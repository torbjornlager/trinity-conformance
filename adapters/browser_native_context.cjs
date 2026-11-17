'use strict';
const fs=require('fs'),path=require('path'),http=require('http'),crypto=require('crypto');
const {chromium}=require('playwright');
const root=path.resolve(process.env.LIBRARY_RUNTIME_ROOT),peers=JSON.parse(process.env.BROWSER_CONTEXT_PEERS),rows=[];
const sha=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const quote=s=>"'"+s.replace(/'/g,"''")+"'";
function save(){fs.writeFileSync(process.env.LIBRARY_REPORT,JSON.stringify({suite:'browser-native-context-0.1',adapter_sha256:sha(__filename),runtime_manifest_sha256:sha(path.join(root,'manifest.json')),results:rows,counts:{pass:rows.filter(x=>x.status==='pass').length,fail:rows.filter(x=>x.status==='fail').length}},null,2)+'\n');}
function deadline(p,ms,label){let t;return Promise.race([p,new Promise((_,reject)=>{t=setTimeout(()=>reject(Error(label+' deadline')),ms);})]).finally(()=>clearTimeout(t));}
const server=http.createServer((req,res)=>{
 const pathname=new URL(req.url,'http://localhost').pathname;
 if(pathname.startsWith('/return/')){const [_,prefix,action,peer]=pathname.split('/');if(!process.env.BROWSER_RETURN_GATES||!['swi','trealla'].includes(peer)){res.writeHead(404);res.end();return;}const dir=path.join(process.env.BROWSER_RETURN_GATES,peer);if(action==='arm'){for(const f of ['arm','entered','continue','token','result'])fs.rmSync(path.join(dir,f),{force:true});fs.writeFileSync(path.join(dir,'arm'),'');}if(action==='release')fs.writeFileSync(path.join(dir,'continue'),'');res.setHeader('Content-Type','application/json');res.end(JSON.stringify({entered:fs.existsSync(path.join(dir,'entered')),result:fs.existsSync(path.join(dir,'result'))?fs.readFileSync(path.join(dir,'result'),'utf8'):null}));return;}
 if(pathname.startsWith('/native/')){const name=pathname.split('/')[2],target=new URL(peers[name]);target.pathname='/call';target.search=new URL(req.url,'http://localhost').search;http.get(target,r=>{res.writeHead(r.statusCode,{'Content-Type':r.headers['content-type']||'text/plain'});r.pipe(res);}).on('error',e=>{res.writeHead(502);res.end(String(e));});return;}
 if(pathname==='/answer/call'){res.setHeader('Content-Type','text/plain');res.end('success([mark],false).');return;}
 if(pathname==='/__context.html'){res.setHeader('Content-Type','text/html; charset=utf-8');res.end('<meta charset="utf-8"><script src="/swi_wasm_actor_worker.js"></script><script src="/vendor/swi-wasm-node.js"></script>');return;}
 const file=path.resolve(root,'web','.'+pathname);if(!file.startsWith(path.join(root,'web')+path.sep)){res.writeHead(403);res.end();return;}
 fs.readFile(file,(e,data)=>{if(e){res.writeHead(404);res.end();return;}res.setHeader('Content-Type',file.endsWith('.js')?'text/javascript; charset=utf-8':file.endsWith('.wasm')?'application/wasm':'text/plain');res.end(data);});
});
(async()=>{
 await new Promise(r=>server.listen(Number(process.env.BROWSER_CONTEXT_PORT),'127.0.0.1',r));
 const base='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 const watchdog=setTimeout(()=>{browser.close();setTimeout(()=>process.exit(2),3000).unref();},210000);
 try{for(const mode of ['worker','main'])for(const [peer,url] of Object.entries(peers))for(const id of (process.env.BROWSER_CONTEXT_CASES||('BN-001,BN-002,BN-003,BN-004,BN-005,BN-006,BN-007,BN-008,BN-009,BN-010,BN-011,BN-012'+(process.env.BROWSER_RETURN_GATES?',BN-013':'')+',BN-014,BN-015,BN-016')).split(',')){
  const row={candidate:'swi-wasm-'+mode,id:id+'-'+peer,peer};const page=await browser.newPage();
  try{
   await page.goto(base+'/__context.html');
   row.observation=await deadline(page.evaluate(async({mode,url,id,base,peer,other})=>{
    const nodes=[],checks=[],events=[],q=s=>"'"+s.replace(/'/g,"''")+"'",u=q(url),answer=q(base+'/answer');
    const check=(ok,label)=>{if(!ok)throw Error(label);checks.push(label);};
    const create=async mode=>{const n=SwiWasmNode.create({mode,workerUrl:new URL('/swi_wasm_actor_worker.js',location.href).href,engineUrl:new URL('/swipl-bundle.js',location.href).href,prologBaseUrl:new URL('/wasm/',location.href).href,sharedDatabaseUrl:null,onEvent:e=>events.push(e)});nodes.push(n);await n.open();return n;};
    const n=await create(mode);
    const run=async(goal,node=n)=>{const a=await node.query('('+goal+'),ContextCheck=passed',{limit:1});check(a.type==='success'&&a.more===false&&a.data.length===1&&a.data[0].ContextCheck==='passed','query '+goal+' '+JSON.stringify(a)+' '+JSON.stringify(events.slice(-10)));return a;};
    const remote=(goal,opts='')=>`self(S),spawn((${goal}),_,[node(${u})${opts}])`;
    const missing=r=>`catch(yield(${r},_,[timeout(0)]),error(existence_error(promise,${r}),_),Missing=true),Missing==true`;
    try{
     if(id==='BN-001')await run(remote('send(S,hello)')+',receive({hello->true},[timeout(3),on_timeout(throw(no_browser_return))])');
     if(id==='BN-002')await run(`promise(${answer},true,R,[template(mark)]),`+remote('catch(yield(R,_,[timeout(0)]),E,true),promise_cleanup(R),send(S,denied(E))')+',receive({denied(error(existence_error(promise,R),_))->true},[timeout(3),on_timeout(throw(no_forward_denial))]),yield(R,success([mark],false))');
     if(id==='BN-003'){
      const a=await run(remote(`promise(${answer},true,R,[template(mark)]),send(S,created(R))`)+',receive({created(Ref)->true},[timeout(3),on_timeout(throw(no_reference))])');
      const ref=a.data[0].Ref;check(/^\d+$/.test(ref),'native reference returned');
      await run(missing(ref)+','+remote(`yield(${ref},A),send(S,collected(A))`)+',receive({collected(success([mark],false))->true},[timeout(3),on_timeout(throw(no_native_collection))])');
     }
     if(id==='BN-004')await run(`promise(${answer},true,R,[template(mark)]),self(S),spawn(receive({return(R)->self(Me),whereis(origin_alias,Me),yield(R,A),S!returned(A)}),Local,[]),register(origin_alias,Local),spawn(send(Local,return(R)),_,[node(${u})]),receive({returned(success([mark],false))->true},[timeout(3),on_timeout(throw(no_return_context))])`);
     if(id==='BN-005'){
      const other=await create('worker');
      const a=await run(remote(`promise(${answer},true,R,[template(mark)]),send(S,created(R))`)+',receive({created(Ref)->true},[timeout(3),on_timeout(throw(no_reference))])');const ref=a.data[0].Ref;
      await run(remote(`catch(yield(${ref},_,[timeout(0)]),E,true),promise_cleanup(${ref}),send(S,denied(E))`)+`,receive({denied(error(existence_error(promise,${ref}),_))->true},[timeout(3),on_timeout(throw(no_foreign_denial))])`,other);
      await Promise.resolve(other.closeSwiWasmClientContext());
      await run(remote(`yield(${ref},A),send(S,collected(A))`)+',receive({collected(success([mark],false))->true},[timeout(3),on_timeout(throw(no_owner_retry))])');
     }
     if(id==='BN-006'){
      await run(`toplevel_spawn(T,[node(${u}),session(true)]),assertz(saved_remote(T)),toplevel_call_synch(T,(self(Me),register(held_name,Me),promise(${answer},true,R,[template(mark)]),assertz(saved_promise(R))),Init,[template(R),timeout(3)]),nonvar(Init),Init=success(T,[R],false),integer(R)`);
      await Promise.resolve(n.closeSwiWasmClientContext());
      await run('saved_remote(T),toplevel_call_synch(T,true,Alive,[template(true),timeout(3)]),nonvar(Alive),Alive=success(T,[true],false)');
      await run('saved_remote(T),toplevel_call_synch(T,once((whereis(held_name,undefined),saved_promise(R),catch(yield(R,_,[timeout(0)]),error(existence_error(promise,R),_),Gone=true),Gone==true,catch((self(Me),register(late,Me)),error(permission_error(register,_,_),_),Denied=true),Denied==true)),Closed,[template(ok),timeout(3)]),nonvar(Closed),Closed=success(T,[ok],false)');
     }
     if(id==='BN-014'){
      await run(`self(S),toplevel_spawn(P,[node(${u}),session(true),monitor(true)]),monitor(P,Keep),monitor(P,Removed),monitor(P,Queued),send(S,down(P,Queued,already_queued)),demonitor(Queued),receive({down(P,Queued,already_queued)->true},[timeout(0)]),spawn((demonitor(Keep,[flush]),send(S,foreign_done)),F,[monitor(true)]),receive({foreign_done->true}),receive({down(F,F,true)->true}),send(S,down(P,Removed,queued_one)),send(S,down(P,Removed,queued_two)),send(S,kept_message),demonitor(Removed,[flush]),demonitor(Removed),toplevel_call_synch(P,true,A,[template(ok),timeout(3)]),nonvar(A),A=success(P,[ok],false),exit(P,kill),receive({down(P,P,Reason)->true},[timeout(3)]),receive({down(P,Keep,Reason)->true},[timeout(3)]),receive({down(_,Removed,_)->throw(withdrawn_monitor_delivered)},[timeout(0),on_timeout(true)]),receive({kept_message->true},[timeout(0)])`);
     }
     if(id==='BN-015'){
      await run(`toplevel_spawn(P,[node(${u}),session(true)]),monitor(P,R),assertz(loss_monitor(P,R))`);
      const entry=n.swiWasmRemoteActorConnections[url],incoming=entry.socket.onmessage,held=[];
      entry.socket.onmessage=e=>{if(JSON.parse(e.data).type==='down')held.push(e);else incoming(e);};
      await new Promise(resolve=>{entry.socket.addEventListener('close',resolve,{once:true});entry.socket.close();});
      await run('loss_monitor(P,R),receive({down(P,R,connection_closed)->true},[timeout(3),on_timeout(throw(no_observation_loss))]),demonitor(R,[flush])');
      for(const e of held)incoming(e);
      await run(`toplevel_spawn(New,[node(${u}),session(true)]),toplevel_halt(New),loss_monitor(_,R),receive({down(_,R,_)->throw(old_monitor_restored)},[timeout(0),on_timeout(true)])`);
     }
     if(id==='BN-016'){
      const a=await run(`toplevel_spawn(P,[node(${u}),session(true)]),monitor(P,R),monitor(P,Keep),assertz(retry_monitor(P,R,Keep))`),ref=a.data[0].R;
      const original=n.demonitorSwiWasmActor.bind(n);let release;
      n.demonitorSwiWasmActor=(watcher,r,operation)=>String(r)===String(ref)?new Promise(resolve=>{release=()=>resolve(original(watcher,r,operation));}):original(watcher,r,operation);
      await run('retry_monitor(P,R,_),self(S),send(S,down(P,R,before_timeout)),catch(demonitor(R,[flush]),error(remote_demonitor_timeout(P),_),Timed=true),Timed==true,receive({down(P,R,before_timeout)->true},[timeout(0),on_timeout(throw(timeout_flushed_mailbox))])');
      check(n.swiWasmActorMonitors.some(m=>m.ref===String(ref)),'timeout retains the monitor for retry');
      release();await Promise.resolve();await Promise.resolve();
      check(n.swiWasmActorMonitors.some(m=>m.ref===String(ref)),'late timed-out withdrawal cannot remove retry state');
      n.demonitorSwiWasmActor=original;
      await run('retry_monitor(P,R,Keep),demonitor(R,[flush]),demonitor(R),exit(P,kill),receive({down(P,Keep,_)->true},[timeout(3)]),receive({down(_,R,_)->throw(retry_left_monitor)},[timeout(0),on_timeout(true)])');
     }
     if(id==='BN-013'){
      await fetch(base+'/return/arm/'+peer);
      await run(`toplevel_spawn(T,[node(${u}),session(true)]),assertz(return_checker(T)),self(S),spawn((self(Owner),register(multihop_closed_home,Owner),promise(${answer},true,R,[template(mark)]),spawn(spawn((whereis(multihop_closed_home,_),send(Owner,revived)),_,[node(${u})]),_,[node(${q(other)})]),receive({revived->send(S,revived)})),Root,[node(${u})]),assertz(return_root(Root))`);
      const until=async predicate=>{const end=Date.now()+4000;while(true){const state=await(await fetch(base+'/return/state/'+peer)).json();if(predicate(state))return state;check(Date.now()<end,'return admission barrier deadline');await new Promise(r=>setTimeout(r,5));}};
      await until(s=>s.entered);await n.closeSwiWasmClientContext();
      await fetch(base+'/return/release/'+peer);const state=await until(s=>s.result);
      check(state.result.includes('rejected(')&&state.result.includes('closed_client_context'),'late real return frame cannot reattach a retired origin '+state.result);
      await run('return_checker(T),toplevel_call_synch(T,once(whereis(multihop_closed_home,undefined)),A,[template(ok),timeout(3)]),nonvar(A),A=success(T,[ok],false),receive({revived->throw(closed_origin_revived)},[timeout(0),on_timeout(true)])');
     }
     if(id==='BN-012'){
      await run(`promise(${answer},true,BR,[template(mark)]),self(S),spawn(receive({multi(Native)->self(Me),whereis(browser_home,Me),yield(BR,Browser),send(S,whole(Native,Browser))}),Local,[]),register(browser_home,Local),spawn((self(Owner),register(multihop_home,Owner),promise(${answer},true,R,[template(mark)]),spawn(spawn((whereis(multihop_home,Visible),Visible==Owner,yield(R,A),send(Owner,hop_result(A))),_,[node(${u})]),_,[node(${q(other)})]),receive({hop_result(A)->send(Local,multi(A))})),Origin,[node(${u}),monitor(true)]),receive({whole(success([mark],false),success([mark],false))->true;down(Origin,Origin,Why) if Why\\==true->throw(multihop_root_down(Why))},[timeout(4),on_timeout(throw(no_multihop_return))])`);
     }
     if(id==='BN-008'){
      const uri=q(base+'/native/'+peer);
      await run(`promise(${uri},X=mark,R,[template(v(X))]),yield(R,success([v(mark)],false)),rpc(${uri},(A=mark,B=A)),A==mark,B==mark`);
     }
     if(id==='BN-009'){
      const entry=await n.ensureSwiWasmRemoteActorConnection(url),socket=entry.socket;
      const reply=await new Promise((resolve,reject)=>{const timer=setTimeout(()=>reject(Error('forged close response missing')),3000);socket.addEventListener('message',function receive(e){const m=JSON.parse(e.data);if(m.request_id==='forged-close'){clearTimeout(timer);socket.removeEventListener('message',receive);resolve(m);}});socket.send(JSON.stringify({command:'context_close',request_id:'forged-close',lineage:'a'.repeat(32),context_origin:url}));});
      check(reply.type==='error','ordinary browser cannot select a delegated scope');
      await run(remote('send(S,still_open)')+',receive({still_open->true},[timeout(3),on_timeout(throw(forged_close_affected_owner))])');
     }
     if(id==='BN-010'){
      const entry=await n.ensureSwiWasmRemoteActorConnection(url);await n.closeSwiWasmClientContext();
      await new Promise(resolve=>{entry.socket.addEventListener('close',resolve,{once:true});entry.socket.close();});
      let denied=false;try{await n.ensureSwiWasmRemoteActorConnection(url);}catch(e){denied=/context closed/.test(e.message);}
      check(denied,'closed browser context cannot reconnect as a fresh context');
     }
     if(id==='BN-011'){
      const NativeWS=window.WebSocket,traffic=[];let captured,entered;
      const at=new Promise(r=>{entered=r;});
      window.WebSocket=class extends NativeWS{
       constructor(...args){super(...args);this.addEventListener('message',e=>{const m=JSON.parse(e.data);if(m.type==='transport_welcome'){e.stopImmediatePropagation();captured=e;entered();}});}
       send(data){traffic.push(JSON.parse(data));super.send(data);}
      };
      const pending=n.query(`spawn(true,_,[node(${u})])`).then(answer=>({answer}),error=>({error:String(error)}));
      await at;const closing=n.closeSwiWasmClientContext();
      check(n.swiWasmClientContextClosed===true,'local closure precedes delayed handshake');
      const entry=n.swiWasmRemoteActorConnections[url];entry.socket.onmessage(captured);
      await closing;const result=await pending;
      check(!result.answer||result.answer.type!=='success','late handshake cannot activate pending spawn');
      check(!traffic.some(m=>m.command==='spawn'),'no creation dispatched after closure');
      check(entry.contextRetired===true,'real native context retirement acknowledged after delayed handshake');
     }
     if(id==='BN-007'){
      await n.ensureSwiWasmRemoteActorConnection(url);await Promise.resolve(n.closeSwiWasmClientContext());
      const socket=n.swiWasmRemoteActorConnections[url].socket;
      const reply=await new Promise((resolve,reject)=>{const timer=setTimeout(()=>reject(Error('late raw spawn response missing')),3000);socket.addEventListener('message',function receive(e){const m=JSON.parse(e.data);if(m.request_id==='late-context-spawn'){clearTimeout(timer);socket.removeEventListener('message',receive);resolve(m);}});socket.send(JSON.stringify({command:'spawn',request_id:'late-context-spawn',goal:'true',options:'[]'}));});
      check(reply.type==='error','late raw creation rejected by native admission '+JSON.stringify(reply));
     }
     return checks;
    }finally{nodes.forEach(n=>n.dispose());}
   },{mode,url,id,base,peer,other:peers[peer==='swi'?'trealla':'swi']}),12000,mode+' '+id+' '+peer);row.status='pass';
  }catch(e){row.status='fail';row.detail=String(e.stack||e);}finally{await page.close();}
  rows.push(row);save();console.log(row.candidate,row.id,row.status,row.detail||'');
 }}finally{clearTimeout(watchdog);await browser.close();await new Promise(r=>server.close(r));}
 process.exitCode=rows.some(x=>x.status==='fail')?1:0;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
