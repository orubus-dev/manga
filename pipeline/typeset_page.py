#!/usr/bin/env python3
"""English typesetter for I am God manga pages.
Draws narration boxes, speech bubbles (say/roar/echo), tails and page numbers
onto generated 768x1344 page art. Zero text in generated art; all lettering here.
"""
import json, sys, os, math
from PIL import Image, ImageDraw, ImageFont

W, H = 768, 1344
FD = "/usr/share/fonts/truetype/dejavu"
F_BUB = ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 25)
F_BUB_B = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 26)
F_NARR = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 24)
F_PAGE = ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 18)

NARR_FILL = (243, 230, 200, 235)
NARR_TXT = (58, 42, 24)
NARR_BORDER = (120, 96, 60, 255)
ECHO_FILL = (232, 238, 244, 235)
ECHO_TXT = (52, 62, 74)
ECHO_BORDER = (128, 140, 155, 255)


def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def draw_narr(im, d, el):
    pad = 22
    maxw = int(el.get("w", 0.8) * W) - 2 * pad
    lines = wrap(d, el["t"], F_NARR, maxw)
    tw = max(d.textlength(l, font=F_NARR) for l in lines)
    th = len(lines) * 32
    bw, bh = int(tw + 2 * pad), th + 2 * pad - 6
    cx, cy = int(el["cx"] * W), int(el["cy"] * H)
    x0, y0 = cx - bw // 2, cy - bh // 2
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=12, fill=NARR_FILL,
                        outline=NARR_BORDER, width=3)
    y = y0 + pad - 6
    for l in lines:
        d.text((cx - d.textlength(l, font=F_NARR) // 2, y), l, font=F_NARR, fill=NARR_TXT)
        y += 32


def _ellipse_for(d, el, font):
    pad = 30
    maxw = int(el.get("w", 0.62) * W) - 2 * pad
    lines = wrap(d, el["t"], font, maxw)
    tw = max(d.textlength(l, font=font) for l in lines)
    th = len(lines) * 31
    return lines, int(tw + 2 * pad), th + 2 * pad - 8


def _stadium_for(d, el, font):
    pad = 28
    maxw = int(el.get("w", 0.62) * W) - 2 * pad
    lines = wrap(d, el["t"], font, maxw)
    tw = max(d.textlength(l, font=font) for l in lines)
    th = len(lines) * 31
    return lines, int(tw + 2 * pad), th + 2 * pad


def draw_bubble(im, d, el):
    kind = el.get("kind", "say")
    font = F_BUB_B if kind in ("roar",) else F_BUB
    lines, tw, th = _stadium_for(d, el, font)
    bw, bh = int(tw), int(th)
    cx, cy = int(el["cx"] * W), int(el["cy"] * H)
    if kind == "roar":
        pts = []
        n = 22
        for i in range(n * 2):
            ang = math.pi * 2 * i / (n * 2)
            rr = 1.0 if i % 2 == 0 else 0.82
            pts.append((cx + math.cos(ang) * bw / 2 * rr,
                        cy + math.sin(ang) * bh / 2 * rr))
        d.polygon(pts, fill=(255, 255, 255, 248), outline=(20, 20, 20, 255))
    else:
        fill = (255, 255, 255, 248) if kind != "echo" else ECHO_FILL
        outline = (25, 25, 25, 255) if kind != "echo" else ECHO_BORDER
        # stadium (stadium = rounded rect with half-height radius): no text overflow
        d.rounded_rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2],
                            radius=bh / 2, fill=fill, outline=outline, width=3)
    if kind != "echo":
        tail = el.get("tail")
        if tail:
            tx, ty = int(tail[0] * W), int(tail[1] * H)
            vx, vy = tx - cx, ty - cy
            n = math.hypot(vx, vy) or 1
            px, py = cx + vx / n * (bh / 2 - 4), cy + vy / n * (bh / 2 - 4)
            ox, oy = -vy / n, vx / n
            d.polygon([(px + ox * 16, py + oy * 16), (px - ox * 16, py - oy * 16),
                       (tx, ty)], fill=(255, 255, 255, 255), outline=(25, 25, 25, 255))
    y = cy - th / 2 + 6
    for l in lines:
        d.text((cx - d.textlength(l, font=font) / 2, y), l, font=font, fill=(20, 20, 20))
        y += 31


def typeset_page(src, elements, out, page_no=None, chapter_tag=""):
    im = Image.open(src).convert("RGBA")
    if im.size != (W, H):
        im = im.resize((W, H))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for el in elements:
        if el.get("type") == "bub" or "kind" in el:
            draw_bubble(im, d, el)
        else:
            draw_narr(im, d, el)
    if page_no is not None:
        label = f"{chapter_tag}  ·  {page_no}" if chapter_tag else str(page_no)
        tw = d.textlength(label, font=F_PAGE)
        d.text(((W - tw) / 2, H - 34), label, font=F_PAGE, fill=(235, 235, 235, 220))
    Image.alpha_composite(im, ov).convert("RGB").save(out, quality=95)


if __name__ == "__main__":
    src, els_json, out = sys.argv[1], sys.argv[2], sys.argv[3]
    page_no = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] != "-" else None
    tag = sys.argv[5] if len(sys.argv) > 5 else ""
    typeset_page(src, json.loads(els_json), out, page_no, tag)
    print("typeset ->", out)
