# I am God — Locked Style Bible (v1.0)

Source of truth: the novel *I am God* (LSLCCF), chapters 1–10. Every page prompt must
derive its scenes and art descriptions **exclusively** from the chapter text.

## Format
- Colored manhwa, full color, webtoon-style vertical panel stacks.
- One generated page = 768x1344 px. One sheet = 3 pages side by side (user crops).
- English typesetting only (DejaVu Sans). All lettering applied programmatically —
  generated art must contain ZERO text (no letters, no bubbles, no SFX, no watermarks).

## GLOBAL STYLE BLOCK (locked — append verbatim to every page prompt)
Professional colored manhwa webtoon comic page, clean confident ink linework, rich cel
shading with soft gradient light, vivid harmonious palette, detailed believable
environment with physical materials, expressive character acting, dramatic cinematic
lighting, crisp high-detail digital illustration. Vertical webtoon page divided into
stacked comic panels separated by clean white gutters. No text, no letters, no words,
no speech bubbles, no sound effects, no watermark, no logo.

## Character locking
- Locked character blocks live in `bible/characters/*.md`. Plans reference them by
  token (`@yinshen@`, `@god@`, `@friend@`, `@redlichia@`, `@shelly@`, `@fmonster@`,
  `@queen@`, `@daughter@`, `@tmen@`, `@afish@`, `@anomalo@`) and the runner injects
  the locked text verbatim. Never paraphrase a locked block.
- No unexplained changes between panels or pages. Visual progression follows the story.

## Era palettes (locked per chapter range)
- **Modern (ch1):** warm amber afternoon light, honey-brown wood teahouse, dusty
  sunbeams through windows, muted street grays, glass doors.
- **Cosmic (ch2 S1):** deep indigo-black void, cyan-white starfields, Earth in blues
  and cloud whites, radiant figure as a spark of warm white.
- **Void (ch2 S2 p4):** absolute black, no horizon, single pale consciousness glow.
- **Cambrian Eden (ch2 S2 p5 – ch10):** teal-emerald shallow sea with golden sun
  shafts, rust-tan barren land like Mars, white limestone pyramid-temple, black
  chitin carapaces with pale amber glow accents, warm sunset ambers for evening scenes.
- **God-Given City (ch7-10):** warm sandstone and white stone, marsh greens,
  sunset gold for vows and harvests, cold blue-gray for the funeral and night scenes.

## Typography (programmatic, English only)
- Font: DejaVu Sans (`/usr/share/fonts/truetype/dejavu/`), Book for bubbles, Bold for
  narration and emphasis.
- Narration box: rounded rect, parchment `#f3e6c8` at 92% alpha, text `#3a2a18`.
- Speech bubble: white ellipse, black text, triangular tail toward the speaker.
- Creature roar bubble: white star-burst polygon, black bold text.
- Memory/echo bubble: pale blue-gray `#e8eef4` fill, gray outline (for remembered lines).
- Page number bottom-center, small, gray.

## Golden rules (standing)
1. Must look like a carefully illustrated, professionally produced manhwa by human
   artists: believable environments, physical materials, expressive characters.
2. No AI slop, no fake realism, no visual nonsense. QC every sheet by eye.
3. Panel/page changes must be explainable by the story.
4. Dialogue and narration are lifted from the chapter text (already English), never invented.
