from pathlib import Path
import subprocess,tempfile,json,time
R=Path('/Users/lager/trinity-demonstrator');O=Path(__file__).resolve().parent
rev=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
assert not subprocess.check_output(['git','status','--porcelain'],cwd=R,text=True).strip()
context=O/'build-context';context.mkdir()
subprocess.run(['tar','-xf','-','-C',str(context)],input=subprocess.check_output(['git','archive',rev],cwd=R),check=True)
(O/'consumer-revision.txt').write_text(rev+'\n')
plans=[
 ('native','Deployment/Dockerfile',[]),
 ('hub','Deployment/Dockerfile.node',[]),
 ('trealla-runtime','Deployment/Dockerfile.trealla',[]),
 ('n5','Deployment/Dockerfile.n5-linda',['--build-context','trealla_runtime=docker-image://trinity-node-uri-io-trealla-runtime:20261106']),
]
rows=[]
with tempfile.TemporaryDirectory(prefix='node-uri-io-build-secret-') as d:
 token=Path(d)/'read-token';token.write_bytes(subprocess.check_output(['gh','auth','token'],stderr=subprocess.DEVNULL));token.chmod(0o600)
 for label,file,extra in plans:
  tag='trinity-node-uri-io-'+label+':20261106'
  print('START',label,flush=True);start=time.monotonic()
  cmd=['docker','build','--secret','id=github_token,src='+str(token),'--label','org.opencontainers.image.revision='+rev,'-f',file,'-t',tag]+extra+['.']
  with (O/('build-'+label+'.log')).open('w') as log:code=subprocess.run(cmd,cwd=context,stdout=log,stderr=subprocess.STDOUT).returncode
  row=dict(component=label,image=tag,exit_code=code,consumer_revision=rev,seconds=round(time.monotonic()-start,2))
  if not code:row['image_id']=subprocess.check_output(['docker','image','inspect',tag,'--format','{{.Id}}'],text=True).strip()
  rows.append(row);(O/'build-results.json').write_text(json.dumps(rows,indent=2)+'\n');print('DONE',label,code,flush=True)
  if code:raise SystemExit(code)
