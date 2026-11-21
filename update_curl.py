#!/usr/bin/env python3
# update_curl.py — rode na raiz do UZDoom. Sem build/commit.
import hashlib, io, shutil, urllib.request, zipfile
from pathlib import Path
ROOT = Path.cwd(); VER = "8.23.0_9"
PKG = {
  "x64":  ("win64-mingw",  "89cb71930f4242d884e8e349463455932ab1d089b20f4f99318261a3cbff9167"),
  "arm64":("win64a-mingw", "2d95c0b751001739f66723a4b56716d13a86755e44c3bdd17a39ffa4bc87913d"),
}
for arch,(suffix,sha) in PKG.items():
    name=f"curl-{VER}-{suffix}.zip"
    with urllib.request.urlopen(f"https://curl.se/windows/dl-{VER}/{name}", timeout=180) as r:
        data=r.read()
    assert hashlib.sha256(data).hexdigest()==sha, f"SHA256 incorreto: {name}"
    z=zipfile.ZipFile(io.BytesIO(data))
    roots={n.split("/")[0] for n in z.namelist()}; assert len(roots)==1
    root=roots.pop(); dst=ROOT/"bin/windows/curl"/arch
    inc=dst/"include/curl"
    if inc.exists(): shutil.rmtree(inc)
    inc.mkdir(parents=True); n=0
    for m in z.infolist():
        if m.is_dir(): continue
        rel=m.filename[len(root)+1:]
        if rel.startswith("include/curl/") and rel.endswith(".h"):
            (inc/Path(rel).name).write_bytes(z.read(m)); n+=1
        elif rel=="lib/libcurl.dll.a":
            (dst/"lib").mkdir(exist_ok=True); (dst/"lib/libcurl.dll.a").write_bytes(z.read(m))
        elif rel in ("BUILD-HASHES.txt","BUILD-MANIFEST.txt","COPYING.txt"):
            (dst/rel).write_bytes(z.read(m))
    assert n>=12 and (dst/"lib/libcurl.dll.a").exists()
    print(f"curl {arch}: {VER} ok ({n} headers)")
ci=ROOT/".github/workflows/continuous_integration.yml"
t=ci.read_bytes().decode("utf-8")
old_sha="d290b4ee475968b04dcb2e0c4f046f2ff25c35c65d3e54259cef7cc6cea069e2"
old_url="https://curl.se/windows/dl-8.20.0_5/curl-8.20.0_5-win64-mingw.zip"
new_url=f"https://curl.se/windows/dl-{VER}/curl-{VER}-win64-mingw.zip"
assert t.count(old_sha)==1 and t.count(old_url)==1
ci.write_bytes(t.replace(old_sha,PKG["x64"][1]).replace(old_url,new_url).encode("utf-8"))
print("CI libcurl.zip ->", new_url)