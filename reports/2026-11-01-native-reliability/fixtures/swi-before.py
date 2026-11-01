import subprocess,pathlib,json
for i in range(10):
 p=subprocess.run(['/usr/bin/swipl','-q','-g',"load_files('tests/tiers/node/supervisor_restart_ownership_tests.pl'),(run_tests([supervisor_restart,supervisor_intensity,supervisor_restart_ownership])->halt;halt(1))"],cwd='/work/swi-base',capture_output=True,text=True,timeout=30)
 pathlib.Path(f'/work/swi-before-{i}.json').write_text(json.dumps({'status':p.returncode,'output':p.stdout+p.stderr},indent=2));print(i,p.returncode,flush=True)
