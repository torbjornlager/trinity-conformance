from pathlib import Path
import json,hashlib,shutil,subprocess,datetime
R=Path('/Users/lager/trinity-conformance');O=R/'reports/2026-11-05-standard-library'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
for src,dst in [('/tmp/standard-library-browser-qualified-suite/standard-library-browser.json','browser.json'),('/tmp/standard-library-browser-qualified-suite/results.json','browser-suite.json'),('/tmp/standard-library-trealla-qualified.txt','trealla-suite.txt'),('/tmp/standard-library-gnu-qualified.txt','gnu-local-suite.txt'),('/tmp/standard-library-browser-qualified-package/manifest.json','browser-package-manifest.json')]:shutil.copy(src,O/dst)
shutil.copy(R/'cases/standard-library-0.1.json',O/'manifest.json')
for p in Path('/tmp/standard-library-browser-qualified-suite').glob('*.log'):shutil.copy(p,O/('browser-'+p.name))
pack=json.loads((O/'manifest.json').read_text());native=json.loads((O/'native.json').read_text());browser=json.loads((O/'browser.json').read_text())
assert len(pack['cases'])==65 and native['counts']=={'pass':325,'fail':0} and browser['counts']=={'pass':132,'fail':0}
assert native['manifest_sha256']==sha(O/'manifest.json')==browser['manifest_sha256']
roots={'swi':Path('/Users/lager/swi-prolog-node'),'trealla':Path('/Users/lager/trealla-port'),'gnu':Path('/Users/lager/gprolog-port')}
for name,record in native['sources'].items():
 for f,h in record['files_sha256'].items():assert sha(roots[name]/f)==h,(name,f)
for f,h in browser['runtime_files_sha256'].items():assert sha(Path('/Users/lager/swi-wasm-node')/f)==h,f
assert sha('/Users/lager/swi-wasm-node/tests/fixtures/standard-library.json')==sha('/Users/lager/trealla-port/standard_library_cases.json')==sha('/Users/lager/gprolog-port/isobase/standard_library_cases.json')==sha(O/'manifest.json')
for repo in ['swi-prolog-node','trealla-port','gprolog-port','swi-wasm-node','trinity-demonstrator']:
 root=Path('/Users/lager')/repo
 (O/(repo+'.diff')).write_bytes(subprocess.check_output(['git','diff'],cwd=root))
for repo,files in {'swi-prolog-node':['prolog/web_prolog/standard_library.pl'],'trealla-port':['standard_library_cases.json','tools/test-standard-library.py'],'gprolog-port':['isobase/standard_library_cases.json','isobase/standard_library_tests.py'],'swi-wasm-node':['tests/fixtures/standard-library.json','tests/wasm/swi_wasm_library_browser.cjs']}.items():
 for f in files:
  target=O/'new-files'/repo/f;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy(Path('/Users/lager')/repo/f,target)
log=(O/'trealla-suite.txt').read_text();assert log.rstrip().endswith('ALL all TESTS PASSED')
parts=log.split('SWI-Prolog: SWI-Prolog version',1)
trealla_counts={'unit':sum(s.startswith('=== ') for s in parts[0].splitlines()),'interop':sum(s.startswith('=== ') for s in parts[1].splitlines())}
bs=json.loads((O/'browser-suite.json').read_text());assert len(bs['runs'])==7 and all(r['exit_code']==0 for r in bs['runs'])
record={'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'development sources only; not committed, pinned, pushed or deployed','scope':'Required standard-library forms and described binding/solution semantics, selected formal errors and callback boundaries; not full ISO mode/error certification','before':{'cases_per_mode':57,'total':285,'pass':228,'fail':57},'after':{'cases_per_mode':65,'shared_five_modes':325,'native_retained_session':130,'browser_child':2,'total':457,'fail':0},'qualification':{'native':'LINT TEXT T0 T2 T5 T1_NATIVE T3_NATIVE T4_NATIVE plus HTTP visitor ownership','trealla_groups':trealla_counts,'gnu':'complete local-test plus inventory/status checks','browser_package_groups':7,'browser_package_dirty':True},'notes':['The suite was strengthened after the original 57-case baseline: empty callbacks, cuts, invalid generators and positional list/accumulator checks were added. Before and after manifests are separately hashed.','The mirrored runtime fixtures are byte-identical to the shared manifest. Runtime source hashes and browser runtime-file hashes were rechecked after qualification. Git diff hashes in native.json identify the run-start snapshots; later documentation edits do not change the checked runtime files.','The browser fixture initially omitted UTF-8 HTML/script declarations, corrupting the embedded binary in main mode. The corrected before run and all after runs use UTF-8; the initial fixture failure is retained separately.','Trealla uses a temporary runner copy with one-second fixture startup waits for the released x86 engine. Installed engines and public services are unchanged.','The test for an invalid higher-order closure checks type_error and its culprit without prescribing the atom-versus-callable refinement. The reference does not give a complete library error taxonomy; the full grouped error/ISO requirements remain unverified.'],'artifacts_sha256':{str(p.relative_to(O)):sha(p) for p in O.rglob('*') if p.is_file() and p.name!='verification.json'}}
(O/'verification.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record['after']));print(trealla_counts)
