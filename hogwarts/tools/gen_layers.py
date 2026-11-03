"""Effect layers for the Hogwarts home, made from the castle photo itself:
    img/castle.jpg       the backdrop at 2560 px (lighter than the 5 MB PNG)
    img/windows_a/b.png  the lit windows (and their reflections) only, split in two so they can flicker separately
    img/mist.png         a soft, tileable band of mist to drift across the lake
    img/shelf.jpg        the bookshelf backdrop at 2560 px
and prints each poster's average colour (for the book spines)."""
import os
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "..", "img")
COV = os.path.join(HERE, "..", "covers")

castle = Image.open(os.path.join(IMG, "castle.png")).convert("RGB")
castle = castle.resize((2560, round(2560 * castle.height / castle.width)), Image.LANCZOS)
castle.save(os.path.join(IMG, "castle.jpg"), quality=90)
a = np.asarray(castle).astype(np.float32) / 255
r, g, b = a[..., 0], a[..., 1], a[..., 2]
lum = 0.3 * r + 0.59 * g + 0.11 * b
warm = np.clip((r - b) * 2.2, 0, 1)                      # orange window light, not the blue moonlight
m = np.clip((lum - 0.22) / 0.35, 0, 1) * warm
m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32) / 255
glow = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9))).astype(np.float32) / 255
alpha = np.clip(m * 0.9 + glow * 0.8, 0, 1)
col = np.dstack([np.ones_like(m) * 1.0, np.ones_like(m) * 0.72, np.ones_like(m) * 0.36])     # candle orange
H, W = m.shape
for name, half in (("windows_a", 0), ("windows_b", 1)):
    # interleave by vertical stripes so neighbouring windows flicker out of step
    stripes = ((np.arange(W) // 37) % 2 == half)[None, :].astype(np.float32)
    rgba = np.dstack([col, alpha * stripes])
    Image.fromarray((rgba * 255).astype(np.uint8), "RGBA").save(os.path.join(IMG, name + ".png"))
print("windows: lit pixels", int((m > 0.3).sum()))

# mist: soft fbm band, tileable left-right
rng = np.random.default_rng(5)
def noise(h, w, cy, cx, seed):
    rr = np.random.default_rng(seed)
    gy, gx = int(np.ceil(h / cy)) + 2, int(np.ceil(w / cx))
    grid = rr.random((gy, gx)); grid = np.concatenate([grid, grid[:, :1]], 1)     # wrap horizontally
    y, x = np.arange(h) / cy, np.arange(w) / cx
    y0, x0 = y.astype(int), x.astype(int); fy, fx = y - y0, x - x0
    sy, sx = fy * fy * (3 - 2 * fy), fx * fx * (3 - 2 * fx)
    x1 = (x0 + 1) % gx
    A, B, C, D = grid[y0][:, x0 % gx], grid[y0][:, x1], grid[y0 + 1][:, x0 % gx], grid[y0 + 1][:, x1]
    top = A + (B - A) * sx; bot = C + (D - C) * sx
    return top + (bot - top) * sy[:, None]
mh, mw = 360, 2048
f = sum(noise(mh, mw, 120 / 2 ** o, 2048 / 8 / 2 ** o, 50 + o) * 0.5 ** o for o in range(4)) / 1.875
band = np.exp(-((np.arange(mh) - mh * 0.55) / (mh * 0.22)) ** 2)[:, None]
ma = np.clip((f - 0.35) * 1.8, 0, 1) * band
mist = np.dstack([np.full_like(ma, 0.80), np.full_like(ma, 0.86), np.full_like(ma, 0.92), ma * 0.55])
Image.fromarray((mist * 255).astype(np.uint8), "RGBA").save(os.path.join(IMG, "mist.png"))

shelf = Image.open(os.path.join(IMG, "shelf.png")).convert("RGB")
shelf.resize((2560, round(2560 * shelf.height / shelf.width)), Image.LANCZOS).save(os.path.join(IMG, "shelf.jpg"), quality=90)

# spine colours: each poster's mean colour, darkened like old leather
for i in range(1, 9):
    p = np.asarray(Image.open(os.path.join(COV, f"{i}.jpg")).convert("RGB").resize((40, 60))).astype(np.float32)
    c = p.reshape(-1, 3).mean(0) * 0.55
    print(i, "#%02x%02x%02x" % tuple(int(v) for v in c))
