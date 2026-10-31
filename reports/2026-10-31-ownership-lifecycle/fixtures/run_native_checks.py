import subprocess,os,json,time
from pathlib import Path
root=Path('/work');out=Path('/results/native-initial');out.mkdir(exist_ok=True)
rows=[]
checks=[('trealla-authority',root/'trealla',['/opt/trealla/tpl','-g',"(catch((consult('actor_authority_tests.pl'),actor_authority_tests:actor_authority_tests),E,(writeq(E),nl,fail))->halt;halt(1))"]),('trealla-unit',root/'trealla',['./tools/test.sh','unit']),('swi-native',root/'swi',['./tools/test.sh','LINT','T0','T2','T4_NATIVE'])]
for name,cwd,cmd in checks:
 start=time.monotonic()
 with (out/(name+'.log')).open('w') as log:
  try:
   r=subprocess.run(cmd,cwd=cwd,env=dict(os.environ,SWIPL='/usr/bin/swipl',TPL='/opt/trealla/tpl',TPL_LIBRARY_PATH='/opt/trealla/library',TEST_TIMEOUT='30'),stdout=log,stderr=subprocess.STDOUT,timeout=240);code=r.returncode
  except subprocess.TimeoutExpired:code='timeout'
 rows.append(dict(name=name,command=cmd,returncode=code,seconds=round(time.monotonic()-start,3)))
 (out/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
 print(name,code,flush=True)
 if code!=0:print((out/(name+'.log')).read_text()[-4500:],flush=True)
