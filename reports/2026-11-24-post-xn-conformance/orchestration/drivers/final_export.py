"""Export only after every live/owned phase has terminal evidence."""
from pathlib import Path
import subprocess,time,sys
P=Path(__file__).resolve().parent
while not ((P/'admission.complete').exists() and (P/'cross-node.complete').exists()):time.sleep(3)
for name in ['verify_completion.py','build_report.py','render_report.py']:
 print('START',name,flush=True);subprocess.run([sys.executable,str(P/'orchestration'/name)],check=True);print('PASS',name,flush=True)
(P/'final-export.complete').write_text('complete\n');print('Fresh full report exported; index update and final review remain',flush=True)
