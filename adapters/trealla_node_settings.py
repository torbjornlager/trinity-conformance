#!/usr/bin/env python3
"""Qualify Trealla public settings on disposable profile/sandbox fixtures."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'runner'))
from baseline import http_case, variant_tokens
from run import Candidate, Harness, row_value, prolog_quote_atom
from local_standard_library import port, atom, sha


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tpl', required=True)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    manifest = ROOT/'cases/node-settings-0.1.json'
    pack = json.loads(manifest.read_text())
    rows = []
    helper = 'ns_read(K,V):-node_setting(K,V).'
    sources = dict(revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=args.root,text=True).strip(),
                   diff_sha256=hashlib.sha256(subprocess.check_output(['git','diff'],cwd=args.root)).hexdigest(),
                   executable_sha256=sha(args.tpl),
                   files_sha256={p.name:sha(p) for p in sorted(args.root.glob('*.pl'))})
    libraries = Path(args.tpl).parent/'library'
    sources['engine_library_sha256'] = hashlib.sha256(''.join(str(p.relative_to(libraries))+':'+sha(p)+'\n' for p in sorted(libraries.rglob('*')) if p.is_file()).encode()).hexdigest()
    def save():
        report = dict(suite='trealla-node-settings-0.1', manifest_sha256=sha(manifest), adapter_sha256=sha(__file__),
                      helper_files_sha256={f:sha(ROOT/f) for f in ['adapters/local_standard_library.py','runner/baseline.py','runner/run.py']},
                      sources=sources, results=rows, counts={s:sum(r['status']==s for r in rows) for s in ['pass','fail']})
        (args.output/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    for profile in ['isobase','isotope','actor']:
      for mode in ['blacklist','whitelist','off']:
        n = port()
        url = f'http://127.0.0.1:{n}'
        public_url = f'https://settings.example.test/{profile}/{mode}'
        expected = dict(url=public_url,profile=profile,sandbox=mode,auth='dev',rate_window_seconds=71,
                        max_inflight_calls=13,max_term_text_bytes=70001,max_call_requests_per_window=1000,
                        max_load_text_bytes=90001,load_uri_allowed_origins=['https://source.example.test:443'],
                        max_session_spawns_per_window=211,max_ws_actors_per_principal=23,
                        max_ws_frame_bytes=262145,max_ws_commands_per_window=307)
        options = [f'profile({profile})',f'sandbox({mode})','auth(dev)',f'node_url({atom(public_url)})',
                   'dev_principal(ns_private_principal)', 'bearer_token(ns_fixture,ns_private_credential,[execute])',
                   'rate_window_seconds(71)','max_inflight_calls(13)','max_term_text_bytes(70001)',
                   'max_call_requests_per_window(1000)','max_source_text_bytes(90001)',
                   "load_uri_allowed_origins(['https://source.example.test'])",'max_session_spawns_per_window(211)',
                   'max_ws_actors_per_principal(23)','max_ws_frame_bytes(262145)','max_ws_commands_per_window(307)']
        if profile != 'actor':
            for key in ['max_ws_actors_per_principal','max_ws_frame_bytes','max_ws_commands_per_window']:
                del expected[key]
        if profile == 'isobase':
            del expected['max_session_spawns_per_window']
        def term(v):
            return '['+','.join(atom(x) for x in v)+']' if isinstance(v,list) else str(v) if isinstance(v,int) else atom(v)
        pairs = '['+','.join(atom(k)+'-'+term(v) for k,v in sorted(expected.items()))+']'
        compare = 'Sorted=='+pairs
        config = 'findall(K-V,node_setting(K,V),Pairs),sort(Pairs,Sorted),'+compare
        fixture = profile+'-'+mode
        def check(case_id, title, operation):
            row = dict(candidate='trealla',id=fixture+'-'+case_id,title=title)
            try:
                row.update(status='pass',observation=operation())
            except Exception as error:
                row.update(status='fail',detail=str(error))
            rows.append(row)
            save()
            print(row['id'],row['status'],flush=True)
        def http(goal, source='', spoof=False, denied=False):
            params = dict(goal='('+goal+'),NodeCheck=passed',template='NodeCheck',format='prolog',limit=1,src_text=source)
            request = Request(url+'/call?'+urlencode(params),headers={'Host':'wrong.example:65000'} if spoof else {})
            with urlopen(request,timeout=8) as response:
                body = response.read().decode()
            if denied:
                error_name = 'profile_violation' if denied == 'profile' else 'permission_error'
                if not body.startswith('error(') or error_name not in body:
                    raise AssertionError(body)
            elif variant_tokens(body) != variant_tokens('success([passed],false).'):
                raise AssertionError(body)
            return dict(body=body)
        env = dict(os.environ,TPL_LIBRARY_PATH=str(libraries))
        with (args.output/(fixture+'.log')).open('w+') as log:
          node = subprocess.Popen([args.tpl,'-g',f'use_module(distribution),web_prolog:web_prolog_node({n},['+','.join(options)+'])'],cwd=args.root,env=env,stdout=log,stderr=subprocess.STDOUT)
          try:
            for _ in range(200):
                if node.poll() is not None:
                    log.seek(0)
                    raise RuntimeError(log.read())
                try:
                    with socket.create_connection(('127.0.0.1',n),timeout=.1):
                        break
                except OSError:
                    time.sleep(.03)
            else:
                raise TimeoutError('node startup')
            for case in pack['cases']:
                check(case['id']+'-http',case['title'],lambda c=case:http(c['goal']))
                check(case['id']+'-source',case['title'],lambda c=case:http(c['goal'].replace('node_setting(','ns_read('),helper))
            check('configured','Complete actual public settings',lambda:http(config))
            check('host-header','Configured identity ignores untrusted Host header',lambda:http(config,spoof=True))
            check('unavailable','Unavailable and private values fail',lambda:http('\\+node_setting(timeout,_),\\+node_setting(max_sessions_per_principal,_),\\+node_setting(dev_principal,_),\\+node_setting(bearer_token,_),\\+node_setting(auth,ns_private_credential)'))
            check('current-values','Bound mismatches cannot fall back to defaults',lambda:http('\\+node_setting(rate_window_seconds,60),\\+node_setting(max_inflight_calls,4),\\+node_setting(max_term_text_bytes,32768),\\+node_setting(max_load_text_bytes,262144),\\+node_setting(load_uri_allowed_origins,[])'))
            if mode != 'off':
                check('reserved-source','Private source cannot replace the public relation',lambda:http('true','node_setting(profile,forged).',denied=True))
                if profile != 'isobase':
                    check('stateless-update','Stateless route rejects a mutating call',lambda:http('assertz(node_setting(profile,forged))',denied='profile'))
            if profile == 'actor':
              for source in ['',helper]:
                label = 'private' if source else 'sourceless'
                with Harness(Candidate(f'ws://127.0.0.1:{n}/ws','actor',8,None,url,False,())) as harness:
                  harness.spawn_shell('[session(true)'+(',src_text('+prolog_quote_atom(source)+')' if source else '')+']')
                  def session(goal, denied=False):
                      harness.call('('+goal+'),NodeCheck=passed','[limit(1)]')
                      event = harness.recv()
                      if denied:
                          if event.get('type') != 'error' or 'permission_error' not in str(event):
                              raise AssertionError(event)
                          return event
                      if event.get('type') != 'success' or event.get('more') is not False or row_value(event,'NodeCheck') != 'passed':
                          raise AssertionError(event)
                      return event
                  for case in pack['cases']:
                      check(case['id']+'-'+label+'-session',case['title'],lambda c=case:session(c['goal'].replace('node_setting(','ns_read(') if source else c['goal']))
                  check('configured-'+label,'Exact settings in a retained session',lambda:session(config))
                  child = 'self(Me),spawn((findall(K-V,node_setting(K,V),Pairs),Me!ns_settings(Pairs)),_,[]),receive({ns_settings(Pairs)->sort(Pairs,Sorted)},[timeout(3)]),'+compare
                  check('child-'+label,'Spawned child retains the serving node',lambda:session(child))
                  program = 'ns_report(To):-findall(K-V,node_setting(K,V),Pairs),To!ns_settings(Pairs).'
                  private_child = 'self(Me),spawn(ns_report(Me),_,[src_text('+prolog_quote_atom(program)+')]),receive({ns_settings(Pairs)->sort(Pairs,Sorted)},[timeout(3)]),'+compare
                  check('source-child-'+label,'A private child helper reads the serving node settings',lambda:session(private_child))
                  guard = "self(Me),Me!ns_guard,receive({ns_guard if node_setting(profile,actor)->node_setting(url,U)},[timeout(1)]),U=="+atom(public_url)
                  check('guard-'+label,'Receive guard and body can read settings',lambda:session(guard))
                  if mode != 'off':
                      check('reserved-update-'+label,'ACTOR mutation cannot replace the public relation',lambda:session('assertz(node_setting(profile,forged))',denied=True))
          finally:
            node.terminate()
            try:
                node.wait(timeout=5)
            except subprocess.TimeoutExpired:
                node.kill()
                node.wait()
    return int(any(row['status']=='fail' for row in rows))


if __name__ == '__main__':
    raise SystemExit(main())
