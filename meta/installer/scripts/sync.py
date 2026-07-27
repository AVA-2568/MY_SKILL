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

# Skills to skip during sync (overlap/conflict with user's existing skills)
SKIP_LIST = {"thinking-first", "caveman", "decide-invest"}


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
    # Strip MY_SKILL-only fields
    for key in ["agent_created", "risk_level", "category", "horizontal",
                "always_active", "source", "data_layer", "related"]:
        fm.pop(key, None)
    return fm, body


def sync(target_dir, dry_run=False, force=False):
    with open(INDEX, encoding="utf-8") as f:
        index = yaml.safe_load(f)
    target = Path(target_dir).expanduser().resolve()
    os.makedirs(target, exist_ok=True)

    for skill in index["skills"]:
        name = skill["name"]

        # Skip listed skills
        if name in SKIP_LIST and not force:
            print(f"SKIP {name}: in skip-list (use --force to override)")
            continue

        skill_path = REPO_ROOT / skill["path"] / "SKILL.md"
        if not skill_path.exists():
            print(f"SKIP {name}: SKILL.md not found at {skill_path}")
            continue

        text = skill_path.read_text(encoding="utf-8")
        fm_end = text.index("---", 3)
        fm_raw = text[4:fm_end].strip()
        fm = yaml.safe_load(fm_raw) or {}
        body = text[fm_end + 3:].lstrip()

        new_fm, body = apply_workbuddy_adapter(fm, body)
        new_text = "---\n" + yaml.dump(new_fm, allow_unicode=True, sort_keys=False) + "---\n\n" + body

        dest = target / name / "SKILL.md"

        # Skip if identical already exists
        if dest.exists() and not force:
            existing = dest.read_text(encoding="utf-8")
            if existing == new_text:
                print(f"SKIP {name}: already up-to-date")
                continue
            print(f"WARN {name}: exists (use --force to overwrite)")

        if dry_run:
            print(f"DRY-RUN: would write {dest}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(new_text, encoding="utf-8")
            print(f"OK: {name} → {dest}")


def main():
    parser = argparse.ArgumentParser(description="Sync MY_SKILL to WorkBuddy")
    parser.add_argument("--target", required=True, help="WorkBuddy skills directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no writes")
    parser.add_argument("--force", action="store_true", help="Overwrite existing skills")
    args = parser.parse_args()
    sync(args.target, args.dry_run, args.force)


if __name__ == "__main__":
    main()
