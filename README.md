> 中文版本: [README.zh-CN.md](./README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Skills](https://img.shields.io/badge/skills-27-blue)](./INDEX.yaml)
[![npm](https://img.shields.io/badge/npx-install-brightgreen)](https://github.com/AVA-2568/MY_SKILL)

# MY_SKILL — Personal TRAE Skill Library

A curated collection of **27 AI agent skills** extracted from my day-to-day TRAE IDE workflow. This is a personal skill library, maintained for my own use and shared for anyone who finds it useful.

## What's Inside

| Category | Skills |
|---|---|
| **Development** | `code-review`, `codebase-design`, `executing-plans`, `writing-plans`, `implement`, `to-spec`, `to-tickets`, `gh-cli`, `grill-with-docs`, `verification-before-completion` |
| **Design** | `brainstorming`, `simple`, `frontend-design`, `frontend-skill`, `report-page`, `web-design-guidelines` |
| **Data** | `data-analysis` |
| **SEO** | `ai-seo` |
| **Automation** | `agent-browser` |
| **Education** | `teach` |
| **Utility** | `defuddle`, `find-skills`, `json-canvas`, `obsidian-bases`, `obsidian-cli`, `obsidian-markdown`, `skill-creator` |

## npx Install

The easiest way to install all skills:

```bash
# Install all skills to default TRAE path
npx github:AVA-2568/MY_SKILL

# Install to a custom directory
npx github:AVA-2568/MY_SKILL --target /path/to/skills

# List available skills without installing
npx github:AVA-2568/MY_SKILL --list

# Show help
npx github:AVA-2568/MY_SKILL --help
```

**Default install path:**
- Windows: `%USERPROFILE%\.trae-cn\skills`
- macOS/Linux: `~/.trae-cn/skills`

After installation, **restart your AI agent** to load the new skills.

### Manual Install

```bash
git clone https://github.com/AVA-2568/MY_SKILL.git
cd MY_SKILL
node bin/install.js
```

## Personal Skill Library Declaration

> **This is a personal skill library.** It reflects my own workflow, preferences, and tooling choices within the TRAE IDE ecosystem. The skills collected here are sourced from the built-in and community skill ecosystem that ships with TRAE, curated for my daily use cases.
>
> **License:** MIT — free to use, modify, and share. No warranty, express or implied.
>
> **Maintenance:** This library is maintained primarily for my own productivity. Updates happen as my workflow evolves. Contributions and forks are welcome.

## Skill Format

Each skill lives in `skills/<name>/` and contains:

```
skills/<name>/
├── SKILL.md          # Skill definition (required)
├── scripts/          # Automation scripts (optional)
├── agents/           # Agent configuration files (optional)
├── references/       # Reference documentation (optional)
└── assets/           # Supporting assets (optional)
```

See [INDEX.yaml](./INDEX.yaml) for the full skill registry.

## Other Install Methods

```bash
# Clone and symlink (for development)
git clone https://github.com/AVA-2568/MY_SKILL.git ~/MY_SKILL
ln -s ~/MY_SKILL/skills/* ~/.trae-cn/skills/

# Python one-liner (Windows)
python -c "import shutil,pathlib;s=pathlib.Path(r'%USERPROFILE%\MY_SKILL\skills');[shutil.copytree(p,pathlib.Path(r'%USERPROFILE%\.trae-cn\skills')/p.name,dirs_exist_ok=True) for p in s.iterdir() if p.is_dir()]"
```

## License

[MIT](./LICENSE)