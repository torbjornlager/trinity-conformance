'use strict';
const fs=require('fs'),path=require('path'),{chromium}=require('playwright');
const output=path.join(__dirname,'public-browser.json'),rows=[];
function save(){fs.writeFileSync(output,JSON.stringify({scope:'Real Chrome loading deployed N0-N6 assets; real N1 HTTPS promise transport, same-context sharing and separate-context denial in both browser modes',results:rows,counts:{pass:rows.filter(r=>r.status==='pass').length,fail:rows.filter(r=>r.status==='fail').length}},null,2)+'\n');}
(async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try {
  for(let n=0;n<7;n++) for(const mode of ['worker','main']){
   const page=await browser.newPage();
   try{
    await page.goto('https://n'+n+'.elfenbenstornet.se/demonstrator');
    await page.waitForFunction(()=>typeof SwiWasmNode==='object');
    const labels=await page.evaluate(async mode=>{
     const nodes=[],labels=[];
     const create=async mode=>{const node=SwiWasmNode.create({mode,workerUrl:new URL('../swi_wasm_actor_worker.js',location.href).href,engineUrl:new URL('../swipl-bundle.js',location.href).href,prologBaseUrl:new URL('../wasm/',location.href).href,sharedDatabaseUrl:null});nodes.push(node);await node.open();return node;};
     const run=async(node,goal,label)=>{const answer=await node.query(goal);if(answer.type!=='success')throw Error(label+': '+JSON.stringify(answer));labels.push(label);return answer;};
     try{
      const node=await create(mode);
      await new Promise(r=>setTimeout(r,1500));
      await run(node,"promise('https://n1.elfenbenstornet.se',X=ok,R,[template(v(X)),http_timeout(5)]),self(S),spawn((yield(R,A),send(S,result(A))),_,[link(false)]),receive({result(success([v(ok)],false))->true},[timeout(8),on_timeout(throw(no_promise_result))]),var(X)",'same-context child collects parent promise');
      await new Promise(r=>setTimeout(r,1500));
      const made=await node.query("promise('https://n1.elfenbenstornet.se',true,R,[template(v(ok)),http_timeout(5)])");
      if(made.type!=='success'||!made.data[0].R)throw Error('promise creation: '+JSON.stringify(made));
      const ref=made.data[0].R,other=await create('worker');
      await run(other,'catch(yield('+ref+',_),error(existence_error(promise,'+ref+'),_),Missing=true),Missing==true,promise_cleanup('+ref+')','foreign context cannot collect or dispose');
      await run(node,'yield('+ref+',success([v(ok)],false))','owner still collects after foreign cleanup');
     }finally{nodes.forEach(node=>node.dispose());}
     return labels;
    },mode);
    labels.forEach(title=>{rows.push({node:n,mode,title,status:'pass'});console.log('N'+n,mode,title,'pass');});
   }catch(e){rows.push({node:n,mode,status:'fail',detail:String(e.stack||e)});console.error('N'+n,mode,String(e));}
   finally{save();await page.close();}
  }
 }finally{await browser.close();}
 if(rows.some(r=>r.status==='fail'))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
