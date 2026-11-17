'use strict';
// All deadlines run in this Node process, outside the CPU-bound renderer.
const fs=require('fs'),path=require('path'),http=require('http'),crypto=require('crypto');
const {chromium}=require('playwright');
const runtime=path.resolve(process.env.LIBRARY_RUNTIME_ROOT||'');
if(!process.env.LIBRARY_RUNTIME_ROOT)throw Error('Set LIBRARY_RUNTIME_ROOT');
const manifest=process.env.LIBRARY_MANIFEST||path.join(__dirname,'../cases/library-noncompletion-0.1.json');
const raw=fs.readFileSync(manifest),pack=JSON.parse(raw),rows=[],entries=new Map(),owned=new Set();
const output=process.env.LIBRARY_REPORT;
const sha=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const delay=ms=>new Promise(r=>setTimeout(r,ms));
function deadline(p,ms,label){let timer;return Promise.race([p,new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error(label+' deadline')),ms);})]).finally(()=>clearTimeout(timer));}
const runtimeFiles=Object.fromEntries(['web/vendor/swi-wasm-node.js','web/swi_wasm_actor_worker.js','web/swipl-bundle.js'].map(f=>[f,sha(path.join(runtime,f))]));
function save(){if(output)fs.writeFileSync(output,JSON.stringify({suite:pack.suite,scope:'Isolated real Chrome sessions; externally killed browsers and fresh-session recovery, not same-session abort or public transport',manifest_sha256:sha(manifest),adapter_sha256:sha(__filename),runtime_files_sha256:runtimeFiles,results:rows,counts:{pass:rows.filter(r=>r.status==='pass').length,fail:rows.filter(r=>r.status==='fail').length}},null,2)+'\n');}
const server=http.createServer((req,res)=>{
 const parsed=new URL(req.url,'http://localhost');
 if(parsed.pathname.startsWith('/entry/')){
  const key=parsed.pathname.replace(/\/call$/,'');
  const item=entries.get(key)||{count:0,finished:false,requests:[]};
  item.count++;item.requests.push(Object.fromEntries(parsed.searchParams));entries.set(key,item);
  const body='success([v],false).\n';res.writeHead(200,{'Content-Length':Buffer.byteLength(body)});
  res.on('finish',()=>{item.finished=true;});res.end(body);return;
 }
 if(parsed.pathname==='/__countall.html'){res.setHeader('Content-Type','text/html; charset=utf-8');res.end('<meta charset="utf-8"><script src="/swi_wasm_actor_worker.js"></script><script src="/vendor/swi-wasm-node.js"></script>');return;}
 const file=path.resolve(runtime,'web','.'+parsed.pathname);
 if(!file.startsWith(path.join(runtime,'web')+path.sep)){res.writeHead(403);res.end();return;}
 fs.readFile(file,(error,data)=>{if(error){res.writeHead(404);res.end();return;}res.setHeader('Content-Type',file.endsWith('.js')?'text/javascript; charset=utf-8':file.endsWith('.wasm')?'application/wasm':'text/plain');res.end(data);});
});
function prologAtom(s){return "'"+s.replace(/\\/g,'\\\\').replace(/'/g,"''")+"'";}
function entry(key){return structuredClone(entries.get(key)||{count:0,finished:false,requests:[]});}
let base;
async function open(mode){
 const owner=await chromium.launchServer({executablePath:process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,timeout:15000});owned.add(owner);
 const browser=await chromium.connect(owner.wsEndpoint());
 const page=await browser.newPage();
 await page.goto(base+'/__countall.html');
 await page.evaluate(async mode=>{
  window.libraryNode=SwiWasmNode.create({mode,workerUrl:new URL('/swi_wasm_actor_worker.js',location.href).href,engineUrl:new URL('/swipl-bundle.js',location.href).href,prologBaseUrl:new URL('/wasm/',location.href).href,sharedDatabaseUrl:null});
  await libraryNode.open({source:''});
 },mode);
 return {owner,browser,page};
}
async function kill(session,timeout){
 const started=performance.now(),process=session.owner.process();
 await deadline(session.owner.kill(),timeout,'browser termination');owned.delete(session.owner);
 return {confirmed:process.exitCode!==null||process.signalCode!==null,duration_ms:performance.now()-started,exit_code:process.exitCode,signal:process.signalCode};
}
async function control(session,mode,c,phase){
 const key='/entry/'+mode+'-'+c.id+'-'+phase;
 const goal='LibraryEntryURI='+prologAtom(base+key)+',('+c.warmup_goal+'),LibraryCheck=passed';
 const answer=await deadline(session.page.evaluate(goal=>libraryNode.query(goal,{limit:1}),goal),8000,phase);
 const marker=entry(key);
 const passed=answer.type==='success'&&answer.more===false&&answer.data.length===1&&answer.data[0].LibraryCheck==='passed'&&marker.count===1&&marker.finished;
 if(!passed)throw Error('finite '+phase+' control failed '+JSON.stringify({answer,marker}));
 return {passed,entry_count:marker.count,answer,requests:marker.requests};
}
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));base='http://127.0.0.1:'+server.address().port;
 const watchdog=setTimeout(()=>{console.error('External countall browser watchdog expired');for(const owner of owned)owner.kill().catch(()=>{});setTimeout(()=>process.exit(2),4000).unref();},90000);
 try{
  for(const mode of ['worker','main'])for(const c of pack.cases){
   const row={candidate:'swi-wasm-'+mode,id:c.id,title:c.title},observed={};
   let session,stopping=false,terminal=null;
   try{
    const {observation_ms:window,entry_timeout_ms:entryTimeout,termination_timeout_ms:terminationTimeout}=c.bounded_noncompletion;
    if(![window,entryTimeout,terminationTimeout].every(Number.isInteger)||window<100||window>2000||entryTimeout<100||entryTimeout>10000||terminationTimeout<100||terminationTimeout>10000)throw Error('invalid bounds');
    session=await deadline(open(mode),20000,'browser startup');
    observed.warmup=await control(session,mode,c,'warmup');
    const key='/entry/'+mode+'-'+c.id+'-probe',goal='LibraryEntryURI='+prologAtom(base+key)+',('+c.goal+')';
    session.page.evaluate(goal=>libraryNode.query(goal,{limit:1}),goal).then(answer=>{if(!stopping)terminal={answer};},error=>{if(!stopping)terminal={error:String(error)};});
    await deadline((async()=>{while(!entry(key).finished){if(terminal)throw Error('query terminated before entry '+JSON.stringify(terminal));await delay(5);}})(),entryTimeout,'callback entry');
    const started=performance.now(),until=started+window;
    while(performance.now()<until)await delay(Math.max(1,until-performance.now()));
    const marker=entry(key);
    observed.probe={entry_count:marker.count,entry_response_finished:marker.finished,requests:marker.requests,elapsed_ms:performance.now()-started,terminal,alive_before_termination:session.owner.process().exitCode===null&&session.owner.process().signalCode===null};
    stopping=true;observed.termination=await kill(session,terminationTimeout);session=null;
    session=await deadline(open(mode),20000,'recovery startup');
    observed.recovery=await control(session,mode,c,'recovery');
    await deadline(session.owner.close(),3000,'recovery close');owned.delete(session.owner);session=null;
    if(marker.count!==1||!observed.probe.entry_response_finished||terminal||!observed.probe.alive_before_termination||observed.probe.elapsed_ms<window||!observed.termination.confirmed||observed.termination.duration_ms>terminationTimeout)throw Error('noncompletion observation failed');
    row.status='pass';
   }catch(error){row.status='fail';row.detail=String(error.stack||error);}
   finally{stopping=true;for(const owner of [...owned]){await deadline(owner.kill(),3000,'cleanup').catch(()=>{});owned.delete(owner);}}
   row.observation=observed;rows.push(row);save();console.log(row.candidate,c.id,row.status);
  }
 }finally{clearTimeout(watchdog);for(const owner of owned)await owner.kill();await new Promise(r=>server.close(r));}
 process.exitCode=rows.some(r=>r.status==='fail')?1:0;
})().catch(error=>{console.error(error);server.close();process.exitCode=1;});
