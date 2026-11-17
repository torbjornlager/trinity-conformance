from pathlib import Path
import subprocess,json,re,hashlib
O=Path(__file__).resolve().parent;before=json.loads((O/'public-spawn-policy-reference.json').read_text())['graph'];graph={};observations=[]
for n in [3,4]:
 path=f'/app/Deployment/start_n{n}.pl';source=subprocess.check_output(['docker','exec',f'deployment-wp_n{n}-1','cat',path],text=True)
 match=re.search(r'load_uri_allowed_origins\(\[(.*?)\]\)',source,re.S);assert match
 origins=re.findall(r"'(https?://[^']+)'",match[1]);graph[f'https://n{n}.elfenbenstornet.se']=origins;observations.append(dict(node=n,source=path,sha256=hashlib.sha256(source.encode()).hexdigest(),allowed=origins))
d=json.loads(subprocess.check_output(['docker','inspect','deployment-wp_n5-1'],text=True))[0];env=dict(x.split('=',1) for x in d['Config']['Env'] if '=' in x)
graph['https://n5.elfenbenstornet.se']=env['WP_LOAD_URI_ORIGINS'].split(',');observations.append(dict(node=5,source='WP_LOAD_URI_ORIGINS',allowed=graph['https://n5.elfenbenstornet.se']))
for origin,targets in graph.items():
 assert set(targets)==set(before[origin]),origin
 assert all(peer in targets for peer in graph),origin
 assert 'https://external.invalid' not in targets
(O/'public-spawn-policy.json').write_text(json.dumps(dict(graph=graph,observations=observations,additions={},policy_changed=False),indent=2)+'\n')
print('PASS N3-N5 source/spawn policy unchanged; peer and return routes remain enabled')
