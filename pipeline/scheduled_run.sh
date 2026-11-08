#!/usr/bin/env bash
# scheduled_run.sh — the I am God manga scheduled tool chain.
# Idempotent: finds chapters whose plan exists but sheets are missing/failing,
# (re)builds them, refreshes the contact sheet, commits+pushes new art.
# Designed to be invoked by the scheduler cron (or by hand).
set -u
cd /home/z/my-project/manga
LOG="pipeline/state/scheduled_run.log"
say(){ echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }

say "=== scheduled run start ==="

# 1) Build any planned-but-missing sheets (skips finished ones; retries failures)
python3 pipeline/run_chapter.py >> "$LOG" 2>&1
say "run_chapter pass done (rc=$?)"

# 2) Refresh the all-sheets QC contact sheet
python3 pipeline/contact_all.py >> "$LOG" 2>&1
say "contact sheet refreshed (rc=$?)"

# 3) Commit + push any new/changed art (novel text is NOT tracked: copyright)
if [ -d .git ]; then
  git add -A "I am God/chapters" "I am God/references" "I am God/adaptation" "I am God/bible" pipeline plans 2>>"$LOG"
  git add "I am God/README.md" README.md 2>>"$LOG" || true
  if ! git diff --cached --quiet; then
    git -c user.name="manga-forge" -c user.email="forge@orubus.dev" \
        commit -q -m "scheduled run: new/updated sheets $(date '+%F %H:%M')" || true
    bash pipeline/push.sh >> "$LOG" 2>&1 && say "pushed to GitHub" || say "push failed (see log)"
  else
    say "nothing new to commit"
  fi
fi
say "=== scheduled run end ==="
