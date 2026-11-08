# Pipeline Learnings — I am God manga

## Image API (z-ai image)
- Rendered prompt length must stay **under ~3,000 chars** (locks + palette + global
  style already cost ~2,050). Above that the API returns `result.data undefined`
  (HTTP-level rejection) and the CLI writes NO output file. Keep plan `art` text
  ≤ ~450 chars after lock tokens. `run_chapter.py` now warns at 2,600.
- Transient API errors happen; `gen_page` retries 6× with growing backoff.
- QC gates (`lum` 18–240, std ≥ 10 at 64×112) catch blanks/garbage; night pages
  are the risk zone for the low bound (white gutters usually lift the mean).

## Character consistency
- **The pillbug trap**: describing trilobite-folk as "chain of segments like a
  pillbug" outweighs "humanoid" and yields literal woodlice that cannot act
  (kneel, weep, rule). Fix that worked: open every trilobite-folk lock with
  "strictly human body plan — one head, upright on two legs, two arms", describe
  chitin as *armadillo-like plate armor*, close with "no antennae, not an insect".
- **Face drift on the god**: even with "no face", the model adds faint features
  ~1 in 6 pages. Hardened lock: "the head is a smooth blank oval of light with
  absolutely no facial features — no eyes, no nose, no mouth".
- **Scene overrides character**: in complex panels the composition wins and the
  character lock loses. For emotional/regal beats, add camera language to the
  *art* text itself: "seen from behind", "standing tall and regal", "tiny
  against the immense pyramid".
- **"Reflection" hazard**: "Redlichia's reflection on the surface" renders a
  human face. Say "the reflection of his armored dome head … no human face".
- **Model-invented scenery**: panels mentioning light/king can sprout modern
  cities or Roman soldiers. Add negative anchors in the art text: "no city
  anywhere", "open starry sky".
- Garbled micro-text still appears ~1 in 8 pages (tiny labels in corners).
  Catch it in visual QC; regenerate the page — do not ship it.

## Process
- Stray background drivers from a previous session can keep generating with
  stale in-memory locks and overwrite sheets mid-QC. Before regenerating, check
  `ps -ef | grep z-ai` and kill leftovers; run rebuilds foreground with
  `python3 -u` so logs flush.
- `run_chapter.py 8 --sheets 1` also parses "1" as a chapter (isdigit); it is
  harmless (existing sheets skip) but remember when reading logs.
- Typeset always re-runs from raws; sheets are recomposed from pages; only raw
  generation is skipped when a QC-ok file exists. Delete the specific bad raw
  + sheet files to force a surgical re-roll.
