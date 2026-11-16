from pathlib import Path
import json,shutil,subprocess,os,hashlib,sys
O=Path(__file__).parent;P=Path('/Users/lager/trinity-demonstrator/.trinity/browser-runtime/current').resolve();F=O/'browser-fixture-qualified';shutil.copytree(P/'web/wasm',F);shutil.copyfile(P/'tests/fixtures/wasm/shared_db.pl',F/'shared_db.pl');Q=O/'browser-qualified';Q.mkdir();rows=[]
sys.path.insert(0,str(P/'tools'));from package_runtime import verify
m=verify(P)
for mode,suite in [(m,s) for s in ['language-actor-0.1','source-directives-0.1'] for m in ['worker','main']]:
 out=Q/(suite+'-'+mode+'.json');log=Q/(suite+'-'+mode+'.log');env={**os.environ,'WP_WASM_SOURCE_DIR':str(F),'NODE_PATH':'/Users/lager/eclipse-node/.trinity/appendix-b11.ujYfkE/node_modules'}
 with log.open('wb') as f:r=subprocess.run(['/Users/lager/.nvm/versions/node/v22.23.4/bin/node',str(O/'conformance/adapters/wasm.cjs'),str(P),mode,str(O/'conformance/cases'/(suite+'.json')),str(out)],env=env,stdout=f,stderr=f,timeout=180)
 rows.append(dict(mode=mode,suite=suite,exit_code=r.returncode,report_present=out.exists(),counts=json.loads(out.read_text())['counts'] if out.exists() else None));print(mode,rows[-1],flush=True)
(Q/'provenance.json').write_text(json.dumps(dict(package=str(P),manifest_sha256=hashlib.sha256((P/'manifest.json').read_bytes()).hexdigest(),source=m['source'],fixture_shared_db_sha256=hashlib.sha256((F/'shared_db.pl').read_bytes()).hexdigest(),note='Packaged schema/runtime and repository-owned test shared DB supplied exactly as packaged runtime test.py; no test or runtime source edits',runs=rows),indent=2)+'\n')
