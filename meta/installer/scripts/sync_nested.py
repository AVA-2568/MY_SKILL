#!/usr/bin/env python3
"""Nested installer — installs MY_SKILL into WorkBuddy while preserving the
meta/ + domain/ folder hierarchy.

Why a second script (vs. sync.py)?
    sync.py flattens skills into <target>/<name>/. sync_nested.py keeps the
    full directory tree (<target>/MY_SKILL/<rel>/) — useful when you want to
    browse the repo layout inside the platform's skills directory.

    Both scripts now share the same adapter dispatching via common.py, so
    field translation (workbuddy/codex/hermes) is consistent between them.

Usage:
    # dry-run preview (no writes)
    python sync_nested.py --dry-run

    # install all skills into ~/.workbuddy/skills/MY_SKILL
    python sync_nested.py --force

    # install into a custom target, skipping the skip-list skills
    python sync_nested.py --target /path/to/skills/MY_SKILL

Safe to re-run: overwrites in place, never deletes dst contents.
"""

import argparse
from pathlib import Path

# All shared logic lives in common.py — edit adapter rules there.
from common import (
    REPO_ROOT, load_skip_list, load_index,
    parse_skill_md, serialize_skill_md, copytree_overwrite, apply_adapter,
)

DEFAULT_TARGET = Path.home() / ".workbuddy" / "skills" / "MY_SKILL"
DEFAULT_ADAPTER = "workbuddy"  # nested install is WorkBuddy-specific by convention


def sync(target_dir, adapter_name=DEFAULT_ADAPTER, dry_run=False, force=False):
    index = load_index()
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
        fm, body = parse_skill_md(text)

        new_fm, body = apply_adapter(adapter_name, fm, body, index_by_name.get(name))
        new_text = serialize_skill_md(new_fm, body)

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
            copytree_overwrite(skill_src, dest_dir)
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
    parser.add_argument("--platform", default=DEFAULT_ADAPTER, choices=["workbuddy", "codex", "hermes"],
                        help="Adapter to use (default: workbuddy)")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no writes")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing skills AND install skip-list skills")
    args = parser.parse_args()
    sync(args.target, args.platform, args.dry_run, args.force)


if __name__ == "__main__":
    main()
