from PIL import Image
import os, shutil

SRC = r"d:/AI-plat-form/01-githubcode/WeKnora/frontend/src/assets/img/weknora.png"
BAK = r"d:/AI-plat-form/01-githubcode/WeKnora/frontend/src/assets/img/weknora-whitebg.png"

# 备份原白底图
if not os.path.exists(BAK):
    shutil.copy2(SRC, BAK)
    print("已备份原白底图 -> weknora-whitebg.png")

# 转 RGBA
im = Image.open(SRC).convert("RGBA")
px = im.load()
W, H = im.size

# 把接近白色的像素设为透明。阈值略低以清除抗锯齿浅灰边缘。
TH = 240
for y in range(H):
    for x in range(W):
        r, g, b, a = px[x, y]
        if r >= TH and g >= TH and b >= TH:
            px[x, y] = (r, g, b, 0)

# 轻微边缘羽化：对半透明边缘做 alpha 收缩，去除残白边
# 简单做法：对 alpha>0 且 <255 的像素，若 RGB 仍偏白则提升透明度
for y in range(H):
    for x in range(W):
        r, g, b, a = px[x, y]
        if 0 < a < 255 and r >= 225 and g >= 225 and b >= 225:
            px[x, y] = (r, g, b, max(0, a - 80))

out = os.path.join(os.path.dirname(SRC), "weknora.png")
im.save(out)
print(f"已生成透明背景 logo -> {out}  ({W}x{H})")

# 验证透明像素占比
transparent = sum(1 for y in range(H) for x in range(W) if px[x, y][3] == 0)
print(f"透明像素占比: {transparent/(W*H)*100:.1f}%")
