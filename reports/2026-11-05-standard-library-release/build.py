from pathlib import Path
import subprocess,tempfile,json,time,tarfile,io
R=Path('/Users/lager/trinity-demonstrator');O=Path(__file__).resolve().parent
rev=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
context=Path('/tmp/standard-library-consumer-release-20261105-nested');context.mkdir(exist_ok=True);assert not any(context.iterdir())
data=subprocess.check_output(['git','archive',rev],cwd=R)
subprocess.run(['tar','-xf','-','-C',str(context)],input=data,check=True)
(O/'consumer-revision.txt').write_text(rev+'\n')
plans=[('native','Deployment/Dockerfile','trinity-standard-library-native:20261105-nested',[]),('hub','Deployment/Dockerfile.node','trinity-standard-library-hub:20261105-nested',[]),('trealla-runtime','Deployment/Dockerfile.trealla','trinity-standard-library-trealla-runtime:20261105-nested',[]),('trealla-node','Deployment/Dockerfile.n5-linda','trinity-standard-library-n5:20261105-nested',['--build-context','trealla_runtime=docker-image://trinity-standard-library-trealla-runtime:20261105-nested']),('gnu-runtime','Deployment/Dockerfile.gprolog','trinity-standard-library-gnu-runtime:20261105-nested',[]),('gnu-node','Deployment/Dockerfile.n6','trinity-standard-library-n6:20261105-nested',['--build-context','gprolog_runtime=docker-image://trinity-standard-library-gnu-runtime:20261105-nested'])]
rows=[]
with tempfile.TemporaryDirectory(prefix='appendix-build-secret-') as d:
 p=Path(d)/'read-token';p.write_bytes(subprocess.check_output(['gh','auth','token'],stderr=subprocess.DEVNULL));p.chmod(0o600)
 for label,file,tag,extra in plans:
  print('START',label,flush=True);started=time.monotonic()
  cmd=['docker','build','--secret','id=github_token,src='+str(p),'--label','org.opencontainers.image.revision='+rev,'-f',file,'-t',tag,*extra,'.']
  with (O/('build-'+label+'.log')).open('w') as log:code=subprocess.run(cmd,cwd=context,stdout=log,stderr=subprocess.STDOUT).returncode
  row=dict(component=label,image=tag,exit_code=code,seconds=round(time.monotonic()-started,2),consumer_revision=rev)
  if not code:row['image_id']=subprocess.check_output(['docker','image','inspect',tag,'--format','{{.Id}}'],text=True).strip()
  rows.append(row);(O/'build-results.json').write_text(json.dumps(rows,indent=2)+'\n');print('DONE',label,code,flush=True)
  if code:raise SystemExit(code)
