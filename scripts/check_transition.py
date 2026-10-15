#!/usr/bin/env python3
"""Fail closed on automatic signer switches or version regressions."""
import json,sys
old={x['entry']['pkg']:x for x in json.load(open(sys.argv[1]))['extensions']}
new=json.load(open(sys.argv[2]))['extensions']
for x in new:
 e=x['entry'];p=old.get(e['pkg'])
 if not p:continue
 if p['signers']!=x['signers']:raise SystemExit('Signer switch needs an explicit migration: '+e['pkg'])
 if e['code']<p['entry']['code']:raise SystemExit('Version code regression: '+e['pkg'])
 if float(e['version'].rsplit('.',1)[0])<float(p['entry']['version'].rsplit('.',1)[0]):raise SystemExit('API version regression: '+e['pkg'])
 if p['sha256']!=x['sha256'] and e['code']<=p['entry']['code']:raise SystemExit('Changed APK without versionCode increase: '+e['pkg'])
print('Signing continuity and version monotonicity passed')
