#!/usr/bin/env python3
"""Reconstruct only reviewed, SHA-256-locked upstream bytes. Never re-sign APKs."""
import argparse,concurrent.futures,json,pathlib,shutil,urllib.request
from validate import digest,require
p=argparse.ArgumentParser();p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
root=pathlib.Path(__file__).resolve().parents[1];out=a.output.resolve()
require(out!=root,'Use a separate output directory')
require(not out.exists(),'Output directory must be new')
lock=json.loads((root/'upstreams.lock.json').read_text());out.mkdir(parents=True)
for n in ['licenses','reports']:shutil.copytree(root/n,out/n)
for n in ['repo.json','upstreams.lock.json']:shutil.copy(root/n,out/n)
(out/'apk').mkdir();(out/'icon').mkdir()
def copy(x):
 e=x['entry']
 for rel,url,sha in [('apk/'+e['apk'],x['apk_url'],x['sha256']),('icon/'+e['pkg']+'.png',x['icon_url'],x['icon_sha256'])]:
  require('..' not in pathlib.PurePosixPath(rel).parts,'Unsafe path')
  dst=out/rel;cached=root/rel
  if cached.is_file() and digest(cached)==sha:shutil.copy(cached,dst)
  else:
   require(url.startswith('https://raw.githubusercontent.com/'),'Unexpected origin')
   with urllib.request.urlopen(url,timeout=60) as response:dst.write_bytes(response.read())
  require(digest(dst)==sha,'Upstream bytes changed: '+url)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:list(ex.map(copy,lock['extensions']))
e=[x['entry'] for x in lock['extensions']]
(out/'index.min.json').write_text(json.dumps(e,separators=(',',':'),ensure_ascii=False)+'\n');(out/'index.json').write_text(json.dumps(e,indent=2,ensure_ascii=False)+'\n')
print('Built',len(e),'locked entries; run validate.py before publishing.')
