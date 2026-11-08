# CHANGELOG — locked blocks & palettes

## 2026-11-09 — Initial locked character set + palette ladder (ch1-10)
- Created `pipeline/locks.py`: @god@, @human@, @redlichia@, @shelly@, @fmon@, @queen@,
  @daughter@, @sons@, @tmen@, @afish@, @anomalo@.
- Palette ladder: teahouse → cosmos → island → temple → city (continuity locked from ch6 on).
- Typesetting bands fixed: P1 [0.04,0.30], P2 [0.37,0.63], P3 [0.70,0.96].
- QC fix: enlarged say/roar bubble padding to stop text clipping at ellipse borders.
- QC fix: @human@ must be referenced by token in every ch1 panel (grey-jacket drift otherwise);
  wounded-Yin-Shen panels must not also show a standing figure (contradiction).

## 2026-11-09 — QC round 1 (ch1-10 full pass)
- **LOCK CHANGED** `@god@`: removed "draped in white garments" (model kept rendering a
  white/dark-robed human with hair). New wording forces a hairless, clothless, faceless
  silhouette of glowing white light. 14/20 sheets passed; regenerating ch002-S2, ch003-S2
  (text leak), ch005-S1, ch006-S2, ch009-S2 (species identity).

## 2026-11-09 — QC rounds 2-3 (ch1-10) + pipeline hardening
- **PROMPT TEMPLATE CHANGED** (locks.render_sheet_prompt): "PAGE 1/2/3" labels caused the
  model to literalize the layout text as garbled captions inside ch002-S2. Now uses
  "TOP/MIDDLE/BOTTOM PANEL" + leading "absolutely no text" sentence. No leaks since.
- **TYPESET HARDENED**: bubble cx clamped inside strip margins (ch009-S2 P5 left-clip fixed).
- Band discipline re-verified for every plan (P1 [0.04,0.30] / P2 [0.37,0.63] / P3 [0.70,0.96]).
- God-identity trick: for close-ups, frame @god@ as "hand(s) with no face visible" or
  "seen from behind" — full-figure god shots tend to regress to robed humans with hair.
- Final v1 status: 19/20 sheets clean; known miss: ch005-S1 P2 (Fusion Monster rendered as
  tentacled humanoid instead of flesh-mountain + spiral shell). Re-roll candidate for next run.
