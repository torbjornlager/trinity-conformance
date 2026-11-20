from pathlib import Path
import subprocess,json,hashlib
P=Path(__file__).resolve().parent;B=P/'build/browser';B.mkdir(exist_ok=True);(P/'browser-compat').mkdir(exist_ok=True)
(B/'Dockerfile').write_text('FROM local/conformance-browser-lab:20261119\nUSER root\nCOPY tools/node_modules /opt/conformance-tools/node_modules\nENV NODE_PATH=/opt/conformance-tools/node_modules\n')
with (P/'logs/browser-build.log').open('w') as log:subprocess.run(['docker','build','-t','local/conformance-browser-lab:20261120-post-uri',str(B)],stdout=log,stderr=subprocess.STDOUT,check=True)
name='conformance-post-uri-browser-20261120';subprocess.run(['docker','create','--name',name,'--network','none','--memory','2g','--cpus','2','--pids-limit','512','--no-healthcheck','--entrypoint','sh','local/conformance-browser-lab:20261120-post-uri','-c','exec sleep infinity'],check=True,stdout=subprocess.DEVNULL);subprocess.run(['docker','start',name],check=True,stdout=subprocess.DEVNULL)
try:
 subprocess.run(['docker','exec',name,'mkdir','-p','/work/current-browser','/work/current-suite','/work/results'],check=True)
 package=Path('/Users/lager/trinity-demonstrator/.trinity/browser-runtime/b5ec41d3f68c49a1a6fac03f82f4481e88035cff')
 for source,dest in [(package,'/work/current-browser'),(P/'suite-snapshot','/work/current-suite')]:subprocess.run(['docker','cp',str(source)+'/.',name+':'+dest],check=True)
 # Test-only module loading; runtime and manifest bytes remain unchanged.
 with (P/'logs/browser-compat.log').open('w') as log:r=subprocess.run(['docker','exec','-e','NODE_PATH=/opt/conformance-tools/node_modules','-e','CHROME_PATH=/usr/bin/chromium','-e','LIBRARY_RUNTIME_ROOT=/work/current-browser','-e','LIBRARY_MANIFEST=/work/current-suite/cases/browser-local-compatibility-0.1.json','-e','LIBRARY_REPORT=/work/results/browser-local-compatibility-0.1.json',name,'node','/work/current-suite/adapters/wasm_actor_cases.cjs'],stdout=log,stderr=subprocess.STDOUT)
 subprocess.run(['docker','cp',name+':/work/results/.',str(P/'browser-compat')],check=True)
 manifest=json.loads((package/'manifest.json').read_text());version=subprocess.check_output(['docker','exec',name,'chromium','--version'],text=True).strip();(P/'browser-provenance.json').write_text(json.dumps(dict(browser=version,playwright='1.62.1',package_source=manifest.get('source'),engine=manifest.get('engine'),package_manifest_sha256=hashlib.sha256((package/'manifest.json').read_bytes()).hexdigest(),exit_code=r.returncode,scope='Fresh real Chromium Worker/main browser-local-compatibility selection on current deployed package; not public UI certification',container_removed=True),indent=2)+'\n');print('Fresh browser compatibility complete, exit',r.returncode)
finally:subprocess.run(['docker','rm','-f',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
