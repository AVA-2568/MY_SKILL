#!/usr/bin/env bash
# install.sh — one-shot MY_SKILL installer.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/AVA-2568/MY_SKILL/main/meta/installer/scripts/install.sh | bash
#   bash install.sh                      # clone + sync to auto-detected platform
#   bash install.sh --target /custom/dir # override target
#   bash install.sh --dry-run            # preview only, no writes
#   bash install.sh --force              # overwrite existing skills
#
# What it does:
#   1. Clone MY_SKILL repo to $MY_SKILL_HOME (default: ~/MY_SKILL)
#   2. Auto-detect installed agent platform (workbuddy / codex / hermes)
#   3. Run sync.py to install all skills to the detected platform directory
#
# Edit skills only in the repo (canonical source). The platform directory is a
# read-only consumer — never hand-edit synced skills there, or the next sync
# will overwrite your changes. See README "Sync workflow" section.

set -e

REPO_URL="https://github.com/AVA-2568/MY_SKILL.git"
MY_SKILL_HOME="${MY_SKILL_HOME:-$HOME/MY_SKILL}"
SCRIPT_DIR="meta/installer/scripts"

# ── Args ────────────────────────────────────────────────────────────────
TARGET=""
DRY_RUN=""
FORCE=""

while [ $# -gt 0 ]; do
    case "$1" in
        --target)  TARGET="$2"; shift 2 ;;
        --dry-run) DRY_RUN="--dry-run"; shift ;;
        --force)   FORCE="--force"; shift ;;
        -h|--help)
            sed -n '2,20p' "$0"
            exit 0 ;;
        *) echo "Unknown arg: $1" >&2; exit 1 ;;
    esac
done

# ── Step 1: clone or update repo ────────────────────────────────────────
if [ -d "$MY_SKILL_HOME/.git" ]; then
    echo "[1/3] MY_SKILL already at $MY_SKILL_HOME — pulling latest..."
    cd "$MY_SKILL_HOME"
    git pull --ff-only
else
    echo "[1/3] Cloning MY_SKILL to $MY_SKILL_HOME..."
    git clone "$REPO_URL" "$MY_SKILL_HOME"
    cd "$MY_SKILL_HOME"
fi

# ── Step 2 + 3: build sync.py args and run ─────────────────────────────
# Only pass --target when explicitly set; otherwise let sync.py auto-detect.
SYNC_ARGS=""
if [ -n "$TARGET" ]; then
    echo "[2/3] Using provided target: $TARGET"
    SYNC_ARGS="$SYNC_ARGS --target $TARGET"
else
    echo "[2/3] Detecting agent platform..."
    SYNC_ARGS="$SYNC_ARGS --auto-detect"
fi
[ -n "$DRY_RUN" ] && SYNC_ARGS="$SYNC_ARGS $DRY_RUN"
[ -n "$FORCE" ]  && SYNC_ARGS="$SYNC_ARGS $FORCE"

echo "[3/3] Syncing skills to platform..."
python "$SCRIPT_DIR/sync.py" $SYNC_ARGS || {
    echo ""
    echo "Install failed. If python is not on PATH, try: py -3 $SCRIPT_DIR/sync.py ..."
    echo "If you're on Windows without git bash, run sync.py directly:"
    echo "  python $SCRIPT_DIR/sync.py --auto-detect"
    exit 1
}

echo ""
echo "Done. Skills installed. Tell the agent: \"sync MY_SKILL\" or \"install MY_SKILL\" to re-run."
echo "Edit skills only in: $MY_SKILL_HOME  (canonical source)"
