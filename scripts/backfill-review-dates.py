#!/usr/bin/env python3
"""Backfill last_reviewed timestamps in INDEX.yaml from SKILL.md file mtime.

Usage:
    python scripts/backfill-review-dates.py

Reads each SKILL.md's modification time, sets the corresponding
INDEX.yaml entry's last_reviewed to that date.
"""

import yaml, os, time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = REPO_ROOT / "meta" / "distributor" / "INDEX.yaml"

with open(INDEX_PATH, encoding="utf-8") as f:
    idx = yaml.safe_load(f)

updated = 0
for entry in idx["skills"]:
    path = entry.get("path")
    if not path:
        continue
    skill_md = REPO_ROOT / path / "SKILL.md"
    if not skill_md.exists():
        continue
    mtime = skill_md.stat().st_mtime
    date_str = time.strftime("%Y-%m-%d", time.localtime(mtime))
    if entry.get("last_reviewed") != date_str:
        entry["last_reviewed"] = date_str
        updated += 1
        print(f"  {entry['name']}: {date_str}")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    yaml.dump(idx, f, allow_unicode=True, sort_keys=False)

print(f"Updated {updated} entries in INDEX.yaml")
