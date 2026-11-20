from pathlib import Path
import json,subprocess,hashlib,tarfile,shutil,datetime
R=Path('/Users/lager/trinity-conformance');P=Path(__file__).resolve().parent;old=P.parent/'conformance-upgraded-live-20261119';assert not (P/'suite-snapshot').exists()
for name in ['suite-snapshot','orchestration','logs','observations','metadata','live-more','live-library','live-controls','smoke','public-extra','build']:(P/name).mkdir()
revision=subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD'],text=True).strip();paths=['cases','profiles','fixtures','runner','adapters','schemas','docs','requirements','README.md']
subprocess.run(['git','-C',str(R),'archive','--output',str(P/'suite.tar'),revision,*paths],check=True)
with tarfile.open(P/'suite.tar') as archive:archive.extractall(P/'suite-snapshot')
files={str(f.relative_to(P/'suite-snapshot')):hashlib.sha256(f.read_bytes()).hexdigest() for folder in paths if (P/'suite-snapshot'/folder).is_dir() for f in (P/'suite-snapshot'/folder).rglob('*') if f.is_file()}
manifests=list((P/'suite-snapshot/cases').glob('*.json'));inputs=dict(revision=revision,files=files,manifest_count=len(manifests),main_case_rows=sum(len(json.loads(f.read_text())['cases']) for f in manifests));(P/'inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
for f in (old/'orchestration').glob('*.py'):
 s=f.read_text().replace(str(old),str(P)).replace('2026-11-19-upgraded-live-conformance','2026-11-20-live-conformance');(P/'orchestration'/f.name).write_text(s)
allbefore=json.loads(subprocess.check_output(['docker','ps','-aq']).decode() and subprocess.check_output(['docker','inspect',*subprocess.check_output(['docker','ps','-aq'],text=True).split()]))
(P/'preservation-before.json').write_text(json.dumps([dict(name=d['Name'],id=d['Id'],image=d['Image']) for d in allbefore if d['State']['Running'] and (d['Config'].get('Labels') or {}).get('com.docker.compose.service')],indent=2)+'\n')
selected=json.loads((P.parent/'admission-120-20261119/release-r5/selected.json').read_text());(P/'release.json').write_text(json.dumps(selected,indent=2)+'\n')
for t in selected['targets']:
 d=next(x for x in allbefore if x['Name']=='/'+t['container']);assert d['Id']==t['id'] and d['Image']==t['candidate_image']
f=P/'orchestration/public.py';s=f.read_text().replace("5.0 if node=='n7' else 2.1","2.1");f.write_text(s)
f=P/'orchestration/live_more.py';s=f.read_text().replace("interval=1.3 if node in ['n1','n6'] else .7","interval=.8").replace("pages.toplevel_case(c,ws.removesuffix('/ws'))","pages.toplevel_case(c,ws.removesuffix('/ws'))");f.write_text(s)
f=P/'orchestration/live_library.py';s=f.read_text();start=s.index('# One job per live node');end=s.index('last_http=0');s=s[:start]+"time.sleep(61)\nhttp_interval=.8\n"+s[end:];s=s.replace("  row=dict(candidate=node+'-http',id=c['id'],title=c['title'])","  if node=='n6' and c.get('bounded_prefix'):\n   print('N6 quiet period before bounded generator:303 seconds',flush=True);time.sleep(303)\n  row=dict(candidate=node+'-http',id=c['id'],title=c['title'])");f.write_text(s)
f=P/'orchestration/public-extra.py';s=f.read_text().replace("if node=='n7':time.sleep(15)","time.sleep(2.1)").replace("15 if node=='n7' else 2.1","2.1").replace("15 if source=='n7' else 2.1","2.1");s=s.replace("F=O/'public-extra';F.mkdir(exist_ok=True);rows=[]","F=O/'public-extra';F.mkdir(exist_ok=True);rows=[]\nwhile not all((O/'logs'/('endpoint-'+n+'.done')).exists() for n in ['n0','n1','n2','n3','n4','n5','n6','n7']):time.sleep(2)");f.write_text(s)
# Unredacted original fixture operator stays private; export redaction happens later.
s=(old/'orchestration/isolated.py').read_text().replace(str(old),str(P));start=s.index("images={");end=s.index('\ndef docker',start);images={k:next(t['candidate_image'] for t in selected['targets'] if t['service']==v) for k,v in [('swi-n134','wp_n3'),('swi-n2','wp_n2'),('trealla-n5','wp_n5')]};s=s[:start]+'images='+repr(images)+s[end:];(P/'orchestration/isolated.py').write_text(s)
state=dict(task='Fresh complete conformance sweep after configurable admission rollout',started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),suite_revision=revision,manifests=inputs['manifest_count'],main_rows=inputs['main_case_rows'],root=str(P),report=str(R/'reports/2026-11-20-live-conformance'),status='running',policy='One sequential controller per public endpoint; .8s HTTP pacing,2.1s session spacing,4s prompt creation pacing,303s N6 quiet periods before bounded producers; no live configuration changes; all old reports immutable')
(P/'STATE.json').write_text(json.dumps(state,indent=2)+'\n');print(json.dumps(state))
