from pathlib import Path
import json,subprocess,hashlib
P=Path(__file__).resolve().parent;R=Path('/Users/lager/swi-prolog-node');B=P/'fixed-build';B.mkdir();base=json.loads((P/'swi/versions.json').read_text())['current']['image'];tag='local/conformance-retirement-fixed:20261120'
subprocess.run(['docker','tag',base,'local/conformance-retirement-base:20261120'],check=True)
for src,dest in [(R/'prolog/web_prolog/actors.pl','actors.pl'),(R/'tests/tiers/retirement_order_tests.pl','retirement_order_tests.pl')]:__import__('shutil').copyfile(src,B/dest)
(B/'Dockerfile').write_text('FROM local/conformance-retirement-base:20261120\nUSER root\nCOPY actors.pl /opt/swi-prolog-node/prolog/web_prolog/actors.pl\nCOPY retirement_order_tests.pl /opt/swi-prolog-node/tests/tiers/retirement_order_tests.pl\n')
with (P/'logs/fixed-build.log').open('w') as log:subprocess.run(['docker','build','-t',tag,str(B)],stdout=log,stderr=subprocess.STDOUT,check=True)
name='conformance-delta-fixed-20261120';F=P/'swi/fixed';F.mkdir()
try:
 subprocess.run(['docker','create','--name',name,'--user','root','--network','none','--memory','1g','--cpus','2','--pids-limit','256','--no-healthcheck','--entrypoint','sh',tag,'-c','exec sleep infinity'],check=True,stdout=subprocess.DEVNULL);subprocess.run(['docker','start',name],check=True,stdout=subprocess.DEVNULL);subprocess.run(['docker','exec',name,'mkdir','-p','/work/suite'],check=True)
 for folder in ['runner','adapters','cases','fixtures','profiles']:subprocess.run(['docker','cp',str(Path('/Users/lager/trinity-conformance')/folder),name+':/work/suite/'],check=True)
 for source,dest in [(P/'nu_probe.py','/work/nu_probe.py'),(P/'retirement_probe.pl','/tmp/retirement_probe.pl')]:subprocess.run(['docker','cp',str(source),name+':'+dest],check=True)
 barrier=subprocess.run(['docker','exec',name,'swipl','-f','none','-q','-s','/tmp/retirement_probe.pl','-g','retirement_probe:main'],capture_output=True,text=True,check=True);assert 'monitor_delivery_actor_state(retired)' in barrier.stdout
 (F/'delivery-barrier.json').write_text(json.dumps(dict(stdout=barrier.stdout,status='pass'),indent=2)+'\n')
 with (P/'logs/fixed-regression.log').open('w') as log:subprocess.run(['docker','exec',name,'swipl','-f','none','-q','-s','/opt/swi-prolog-node/tests/tiers/retirement_order_tests.pl','-g','run_tests(retirement_order)','-t','halt'],stdout=log,stderr=subprocess.STDOUT,check=True)
 with (P/'logs/swi-fixed.log').open('w') as log:r=subprocess.run(['docker','exec',name,'python3','/work/nu_probe.py','fixed','1000'],stdout=log,stderr=subprocess.STDOUT)
 subprocess.run(['docker','cp',name+':/work/results/.',str(F)],check=True)
 engine=subprocess.check_output(['docker','exec',name,'sh','-c','find /usr/lib/swipl -type f -exec sha256sum {} + | sort | sha256sum'],text=True).strip();expected=json.loads((P/'swi/versions.json').read_text())['current']['identity'][2];assert engine==expected
 (F/'candidate.json').write_text(json.dumps(dict(base_revision='e25b2302017836ff89294999e8fb16f9667cfda6',actor_file_sha256=hashlib.sha256((R/'prolog/web_prolog/actors.pl').read_bytes()).hexdigest(),regression_test_sha256=hashlib.sha256((R/'tests/tiers/retirement_order_tests.pl').read_bytes()).hexdigest(),engine_inventory_unchanged=True,engine_inventory_sha256=engine.split()[0],exit_code=r.returncode),indent=2)+'\n');print('Fixed candidate1000trial replay complete',flush=True)
finally:subprocess.run(['docker','rm','-f',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
(P/'swi-fixed.complete').write_text('complete\n')
