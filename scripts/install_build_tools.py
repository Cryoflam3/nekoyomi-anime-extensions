#!/usr/bin/env python3
"""Install pinned official Android verification tools without relying on runner SDK paths."""
import hashlib,pathlib,sys,urllib.request,zipfile
out=pathlib.Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
archive=out/'build-tools.zip'
with urllib.request.urlopen('https://dl.google.com/android/repository/build-tools_r35_linux.zip',timeout=120) as response:archive.write_bytes(response.read())
if hashlib.sha256(archive.read_bytes()).hexdigest() != 'bd3a4966912eb8b30ed0d00b0cda6b6543b949d5ffe00bea54c04c81e1561d88':raise SystemExit('Android Build Tools checksum mismatch')
with zipfile.ZipFile(archive) as z:z.extractall(out)
for name in ['aapt','apksigner']:(out/'android-15'/name).chmod(0o755)
print(out/'android-15')
