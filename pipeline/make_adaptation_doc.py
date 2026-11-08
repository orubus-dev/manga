#!/usr/bin/env python3
"""Generate adaptation/ADAPTATION_PLAN.md from the per-chapter plan files."""
import importlib.util, os, re, datetime

PIPE = "/home/z/my-project/manga/pipeline"
OUT = "/home/z/my-project/manga/I am God/adaptation/ADAPTATION_PLAN.md"

rows, page_total = [], 0
for n in range(1, 11):
    spec = importlib.util.spec_from_file_location(f"ch{n:03d}", f"{PIPE}/plans/ch{n:03d}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    p = mod.PLAN
    ch_rows = []
    for sh in p["sheets"]:
        for pg in sh["pages"]:
            page_total += 1
            art = re.sub(r"Top panel: |Middle panel: |Bottom panel: |Top wide panel: ",
                         "\n    - ", pg["art"]).replace("\n", " ")
            chars = sorted(set(re.findall(r"@(\\w+)@", pg["art"])))
            dials = [e["t"] for e in pg.get("els", []) if "kind" in e]
            narr = [e["t"] for e in pg.get("els", []) if "kind" not in e]
            ch_rows.append((sh["n"], pg["page"], art, chars, dials, narr))
    rows.append((n, p["title"], p.get("palette", ""), ch_rows))

L = []
L.append("# I AM GOD — Adaptation Plan, Chapters 1–10")
L.append("")
L.append(f"_Generated {datetime.date.today()}; source of truth: `pipeline/plans/chNNN.py`, "
         f"adapted verbatim from `I am God/novel/chNNN.txt` (LSLCCF translation)._")
L.append("")
L.append("## Format")
L.append("- 1 generated page = 768×1344 px; 1 sheet = 3 pages side-by-side (cropped by the reader).")
L.append("- 2 sheets per chapter → **20 sheets, 60 pages** for chapters 1–10; page numbers are")
L.append("  continuous across the book.")
L.append("- All art is generated text-free; English lettering (narration, dialogue, roar bursts,")
L.append("  page numbers) is typeset programmatically from the plan `els`.")
L.append("- Character art is locked via verbatim prompt blocks (`pipeline/locks.py`); see")
L.append("  `bible/characters/CHARACTERS.md` for the pre-destined character set.")
L.append("")
L.append("## Chapter map")
L.append("")
L.append("| Ch | Title | Palette | Sheets | Pages |")
L.append("|----|-------|---------|--------|-------|")
for n, title, pal, ch_rows in rows:
    sns = sorted(set(r[0] for r in ch_rows))
    pgs = f"{ch_rows[0][1]}–{ch_rows[-1][1]}"
    L.append(f"| {n} | {title} | {pal} | {len(sns)} | {pgs} |")
L.append("")
for n, title, pal, ch_rows in rows:
    L.append(f"## Chapter {n:02d} — {title}")
    L.append(f"*Palette: {pal} · Source: novel/ch{n:03d}.txt*")
    L.append("")
    for sn, pno, art, chars, dials, narr in ch_rows:
        L.append(f"### Page {pno} (sheet {sn})")
        L.append(f"- **Art:** {art.strip()}")
        if chars:
            L.append(f"- **Locked characters:** {', '.join('@'+c+'@' for c in chars)}")
        for d in dials:
            L.append(f"- **Dialogue:** “{d}”")
        for t in narr:
            L.append(f"- **Narration:** {t}")
        L.append("")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w").write("\n".join(L))
print(OUT, f"{len(rows)} chapters, {page_total} pages")
