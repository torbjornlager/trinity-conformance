from pathlib import Path
import subprocess,hashlib,json
O=Path(__file__).resolve().parent;R=Path('/Users/lager/trealla-port')
assert not subprocess.check_output(['git','status','--porcelain'],cwd=R,text=True).strip()
files=sorted(R.glob('*.pl'));expected={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
lines=subprocess.check_output(['docker','exec','deployment-wp_n5-1','sha256sum',*('/app/'+f.name for f in files)],text=True).splitlines()
actual={Path(line.split(None,1)[1].strip()).name:line.split()[0] for line in lines};assert actual==expected
record=dict(revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),all_match=True,file_count=len(files),files_sha256=actual)
(O/'running-n5-source.json').write_text(json.dumps(record,indent=2)+'\n');print('PASS all',len(files),'N5 root Prolog source files match the committed qualified runtime')
