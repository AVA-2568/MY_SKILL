---
name: installer
description: Translate MY_SKILL's generic SKILL.md into platform-specific formats (workbuddy / codex / hermes) and bootstrap session activation. Two internal sub-modules — adapters/ (per-platform translation) + bootstrap/ (session activation). Manually invocable via `installer sync` and `installer install`.
user-invocable: true
risk_level: mid
---

# Installer (安装配置器)

Two sub-modules. **Not on the B-Chain runtime path**; runs when skills enter or leave the library, and at session start.

## Sub-modules

### `adapters/`

Per-platform translation. Three adapters: workbuddy / codex / hermes. **Implemented as `adapters/workbuddy.yaml`, `adapters/codex.yaml`, `adapters/hermes.yaml`** — each file holds the exact field mapping below.

For each platform, map MY_SKILL's extension fields to the platform's expected format:

| MY_SKILL field | workbuddy | codex | hermes |
|---|---|---|---|
| `risk_level` | (not native; encode in description) | (not native) | (not native) |
| `verifiable` | (not native) | (not native) | (not native) |
| `user-invocable: false` | `disable-model-invocation: true` | `disable-model-invocation: true` | (not native; rely on description) |
| `category` | (in `metadata`) | (in `metadata`) | (in `metadata.hermes.tags`) |

**Core fields** (`name`, `description`) pass through unchanged per ADR-0002.

### `bootstrap/`

**Implemented as `bootstrap/SKILL.md`.** Session activation. On session start:
1. Verify Distributor is `user-invocable: false` and always-loaded.
2. Verify all other skills remain on-demand.
3. Verify INDEX.yaml matches the actual `domain/` + `meta/` directory contents; rebuild if drift detected.
4. Report any installation issues to the user.

## Trigger

- **Manual**: `installer sync` to run all adapters and update installed skills on each platform.
- **Manual**: `installer install <skill-name> --platform=<workbuddy|codex|hermes>` to install a single skill on a specific platform.
- **Auto**: on session start, `bootstrap/` runs once.

## Procedure (sync)

1. Read INDEX.yaml to get the canonical skill list.
2. For each skill, run each platform's adapter; write the platform-specific output to the platform's skill directory.
3. Verify by listing each platform's installed skills; report any mismatch.

## Pitfalls

- **Field drift**: Platform SKILL.md field names change between platform versions; pin to a known version.
- **Index staleness**: INDEX.yaml can drift from actual `domain/` directory; the bootstrap pass should detect this and rebuild.
- **Cross-platform divergence**: A feature MY_SKILL adds (e.g., new frontmatter field) won't appear on platforms that don't support it; the adapter must translate or document the gap.
- **Network safety**: Installing to remote platforms may need credentials; never embed secrets in the adapter output.

## Verification

- After sync, each platform's skill directory should contain the same set of skills as INDEX.yaml.
- After bootstrap, the session should have Distributor loaded and INDEX.yaml readable.
- Any drift between INDEX.yaml and filesystem must be reported and resolved before continuing.
