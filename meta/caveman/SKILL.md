---
name: caveman
description: "思考 + 输出双层精简——让 AI 在思考阶段就只列核心要点（不展开不写过渡），输出阶段再兜底压一遍。Distributor 在 pre-think（thinking-first 之后）和 post-output 两个时点强制触发。Triggers: \"简短点\", \"caveman mode\", \"少废话\", \"token 压缩\", \"少说废话\"。即使没显式要求，对长思考链 + 长输出也默认应用。"
user-invocable: false
risk_level: low
category: meta
---

# Caveman (思考约束 + 输出压缩)

**思考约束器**——让 AI 在思考阶段就精简，而不是事后删除。

## 核心洞察

LLM 的\"思考\"= 生成 token 流。**post-compress（事后压缩）**是浪费 token 先生成再删；**pre-think minimal（思考约束）**才是真正的精简——思考时只列要点不展开，输出自然简洁。

caveman 采用 **pre-think 强约束 + post-output 兜底** 双触发。

## 触发（双触发点，由 Distributor 强制调用）

| 触发点 | 时机 | 作用 |
|---|---|---|
| **pre-think** | thinking-first 之后、路由之前 | 思考时只列 3-5 要点，每点 ≤10 词；不展开不写过渡 |
| **post-output** | Domain skill 执行后、最终输出前 | 兜底：删除\"让我...\"等过渡、表格化、压缩重复 |

两者都 `user-invocable: false`，由 Distributor 内部强制调用。

## Procedure (pre-think)

1. thinking-first 完成（5 大纪律已落地：理解 + 源 + 不确定性 + 最小干预 + 交付前自检）
2. caveman 介入：
   - 把 thinking-first 的\"理解 + 源 + 不确定性\"产物**压成 3-5 短要点**
   - 每个要点 ≤10 词，名词/动词为主，砍形容词/副词
   - **不展开**——\"为什么\"、\"怎么样\"、\"让我们先...\"等过渡必须砍
3. 路由扫描时，Distributor 用\"3-5 要点\"作为路由输入（不是完整 user task）
4. Domain skill 收到的是精简版任务，输出自然精简

## Procedure (post-output)

1. Domain skill 生成完整输出
2. caveman 介入兜底：
   - 删除\"让我...\"、\"首先...\"、\"值得注意的是...\"、\"接下来...\"等过渡
   - 表格化（如果可能）
   - 数字结论不带冗长解释
   - 不重复用户已知的信息
3. 输出最终版

## 关键原则

- **思考时只列要点，不展开**——展开是 Domain skill 的事，caveman 只负责\"想得短\"
- **删除\"为完整性而写的废话\"**——完整性是 thinking-first 的职责（纪律 4），caveman 砍未要求内容
- **保留 thinking-first 的产物**——不确定性标签（\"推测\"/\"未知\"）+ 源引用必须保留，不能压缩
- **pre-think 是主战场，post-output 是兜底**——如果 pre-think 到位，post-output 几乎不需要做事

## Pitfalls

- **不要压缩源引用**（溯源信息必须保留）
- **不要压缩不确定性标签**（thinking-first 标注的\"推测\"必须保留）
- **不要为了短而牺牲准确性**——短 ≠ 模糊，保持精确
- **不要在 pre-think 阶段展开思考**——caveman 的核心是\"约束\"，展开就违反本意
- **pre-think 不能太早**——它依赖 thinking-first 的产物（理解 + 源 + 不确定性），必须等 thinking-first 完成

## Verification

- **pre-think 阶段**：列出的要点 ≤5 个，每个 ≤10 词；无\"为什么/怎么样/让我们\"等过渡词
- **post-output 阶段**：每 100 词 ≥1 个事实/结论；thinking-first 的产物（不确定性标签 + 源引用）100% 保留
- **整体**：思考过程生成的 token 数 vs 旧 post-only 模式应下降 30%+
