#!/usr/bin/env python3
"""Scoped draft baseline runner. Existing draft reports and runner stay usable."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
import re
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import run as actor

ROOT = Path(__file__).resolve().parents[1]
# Only the canonical ordinary-term fixture subset is compared here. Quoted
# text stays exact; variable names are normalized by first occurrence, not erased.
TOKEN = re.compile(r"\s+|'(?:''|\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"|[A-Za-z_][A-Za-z_0-9]*|[0-9]+(?:\.[0-9]+)?|[^\s]")
def variant_tokens(text: str) -> list[str]:
    names: dict[str,str] = {}
    out = []
    for token in TOKEN.findall(text):
        if token.isspace(): continue
        if re.fullmatch(r'[A-Z_][A-Za-z_0-9]*', token):
            if token == '_': token = f'V{len(names)}'; names[f'#anon{len(out)}'] = token
            else: token = names.setdefault(token, f'V{len(names)}')
        out.append(token)
    return out

def http_request(url: str, params: dict, timeout: float, token: str | None) -> dict:
    # Frame operator goals/templates identically for every node; HTTP carries
    # Prolog text, not the raw fragments used by a server's concatenation.
    params=dict(params)
    if not params.pop('_bare_goal',False):
        params['goal']='('+params['goal']+')'
        if 'template' in params:params['template']='('+params['template']+')'
    request = Request(url.rstrip('/')+'/call?'+urlencode(params))
    if token: request.add_header('Authorization','Bearer '+token)
    try:
        with urlopen(request,timeout=timeout) as response:
            status,body=response.status,response.read().decode('utf-8')
    except HTTPError as error:
        status,body=error.code,error.read().decode('utf-8')
    return dict(http_status=status,body=body)

def http_case(case: dict, url: str, timeout: float, token: str | None, diagnostic: bool) -> list:
    observations=[]
    for request in case['requests']:
        observed=http_request(url,request['params'],timeout,token);observations.append(observed)
        if diagnostic: continue
        actor.require(observed['http_status']==200,f'HTTP outcome {observed!r}')
        body=observed['body']
        if 'expect_prolog' in request:
            actor.require(variant_tokens(body)==variant_tokens(request['expect_prolog']),
                          f"expected {request['expect_prolog']!r}, got {body!r}")
        else:
            decoded=json.loads(body)
            if 'expect_json' in request:
                actor.require(all(decoded.get(k)==v for k,v in request['expect_json'].items()),repr(decoded))
            if 'expect_json_type' in request:
                actor.require(decoded.get('type')==request['expect_json_type'],repr(decoded))
    return observations

def query_case(case: dict, url: str, timeout: float, token: str | None) -> dict:
    candidate=actor.Candidate(url,'actor',timeout,token,None,False,())
    with actor.Harness(candidate) as harness:
        options='[session(true)]'
        if case.get('source'): options='[session(true),src_text('+actor.prolog_quote_atom(case['source'])+')]'
        harness.spawn_shell(options)
        # No once/1 or if-then-else around the assertion: More must expose
        # accidental nondeterminism instead of concealing it in the fixture.
        harness.call('('+case['goal']+'),BaselineResult=passed','[limit(1)]')
        result=harness.recv_type('success',limit=64)
        actor.require(actor.row_value(result,'BaselineResult')=='passed',repr(result))
        actor.require(result.get('more') is False,f'assertion left a continuation: {result!r}')
        try:harness.halt()
        except Exception as error:raise actor.ConformanceFailure(f'query answered {result!r}, but halt failed: {error}') from error
        return result

def wire_case(case: dict, url: str, timeout: float, token: str | None) -> dict:
    protocol=case['protocol']
    headers=(f'Sec-WebSocket-Protocol: {protocol}',) if protocol else ()
    ws=actor.WebSocket(url,timeout,token,extra_headers=headers)
    try:
        selected=ws.response_headers.get('sec-websocket-protocol')
        actor.require(selected==protocol,f'expected {protocol!r}, negotiated {selected!r}')
        tagged=protocol=='web-prolog-sync-spawn-v1'
        bad=dict(command='toplevel_call',pid=99999999999,goal='true',options='[]')
        requests=[bad,dict(command='toplevel_spawn',options='[session(true)]'),bad,
                  dict(command='toplevel_spawn',options="[src_text('broken(')]")]
        if tagged:
            requests[1]['request_id']='baseline-good'
            requests[3]['request_id']='baseline-bad'
        for request in requests: ws.send_json(request)
        replies=[ws.recv_json() for _ in range(4)]
        spawned=[r for r in replies if r.get('type')=='spawned']
        errors=[r for r in replies if r.get('type')=='error']
        actor.require(len(spawned)==1 and len(errors)==3,repr(replies))
        if tagged:
            actor.require(spawned[0].get('request_id')=='baseline-good',repr(replies))
            actor.require(sum(r.get('request_id')=='baseline-bad' for r in errors)==1,repr(replies))
            actor.require(sum('request_id' not in r for r in errors)==2,repr(replies))
        else:
            actor.require(all('request_id' not in r for r in replies),repr(replies))
        return dict(negotiated_subprotocol=selected,replies=replies)
    finally: ws.close()

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--url',required=True,help='HTTP base or WebSocket endpoint, according to the pack')
    parser.add_argument('--peer',help='peer HTTP base for cross-node cases')
    parser.add_argument('--candidate',required=True)
    parser.add_argument('--profile',choices=tuple(actor.PROFILE_ORDER),required=True)
    parser.add_argument('--timeout',type=float,default=8)
    parser.add_argument('--token-env')
    parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args()
    import os
    token=os.environ[args.token_env] if args.token_env else None
    pack=json.loads(args.manifest.read_text())
    if '__PEER__' in json.dumps(pack):
        if not args.peer: parser.error('this pack requires --peer')
        if not re.fullmatch(r'https?://[A-Za-z0-9.:-]+',args.peer): parser.error('peer must be a simple HTTP(S) node origin')
        pack=json.loads(json.dumps(pack).replace('__PEER__',args.peer))
    started=datetime.now(timezone.utc).isoformat();clock=time.monotonic();rows=[]
    diagnostic=pack['scope']=='diagnostic'
    for case in pack['cases']:
        row=dict(id=case['id'],title=case['title']);before=time.monotonic()
        if case.get('issue'): row['issue']=case['issue']
        minimum='isobase' if case['transport']=='http' else 'actor'
        if actor.PROFILE_ORDER[args.profile]<actor.PROFILE_ORDER[minimum]:
            row.update(status='unsupported',detail=f'requires {minimum}')
        else:
            try:
                if case['transport']=='http': observed=http_case(case,args.url,args.timeout,token,diagnostic)
                elif case['transport']=='query': observed=query_case(case,args.url,args.timeout,token)
                else: observed=wire_case(case,args.url,args.timeout,token)
                row.update(status='observed' if diagnostic else 'pass',observation=observed)
            except Exception as error:
                row.update(status='diagnostic_error' if diagnostic else 'fail',detail=f'{type(error).__name__}: {error}')
        row['duration_ms']=round((time.monotonic()-before)*1000);rows.append(row)
        print(row['status'].upper(),row['id'],row.get('detail',''),flush=True)
    counts={s:sum(r['status']==s for r in rows) for s in ['pass','fail','unsupported','observed','diagnostic_error']}
    report=dict(schema_version=2,baseline='0.1',suite=pack['suite'],scope=pack['scope'],
                candidate=args.candidate,advertised_profile=args.profile,endpoint=args.url,peer=args.peer,
                started_at=started,duration_ms=round((time.monotonic()-clock)*1000),counts=counts,results=rows)
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(counts));return bool(counts['fail'] or counts['diagnostic_error'])
if __name__=='__main__': raise SystemExit(main())
