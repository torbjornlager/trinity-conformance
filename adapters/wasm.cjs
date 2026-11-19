// Test-only adapter. The manifest owns assertions; the runtime repo owns engine setup.
// Manifest assertions run in independent processes, matching native shell isolation.
const fs=require('fs'),path=require('path'),{spawnSync}=require('child_process');
const [root,mode,manifest,report,caseId]=process.argv.slice(2);
if(!['worker','main'].includes(mode))throw new Error('mode must be worker or main');
const pack=JSON.parse(fs.readFileSync(manifest,'utf8'));
// The packaged engine runs sandbox(off): cases that require a goal sandbox do not apply.
const capabilities=new Set();
const unmet=c=>(c.requires||[]).filter(r=>!capabilities.has(r));
async function main(){
 // The embedded coordinator has no source-loading API. Use the maintained
 // session adapter rather than executing source-dependent goals without helpers.
 if(!caseId && (pack.source || pack.cases.some(c=>c.source))){
  const child=spawnSync(process.execPath,[path.join(__dirname,'wasm_actor_cases.cjs')],{
   env:{...process.env,LIBRARY_RUNTIME_ROOT:path.resolve(root),LIBRARY_MANIFEST:path.resolve(manifest),LIBRARY_REPORT:path.resolve(report),LIBRARY_MODES:mode},
   stdio:'inherit'
  });
  if(child.error)throw child.error;
  if(child.status!==0 && fs.existsSync(report)){
   const observed=JSON.parse(fs.readFileSync(report,'utf8'));
   // Exit 1 is expected when recorded assertions fail; keep other passes.
   // A nonzero exit with only passing rows is an infrastructure failure.
   if(!observed.results.some(r=>r.status==='fail'))for(const row of observed.results)if(row.status==='pass')Object.assign(row,{status:'fail',detail:'source-aware adapter exited '+child.status});
   observed.counts={...observed.counts,pass:observed.results.filter(r=>r.status==='pass').length,fail:observed.results.filter(r=>r.status==='fail').length};
   fs.writeFileSync(report,JSON.stringify(observed,null,2)+'\n');
  }
  process.exitCode=child.status===null?2:child.status;
  return;
 }

 const started=new Date().toISOString(),clock=Date.now();let results=[];
 if(caseId){
  const c=pack.cases.find(c=>c.id===caseId);if(!c)throw Error('unknown case '+caseId);
  const {runExternalContractCases}=require(path.join(path.resolve(root),'tests/wasm/swi_wasm_contracts.js'));
  results=await runExternalContractCases(mode,[c]);
 }else{
  fs.mkdirSync(path.dirname(report),{recursive:true});
  for(const c of pack.cases){
   if(unmet(c).length){
    results.push({id:c.id,title:c.title,status:'unsupported',detail:'requires '+unmet(c).join(', ')+' (engine runs sandbox(off))'});
    continue;
   }
   const file=report+'.'+c.id+'.tmp',caseStart=Date.now();
   const child=spawnSync(process.execPath,[__filename,root,mode,manifest,file,c.id],{env:process.env,encoding:'utf8',timeout:40000});
   if(fs.existsSync(file)){
    const rows=JSON.parse(fs.readFileSync(file,'utf8')).results;fs.unlinkSync(file);
    if(rows.length!==1||rows[0].id!==c.id)throw Error('invalid case accounting for '+c.id);
    if(child.status!==0 && rows[0].status==='pass')rows[0]={id:c.id,title:c.title,status:'fail',detail:'adapter exited '+child.status,duration_ms:Date.now()-caseStart};
    results.push(...rows);
   }
   else results.push({id:c.id,title:c.title,status:'fail',detail:child.error?String(child.error):'adapter exited '+child.status+': '+child.stderr,duration_ms:Date.now()-caseStart});
  }
 }
 const count=s=>results.filter(r=>r.status===s).length;
 const counts={pass:count('pass'),fail:count('fail'),unsupported:count('unsupported'),observed:0,diagnostic_error:0};
 const output={schema_version:2,baseline:'0.1',suite:pack.suite,scope:pack.scope,candidate:'swi-wasm-'+mode,
  advertised_profile:'actor',endpoint:'embedded-'+mode,peer:null,started_at:started,duration_ms:Date.now()-clock,counts,results};
 fs.mkdirSync(path.dirname(report),{recursive:true});fs.writeFileSync(report,JSON.stringify(output,null,2)+'\n');
 console.log(JSON.stringify(counts));process.exitCode=counts.fail?1:0;
}
main().catch(error=>{console.error(error.stack||error);process.exitCode=1;});
