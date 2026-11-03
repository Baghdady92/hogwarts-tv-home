"""Packs the see-through owl clips (owl/*.webm from owl_alpha.py) into sprite sheets the page draws on a canvas:
    owl/idle.webp   every 2nd frame (12 fps; the idle is slow, so that's plenty)
    owl/hop.webp    every frame of hopwide.webm (24 fps; the wings move fast; the 16:9 take, where the wings stay in frame)
    owl/owl.js      window.OWL_SHEETS = { idle: {...}, hop: {...} }
Clips can differ in framing (the idle is square, the hop wide), so each is scaled until the standing owl is
OWL_H px tall, cropped to the space its wings ever use, and its feet's position in the cell is recorded.
A canvas behaves the same in every browser and on the TV's WebView, where see-through video is unreliable."""
import json, os, re, subprocess
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OWL = os.path.join(HERE, "..", "owl")
_ffp = os.path.join(HERE, "..", "..", "tools", "ffmpeg-path")        # a pinned ffmpeg, if you keep one there; else the one on PATH
FF = open(_ffp).read().strip() if os.path.exists(_ffp) else "ffmpeg"
OWL_H = 150                                     # the standing owl's height in every sheet, px

meta = {}
for name, clip, every, fps in (("idle", "idle", 2, 12), ("hop", "hopwide", 1, 24)):
    path = os.path.join(OWL, clip + ".webm")
    W, H = map(int, re.search(r", (\d+)x(\d+)", subprocess.run([FF, "-hide_banner", "-c:v", "libvpx-vp9", "-i", path], capture_output=True, text=True).stderr).groups())
    raw = subprocess.run([FF, "-v", "error", "-c:v", "libvpx-vp9", "-i", path, "-f", "rawvideo", "-pix_fmt", "rgba", "-"], capture_output=True, check=True).stdout
    frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 4)[::every]
    ys, xs = np.nonzero(frames[0, ..., 3] > 128)                                 # the first frame: standing still
    k = OWL_H / (ys.max() - ys.min())
    feet = xs[ys > ys.max() - 0.04 * (ys.max() - ys.min())]
    foot = (feet.mean() * k, ys.max() * k)
    used = (frames[..., 3] > 8).any(0)                                           # everywhere a wing ever reaches
    uy, ux = np.nonzero(used)
    x0, x1 = max(0, int(ux.min() * k) - 4), int(ux.max() * k) + 5
    y0, y1 = max(0, int(uy.min() * k) - 4), int(uy.max() * k) + 5
    cw, ch, n = x1 - x0, y1 - y0, len(frames)
    cols = max(1, min(n, 4000 // cw))
    rows = -(-n // cols)
    sheet = Image.new("RGBA", (cols * cw, rows * ch), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        im = Image.fromarray(f, "RGBA").resize((round(W * k), round(H * k)), Image.LANCZOS).crop((x0, y0, x1, y1))
        sheet.paste(im, ((i % cols) * cw, (i // cols) * ch))
    sheet.save(os.path.join(OWL, name + ".webp"), quality=84, method=6)
    meta[name] = {"src": f"owl/{name}.webp", "n": n, "cols": cols, "cw": cw, "ch": ch, "fps": fps,
                  "footX": round(foot[0] - x0, 1), "footY": round(foot[1] - y0, 1)}
    print(name, n, "frames, cell", cw, "x", ch, "sheet", sheet.size, os.path.getsize(os.path.join(OWL, name + ".webp")) // 1024, "KB", meta[name])

with open(os.path.join(OWL, "owl.js"), "w") as f:
    f.write("window.OWL_SHEETS = " + json.dumps(meta) + ";\n")
