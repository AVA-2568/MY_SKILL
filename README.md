# MY_SKILL

A cross-platform AI skill library — workbuddy + codex + hermes, self-use, fully autonomously rebuilt.

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

The 4 verticals (Distributor / Builder / Installer / Domain-entry) are on-demand. The horizontal layer has 4 components force-triggered by Distributor at specific flow points: thinking-first (pre-route) / Review (per-task + per-skill) / caveman (post-route) / grill-with-docs (on-gap).

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
| **thinking-first** | pre-route | Cognitive discipline (5 rules: understand / source-anchor / uncertainty / pre-delivery check / minimal intervention) |
| **Review** | per-task + per-skill | Code Review (soft) / Task Recheck (soft) / Security Review (reflection + extreme-risk hard) + Lifecycle Governance |
| **caveman** | pre-think + post-output | Pre-think constrains *thinking* to 3-5 short points; post-output compresses residual verbosity. Not post-only — affects AI thought. |
| **grill-with-docs** | on-gap | Design interrogation + ADR/glossary landing |

All 4 are `user-invocable: false`; they cannot be /slash-called directly by the user.

## Domain (5 LLM Capabilities)

| Category | Meaning | Example seed skills |
|---|---|---|
| **Understanding** | Read input, parse context, recognize intent | `comprehend-code`, `comprehend-doc` |
| **Generation** | Produce output: code, documents, interface contracts, architecture, schemas, visual specifications, productivity aids | `generate-api`, `generate-doc`, `api-design`, `system-design`, `database-design`, `ui-design`, `ux-design`, `writing-great-skills`, `handoff`, `teach` |
| **Retrieval** | Find information, query data, call APIs (incl. analysis) | `retrieve-rag`, `retrieve-sql` |
| **Execution** | Run commands, manipulate files, invoke tools | `execute-bash`, `execute-git` |
| **Decision** | Plan, choose, weigh tradeoffs (incl. analysis) | `decide-invest`, `decide-product` |

Governance (lifecycle) belongs to Review (horizontal), not to Domain.

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
│   │   └── INDEX.yaml       # 23-skill registry + routing config + lifecycle governance
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

## Local development first

This repository is developed locally first. Clone it anywhere and the layout under `meta/` and `domain/` works as-is.
