#!/usr/bin/env python3
"""Build helper for NicoTV.

  python3 tools/build.py ipk
  python3 tools/build.py apk --base path/to/original-NicoTV.apk

ipk: packages ./webos into a webOS .ipk (pure Python, no SDK needed).
apk: takes an existing NicoTV APK (the Android WebView shell), swaps in
     ./android/www as assets/www, and signs
     it with a v1 (JAR) signature using OpenSSL. Needs `openssl` in PATH.
     The key is generated once into tools/key.pem + cert.pem (git-ignored).
"""
import argparse, base64, hashlib, io, os, struct, subprocess, tarfile, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")

def b64(b): return base64.b64encode(b).decode()

def ar_member(name, b):
    hdr = (name.ljust(16) + "0".ljust(12) + "0".ljust(6) + "0".ljust(6) + "100644".ljust(8) + str(len(b)).ljust(10) + "`\n").encode()
    return hdr + b + (b"\n" if len(b) % 2 else b"")

def tar_gz(entries):
    bio = io.BytesIO()
    with tarfile.open(fileobj=bio, mode="w:gz", format=tarfile.GNU_FORMAT) as t:
        for arc, path in entries:
            ti = t.gettarinfo(path, arc); ti.uid = ti.gid = 0; ti.uname = ti.gname = "root"
            t.addfile(ti, open(path, "rb")) if ti.isreg() else t.addfile(ti)
    return bio.getvalue()

def build_ipk():
    w = os.path.join(ROOT, "webos"); app = "./usr/palm/applications/com.nico.nicotv"
    files = [f for f in sorted(os.listdir(w)) if f not in ("control", "packageinfo.json")]
    ent = []
    for d in ("./usr", "./usr/palm", "./usr/palm/applications", app, "./usr/palm/packages", "./usr/palm/packages/com.nico.nicotv"):
        ent.append((d, None))
    bio = io.BytesIO()
    with tarfile.open(fileobj=bio, mode="w:gz", format=tarfile.GNU_FORMAT) as t:
        for d, _ in ent:
            ti = tarfile.TarInfo(d); ti.type = tarfile.DIRTYPE; ti.mode = 0o755; t.addfile(ti)
        for f in files:
            p = os.path.join(w, f); ti = t.gettarinfo(p, app + "/" + f); ti.uid = ti.gid = 0; ti.uname = ti.gname = "root"; t.addfile(ti, open(p, "rb"))
        p = os.path.join(w, "packageinfo.json"); ti = t.gettarinfo(p, "./usr/palm/packages/com.nico.nicotv/packageinfo.json"); ti.uid = ti.gid = 0; ti.uname = ti.gname = "root"; t.addfile(ti, open(p, "rb"))
    data = bio.getvalue()
    ctrl = tar_gz([("./control", os.path.join(w, "control"))])
    ver = [l.split(":")[1].strip() for l in open(os.path.join(w, "control")) if l.startswith("Version:")][0]
    os.makedirs(DIST, exist_ok=True)
    out = os.path.join(DIST, "com_nico_nicotv_%s_all.ipk" % ver.replace(".", "_"))
    open(out, "wb").write(b"!<arch>\n" + ar_member("debian-binary", b"2.0\n") + ar_member("control.tar.gz", ctrl) + ar_member("data.tar.gz", data))
    print("wrote", out)

def wrap(line):
    b = line.encode(); o = []; first = True
    while len(b) > (72 if first else 71):
        n = 72 if first else 71
        o.append(b[:n] if first else b" " + b[:n]); b = b[n:]; first = False
    o.append(b if first else b" " + b)
    return b"\r\n".join(o) + b"\r\n"

def build_apk(base):
    zin = zipfile.ZipFile(base); www = os.path.join(ROOT, "android", "www"); files = []
    for i in zin.infolist():
        if i.filename.startswith("META-INF/") or i.filename.startswith("assets/www/"): continue
        d = zin.read(i.filename)
        files.append((i, d))
    for f in sorted(os.listdir(www)):
        zi = zipfile.ZipInfo("assets/www/" + f, date_time=(1980, 1, 1, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED
        files.append((zi, open(os.path.join(www, f), "rb").read()))
    mf = b"Manifest-Version: 1.0\r\nCreated-By: 1.0 (Android)\r\n\r\n"; sec = {}
    for i, d in files:
        if i.filename.endswith("/"): continue
        s = wrap("Name: " + i.filename) + ("SHA-256-Digest: " + b64(hashlib.sha256(d).digest()) + "\r\n\r\n").encode()
        sec[i.filename] = s; mf += s
    sf = ("Signature-Version: 1.0\r\nCreated-By: 1.0 (Android)\r\nSHA-256-Digest-Manifest: " + b64(hashlib.sha256(mf).digest()) + "\r\n\r\n").encode()
    for n, s in sec.items():
        sf += wrap("Name: " + n) + ("SHA-256-Digest: " + b64(hashlib.sha256(s).digest()) + "\r\n\r\n").encode()
    tools = os.path.join(ROOT, "tools"); key = os.path.join(tools, "key.pem"); crt = os.path.join(tools, "cert.pem")
    if not os.path.exists(key):
        subprocess.check_call(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-keyout", key, "-out", crt, "-days", "10000", "-subj", "/CN=NicoTV"], stderr=subprocess.DEVNULL)
    os.makedirs(DIST, exist_ok=True)
    tmp_sf = os.path.join(DIST, "CERT.SF"); open(tmp_sf, "wb").write(sf)
    rsa = subprocess.check_output(["openssl", "smime", "-sign", "-binary", "-noattr", "-outform", "DER", "-in", tmp_sf, "-signer", crt, "-inkey", key, "-md", "sha256"])
    os.remove(tmp_sf)
    out = os.path.join(DIST, "NicoTV-custom.apk")
    with zipfile.ZipFile(out, "w") as z:
        z.writestr("META-INF/MANIFEST.MF", mf); z.writestr("META-INF/CERT.SF", sf); z.writestr("META-INF/CERT.RSA", rsa)
        for i, d in files:
            zi = zipfile.ZipInfo(i.filename, date_time=i.date_time)
            zi.compress_type = zipfile.ZIP_STORED if (i.filename == "resources.arsc" or i.compress_type == 0) else zipfile.ZIP_DEFLATED
            zi.external_attr = i.external_attr; z.writestr(zi, d)
    print("wrote", out)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("target", choices=["ipk", "apk"])
    ap.add_argument("--base")
    a = ap.parse_args()
    if a.target == "ipk": build_ipk()
    else:
        if not a.base: ap.error("apk needs --base <original.apk>")
        build_apk(a.base)
