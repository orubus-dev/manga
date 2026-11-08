#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regenerate 'I am God/ADAPTATION.md' from the plan files + on-disk sheets."""
import importlib.util
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "I am God")
PLANS = os.path.join(ROOT, "pipeline", "plans")

from locks import LOCKS, PALETTES  # noqa: E402

CAST_DOC = {
    "@god@": "Yin Shen the God — faceless radiant figure of soft white light",
    "@human@": "Yin Shen (human) — young Chinese man, grey open jacket",
    "@redlichia@": "Redlichia — first Trilobite Man, King of Wisdom, black chitin plate armor + three-lobed helmet",
    "@shelly@": "Shelly — the Fusion Monster's girl form, brown braid, green eyes, white gauzy jellyfish-bell cloak",
    "@fmon@": "Fusion Monster — colossal flesh mountain, spiral shell, tentacles, many green eyes",
    "@queen@": "The Queen — female Trilobite Man in white chitin armor",
    "@daughter@": "The King's eldest daughter — white armor, slender",
    "@sons@": "The King's sons — dark ornate chitin armor, first noble class",
    "@tmen@": "Trilobite Men — the species, human body plan + chitin plate armor",
    "@afish@": "Ancestral Fish — jawless armored fish, sucker mouth",
    "@anomalo@": "Anomalocaris — five-meter shrimp-like sea predator",
}


def load_plans():
    out = []
    for f in sorted(os.listdir(PLANS)):
        if f.startswith("ch") and f.endswith(".py"):
            spec = importlib.util.spec_from_file_location(f"p_{f[:-3]}", os.path.join(PLANS, f))
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            out.append(m.PLAN)
    return out


def main():
    plans = load_plans()
    lines = [
        "# I am God — Adaptation Plan (Chapters 1-10)",
        "",
        "Source: *I am God* (web novel, 458 chapters). This document records the chapter-by-chapter",
        "adaptation produced so far. Each generated image is a vertical strip of **3 manga pages**;",
        "each chapter = **2 sheets (6 pages)**. All dialogue/narration is lifted verbatim from the",
        "English translation. Generated art is **zero-text**; all lettering is overlaid programmatically.",
        "",
        "## Locked cast (character set)",
        "",
    ]
    for tok, desc in CAST_DOC.items():
        lines.append(f"- `{tok}` — {desc}")
    lines += ["", "## Palette continuity", ""]
    for name, p in PALETTES.items():
        lines.append(f"- **{name}** — {p}")
    lines += ["", "## Chapters", "",
              "| Ch | Title | Palette | Sheets | Pages | Status |", "|---|---|---|---|---|---|"]
    for p in plans:
        ch = p["chapter"]
        ch_dir = os.path.join(BOOK, "chapters", f"ch{ch:03d}")
        n_sheets = len(p["sheets"])
        n_pages = sum(len(s["pages"]) for s in p["sheets"])
        done = sum(1 for s in p["sheets"]
                   if os.path.exists(os.path.join(ch_dir, f"sheet_{s['sheet']}.png")))
        status = "complete" if done == n_sheets else f"{done}/{n_sheets} sheets"
        lines.append(f"| {ch} | {p['title']} | {p['palette']} | {n_sheets} | {n_pages} | {status} |")
    lines += ["", "## Page-by-page breakdown", ""]
    for p in plans:
        lines.append(f"### Chapter {p['chapter']} — {p['title']}  (palette: {p['palette']})")
        lines.append("")
        for s in p["sheets"]:
            lines.append(f"**Sheet {s['sheet']}**")
            lines.append("")
            for pg in s["pages"]:
                lines.append(f"- **P{pg['page']}** — {pg['art']}")
                for e in pg.get("els", []):
                    lines.append(f"  - `{e['kind']}`: \"{e['text']}\"")
            lines.append("")
    out_path = os.path.join(BOOK, "ADAPTATION.md")
    with open(out_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(out_path)


if __name__ == "__main__":
    main()
