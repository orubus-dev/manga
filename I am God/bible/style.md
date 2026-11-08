# I am God — Style Bible

## Standing rules (permanent)
1. No unexplained changes between panels or pages. Visual progression must follow the story.
2. The golden rule: the manga must look like a carefully illustrated, professionally produced
   manhwa made by human artists — believable environments, physical materials, expressive characters.
3. No AI slop. No fake realism. No visual nonsense.
4. **Zero text in generated art.** The image model always produces garbled letters, so every
   caption, speech bubble and page number is overlaid programmatically (PIL, DejaVu, English).
5. Locked character blocks (`pipeline/locks.py`) are injected **verbatim** into every prompt.
   Any change to a locked block or palette requires a `bible/CHANGELOG.md` entry.
6. One generated image = one vertical strip of **3 manga pages** (768x1344). One chapter = 2 sheets.
7. Speech/narration must be lifted verbatim from the English translation of the novel.

## Trilobite folk rule
Trilobite Men are **strictly human body plan + chitin plate armor**. Never insectoid faces,
never extra limbs, never non-human silhouettes. The armor and the three-lobed bone helmet
carry the species identity. The God is always **faceless light** — no facial features, ever.

## Palettes (in story order)
- `teahouse` (ch1): warm amber interior, red lanterns, dusk glass light.
- `cosmos` (ch2): indigo/violet deep space vs. sunlit teal Cambrian sea.
- `island` (ch3): amber sunset, black rock, first green moss.
- `temple` (ch4-5): golden light on white stone pyramid, turquoise sea.
- `city` (ch6-10+): sunlit white/grey stone city-state, teal shallows, green marshes.

## Text bands per strip (typesetting)
- Page 1 of a strip: cy in [0.04, 0.30]
- Page 2: cy in [0.37, 0.63]
- Page 3: cy in [0.70, 0.96]
Narration boxes top of page; say bubbles above/beside speakers; tails point at the speaker.

## Pipeline
- `pipeline/run_chapter.py` — idempotent builder (sheet rebuilt iff its raw PNG is missing).
- `pipeline/contact_all.py` — QC contact sheets per chapter + global overview.
- `pipeline/make_adaptation_doc.py` — regenerates `I am God/ADAPTATION.md`.
- `pipeline/gh_publish.py` — push to GitHub (token sanitized).
- The `novel/` folder is third-party translated text: **never committed** (gitignored).
