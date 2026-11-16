// Test-only adapter. The manifest owns assertions; the runtime repo owns engine setup.
const fs=require('fs'),path=require('path');
const [root,mode,manifest,report]=process.argv.slice(2);
if(!['worker','main'].includes(mode))throw new Error('mode must be worker or main');
const pack=JSON.parse(fs.readFileSync(manifest,'utf8'));
const {runExternalContractCases}=require(path.join(path.resolve(root),'tests/wasm/swi_wasm_contracts.js'));
const started=new Date().toISOString(),clock=Date.now();
// The packaged engine runs sandbox(off): cases that require a goal sandbox do not apply.
const capabilities=new Set();
const applicable=pack.cases.filter(c=>(c.requires||[]).every(r=>capabilities.has(r)));
const skipped=pack.cases.filter(c=>!applicable.includes(c)).map(c=>({id:c.id,title:c.title,status:'unsupported',detail:'requires '+(c.requires||[]).filter(r=>!capabilities.has(r)).join(', ')+' (engine runs sandbox(off))'}));
runExternalContractCases(mode,applicable).then(ran=>{
 const order=new Map(pack.cases.map((c,i)=>[c.id,i]));
 const results=[...ran,...skipped].sort((x,y)=>order.get(x.id)-order.get(y.id));
 const count=s=>results.filter(r=>r.status===s).length;
 const counts={pass:count('pass'),fail:count('fail'),unsupported:count('unsupported'),observed:0,diagnostic_error:0};
 const output={schema_version:2,baseline:'0.1',suite:pack.suite,scope:pack.scope,candidate:'swi-wasm-'+mode,
   advertised_profile:'actor',endpoint:'embedded-'+mode,peer:null,started_at:started,duration_ms:Date.now()-clock,counts,results};
 fs.mkdirSync(path.dirname(report),{recursive:true});fs.writeFileSync(report,JSON.stringify(output,null,2)+'\n');
 console.log(JSON.stringify(counts));process.exit(counts.fail?1:0);
}).catch(error=>{console.error(error.stack||error);process.exit(1);});
