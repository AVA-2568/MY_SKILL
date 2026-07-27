---
name: ui-design
description: "Generate the visual and structural UI specification for a product, feature, page, or component from product goals and brand constraints. Use whenever the user asks for a UI design, mockup spec, screen layout, design tokens, component breakdown, state catalog, responsive rules, or accessibility treatment—even if the brief is just \"design the screen for X,\" \"build a UI for Y,\" \"mock up the dashboard,\" \"define the visual language,\" or \"style the component.\" Covers information hierarchy, page layout, components, states, design tokens, color, typography, responsive behavior, accessibility, interaction notes, and handoff specs. Does not replace UX research, task flow, or information architecture—assume those are already decided or produced by `ux-design`."
user-invocable: true
agent_created: true
risk_level: low
category: generation
---

# UI Design（界面视觉与结构设计）

从产品目标、品牌约束与已定的体验（IA / 流程 / 任务）出发，输出可交付的界面视觉结构：层级、布局、组件、状态、token、色彩、排版、响应式、a11y、交互说明与交付规格。明确边界——本技能不重做用户研究、不重画流程图、不替代 `ux-design`。

## 使用时机

- 设计或重构页面、屏、视图、组件库的视觉结构
- 需要设计 token（颜色、字体、间距、圆角、阴影、动效）规范
- 需要把模糊视觉想法转成可交付的高保真规范
- 需要为响应式、可访问性、状态机、交互手势给工程一份可落地说明
- 需统一多页面或多端的设计语言与组件契约

不适用：纯 UX 流程、用户访谈、可用性测试（→ `ux-design`）；纯品牌战略与 Logo 设计；可运行前端代码（→ 由开发技能实现）。

## 输入

收集产品目标、目标用户一句话画像、品牌约束（已有品牌色 / 字体 / 语气则沿用，否则按行业惯例先假设）、平台与设备、屏与断点、关键页面清单或核心组件、参考风格关键词、信息架构（来自 `ux-design` 或用户简述）、暗色模式与可访问性等级（默认 WCAG 2.1 AA）。缺失时先标注假设；只有会改变视觉主调时才追问。

## 流程

1. **锁定目标**：产品要传达的核心动作、情绪基线、品牌硬度（保守 / 中性 / 强烈）。
2. **建立 token 基线**：颜色（语义 + 中性 + 品牌）、字号阶梯、行高、间距阶（4/8 基线）、圆角、阴影���级、动效曲线与时长。
3. **划信息层级**：每屏给出主标题 / 次标题 / 正文 / 辅助 / 操作五级语义层级与对应 token。
4. **排版布局**：栅格列数、gutter、容器最大宽、断点（sm/md/lg/xl）、安全区与触摸目标（≥44×44）。
5. **拆组件清单**：每屏列出所用组件（按钮、输入、卡片、列表、模态、导航、Toast、Empty/Loading/Error），含 props 与状态。
6. **枚举状态**：default / hover / focus / active / disabled / loading / empty / error / success / selected / pressed / expanded，每个写视觉差异。
7. **响应式规则**：每组件说明 sm/md/lg/xl 的尺寸、排列与可见性变化。
8. **a11y 处理**：对比度（正文 ≥4.5:1，大字 ≥3:1）、焦点可见、键盘顺序、ARIA 角色、替代文本、动效减弱。
9. **交互说明**：hover/focus/press/进入/退出/页面转场/滚动行为的视觉与时长。
10. **交付规格**：交付物列表（规范文档 + 组件清单 + token JSON + 标注图）+ 命名规范 + 版本号 + 变更日志。

## 精确输出模板

```markdown
# UI 设计：[产品 / 页面 / 组件名]
## 1. 目标与约束
- 产品目标 / 用户目标 / 情绪基线：
- 品牌硬度：保守 | 中性 | 强烈
- 平台 / 断点 / 设备：
- 暗色模式：必 / 选 / 不提供；a11y 等级：AA / AAA
- 已知事实 / 假设 / 待确认：
## 2. 设计 Token
- 颜色：primary / secondary / neutral(50–900) / semantic(success/warning/danger/info) / surface / on-*
- 字号：display / h1 / h2 / h3 / body / caption；行高；字重
- 间距：4 / 8 / 12 / 16 / 24 / 32 / 48 / 64
- 圆角：sm / md / lg / pill；阴影：0/1/2/3 级；动效：duration + easing
## 3. 信息层级
| 层级 | 用途 | token 引用 | 字号 / 字重 / 颜色 |
## 4. 布局与栅格
- 容器最大宽 / 列数 / gutter / 安全区
- 断点：sm md lg xl
- 关键屏布局示意：Header / Sidebar / Main / Footer 的占比与行为
## 5. 组件清单
| 组件 | props | 状态 | 响应式 | a11y 备注 |
## 6. 状态矩阵
| 组件 | default | hover | focus | active | disabled | loading | empty | error |
## 7. 响应式规则
| 断点 | 容器 | 栅格 | 导航 | 关键组件 |
## 8. 可访问性
- 对比度核查表、焦点环、键盘顺序、ARIA、替代文本、动效减弱
## 9. 交互与动效
| 触发 | 视觉变化 | 时长 / 曲线 | 备注 |
## 10. 交付规格
- 物：规范 PDF / Figma / token.json / 组件包
- 命名：kebab-case 文件，BEM 或 atomic 类
- 版本：v0.1.0 + 变更日志
```

## 验证清单

- [ ] 明确写出目标、品牌硬度、a11y 等级与暗色模式策略
- [ ] Token 完整覆盖颜色 / 字号 / 间距 / 圆角 / 阴影 / 动效六类
- [ ] 颜色对比度满足 WCAG AA，关键文本可量化
- [ ] 每屏有栅格、列数、容器最大宽与断点
- [ ] 组件清单含 props、状态、响应式与 a11y 备注四列
- [ ] 状态矩阵至少覆盖 default / hover / focus / disabled / loading / empty / error
- [ ] 触摸目标 ≥44×44，关键流程键盘可达
- [ ] 区分事实与假设，不把推测包装成研究结论
- [ ] 不重画用户旅程或信息架构（由 `ux-design` 负责）
- [ ] 输出含可交付物清单、命名规范、版本号

## 简短示例

用户请求："为远程团队协作工具的'项目仪表盘'设计视觉规范。"

输出摘要：情绪基线"克制专业"，品牌硬度中性；token 基线 primary #4F46E5、neutral 50–900、字号阶梯 12/14/16/20/24/32、间距 4 基线、圆角 md=8、阴影三级、动效 150–300ms ease-out；栅格 12 列容器 1280、gutter 24、断点 sm 640 / md 768 / lg 1024 / xl 1280；主屏分 Header / Sidebar / Main 三区，组件含 NavItem / StatCard / TaskTable / FilterBar / EmptyState / Toast；状态矩阵覆盖 default/hover/focus/loading/empty/error，焦点环 2px primary 偏移 2；交付 Figma + token.json + 组件包 v0.1.0；假设"用户已熟悉线性看板"待确认。
