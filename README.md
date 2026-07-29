> 中文版本: [README.zh-CN.md](./README.zh-CN.md)

[![CI](https://github.com/AVA-2568/MY_SKILL/actions/workflows/validate.yaml/badge.svg)](https://github.com/AVA-2568/MY_SKILL/actions/workflows/validate.yaml)
[![License: MIT](https://img.shields.io/github/license/AVA-2568/MY_SKILL?label=license)](./LICENSE)
[![Skills](https://img.shields.io/badge/skills-27-blue)](./meta/distributor/INDEX.yaml)
[![Platforms](https://img.shields.io/badge/platforms-workbuddy%20%7C%20codex%20%7C%20hermes-0F6E56)](./docs/adr/0002-protocol-compatible-adapters.md)

# MY_SKILL

A cross-platform AI skill library for WorkBuddy, Codex, and Hermes — built for personal use and continuously reconstructed by an AI agent.

## Highlights

- **4 verticals + 1 horizontal review layer** — clean separation between routing, building, installing, and the cross-cutting review gate.
- **Protocol-compatible** — generic `SKILL.md` conforms to the Anthropic Agent Skills standard; per-platform adapters translate to WorkBuddy / Codex / Hermes.
- **AI-driven deployment** — the `installer` skill does the install; you talk to the agent, you don't type shell commands.
- **Self-rebuilding** — short on a skill? the `Builder` vertical generates a new one on demand.

## Architecture

**4 Verticals + 1 Horizontal Layer** (see [ADR-0003](./docs/adr/0003-four-verticals-one-horizontal.md)):

```
                       ┌────────────────────────────────────────────────────┐
                       │   Horizontal Layer (force-triggered by Distributor) │
                       │  ┌─────────────┐  ┌─────────┐  ┌────────────────┐    │
                       │  │Review       │  │thinking-│  │grill-with-docs │    │
                       │  │ code/task/  │  │ first   │  │ (on-gap)       │    │
                       │  │ security +  │  │(pre)    │  │                │    │
                       │  │ lifecycle   │  └─────────┘  └────────────────┘    │
                       │  └─────────────┘  ┌─────────┐                        │
                       │                    │caveman  │                        │
                       │                    │(post)   │                        │
                       │                    └─────────┘                        │
                       └──────────────────────────┬─────────────────────────┘
                                                  │ force-triggers at specific flow points
                                                  ▼
User task  ──▶  [Distributor]  pre:thinking-first  →  route + risk-score + gap-detect
                      │ (matched)                              │ (gap)
                      ▼                                        ▼
                [Domain]       execute skill         [grill-with-docs] (on-gap)
                (5 LLM         (5 LLM                                  │
                 capabilities) capabilities)                          ▼
                      ▲                                       [Builder] confirm→plan→generate
                      │ re-route                              ↓
                [Builder]      confirm → plan → generate   [Distributor] re-route
                      ▲
                      │ gap detected
                      │
                [Distributor]

                [Installer]    adapter (per platform) +
                               bootstrap (session activation)
                — runs alongside, not part of B-Chain runtime —
```

The 4 verticals (Distributor / Builder / Installer / Domain-entry) load on demand. The horizontal layer holds 4 components that the Distributor force-triggers at specific flow points: thinking-first (pre-route) / Review (per-task + per-skill) / caveman (post-route) / grill-with-docs (on-gap).

## Decisions

| # | Decision | Status |
|---|---|---|
| [0001](./docs/adr/0001-full-autonomous-rebuild.md) | Full autonomous rebuild | accepted |
| [0002](./docs/adr/0002-protocol-compatible-adapters.md) | Protocol compatible (Anthropic standard) + per-platform adapters | accepted |
| [0003](./docs/adr/0003-four-verticals-one-horizontal.md) | 4 verticals + 1 horizontal layer (4 components) | accepted |
| [0004](./docs/adr/0004-review-subsystem.md) | Review subsystem: code / task / security + lifecycle governance + reflection gate | accepted |
| [0005](./docs/adr/0005-b-chain-vertical-roles.md) | B-Chain trigger + vertical roles | accepted |
| [0006](./docs/adr/0006-domain-five-llm-capabilities.md) | Domain: 5 LLM capabilities (Understanding / Generation / Retrieval / Execution / Decision) | accepted |
| [0007](./docs/adr/0007-mvp-minimum-viable.md) | MVP: 8 metadata modules + 18-22 seed skills | accepted |

## Horizontal Layer (4 components, all force-triggered by Distributor)

| Component | Trigger point | Role |
|---|---|---|
| **thinking-first** | pre-route | Cognitive discipline — 5 rules: understand / anchor to sources / surface uncertainty / pre-delivery check / minimal intervention |
| **Review** | per-task + per-skill | Code Review (soft) / Task Recheck (soft) / Security Review (reflective; hard gate on extreme risk) + Lifecycle Governance |
| **caveman** | pre-think + post-output | Pre-think caps reasoning at 3–5 short points; post-output compresses leftover verbosity. It shapes thinking, not just text. |
| **grill-with-docs** | on-gap | Design interrogation + ADR/glossary landing |

All 4 are `user-invocable: false` and cannot be triggered via a `/slash` command.

## Domain (5 LLM Capabilities)

| Category | Meaning | Example seed skills |
|---|---|---|
| **Understanding** | Read input, parse context, recognize intent | `comprehend-code`, `comprehend-doc` |
| **Generation** | Produce output — code, documents, interface contracts, architecture, schemas, visual specs, productivity aids | `generate-api`, `generate-doc`, `api-design`, `system-design`, `database-design`, `ui-design`, `ux-design`, `writing-great-skills`, `handoff`, `teach` |
| **Retrieval** | Find information, query data, call APIs (analysis included) | `retrieve-rag`, `retrieve-sql` |
| **Execution** | Run commands, manipulate files, invoke tools | `execute-bash`, `execute-git` |
| **Decision** | Plan, choose, weigh tradeoffs (analysis included) | `decide-invest`, `decide-product` |

Lifecycle governance lives in Review (horizontal), not in Domain.

> **`Domain` vs `domain-entry`**: `domain/` holds the **execution units** (the 18 seed skills, routed by Distributor at runtime). `domain-entry` is a **browsing entrypoint** skill (on-demand, `user-invocable: true`) — it only lists categories/skills for the user; actual routing still goes through Distributor's risk-score + match logic. The two are not the same node; the architecture diagram's `[Domain]` box refers to the execution units, not the `domain-entry` skill.

## Glossary

See [CONTEXT.md](./CONTEXT.md) for the canonical term definitions.

## Layout

```
MY_SKILL/
├── docs/adr/                # Architecture Decision Records
├── CONTEXT.md               # Glossary / ubiquitous language
├── meta/                    # 8 metadata modules (4V + 1H layer)
│   ├── distributor/         # vertical: route + risk-score + gap-detect (force-triggers horizontal layer)
│   │   ├── SKILL.md
│   │   └── INDEX.yaml       # 27-skill registry (8 modules + installer-bootstrap + 18 domain) + routing config + lifecycle governance
│   ├── builder/             # vertical: confirm → plan → generate
│   ├── installer/           # vertical: adapters/ + bootstrap/
│   │   ├── adapters/        # per-platform translation (workbuddy/codex/hermes)
│   │   └── bootstrap/       # session activation (only distributor is always-active)
│   ├── domain-entry/        # vertical: 5-category domain registry entrypoint
│   ├── review/              # horizontal: per-task + per-skill scopes
│   ├── thinking-first/      # horizontal: pre-route cognitive discipline
│   ├── caveman/             # horizontal: pre-think constraint + post-output compression
│   └── grill-with-docs/     # horizontal: on-gap design interrogation + ADR landing
├── domain/                  # 5 LLM-capability categories of skills (18 seeds: 2+10+2+2+2)
│   ├── understanding/
│   ├── generation/           # implementation, design specs, productivity aids (10 skills)
│   ├── retrieval/
│   ├── execution/
│   └── decision/
├── AGENTS.md                # Agent entrypoint
└── README.md
```

## Deployment

Deployment is **AI-driven**: the `installer` vertical does the work — you don't type shell commands. MY_SKILL is cross-platform; `installer` translates a generic `SKILL.md` into each platform's format via `meta/installer/adapters/` (workbuddy / codex / hermes). At session start, `bootstrap/` auto-verifies the registry.

**Invoke it by talking to the agent, not the shell:**

- Slash command: `/installer sync` — install every skill to the default platform.
- Natural language: "把 MY_SKILL 装到 WorkBuddy" / "install MY_SKILL to WorkBuddy".
- Single skill: `/installer install <skill-name> --platform=workbuddy`.

The agent reads `INDEX.yaml`, applies the platform adapter, writes each skill to the target, and reports skips/conflicts. Full safety rules, skip-list (`thinking-first` / `caveman` / `decide-invest`), and `--force`: [docs/INSTALL.md](./docs/INSTALL.md).

> `codex` / `hermes` adapters ship as `meta/installer/adapters/*.yaml`. The WorkBuddy path is the only automated installer today; port `sync.py` per adapter to reach other platforms. Running `sync.py` by hand is an escape hatch for when no agent is available.

## Documentation

| Doc | Purpose |
|---|---|
| [README.md](./README.md) | Architecture diagram + repo layout (English) |
| [README.zh-CN.md](./README.zh-CN.md) | 中文版 (Chinese) |
| [CONTEXT.md](./CONTEXT.md) | Glossary / ubiquitous language |
| [AGENTS.md](./AGENTS.md) | Agent read order when working in this repo |
| [docs/INSTALL.md](./docs/INSTALL.md) | Install / deploy skills to a platform |
| [docs/adr/](./docs/adr/) | 7 architecture decision records (Q1–Q7) |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | AI agent contribution guidelines |
| [CHANGELOG.md](./CHANGELOG.md) | Version history |
| [LICENSE](./LICENSE) | MIT |

## Local development first

This repository is developed locally first. Clone it anywhere — the `meta/` and `domain/` layouts work as-is.
