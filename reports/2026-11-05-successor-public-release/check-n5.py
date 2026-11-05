from pathlib import Path
import subprocess,json,urllib.request,urllib.parse,time
O=Path(__file__).resolve().parent;name='successor-n5-candidate';rows=[]
pack=json.loads((O/'manifest.json').read_text())
def docker(*args):return subprocess.check_output(['docker',*args],text=True).strip()
try:
 docker('run','-d','--name',name,'-p','127.0.0.1::3060','--entrypoint','/opt/trealla/tpl','trinity-successor-n5:20261105','-g','use_module(distribution),web_prolog:web_prolog_node(3060,[sandbox(blacklist),max_call_requests_per_window(1000)])')
 port=json.loads(docker('inspect',name))[0]['NetworkSettings']['Ports']['3060/tcp'][0]['HostPort'];base='http://127.0.0.1:'+port
 for _ in range(100):
  try:
   with urllib.request.urlopen(base+'/healthz',timeout=1):break
  except Exception:time.sleep(.1)
 else:raise TimeoutError('candidate readiness')
 def check(label,goal):
  q=dict(goal='('+goal+'),LibraryCheck=passed',template='LibraryCheck',format='prolog',limit=1,src_text=pack['source'])
  with urllib.request.urlopen(base+'/call?'+urllib.parse.urlencode(q),timeout=10) as response:body=response.read().decode()
  ok=''.join(body.split())=='success([passed],false).';rows.append(dict(id=label,status='pass' if ok else 'fail',body=body));assert ok,(label,body)
 for c in pack['cases']:
  check(c['id'],c['goal']);check('nested-'+c['id'],'findall(passed,('+c['goal']+'),[passed])')
 for offset in range(0,len(pack['cases']),8):check('batch-'+str(offset),','.join('findall(passed,('+c['goal']+'),[passed])' for c in pack['cases'][offset:offset+8]))
 print('PASS N5 candidate:',len(rows),'individual, nested and batch library controls',flush=True)
finally:
 (O/'candidate-n5-library.json').write_text(json.dumps(dict(scope='Actual Linux Trealla image: shared assertions individually, nested in findall and in public probe batches',results=rows,counts={s:sum(r['status']==s for r in rows) for s in ['pass','fail']}),indent=2)+'\n')
 subprocess.run(['docker','rm','-f',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
