'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto'),{chromium}=require('playwright');
const raw=fs.readFileSync(path.join(__dirname,'../../cases/standard-library-0.1.json')),pack=JSON.parse(raw),rows=[];
function save(){fs.writeFileSync(path.join(__dirname,'public-library-browser.json'),JSON.stringify({scope:'All shared library cases in real Chrome using deployed N0-N6 assets in worker and main modes',manifest_sha256:crypto.createHash('sha256').update(raw).digest('hex'),results:rows,counts:{pass:rows.filter(r=>r.status==='pass').length,fail:rows.filter(r=>r.status==='fail').length}},null,2)+'\n');}
(async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try{
  for(let n=0;n<7;n++)for(const mode of ['worker','main']){
   const page=await browser.newPage();
   try{
    await page.goto('https://n'+n+'.elfenbenstornet.se/demonstrator');
    await page.waitForFunction(()=>typeof SwiWasmNode==='object');
    await page.evaluate(async({mode,source})=>{
     window.libraryNode=SwiWasmNode.create({mode,workerUrl:new URL('../swi_wasm_actor_worker.js',location.href).href,engineUrl:new URL('../swipl-bundle.js',location.href).href,prologBaseUrl:new URL('../wasm/',location.href).href,sharedDatabaseUrl:null});
     await libraryNode.open({source});
    },{mode,source:pack.source});
    for(const c of pack.cases){
     const row={node:n,candidate:'swi-wasm-'+mode,id:c.id};
     try{
      row.observation=await page.evaluate(async goal=>libraryNode.query('('+goal+'),LibraryCheck=passed',{limit:1}),c.goal);
      if(row.observation.type!=='success'||row.observation.more!==false||row.observation.data.length!==1)throw Error(JSON.stringify(row.observation));row.status='pass';
     }catch(e){row.status='fail';row.detail=String(e);}
     rows.push(row);
    }
    save();console.log('N'+n,mode,rows.filter(r=>r.node===n&&r.candidate==='swi-wasm-'+mode&&r.status==='pass').length,'pass');
   }catch(e){rows.push({node:n,candidate:'swi-wasm-'+mode,id:'initialization',status:'fail',detail:String(e)});save();}
   finally{await page.evaluate(()=>libraryNode.dispose()).catch(()=>{});await page.close();}
  }
 }finally{await browser.close();save();}
 process.exitCode=rows.some(r=>r.status==='fail')?1:0;
})().catch(e=>{console.error(e);process.exitCode=1;});
