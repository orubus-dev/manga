# Character & style locks for "I am God" — inject VERBATIM into every prompt.
# Any change here requires a bible/CHANGELOG.md entry.

LOCKS = {
    "@god@": "Yin Shen the God, a tall slender humanoid figure made entirely of glowing white light, completely faceless with no facial features, no hair and no cloth — a luminous white silhouette brighter than the surroundings, edges dissolving into wisps of light like a holy ghost",
    "@human@": "Yin Shen, a young Chinese man in his mid-twenties, short neat black hair, sharp calm dark eyes, slim build, wearing a light grey open jacket over a plain white t-shirt, dark slim trousers, white sneakers",
    "@redlichia@": "Redlichia the Trilobite Man king, a tall humanoid male with strictly human body plan clad in glossy black chitin plate armor, his head fully encased in a dark three-lobed trilobite bone helmet, strong dignified build, wise noble bearing",
    "@shelly@": "Shelly, a petite girl-like creature, a small humanoid girl with soft brown hair in a loose braid, large vacant green eyes, pale skin, bare feet with pink toenails, wearing a flowing white gauzy cloak that grows directly from her body like a jellyfish bell",
    "@fmon@": "the Fusion Monster, a colossal mountain of pale flesh dozens of meters tall with a huge spiral shell on its back, sharp spikes protruding from its body, many eerie green eyeballs peering from cracks, thick tentacles emerging around the shell",
    "@queen@": "the Trilobite queen, a graceful female humanoid with strictly human body plan wearing white chitin plate armor, her head encased in a white three-lobed bone helmet, slender elegant figure, gentle demeanor",
    "@daughter@": "the King's eldest daughter, a young female humanoid with strictly human body plan wearing white chitin plate armor like the queen, head encased in a white three-lobed bone helmet, slender graceful figure",
    "@sons@": "the King's sons, adult male humanoids with strictly human body plans wearing dark chitin plate armor with ornate three-lobed helmets marked with gold trims",
    "@tmen@": "Trilobite Men, a crowd of adult humanoids with strictly human body plans, each clad in chitin plate armor of varying dark earthy colors, heads encased in three-lobed trilobite bone helmets",
    "@afish@": "Ancestral Fish, small jawless armored fish with thick bony carapace head shields, eel-like bodies, no jaws, a round straw-like sucker mouth, dull bronze armor plating",
    "@anomalo@": "Anomalocaris, a five-meter shrimp-like sea predator with a flat oval body, two large segmented grasping claws at its head, a round tooth-ringed mouth, side fin flaps undulating along its body",
}

PALETTES = {
    "teahouse": "warm amber teahouse interior, red paper lanterns, dark polished wood, dusk light through tall glass doors, cozy muted golds and browns",
    "cosmos": "deep space indigo and violet with cold starlight, contrasted against a warm sunlit teal Cambrian shallow sea and golden sand",
    "island": "amber sunset over a teal ocean, black rock island with rare green moss and lichen, warm golden-hour light",
    "temple": "golden sunlight on a white stone pyramid temple, turquoise sea, glossy black chitin armor contrast, epic mythic atmosphere",
    "city": "sunlit white and grey stone city-state, teal shallows and green marshes, warm golden light, glossy black chitin armor contrast, hopeful epic atmosphere",
}

STYLE = ("Full-color professional manhwa webtoon strip, three stacked manga pages in one vertical image, "
         "clean thin panel borders, crisp confident ink lineart, soft cel shading with painterly light, "
         "believable anatomy and physical materials, expressive body language, cinematic composition, "
         "premium Korean webtoon illustration quality. "
         "No text, no speech bubbles, no letters, no numbers, no logos, no watermark, no sound effects.")

FRIEND = "the buzz-cut friend, a stocky Chinese man in his mid-twenties with a buzz cut and round glasses, wearing a mustard-yellow hoodie and canvas backpack"


def collect_tokens(text: str):
    return [t for t in LOCKS if t in text]


def render_sheet_prompt(arts, palette_name):
    """arts: list of 3 page art strings (top, middle, bottom)."""
    all_art = " ".join(arts)
    toks = collect_tokens(all_art)
    parts = ["Color illustration with absolutely no text, no letters, no captions anywhere in the image."]
    labels = ["TOP PANEL", "MIDDLE PANEL", "BOTTOM PANEL"]
    for lab, art in zip(labels, arts):
        parts.append(f"{lab}: {art.strip()}")
    body = "\n".join(parts)
    blocks = [f"{t} = {LOCKS[t]}" for t in toks]
    cast = ("Cast (keep EXACTLY these designs, absolutely consistent): " + "; ".join(blocks)) if blocks else ""
    prompt = f"{body}\n{cast}\nColor palette: {PALETTES[palette_name]}\n{STYLE}"
    return prompt
