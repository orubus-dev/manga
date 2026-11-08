#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Idempotent chapter builder for 'I am God' manga pipeline.

Usage:
  python3 -u pipeline/run_chapter.py          # build ALL planned-but-missing sheets
  python3 -u pipeline/run_chapter.py 3        # build only chapter 3 (accepts '3' or '003')

Idempotency: a sheet is (re)built iff its raw PNG is missing. To force a regen,
delete raw_sheet_N.png AND sheet_N.png, then rerun.
"""
import importlib.util
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "I am God")
PIPE = os.path.join(ROOT, "pipeline")
PLANS = os.path.join(PIPE, "plans")
STATE = os.path.join(PIPE, "state", "progress.json")
RAW_NAME = "raw_sheet_{n}.png"
SHEET_NAME = "sheet_{n}.png"
SIZE = "768x1344"
MAX_RETRY = 3


def load_plan(ch):
    path = os.path.join(PLANS, f"ch{int(ch):03d}.py")
    spec = importlib.util.spec_from_file_location(f"plan_ch{int(ch):03d}", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.PLAN


def all_plans():
    out = []
    for f in sorted(os.listdir(PLANS)):
        if f.startswith("ch") and f.endswith(".py"):
            out.append(load_plan(f[2:5]))
    return out


def zai_generate(prompt, out_path):
    for attempt in range(1, MAX_RETRY + 1):
        r = subprocess.run(["z-ai", "image", "-p", prompt, "-o", out_path, "-s", SIZE],
                           capture_output=True, text=True, timeout=600)
        if r.returncode == 0 and os.path.exists(out_path) and os.path.getsize(out_path) > 30000:
            return True
        print(f"    attempt {attempt} failed: {r.stderr.strip()[:200]}")
    return False


def build_sheet(plan, sheet, ch_dir):
    n = sheet["sheet"]
    raw = os.path.join(ch_dir, RAW_NAME.format(n=n))
    final = os.path.join(ch_dir, SHEET_NAME.format(n=n))
    if os.path.exists(raw) and os.path.getsize(raw) > 30000:
        if os.path.exists(final):
            return "cached"
        # raw exists but typeset missing -> just typeset
    else:
        from locks import render_sheet_prompt
        arts = [p["art"] for p in sheet["pages"]]
        prompt = render_sheet_prompt(arts, plan["palette"])
        if len(prompt) > 2600:
            print(f"    WARN prompt {len(prompt)} chars (>2600)")
        print(f"    generating sheet {n} ({len(prompt)} chars)...")
        if not zai_generate(prompt, raw):
            return "failed"
    from typeset import typeset
    els = []
    labels = []
    for idx, pg in enumerate(sheet["pages"]):
        labels.append(f"P{pg['page']}")
        for e in pg.get("els", []):
            els.append(e)
    typeset(raw, final, els, labels)
    return "built"


def progress_path(ch_dir):
    return os.path.join(ch_dir, "progress.json")


def update_state(plan, results):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    state = {}
    if os.path.exists(STATE):
        try:
            state = json.load(open(STATE))
        except Exception:
            state = {}
    ch_key = f"ch{plan['chapter']:03d}"
    entry = state.get(ch_key, {})
    for sheet_n, res in results.items():
        entry[str(sheet_n)] = {"ok": res == "built" or res == "cached", "status": res}
    state[ch_key] = entry
    with open(STATE, "w") as f:
        json.dump(state, f, indent=1, sort_keys=True)


def run_chapter(plan):
    ch = plan["chapter"]
    ch_dir = os.path.join(BOOK, "chapters", f"ch{ch:03d}")
    os.makedirs(ch_dir, exist_ok=True)
    print(f"ch{ch:03d} — {plan['title']} ({plan['palette']})")
    results = {}
    for sheet in plan["sheets"]:
        res = build_sheet(plan, sheet, ch_dir)
        results[sheet["sheet"]] = res
        print(f"  sheet {sheet['sheet']}: {res}")
    update_state(plan, results)
    return results


def main():
    args = sys.argv[1:]
    if args:
        ch = int(args[0].lstrip("0") or "0")
        plans = [load_plan(ch)]
    else:
        plans = all_plans()
    if not plans:
        print("no plans found")
        return
    fail = False
    for plan in plans:
        res = run_chapter(plan)
        if any(v == "failed" for v in res.values()):
            fail = True
    # final summary
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    total_ok = sum(1 for c in state.values() for s in c.values() if s.get("ok"))
    total = sum(len(c) for c in state.values())
    print(f"progress: {total_ok}/{total} sheets ok")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
