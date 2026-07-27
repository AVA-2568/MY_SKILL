---
name: grill-with-docs
description: "设计拷问 + ADR/glossary 落地——Distributor 检测到模糊任务或设计请求时强制触发。Relentless 拷问逐个收窄设计分支，同时落地 ADR 和术语表。Triggers: \"帮我设计 X\", \"规划 Y\", \"做项目 Z\", 或任何 description match_score 低于阈值的模糊任务。user-invocable: false。"
user-invocable: false
risk_level: low
---

# Grill-With-Docs (设计拷问 + ADR 落地)

设计/规划阶段的拷问工具。**Distributor 检测到模糊任务或设计请求时强制调用**。

## 工作流

1. **拷问** — 用 relentless 拷问逐个收窄设计分支（一次一个）
2. **记录** — 每个决策落地为 ADR（`docs/adr/000N-slug.md`）
3. **术语表** — 每个新术语落地到 `CONTEXT.md`
4. **决策树推进** — 广度优先铺开 frontier，逐个解决

## 触发

- **由 Distributor 检测到模糊/设计/规划任务时强制调用**
- user-invocable: false（不让用户直接 /slash 调用）
- Distributor 检测的触发条件（任一）：
  - 任务包含"设计 / 规划 / 方案 / 架构 / 做一个项目"等关键词
  - 任务的 description match_score 都低于 routing.match_threshold
  - 用户说"我有个想法"等模糊表达

## Procedure

1. Distributor 检测到模糊任务
2. 调用 grill-with-docs
3. 开始拷问流程：
   - 问一个最关键的问题（一次一个）
   - 用户回答
   - 落地决策为 ADR
   - 进入下一层
4. 收尾：写入 `docs/adr/` 和 `CONTEXT.md`

## Pitfalls

- **不要一次问多个问题**（一次一个，grill 规则）
- **不要替用户决定**（提供推荐 + 等用户选）
- **不要跳过 ADR 落地**（拷问完了不等于决策落地了）
- **不要让拷问无限循环**（设定退出条件：shared understanding 达成 + 用户确认"开始建"）

## Verification

- 每次 grill 必须产出至少 1 个 ADR（如果产生决策）
- 所有新术语必须进 `CONTEXT.md`
- 退出条件：用户确认 "OK 落地" / "开始建" / "进阶段 X"
- Distributor 调用 grill-with-docs 后必须等待收尾完成才能继续路由
