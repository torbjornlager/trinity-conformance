from pathlib import Path
import json,sys,time,hashlib,collections
P=Path(__file__).resolve().parents[1];R=P/'suite-snapshot';sys.path[:0]=[str(R/'runner'),str(R/'adapters')]
import run as actor,baseline,admission_probe,local_runtime_contracts as contracts,local_page_errors as pages,node_uri_io,portable_text,client_naming
node=sys.argv[1];url='https://'+node+'.elfenbenstornet.se';ws=url.replace('https:','wss:')+'/ws';profile='isobase' if node in ['n1','n6'] else 'isotope' if node=='n2' else 'actor';engine='trealla' if node=='n5' else 'swi';peer='https://n3.elfenbenstornet.se' if node=='n4' else 'https://n4.elfenbenstornet.se';F=P/'live-more'/node;F.mkdir(parents=True,exist_ok=True)
while True:
 f=P/'logs'/('public-'+node+'.log')
 if f.exists() and ('complete' in f.read_text() if profile=='actor' else (P/'observations'/node/'isobase-http-0.1.json').exists()):break
 time.sleep(2)
actor.set_session_interval(2.1)
old_http=baseline.http_request;last_http=0
interval=1.3 if node in ['n1','n6'] else .7
def http(*a,**kw):
 global last_http
 delay=interval-(time.monotonic()-last_http)
 if delay>0:time.sleep(delay)
 last_http=time.monotonic();return old_http(*a,**kw)
baseline.http_request=http
# These suites have a maintained adapter requiring owned fixture configuration.
fixture_only={'retained-context-0.1':'Requires configured client identities and four controlled transport routes; separate exact-source fixture matrix', 'ownership-lifecycle-0.1':'Requires disposable PRIVATE node and two distinct execution-only principals', 'library-noncompletion-0.1':'Requires externally terminated infinite computation in an owned process', 'receive-control-0.1':'Requires controlled transport/guard peer and delivery barriers', 'http-session-context-0.1':'Dedicated live HTTP adapter and owned equal-credential controls recorded separately', 'prompt-http-0.1':'Dedicated retained HTTP prompt adapter recorded separately'}
for path in sorted((R/'cases').glob('*.json')):
 pack=json.loads(path.read_text());suite=pack['suite']
 if suite.startswith('standard-library-'):continue
 # Primary public observations already cover this manifest on this node.
 if (P/'observations'/node/(suite+'.json')).exists():continue
 rows=[]
 def save():
  (F/(suite+'.json')).write_text(json.dumps(dict(suite=suite,candidate=node,profile=profile,endpoint=url,manifest_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),scope=pack.get('scope','required'),results=rows,counts=dict(collections.Counter(r['status'] for r in rows))),indent=2)+'\n')
 for index,original in enumerate(pack['cases']):
  c=json.loads(json.dumps(original).replace('__PEER__',peer));transport=c.get('transport');minimum=c.get('minimum_profile',pack.get('minimum_profile','isobase' if transport=='http' else 'actor'));row=dict(id=c['id'],case_index=index,title=c.get('title',''))
  if actor.PROFILE_ORDER[profile]<actor.PROFILE_ORDER[minimum]:row.update(status='not_applicable',detail='requires '+minimum)
  elif suite in fixture_only:row.update(status='blocked',detail=fixture_only[suite])
  elif c.get('candidate') and c['candidate'] not in [engine,node]:row.update(status='not_applicable',detail='case selects another engine or route')
  elif 'blacklist' not in c.get('only_sandbox_modes',['blacklist']):row.update(status='not_applicable',detail='requires a different sandbox mode')
  elif 'blacklist' not in c.get('sandbox_modes',['blacklist']):row.update(status='deferred',detail=c.get('deferred_reason','not specified for deployed blacklist policy'))
  elif transport in ['wire','query_rejection','toplevel'] and profile!='actor':row.update(status='not_applicable',detail='requires retained WebSocket transport; this node exposes stateless HTTP')
  elif transport=='profile_policy':row.update(status='blocked',detail='compiled policy fixture; cannot inspect through public endpoint')
  elif transport is None and 'execution' in c and c['execution']=='source_uri':row.update(status='blocked',detail='requires a publicly served controlled portable-text source fixture')
  else:
   start=time.monotonic();diagnostic=pack.get('scope')=='diagnostic'
   try:
    if pack.get('source'):c['source']=pack['source']+'\n'+c.get('source','')
    if c.get('candidate_error_formals') and engine in c['candidate_error_formals']:
     c['expected_formal']=c['candidate_error_formals'][engine];c['expected_error_names']=[c['expected_formal'].split('(')[0]]
    candidate=actor.Candidate(ws,profile,10,None,url,False,())
    if suite=='client-naming-0.1':
     observed=client_naming.execute(c,lambda:client_naming.Session(ws,None));actor.require(observed['status']=='pass',repr(observed))
    elif suite=='node-uri-io-0.1':
     source=(R/pack['source_file']).read_text();goal=c['goal'].replace('$SELF_SLASH',actor.prolog_quote_atom(url+'/')).replace('$PEER_SLASH',actor.prolog_quote_atom(peer+'/')).replace('$SELF',actor.prolog_quote_atom(url)).replace('$PEER',actor.prolog_quote_atom(peer));observed=node_uri_io.query(ws,source,goal,c,10)
    elif suite=='portable-text-0.2':observed=portable_text.execute(candidate,c,peer,None)
    elif transport=='http':observed=baseline.http_case(c,url,10,None,diagnostic)
    elif transport=='query' and profile!='actor':
     params=dict(goal='('+c['goal']+'),BaselineResult=passed',template='BaselineResult',format='prolog',limit=1)
     if c.get('source'):params['src_text']=c['source']
     observed=baseline.http_case(dict(requests=[dict(params=params,expect_prolog='success([passed],false).')]),url,10,None,diagnostic)
    elif transport=='query':observed=baseline.query_case(c,ws,10,None)
    elif transport=='query_rejection':observed=contracts.query_rejection_case(c,ws)
    elif transport=='wire':observed=baseline.wire_case(c,ws,10,None)
    elif transport=='toplevel':observed=pages.toplevel_case(c,ws.removesuffix('/ws'))
    elif transport=='admission':observed=admission_probe.observe(c,ws,10,None)
    elif c['id'] in actor.CASE_FUNCTIONS:observed=actor.CASE_FUNCTIONS[c['id']](candidate)
    else:raise ValueError('No public handler for '+str(transport)+'/'+c['id'])
    row.update(status=('observed' if diagnostic else 'pass'),observation=observed)
    if diagnostic and isinstance(observed,dict) and observed.get('complete') is False:row['status']='diagnostic_error'
   except Exception as e:row.update(status='diagnostic_error' if diagnostic else 'fail',detail=type(e).__name__+': '+str(e))
   row['duration_ms']=round((time.monotonic()-start)*1000)
  rows.append(row);save()
 print(node,suite,dict(collections.Counter(r['status'] for r in rows)),flush=True)
(P/'logs'/('more-'+node+'.done')).write_text('complete\n')
