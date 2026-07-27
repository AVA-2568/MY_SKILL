> English: [README.md](./README.md)

[![CI](https://github.com/AVA-2568/MY_SKILL/actions/workflows/validate.yaml/badge.svg)](https://github.com/AVA-2568/MY_SKILL/actions/workflows/validate.yaml)
[![License: MIT](https://img.shields.io/github/license/AVA-2568/MY_SKILL?label=license)](./LICENSE)
[![Skills](https://img.shields.io/badge/skills-27-blue)](./meta/distributor/INDEX.yaml)
[![Platforms](https://img.shields.io/badge/platforms-workbuddy%20%7C%20codex%20%7C%20hermes-0F6E56)](./docs/adr/0002-protocol-compatible-adapters.md)

# MY_SKILL

跨平台 AI 技能库，面向 WorkBuddy、Codex、Hermes —— 自用，且由 AI 持续自主重构。

## 亮点

- **4 纵 1 横审查层** —— 路由、构建、安装与横切审查门禁职责清晰分离。
- **协议兼容** —— 通用 `SKILL.md` 遵循 Anthropic Agent Skills 标准；跨平台适配器翻译到 WorkBuddy / Codex / Hermes。
- **AI 驱动部署** —— 由 `installer` 技能执行安装，你只需告诉 agent，无需敲命令。
- **自重构** —— 缺某个技能？`Builder` 纵向模块按需生成新的。

## 架构

**4 纵 1 横**（见 [ADR-0003](./docs/adr/0003-four-verticals-one-horizontal.md)）：

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

4 个纵向模块（Distributor / Builder / Installer / Domain-entry）按需加载。横向层含 4 个组件，由 Distributor 在特定流程点强制触发：thinking-first（路由前）/ Review（每任务 + 每技能）/ caveman（输出后）/ grill-with-docs（缺口时）。

## 决策

| # | 决策 | 状态 |
|---|---|---|
| [0001](./docs/adr/0001-full-autonomous-rebuild.md) | 完全自主重建 | 已采纳 |
| [0002](./docs/adr/0002-protocol-compatible-adapters.md) | 协议兼容（Anthropic 标准）+ 跨平台适配器 | 已采纳 |
| [0003](./docs/adr/0003-four-verticals-one-horizontal.md) | 4 纵 1 横（4 组件） | 已采纳 |
| [0004](./docs/adr/0004-review-subsystem.md) | 审查子系统：代码 / 任务 / 安全 + 生命周期治理 + 反射门禁 | 已采纳 |
| [0005](./docs/adr/0005-b-chain-vertical-roles.md) | B-Chain 触发 + 纵向角色 | 已采纳 |
| [0006](./docs/adr/0006-domain-five-llm-capabilities.md) | 领域：5 类 LLM 能力（理解 / 生成 / 检索 / 执行 / 决策） | 已采纳 |
| [0007](./docs/adr/0007-mvp-minimum-viable.md) | MVP：8 元模块 + 18-22 种子技能 | 已采纳 |

## 横向层（4 组件，全部由 Distributor 强制触发）

| 组件 | 触发点 | 角色 |
|---|---|---|
| **thinking-first** | 路由前 | 认知纪律 —— 5 条规则：理解 / 来源锚定 / 坦诚不确定性 / 交付前自检 / 最小干预 |
| **Review** | 每任务 + 每技能 | 代码审查（软）/ 任务复查（软）/ 安全审查（反思式；极高风险硬门禁）+ 生命周期治理 |
| **caveman** | 思考前 + 输出后 | 思考前将推理压缩为 3–5 个要点；输出后精简多余内容。它塑造的是思考，不只是文字。 |
| **grill-with-docs** | 缺口时 | 设计诘问 + ADR/术语落地 |

4 个均为 `user-invocable: false`，无法通过 /slash 命令直接调用。

## 领域（5 类 LLM 能力）

| 类别 | 含义 | 示例种子技能 |
|---|---|---|
| **Understanding 理解** | 读取输入、解析上下文、识别意图 | `comprehend-code`, `comprehend-doc` |
| **Generation 生成** | 产出内容 —— 代码、文档、接口契约、架构、schema、视觉规范、效率工具 | `generate-api`, `generate-doc`, `api-design`, `system-design`, `database-design`, `ui-design`, `ux-design`, `writing-great-skills`, `handoff`, `teach` |
| **Retrieval 检索** | 查找信息、查询数据、调用 API（含分析） | `retrieve-rag`, `retrieve-sql` |
| **Execution 执行** | 运行命令、操作文件、调用工具 | `execute-bash`, `execute-git` |
| **Decision 决策** | 规划、选择、权衡取舍（含分析） | `decide-invest`, `decide-product` |

生命周期治理归属横向层的 Review，而非领域层。

## 术语表

术语定义见 [CONTEXT.md](./CONTEXT.md)。

## 目录结构

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

## 部署

部署是 **AI 驱动** 的：由 `installer` 纵向模块执行，你不必在终端敲命令。MY_SKILL 跨平台——`installer` 通过 `meta/installer/adapters/`（workbuddy / codex / hermes）把通用 `SKILL.md` 翻译成各平台专属格式。会话启动时，`bootstrap/` 自动校验注册表。

**用自然语言告诉 agent，而不是在 shell 里敲命令：**

- 斜杠命令：`/installer sync` —— 安装所有技能到默认平台。
- 自然语言："把 MY_SKILL 装到 WorkBuddy" / "install MY_SKILL to WorkBuddy"。
- 单个技能：`/installer install <skill-name> --platform=workbuddy`。

agent 读取 `INDEX.yaml`、套用平台适配器、将每个技能写入目标目录，并汇报跳过/冲突。完整安全规则、跳过清单（`thinking-first` / `caveman` / `decide-invest`）与 `--force` 见 [docs/INSTALL.md](./docs/INSTALL.md)。

> `codex` / `hermes` 适配器以 `meta/installer/adapters/*.yaml` 形式提供。目前 WorkBuddy 路径是唯一自动化安装器；要覆盖其他平台，需按对应适配器移植 `sync.py`。仅在无 agent 可用时，才手动运行 `sync.py` 作为兜底。

## 文档

| 文档 | 用途 |
|---|---|
| [README.md](./README.md) | 架构图 + 仓库结构（英文版） |
| [README.zh-CN.md](./README.zh-CN.md) | 中文版（本文件） |
| [CONTEXT.md](./CONTEXT.md) | 术语表 / 统一语言 |
| [AGENTS.md](./AGENTS.md) | agent 在本仓库的阅读顺序 |
| [docs/INSTALL.md](./docs/INSTALL.md) | 安装 / 部署技能到平台 |
| [docs/adr/](./docs/adr/) | 7 份架构决策记录（Q1–Q7） |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | AI agent 贡献指南 |
| [CHANGELOG.md](./CHANGELOG.md) | 版本历史 |
| [LICENSE](./LICENSE) | MIT |

## 本地优先开发

本仓库本地优先开发。克隆到任意位置，`meta/` 与 `domain/` 的结构开箱即用。
