#!/usr/bin/env bash
# Generate individual character reference portraits (parallel).
set -u
cd "/home/z/my-project/manga/I am God/references" || exit 1
mkdir -p indiv
LOG=indiv/gen.log; : > "$LOG"

STYLE="Full body single character reference on a flat warm beige background, professional colored manhwa style, clean confident ink linework, rich cel shading, crisp high-detail digital illustration. No text, no letters, no words, no watermark, no logo."

gen() { # name, description
  local name="$1" desc="$2"
  if [ -s "indiv/$name.png" ]; then echo "SKIP $name" | tee -a "$LOG"; return 0; fi
  z-ai image -p "$STYLE $desc" -o "indiv/$name.png" -s 768x1344 >>"$LOG" 2>&1 \
    && echo "OK $name" | tee -a "$LOG" || echo "FAIL $name" | tee -a "$LOG"
}

gen yinshen "Yin Shen, a young East Asian man with messy black hair and sharp dark eyes, fair skin, calm detached expression, wearing a dark navy modern hooded jacket with a small white zipper line, dark slim pants, black shoes, standing relaxed, full length head to toe." &
gen friend "A cheerful East Asian man in his late twenties with a buzz cut and thick eyebrows, warm smile, wearing an open olive green plaid shirt over a white t-shirt, dark jeans, canvas sneakers, a worn canvas backpack on one shoulder, full length head to toe." &
gen god "On a dark neutral charcoal background instead: a faceless luminous human figure whose entire body is wrapped in flowing white garments made of pure glowing light, no facial features at all, the head a smooth featureless glow, gentle radiant aura, wisps and threads of white light rising from the silhouette toward the sky, serene standing pose, full length." &
gen redlichia "Redlichia the Trilobite Man, a humanoid male whose body is fully covered in glossy black organic sea-insect chitin, smooth curved carapace plates with barnacle-like edges, NOT medieval armor, his head fully encased in a smooth sealed pale bone helmet shaped like a three-lobed trilobite shell with one central longitudinal ridge, the helmet has no human face, no mouth, no nose, only two small glowing amber eye lights set in deep shadowed sockets, powerful but slender build, claws instead of hands, standing reverently, full length head to toe." &
gen shelly "Shelly, a very small petite eight-year-old girl with child proportions and child height, large round green eyes, brown hair in a loose short braid, barefoot with pink toenails, wearing a flowing translucent white gauzy cloak that grows directly from her shoulders and drapes around her like a jellyfish bell, the cloak edges semi-transparent like jellyfish membrane, innocent vacant expression, full length head to toe." &
gen queen "The queen, a female humanoid whose body is covered in smooth white organic chitin like polished seashell, NOT metal armor, her head fully encased in a sealed white bone helmet shaped like a three-lobed trilobite shell with one central longitudinal ridge, no human face, no mouth, only two gentle glowing amber eye lights, slender graceful feminine silhouette, serene posture, full length head to toe." &
wait
ls -la indiv/*.png 2>/dev/null
