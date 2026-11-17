from pathlib import Path
import subprocess,json,hashlib,urllib.request
O=Path(__file__).resolve().parent
names=['deployment-wp_n1-1','deployment-wp_n2-1','deployment-wp_n3-1','deployment-wp_n4-1','deployment-wp_admin-1','deployment-wp_n5-1','web-prolog-hub-n0-1','trinity-n6-host-wp_n6-1','trinity-n6-local-wp_n6-1','trinity-n6-host-n6_assets-1','trinity-n6-local-n6_assets-1','trinity-n6-local-n6_hub-1']
rows=[]
for name in names:
 d=json.loads(subprocess.check_output(['docker','inspect',name],text=True))[0];labels=d['Config']['Labels'] or {}
 row=dict(name=name,image_id=d['Image'],configured_image=d['Config']['Image'],revision=labels.get('org.opencontainers.image.revision'),environment_sha256=hashlib.sha256(json.dumps(sorted(d['Config']['Env'])).encode()).hexdigest(),user=d['Config']['User'],entrypoint=d['Config']['Entrypoint'],command=d['Config']['Cmd'],controls={k:d['HostConfig'].get(k) for k in ['Memory','NanoCpus','PidsLimit','ReadonlyRootfs','CapAdd','CapDrop','SecurityOpt']},mounts=[{k:m.get(k) for k in ['Type','Name','Destination','RW']} for m in d['Mounts']])
 if name=='deployment-wp_n5-1':
  tag='successor-release-rollback:20261105-n5';subprocess.run(['docker','tag',d['Image'],tag],check=True);row['rollback_tag']=tag;row['compose_files']=labels['com.docker.compose.project.config_files']
 rows.append(row)
(O/'before-services.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Snapshot saved for twelve services; N5 rollback image retained.')
