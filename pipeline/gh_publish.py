#!/usr/bin/env python3
"""Create the GitHub repo 'manga' (if missing) and push. Token never printed."""
import json, re, subprocess, urllib.request

SRC = "/home/z/my-project/scripts/gh_state.py"
tok = re.search(r"github_pat_11[A-Za-z0-9_]+", open(SRC).read())
assert tok, "no token"
T = tok.group(0)
HDR = {"Authorization": f"Bearer {T}", "Accept": "application/vnd.github+json",
       "User-Agent": "manga-forge"}


def api(path, method="GET", body=None):
    req = urllib.request.Request(f"https://api.github.com{path}", method=method,
                                 data=json.dumps(body).encode() if body else None, headers=HDR)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode()
            return r.status, (json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]


s, me = api("/user")
login = me.get("login", "?") if isinstance(me, dict) else "?"
print("auth as:", login)
if s != 200:
    raise SystemExit("token dead")

# try org namespace first (matches existing orubus-dev repos), then personal
owner = "orubus-dev" if isinstance(me, dict) and login != "orubus-dev" else login
for cand in ([f"/orgs/{owner}/repos"] if owner == "orubus-dev" else []) + ["/user/repos"]:
    s2, r2 = api(cand, "POST", {"name": "manga", "description":
                   "Manga adaptation pipeline + library — I am God (ch1-10)",
                   "private": False, "auto_init": False})
    print("create via", cand, "->", s2)
    if s2 in (201, 422):
        break
s3, r3 = api(f"/repos/{owner}/manga")
full = r3.get("full_name") if isinstance(r3, dict) else None
print("repo:", s3, full)
if not full:
    owner, _ = login, api("/user/repos", "POST", {"name": "manga"})
    s3, r3 = api(f"/repos/{owner}/manga")
    full = r3.get("full_name")
print("pushing to:", full)
remote = f"https://x-access-token:{T}@github.com/{full}.git"
subprocess.run(["git", "remote", "remove", "origin"], cwd="/home/z/my-project/manga")
subprocess.run(["git", "remote", "add", "origin", remote], cwd="/home/z/my-project/manga")
r = subprocess.run(["git", "push", "-u", "origin", "HEAD"], cwd="/home/z/my-project/manga",
                   capture_output=True, text=True)
out = (r.stdout + r.stderr).replace(T, "[REDACTED]")
print(out[-1500:])
print("RC", r.returncode)
