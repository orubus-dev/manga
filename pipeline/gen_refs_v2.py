#!/usr/bin/env python3
"""Character reference sheets v2 — prompts built VERBATIM from pipeline/locks.py.
Individual full-body refs + a composed, labeled 2x3 lineup poster (PIL)."""
import os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, "/home/z/my-project/manga/pipeline")
from locks import LOCKS  # single source of truth

REF = "/home/z/my-project/manga/I am God/references"
STYLE = ("Full body single character reference, standing, head to toe, centered, on a "
         "flat warm beige background, professional colored manhwa style, clean "
         "confident ink linework, rich cel shading, crisp high-detail digital "
         "illustration. No text, no letters, no words, no watermark, no logo.")

ROSTER = [  # (file, lock token, extra scene direction)
    ("yinshen",   "@yinshen@",   "calm detached expression, standing relaxed."),
    ("friend",    "@friend@",    "warm smile, backpack on one shoulder."),
    ("god",       "@god@",       "on a dark charcoal background; serene standing pose."),
    ("redlichia", "@redlichia@", "standing tall with dignified regal posture."),
    ("shelly",    "@shelly@",    "innocent vacant expression, hands at her sides."),
    ("queen",     "@queen@",     "serene graceful standing posture."),
]


def gen(item):
    name, tok, extra = item
    out = f"{REF}/indiv/{name}.png"
    if os.path.exists(out) and os.path.getsize(out) > 100000:
        return name, "keep"
    prompt = f"{LOCKS[tok]}. {extra} {STYLE}"
    for i in range(4):
        r = subprocess.run(["z-ai", "image", "-p", prompt, "-o", out, "-s", "768x1344"],
                           capture_output=True, text=True, timeout=300)
        if os.path.exists(out) and os.path.getsize(out) > 100000:
            return name, "ok"
        time.sleep(10 + i * 10)
    return name, "FAIL"


def lineup():
    from PIL import Image, ImageDraw, ImageFont
    fd = "/usr/share/fonts/truetype/dejavu"
    f_name = ImageFont.truetype(f"{fd}/DejaVuSans-Bold.ttf", 30)
    f_sub = ImageFont.truetype(f"{fd}/DejaVuSans.ttf", 20)
    LABEL = {"yinshen": "YIN SHEN — the observer", "friend": "THE FRIEND — novelist",
             "god": "THE GOD — faceless light", "redlichia": "REDLICHIA — King of Wisdom",
             "shelly": "SHELLY — Fusion Monster", "queen": "THE QUEEN — of the trilobite folk"}
    cell_w, bar = 500, 64
    ims = []
    for name, _, _ in ROSTER:
        im = Image.open(f"{REF}/indiv/{name}.png").convert("RGB")
        ims.append((name, im.resize((cell_w, int(im.size[1] * cell_w / im.size[0])))))
    cell_h = max(im.size[1] for _, im in ims) + bar
    W, H = cell_w * 3 + 24, cell_h * 2 + 24
    canvas = Image.new("RGB", (W, H), (245, 238, 225))
    d = ImageDraw.Draw(canvas)
    for i, (name, im) in enumerate(ims):
        r, c = divmod(i, 3)
        x, y = 8 + c * (cell_w + 4), 8 + r * (cell_h + 4)
        canvas.paste(im, (x, y + bar))
        d.rectangle([x, y, x + cell_w, y + bar - 6], fill=(38, 34, 30))
        d.text((x + 10, y + 8), LABEL[name], font=f_name, fill=(245, 238, 225))
        d.text((x + 10, y + bar - 26), "I AM GOD · character set ch1-10", font=f_sub, fill=(190, 175, 150))
    out = f"{REF}/character_lineup.png"
    canvas.save(out, quality=92)
    print("lineup ->", out, canvas.size)


if __name__ == "__main__":
    os.makedirs(f"{REF}/indiv", exist_ok=True)
    with ThreadPoolExecutor(max_workers=3) as ex:
        for name, st in ex.map(gen, ROSTER):
            print(name, st, flush=True)
    lineup()
