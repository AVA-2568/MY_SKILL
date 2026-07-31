> English: [README.md](./README.md)

[![CI](https://github.com/AVA-2568/MY_SKILL/actions/workflows/validate.yaml/badge.svg)](https://github.com/AVA-2568/MY_SKILL/actions/workflows/validate.yaml)
[![License: MIT](https://img.shields.io/github/license/AVA-2568/MY_SKILL?label=license)](./LICENSE)
[![Skills](https://img.shields.io/badge/skills-8-blue)](./meta/distributor/INDEX.yaml)
[![Platforms](https://img.shields.io/badge/platforms-workbuddy%20%7C%20codex%20%7C%20hermes-0F6E56)](./docs/adr/0002-protocol-compatible-adapters.md)

# MY_SKILL

跨平台 AI agent 的技能**基础设施**——不是又一个 skill 库。解决两件事：

1. **N 平台 × M 技能**——一次导入，到处安装（workbuddy / codex / hermes）。
2. **模型幻视**（"装了但被忽略"）——三层反幻视机制。

## 为什么不直接用 obra/superpowers？

技能层面你应该用 superpowers。MY_SKILL 不在内容上竞争，它在**管道**上竞争：skill 如何被注册、发现、路由、强制执行，并跨平台同步。来自 superpowers、mattpocock/skills 或你自己 repo 的 skill，都走同一套基础设施。

## 反幻视三层

模型忽略已装 skill 有三个根因，MY_SKILL 全覆盖：

| 根因 | 负责 | 机制 |
|---|---|---|
| 模型根本没加载 skill description | Distributor | session 启动时把所有 description 注入 context |
| 模型加载了但路由不准 | Distributor | keyword 路由 + fuzzy 评分选 top-1，模型不自由选 |
| 模型选了但跳过执行 | Review | Reflection Gate 反射注入"你提到了 X 但没执行" |

没有任何其他层（模型 / 平台 / superpowers）覆盖第 3 类。

## 同步工作流（跨机器 / 跨平台）

MY_SKILL repo 是你的个人 skill hub，GitHub 是云端中转。**核心约定：编辑只在 repo 发生，平台目录是只读消费者。**

### 平台 A（编辑 skill）

1. 直接改 MY_SKILL repo 里的 SKILL.md（**不要在平台端改**）
2. `installer sync` 装到当前平台
3. `git push` 同步到 GitHub

### 平台 B（一键安装）

在新机器 / 新 agent 上，对模型说一句：**"帮我安装 MY_SKILL"**

模型会自动：
1. `git clone https://github.com/AVA-2568/MY_SKILL.git ~/MY_SKILL`（已存在则 `git pull`）
2. 探测当前平台（workbuddy / codex / hermes）
3. `sync.py --auto-detect` 装好所有 skill
4. 报告安装结果

也可以直接跑脚本：
```bash
curl -fsSL https://raw.githubusercontent.com/AVA-2568/MY_SKILL/main/meta/installer/scripts/install.sh | bash
```

### 关键约定

| 约定 | 为什么 |
|---|---|
| **编辑只在 repo 发生** | 保证 canonical 源干净，不会把平台格式污染带回 repo |
| **平台端是只读消费者** | sync 出来的派生品不要手改，下次 sync 会覆盖 |
| **GitHub 是唯一中转** | 不要用 U 盘 / 邮件传 skill，永远走 GitHub |

这个模式下**不需要"反标准化"**——因为编辑永远在 repo 里发生，repo 保持干净。

## 架构

```
外部 skill（superpowers / mattpocock / 你的 repo）
    │
    ▼
[importer.py] ── 拉取 + 标准化 frontmatter ──▶ domain/<category>/<name>/
    │
    ▼
[INDEX.yaml] ── 注册表（8 个 skill：5 meta + 3 domain）
    │
    ├──▶ [Distributor] session 启动：注入所有 description 到 context
    │                  每个任务：keyword + fuzzy 路由到 top-1 skill
    │                        │
    │                        ▼
    │                  [Domain skill] 执行
    │                        │
    │                        ▼
    │                  [Review] Reflection Gate：模型真的调用了吗？
    │
    └──▶ [Installer] adapters/ ── 翻译到 workbuddy/codex/hermes
                      bootstrap/ ── 校验 session 启动状态
```

## 模块

### Meta（5 个）

| 模块 | 角色 | 可调用 |
|---|---|---|
| **distributor** | 发现保证器 + skill 路由器 | `always_active`（不可用户调用） |
| **installer** | 导入器 + 3 平台适配器 + bootstrap | 是 |
| **installer-bootstrap** | session 启动校验 | 否（启动时自动） |
| **domain-entry** | 浏览 skill 注册表 | 是 |
| **review** | Reflection Gate + 生命周期治理 | 否（horizontal，强制触发） |

### Domain（3 个）

只保留**没有生态等价物**的 skill，其他按需导入。

| skill | 类别 | 为什么保留 |
|---|---|---|
| `decide-invest` | decision | 金融决策——无公开等价物 |
| `ui-design` | generation | 视觉规格输出——superpowers 做工程流不做视觉设计 |
| `ux-design` | generation | user journey / 信息架构——UX 专属 |

导入更多：`python meta/installer/scripts/importer.py owner/repo`

## 决策

| # | 决策 | 状态 |
|---|---|---|
| [0001](./docs/adr/0001-full-autonomous-rebuild.md) | 完全自主重建 | 已采纳 |
| [0002](./docs/adr/0002-protocol-compatible-adapters.md) | 协议兼容 + 跨平台适配器 | 已采纳 |
| [0003](./docs/adr/0003-four-verticals-one-horizontal.md) | 4 纵 1 横 | 被 0008 取代 |
| [0004](./docs/adr/0004-review-subsystem.md) | 审查子系统（3 门禁 + lifecycle） | 被 0008 取代 |
| [0005](./docs/adr/0005-b-chain-vertical-roles.md) | B-Chain 触发 + 纵向角色 | 被 0008 取代 |
| [0006](./docs/adr/0006-domain-five-llm-capabilities.md) | 领域：5 类 LLM 能力 | 被 0008 取代 |
| [0007](./docs/adr/0007-mvp-minimum-viable.md) | MVP：8 模块 + 18 种子 | 被 0008 取代 |
| [0008](./docs/adr/0008-slim-infra-not-content-library.md) | **精简基础设施，不做内容库** | **已采纳（当前）** |

## 目录结构

```
MY_SKILL/
├── docs/adr/                # 8 份 ADR（0008 是当前事实）
├── CONTEXT.md               # 术语表 / 统一语言
├── meta/                    # 5 个 metadata 模块
│   ├── distributor/         # 发现保证器 + 路由器
│   │   ├── SKILL.md
│   │   ├── INDEX.yaml       # 8-skill 注册表 + 路由 + lifecycle 配置
│   │   └── scripts/score.py # keyword + fuzzy 路由器
│   ├── installer/           # 导入器 + 适配器 + bootstrap
│   │   ├── scripts/
│   │   │   ├── sync.py      # 装到平台（支持 --auto-detect）
│   │   │   ├── sync_nested.py
│   │   │   ├── importer.py  # 从 GitHub / 本地拉取 skill
│   │   │   └── install.sh   # 一键安装（clone + sync）
│   │   ├── adapters/        # workbuddy.yaml / codex.yaml / hermes.yaml
│   │   └── bootstrap/       # session 启动校验
│   ├── domain-entry/        # 浏览入口
│   └── review/              # Reflection Gate + 生命周期治理
├── domain/                  # 3 个种子 skill（无生态等价物）
│   ├── decision/decide-invest/
│   └── generation/{ui-design,ux-design}/
├── tests/fixtures/          # route-cases.yaml
├── AGENTS.md                # Agent 入口
└── README.md
```

## 用法

### 一键安装（新机器）

```bash
# 模型说"帮我安装 MY_SKILL"时跑这个；或直接：
curl -fsSL https://raw.githubusercontent.com/AVA-2568/MY_SKILL/main/meta/installer/scripts/install.sh | bash

# 也可以手动：
bash meta/installer/scripts/install.sh
```

> **Windows**：用 Git Bash（随 Git for Windows 安装）运行 `install.sh`。
> 没有 Git Bash 就直接跑 `sync.py`——见 [docs/INSTALL.md](./docs/INSTALL.md#manual-fallback-no-agent-available)。

### 从任意 repo 导入 skill

```bash
python meta/installer/scripts/importer.py obra/superpowers          # 扫整个 repo
python meta/installer/scripts/importer.py mattpocock/skills/productivity/handoff
python meta/installer/scripts/importer.py --local /path/to/my/skill --category generation
```

### 装到当前平台

```bash
python meta/installer/scripts/sync.py --auto-detect          # 自动探测平台
python meta/installer/scripts/sync.py --target ~/.workbuddy/skills/
```

或者告诉 agent："install MY_SKILL to WorkBuddy" / "把 MY_SKILL 装到 WorkBuddy"。

### 路由任务

Distributor 在每个 session + 每个任务上自动跑。无需手动调用。

## 文档

| 文档 | 用途 |
|---|---|
| [README.md](./README.md) | 架构 + 目录结构（英文） |
| [README.zh-CN.md](./README.zh-CN.md) | 中文版（本文件） |
| [CONTEXT.md](./CONTEXT.md) | 术语表 / 统一语言 |
| [AGENTS.md](./AGENTS.md) | agent 在本仓库的阅读顺序 |
| [docs/INSTALL.md](./docs/INSTALL.md) | 安装 / 部署 skill 到平台 |
| [docs/adr/0008](./docs/adr/0008-slim-infra-not-content-library.md) | 当前架构事实 |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | AI agent 贡献指南 |
| [CHANGELOG.md](./CHANGELOG.md) | 版本历史 |
| [LICENSE](./LICENSE) | MIT |

## 本地优先开发

本仓库本地优先开发。克隆到任意位置，`meta/` 与 `domain/` 的结构开箱即用。
