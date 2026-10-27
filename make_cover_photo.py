"""Pre-fade brand/hospital_cover.jpg for the PPTX cover (mirrors the CSS mask on .cover-photo).

The HTML fades the photo to transparent toward the left (opaque from 58% of the width),
the top (opaque from 46% of the height) and the bottom (last ~21% of the height).
Output: brand/hospital_cover_faded.png with an alpha channel, cropped to the slide box aspect.
"""
from PIL import Image
import numpy as np

SRC = "brand/hospital_cover.jpg"
OUT = "brand/hospital_cover_faded.png"
BOX_W, BOX_H = 5.75, 5.55          # inches on the slide
POS_X, POS_Y = 0.30, 0.62          # CSS object-position

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
right = np.clip(xs / 0.58, 0, 1)                 # transparent at left -> opaque at 58%
down = np.clip(ys / 0.46, 0, 1)                  # transparent at top -> opaque at 46%
up = np.clip((1 - ys) / 0.21, 0, 1)              # transparent at bottom -> opaque 21% up
alpha = (right * down * up)
# ease the ramps a little so the edge does not read as a straight line
alpha = alpha ** 1.15
a = Image.fromarray((alpha * 255).astype("uint8"), "L")
im.putalpha(a)
im.save(OUT, optimize=True)
print(OUT, im.size)
