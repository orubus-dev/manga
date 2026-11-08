#!/usr/bin/env python3
"""Chapter orchestrator for the I am God manga tool chain.
Generates page art (3 parallel), typesets English lettering, composes 3-up sheets,
runs QC, updates progress state. Idempotent: finished sheets are skipped.

Usage: run_chapter.py [chapter_no ...] [--force] [--sheets N]
"""
import sys, os, json, subprocess, importlib.util, time
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

ROOT = "/home/z/my-project/manga"
BOOK = f"{ROOT}/I am God"
PIPE = f"{ROOT}/pipeline"
sys.path.insert(0, PIPE)
from locks import render, GLOBAL_STYLE, PALETTES  # noqa
from typeset_page import typeset_page  # noqa
from compose_sheet import compose  # noqa

FORCE = "--force" in sys.argv
ONLY_SHEET = None
if "--sheets" in sys.argv:
    ONLY_SHEET = int(sys.argv[sys.argv.index("--sheets") + 1])
CHAPTERS = [int(a) for a in sys.argv[1:] if a.isdigit()]

QC = {"min_lum": 18, "max_lum": 240, "min_std": 10}


def load_plan(n):
    spec = importlib.util.spec_from_file_location(f"ch{n:03d}", f"{PIPE}/plans/ch{n:03d}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.PLAN


def qc_img(path):
    try:
        im = Image.open(path).convert("L")
        if im.size[0] < 300:
            return False, "too small"
        px = list(im.resize((64, 112)).getdata())
        mean = sum(px) / len(px)
        var = sum((p - mean) ** 2 for p in px) / len(px)
        if mean < QC["min_lum"] or mean > QC["max_lum"]:
            return False, f"lum {mean:.0f}"
        if var ** 0.5 < QC["min_std"]:
            return False, "blank"
        return True, "ok"
    except Exception as e:
        return False, str(e)


def gen_page(prompt, out):
    if os.path.exists(out) and not FORCE:
        ok, _ = qc_img(out)
        if ok:
            return True
    os.makedirs(os.path.dirname(out), exist_ok=True)
    for attempt in range(6):
        r = subprocess.run(["z-ai", "image", "-p", prompt, "-o", out, "-s", "768x1344"],
                           capture_output=True, text=True, timeout=300)
        if os.path.exists(out):
            ok, why = qc_img(out)
            if ok:
                return True
        time.sleep(10 + attempt * 12)
    print(f"    GEN-FAIL {os.path.basename(out)}")
    return False


def sheet_page_palette(sheet):
    for pg in sheet["pages"]:
        if pg.get("palette"):
            return None  # mixed palettes: per-page override wins
    return None


def build_sheet(plan, sheet):
    ch = plan["chapter"]
    chdir = f"{BOOK}/chapters/ch{ch:02d}"
    rawd, pagd = f"{chdir}/raw", f"{chdir}/pages"
    os.makedirs(rawd, exist_ok=True)
    os.makedirs(pagd, exist_ok=True)
    s = sheet["n"]
    sheet_out = f"{chdir}/sheet_ch{ch:02d}_n{s}.png"
    if os.path.exists(sheet_out) and not FORCE:
        print(f"  ch{ch:02d} sheet {s}: exists, skip")
        return True
    palette = PALETTES[sheet_page_palette(sheet) or plan.get("palette", "cambrian")]
    jobs = []
    for pg in sheet["pages"]:
        pno = pg["page"]
        ppal = pg.get("palette")
        pal = PALETTES[ppal] if ppal else palette
        prompt = (render(pg["art"]) + ". " + pal + " " + GLOBAL_STYLE)
        if len(prompt) > 2600:
            print(f"    WARN p{pno}: rendered prompt {len(prompt)} chars — the image API "
                  f"fails (result.data undefined) above ~3000; trim the plan art text")
        jobs.append((pno, prompt, f"{rawd}/s{s}_p{pno}.png"))
    with ThreadPoolExecutor(max_workers=3) as ex:
        results = list(ex.map(lambda j: gen_page(j[1], j[2]), jobs))
    if not all(results):
        return False
    for (pno, _, raw), ok in zip(jobs, results):
        pg = next(p for p in sheet["pages"] if p["page"] == pno)
        els = pg.get("els", [])
        typeset_page(raw, els, f"{pagd}/s{s}_p{pno}.png",
                     page_no=pno, chapter_tag=f"Ch.{ch:02d}")
    pages = [f"{pagd}/s{s}_p{p['page']}.png" for p in sheet["pages"]]
    title = f"I AM GOD  ·  Chapter {ch:02d} — {plan['title']}"
    sub = f"Sheet {s}/{len(plan['sheets'])}  ·  Pages {pages[0] and sheet['pages'][0]['page']}-{sheet['pages'][-1]['page']}"
    compose(pages, sheet_out, title, sub)
    ok, why = qc_img(sheet_out)
    state = json.load(open(f"{PIPE}/state/progress.json")) if os.path.exists(f"{PIPE}/state/progress.json") else {}
    state.setdefault("sheets", {})[f"ch{ch:02d}_n{s}"] = {"ok": ok, "why": why, "file": sheet_out}
    os.makedirs(f"{PIPE}/state", exist_ok=True)
    json.dump(state, open(f"{PIPE}/state/progress.json", "w"), indent=1)
    print(f"  ch{ch:02d} sheet {s}: {'OK' if ok else 'QC-FAIL ' + why}")
    return ok


def main():
    plans = CHAPTERS or sorted(
        int(f.split("ch")[1].split(".")[0]) for f in os.listdir(f"{PIPE}/plans")
        if f.startswith("ch") and f.endswith(".py"))
    for n in plans:
        plan = load_plan(n)
        print(f"Chapter {n:02d} — {plan['title']}")
        for sheet in plan["sheets"]:
            if ONLY_SHEET and sheet["n"] != ONLY_SHEET:
                continue
            build_sheet(plan, sheet)


if __name__ == "__main__":
    main()
