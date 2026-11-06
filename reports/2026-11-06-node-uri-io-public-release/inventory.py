from pathlib import Path
import subprocess,json,hashlib,urllib.request
O=Path(__file__).resolve().parent
names=['deployment-wp_n1-1','deployment-wp_n2-1','deployment-wp_n3-1','deployment-wp_n4-1','deployment-wp_admin-1','deployment-wp_n5-1','web-prolog-hub-n0-1','trinity-n6-host-wp_n6-1','trinity-n6-local-wp_n6-1','trinity-n6-host-n6_assets-1','trinity-n6-local-n6_assets-1','trinity-n6-local-n6_hub-1','deployment-caddy-1','trinity-n6-host-n6_admission-1','deployment-n5_admission-1','deployment-oauth2_n5-1']
def invariant(d):
 return dict(environment_sha256=hashlib.sha256(json.dumps(sorted(d['Config']['Env'])).encode()).hexdigest(),user=d['Config']['User'],entrypoint=d['Config']['Entrypoint'],command=d['Config']['Cmd'],controls={k:d['HostConfig'].get(k) for k in ['Memory','NanoCpus','PidsLimit','ReadonlyRootfs','CapAdd','CapDrop','SecurityOpt','PortBindings','Tmpfs','Init']},mounts=sorted([{k:m.get(k) for k in ['Name','Type','Source','Destination','RW','Propagation']} for m in d['Mounts']],key=lambda m:m['Destination']))
if __name__=='__main__':
 rows=[]
 for i,name in enumerate(names):
  d=json.loads(subprocess.check_output(['docker','inspect',name],text=True))[0];tag='node-uri-io-rollback-20261106:service-'+str(i)
  subprocess.run(['docker','tag',d['Image'],tag],check=True)
  labels=d['Config']['Labels'] or {}
  rows.append(dict(name=name,image_id=d['Image'],rollback_tag=tag,configured_image=d['Config']['Image'],project=labels.get('com.docker.compose.project'),service=labels.get('com.docker.compose.service'),compose_files=labels.get('com.docker.compose.project.config_files'),running=d['State']['Running'],health=d['State'].get('Health',{}).get('Status'),invariant=invariant(d)))
 (O/'rollback-inventory.json').write_text(json.dumps(rows,indent=2)+'\n')
 observations=[]
 for n in range(7):
  with urllib.request.urlopen(f'https://n{n}.elfenbenstornet.se/node_info',timeout=10) as r:info=json.load(r)
  observations.append(dict(node=n,profile=info.get('profile'),status=200))
 (O/'public-before.json').write_text(json.dumps(observations,indent=2)+'\n')
 print('Recorded rollback images and configuration fingerprints for',len(rows),'services; all seven public hosts respond.')
