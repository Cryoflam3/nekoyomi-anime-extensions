#!/usr/bin/env python3
"""Verify live metadata, indexes and all locked APK/icon hashes."""
import json,urllib.request,hashlib,concurrent.futures,datetime,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
base='https://raw.githubusercontent.com/Cryoflam3/nekoyomi-anime-extensions/main/'
def get(path):
 with urllib.request.urlopen(base+path,timeout=90) as r:return r.status,r.read()
proof={'verified_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base_url':base,'endpoints':{},'device_runtime':'not-tested'}
for f in ('repo.json','index.min.json','index.json'):
 status,data=get(f); parsed=json.loads(data)
 assert parsed==json.loads((root/f).read_bytes()),f
 proof['endpoints'][f]={'http_status':status,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
lock=json.loads((root/'upstreams.lock.json').read_text())['extensions']
def check(x):
 out={'package':x['entry']['pkg']}
 for kind,path,want in [('apk','apk/'+x['entry']['apk'],x['sha256']),('icon','icon/'+x['entry']['pkg']+'.png',x['icon_sha256'])]:
  status,data=get(path);actual=hashlib.sha256(data).hexdigest();assert actual==want,path
  out[kind]={'http_status':status,'sha256':actual}
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
 proof['packages']=[]
 for result in pool.map(check,lock):
  proof['packages'].append(result)
  if len(proof['packages']) % 25 == 0: print(f"Verified {len(proof['packages'])}/{len(lock)} packages",flush=True)
proof['counts']={'extensions':len(lock),'apk_downloads_verified':len(lock),'icon_downloads_verified':len(lock),'nsfw':sum(x['entry']['nsfw'] for x in lock)}
(root/'reports/live-validation.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({k:v for k,v in proof.items() if k!='packages'},indent=2))
