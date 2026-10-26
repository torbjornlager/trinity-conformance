#!/usr/bin/env python3
"""Audit saved checkpoint evidence; does not contact or start a node."""
import gzip,hashlib,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
load=lambda p:json.loads((HERE/p).read_text())
raw=json.loads(gzip.decompress((HERE/'browser-evidence.json.gz').read_bytes()))
compact=load('browser-results.json')
assert len(raw)==len(compact)==70
for mode in ['worker','main']:
 rows=[r for r in raw if r['mode']==mode];assert len(rows)==35
 observed=set()
 for r in rows:
  assert ('ACTOR (DOM)' if mode=='main' else 'ACTOR (WORKERS)') in r['state']
  for state in [r['state'],r.get('completion_state','')]:
   normalized=state.replace('\u00a0',' ')
   terminal=normalized[normalized.find('text Terminal'):normalized.find('text Logger')]
   observed.update(re.findall(r'text Checkpoint = ([a-z0-9]+)(?=[.,\n])',terminal))
 for r in rows:assert r['passed']==(r['id'].lower().replace('-','') in observed),r['id']
 assert {r['id'] for r in rows if not r['passed']}=={'TXT-018','TXT-023','TXT-024'}
 assert len({r['id'] for r in rows})==35
for r,c in zip(raw,compact):
 assert c['state_sha256']==hashlib.sha256(r['state'].encode()).hexdigest()
 assert all(c[k]==r[k] for k in ['mode','id','passed'])
for filename,expected in [('native/swi-portable-text.json',{'pass':26,'fail':0,'unsupported':0}),('native/trealla-portable-text.json',{'pass':22,'fail':4,'unsupported':0}),('trealla-literal-utf8-control.json',{'pass':26,'fail':0,'unsupported':0})]:assert load(filename)['counts']==expected
controls=load('native-controls.json');assert len(controls)==24
for r in controls:
 expected=not (r['candidate']=='swi' and r['id']=='CONTROL-ROUNDTRIP' or r['candidate']=='trealla' and r.get('encoding')=='escaped_surrogates')
 assert r['passed']==expected,r
 if r['id']=='OUT-001':assert r['outputs']==['[a,b,c]']
for filename in ['preservation.json','final-source-preservation.json','native/preservation.json']:assert all(load(filename)['checks'].values())
assert load('browser-provenance.json')['ui_fixture_stopped']
for name in ['worker','main']:
 text=(HERE/(name+'-output.ax.txt')).read_text().replace('\u00a0',' ')
 terminal=text[text.index('text Terminal'):text.index('text Logger')]
 assert re.search(r'text \[a,b,c\]\n',terminal)
 assert terminal.rfind('text [a,b,c]')<terminal.rfind('text true.')
print('Evidence verified: native 26/26 and 22/26; UTF-8 control 26/26; each browser 32 pass + 3 diagnostics; preservation checks pass.')
