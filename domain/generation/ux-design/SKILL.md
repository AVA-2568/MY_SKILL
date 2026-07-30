---
name: ux-design
description: "Design user experience flows, information architecture, task journeys, and interaction behavior from user goals and business constraints. Use whenever the user asks for UX design, user flow, journey map, information architecture, onboarding, task flow, interaction design, edge cases, error recovery, usability assumptions, or usability validation—even if they only say \"make this easier to use\" or \"design the experience.\" Produce a testable UX specification before visual styling; do not silently replace research with assumptions."
user-invocable: true
agent_created: true
risk_level: low
category: generation
---

# UX design（用户体验设计）

把用户目标、场景和业务约束转换为可验证的体验流程。关注任务、信息架构、决策点、反馈、错误恢复和验证计划；不替代 UI 视觉规范，也不把未经验证的假设包装成用户研究结论。

## 使用时机

- 设计用户旅程、任务流程、信息架构或页面结构
- 优化注册、搜索、购买、审批、协作等关键流程
- 处理空状态、错误、撤销、权限、加载和恢复路径
- 识别体验摩擦、认知负担和流程断点
- 制定可用性假设、验证指标和测试计划

## 输入与边界

收集目标用户、场景、触发原因、成功标准、频率、设备、权限、业务规则、已有研究和约束。缺失信息先标注假设并说明验证方式；不要捏造用户访谈或行为数据。

本技能产出体验与流程规格（→ `ui-design` 负责视觉、组件和 token）；不替代投资决策（→ `decide-invest`），不执行用户测试或修改前端代码。

## 流程

1. **定义用户**：列出角色、目标、动机、前置条件和成功标准。
2. **描述场景**：说明触发、环境、频率、风险和当前替代方案。
3. **拆任务**：把目标拆为主路径、决策点、依赖和完成判据。
4. **建立流程**：标记步骤、用户动作、系统反馈、情绪和摩擦。
5. **组织信息**：设计信息架构、导航、命名、层级和查找路径。
6. **设计状态**：覆盖首次使用、加载、空、成功、错误、权限、离线和恢复。
7. **降低负担**：减少不必要输入、记忆、跳转和不可逆动作；提供撤销与确认。
8. **连接视觉交付**：向 `ui-design` 传递页面、组件状态、内容层级和响应式需求。
9. **定义验证**：提出可用性假设、任务成功率、完成时间、错误率和测试方案。
10. **标注不确定性**：区分事实、假设、设计判断和待验证问题。

## 精确输出模板

```markdown
# UX 设计：[产品 / 流程名]
## 1. 用户、场景与成功标准
## 2. 关键任务与前置条件
## 3. 用户旅程
| 阶段 | 用户目标 / 动作 | 系统反馈 | 摩擦 | 机会 |
## 4. 信息架构
[层级、导航、命名与查找路径]
## 5. 主流程与分支
[主路径、决策点、异常路径、恢复路径]
## 6. 状态与内容策略
| 状态 | 触发 | 用户看到什么 | 可执行动作 |
## 7. UI 交付接口
| 页面 | 组件 | 内容层级 | 状态 | 交给 ui-design 的约束 |
## 8. 可用性假设与验证计划
## 9. 风险、假设与待确认问题
```

## 验证清单

- [ ] 用户角色、场景、触发和成功标准明确
- [ ] 主流程、分支、错误、空状态、权限和恢复路径完整
- [ ] 每个步骤都有用户动作和系统反馈
- [ ] 信息架构、导航和命名可解释
- [ ] 不可逆操作提供预防、确认或撤销机制
- [ ] 将事实、假设、设计判断和研究结论分开
- [ ] 每个关键假设都有验证方法和成功指标
- [ ] 明确交给 `ui-design` 的页面、组件和状态边界

## 简短示例

用户请求：“设计一个新用户首次创建项目的体验。”

先定义“创建成功”的判据，再设计首次进入、模板选择、命名、成员邀请、权限提示、保存失败和撤销路径，最后给出任务成功率与完成时间的可用性验证方案。
