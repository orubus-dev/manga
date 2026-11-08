# Change Log — I am God manga

All visual changes between panels/pages/chapters must be explained here.
Locked blocks live in `pipeline/locks.py`; this file records every deliberate change.

## 2026-11-08 — v1.0 production run (ch1–10)
- English lettering throughout (DejaVu Sans, programmatic typesetting; zero text
  inside generated art). Generated art is text-free by design; all narration
  boxes, speech bubbles, roar bursts and page numbers are drawn by
  `pipeline/typeset_page.py` from the chapter plans.
- 20 sheets planned: 10 chapters × 2 sheets × 3 pages (768×1344 pages, 3-up
  sheets with title bar). Page numbering is continuous across the book (P1–P60).

## 2026-11-08 — QC fix: trilobite-folk body plan + god facelessness
- Symptom: in ch07/08 renders Redlichia drifted into a literal giant pillbug
  (non-humanoid, unreadable acting) and the god was drawn with a visible face —
  both violations of the locked canon. Affected sheets were scrapped and
  regenerated.
- Root cause: the phrase "chain of … segments like a pillbug" in `@redlichia@`
  overpowered "humanoid", and the god lock allowed facial drift.
- Fix (locks.py, injected verbatim into all future page prompts):
  - `@redlichia@`, `@queen@`, `@daughter@`, `@sons@`, `@tmen@` now open with
    "strictly human body plan — one head, upright on two legs, two arms" and
    close with "no antennae, not an insect"; chitin is described as
    armadillo-like plate armor.
  - `@god@` now states the head is "a smooth blank oval of light with absolutely
    no facial features — no eyes, no nose, no mouth".
- Chapters 1–6 and 9–10 sheets that already passed QC were kept as delivered;
  ch07–08 fully regenerated under the new locks. From ch08 onward the King's
  arc (mourning → lawgiver) reads with a consistent humanoid silhouette.
- Known accepted drift: ch03–06 crowd scenes show smaller, more literal
  trilobite fauna (primordial-era aesthetic) before the civilization arc;
  documented here as the explanation required by the standing visual rules.
