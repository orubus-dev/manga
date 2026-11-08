# I Am God — The Manga

Colored manhwa adaptation of the novel *I am God* (LSLCCF translation).
**Chapters 1–10 complete: 20 sheets × 3 pages = 60 pages**, delivered as 3-up
sheets (crop pages from `chapters/chNN/sheet_chNN_nX.png`; pages are 768×1344
each, numbering is continuous P1–P60).

## Start reading

| Arc | Chapters | Sheets |
|-----|----------|--------|
| The Observer Unbound by Time (modern day → death) | 1 | `ch01` n1–n2 |
| Creation, the Void, the Cambrian Eden | 2–3 | `ch02`–`ch03` |
| Wisdom, Life, Shelly the Fusion Monster, the First King | 4–6 | `ch04`–`ch06` |
| Faith and the King of Wisdom; famine; Ancestral Fish | 7–8 | `ch07`–`ch08` |
| Food and a New Species; Writing and Mythology | 9–10 | `ch09`–`ch10` |

Chapter-by-chapter page plan: [`adaptation/ADAPTATION_PLAN.md`](./adaptation/ADAPTATION_PLAN.md).
Character set + locked looks: [`bible/characters/CHARACTERS.md`](./bible/characters/CHARACTERS.md).
What changed and why: [`bible/CHANGELOG.md`](./bible/CHANGELOG.md).

## Folders

- `chapters/chNN/raw/` — generated panel art, **text-free by design** (the image
  model cannot letter; all words are drawn by the typesetter).
- `chapters/chNN/pages/` — typeset pages (English lettering, page numbers).
- `chapters/chNN/sheet_chNN_nX.png` — **the deliverable** 3-up sheets.
- `references/` — character lineup, contact sheets, QC grid.
- `novel/` — local source chapters (not committed: third-party translation).

## Pipeline

Scripts live in `../pipeline/` (plan files per chapter, runner, typesetter,
compositor, QC). `../pipeline/scheduled_run.sh` advances the book on schedule.
