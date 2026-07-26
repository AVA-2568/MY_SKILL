---
name: ui-design
description: Generate the visual and structural UI specification for a product, feature, page, or component from product goals and brand constraints. Use whenever the user asks for a UI design, mockup spec, screen layout, design tokens, component breakdown, state catalog, responsive rules, or accessibility treatment—even if the brief is just "design the screen for X," "build a UI for Y," "mock up the dashboard," "define the visual language," or "style the component." Covers information hierarchy, page layout, components, states, design tokens, color, typography, responsive behavior, accessibility, interaction notes, and handoff specs. Does not replace UX research, task flow, or information architecture—assume those are already decided or produced by `ux-design`.
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
2. **建立 token 基线**：颜色（语义 + 中性 + 品牌）、字号阶梯、行高、间距阶（4/8 基线）、圆角、阴影层级、动效曲线与时长。
3. **划信息层级**：每屏给出主标题 / 次标题 / 正文 / 辅助 / 操作五级语义层级与对应 token。
4. **排版布局**：栅格列数、gutter、容器最大宽、断点（sm/md/lg/xl）、安全区与触摸目标（≥44×44）。
5. **拆组件清单**：每屏列出所用组件（按钮、输入、卡片、列表、模态、导航、Toast、Empty/Loading/Error），含 props 与状态。
6. **枚举状态**：default / hover / focus / active / disabled / loading / empty / error / success / selected / pressed / expanded，每个写视觉差异。
7. **响应式规则**：每组件说明 sm/md/lg/xl 的尺寸、排列与可见性变化。
8. **a11y 策略**：色彩对比、焦点顺序、aria 角色、文本替代、键盘操作和语义 HTML。
9. **交互说明**：hover、点击、长按、拖拽、手势、动画和不活跃状态过渡。
10. **交付清单**：逐页逐组件交付清单、token 表和 handoff 说明。