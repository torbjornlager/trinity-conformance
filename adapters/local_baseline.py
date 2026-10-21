#!/usr/bin/env python3
"""Reproduce the bounded matrix on disposable loopback nodes; no runtime edits."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import select
import socket
import subprocess
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parents[1]
def free_port():
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));return sock.getsockname()[1]
def quoted(value):return "'"+str(value).replace('\\','\\\\').replace("'","''")+"'"
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--swipl',required=True);parser.add_argument('--tpl',required=True)
    parser.add_argument('--node',required=True);parser.add_argument('--gnu-root',type=Path,default=ROOT.parent/'gprolog-port')
    parser.add_argument('--swi-root',type=Path,default=ROOT.parent/'trinity-demonstrator')
    parser.add_argument('--trealla-root',type=Path,default=ROOT.parent/'trealla-port')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy();env['TPL_LIBRARY_PATH']=str(Path(args.tpl).resolve().parent/'library')
    processes=[];logs=[];reports=[];native={};start=time.time()
    def launch(name,command,cwd):
        log=(args.output/(name+'-node.log')).open('w');logs.append(log)
        proc=subprocess.Popen(command,cwd=cwd,env=env,stdout=log,stderr=log);processes.append(proc);return proc
    def ready(port,proc):
        for _ in range(150):
            if proc.poll() is not None:raise RuntimeError(f'node exited during startup: {proc.returncode}')
            try:
                with socket.create_connection(('127.0.0.1',port),timeout=.1):return
            except OSError:time.sleep(.05)
        raise TimeoutError('node startup timed out')
    def run(label,command):
        with (args.output/(label+'.log')).open('w') as log:
            try: result=subprocess.run(command,cwd=ROOT,env=env,stdout=log,stderr=log,timeout=150);code=result.returncode
            except subprocess.TimeoutExpired:code='timeout'
        print(label,code,flush=True)
        report=args.output/(label+'.json')
        reports.append(dict(label=label,exit_code=code,report=report.name if report.exists() else None))
    def pack(name,candidate,url,profile='actor',peer=None):
        label=candidate+'-'+name+('-to-'+peer[0] if peer else '')
        command=[sys.executable,'runner/baseline.py','--manifest','cases/'+name+'-0.1.json','--url',url,
                 '--candidate',candidate,'--profile',profile,'--report',str(args.output/(label+'.json'))]
        if peer:command+=['--peer',peer[1]]
        run(label,command)
    metadata=dict(started_at=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(start)),nodes={},sources={},runs=reports)
    for name,path in [('conformance',ROOT),('swi',args.swi_root),('trealla',args.trealla_root),('gnu',args.gnu_root)]:
        metadata['sources'][name]=dict(path=str(path),revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=path,text=True).strip(),
          dirty=subprocess.check_output(['git','status','--short'],cwd=path,text=True).splitlines())
    input_files=list((ROOT/'cases').glob('*.json'))+list((ROOT/'profiles').glob('*.md'))+list((ROOT/'baselines').glob('*'))
    input_files += [ROOT/f for f in ['runner/run.py','runner/baseline.py','runner/coverage.py','adapters/local_baseline.py','adapters/wasm.cjs','schemas/report-v2.schema.json']]
    input_files += [args.swi_root/'tests/wasm/swi_wasm_contracts.js']
    metadata['inputs']={str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):digest(p) for p in input_files if p.is_file()}
    metadata['versions']={}
    for name,cmd in [('swi',[args.swipl,'--version']),('trealla',[args.tpl,'-g','current_prolog_flag(version_data,V),writeq(V),nl,halt']),
                     ('gnu',[str(args.gnu_root/'install/bin/gprolog'),'--version']),('node',[args.node,'--version'])]:
        r=subprocess.run(cmd,capture_output=True,text=True,env=env,timeout=10)
        metadata['versions'][name]=(r.stdout+r.stderr).strip()
    try:
      with tempfile.TemporaryDirectory(prefix='trinity-baseline-') as temp:
        for name in ['swi','trealla']:
            port=free_port();url=f'http://127.0.0.1:{port}';native[name]=url
            if name=='swi':
                goal=f"use_module(library(sgml)),use_module(library(option)),use_module({quoted(args.swi_root/'prolog/web_prolog/node.pl')}),set_setting(http:public_host,'127.0.0.1'),set_setting(http:public_port,{port}),set_setting(http:public_scheme,http),use_module(library(socket)),tcp_socket(Socket),tcp_bind(Socket,ip(127,0,0,1):{port}),tcp_listen(Socket,128),node:node({port},[tcp_socket(Socket),profile(actor),sandbox(blacklist),auth(open)]),thread_get_message(stop)"
                cmd=[args.swipl,'-f','none','-q','-g',goal];cwd=args.swi_root
            else:
                goal=f"consult('distribution.pl'),web_prolog:web_prolog_node({port},[bind_address('127.0.0.1'),node_url({quoted(url)}),profile(actor),sandbox(blacklist),auth(open)]),thread_get_message(stop)"
                cmd=[args.tpl,'-g',goal];cwd=args.trealla_root
            proc=launch(name,cmd,cwd);ready(port,proc)
        policy=Path(temp)/'outbound.policy';policy.write_text('');policy.chmod(0o600)
        startup=(args.output/'gnu-startup.log').open('w+');logs.append(startup)
        gnu_exe=args.gnu_root/'isobase/isobase-node'
        proc=subprocess.Popen([str(gnu_exe),'--auth','open','--port','0','--time-ms','5000','--idle-ms','30000',
                               '--outbound-policy',str(policy)],cwd=args.gnu_root/'isobase',env=env,stdout=subprocess.PIPE,stderr=startup,text=True)
        processes.append(proc)
        if not select.select([proc.stdout],[],[],10)[0]:raise TimeoutError('GNU startup timed out')
        line=proc.stdout.readline();startup.write(line);startup.flush();port=json.loads(line)['port'];native['gnu']=f'http://127.0.0.1:{port}'
        policy.write_text(''.join(f'http 127.0.0.1 {url.rsplit(":",1)[1]} 127.0.0.1\n' for url in native.values()))
        for name,url in native.items():
            metadata['nodes'][name]=dict(url=url,bind_address='127.0.0.1',profile='isobase' if name=='gnu' else 'actor',sandbox='restricted ISOBASE' if name=='gnu' else 'blacklist',auth='open, disposable loopback fixture')
            pack('isobase-http',name,url,'isobase' if name=='gnu' else 'actor')
            pack('isobase-diagnostics',name,url,'isobase' if name=='gnu' else 'actor')
        for name,url in native.items():
            if name=='gnu':continue
            ws=url.replace('http:','ws:')+'/ws'
            pack('language-actor',name,ws);pack('wire-capabilities',name,ws)
            for suite in ['actor-core','actor-workers','actor-behaviours','actor-supervisors','supervisor-diagnostics','worker-diagnostics','portable-text']:
                label=name+'-'+suite
                run(label,[sys.executable,'runner/run.py','--manifest','cases/'+suite+'-0.1.json','--ws-url',ws,
                           '--candidate',name,'--timeout','8','--report',str(args.output/(label+'.json'))])
        for name,url in native.items():
            for peer,peer_url in native.items():pack('interop-http',name,url,'isobase' if name=='gnu' else 'actor',(peer,peer_url))
            if name!='gnu':
                for peer,peer_url in native.items():
                    if peer!='gnu':pack('interop-actor',name,url.replace('http:','ws:')+'/ws',peer=(peer,peer_url))
        for mode in ['worker','main']:
            label='swi-wasm-'+mode+'-language-actor'
            run(label,[args.node,'adapters/wasm.cjs',str(args.swi_root),mode,'cases/language-actor-0.1.json',str(args.output/(label+'.json'))])
        for name,exe in [('swi',args.swipl),('trealla',args.tpl),('gnu',str(gnu_exe)),('gnu-worker',str(args.gnu_root/'isobase/query-worker')),('gnu-supervisor',str(args.gnu_root/'isobase/query-supervisor')),('wasm',str(args.swi_root/'web/swipl-bundle.js'))]:
            metadata.setdefault('binaries',{})[name]=dict(path=exe,sha256=digest(exe))
    finally:
        for proc in reversed(processes):
            proc.terminate()
            try:proc.wait(timeout=5)
            except subprocess.TimeoutExpired:proc.kill();proc.wait()
        for log in logs:log.close()
        metadata['duration_seconds']=round(time.time()-start,2)
        (args.output/'provenance.json').write_text(json.dumps(metadata,indent=2)+'\n')
    subprocess.run([sys.executable,'runner/coverage.py',str(args.output)],cwd=ROOT,check=True)
    bad=False
    for row in reports:
        if not row['report']:bad=True;continue
        report=json.loads((args.output/row['report']).read_text())
        diagnostic=report.get('scope')=='diagnostic' or any(part in row['label'] for part in ['supervisor-diagnostics','worker-diagnostics','portable-text'])
        if report['counts'].get('diagnostic_error',0) or (not diagnostic and report['counts']['fail']):bad=True
    return int(bad)
if __name__=='__main__':raise SystemExit(main())
