#!/usr/bin/env python3
"""One-glance QC: grid of all existing chapter sheets, small thumbnails."""
import os, sys
from PIL import Image, ImageDraw, ImageFont

BOOK = "/home/z/my-project/manga/I am God"
FD = "/usr/share/fonts/truetype/dejavu"
F = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 22)

sheets = []
for ch in sorted(os.listdir(f"{BOOK}/chapters")):
    d = f"{BOOK}/chapters/{ch}"
    if not os.path.isdir(d):
        continue
    for f in sorted(os.listdir(d)):
        if f.startswith("sheet_") and f.endswith(".png"):
            sheets.append((ch, f, f"{d}/{f}"))

TW = 360
cols = 4
rows = (len(sheets) + cols - 1) // cols
th_h = int(TW * 1344 / 768 / 3)  # sheet aspect: 3 pages wide
cell_h = th_h + 34
W = cols * (TW + 12) + 12
H = rows * (cell_h + 12) + 12
canvas = Image.new("RGB", (W, H), (28, 28, 32))
d = ImageDraw.Draw(canvas)
for i, (ch, name, path) in enumerate(sheets):
    r, c = divmod(i, cols)
    x = 12 + c * (TW + 12)
    y = 12 + r * (cell_h + 12)
    try:
        im = Image.open(path).convert("RGB")
        im = im.resize((TW, int(im.size[1] * TW / im.size[0])))
        canvas.paste(im, (x, y + 28))
        d.text((x, y + 2), f"{ch} {name}", font=F, fill=(255, 220, 120))
    except Exception as e:
        d.text((x, y + 40), f"ERR {e}", font=F, fill=(255, 80, 80))
out = "/home/z/my-project/manga/I am God/references/qc_all_sheets.png"
canvas.save(out, quality=88)
print(out, canvas.size, f"{len(sheets)} sheets")
