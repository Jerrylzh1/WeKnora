import os

LOG = r"d:/weknora-frontend-build4.log"
DIST = r"d:/AI-plat-form/01-githubcode/WeKnora/frontend/dist"

print("=== dist weknora png 资源 ===")
for root, _, files in os.walk(os.path.join(DIST, "assets")):
    for f in files:
        if "weknora" in f and f.lower().endswith(".png"):
            p = os.path.join(root, f)
            print(f"  {f}  {os.path.getsize(p)} bytes")

print("=== build log tail ===")
with open(LOG, encoding="utf-8", errors="replace") as fh:
    for ln in fh.read().splitlines()[-15:]:
        print(ln.encode("gbk", "ignore").decode("gbk"))
