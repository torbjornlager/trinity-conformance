// Manifest assertions run in independent processes, matching native shell isolation.
const fs=require('fs'),path=require('path'),{spawnSync}=require('child_process');
const [root,mode,manifest,report,caseId]=process.argv.slice(2);
if(!['worker','main'].includes(mode))throw new Error('mode must be worker or main');
const pack=JSON.parse(fs.readFileSync(manifest,'utf8'));
async function main(){
 const started=new Date().toISOString(),clock=Date.now();let results=[];
 if(caseId){
  const c=pack.cases.find(c=>c.id===caseId);if(!c)throw Error('unknown case '+caseId);
  const {runExternalContractCases}=require(path.join(path.resolve(root),'tests/wasm/swi_wasm_contracts.js'));
  results=await runExternalContractCases(mode,[c]);
 }else{
  fs.mkdirSync(path.dirname(report),{recursive:true});
  for(const c of pack.cases){
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
 const counts={pass:results.filter(r=>r.status==='pass').length,fail:results.filter(r=>r.status==='fail').length,unsupported:0,observed:0,diagnostic_error:0};
 const output={schema_version:2,baseline:'0.1',suite:pack.suite,scope:pack.scope,candidate:'swi-wasm-'+mode,
  advertised_profile:'actor',endpoint:'embedded-'+mode,peer:null,started_at:started,duration_ms:Date.now()-clock,counts,results};
 fs.mkdirSync(path.dirname(report),{recursive:true});fs.writeFileSync(report,JSON.stringify(output,null,2)+'\n');
 console.log(JSON.stringify(counts));process.exitCode=counts.fail?1:0;
}
main().catch(error=>{console.error(error.stack||error);process.exitCode=1;});
