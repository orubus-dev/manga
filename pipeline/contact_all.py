#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build QC contact sheets: one grid image per chapter + one global overview."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "I am God")
CH = os.path.join(BOOK, "chapters")
TH_W = 240

def font(sz, bold=False):
    return ImageFont.truetype(os.path.join("/usr/share/fonts/truetype/dejavu",
                                           "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), sz)

def chapter_contact(ch_dir, ch_name):
    sheets = sorted(f for f in os.listdir(ch_dir) if f.startswith("sheet_") and f.endswith(".png"))
    if not sheets:
        return None
    thumbs = []
    for s in sheets:
        im = Image.open(os.path.join(ch_dir, s))
        r = TH_W / im.width
        thumbs.append((s, im.resize((TH_W, int(im.height * r)))))
    pad, label_h = 10, 34
    w = len(thumbs) * (TH_W + pad) + pad
    h = max(t.height for _, t in thumbs) + label_h + 2 * pad
    out = Image.new("RGB", (w, h), (18, 18, 24))
    dr = ImageDraw.Draw(out)
    dr.text((pad, 6), f"{ch_name}  ({len(thumbs)} sheets)", font=font(20, True), fill=(240, 240, 240))
    x = pad
    for name, t in thumbs:
        out.paste(t, (x, label_h))
        dr.text((x + 4, label_h + t.height + 2), name.replace(".png", ""), font=font(14), fill=(180, 180, 190))
        x += TH_W + pad
    p = os.path.join(ch_dir, f"contact_{ch_name}.png")
    out.save(p)
    return p

def main():
    made = []
    all_rows = []
    for ch in sorted(os.listdir(CH)):
        ch_dir = os.path.join(CH, ch)
        if not os.path.isdir(ch_dir):
            continue
        p = chapter_contact(ch_dir, ch)
        if p:
            made.append(p)
            im = Image.open(p)
            r = 300 / im.width
            all_rows.append((ch, im.resize((300, int(im.height * r)))))
    # global overview
    if all_rows:
        pad, label_h = 8, 26
        w = len(all_rows) * (300 + pad) + pad
        h = max(t.height for _, t in all_rows) + label_h + 2 * pad
        g = Image.new("RGB", (w, h), (10, 10, 14))
        dr = ImageDraw.Draw(g)
        dr.text((pad, 4), "I am God — all chapters", font=font(18, True), fill=(240, 240, 240))
        x = pad
        for name, t in all_rows:
            g.paste(t, (x, label_h))
            dr.text((x + 4, label_h + t.height + 2), name, font=font(13), fill=(180, 180, 190))
            x += 300 + pad
        gp = os.path.join(BOOK, "chapters", "contact_ALL.png")
        g.save(gp)
        made.append(gp)
    for m in made:
        print(m)

if __name__ == "__main__":
    main()
