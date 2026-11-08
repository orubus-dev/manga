#!/usr/bin/env python3
"""Extract novel chapters from epub into plain text files (chNNN.txt + toc.txt)."""
import sys, zipfile, re, os
from xml.etree import ElementTree as ET

EPUB = "/home/z/my-project/upload/I_am_God_LSLCCF.epub"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/z/my-project/manga/I am God/novel"
os.makedirs(OUT, exist_ok=True)

NS = {"oc": "http://www.idpf.org/2007/opf", "dc": "http://purl.org/dc/elements/1.1/"}
z = zipfile.ZipFile(EPUB)
opf_path = [n for n in z.namelist() if n.endswith(".opf")][0]
base = os.path.dirname(opf_path)
opf = ET.fromstring(z.read(opf_path))

title = opf.find(".//dc:title", NS)
manifest = {i.get("id"): i.get("href") for i in opf.findall(".//oc:manifest/oc:item", NS)}
spine = [i.get("idref") for i in opf.findall(".//oc:spine/oc:itemref", NS)]

def strip_html(h):
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", h, flags=re.S)
    h = re.sub(r"<br\s*/?>", "\n", h)
    h = re.sub(r"</p>", "\n", h)
    h = re.sub(r"<[^>]+>", "", h)
    h = (h.replace("&nbsp;", " ").replace("&amp;", "&")
          .replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"'))
    lines = [ln.strip() for ln in h.split("\n")]
    return "\n".join(ln for ln in lines if ln)

toc_lines = []
for n, idref in enumerate(spine, 1):
    href = manifest.get(idref)
    if not href:
        continue
    raw = z.read(os.path.join(base, href)).decode("utf-8", "ignore")
    m = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
    ctitle = strip_html(m.group(1)) if m else ""
    body = strip_html(raw)
    body = body.replace(ctitle, "", 1) if ctitle and body.startswith(ctitle) else body
    fn = os.path.join(OUT, f"ch{n:03d}.txt")
    with open(fn, "w") as f:
        f.write(body.strip() + "\n")
    toc_lines.append(f"ch{n:03d}\t{ctitle}")

with open(os.path.join(OUT, "toc.txt"), "w") as f:
    f.write("\n".join(toc_lines) + "\n")
print(f"book title: {title.text if title is not None else '?'}")
print(f"chapters: {len(spine)} -> {OUT}")
