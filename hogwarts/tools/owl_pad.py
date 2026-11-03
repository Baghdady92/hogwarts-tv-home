"""Puts the chosen owl still on a wider, taller 16:9 canvas so a generated hop has room for its wingbeats:
    owl/src/still_1.png (1024 x 1024)  ->  owl/src/still_wide.png (1920 x 1080)
The owl is scaled to about 30% of the frame height with its feet at 80%; the backdrop is extended from the
still's own (almost flat) background, row by row, so the owl itself stays pixel-identical to the idle clip."""
import os
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "owl", "src")
still = cv2.imread(os.path.join(SRC, "still_1.png")).astype(np.float32)
S = still.shape[0]
W, H = 1920, 1080
FOOT = (0.461, 0.846)                           # where its feet are in the still
k = 0.30 * H / (0.469 * S)                      # owl height: 47% of the still -> 30% of the new frame
size = round(S * k)
left, top = round(W / 2 - FOOT[0] * size), round(0.80 * H - FOOT[1] * size)

# the backdrop, one colour per row, read from the still's empty left and right edges
side = np.concatenate([still[:, :120], still[:, -120:]], 1)
rows = np.median(side, 1)                                        # S x 3
rows = cv2.GaussianBlur(rows[:, None, :], (1, 0), sigmaX=0.1, sigmaY=6)[:, 0, :]
src_row = np.clip(((np.arange(H) - top) / k).round().astype(int), 0, S - 1)
canvas = np.repeat(rows[src_row][:, None, :], W, 1)
canvas += np.random.default_rng(1).normal(0, 1.6, canvas.shape)   # the still's own fine grain

small = cv2.resize(still, (size, size), interpolation=cv2.INTER_AREA)
r = np.minimum(np.arange(size), np.arange(size)[::-1]) / 60
feather = np.clip(np.minimum(r[None, :], r[:, None]), 0, 1)[..., None]
feather = feather * feather * (3 - 2 * feather)
region = canvas[top:top + size, left:left + size]
canvas[top:top + size, left:left + size] = region * (1 - feather) + small * feather
cv2.imwrite(os.path.join(SRC, "still_wide.png"), np.clip(canvas, 0, 255).astype(np.uint8))
print("owl", size, "px at", left, top, "-> feet at", W / 2, 0.8 * H)
