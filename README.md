# manga

Production pipeline and library for manga adaptations, generated with the
manga-forge tool chain (AI art + programmatic lettering + locked character bibles).

## Books

- **[I am God](./I%20am%20God/README.md)** — adaptation of the novel *I am God*
  (LSLCCF translation), chapters 1–10. 20 sheets / 60 pages.

## How a book is structured

```
manga/
└── <Book Title>/
    ├── bible/          # locked style guide + pre-destined character set
    ├── adaptation/     # human-readable page-by-page adaptation plan
    ├── chapters/chNN/  # raw/ (text-free art) → pages/ (typeset) → sheets
    ├── references/     # character lineups, contact sheets, QC grids
    └── novel/          # source text (LOCAL ONLY — not tracked: copyright)
manga/pipeline/         # the tool chain (plans, runner, typesetter, compositor)
```

## Tool chain (scheduled)

`pipeline/scheduled_run.sh` is the idempotent entry point — it builds any
planned-but-missing sheets, refreshes QC contact sheets, and commits+pushes new
art. It runs on a schedule (every 6 h) and advances the adaptation: with the
1–10 adaptation complete, subsequent runs extend plans to chapters 11+ from
`<Book>/novel/chNNN.txt`, one chapter at a time, under the same locked bibles.

Pipeline rules (standing):
1. Every page's scenes and art descriptions derive **exclusively** from the
   chapter text — no invented scenes.
2. Generated art contains **zero text**; all lettering is typeset programmatically.
3. Character looks are locked verbatim (`pipeline/locks.py`); any change needs a
   `bible/CHANGELOG.md` entry.
4. QC every sheet by eye; no AI slop, no fake realism, no visual nonsense.
