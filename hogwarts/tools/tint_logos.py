"""Tints the white dock logos to the castle's candlelight, a little lighter than the lit windows:
    img/logos/icon_*.png  ->  img/logos/warm/icon_*.png
The window cores in castle.jpg measure about #e8a46e; lifted 30% toward white that's #F0C29C.
Multiplying keeps each logo's own shading (the fold in the N, the cut-out play arrow)."""
import glob, os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
LOGOS = os.path.join(HERE, "..", "img", "logos")
TINT = np.array([0xF0, 0xC2, 0x9C], np.float32) / 255
os.makedirs(os.path.join(LOGOS, "warm"), exist_ok=True)
for p in glob.glob(os.path.join(LOGOS, "icon_*.png")):
    a = np.asarray(Image.open(p).convert("RGBA")).astype(np.float32)
    a[..., :3] *= TINT
    Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGBA").save(os.path.join(LOGOS, "warm", os.path.basename(p)))
    print(os.path.basename(p))
