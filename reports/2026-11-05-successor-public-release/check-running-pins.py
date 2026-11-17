from pathlib import Path
import json,subprocess
O=Path(__file__).resolve().parent;R=Path('/Users/lager/trinity-demonstrator')
expected={n:json.loads((R/'dependencies'/f'{n}.json').read_text()) for n in ['swi-prolog-node','swi-wasm-node','trealla-port','gprolog-port']}
rows=[]
for service in json.loads((O/'rollout-results.json').read_text())['services']:
 name=service['name'];pins={}
 names=['trealla-port'] if name=='deployment-wp_n5-1' else ['gprolog-port'] if name.endswith('-wp_n6-1') else ['swi-prolog-node','swi-wasm-node']
 for kind in names:
  file='/usr/share/doc/trealla/runtime-pins.json' if kind=='trealla-port' else '/usr/share/doc/gprolog/runtime-pins.json' if kind=='gprolog-port' else f'/app/dependencies/{kind}.json'
  pin=json.loads(subprocess.check_output(['docker','exec',name,'cat',file],text=True));assert pin==expected[kind],(name,kind)
  pins[kind]=pin['revision']
 rows.append(dict(container=name,pins=pins))
(O/'running-runtime-pins.json').write_text(json.dumps(rows,indent=2)+'\n')
print('PASS exact runtime pins in all',len(rows),'running services')
