import subprocess,pathlib,json
root=pathlib.Path('/work');rows=[]
for label,folder in [('before','trealla-base'),('after','final-sources/trealla')]:
 for module in ['actor_exit_wait_tests','node_shutdown_tests']:
  p=subprocess.run(['/opt/trealla/tpl','-g',f"(catch((consult('{module}.pl'),{module}:run),E,(writeq(E),nl,fail))->halt;halt(1))"],cwd=root/folder,capture_output=True,text=True,timeout=5)
  row=dict(source=label,case=module,status=p.returncode,output=p.stdout+p.stderr);rows.append(row);print(row,flush=True)
(root/'verified-controls.json').write_text(json.dumps(rows,indent=2));raise SystemExit(any(r['status']!=(1 if r['source']=='before' else 0) for r in rows))
