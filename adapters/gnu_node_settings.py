#!/usr/bin/env python3
"""Record GNU's maintained owner/worker settings and privacy checks."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import re
import select
import tarfile
import tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runner'))
from baseline import http_case


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def baseline(args):
    revision=args.baseline_revision
    if not re.fullmatch('[0-9a-f]{40}',revision):raise ValueError('Use a full baseline commit SHA')
    manifest=ROOT/'cases/node-settings-0.1.json'
    pack=json.loads(manifest.read_text());rows=[]
    archive=subprocess.check_output(['git','archive',revision,'isobase'],cwd=args.gnu_root)
    with tempfile.TemporaryDirectory(prefix='gnu-settings-baseline-') as directory:
        root=Path(directory)
        with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
            for member in tar.getmembers():
                if (member.name!='isobase' and not member.name.startswith('isobase/')) or '..' in Path(member.name).parts or member.issym() or member.islnk():
                    raise ValueError('Baseline fixture requires an ordinary isobase source tree')
            tar.extractall(root)
        scope=root/'isobase'
        with (args.output/'build.txt').open('w') as log:
            subprocess.run(['make','all','ROOT='+str(args.gnu_root)],cwd=scope,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=120)
        source=dict(revision=revision,scope='Immutable Git archive built with the current installed GNU toolchain; not an original-release binary certificate',
                    files_sha256={str(p.relative_to(root)):sha(p) for p in sorted(scope.iterdir()) if p.suffix in ['.c','.h','.pl']},
                    compiler_sha256=sha(args.gnu_root/'install/bin/gplc'),
                    binaries_sha256={f:sha(scope/f) for f in ['isobase-node','query-supervisor','query-worker']})
        env={k:v for k,v in os.environ.items() if not k.startswith('ISO_')}
        node=subprocess.Popen([str(scope/'isobase-node'),'--auth','open','--port','0','--time-ms','3000'],cwd=scope,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        try:
            if not select.select([node.stdout],[],[],5)[0]:raise TimeoutError('baseline startup')
            started=node.stdout.readline()
            if not started:raise RuntimeError(node.stderr.read())
            url='http://127.0.0.1:'+str(json.loads(started)['port'])
            for case in pack['cases']:
                row=dict(candidate='gnu',id=case['id'],title=case['title'])
                wire=dict(requests=[dict(params=dict(goal='('+case['goal']+'),NodeCheck=passed',template='NodeCheck',format='prolog',limit=1,src_text=pack['source']),expect_prolog='success([passed],false).')])
                try:row.update(status='pass',observation=http_case(wire,url,8,None,False))
                except Exception as error:row.update(status='fail',detail=str(error))
                rows.append(row)
        finally:
            node.terminate()
            try:node.wait(timeout=5)
            except subprocess.TimeoutExpired:node.kill();node.wait()
    report=dict(suite=pack['suite'],adapter_sha256=sha(__file__),manifest_sha256=sha(manifest),sources=source,results=rows,
                counts={s:sum(r['status']==s for r in rows) for s in ['pass','fail']})
    (args.output/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['counts']))
    return int(report['counts']['fail']>0)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gnu-root',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--baseline-revision',help='Rebuild an immutable pre-repair source archive and run the shared cases')
    args=parser.parse_args()
    args.gnu_root=args.gnu_root.resolve()
    args.output=args.output.resolve()
    args.output.mkdir(parents=True,exist_ok=False)
    if args.baseline_revision:return baseline(args)
    scope=args.gnu_root/'isobase'
    env={k:v for k,v in os.environ.items() if not k.startswith('ISO_')}
    env.update(ISO_NODE=str(scope/'isobase-node'),ISO_WORKER=str(scope/'query-worker'),ISO_SUPERVISOR=str(scope/'query-supervisor'))
    report_path=(args.output/'results.json').resolve()
    with (args.output/'driver.txt').open('w') as log:
        result=subprocess.run([sys.executable,str(scope/'node_settings_tests.py'),'--report',str(report_path)],cwd=scope,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=120)
    if not report_path.exists():raise RuntimeError('GNU checks produced no report; see driver.txt')
    report=json.loads(report_path.read_text())
    report.update(adapter_sha256=sha(__file__),test_source_sha256=sha(scope/'node_settings_tests.py'),
                  sources=dict(revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=args.gnu_root,text=True).strip(),
                               tracked_diff_sha256=hashlib.sha256(subprocess.check_output(['git','diff','HEAD','--'],cwd=args.gnu_root)).hexdigest(),
                               files_sha256={str(p.relative_to(args.gnu_root)):sha(p) for p in sorted(scope.iterdir()) if p.suffix in ['.c','.h','.pl','.py'] or p.name=='Makefile'},
                               binaries_sha256={f:sha(scope/f) for f in ['isobase-node','query-supervisor','query-worker']}),
                  driver_exit_code=result.returncode,
                  scope='Disposable GNU ISOBASE HTTP nodes and trusted private worker/supervisor inputs; no public deployment or Linux query-jail qualification')
    report_path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['counts']))
    return result.returncode


if __name__=='__main__':raise SystemExit(main())
