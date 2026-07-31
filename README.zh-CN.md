> English: [README.md](./README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Skills](https://img.shields.io/badge/skills-27-blue)](./INDEX.yaml)

# MY_SKILL — 个人 TRAE 技能库

从日常 TRAE IDE 工作流中精选的 **27 个 AI Agent 技能**。这是我的个人技能库，为自己日常使用而维护，也分享给任何觉得有用的人。

## 技能清单

| 分类 | 技能 |
|---|---|
| **开发** | `code-review`、`codebase-design`、`executing-plans`、`writing-plans`、`implement`、`to-spec`、`to-tickets`、`gh-cli`、`grill-with-docs`、`verification-before-completion` |
| **设计** | `brainstorming`、`simple`、`frontend-design`、`frontend-skill`、`report-page`、`web-design-guidelines` |
| **数据** | `data-analysis` |
| **SEO** | `ai-seo` |
| **自动化** | `agent-browser` |
| **教育** | `teach` |
| **工具** | `defuddle`、`find-skills`、`json-canvas`、`obsidian-bases`、`obsidian-cli`、`obsidian-markdown`、`skill-creator` |

## 安装

```bash
# 安装全部 27 个技能
npx skills add AVA-2568/MY_SKILL

# 安装指定技能
npx skills add AVA-2568/MY_SKILL@skill-name
```

### 手动安装

```bash
git clone https://github.com/AVA-2568/MY_SKILL.git
cp -r MY_SKILL/skills/* /path/to/your/skills/dir/
```

## 个人技能库声明

> **这是一个个人技能库。** 它反映了我个人的工作流、偏好以及在 TRAE IDE 生态中的工具选择。这里收集的技能来自 TRAE 内置和社区技能生态，根据我的日常使用场景精选而成。
>
> **许可证：** MIT — 可自由使用、修改和分享。不作任何明示或暗示的担保。
>
> **维护：** 本库主要为提升个人生产力而维护。更新随工作流演变而进行。欢迎贡献和 Fork。

## 技能格式

```
skills/<name>/
├── SKILL.md          # 技能定义（必需）
├── scripts/          # 自动化脚本（可选）
├── agents/           # Agent 配置文件（可选）
├── references/       # 参考文档（可选）
└── assets/           # 支持资源（可选）
```

详见 [INDEX.yaml](./INDEX.yaml) 完整技能注册表。

## 许可证

[MIT](./LICENSE)