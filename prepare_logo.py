# -*- coding: utf-8 -*-
"""Cut the LaborForce logo into a transparent mark and a transparent full lockup.

Usage: python -I prepare_logo.py brand/logo_source.webp brand/
"""
import sys
from PIL import Image

src, out_dir = sys.argv[1], sys.argv[2].rstrip('/\\')
im = Image.open(src).convert('RGB')


def unmatte(img):
    """Turn a logo drawn on white into RGBA by removing the white matte."""
    px = img.load()
    out = Image.new('RGBA', img.size)
    po = out.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            a = 255 - min(r, g, b)
            if a <= 6:
                po[x, y] = (0, 0, 0, 0)
                continue
            k = a / 255.0
            rr = max(0, min(255, round((r - 255 * (1 - k)) / k)))
            gg = max(0, min(255, round((g - 255 * (1 - k)) / k)))
            bb = max(0, min(255, round((b - 255 * (1 - k)) / k)))
            po[x, y] = (rr, gg, bb, a)
    return out


def crop_trim(img, box):
    part = unmatte(img.crop(box))
    bbox = part.getchannel('A').getbbox()
    return part.crop(bbox)


mark = crop_trim(im, (460, 90, 1060, 640))
full = crop_trim(im, (180, 90, 1360, 890))

mark_small = mark.resize((round(mark.width * 160 / mark.height), 160), Image.LANCZOS)
full_small = full.resize((640, round(full.height * 640 / full.width)), Image.LANCZOS)
mark_small.save(f'{out_dir}/logo_mark.png', optimize=True)
full_small.save(f'{out_dir}/logo_full.png', optimize=True)
full.save(f'{out_dir}/logo_full_large.png', optimize=True)
print('mark', mark_small.size, 'full', full_small.size, 'large', full.size)
