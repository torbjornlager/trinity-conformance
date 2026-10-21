// Test-only adapter. The manifest owns assertions; the runtime repo owns engine setup.
const fs=require('fs'),path=require('path');
const [root,mode,manifest,report]=process.argv.slice(2);
if(!['worker','main'].includes(mode))throw new Error('mode must be worker or main');
const pack=JSON.parse(fs.readFileSync(manifest,'utf8'));
const {runExternalContractCases}=require(path.join(path.resolve(root),'tests/wasm/swi_wasm_contracts.js'));
const started=new Date().toISOString(),clock=Date.now();
runExternalContractCases(mode,pack.cases).then(results=>{
 const counts={pass:results.filter(r=>r.status==='pass').length,fail:results.filter(r=>r.status==='fail').length,unsupported:0,observed:0,diagnostic_error:0};
 const output={schema_version:2,baseline:'0.1',suite:pack.suite,scope:pack.scope,candidate:'swi-wasm-'+mode,
   advertised_profile:'actor',endpoint:'embedded-'+mode,peer:null,started_at:started,duration_ms:Date.now()-clock,counts,results};
 fs.mkdirSync(path.dirname(report),{recursive:true});fs.writeFileSync(report,JSON.stringify(output,null,2)+'\n');
 console.log(JSON.stringify(counts));process.exit(counts.fail?1:0);
}).catch(error=>{console.error(error.stack||error);process.exit(1);});
