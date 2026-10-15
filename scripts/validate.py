#!/usr/bin/env python3
"""Validate the locked mirror. Requires Android SDK aapt and apksigner."""
import argparse, hashlib, json, os, pathlib, re, subprocess, concurrent.futures

def require(ok, message):
    if not ok: raise ValueError(message)

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def validate(root, tools):
    lock=json.loads((root/'upstreams.lock.json').read_text())
    entries=json.loads((root/'index.min.json').read_text())
    require(entries == json.loads((root/'index.json').read_text()), 'Indexes differ')
    require(entries == [x['entry'] for x in lock['extensions']], 'Index differs from reviewed lock')
    require(bool(entries), 'Refuse empty repository')
    meta=json.loads((root/'repo.json').read_text())['meta']
    for k in ['name','shortName','website','signingKeyFingerprint']: require(isinstance(meta[k],str) and bool(meta[k]), 'Invalid repo metadata '+k)
    require(meta['website'].startswith('https://'),'HTTPS website required')
    require(meta['signingKeyFingerprint']=='NOFINGERPRINT-Cryoflam3-nekoyomi-anime-extensions','Mixed-signer repository must require per-extension trust')
    packages=set();sourceids=set();apks=set()
    for x in lock['extensions']:
        e=x['entry'];require(x['license']=='Apache-2.0','License review needed')
        for k in ['name','pkg','apk','lang','version']: require(isinstance(e[k],str) and bool(e[k]),'Invalid '+k)
        require(re.fullmatch(r'[a-zA-Z0-9_.-]+\.apk',e['apk']), 'Unsafe APK filename')
        require(re.fullmatch(r'[A-Za-z0-9_.]+',e['pkg']), 'Unsafe package name')
        require(e['pkg'] not in packages and e['apk'] not in apks,'Duplicate package or APK')
        packages.add(e['pkg']);apks.add(e['apk'])
        require(type(e['code']) is int and 0<e['code']<=2147483647,'Invalid version code')
        require(re.fullmatch(r'\d+(?:\.\d+)+',e['version']) is not None,'Invalid version string')
        require(12<=float(e['version'].rsplit('.',1)[0])<=16,'Unsupported extension API')
        require(type(e['nsfw']) is int and e['nsfw'] in (0,1),'Invalid NSFW flag')
        require(type(e.get('torrent',0)) is int and e.get('torrent',0) in (0,1),'Invalid torrent flag')
        for s in e.get('sources') or []:
            sid=int(s['id']);require(-2**63<=sid<2**63,'Source ID outside Kotlin Long')
            require(sid not in sourceids,'Duplicate source ID');sourceids.add(sid)
            for k in ['name','lang','baseUrl']:require(isinstance(s[k],str),'Invalid source field '+k)
        u=lock['upstreams'][x['upstream']]
        require(re.fullmatch('[a-f0-9]{40}',x['upstream_commit']),'Unpinned commit')
        base=f'https://raw.githubusercontent.com/{u["repository"]}/{x["upstream_commit"]}'
        require(x['apk_url']==base+'/apk/'+e['apk'],'Unexpected APK origin')
        require(x['icon_url']==base+'/icon/'+e['pkg']+'.png','Unexpected icon origin')
        require((root/'licenses'/x['upstream']/'LICENSE').is_file(),'Missing upstream license')
    def apk_check(x):
        e=x['entry'];a=root/'apk'/e['apk'];icon=root/'icon'/(e['pkg']+'.png')
        require(digest(a)==x['sha256'],'APK hash mismatch '+e['pkg'])
        require(digest(icon)==x['icon_sha256'],'Icon hash mismatch '+e['pkg'])
        p=subprocess.run([str(tools/'apksigner'),'verify','--print-certs',str(a)],capture_output=True,text=True)
        require(p.returncode==0,'Invalid signature '+e['pkg'])
        signers=re.findall(r'certificate SHA-256 digest: ([a-f0-9]+)',p.stdout)
        require(signers==x['signers'],'Signer changed '+e['pkg'])
        badging=subprocess.check_output([str(tools/'aapt'),'dump','badging',str(a)],text=True)
        m=re.search(r"package: name='([^']+)' versionCode='([^']+)' versionName='([^']+)'",badging)
        require(m is not None and m.groups()==(e['pkg'],str(e['code']),e['version']),'APK metadata mismatch '+e['pkg'])
        require("uses-feature: name='tachiyomi.animeextension'" in badging,'Not an anime extension')
        xml=subprocess.check_output([str(tools/'aapt'),'dump','xmltree',str(a),'AndroidManifest.xml'],text=True)
        require('"tachiyomi.animeextension.class"' in xml,'Missing entrypoint metadata')
        m=re.search(r'"tachiyomi.animeextension.nsfw"[^\n]*\n\s*A: android:value[^=]*=\(type 0x10\)0x([0-9a-f]+)',xml)
        require((int(m[1],16) if m else 0)==e['nsfw'],'NSFW index differs from manifest')
        return e['pkg']
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex: list(ex.map(apk_check,lock['extensions']))
    return {'extensions':len(entries),'nsfw':sum(e['nsfw'] for e in entries),'standard':sum(e['nsfw']==0 for e in entries),'device_installation':'not-tested','source_loading':'not-tested','playback':'not-tested'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=pathlib.Path,default=pathlib.Path('.'));p.add_argument('--build-tools',type=pathlib.Path,required=True);a=p.parse_args()
    print(json.dumps(validate(a.root.resolve(),a.build_tools.resolve()),indent=2))
