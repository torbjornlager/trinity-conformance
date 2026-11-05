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
 try{for(const mode of ['worker','main'])for(const [peer,url] of Object.entries(peers))for(const id of (process.env.BROWSER_CONTEXT_CASES||'BN-001,BN-002,BN-003,BN-004,BN-005,BN-006,BN-007,BN-008,BN-009,BN-010,BN-011').split(',')){
  const row={candidate:'swi-wasm-'+mode,id:id+'-'+peer,peer};const page=await browser.newPage();
  try{
   await page.goto(base+'/__context.html');
   row.observation=await deadline(page.evaluate(async({mode,url,id,base,peer})=>{
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
   },{mode,url,id,base,peer}),12000,mode+' '+id+' '+peer);row.status='pass';
  }catch(e){row.status='fail';row.detail=String(e.stack||e);}finally{await page.close();}
  rows.push(row);save();console.log(row.candidate,row.id,row.status,row.detail||'');
 }}finally{clearTimeout(watchdog);await browser.close();await new Promise(r=>server.close(r));}
 process.exitCode=rows.some(x=>x.status==='fail')?1:0;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
