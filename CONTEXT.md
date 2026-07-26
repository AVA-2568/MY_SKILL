# MY_SKILL

A cross-platform AI skill library (workbuddy + codex + hermes), self-use, fully autonomously rebuilt from scratch. The 4-vertical + 1-horizontal architecture classifies the domain layer by LLM capability graph rather than by task content.

## Language

**Skill**:
A self-contained package of instructions, scripts, and resources that an AI agent loads dynamically to perform a specialized task. A skill consists of a `SKILL.md` file (required) plus optional bundled resources (`scripts/`, `references/`, `assets/`).
_Avoid_: prompt template, instruction file, recipe

**Distributor (分发器)**:
The vertical module that routes user tasks to the most appropriate skill. Implements soft routing via description matching, plus risk scoring (soft constraint) and gap detection (triggers Builder when no skill matches).
_Avoid_: router, dispatcher, classifier

**Builder (构建器)**:
The vertical module that creates new skills on demand. Three internal sub-modules: `confirm` (clarify user intent) → `plan` (design skill structure) → `generate` (write SKILL.md + bundled resources). Decoupled from the domain layer.
_Avoid_: skill creator, generator, scaffolder

**Installer (安装配置器)**:
The vertical module that translates a generic SKILL.md into platform-specific formats (workbuddy / codex / hermes) and bootstraps session loading (only Distributor is always-active; others are on-demand).
_Avoid_: adapter (use only as a sub-component), loader, packager

**Review (审查)**:
The horizontal concern that intercepts every task and governs the skill library. Two scopes:
- *Per-task*: three sub-types — Code Review (product view, soft gate), Task Recheck (goal view, soft gate), Security Review (risk view, reflection gate + extreme-risk hard gate). Triggered at input / process / output points of every task.
- *Per-skill*: Lifecycle Governance — review, merge, split, retire skills. The meta-governance role no major public skill ecosystem abstracts as a first-class module; MY_SKILL treats it as part of Review.
_Avoid_: validation, audit, verification, quality-check

**Thinking-First (思考纪律)**:
A horizontal discipline skill force-triggered by Distributor **pre-route** (before any task routes). Enforces 5 cognitive rules: understand the task / source-anchor every fact / honestly mark uncertainty / pre-delivery self-check / minimal intervention. Cannot be /slash-called directly.
_Avoid_: self-check, sanity-check (these are softer, less structured)

**Caveman (思考约束 + 输出压缩)**:
A horizontal discipline + compression skill force-triggered by Distributor at **two** points: (1) **pre-think** (after thinking-first, before routing) — constrains the model's *thinking itself* to 3-5 short points (each ≤10 words), preventing verbose thought generation rather than post-deleting; (2) **post-output** (after Domain skill) — compresses residual verbosity in the final output. Pre-think is the primary lever (it affects AI thought); post-output is the safety net. Cannot be /slash-called directly.
_Avoid_: summarize, shorten (these are softer, no discipline; caveman constrains thinking, not just output)

**Grill-With-Docs (设计拷问 + ADR 落地)**:
A horizontal design-interrogation skill force-triggered by Distributor **on-gap** (when match_score < threshold, OR task is design/planning). Runs relentless one-question-at-a-time interrogation, lands each decision as an ADR, and updates the glossary. Cannot be /slash-called directly.
_Avoid_: brainstorm, design-thinking (these are softer, no ADR discipline)

**Capability (能力)**:
A category in the domain layer corresponding to a core LLM capability. Five categories: Understanding, Generation, Retrieval, Execution, Decision. Generation includes both implementation skills (`generate-api`, `generate-doc`) and design-specification skills (`api-design`, `system-design`, `database-design`, `ui-design`, `ux-design`).
_Avoid_: domain, category, area

**Reflection Gate (反射门禁)**:
A security review pattern where detected risks are injected back into system context, forcing the model to explicitly process (fix / explain / refuse) them before continuing. Does not directly block flow but cannot be silently ignored.
_Avoid_: soft block, advisory, warning

**B-Chain (B 链式)**:
The trigger relationship among the four verticals. `Distributor → Domain` (with Review as horizontal). When Distributor detects a gap (no matching skill), it triggers Builder to create a new skill, which is registered and routed back through Distributor.
_Avoid_: pipeline, sequential flow, waterfall

**Seed (种子技能)**:
A pre-built skill in the MVP that demonstrates the architecture and provides initial coverage for common tasks. The B-Chain grows the library beyond seeds via gap-triggered creation.
_Avoid_: starter, template, example

**INDEX.yaml**:
A lightweight lookup file inside Distributor, listing every skill's `name + risk_level + capability_category + status`. Used for fast routing. Not a separate registry module — frontmatter and Review own the other metadata.
_Avoid_: registry, catalog, manifest

**Soft Gate (软门禁)**:
A review pattern that emits advisory output without blocking flow. Used by Code Review and Task Recheck. The model may proceed with the advisory unaddressed.
_Avoid_: warning, suggestion

**Hard Gate (硬门禁)**:
A review pattern that blocks flow until the risk is resolved. Used only at the extreme-risk tier of Security Review.
_Avoid_: blocker, hard stop
