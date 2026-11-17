from pathlib import Path
import subprocess,tempfile,json,shutil
R=Path('/Users/lager/trinity-demonstrator');ctx=Path('/tmp/localhost-n6-build-context-v2');ctx.mkdir(exist_ok=False)
subprocess.run(['tar','-xf','-','-C',str(ctx)],input=subprocess.check_output(['git','archive','HEAD'],cwd=R),check=True)
for name in ['Deployment/n6_egress.py','Deployment/n6_contained.py']:
 shutil.copyfile(R/name,ctx/name)
p=ctx/'Deployment/Dockerfile.gprolog';s=p.read_text();needle='RUN cd /src/gprolog/src && ./configure';s=s.replace(needle,'COPY --from=gnu_fix isobase/rpc.pl isobase/transport.c isobase/http.c /src/gprolog-port/isobase/\n'+needle,1);p.write_text(s)
with tempfile.TemporaryDirectory(prefix='localhost-build-secret-') as d:
 secret=Path(d)/'read-token';secret.write_bytes(subprocess.check_output(['gh','auth','token'],stderr=subprocess.DEVNULL));secret.chmod(0o600)
 plans=[('runtime','Deployment/Dockerfile.gprolog','trinity-localhost-gnu-dev2:20261105',['--build-context','gnu_fix=/Users/lager/gprolog-port']),('node','Deployment/Dockerfile.n6','trinity-localhost-n6-dev2:20261105',['--build-context','gprolog_runtime=docker-image://trinity-localhost-gnu-dev2:20261105'])]
 for name,file,image,extra in plans:
  print('Building',name,flush=True)
  with open('/tmp/localhost-build-'+name+'.txt','w') as log:
   p=subprocess.run(['docker','build','--secret','id=github_token,src='+str(secret),'-f',file,'-t',image,*extra,'.'],cwd=ctx,stdout=log,stderr=subprocess.STDOUT)
  if p.returncode:raise SystemExit(p.returncode)
  print('Built',image,flush=True)
