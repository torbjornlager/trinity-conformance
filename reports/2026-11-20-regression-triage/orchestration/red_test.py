from pathlib import Path
import subprocess,json
P=Path(__file__).resolve().parent;R=Path('/Users/lager/swi-prolog-node');versions=json.loads((P/'swi/versions.json').read_text());rows=[]
for label,data in versions.items():
 name='conformance-red-'+label+'-20261120'
 try:
  subprocess.run(['docker','create','--name',name,'--user','root','--network','none','--memory','512m','--cpus','1','--pids-limit','128','--no-healthcheck','--entrypoint','sh',data['image'],'-c','exec sleep infinity'],stdout=subprocess.DEVNULL,check=True);subprocess.run(['docker','start',name],stdout=subprocess.DEVNULL,check=True);subprocess.run(['docker','cp',str(R/'tests/tiers/retirement_order_tests.pl'),name+':/opt/swi-prolog-node/tests/tiers/retirement_order_tests.pl'],check=True)
  result=subprocess.run(['docker','exec',name,'swipl','-f','none','-q','-s','/opt/swi-prolog-node/tests/tiers/retirement_order_tests.pl','-g','run_tests(retirement_order)','-t','halt'],capture_output=True,text=True,timeout=15);assert result.returncode!=0 and 'memberchk' in result.stderr
  rows.append(dict(label=label,status='expected_regression_test_failure',exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr));print(label,'expectedred',result.returncode)
 finally:subprocess.run(['docker','rm','-f',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
(P/'swi/deterministic-red.json').write_text(json.dumps(dict(scope='New regression test copied onto unchanged old/current runtime images; both must fail before the fix',results=rows),indent=2)+'\n')
