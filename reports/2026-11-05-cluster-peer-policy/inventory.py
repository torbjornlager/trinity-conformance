from pathlib import Path
import subprocess,json,urllib.request,urllib.error,hashlib
O=Path(__file__).resolve().parent
names=['deployment-wp_n1-1','deployment-wp_n2-1','deployment-wp_n3-1','deployment-wp_n4-1','deployment-wp_admin-1','deployment-wp_n5-1','web-prolog-hub-n0-1','trinity-n6-host-wp_n6-1','trinity-n6-local-wp_n6-1','trinity-n6-host-n6_assets-1','trinity-n6-local-n6_assets-1','trinity-n6-local-n6_hub-1']
rows=[]
for i,name in enumerate(names):
 d=json.loads(subprocess.check_output(['docker','inspect',name],text=True))[0]
 tag=f'cluster-policy-release-rollback-20261105-cluster:service-{i}'
 subprocess.run(['docker','tag',d['Image'],tag],check=True)
 labels=d['Config']['Labels'] or {}
 rows.append(dict(name=name,image_id=d['Image'],rollback_tag=tag,configured_image=d['Config']['Image'],project=labels.get('com.docker.compose.project'),service=labels.get('com.docker.compose.service'),compose_files=labels.get('com.docker.compose.project.config_files'),volumes=[{'name':m.get('Name'),'destination':m['Destination']} for m in d['Mounts']],health=d['State'].get('Health',{}).get('Status'),environment_sha256=hashlib.sha256(json.dumps(sorted(d['Config']['Env'])).encode()).hexdigest(),user=d['Config']['User'],controls={k:d['HostConfig'].get(k) for k in ['Memory','NanoCpus','PidsLimit','ReadonlyRootfs','CapAdd','CapDrop','SecurityOpt']}))
(O/'rollback-images.json').write_text(json.dumps(rows,indent=2)+'\n')
responses=[]
for n in range(7):
 url=f'https://n{n}.elfenbenstornet.se/node_info'
 try:
  with urllib.request.urlopen(url,timeout=15) as response:
   body=json.load(response);row=dict(node=n,status=response.status,profile=body.get('profile'),auth=body.get('auth'))
 except Exception as e:row=dict(node=n,error=str(e))
 responses.append(row);print(row,flush=True)
(O/'public-before.json').write_text(json.dumps(responses,indent=2)+'\n')
