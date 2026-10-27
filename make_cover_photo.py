"""Pre-fade brand/hospital_cover.jpg for the PPTX cover (mirrors the CSS mask on .cover-photo).

The photo sits in the top-right corner (64% x 68% of the slide) and fades to transparent toward
the left (opaque from 52% of the width) and toward the bottom (opaque from 48% up).
Output: brand/hospital_cover_faded.png with an alpha channel, cropped to the slide box aspect.
"""
from PIL import Image
import numpy as np

SRC = "brand/hospital_cover.jpg"
OUT = "brand/hospital_cover_faded.png"
BOX_W, BOX_H = 13.333 * 0.64, 7.5 * 0.68   # inches on the slide (64% x 68%), top-right corner
POS_X, POS_Y = 0.62, 0.80          # CSS object-position

im = Image.open(SRC).convert("RGB")
sw, sh = im.size
aspect = BOX_W / BOX_H
if sw / sh > aspect:               # too wide -> crop width
    cw, ch = int(round(sh * aspect)), sh
else:                              # too tall -> crop height
    cw, ch = sw, int(round(sw / aspect))
x0 = int(round((sw - cw) * POS_X)); y0 = int(round((sh - ch) * POS_Y))
im = im.crop((x0, y0, x0 + cw, y0 + ch))
w, h = im.size

xs = np.linspace(0, 1, w)[None, :]
ys = np.linspace(0, 1, h)[:, None]
right = np.clip(xs / 0.52, 0, 1)                 # transparent at left -> opaque at 52%
up = np.clip((1 - ys) / 0.48, 0, 1)              # transparent at bottom -> opaque 48% up
alpha = (right * up)
# ease the ramps a little so the edge does not read as a straight line
alpha = alpha ** 1.15
a = Image.fromarray((alpha * 255).astype("uint8"), "L")
im.putalpha(a)
im.save(OUT, optimize=True)
print(OUT, im.size)
