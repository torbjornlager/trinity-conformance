from pathlib import Path
import subprocess,json
P=Path(__file__).resolve().parent;T=json.loads((P/'release.json').read_text())['targets']
for kind,service in [('swi','wp_n3'),('trealla','wp_n5'),('gnu','wp_n6')]:subprocess.run(['docker','tag',next(t['candidate_image'] for t in T if t['service']==service),'local/conformance-post-uri-input-'+kind+':20261120'],check=True)
text='''FROM local/conformance-post-uri-input-trealla:20261120 AS trealla
FROM local/conformance-post-uri-input-gnu:20261120 AS gnu
FROM local/conformance-post-uri-input-swi:20261120
USER root
COPY --from=trealla /opt/trealla/ /opt/trealla/
COPY --from=trealla /app/*.pl /work/trealla/
COPY --from=gnu /app/isobase/ /work/gnu/isobase/
RUN apt-get update && apt-get install -y --no-upgrade --no-install-recommends procps && rm -rf /var/lib/apt/lists/*
RUN git config --global user.name 'Conformance fixture snapshot' && git config --global user.email 'fixture@localhost' \\
 && cd /work/trealla && git init -q && git add . && git commit -q -m 'Exact deployed N5 runtime snapshot' \\
 && cd /work/gnu && git init -q && git add . && git commit -q -m 'Exact deployed N6 ISOBASE snapshot'
ENV TPL_LIBRARY_PATH=/opt/trealla/library
ENTRYPOINT []
'''
(P/'build/Dockerfile').write_text(text)
with (P/'logs/build-lab.log').open('w') as log:subprocess.run(['docker','build','-t','local/conformance-live-lab:20261120-post-uri',str(P/'build')],stdout=log,stderr=subprocess.STDOUT,check=True)
print('Owned current-image lab built with test-only procps; engine files unchanged',flush=True)
name='conformance-post-uri-lab-20261120';subprocess.run(['docker','create','--name',name,'--network','none','--memory','2g','--cpus','2','--pids-limit','512','--no-healthcheck','--entrypoint','sh','local/conformance-live-lab:20261120-post-uri','-c','exec sleep infinity'],check=True,stdout=subprocess.DEVNULL);subprocess.run(['docker','start',name],check=True,stdout=subprocess.DEVNULL)
subprocess.run(['docker','exec',name,'mkdir','-p',str(P/'suite-snapshot'),str(P/'orchestration'),str(P/'logs')],check=True)
for folder in ['suite-snapshot','orchestration']:subprocess.run(['docker','cp',str(P/folder)+ '/.',name+':'+str(P/folder)],check=True)
subprocess.run(['docker','cp',str(P/'inputs.json'),name+':'+str(P/'inputs.json')],check=True)
provenance={key:subprocess.check_output(['docker','exec',name,'git','-C',path,'rev-parse','HEAD'],text=True).strip() for key,path in [('native','/opt/swi-prolog-node'),('trealla_snapshot','/work/trealla'),('gnu_snapshot','/work/gnu')]};provenance.update(lab_image=subprocess.check_output(['docker','image','inspect','local/conformance-live-lab:20261120-post-uri','--format','{{.Id}}'],text=True).strip(),suite_revision=json.loads((P/'inputs.json').read_text())['revision'],deployed_release=json.loads((P/'release.json').read_text())['revisions'],synthetic_revision_note='Trealla/GNU lab Git revisions identify snapshots of deployed-image files, not upstream commits.')
(P/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
for script in ['native.py','followup-native.py','extras.py']:
 print('START owned',script,flush=True)
 with (P/'logs'/('owned-'+script+'.log')).open('w') as log:r=subprocess.run(['docker','exec',name,'python3',str(P/'orchestration'/script)],stdout=log,stderr=subprocess.STDOUT)
 print('DONE owned',script,r.returncode,flush=True)
 # Export fresh results incrementally, never old observations.
 for folder in ['native','followup-native','extras','logs']:
  subprocess.run(['docker','cp',name+':'+str(P/folder),str(P)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 for output in ['native-plan.json','native-jobs.json','followup-native-jobs.json']:subprocess.run(['docker','cp',name+':'+str(P/output),str(P/output)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
(P/'owned-native.complete').write_text('complete\n')
print('Owned native matrix finished; lab retained temporarily for supplemental controls',flush=True)
