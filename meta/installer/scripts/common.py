#!/usr/bin/env python3
"""Shared helpers for sync.py and sync_nested.py.

Keeps the per-platform adapter dispatching + frontmatter parsing in one place
so both installers stay in sync. Edit adapter logic here, not in the scripts.
"""

import re
import shutil
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
INDEX = REPO_ROOT / "meta" / "distributor" / "INDEX.yaml"
SKIP_CONFIG = REPO_ROOT / "meta" / "installer" / "skip.yaml"

# Skills withheld from auto-deploy (overlap/conflict with user's existing skills).
DEFAULT_SKIP_LIST = {"decide-invest"}

# MY_SKILL-only extension fields with no platform equivalent. Stripped on install.
# NOTE: `user-invocable` is intentionally NOT in this list — it is a WorkBuddy
# native field (hide from menu / callable internally) and must be preserved
# (or translated per-platform) by the adapter.
STRIP_FIELDS = [
    "risk_level", "category", "horizontal", "always_active",
    "source", "data_layer", "related", "forced_trigger",
]

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def load_skip_list():
    if not SKIP_CONFIG.exists():
        return set(DEFAULT_SKIP_LIST)
    with open(SKIP_CONFIG, encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    return set(cfg.get("skip_list", DEFAULT_SKIP_LIST))


def load_index():
    with open(INDEX, encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_skill_md(text):
    """Split SKILL.md into (frontmatter_dict, body_str).

    Robust against `---` appearing inside the description: uses the same regex
    as importer.py / score.py instead of str.index.
    """
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm = yaml.safe_load(m.group(1)) or {}
    body = text[m.end():]
    return fm, body


def serialize_skill_md(fm, body):
    return "---\n" + yaml.dump(fm, allow_unicode=True, sort_keys=False) + "---\n\n" + body


def copytree_overwrite(src, dst):
    """Copy src tree into dst, overwriting files in place. Never deletes dst
    contents — avoids bulk-delete gates and is safe for incremental updates."""
    for item in src.rglob("*"):
        if item.is_file():
            rel = item.relative_to(src)
            target = dst / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


# ── Adapter dispatch ──────────────────────────────────────────────────

def _fold_risk_and_source(fm, index_entry):
    """Fold risk_level + source attribution into description.

    Shared by all adapters — only the field stripping / user-invocable handling
    differs per platform.
    """
    idx = index_entry or {}
    risk = str(fm.get("risk_level") or idx.get("risk_level") or "low").lower()
    desc = fm.get("description", "") or ""
    if risk != "low" and f"risk={risk}" not in desc.lower():
        desc = f"{desc} [risk={risk}]"

    src = fm.get("source") or idx.get("source")
    if src and "source:" not in desc.lower() and "来源" not in desc:
        desc = f"{desc} (source: {src})"

    if desc:
        fm["description"] = desc


def apply_workbuddy_adapter(fm, body, index_entry=None):
    """WorkBuddy: preserve `user-invocable` as-is (native field, hide-from-menu
    but callable internally). Strip MY_SKILL-only extension fields."""
    fm = dict(fm)
    _fold_risk_and_source(fm, index_entry)
    for key in STRIP_FIELDS:
        fm.pop(key, None)
    return fm, body


def apply_codex_adapter(fm, body, index_entry=None):
    """Codex: translate `user-invocable: false` -> `disable-model-invocation: true`
    (Codex native field). Strip MY_SKILL-only extension fields."""
    fm = dict(fm)
    _fold_risk_and_source(fm, index_entry)

    if fm.get("user-invocable") is False:
        fm.pop("user-invocable", None)
        fm["disable-model-invocation"] = True

    for key in STRIP_FIELDS:
        fm.pop(key, None)
    return fm, body


def apply_hermes_adapter(fm, body, index_entry=None):
    """Hermes: no native user-invocable flag. Encode the constraint in description
    for horizontal / internal skills; strip MY_SKILL-only extension fields."""
    fm = dict(fm)
    _fold_risk_and_source(fm, index_entry)

    if fm.get("user-invocable") is False:
        desc = fm.get("description", "") or ""
        note = "Do not invoke unless called by distributor."
        if note.lower() not in desc.lower():
            desc = f"{desc} {note}".strip()
        fm["description"] = desc
        fm.pop("user-invocable", None)

    for key in STRIP_FIELDS:
        fm.pop(key, None)
    return fm, body


ADAPTERS = {
    "workbuddy": apply_workbuddy_adapter,
    "codex": apply_codex_adapter,
    "hermes": apply_hermes_adapter,
}


def apply_adapter(adapter_name, fm, body, index_entry=None):
    """Dispatch to the per-platform adapter. Falls back to workbuddy if unknown."""
    fn = ADAPTERS.get(adapter_name, apply_workbuddy_adapter)
    return fn(fm, body, index_entry)
