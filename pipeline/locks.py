"""Locked prompt blocks + style constants. Single source of truth."""

GLOBAL_STYLE = (
    "Professional colored manhwa webtoon comic page, clean confident ink linework, "
    "rich cel shading with soft gradient light, vivid harmonious palette, detailed "
    "believable environment with physical materials, expressive character acting, "
    "dramatic cinematic lighting, crisp high-detail digital illustration. Vertical "
    "webtoon page divided into stacked comic panels separated by clean white gutters. "
    "No text, no letters, no words, no speech bubbles, no sound effects, no watermark, "
    "no logo. Absolutely no writing of any language, no captions, no dialogue "
    "balloons, no symbols, no signage anywhere in the image."
)

PALETTES = {
    "modern": "Warm amber afternoon light, honey-brown wooden teahouse interior, dusty sunbeams, muted street grays, glass doors.",
    "cosmic": "Deep indigo-black cosmic void, cyan-white starfields, Earth in ocean blues and cloud whites, the soul as a spark of warm white light.",
    "void": "Absolute black void without horizon or depth, one faint pale glow of consciousness, oppressive emptiness.",
    "cambrian": "Teal-emerald shallow sea with golden sun shafts, rust-tan barren land like Mars, white limestone pyramid-temple, black chitin carapaces with amber glow accents.",
    "city": "Warm sandstone and white stone city, marsh greens, golden harvest light; cold blue-gray for funerals and night scenes.",
}

LOCKS = {
    "@yinshen@": (
        "Yin Shen, a young East Asian man with messy black hair and sharp dark eyes, "
        "fair skin, wearing a dark navy modern hooded jacket with a small white "
        "zipper line, dark slim pants, black shoes — always shown in this same dark "
        "navy hooded jacket in every panel of the page"
    ),
    "@friend@": (
        "a cheerful East Asian man in his late twenties with a buzz cut and thick "
        "eyebrows, wearing an open olive green plaid shirt over a white t-shirt, dark "
        "jeans, canvas sneakers, a worn canvas backpack — identical outfit in every "
        "panel of the page"
    ),
    "@god@": (
        "a tall smooth silhouette of pure glowing white light shaped like a "
        "genderless human, entirely featureless like a white mannequin of light: "
        "the head is a smooth blank oval of light with absolutely no facial "
        "features - no eyes, no nose, no mouth, no expression, no hair, no "
        "clothing details, softly luminous edges, thin threads of light rising "
        "from the silhouette. Every panel shows the same blank radiant white "
        "outline with a completely blank faceless head and no lettering anywhere."
    ),
    "@redlichia@": (
        "Redlichia the Trilobite Man, a towering humanoid male with a strictly "
        "human body plan - exactly one head, upright posture on two strong legs, "
        "two arms with five-fingered claw-tipped hands - his body clothed in "
        "natural glossy black-brown chitin armor of smooth overlapping rounded "
        "plates like an armadillo's plating, his head covered by a smooth "
        "semicircular dome shell helmet with fine radial ridges and a small "
        "central lobe, two small calm glowing amber eye lights under the front "
        "rim of the dome, no human face, no antennae, no extra legs, not an "
        "insect, dignified expressive human posture and gestures"
    ),
    "@shelly@": (
        "Shelly, a small petite eight-year-old girl with child proportions, large "
        "round green eyes, brown hair in two loose short braids, wearing a simple "
        "opaque white knee-length dress with short sleeves, barefoot, and over the "
        "dress a translucent seafoam oversheet like a jellyfish bell draping from her "
        "shoulders to her knees, its edges fading to transparency"
    ),
    "@fmonster@": (
        "the Fusion Monster, a colossal mountain of pale worm flesh bearing an "
        "immense spiral ammonite-like shell on its back, sharp spines protruding from "
        "its body, eerie green eyeballs of many sizes dotting its flesh, and a myriad "
        "of thick tentacles"
    ),
    "@queen@": (
        "the queen, a female trilobite person with a strictly human body plan - "
        "one head, upright on two legs, two arms - the same smooth semicircular "
        "dome head shield and overlapping glossy chitin plate armor as Redlichia "
        "but in pearl-white with a soft nacre sheen, a slender graceful narrower "
        "frame, two gentle amber eye lights under the front rim of her dome, no "
        "human face, no antennae, not an insect"
    ),
    "@daughter@": (
        "the King's eldest daughter, a young female trilobite person with a "
        "strictly human body plan, pearl-white chitin plate armor like the "
        "queen's, slender and graceful, youthful bearing, dome head shield with "
        "two gentle amber eye lights, no human face, not an insect"
    ),
    "@sons@": (
        "Trilobite Man nobles, humanoid figures with strictly human body plans - "
        "one head, two legs, two arms - in glossy black-brown chitin plate armor "
        "with smooth dome head shields and amber eye lights, robust builds, each "
        "with a slightly different dome ridge pattern, no human faces, not "
        "insects"
    ),
    "@tmen@": (
        "a crowd of Trilobite Men, humanoid people with strictly human body "
        "plans - one head, upright on two legs, two arms - covered in chitin "
        "plate armor of varied earthy colors - black, brown, olive, rust - heads "
        "smooth semicircular domes with radial ridges and small amber eye lights "
        "under the front rim, human-proportioned with expressive human body "
        "language, no human faces, no antennae, not insects"
    ),
    "@anomalo@": (
        "Anomalocaris, a five-meter shrimp-like sea predator with two large ribbed "
        "feeding claws, a segmented flattened body with fin-like side lobes, and "
        "stalked compound eyes"
    ),
    "@afish@": (
        "Ancestral Fish, jawless armored fish the size of an arm, thick bony head "
        "shield carapace, eel-like scaled body, round straw-like sucker mouth, small "
        "close-set eyes"
    ),
}

def render(text: str) -> str:
    out = text
    for k, v in LOCKS.items():
        out = out.replace(k, v)
    return out
