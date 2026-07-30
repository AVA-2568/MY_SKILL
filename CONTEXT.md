# MY_SKILL

Skill **infrastructure** for cross-platform AI agents — a registry + installer + router + review that makes skills from any source (superpowers, mattpocock, your own repo) installable across platforms and resistant to model hallucination. Not a content library.

## Language

**Skill**:
A self-contained package of instructions, scripts, and resources that an AI agent loads dynamically to perform a specialized task. A skill consists of a `SKILL.md` file (required) plus optional bundled resources (`scripts/`, `references/`, `assets/`).
_Avoid_: prompt template, instruction file, recipe

**Distributor (分发器)**:
The always-active module that guarantees skill discoverability and routes user tasks. Two responsibilities: (1) at session start, inject every registered skill's `name` + `description` into context so the model cannot "forget" installed skills exist; (2) per task, match the task against skill descriptions via keyword routes + fuzzy scoring with risk penalty, and forward to the top match or report a gap.
_Avoid_: router, dispatcher, classifier

**Installer (安装配置器)**:
The module that imports skills from external sources and installs them to platforms. Three sub-modules: `importer.py` (pull SKILL.md from GitHub repos or local paths, normalize frontmatter, register in INDEX.yaml) + `adapters/` (translate to workbuddy/codex/hermes) + `bootstrap/` (session-start verification).
_Avoid_: adapter (use only as a sub-component), loader, packager

**Importer (导入器)**:
Source-agnostic skill puller. Part of Installer. Scans GitHub repos (`owner/repo`) or local paths for SKILL.md files, normalizes frontmatter to ensure required fields exist, copies to `domain/<category>/<name>/`, and registers in INDEX.yaml. Works with any repo following the SKILL.md convention.
_Avoid_: downloader, cloner

**Review (审查)**:
The horizontal module with two focused scopes: (1) **Reflection Gate** — after Distributor routes to a skill, verify the model actually executed it; if not, re-inject "you mentioned X but did not execute it" so the model must respond. (2) **Lifecycle Governance** — review/merge/split/retire skills in INDEX.yaml. Code Review and Task Recheck were removed (ecosystem's job).
_Avoid_: validation, audit, verification, quality-check

**Reflection Gate (反射门禁)**:
The mechanism that catches "routed but skipped" hallucination. After Distributor routes a task to skill X and the model produces output, Review checks whether X was actually invoked. If not, it injects a reflection forcing the model to either execute X or explain why it doesn't apply. The model cannot silently ignore the injection. This is anti-hallucination layer 3/3 — no other layer (model, platform, superpowers) catches this.
_Avoid_: soft block, advisory, warning

**Anti-hallucination Triad (反幻视三层)**:
MY_SKILL's core value proposition. Three layers that together prevent "installed but ignored": (1) Distributor session-start injection — model sees all skill descriptions; (2) Distributor routing — model doesn't choose freely, the router picks; (3) Review Reflection Gate — model can't skip what was routed.
_Avoid_: skill enforcement, invocation guarantee

**Discoverability Guarantee (发现性保证)**:
Distributor's primary responsibility. At session start, read INDEX.yaml and inject all skill `name` + `description` pairs into context as a manifest. The model cannot claim it did not know a skill existed. This is anti-hallucination layer 1/3.
_Avoid_: skill listing, menu injection

**Capability (能力)**:
A category in the domain layer corresponding to a core LLM capability. Five categories: Understanding, Generation, Retrieval, Execution, Decision. The framework supports all five, but only 3 seeds currently exist (decide-invest / ui-design / ux-design) — the rest are imported on demand from the ecosystem.
_Avoid_: domain, category, area

**Seed (种子技能)**:
A skill kept in MY_SKILL because no public ecosystem equivalent exists. v0.1 had 18 seeds; v0.2 kept only 3 (decide-invest, ui-design, ux-design) and removed 15 that overlap with superpowers/mattpocock/platform-native tooling. New skills are added via `importer.py`, not generated internally.
_Avoid_: starter, template, example

**INDEX.yaml**:
The skill registry inside Distributor. Lists every skill's `name` + `risk_level` + `category` + `user-invocable` + `path` + `status` + `last_reviewed`. Used for session-start injection and routing. Currently 8 entries (5 meta + 3 domain).
_Avoid_: registry, catalog, manifest

**Gap Detection (缺口检测)**:
When Distributor's top match composite score falls below the threshold (default 50), it reports a gap — "no installed skill matches; consider importing one with `installer import <repo>` or writing a new SKILL.md". Unlike v0.1, it does NOT auto-trigger a Builder; the user decides.
_Avoid_: fallback, auto-generation
