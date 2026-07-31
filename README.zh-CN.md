> English: [README.md](./README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Skills](https://img.shields.io/badge/skills-27-blue)](./INDEX.yaml)
[![npm](https://img.shields.io/badge/npx-install-brightgreen)](https://github.com/AVA-2568/MY_SKILL)

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

## npx 安装

没有硬编码路径，你决定技能装到哪里。

```bash
# 复制到 ./skills/（当前目录）
npx github:AVA-2568/MY_SKILL

# 复制到自定义目录（比如你的 Agent 技能目录）
npx github:AVA-2568/MY_SKILL --target /path/to/your/skills

# 列出可用技能（不安装）
npx github:AVA-2568/MY_SKILL --list

# 查看帮助
npx github:AVA-2568/MY_SKILL --help
```

**示例：**
```bash
npx github:AVA-2568/MY_SKILL --target ~/.trae-cn/skills
npx github:AVA-2568/MY_SKILL --target ./my-awesome-skills
```

### 手动安装

```bash
git clone https://github.com/AVA-2568/MY_SKILL.git
cd MY_SKILL
node bin/install.js --target ./my-skills
```

## 个人技能库声明

> **这是一个个人技能库。** 它反映了我个人的工作流、偏好以及在 TRAE IDE 生态中的工具选择。这里收集的技能来自 TRAE 内置和社区技能生态，根据我的日常使用场景精选而成。
>
> **许可证：** MIT — 可自由使用、修改和分享。不作任何明示或暗示的担保。
>
> **维护：** 本库主要为提升个人生产力而维护。更新随工作流演变而进行。欢迎贡献和 Fork。

## 技能格式

每个技能存放在 `skills/<name>/` 目录下：

```
skills/<name>/
├── SKILL.md          # 技能定义（必需）
├── scripts/          # 自动化脚本（可选）
├── agents/           # Agent 配置文件（可选）
├── references/       # 参考文档（可选）
└── assets/           # 支持资源（可选）
```

详见 [INDEX.yaml](./INDEX.yaml) 完整技能注册表。

## 其他安装方式

```bash
# 克隆后手动复制
git clone https://github.com/AVA-2568/MY_SKILL.git
cp -r MY_SKILL/skills/* /your/target/skills/dir/
```

## 许可证

[MIT](./LICENSE)