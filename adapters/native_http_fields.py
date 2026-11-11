#!/usr/bin/env python3
"""Qualify native HTTP fields using a disposable loopback peer and synthetic tokens."""
from pathlib import Path
import argparse
import http.server, threading, json, subprocess, os, base64
from urllib.parse import parse_qs, urlsplit

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['swi-root', 'trealla-root', 'tpl', 'output']:
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    p = args.output
    requests = []

    class Peer(http.server.BaseHTTPRequestHandler):

        def log_message(self, *a):
            pass

        def do_GET(self):
            path = self.path.split('?')[0]
            requests.append({'path': path, 'fields': [(k, v) for (k, v) in self.headers.items() if k.lower() in ['x-probe', 'authorization', 'user-agent']]})
            query = parse_qs(urlsplit(self.path).query)
            more = query.get('limit') == ['1'] and query.get('offset') == ['0']
            body = b'helper(ok).\n' if path == '/source.pl' else b'success([v(ok)],true).\n' if more else b'success([v(ok)],false).\n'
            self.send_response(200)
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
    peer = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Peer)
    threading.Thread(target=peer.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{peer.server_port}'

    def atom(s):
        return "'" + s.replace("'", "''") + "'"
    cases = [{'id': 'H-001', 'title': 'ASCII control', 'opts': "request_header('X-Probe'=value)", 'field': 'x-probe', 'wire': 'value'}, {'id': 'H-002', 'title': 'Character-list header', 'opts': "request_header('X-Probe'=[v,a,l,u,e])", 'field': 'x-probe', 'wire': 'value'}, {'id': 'H-003', 'title': 'First case-insensitive header wins', 'opts': "request_header('X-Probe'=first),request_header('x-probe'=second)", 'field': 'x-probe', 'wire': 'first'}, {'id': 'H-004', 'title': 'Explicit Authorization precedes credential option', 'opts': "request_header('Authorization'='Bearer first'),authorization(bearer(second))", 'field': 'authorization', 'wire': 'Bearer first'}, {'id': 'H-005', 'title': 'Bearer credentials', 'opts': 'authorization(bearer(test_token))', 'field': 'authorization', 'wire': 'Bearer test_token'}, {'id': 'H-006', 'title': 'UTF-8 header', 'opts': "request_header('X-Probe'='räv')", 'field': 'x-probe', 'wire': 'räv'.encode().decode('latin1')}, {'id': 'H-007', 'title': 'UTF-8 Basic credentials', 'opts': "authorization(basic('räv','testpass'))", 'field': 'authorization', 'wire': 'Basic ' + base64.b64encode('räv:testpass'.encode()).decode()}, {'id': 'H-008', 'title': 'Malformed pair before source fetch', 'opts': 'request_header(bad)', 'error': 'type_error(http_request_header,bad)'}, {'id': 'H-009', 'title': 'Numeric field name before source fetch', 'opts': 'request_header(42=value)', 'error': 'type_error(atom,42)'}, {'id': 'H-010', 'title': 'Invalid token name before source fetch', 'opts': "request_header('bad name'=value)", 'error': "domain_error(http_header_name,'bad name')"}, {'id': 'H-011', 'title': 'Reserved proxy identity before source fetch', 'opts': "request_header('X-Web-Prolog-User'=fake_identity)", 'error': "permission_error(set,proxy_header,'X-Web-Prolog-User')"}, {'id': 'H-012', 'title': 'Shadowed invalid duplicate still validated', 'opts': "request_header('X-Probe'=first),request_header('x-probe'='bad\nvalue')", 'error': "domain_error(http_header_value,'bad\nvalue')"}]
    cases += [{'id': 'H-013', 'title': 'Credential option precedes explicit Authorization', 'opts': "authorization(bearer(first)),request_header('Authorization'='Bearer second')", 'field': 'authorization', 'wire': 'Bearer first'}, {'id': 'H-014', 'title': 'User agent precedence', 'opts': "user_agent([f,i,r,s,t]),request_header('USER-AGENT'=second)", 'field': 'user-agent', 'wire': 'first'}, {'id': 'H-015', 'title': 'Explicit user agent precedence', 'opts': "request_header('User-Agent'=first),user_agent(second)", 'field': 'user-agent', 'wire': 'first'}, {'id': 'H-016', 'title': 'Later slices preserve fields', 'opts': "request_header('X-Probe'=first),request_header('x-probe'=second),limit(1)", 'field': 'x-probe', 'wire': 'first', 'pages': 2}, {'id': 'H-017', 'title': 'Execution fields excluded from source fetch', 'opts': "request_header('X-Probe'=execution),src_uri(" + atom(base + '/source.pl') + ')', 'field': 'x-probe', 'wire': 'execution', 'source': True}]
    cases += [{'id': 'H-018', 'title': 'Native string field', 'opts': 'request_header(\'X-Probe\'="value")', 'field': 'x-probe', 'wire': 'value'}, {'id': 'H-019', 'title': 'HTAB is permitted', 'opts': "request_header('X-Probe'='a\\tb')", 'field': 'x-probe', 'wire': 'a\tb'}, {'id': 'H-020', 'title': 'Empty character list is permitted', 'opts': "request_header('X-Probe'=[])", 'field': 'x-probe', 'wire': ''}, {'id': 'H-021', 'title': 'Supplementary Unicode field', 'opts': "request_header('X-Probe'='🦊')", 'field': 'x-probe', 'wire': '🦊'.encode().decode('latin1')}]
    for c in cases:
        c['opts'] = c['opts'].replace('\n', '\\n')
        if 'error' in c:
            c['error'] = c['error'].replace('\n', '\\n')
    results = []
    env = dict(os.environ, TPL_LIBRARY_PATH=str(args.tpl.parent / 'library'), PYTHONDONTWRITEBYTECODE='1')
    try:
        for (host, root) in [('swi', args.swi_root), ('trealla', args.trealla_root)]:
            fixture = atom(str(Path(__file__).with_name('http_field_order.pl')))
            check = 'use_module(' + fixture + '),(http_field_order:check->halt;halt(1))'
            command = ['swipl', '-f', 'none', '-q', '-g', 'use_module(prolog/web_prolog),' + check] if host == 'swi' else [str(args.tpl), '-g', 'use_module(rpc),' + check]
            order = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True, timeout=10)
            results.append({'host': host, 'kind': 'rpc/promise', 'id': 'ORDER', 'title': 'Validation precedes resolver and promise allocation (instrumented positive control)', 'status': 'pass' if order.returncode == 0 else 'fail', 'stdout': order.stdout, 'stderr': order.stderr})
            for kind in ['rpc', 'promise']:
                for c in cases:
                    if kind == 'promise' and c.get('pages'):
                        continue
                    opts = c['opts']
                    invoke = lambda options: 'rpc(' + atom(base) + ',X=ok,[' + options + '])' if kind == 'rpc' else 'promise(' + atom(base) + ',X=ok,Ref,[template(v(X)),' + options + '])'
                    if 'error' in c:
                        opts += ',src_uri(' + atom(base + '/source.pl') + ')'
                        body = 'catch(' + invoke(opts) + ',E,true),(nonvar(E),E=error(' + c['error'] + ',_),var(X),var(Ref)->true;write_canonical(E),nl,fail)'
                    else:
                        body = 'findall(X,' + invoke(opts) + ',Xs),Xs==[ok,ok]' if c.get('pages') else invoke(opts) + (',X==ok' if kind == 'rpc' else ',var(X),yield(Ref,A,[timeout(3)]),A==success([v(ok)],false),rpc:promise_cleanup(Ref)')
                    if 'error' in c:
                        body += ',rpc(' + atom(base + '/recovery') + ",Recovery=ok,[request_header('X-Probe'=recovery)]),Recovery==ok"
                    if host == 'swi':
                        cmd = ['swipl', '-f', 'none', '-q', '-g', 'use_module(prolog/web_prolog),(catch((' + body + '),Error,(write_canonical(Error),nl,fail))->halt;halt(1))']
                    else:
                        cmd = [str(args.tpl), '-g', 'use_module(rpc),use_module(source_policy),source_policy:configure_source_policy([load_uri_allowed_origins([' + atom(base) + "]),load_uri_allowed_ip_ranges(['127.0.0.0/8'])],_),(catch((" + body + '),Error,(write_canonical(Error),nl,fail))->halt;halt(1))']
                    start = len(requests)
                    try:
                        q = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True, timeout=8)
                        seen = requests[start:]
                        ok = q.returncode == 0
                        if 'error' in c:
                            ok = ok and len(seen) == 1 and (seen[0]['path'] in ['/call', '/recovery/call']) and ([v for (k, v) in seen[0]['fields'] if k.lower() == 'x-probe'] == ['recovery'])
                        else:
                            execution = [x for x in seen if x['path'] == '/call']
                            source = [x for x in seen if x['path'] == '/source.pl']
                            ok = ok and len(execution) == c.get('pages', 1) and all(([v for (k, v) in x['fields'] if k.lower() == c['field']] == [c['wire']] for x in execution))
                            if c.get('source'):
                                ok = ok and len(source) == 1 and all((k.lower() != c['field'] for x in source for (k, v) in x['fields']))
                        row = {'kind': kind, 'host': host, 'id': c['id'], 'title': c['title'], 'status': 'pass' if ok else 'fail', 'exit_code': q.returncode, 'stdout': q.stdout, 'stderr': q.stderr, 'requests': seen}
                    except subprocess.TimeoutExpired:
                        row = {'kind': kind, 'host': host, 'id': c['id'], 'title': c['title'], 'status': 'fail', 'detail': 'probe exceeded 8 seconds', 'requests': requests[start:]}
                    results.append(row)
                    print(host, c['id'], row['status'], flush=True)
    finally:
        peer.shutdown()
        peer.server_close()
    (p / 'http-probes.json').write_text(json.dumps(cases, indent=2) + '\n')
    (p / 'http-probe-results.json').write_text(json.dumps(results, indent=2) + '\n')
    raise SystemExit(int(any((r['status'] != 'pass' for r in results))))
if __name__ == '__main__':
    main()
