# -*- coding: utf-8 -*-
"""Render the web deck's slides into the PDF that "Print report" opens.

Usage (with the deck served on http://localhost:8765):
    python -I render_web_pdf.py http://localhost:8765/index.html LaborForce_Print.pdf

Each slide is opened in headless Edge at index.html?export#<slide-id> (no header
or navigation, slide at 1440x850, reduced motion so animations sit at rest),
captured at 2x, and the captures are joined into one landscape PDF.
Rebuild index.html afterwards so the new PDF is embedded.
"""
import os
import re
import subprocess
import sys
import tempfile

from PIL import Image

Image.init()  # register the JPEG writer the PDF plugin needs

EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
url, out_pdf = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(here, 'index.html'), encoding='utf-8') as fh:
    slide_ids = re.findall(r'<section class="report-section[^"]*" id="([^"]+)"', fh.read())

pages = []
with tempfile.TemporaryDirectory() as tmp:
    for n, sid in enumerate(slide_ids):
        shot = os.path.join(tmp, f'{n:02d}.png')
        subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                        '--force-prefers-reduced-motion', '--window-size=1440,850',
                        '--force-device-scale-factor=2', '--virtual-time-budget=4000',
                        '--user-data-dir=' + os.path.join(tmp, 'profile'),
                        '--screenshot=' + shot, f'{url}?export&n={n}#{sid}'],
                       check=True, capture_output=True, timeout=120)
        im = Image.open(shot).convert('RGB')
        pages.append(im.resize((2160, round(im.height * 2160 / im.width)), Image.LANCZOS))
        print(sid, pages[-1].size)

pages[0].save(out_pdf, save_all=True, append_images=pages[1:], resolution=162, quality=82,
              title='LaborForce Medical Management', author='LaborForce Medical Management')
if len(sys.argv) > 3:  # optional: folder for a contact sheet of the pages
    w, h = pages[0].size
    sheet = Image.new('RGB', (w * 2, h * ((len(pages) + 1) // 2)), 'white')
    for i, im in enumerate(pages):
        sheet.paste(im, ((i % 2) * w, (i // 2) * h))
    sheet.resize((sheet.width // 4, sheet.height // 4)).save(os.path.join(sys.argv[3], 'print_pdf_sheet.png'))
print('wrote', out_pdf, os.path.getsize(out_pdf), 'bytes,', len(pages), 'pages')
