#!/usr/bin/env python3
"""Rebuild all typeset pages + sheets from raw art (no re-generation unless raw missing)."""
import sys, os
sys.path.insert(0, "/home/z/my-project/manga/pipeline")
os.chdir("/home/z/my-project/manga")
from run_chapter import load_plan, build_sheet  # noqa

for n in [2, 1, 3, 4, 5, 6, 7, 8, 9, 10]:
    plan = load_plan(n)
    print(f"ch{n:02d}")
    for s in plan["sheets"]:
        build_sheet(plan, s)
