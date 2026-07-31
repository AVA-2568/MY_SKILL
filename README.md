> 中文版本: [README.zh-CN.md](./README.zh-CN.md)

[![CI](https://github.com/AVA-2568/MY_SKILL/actions/workflows/validate.yaml/badge.svg)](https://github.com/AVA-2568/MY_SKILL/actions/workflows/validate.yaml)
[![License: MIT](https://img.shields.io/github/license/AVA-2568/MY_SKILL?label=license)](./LICENSE)
[![Skills](https://img.shields.io/badge/skills-8-blue)](./meta/distributor/INDEX.yaml)
[![Platforms](https://img.shields.io/badge/platforms-workbuddy%20%7C%20codex%20%7C%20hermes-0F6E56)](./docs/adr/0002-protocol-compatible-adapters.md)

# MY_SKILL

Skill **infrastructure** for cross-platform AI agents — not another skill library. Solves two problems:

1. **N platforms × M skills** — import once, install anywhere (workbuddy / codex / hermes).
2. **Model hallucination** ("installed but ignored") — three-layer anti-hallucination triad.

## Why not just use obra/superpowers?

You should — for skills. MY_SKILL doesn't compete on content. It competes on the **pipe**: how skills get registered, discovered, routed, and enforced across platforms. Skills from superpowers, mattpocock/skills, or your own repo all flow through the same infrastructure.

## The anti-hallucination triad

Models ignore installed skills for three reasons. MY_SKILL covers all three:

| Cause | Owner | Mechanism |
|---|---|---|
| Model never loaded skill description | Distributor | Session-start injection forces all descriptions into context |
| Model loaded but mis-routes | Distributor | Keyword routes + fuzzy score pick the match; model doesn't choose freely |
| Model routed but skipped execution | Review | Reflection Gate re-injects "you mentioned X but did not execute it" |

No other layer (model, platform, superpowers) catches cause 3.

## Sync workflow (cross-machine / cross-platform)

MY_SKILL repo is your personal skill hub. GitHub is the cloud relay. **Core contract: editing happens only in the repo; the platform directory is a read-only consumer.**

### Platform A (edit skills)

1. Edit SKILL.md directly in the MY_SKILL repo (**never edit on the platform side**)
2. `installer sync` to install to the current platform
3. `git push` to sync to GitHub

### Platform B (one-shot install)

On a new machine / new agent, tell the model: **"install MY_SKILL"**

The model will automatically:
1. `git clone https://github.com/AVA-2568/MY_SKILL.git ~/MY_SKILL` (or `git pull` if exists)
2. Detect the current platform (workbuddy / codex / hermes)
3. Run `sync.py --auto-detect` to install all skills
4. Report the result

Or run the script directly:
```bash
curl -fsSL https://raw.githubusercontent.com/AVA-2568/MY_SKILL/main/meta/installer/scripts/install.sh | bash
```

### Key contracts

| Contract | Why |
|---|---|
| **Edit only in the repo** | Keeps the canonical source clean; no platform-format pollution flows back |
| **Platform dir is read-only** | Synced derivatives are overwritten on next sync; don't hand-edit them |
| **GitHub is the only relay** | Don't transfer skills via USB / email; always go through GitHub |

Under this model **no "denormalization" is needed** — because editing always happens in the repo, the repo stays clean.

## Architecture

```
External skills (superpowers / mattpocock / your repo)
    │
    ▼
[importer.py] ── pull + normalize frontmatter ──▶ domain/<category>/<name>/
    │
    ▼
[INDEX.yaml] ── registry (8 skills: 5 meta + 3 domain)
    │
    ├──▶ [Distributor] session-start: inject all descriptions into context
    │                  per-task: keyword + fuzzy route to top-1 skill
    │                        │
    │                        ▼
    │                  [Domain skill] executes
    │                        │
    │                        ▼
    │                  [Review] Reflection Gate: did model actually call it?
    │
    └──▶ [Installer] adapters/ ── translate to workbuddy/codex/hermes
                      bootstrap/ ── verify session-start state
```

## Modules

### Meta (5)

| Module | Role | Invocable |
|---|---|---|
| **distributor** | Discoverability guarantor + skill router | `always_active` (not user-invocable) |
| **installer** | Importer + 3-platform adapters + bootstrap | yes |
| **installer-bootstrap** | Session-start verification | no (auto on session start) |
| **domain-entry** | Browse the skill registry | yes |
| **review** | Reflection Gate + Lifecycle Governance | no (horizontal, force-triggered) |

### Domain (3)

Only skills with **no ecosystem equivalent** are kept as seeds. Everything else is imported on demand.

| Skill | Category | Why kept |
|---|---|---|
| `decide-invest` | decision | Financial decision — no public equivalent |
| `ui-design` | generation | Visual spec output — superpowers does engineering flow, not visual design |
| `ux-design` | generation | User journey / information architecture — UX-specific |

Import more with: `python meta/installer/scripts/importer.py owner/repo`

## Decisions

| # | Decision | Status |
|---|---|---|
| [0001](./docs/adr/0001-full-autonomous-rebuild.md) | Full autonomous rebuild | accepted |
| [0002](./docs/adr/0002-protocol-compatible-adapters.md) | Protocol compatible + per-platform adapters | accepted |
| [0003](./docs/adr/0003-four-verticals-one-horizontal.md) | 4 verticals + 1 horizontal layer | superseded by 0008 |
| [0004](./docs/adr/0004-review-subsystem.md) | Review subsystem (3 gates + lifecycle) | superseded by 0008 |
| [0005](./docs/adr/0005-b-chain-vertical-roles.md) | B-Chain trigger + vertical roles | superseded by 0008 |
| [0006](./docs/adr/0006-domain-five-llm-capabilities.md) | Domain: 5 LLM capabilities | superseded by 0008 |
| [0007](./docs/adr/0007-mvp-minimum-viable.md) | MVP: 8 modules + 18 seeds | superseded by 0008 |
| [0008](./docs/adr/0008-slim-infra-not-content-library.md) | **Slim infrastructure, not content library** | **accepted (current)** |

## Layout

```
MY_SKILL/
├── docs/adr/                # 8 ADRs (0008 is current truth)
├── CONTEXT.md               # Glossary / ubiquitous language
├── meta/                    # 5 metadata modules
│   ├── distributor/         # discoverability guarantor + router
│   │   ├── SKILL.md
│   │   ├── INDEX.yaml       # 8-skill registry + routing + lifecycle config
│   │   └── scripts/score.py # keyword + fuzzy router
│   ├── installer/           # importer + adapters + bootstrap
│   │   ├── scripts/
│   │   │   ├── sync.py      # install to platforms (supports --auto-detect)
│   │   │   ├── sync_nested.py
│   │   │   ├── importer.py  # pull skills from GitHub/local
│   │   │   └── install.sh   # one-shot install (clone + sync)
│   │   ├── adapters/        # workbuddy.yaml / codex.yaml / hermes.yaml
│   │   └── bootstrap/       # session-start verification
│   ├── domain-entry/        # browsing entrypoint
│   └── review/              # Reflection Gate + Lifecycle
├── domain/                  # 3 seed skills (no ecosystem equivalent)
│   ├── decision/decide-invest/
│   └── generation/{ui-design,ux-design}/
├── tests/fixtures/          # route-cases.yaml
├── AGENTS.md                # Agent entrypoint
└── README.md
```

## Usage

### One-shot install (new machine)

```bash
# Run when the model says "install MY_SKILL"; or directly:
curl -fsSL https://raw.githubusercontent.com/AVA-2568/MY_SKILL/main/meta/installer/scripts/install.sh | bash

# Or manually:
bash meta/installer/scripts/install.sh
```

> **Windows**: use Git Bash (ships with Git for Windows) to run `install.sh`.
> Without Git Bash, run `sync.py` directly — see [docs/INSTALL.md](./docs/INSTALL.md#manual-fallback-no-agent-available).

### Import skills from any repo

```bash
python meta/installer/scripts/importer.py obra/superpowers          # scan whole repo
python meta/installer/scripts/importer.py mattpocock/skills/productivity/handoff
python meta/installer/scripts/importer.py --local /path/to/my/skill --category generation
```

### Install to current platform

```bash
python meta/installer/scripts/sync.py --auto-detect          # auto-detect platform
python meta/installer/scripts/sync.py --target ~/.workbuddy/skills/
```

Or talk to the agent: "install MY_SKILL to WorkBuddy" / "把 MY_SKILL 装到 WorkBuddy".

### Route tasks

Distributor runs automatically on every session + every task. No manual invocation needed.

## Documentation

| Doc | Purpose |
|---|---|
| [README.md](./README.md) | Architecture + layout (this file, English) |
| [README.zh-CN.md](./README.zh-CN.md) | 中文版 |
| [CONTEXT.md](./CONTEXT.md) | Glossary / ubiquitous language |
| [AGENTS.md](./AGENTS.md) | Agent read order when working in this repo |
| [docs/INSTALL.md](./docs/INSTALL.md) | Install / deploy skills to a platform |
| [docs/adr/0008](./docs/adr/0008-slim-infra-not-content-library.md) | Current architectural truth |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | AI agent contribution guidelines |
| [CHANGELOG.md](./CHANGELOG.md) | Version history |
| [LICENSE](./LICENSE) | MIT |

## Local development first

This repository is developed locally first. Clone it anywhere — the `meta/` and `domain/` layouts work as-is.
