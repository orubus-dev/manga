# manga

Full-color AI-assisted manga adaptations. Each book lives in its own folder; each generated image is a vertical webtoon strip that equals **3 manga pages**.

## Books

| Book | Source | Status | Chapters |
|---|---|---|---|
| [Guarding the River of Time](Guarding-the-River-of-Time/) | web novel by *The Raccoon that Plucks Stars* (610 ch.) | Ch. 1 released (18 pages, EPUB + CBZ) | 1 / ongoing |
| [I am God](I%20am%20God/) | web novel *I am God* (458 ch.) | Ch. 1-10 adapted (6 pages/ch, full color) | 10 / ongoing |

## How a chapter is made

1. Character card locks the protagonist's design (hair / brows / build anchors never drift).
2. The chapter is storyboarded into 18 panels -> 6 vertical strips (3 pages each).
3. Panels are AI-generated **full color, with no text**.
4. All narration captions, speech bubbles and page numbers are overlaid programmatically (PIL), so text is always crisp and fixable.
5. Pages are also shipped as a CBZ for one-click reading.

See `Guarding-the-River-of-Time/metadata.json` for the full book metadata.

### I am God pipeline

- Locked character set + palettes: `pipeline/locks.py` (changes require `I am God/bible/CHANGELOG.md` entry).
- Style bible: `I am God/bible/style.md`. Per-page adaptation plan: `I am God/ADAPTATION.md`.
- Idempotent builder: `python3 pipeline/run_chapter.py [NNN]` (rebuilt iff a strip's raw PNG is missing).
- QC: `python3 pipeline/contact_all.py`. Publish: `python3 pipeline/gh_publish.py`.
- The `novel/` folders hold third-party translated source text and are **never committed**.
