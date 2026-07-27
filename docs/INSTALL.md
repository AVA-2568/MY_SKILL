# Installing MY_SKILL skills to WorkBuddy

## Quick start

```bash
cd /path/to/MY_SKILL
python meta/installer/scripts/sync.py --target ~/.workbuddy/skills --dry-run
# Review the DRY-RUN output; if OK:
python meta/installer/scripts/sync.py --target ~/.workbuddy/skills
```

## Safety rules

1. **同名不覆盖** — If a skill already exists at the target with the same name, skip and warn. Use `--force` to overwrite.
2. **冲突技能黑名单** — These skills default to skip because they overlap with existing user-level skills:
   - `thinking-first` — may semantically diverge from the user's existing `thinking-first`. Skipped by default.
   - `caveman` — overlaps with `token-economy` in purpose. Skipped by default.
   - `decide-invest` — not enriched enough for safe installation (conflicts with `stock-analysis`, `trading-decision`). Skipped by default.
3. **金融类技能** — Skills in `decision/` category default to `mid` risk; installer warns before installing.
4. **安装后** — Restart WorkBuddy or wait for the next session to load new skills.

## Uninstall

```bash
# Remove an installed skill's entire directory
rm -rf ~/.workbuddy/skills/<skill-name>
# This does NOT affect the MY_SKILL source repository
```

## `--force` usage

```bash
# Overwrite an existing skill (bypasses the "exists" check)
python meta/installer/scripts/sync.py --target ~/.workbuddy/skills --force

# Override the skip-list for blacklisted skills
python meta/installer/scripts/sync.py --target ~/.workbuddy/skills --force
```

## Verification

After installation, run:

```bash
# List installed skills
ls ~/.workbuddy/skills/

# Verify a specific skill has the expected frontmatter
head -5 ~/.workbuddy/skills/<skill-name>/SKILL.md
```

The Distributor and horizontal skills (`thinking-first`, `caveman`, `review`) have `disable-model-invocation: true` after adapter translation, meaning they load automatically every session. All domain skills remain user-invocable (`user-invocable: true` in MY_SKILL, stripped to default by adapter).
