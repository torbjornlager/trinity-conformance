'use strict';
// One browser page/coordinator is one client context. Both engines run the same steps.
const fs=require('fs'),path=require('path'),http=require('http'),crypto=require('crypto');
const {chromium}=require('playwright');
const root=path.resolve(process.env.LIBRARY_RUNTIME_ROOT),manifest=path.join(__dirname,'../cases/client-naming-0.1.json');
const raw=fs.readFileSync(manifest),pack=JSON.parse(raw),rows=[],report=process.env.LIBRARY_REPORT;
function save(){fs.writeFileSync(report,JSON.stringify({suite:pack.suite,manifest_sha256:crypto.createHash('sha256').update(raw).digest('hex'),adapter_sha256:crypto.createHash('sha256').update(fs.readFileSync(__filename)).digest('hex'),package_manifest_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'manifest.json'))).digest('hex'),scope:'Independent browser page/coordinator contexts; not multiple clients hosted inside one browser coordinator. No service-publication qualification.',results:rows,counts:{pass:rows.filter(r=>r.status==='pass').length,fail:rows.filter(r=>r.status==='fail').length,unsupported:rows.filter(r=>r.status==='unsupported').length}},null,2)+'\n');}
const server=http.createServer((req,res)=>{
 const pathname=new URL(req.url,'http://localhost').pathname;
 if(pathname==='/__naming.html'){res.setHeader('Content-Type','text/html; charset=utf-8');res.end('<meta charset="utf-8"><script src="/swi_wasm_actor_worker.js"></script><script src="/vendor/swi-wasm-node.js"></script>');return;}
 const file=path.resolve(root,'web','.'+pathname);if(!file.startsWith(path.join(root,'web')+path.sep)){res.writeHead(403);res.end();return;}
 fs.readFile(file,(e,d)=>{if(e){res.writeHead(404);res.end();return;}res.setHeader('Content-Type',file.endsWith('.js')?'text/javascript; charset=utf-8':file.endsWith('.wasm')?'application/wasm':'text/plain');res.end(d);});
});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const browser=await chromium.launch({executablePath:process.env.CHROME_PATH,headless:true});
 const watchdog=setTimeout(()=>{console.error('client naming watchdog');browser.close();setTimeout(()=>process.exit(2),3000).unref();},180000);
 try{for(const mode of ['worker','main'])for(const c of pack.cases){
  const pages={},row={candidate:'swi-wasm-'+mode,id:c.id,title:c.title,trace:[]};
  try{
   // A page owns a retained browser session. A new toplevel on the same connection
   // has no equivalent in the current high-level browser API: keep that case explicit.
   if(c.steps.some(s=>s.action==='new_toplevel')){row.status='unsupported';row.detail='Browser session API does not expose multiple toplevels on one retained connection';}
   else{
    for(const who of ['a','b']){const page=await browser.newPage();pages[who]=page;page.setDefaultTimeout(15000);await page.goto('http://127.0.0.1:'+server.address().port+'/__naming.html');await page.evaluate(async mode=>{window.n=SwiWasmNode.create({mode,workerUrl:new URL('/swi_wasm_actor_worker.js',location.href).href,engineUrl:new URL('/swipl-bundle.js',location.href).href,prologBaseUrl:new URL('/wasm/',location.href).href,sharedDatabaseUrl:null});await n.open();},mode);}
    const name='cn_'+crypto.randomBytes(10).toString('hex');
    for(const s of c.steps){let result;
     if(s.action==='close'){await pages[s.client].close();delete pages[s.client];result={closed:true};}
     else{result=await pages[s.client].evaluate(goal=>n.query('('+goal+'),ScopeCheck=passed',{limit:1}),s.goal.replaceAll('__NAME__',name));if(result.type!=='success'||result.more!==false||result.data.length!==1||result.data[0].ScopeCheck!=='passed')throw Error(JSON.stringify(result));}
     row.trace.push({step:s,observation:result});
    }
    row.status='pass';
   }
  }catch(e){row.status='fail';row.detail=String(e.stack||e);}
  finally{for(const page of Object.values(pages))await page.close();}
  rows.push(row);save();console.log(row.candidate,c.id,row.status);
 }}finally{clearTimeout(watchdog);await browser.close();await new Promise(r=>server.close(r));}
 process.exitCode=rows.some(r=>r.status!=='pass')?1:0;
})().catch(e=>{console.error(e);process.exitCode=2;server.close();});
