"""Crops the window-glow layers (img/windows_a/b.png, full frame and mostly empty) to the area that has any light,
so the TV only draws the castle's windows and their reflection, not a whole transparent screen:
    img/windows_a_crop.png, img/windows_b_crop.png   the lit part
    img/layers.js                                     window.WIN_CROP = [x, y, w, h] as fractions of the photo
Run after gen_layers.py."""
import json, os
import numpy as np
from PIL import Image

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img")
ims = [Image.open(os.path.join(IMG, f"windows_{k}.png")) for k in "ab"]
W, H = ims[0].size
a = np.maximum(*(np.asarray(im)[..., 3] for im in ims))
ys, xs = np.nonzero(a > 2)
pad = 8
x0, y0, x1, y1 = max(0, xs.min() - pad), max(0, ys.min() - pad), min(W, xs.max() + pad), min(H, ys.max() + pad)
for k, im in zip("ab", ims):
    im.crop((x0, y0, x1, y1)).save(os.path.join(IMG, f"windows_{k}_crop.png"), optimize=True)
rect = [round(x0 / W, 5), round(y0 / H, 5), round((x1 - x0) / W, 5), round((y1 - y0) / H, 5)]
with open(os.path.join(IMG, "layers.js"), "w") as f:
    f.write("window.WIN_CROP = " + json.dumps(rect) + ";   // x, y, w, h of windows_*_crop.png within the photo (tools/crop_windows.py)\n")
print("crop", (x0, y0, x1, y1), "of", (W, H), "=", round((x1 - x0) * (y1 - y0) / (W * H) * 100), "% of the frame")
