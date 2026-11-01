from pathlib import Path
import subprocess,os,json
rows=[]
for label,goal in [('sandbox-denials','t47,t48,t49,t50,t51,t52,t53,t54,t56'),('private-source-and-copy','t102,t103,t104,t105,t109'),('nested-copy-sandbox-controls','t119,t120,t144,t145,t146,t147,t148,t149,t150,t151,t153')]:
 with (Path('/work')/(label+'.log')).open('w') as f:
  try:r=subprocess.run(['/opt/trealla/tpl','-g',f"(catch((consult('tests.pl'),{goal}),E,(writeq(E),nl,fail))->halt;halt(1))"],cwd='/work/sources/trealla',env=dict(os.environ,TPL_LIBRARY_PATH='/opt/trealla/library'),stdout=f,stderr=subprocess.STDOUT,timeout=45);code=r.returncode
  except subprocess.TimeoutExpired:code='timeout'
 rows.append(dict(label=label,returncode=code));print(label,code,flush=True)
 Path('/work/security-checks.json').write_text(json.dumps(rows,indent=2)+'\n')
