#!/usr/bin/env python3
"""Report upstream changes for review. Does not change the lock or publish."""
import json,pathlib,urllib.request
root=pathlib.Path(__file__).resolve().parents[1];lock=json.loads((root/'upstreams.lock.json').read_text());report=[]
for owner,u in lock['upstreams'].items():
 url=f'https://raw.githubusercontent.com/{u["repository"]}/repo/index.min.json'
 try:
  with urllib.request.urlopen(url,timeout=60) as response:live=json.load(response)
  before={x['entry']['pkg']:x for x in lock['extensions'] if x['upstream']==owner}
  now={x['pkg']:x for x in live}
  report.append({'upstream':owner,'changed':[e for pkg,e in now.items() if pkg not in before or e!=before[pkg]['entry']],'removed':[pkg for pkg in before if pkg not in now],'action':'Review source license, APK signature, package and source-ID conflicts; update lock through a reviewed change. Never switch signer automatically.'})
 except Exception as e:report.append({'upstream':owner,'error':str(e)})
print(json.dumps(report,indent=2))
