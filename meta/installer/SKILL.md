---
name: installer
description: "Source-agnostic skill importer + cross-platform adapter + session bootstrap. Import skills from any GitHub repo or local path (importer.py), translate generic SKILL.md into platform formats (workbuddy/codex/hermes), and verify session-start state. Manually invocable via `installer sync`, `installer install`, `installer import`."
user-invocable: true
risk_level: mid
category: meta
---

# Installer (安装配置器)

Three sub-modules. **Not on the runtime path**; runs when skills enter or leave the library, and at session start.

## Sub-modules

### `scripts/importer.py` — source-agnostic importer

Pulls skills from any source that follows the SKILL.md convention:

```
python importer.py owner/repo                    # scan GitHub repo for SKILL.md
python importer.py owner/repo/path/to/skill      # specific path in repo
python importer.py --local /path/to/skill        # from local directory
python importer.py owner/repo --category decision  # override category
```

Normalizes frontmatter (ensures `name`/`description`/`category`/`risk_level`/`user-invocable`), copies to `domain/<category>/<name>/`, and registers in INDEX.yaml. Works with `obra/superpowers`, `mattpocock/skills`, or any repo.

### `adapters/`

Per-platform translation. Three adapters: workbuddy / codex / hermes. **Implemented as `adapters/workbuddy.yaml`, `adapters/codex.yaml`, `adapters/hermes.yaml`** — each file holds the exact field mapping below.

For each platform, map MY_SKILL's extension fields to the platform's expected format:

| MY_SKILL field | workbuddy | codex | hermes |
|---|---|---|---|
| `risk_level` | (not native; encode in description) | (not native) | (not native) |
| `verifiable` | (not native) | (not native) | (not native) |
| `user-invocable: false` | `user-invocable: false` (preserved as-is; native WorkBuddy field) | `disable-model-invocation: true` | (not native; rely on description) |
| `category` | (in `metadata`) | (in `metadata`) | (in `metadata.hermes.tags`) |

**Core fields** (`name`, `description`) pass through unchanged per ADR-0002.

### `bootstrap/`

**Implemented as `bootstrap/SKILL.md`.** Session activation. On session start:
1. Verify Distributor is `user-invocable: false` and `always_active: true`.
2. Verify all other skills remain on-demand.
3. Verify INDEX.yaml matches the actual `domain/` + `meta/` directory contents; rebuild if drift detected.
4. Report any installation issues to the user.

## Trigger

- **Manual**: `installer import owner/repo` to pull skills from a GitHub repo.
- **Manual**: `installer sync` to run all adapters and update installed skills on each platform.
- **Manual**: `installer install <skill-name> --platform=<workbuddy|codex|hermes>` to install a single skill on a specific platform.
- **Auto**: on session start, `bootstrap/` runs once.

## Procedure (sync)

1. Read INDEX.yaml to get the canonical skill list.
2. For each skill, run each platform's adapter; write the platform-specific output to the platform's skill directory.
3. Verify by listing each platform's installed skills; report any mismatch.

## Procedure (import)

1. Parse the source spec (`owner/repo` or `--local path`).
2. Scan for SKILL.md files.
3. For each: parse frontmatter, normalize fields, write to `domain/<category>/<name>/`.
4. Register in INDEX.yaml (idempotent — replaces existing entry with same name).

## Pitfalls

- **Field drift**: Platform SKILL.md field names change between platform versions; pin to a known version.
- **Index staleness**: INDEX.yaml can drift from actual `domain/` directory; the bootstrap pass should detect this and rebuild.
- **Import conflicts**: if importing a skill whose name already exists, importer replaces it. Use `--name` to override if you want both.
- **Network safety**: Installing to remote platforms may need credentials; never embed secrets in the adapter output.

## Verification

- After sync, each platform's skill directory should contain the same set of skills as INDEX.yaml.
- After import, the new skill should appear in INDEX.yaml and be routable by Distributor.
- After bootstrap, the session should have Distributor loaded and INDEX.yaml readable.
- Any drift between INDEX.yaml and filesystem must be reported and resolved before continuing.
