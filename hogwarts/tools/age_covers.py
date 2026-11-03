"""Ages the film posters into book covers that sit in the shelf photo:
    covers/N.jpg  ->  covers/aged/N.jpg   (600 x 900)
  grade   pulled toward the photo's warm candlelight: lifted blacks, softer highlights, less saturation
  haze    a soft bloom and a warm veil, like the air in the photo
  texture cloth-and-paper mottling, fine grain, a few scuffs, rubbed edges and corners
Baked here rather than done with CSS filters, so the TV only has to draw a plain image."""
import os
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
COV = os.path.join(HERE, "..", "covers")
OUT = os.path.join(COV, "aged")
os.makedirs(OUT, exist_ok=True)
W, H = 600, 900

# the photo's own look, measured off the old books on the shelf (left of the middle shelf)
shelf = cv2.imread(os.path.join(HERE, "..", "img", "shelf.jpg"))
sh, sw = shelf.shape[:2]
ref = cv2.cvtColor(shelf[int(sh * .37):int(sh * .63), int(sw * .06):int(sw * .21)], cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
ref_mean, ref_std = ref.mean(0), ref.std(0)


def fbm(h, w, cell, seed, octaves=4):
    rng = np.random.default_rng(seed)
    out, amp, tot = np.zeros((h, w), np.float32), 1.0, 0.0
    for o in range(octaves):
        c = max(2, int(cell / 2 ** o))
        g = rng.random((h // c + 2, w // c + 2)).astype(np.float32)
        out += amp * cv2.resize(g, (w + 2 * c, h + 2 * c), interpolation=cv2.INTER_CUBIC)[c:c + h, c:c + w]
        tot += amp; amp *= 0.5
    return out / tot


for i in range(1, 9):
    rng = np.random.default_rng(100 + i)
    img = cv2.resize(cv2.imread(os.path.join(COV, f"{i}.jpg")), (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255

    # 1. grade: part of the way toward the shelf photo's colour (Reinhard transfer in Lab), then a warm, low-contrast curve
    lab = cv2.cvtColor((img * 255).astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
    m, s = lab.reshape(-1, 3).mean(0), lab.reshape(-1, 3).std(0)
    moved = (lab - m) / (s + 1e-6) * (s * 0.75 + ref_std * 0.25) + (m * 0.55 + ref_mean * 0.45)
    moved[..., 0] = lab[..., 0] * 0.6 + moved[..., 0] * 0.4                  # keep most of the poster's own light and dark
    img = cv2.cvtColor(np.clip(moved, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32) / 255
    grey = img.mean(2, keepdims=True)
    img = grey + (img - grey) * 0.78                                         # a little less saturated
    img = 0.045 + img * 0.86                                                 # lifted blacks, softer whites
    img = img * np.array([0.80, 0.92, 1.0], np.float32)                      # BGR: warm, candle-lit

    # 2. haze: bloom from the bright parts, a warm veil, and a touch of softness
    bloom = cv2.GaussianBlur(np.clip(img - 0.45, 0, 1), (0, 0), 14)
    img = 1 - (1 - img) * (1 - bloom * 0.55)                                 # screen
    img = img * 0.92 + np.array([0.20, 0.27, 0.34], np.float32) * 0.08       # the veil
    img = cv2.GaussianBlur(img, (0, 0), 0.7)

    # 3. texture: mottled cloth/paper, fine grain, scuffs
    mott = fbm(H, W, 90, i) * 0.6 + fbm(H, W, 18, i + 50) * 0.4
    img *= (0.90 + 0.16 * mott)[..., None]
    weave = (np.sin(np.arange(W)[None, :] * 2.1) * np.sin(np.arange(H)[:, None] * 2.1)).astype(np.float32)
    img *= (1 + 0.018 * weave)[..., None]                                    # the faint cross-hatch of book cloth
    img += rng.normal(0, 0.022, (H, W, 1)).astype(np.float32)                # grain, same in all channels
    scuff = np.zeros((H, W), np.float32)
    for _ in range(14):                                                      # hairline scratches, mostly near the edges
        x0, y0 = rng.uniform(0, W), rng.uniform(0, H)
        ang, ln = rng.uniform(0, np.pi), rng.uniform(20, 90)
        cv2.line(scuff, (int(x0), int(y0)), (int(x0 + np.cos(ang) * ln), int(y0 + np.sin(ang) * ln)), float(rng.uniform(.3, .8)), 1, cv2.LINE_AA)
    scuff = cv2.GaussianBlur(scuff, (0, 0), 0.6) * (0.4 + 0.6 * (fbm(H, W, 120, i + 9) > 0.5))
    img = img + scuff[..., None] * 0.10

    # 4. wear: darker toward the edges, a rubbed lighter rim, softened corners
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.minimum.reduce([xx, W - 1 - xx, yy, H - 1 - yy])                  # distance to the nearest edge
    ragged = d + (fbm(H, W, 10, i + 20) - 0.5) * 10                          # edge wear isn't a clean line
    img *= (0.80 + 0.20 * np.clip(ragged / 42, 0, 1))[..., None]             # edges gather grime
    rim = np.exp(-((ragged - 3.5) / 2.2) ** 2) * (0.5 + 0.5 * fbm(H, W, 30, i + 30))
    img = img + rim[..., None] * np.array([0.10, 0.13, 0.16], np.float32)    # where the cover rubs, the colour wears off
    for cx, cy in ((0, 0), (W, 0), (0, H), (W, H)):                         # corners: the most worn
        cd = np.hypot(xx - cx, yy - cy)
        img = img + (np.exp(-(cd / 26) ** 2) * 0.12)[..., None] * np.array([0.7, 0.85, 1.0], np.float32)
    vig = ((xx / W - 0.42) ** 2 + (yy / H - 0.40) ** 2)                      # lit from the candle, up and to the left
    img *= (1.02 - 0.42 * vig)[..., None]

    cv2.imwrite(os.path.join(OUT, f"{i}.jpg"), (np.clip(img, 0, 1) * 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 90])
    print("aged", i)
