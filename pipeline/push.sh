#!/usr/bin/env bash
# push.sh — push manga repo to GitHub without leaking the token into logs.
# Token is read at runtime from scripts/gh_state.py (never echoed).
set -u
cd /home/z/my-project/manga
TOKEN="$(grep -ohE 'github_pat_11[A-Za-z0-9_]+' /home/z/my-project/scripts/gh_state.py | head -1)"
[ -n "$TOKEN" ] || { echo "no token found"; exit 1; }
OWNER="$(python3 - <<'EOF'
import re,urllib.request,json
t=__import__('subprocess').run("grep -ohE 'github_pat_11[A-Za-z0-9_]+' /home/z/my-project/scripts/gh_state.py | head -1",shell=True,capture_output=True,text=True).stdout.strip()
r=urllib.request.Request("https://api.github.com/user",headers={"Authorization":f"Bearer {t}","User-Agent":"manga-forge"})
print(json.load(urllib.request.urlopen(r))["login"])
EOF
)"
echo "pushing as user/org: $OWNER"
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$OWNER/manga.git"
GIT_TERMINAL_PROMPT=0 git -c credential.helper= -c "credential.helper=!f(){ echo username=x-access-token; echo password=$TOKEN; };f" push -u origin "$(git rev-parse --abbrev-ref HEAD)" 2>&1 | sed -E 's/github_pat_[A-Za-z0-9_]+/[REDACTED]/g'
