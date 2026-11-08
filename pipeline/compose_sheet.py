#!/usr/bin/env python3
"""Compose a 3-up manga sheet: title bar + 3 typeset pages side by side."""
import sys
from PIL import Image, ImageDraw, ImageFont

FD = "/usr/share/fonts/truetype/dejavu"
F_TITLE = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 34)
F_SUB = ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 22)
BAR, GAP = 76, 10


def compose(page_paths, out, title, subtitle):
    pages = [Image.open(p).convert("RGB") for p in page_paths]
    pw, ph = pages[0].size
    W = len(pages) * pw + (len(pages) + 1) * GAP
    H = BAR + ph + GAP
    sheet = Image.new("RGB", (W, H), (16, 15, 18))
    d = ImageDraw.Draw(sheet)
    d.rectangle([0, 0, W, BAR], fill=(24, 22, 27))
    d.text((GAP + 4, 12), title, font=F_TITLE, fill=(242, 232, 210))
    tw = d.textlength(subtitle, font=F_SUB)
    d.text((W - tw - GAP - 4, 26), subtitle, font=F_SUB, fill=(180, 170, 150))
    for i, pg in enumerate(pages):
        sheet.paste(pg, (GAP + i * (pw + GAP), BAR))
        d.text((GAP + i * (pw + GAP) + 6, BAR + 8), f"P{i+1}",
               font=F_SUB, fill=(255, 255, 255, 200))
    sheet.save(out, quality=95)
    print("sheet ->", out, sheet.size)


if __name__ == "__main__":
    pages = sys.argv[1:4]
    out, title, subtitle = sys.argv[4], sys.argv[5], sys.argv[6]
    compose(pages, out, title, subtitle)
