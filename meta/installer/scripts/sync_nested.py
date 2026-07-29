#!/usr/bin/env python3
"""Nested installer — installs MY_SKILL into WorkBuddy while preserving the
meta/ + domain/ folder hierarchy.

Why a second script (vs. sync.py)?
    sync.py flattens skills into <target>/<name>/ and, critically, converts
    `user-invocable: false` -> `disable-model-invocation: true`. That conversion
    is WRONG for WorkBuddy: disable-model-invocation:true prevents the AI from
    auto-selecting the skill, which would break Distributor's force-trigger of the
    horizontal discipline skills (caveman/thinking-first/review/...). WorkBuddy's
    native `user-invocable: false` already means "hidden from /slash menu but
    callable by the AI / other skills" — exactly what MY_SKILL needs.

    sync_nested.py keeps the full directory tree
    (<target>/MY_SKILL/<rel>/) and PRESERVES `user-invocable` as-is.

Usage:
    # dry-run preview (no writes)
    python sync_nested.py --dry-run

    # install all 27 skills into ~/.workbuddy/skills/MY_SKILL
    python sync_nested.py --force

    # install into a custom target, skipping the skip-list skills
    python sync_nested.py --target /path/to/skills/MY_SKILL

Safe to re-run: overwrites in place, never deletes dst contents.
"""

import os
import shutil
import argparse
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
INDEX = REPO_ROOT / "meta" / "distributor" / "INDEX.yaml"
SKIP_CONFIG = REPO_ROOT / "meta" / "installer" / "skip.yaml"
DEFAULT_TARGET = Path.home() / ".workbuddy" / "skills" / "MY_SKILL"

# Deployment policy lives in skip.yaml (ADR-0002 purity), not in adapter logic.
DEFAULT_SKIP_LIST = {"thinking-first", "caveman", "decide-invest"}

# MY_SKILL-only extension fields with no WorkBuddy equivalent. Stripped on install.
# NOTE: `user-invocable` is intentionally NOT in this list — it is a WorkBuddy
# native field (hide from menu / callable internally) and must be preserved.
STRIP_FIELDS = [
    "risk_level", "category", "horizontal", "always_active",
    "source", "data_layer", "related", "forced_trigger",
]


def load_skip_list():
    if not SKIP_CONFIG.exists():
        return set(DEFAULT_SKIP_LIST)
    with open(SKIP_CONFIG, encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    return set(cfg.get("skip_list", DEFAULT_SKIP_LIST))


def _copytree_overwrite(src, dst):
    """Copy src tree into dst, overwriting files in place. Never deletes dst
    contents — avoids bulk-delete gates and is safe for incremental updates."""
    for item in src.rglob("*"):
        if item.is_file():
            rel = item.relative_to(src)
            target = dst / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def apply_nested_adapter(fm, body, index_entry):
    """Translate a MY_SKILL SKILL.md for nested install.

    - Folds risk_level (from SKILL.md, falling back to INDEX.yaml) into the
      description as `[risk=...]` when non-low.
    - Folds `source` attribution into the description when present.
    - PRESERVES `user-invocable` exactly (no disable-model-invocation swap).
    - Strips MY_SKILL-only extension fields (STRIP_FIELDS).
    """
    fm = dict(fm)
    idx = index_entry or {}

    # 1) risk -> description tag (fallback to INDEX so drift in SKILL.md is covered)
    risk = str(fm.get("risk_level") or idx.get("risk_level") or "low").lower()
    desc = fm.get("description", "") or ""
    if risk != "low" and f"risk={risk}" not in desc.lower():
        desc = f"{desc} [risk={risk}]"

    # 2) source attribution -> description (preserve credit, strip the raw field)
    src = fm.get("source") or idx.get("source")
    if src and "source:" not in desc.lower() and "来源" not in desc:
        desc = f"{desc} (source: {src})"

    if desc:
        fm["description"] = desc

    # 3) strip MY_SKILL-only fields (user-invocable stays)
    for key in STRIP_FIELDS:
        fm.pop(key, None)

    return fm, body


def sync(target_dir, dry_run=False, force=False):
    with open(INDEX, encoding="utf-8") as f:
        index = yaml.safe_load(f)
    skip_list = load_skip_list()
    target = Path(target_dir).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)

    installed, skipped = [], []
    index_by_name = {s["name"]: s for s in index["skills"]}

    for skill in index["skills"]:
        name = skill["name"]

        if name in skip_list and not force:
            skipped.append((name, "in skip-list (use --force to override)"))
            print(f"SKIP {name}: in skip-list (use --force to override)")
            continue

        skill_src = REPO_ROOT / skill["path"]
        skill_md_src = skill_src / "SKILL.md"
        if not skill_md_src.exists():
            skipped.append((name, f"no SKILL.md at {skill['path']}"))
            print(f"SKIP {name}: SKILL.md not found at {skill['path']}")
            continue

        text = skill_md_src.read_text(encoding="utf-8")
        if not text.startswith("---"):
            skipped.append((name, "no frontmatter"))
            print(f"SKIP {name}: SKILL.md has no frontmatter")
            continue

        fm_end = text.index("---", 3)
        fm_raw = text[4:fm_end].strip()
        fm = yaml.safe_load(fm_raw) or {}
        body = text[fm_end + 3:].lstrip()

        new_fm, body = apply_nested_adapter(fm, body, index_by_name.get(name))
        new_text = "---\n" + yaml.dump(new_fm, allow_unicode=True, sort_keys=False) + "---\n\n" + body

        # Nested path preserves the meta/ + domain/ hierarchy.
        dest_dir = target / skill["path"]

        # Idempotency: skip unchanged (unless --force).
        if dest_dir.exists() and not force:
            existing_md = dest_dir / "SKILL.md"
            existing = existing_md.read_text(encoding="utf-8") if existing_md.exists() else ""
            if existing == new_text:
                installed.append(name)
                print(f"OK (up-to-date): {name} → {dest_dir}")
                continue
            print(f"WARN {name}: exists, overwriting (use --force to silence)")

        if dry_run:
            print(f"DRY-RUN: would write {dest_dir}")
        else:
            _copytree_overwrite(skill_src, dest_dir)
            (dest_dir / "SKILL.md").write_text(new_text, encoding="utf-8")
            print(f"OK: {name} → {dest_dir}")
        installed.append(name)

    print("\n=== Summary ===")
    print(f"Target   : {target}")
    print(f"Installed: {len(installed)} -> {installed}")
    print(f"Skipped  : {len(skipped)} -> {[n for n,_ in skipped]}")
    if not force and skip_list:
        print(f"Note     : {len(skip_list & set(n for n,_ in skipped))} skill(s) skipped via skip.yaml. "
              f"Pass --force to install all.")


def main():
    parser = argparse.ArgumentParser(description="Nested-install MY_SKILL into WorkBuddy (preserves tree)")
    parser.add_argument("--target", default=str(DEFAULT_TARGET),
                        help="Destination skills dir (default: ~/.workbuddy/skills/MY_SKILL)")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no writes")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing skills AND install skip-list skills")
    args = parser.parse_args()
    sync(args.target, args.dry_run, args.force)


if __name__ == "__main__":
    main()
