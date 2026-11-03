"""Copies the castle home into the TV app (hogwarts-tv/app/src/main/assets/www), sized for a 1080p TV:
  - the page, its scripts, the logos, the aged covers, the mist, as they are
  - the three backdrops and the window glow at 1936 px wide (the screen shows them 1935 px wide), not 2560,
    with the page's static shading (#hshade, #lvig, #gvig) baked in: the TV hides those layers to save drawing
  - the owl's frames at the size it's drawn (a 128 px owl), each trimmed to its own outline and packed tightly
    (a fixed grid wastes most of each cell on empty air around the wings: ~46 MB decoded, which pushed the photos
    out of the TV's image memory and made them re-decode mid-scroll), with owl.js listing where each frame is
  - the book covers at 400 x 600 (they're never shown bigger than ~230 x 345)
Run by build.sh before the APK is built."""
import json, os, re, shutil, subprocess, sys, tempfile
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.normpath(os.path.join(SRC, "..", "hogwarts-tv", "app", "src", "main", "assets", "www"))
WIDE = 1936
OWL_H = 128                                      # matches OWL_H in index.html

# never ship a page whose script doesn't parse: on the TV that's a frozen screen
page = open(os.path.join(SRC, "index.html")).read()
inline = [m for m in re.findall(r"<script>(.*?)</script>", page, re.S)]
with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as js:
    js.write("\n".join(inline))
try:
    check = subprocess.run(["node", "--check", js.name], capture_output=True, text=True)
except FileNotFoundError:
    check = None
    print("node not found: skipping the script check")
os.unlink(js.name)
if check and check.returncode:
    sys.exit("index.html has a script error, not building:\n" + check.stderr)

shutil.rmtree(OUT, ignore_errors=True)
for d in ("img/logos/warm", "covers/aged", "owl"):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)


def copy(rel):
    shutil.copy2(os.path.join(SRC, rel), os.path.join(OUT, rel))


for rel in ["index.html", "config.js", "img/points.js", "img/layers.js", "img/mist.png"] + \
           [f"img/logos/warm/{f}" for f in os.listdir(os.path.join(SRC, "img/logos/warm")) if f.endswith(".png")]:
    copy(rel)
for i in range(1, 9):
    Image.open(os.path.join(SRC, f"covers/aged/{i}.jpg")).resize((400, 600), Image.LANCZOS).save(os.path.join(OUT, f"covers/aged/{i}.jpg"), quality=88)


def ramp(t, stops):                              # a CSS gradient's alpha along t, from (position, alpha) stops
    return np.interp(t, [p for p, _ in stops], [a for _, a in stops])


def radial(X, Y, cx, cy, rx, ry, stops):         # CSS radial-gradient(ellipse rx ry at cx cy, ...), alpha only
    return ramp(np.hypot((X - cx) / rx, (Y - cy) / ry), stops)


def shaded(im, alphas):
    """Black layers over the picture, as the browser stacks them (X, Y = screen position as 0..1)."""
    a = np.asarray(im).astype(np.float32)
    h, w = a.shape[:2]
    X = ((np.arange(w) + 0.5) / w * 1935 - 7.5) / 1920       # where each column lands on screen (photoBox: 1935 px, 7.5 px off the left)
    Y = (np.arange(h) + 0.5) / h
    X, Y = np.meshgrid(X, Y)
    keep = np.ones_like(X)
    for f in alphas:
        keep *= 1 - f(X, Y)
    return Image.fromarray((a * keep[..., None]).clip(0, 255).astype(np.uint8))


BAKE = {   # the same gradients as #hshade, #lvig and #gvig in index.html
    "img/castle.jpg": [lambda X, Y: ramp(Y, [(0, .30), (.16, 0), (.52, 0), (.66, .30), (.80, .62), (1, .80)]),
                       lambda X, Y: radial(X, Y, .55, .45, .80, .70, [(0, 0), (.60, 0), (1, .45), (9, .45)])],
    "img/shelf.jpg": [lambda X, Y: radial(X, Y, .51, .50, .80, .75, [(0, 0), (.58, 0), (1, .50), (9, .50)])],
    "img/greenhouse_beasts.jpg": [lambda X, Y: ramp(Y, [(0, .25), (.20, 0), (.70, 0), (1, .55)])],
}
for rel, alphas in BAKE.items():
    im = Image.open(os.path.join(SRC, rel)).convert("RGB")
    im = im.resize((WIDE, round(WIDE * im.height / im.width)), Image.LANCZOS)
    shaded(im, alphas).save(os.path.join(OUT, rel), quality=88)
for rel in ("img/windows_a_crop.png", "img/windows_b_crop.png"):
    im = Image.open(os.path.join(SRC, rel))
    k = WIDE / Image.open(os.path.join(SRC, "img/castle.jpg")).width
    im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS).save(os.path.join(OUT, rel), optimize=True)

meta = json.loads(re.search(r"=\s*(\{.*\});", open(os.path.join(SRC, "owl/owl.js")).read()).group(1))
def pack(sizes, width):
    """Shelf packing: tallest first, left to right, a new row when one is full. Returns positions and the height used."""
    order = sorted(range(len(sizes)), key=lambda i: -sizes[i][1])
    pos, x, y, row = [None] * len(sizes), 0, 0, 0
    for i in order:
        w, h = sizes[i]
        if x + w > width: x, y, row = 0, y + row, 0
        pos[i] = (x, y); x += w; row = max(row, h)
    return pos, y + row


for name, m in meta.items():
    k = OWL_H / m.get("owlH", 150)
    sheet = Image.open(os.path.join(SRC, m["src"]))
    cw, ch = round(m["cw"] * k), round(m["ch"] * k)
    pieces, rects = [], []
    for i in range(m["n"]):
        x, y = (i % m["cols"]) * m["cw"], (i // m["cols"]) * m["ch"]
        cell = sheet.crop((x, y, x + m["cw"], y + m["ch"])).resize((cw, ch), Image.LANCZOS)
        box = cell.getchannel("A").point(lambda a: 255 if a > 2 else 0).getbbox() or (0, 0, 1, 1)
        box = (max(0, box[0] - 1), max(0, box[1] - 1), min(cw, box[2] + 1), min(ch, box[3] + 1))
        pieces.append(cell.crop(box)); rects.append(box)
    sizes = [p.size for p in pieces]
    width = min((wd for wd in range(512, 4097, 64) if pack(sizes, wd)[1] <= 4096), key=lambda wd: wd * pack(sizes, wd)[1])
    pos, height = pack(sizes, width)
    out = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    frames = []
    for p, (px, py), box in zip(pieces, pos, rects):
        out.paste(p, (px, py))
        frames.append([px, py, p.width, p.height, box[0], box[1]])     # where it is in the sheet, where it goes in the cell
    out.save(os.path.join(OUT, m["src"]), quality=84, method=6)
    meta[name] = dict(m, cw=cw, ch=ch, footX=round(m["footX"] * k, 1), footY=round(m["footY"] * k, 1), owlH=OWL_H, frames=frames)
    print(name, "sheet", out.size, f"{width * height * 4 / 1e6:.1f} MB decoded (a grid would be {m['n'] * cw * ch * 4 / 1e6:.1f} MB)")
with open(os.path.join(OUT, "owl/owl.js"), "w") as f:
    f.write("window.OWL_SHEETS = " + json.dumps(meta) + ";\n")

size = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(OUT) for f in fs)
print("www:", round(size / 1e6, 1), "MB")
