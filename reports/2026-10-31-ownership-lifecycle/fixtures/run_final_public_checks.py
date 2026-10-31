from pathlib import Path
import subprocess,json,sys,shutil
root=Path('/work');out=Path('/results');rows=[]
for name,driver,repetitions,extra in [('repair-confirmed','paper/experiments/run_boundary_experiments.py',3,[]),('lifecycle-confirmed','run_lifecycle_repair_checks.py',3,[]),('cli-confirmed','run_lifecycle_cli_checks.py',1,['--only','CLI'])]:
 command=[sys.executable,str(root/driver),'--output',str(out/name),'--repetitions',str(repetitions),*extra]
 result=subprocess.run(command)
 shutil.copy2(root/driver,out/name/'harness.py')
 rows.append(dict(name=name,returncode=result.returncode,command=command))
(out/'final-public-checks.json').write_text(json.dumps(rows,indent=2)+'\n')
sys.exit(any(row['returncode']!=0 for row in rows))
