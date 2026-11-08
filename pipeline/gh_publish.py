#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Push the manga repo to GitHub. Never prints the token."""
import subprocess
import sys

ROOT = "/home/z/my-project/manga"

def main():
    r = subprocess.run(["git", "push", "origin", "HEAD"], cwd=ROOT,
                       capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    # sanitize any token that might appear in remote output
    import re
    out = re.sub(r"github_pat_[A-Za-z0-9_]+", "***TOKEN***", out)
    out = re.sub(r"x-access-token:[^@]+@", "***@", out)
    print(out.strip())
    sys.exit(r.returncode)

if __name__ == "__main__":
    main()
