#!/usr/bin/env python3
"""Installer sync — translates MY_SKILL → platform skill directory.

Usage:
    python sync.py --auto-detect                          # detect platform, install
    python sync.py --target ~/.workbuddy/skills/          # explicit target (workbuddy)
    python sync.py --platform codex --target ~/.codex/skills/  # explicit platform
    python sync.py --auto-detect --dry-run                # preview only
    python sync.py --target /path --force                 # overwrite existing

Reads INDEX.yaml, applies the per-platform adapter (workbuddy / codex / hermes),
writes platform-ready SKILL.md files under <target>/<skill-name>/.

Platform directory is a read-only consumer. Edit skills only in the MY_SKILL
repo (canonical source); re-run sync to propagate changes.
"""

import sys, os, argparse
from pathlib import Path

# All shared logic lives in common.py — edit adapter rules there.
from common import (
    REPO_ROOT, INDEX, load_skip_list, load_index,
    parse_skill_md, serialize_skill_md, copytree_overwrite, apply_adapter,
)

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


def sync(target_dir, adapter_name, dry_run=False, force=False):
    index = load_index()
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
        fm, body = parse_skill_md(text)

        # Dispatch to the platform-specific adapter (workbuddy / codex / hermes).
        new_fm, body = apply_adapter(adapter_name, fm, body, index_by_name.get(name))
        new_text = serialize_skill_md(new_fm, body)

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
            copytree_overwrite(skill_src, dest_dir)
            (dest_dir / "SKILL.md").write_text(new_text, encoding="utf-8")
            print(f"OK: {name} → {dest_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Sync MY_SKILL to a platform skills directory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python sync.py --auto-detect                          # detect platform, install
  python sync.py --target ~/.workbuddy/skills/          # explicit target
  python sync.py --platform codex --target ~/.codex/skills/  # explicit platform
  python sync.py --auto-detect --dry-run                # preview only
  python sync.py --target /path --force                 # overwrite existing
""",
    )
    parser.add_argument("--target", default=None,
                        help="Platform skills directory (e.g. ~/.workbuddy/skills/). "
                             "If omitted with --auto-detect, will be filled in.")
    parser.add_argument("--platform", default=None, choices=["workbuddy", "codex", "hermes"],
                        help="Explicit platform. If omitted, inferred from --target path "
                             "or auto-detected.")
    parser.add_argument("--auto-detect", action="store_true",
                        help="Auto-detect installed platform and target directory.")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no writes")
    parser.add_argument("--force", action="store_true", help="Overwrite existing skills")
    args = parser.parse_args()

    target = args.target
    adapter_name = args.platform

    if args.auto_detect:
        name, detected_target, detected_adapter = detect_platform()
        if name is None:
            print("ERROR: no supported platform detected. "
                  "Looked for: " + ", ".join(p["name"] for p in PLATFORMS),
                  file=sys.stderr)
            print("Pass --target explicitly, e.g. --target ~/.workbuddy/skills/",
                  file=sys.stderr)
            sys.exit(1)
        if target is None:
            target = str(detected_target)
        if adapter_name is None:
            adapter_name = detected_adapter
        print(f"Detected platform: {name}")
        print(f"Target directory:  {target}")

    # Infer adapter from target path if only --target was given.
    if adapter_name is None and target:
        for p in PLATFORMS:
            if f".{p['name']}" in str(target):
                adapter_name = p["adapter"]
                break
    if adapter_name is None:
        adapter_name = "workbuddy"  # safe fallback

    if not target:
        parser.error("either --target or --auto-detect is required")

    if adapter_name != "workbuddy":
        print(f"Using adapter: {adapter_name}")

    sync(target, adapter_name, args.dry_run, args.force)


if __name__ == "__main__":
    main()
