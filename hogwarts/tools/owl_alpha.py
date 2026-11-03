"""Turns a generated owl clip into a see-through WebM (the input to owl_sprites.py):
    python owl_alpha.py NAME [trim_start trim_end]
  reads  owl/src/NAME.mp4        the clip as generated (owl on a flat slate background)
         owl/src/NAME_nobg.mp4   the same clip from the background remover (owl on pure black, no alpha channel)
  writes owl/NAME.webm           VP9 with alpha, same size as the clip, 24 fps
The remover's black is exact, so "not black" is the owl's silhouette; small enclosed gaps (eyes, beak, between
the talons) are filled, big ones are left alone, so background boxed in by a wing never turns solid.
The colour comes from the original clip."""
import os, re, subprocess, sys
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OWL = os.path.join(HERE, "..", "owl")
_ffp = os.path.join(HERE, "..", "..", "tools", "ffmpeg-path")        # a pinned ffmpeg, if you keep one there; else the one on PATH
FF = open(_ffp).read().strip() if os.path.exists(_ffp) else "ffmpeg"
name = sys.argv[1]
t0, t1 = (float(sys.argv[2]), float(sys.argv[3])) if len(sys.argv) > 3 else (0, 1e9)
src_path, cut_path = os.path.join(OWL, "src", name + ".mp4"), os.path.join(OWL, "src", name + "_nobg.mp4")
W, H = map(int, re.search(r", (\d+)x(\d+)", subprocess.run([FF, "-hide_banner", "-i", src_path], capture_output=True, text=True).stderr).groups())


def frames(path):
    p = subprocess.Popen([FF, "-v", "error", "-i", path, "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)


enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", "24", "-i", "-",
                        "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "24", "-auto-alt-ref", "0", "-row-mt", "1",
                        os.path.join(OWL, name + ".webm")], stdin=subprocess.PIPE)
ry, rx = np.minimum(np.arange(H), np.arange(H)[::-1]), np.minimum(np.arange(W), np.arange(W)[::-1])
edge = lambda r: (lambda e: e * e * (3 - 2 * e))(np.clip(r / 30, 0, 1))
EDGE = (edge(ry)[:, None] * edge(rx)[None, :]).astype(np.float32)   # anything touching the frame edge fades out
HOLE = 0.004 * W * H                                                  # gaps smaller than this inside the owl get filled
kept = 0
for i, (src, cut) in enumerate(zip(frames(src_path), frames(cut_path))):
    if not (t0 <= i / 24 < t1):
        continue
    m = (cut.max(2) > 14).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))           # drop compression specks
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n > 1:                                                                    # keep the owl, not stray islands
        m = (lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(1 - m)
    for k in range(1, n):                                                        # small enclosed gaps -> owl
        x, y, w, h, area = st[k]
        if area < HOLE and x > 0 and y > 0 and x + w < W and y + h < H:
            m[lab == k] = 1
    a = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.1) * EDGE
    rgb = src.astype(np.float32) * np.array([0.93, 0.94, 0.97], np.float32)      # a touch dimmer and cooler, to sit in the night
    enc.stdin.write(np.dstack([rgb, a * 255]).clip(0, 255).astype(np.uint8).tobytes())
    kept += 1
enc.stdin.close(); enc.wait()
print(name, f"{W}x{H}", "frames", kept)
