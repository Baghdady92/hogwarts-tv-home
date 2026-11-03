"""Points picked out of the castle photo, so the motion sits on what's really there:
    stars   the photo's own stars (small bright dots in the open sky), to twinkle
    glints  bright spots in the castle's reflection on the lake, to shimmer
Writes img/points.js (a script, so the page also works straight from file://), all positions as fractions of the photo's width / height."""
import json, os
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "..", "img")

bgr = cv2.imread(os.path.join(IMG, "castle.jpg"))
H, W = bgr.shape[:2]
a = bgr[..., ::-1].astype(np.float32) / 255
lum = 0.3 * a[..., 0] + 0.59 * a[..., 1] + 0.11 * a[..., 2]

# stars: a white top-hat finds dots smaller than the kernel; keep the ones on dark open sky
top = cv2.morphologyEx(lum, cv2.MORPH_TOPHAT, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
around = cv2.blur(lum, (41, 41))
cand = (top > 0.06) & (around < 0.30)
cand[int(H * 0.20):] = False                                   # open sky only: above the spires and the ridges
n, lab, stats, cen = cv2.connectedComponentsWithStats(cand.astype(np.uint8))
moon = (W * 0.352, H * 0.279)
stars = []
for i in range(1, n):
    x, y = cen[i]
    if stats[i, cv2.CC_STAT_AREA] > 14 or np.hypot(x - moon[0], y - moon[1]) < W * 0.05:
        continue
    stars.append([round(x / W, 4), round(y / H, 4), round(float(top[int(y), int(x)]), 3)])
stars.sort(key=lambda s: -s[2])
stars = stars[:140]

# glints: warm light in the water (the windows' reflection), below the far shore
warm = np.clip((a[..., 0] - a[..., 2]) * 2.2, 0, 1)
m = np.clip((lum - 0.18) / 0.35, 0, 1) * warm
ys, xs = np.nonzero(m[int(H * 0.76):] > 0.25)
ys = ys + int(H * 0.76)
rng = np.random.default_rng(3)
pick = rng.choice(len(xs), size=min(420, len(xs)), replace=False)
glints = [[round(xs[i] / W, 4), round(ys[i] / H, 4)] for i in pick]

with open(os.path.join(IMG, "points.js"), "w") as f:
    f.write("window.POINTS = " + json.dumps({"stars": stars, "glints": glints}, separators=(",", ":")) + ";\n")
print("stars", len(stars), "glints", len(glints), "of", len(xs))
