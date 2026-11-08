# -*- coding: utf-8 -*-
"""Programmatic typesetting for 'I am God' strips (English, DejaVu).
Overlays narration boxes / speech bubbles / page numbers on raw 768x1344 strip images.
Zero text ever goes through the image model."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 768, 1344
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
_F_OBL_CAND = os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf")
F_OBL = _F_OBL_CAND if os.path.exists(_F_OBL_CAND) else F_REG

def _font(size, bold=False, oblique=False):
    path = F_BOLD if bold else (F_OBL if oblique else F_REG)
    return ImageFont.truetype(path, size)

def _wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def _poly_bbox(cx, cy, tw, th):
    return [cx - tw / 2, cy - th / 2, cx + tw / 2, cy + th / 2]

def _tail(draw, bx0, by0, bx1, by1, tx, ty, color="black"):
    """Draw a triangle tail from bubble edge toward (tx,ty)."""
    import math
    mx, my = (bx0 + bx1) / 2, (by0 + by1) / 2
    dx, dy = tx - mx, ty - my
    d = math.hypot(dx, dy) or 1.0
    ux, uy = dx / d, dy / d
    # start point on ellipse edge approx
    sx = mx + ux * (bx1 - bx0) / 2 * 0.92
    sy = my + uy * (by1 - by0) / 2 * 0.92
    px, py = -uy, ux
    w_ = 14
    tipx, tipy = sx + ux * min(d * 0.55, 90), sy + uy * min(d * 0.55, 90)
    draw.polygon([(sx + px * w_, sy + py * w_), (sx - px * w_, sy - py * w_), (tipx, tipy)],
                 fill=color, outline=color)

def _clamp_cx(cx_px, tw):
    half = tw / 2
    return max(half + 12, min(W - half - 12, cx_px))

def draw_say(img, dr, text, cx, cy, tx=None, ty=None, bold=False):
    font = _font(24, bold=bold)
    max_tw = 560
    lines = _wrap(dr, text, font, max_tw)
    lh = font.size + 8
    tw = max(dr.textlength(l, font=font) for l in lines) + 72
    th = lh * len(lines) + 46
    cx = _clamp_cx(cx * W, tw); cy *= H
    b = _poly_bbox(cx, cy, tw, th)
    dr.ellipse(b, fill=(255, 255, 255, 245), outline=(20, 20, 20, 255), width=3)
    if tx is not None:
        _tail(dr, b[0], b[1], b[2], b[3], tx * W, ty * H)
        # redraw border over tail seam lightly
        dr.ellipse(b, outline=(20, 20, 20, 255), width=3)
    y = b[1] + (th - lh * len(lines)) / 2 + 4
    for l in lines:
        lw = dr.textlength(l, font=font)
        dr.text((cx - lw / 2, y), l, font=font, fill=(15, 15, 15, 255))
        y += lh

def draw_roar(img, dr, text, cx, cy, tx=None, ty=None):
    import math
    font = _font(27, bold=True)
    max_tw = 540
    lines = _wrap(dr, text, font, max_tw)
    lh = font.size + 8
    tw = max(dr.textlength(l, font=font) for l in lines) + 90
    th = lh * len(lines) + 70
    cx = _clamp_cx(cx * W, tw); cy *= H
    n = 22
    pts = []
    rx, ry = tw / 2, th / 2
    for i in range(n * 2):
        ang = math.pi * i / n
        r = 1.0 if i % 2 == 0 else 0.86
        pts.append((cx + math.cos(ang) * rx * r, cy + math.sin(ang) * ry * r))
    dr.polygon(pts, fill=(255, 255, 255, 248), outline=(20, 20, 20, 255))
    dr.polygon(pts, outline=(20, 20, 20, 255), width=3)
    if tx is not None:
        pass  # tails less critical on roar
    y = cy - th / 2 + 20
    for l in lines:
        lw = dr.textlength(l, font=font)
        dr.text((cx - lw / 2, y), l, font=font, fill=(10, 10, 10, 255))
        y += lh

def draw_echo(img, dr, text, cx, cy):
    font = _font(26, oblique=True)
    max_tw = 560
    lines = _wrap(dr, text, font, max_tw)
    lh = font.size + 8
    tw = max(dr.textlength(l, font=font) for l in lines) + 40
    th = lh * len(lines) + 28
    cx = _clamp_cx(cx * W, tw); cy *= H
    b = _poly_bbox(cx, cy, tw, th)
    dr.ellipse([b[0] - 7, b[1] - 7, b[2] + 7, b[3] + 7], outline=(255, 255, 255, 200), width=2)
    dr.ellipse(b, fill=(255, 255, 255, 235), outline=(60, 60, 70, 255), width=3)
    y = b[1] + (th - lh * len(lines)) / 2 + 2
    for l in lines:
        lw = dr.textlength(l, font=font)
        dr.text((cx - lw / 2, y), l, font=font, fill=(40, 40, 50, 255))
        y += lh

def draw_narration(img, dr, text, cx, cy):
    font = _font(23)
    max_tw = 620
    lines = _wrap(dr, text, font, max_tw)
    lh = font.size + 7
    tw = max(dr.textlength(l, font=font) for l in lines) + 36
    th = lh * len(lines) + 22
    cx = _clamp_cx(cx * W, tw); cy *= H
    b = [cx - tw / 2, cy - th / 2, cx + tw / 2, cy + th / 2]
    dr.rounded_rectangle(b, radius=8, fill=(12, 12, 18, 200), outline=(240, 240, 240, 210), width=2)
    y = b[1] + 11
    for l in lines:
        lw = dr.textlength(l, font=font)
        dr.text((cx - lw / 2, y), l, font=font, fill=(245, 245, 245, 255))
        y += lh

def draw_page_no(dr, label, page_idx):
    """page_idx 0..2 -> bottom-right of that page's third."""
    font = _font(22, bold=True)
    cy = (page_idx + 1) / 3.0 * H - 26
    dr.rounded_rectangle([W - 92, cy - 18, W - 22, cy + 18], radius=9,
                         fill=(12, 12, 18, 190))
    lw = dr.textlength(label, font=font)
    dr.text((W - 57 - lw / 2, cy - font.size / 2 - 1), label, font=font, fill=(250, 250, 250, 255))

def typeset(raw_path, out_path, els, page_labels):
    img = Image.open(raw_path).convert("RGBA")
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(ov)
    for e in els:
        kind = e["kind"]
        if kind == "narration":
            draw_narration(img, dr, e["text"], e["cx"], e["cy"])
        elif kind == "say":
            draw_say(img, dr, e["text"], e["cx"], e["cy"], e.get("tx"), e.get("ty"),
                     bold=e.get("bold", False))
        elif kind == "roar":
            draw_roar(img, dr, e["text"], e["cx"], e["cy"])
        elif kind == "echo":
            draw_echo(img, dr, e["text"], e["cx"], e["cy"])
    img = Image.alpha_composite(img, ov)
    dr2 = ImageDraw.Draw(img)
    for i, lab in enumerate(page_labels):
        draw_page_no(dr2, lab, i)
    img.convert("RGB").save(out_path, "PNG")
