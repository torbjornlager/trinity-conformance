import subprocess,os,json,time
from pathlib import Path
r=Path('/work'); rows=[]
env=dict(os.environ,TPL_LIBRARY_PATH='/opt/trealla/library')
checks=[('release',['python3','/work/conformance/adapters/local_actor_release.py','--sources','/work/sources','--output','/work/release-final-stable'],r),('old-source-regressions',['python3','/work/run_checks.py','--sources','/work/original-sources','--output','/work/before-final-stable','--engine','trealla'],r)]
for g in ['isolation','sandbox','source_policy','actors','auth','lifecycle']:
 checks.append(('native-'+g,['/opt/trealla/tpl','-g',f"(catch((consult('tests.pl'),run_test_group({g})),E,(writeq(E),nl,fail))->halt;halt(1))"],r/'sources/trealla'))
for name,cmd,cwd in checks:
 before=time.monotonic()
 with (r/(name+'-final.log')).open('w') as log:
  try:p=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=240 if name=='release' else 45);code=p.returncode
  except subprocess.TimeoutExpired:code='timeout'
 rows.append(dict(name=name,returncode=code,seconds=round(time.monotonic()-before,3)));print(name,code,flush=True)
 (r/'final-checks.json').write_text(json.dumps(rows,indent=2)+'\n')
