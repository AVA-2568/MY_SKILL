#!/usr/bin/env python3
"""Installer sync — translates MY_SKILL → WorkBuddy skill directory.

Usage:
    python sync.py --target ~/.workbuddy/skills/ [--dry-run]

Reads INDEX.yaml, applies workbuddy adapter rules, writes platform-ready
SKILL.md files under <target>/<skill-name>/.
"""

import sys, yaml, shutil, argparse, os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
INDEX = REPO_ROOT / "meta" / "distributor" / "INDEX.yaml"
SKIP_CONFIG = REPO_ROOT / "meta" / "installer" / "skip.yaml"

# Skills to skip during sync (overlap/conflict with user's existing skills).
# Loaded from meta/installer/skip.yaml; falls back to this set if the file is
# missing so sync.py never breaks on a bare checkout.
DEFAULT_SKIP_LIST = {"thinking-first", "caveman", "decide-invest"}


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


def apply_workbuddy_adapter(frontmatter, body):
    """Translate extension fields per workbuddy.yaml rules."""
    fm = dict(frontmatter)
    # risk_level → append to description
    risk = fm.get("risk_level", "low")
    if risk != "low" and "risk" not in fm.get("description", "").lower():
        fm["description"] = fm.get("description", "") + f" [risk={risk}]"
    # user-invocable: false → disable-model-invocation: true
    if fm.get("user-invocable") is False:
        fm["disable-model-invocation"] = True
        fm.pop("user-invocable", None)
    else:
        fm.pop("user-invocable", None)
    # Strip MY_SKILL-only fields (keep agent_created so user-level install
    # survives app's builtin-skill sync/restore)
    for key in ["risk_level", "category", "horizontal",
                "always_active", "source", "data_layer", "related"]:
        fm.pop(key, None)
    return fm, body


def sync(target_dir, dry_run=False, force=False):
    with open(INDEX, encoding="utf-8") as f:
        index = yaml.safe_load(f)
    skip_list = load_skip_list()
    target = Path(target_dir).expanduser().resolve()
    os.makedirs(target, exist_ok=True)

    for skill in index["skills"]:
        name = skill["name"]

        # Skip listed skills
        if name in skip_list and not force:
            print(f"SKIP {name}: in skip-list (use --force to override)")
            continue

        skill_src = REPO_ROOT / skill["path"]
        skill_md_src = skill_src / "SKILL.md"
        if not skill_md_src.exists():
            print(f"SKIP {name}: SKILL.md not found at {skill_md_src}")
            continue

        text = skill_md_src.read_text(encoding="utf-8")
        fm_end = text.index("---", 3)
        fm_raw = text[4:fm_end].strip()
        fm = yaml.safe_load(fm_raw) or {}
        body = text[fm_end + 3:].lstrip()

        new_fm, body = apply_workbuddy_adapter(fm, body)
        new_text = "---\n" + yaml.dump(new_fm, allow_unicode=True, sort_keys=False) + "---\n\n" + body

        dest_dir = target / name

        # Skip if identical already exists
        if dest_dir.exists() and not force:
            existing_md = dest_dir / "SKILL.md"
            existing = existing_md.read_text(encoding="utf-8") if existing_md.exists() else ""
            if existing == new_text:
                print(f"SKIP {name}: already up-to-date")
                continue
            print(f"WARN {name}: exists (use --force to overwrite)")

        if dry_run:
            print(f"DRY-RUN: would write {dest_dir}")
        else:
            _copytree_overwrite(skill_src, dest_dir)
            (dest_dir / "SKILL.md").write_text(new_text, encoding="utf-8")
            print(f"OK: {name} → {dest_dir}")


def main():
    parser = argparse.ArgumentParser(description="Sync MY_SKILL to WorkBuddy")
    parser.add_argument("--target", required=True, help="WorkBuddy skills directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no writes")
    parser.add_argument("--force", action="store_true", help="Overwrite existing skills")
    args = parser.parse_args()
    sync(args.target, args.dry_run, args.force)


if __name__ == "__main__":
    main()
