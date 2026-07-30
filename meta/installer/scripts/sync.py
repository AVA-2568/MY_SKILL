#!/usr/bin/env python3
"""Installer sync — translates MY_SKILL → platform skill directory.

Usage:
    python sync.py --auto-detect                          # detect platform, install
    python sync.py --target ~/.workbuddy/skills/          # explicit target
    python sync.py --auto-detect --dry-run                # preview only
    python sync.py --target /path --force                 # overwrite existing

Reads INDEX.yaml, applies platform adapter rules (workbuddy / codex / hermes),
writes platform-ready SKILL.md files under <target>/<skill-name>/.

Platform directory is a read-only consumer. Edit skills only in the MY_SKILL
repo (canonical source); re-run sync to propagate changes.
"""

import sys, yaml, shutil, argparse, os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
INDEX = REPO_ROOT / "meta" / "distributor" / "INDEX.yaml"
SKIP_CONFIG = REPO_ROOT / "meta" / "installer" / "skip.yaml"

# Skills to skip during sync (overlap/conflict with user's existing skills).
# Loaded from meta/installer/skip.yaml; falls back to this set if the file is
# missing so sync.py never breaks on a bare checkout.
DEFAULT_SKIP_LIST = {"decide-invest"}

# MY_SKILL-only extension fields with no platform equivalent. Stripped on install.
# NOTE: `user-invocable` is intentionally NOT in this list — it is a WorkBuddy
# native field (hide from menu / callable internally) and must be preserved.
# Kept in sync with sync_nested.py.STRIP_FIELDS.
STRIP_FIELDS = [
    "risk_level", "category", "horizontal", "always_active",
    "source", "data_layer", "related", "forced_trigger",
]

# Platform detection table — order matters: first match wins.
# `detect` is a sentinel file/dir whose presence indicates the platform is
# installed on this machine. `target` is the default skills directory.
PLATFORMS = [
    {
        "name": "workbuddy",
        "detect": Path.home() / ".workbuddy",
        "target": Path.home() / ".workbuddy" / "skills",
        "adapter": "workbuddy",
    },
    {
        "name": "codex",
        "detect": Path.home() / ".codex",
        "target": Path.home() / ".codex" / "skills",
        "adapter": "codex",
    },
    {
        "name": "hermes",
        "detect": Path.home() / ".hermes",
        "target": Path.home() / ".hermes" / "skills",
        "adapter": "hermes",
    },
]


def detect_platform():
    """Return (name, target_dir, adapter_name) for the first detected platform.
    Returns (None, None, None) if no platform is installed."""
    for p in PLATFORMS:
        if p["detect"].exists():
            return p["name"], p["target"], p["adapter"]
    return None, None, None


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


def apply_workbuddy_adapter(frontmatter, body, index_entry=None):
    """Translate extension fields per workbuddy.yaml rules.

    - Folds risk_level (from SKILL.md, falling back to INDEX.yaml) into the
      description as `[risk=...]` when non-low.
    - Folds `source` attribution into the description when present.
    - PRESERVES `user-invocable` exactly (no disable-model-invocation swap).
    - Strips MY_SKILL-only extension fields (STRIP_FIELDS).
    Kept in sync with sync_nested.py.apply_nested_adapter.
    """
    fm = dict(frontmatter)
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
    os.makedirs(target, exist_ok=True)
    index_by_name = {s["name"]: s for s in index["skills"]}

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

        new_fm, body = apply_workbuddy_adapter(fm, body, index_by_name.get(name))
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
    parser = argparse.ArgumentParser(
        description="Sync MY_SKILL to a platform skills directory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python sync.py --auto-detect                    # detect platform, install
  python sync.py --target ~/.workbuddy/skills/    # explicit target
  python sync.py --auto-detect --dry-run          # preview only
  python sync.py --target /path --force           # overwrite existing
""",
    )
    parser.add_argument("--target", default=None,
                        help="Platform skills directory (e.g. ~/.workbuddy/skills/). "
                             "If omitted with --auto-detect, will be filled in.")
    parser.add_argument("--auto-detect", action="store_true",
                        help="Auto-detect installed platform and target directory.")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no writes")
    parser.add_argument("--force", action="store_true", help="Overwrite existing skills")
    args = parser.parse_args()

    target = args.target

    if args.auto_detect:
        name, detected_target, adapter = detect_platform()
        if name is None:
            print("ERROR: no supported platform detected. "
                  "Looked for: " + ", ".join(p["name"] for p in PLATFORMS),
                  file=sys.stderr)
            print("Pass --target explicitly, e.g. --target ~/.workbuddy/skills/",
                  file=sys.stderr)
            sys.exit(1)
        if target is None:
            target = str(detected_target)
        print(f"Detected platform: {name}")
        print(f"Target directory:  {target}")

    if not target:
        parser.error("either --target or --auto-detect is required")

    sync(target, args.dry_run, args.force)


if __name__ == "__main__":
    main()
