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
- *Per-skill*: Lifecycle Governance — review, merge, split, retire skills. The meta-governance role no major public skill ecosystem abstracts as a first-class skill.
_Avoid_: auditor, quality gate

**thinking-first**:
Pre-route cognitive discipline. 5 rules: (1) truly understand intent, (2) anchor factual claims to sources, (3) declare uncertainty honestly, (4) verify against requirements before delivering, (5) do only what was asked — no scope creep.
_Avoid_: cognitive checklist, pre-flight check

**caveman**:
Two trigger points: pre-think constrains the model's thinking block to ≤5 short points; post-output compresses residual verbosity from the final output. The per-turn equivalent of an editor that cuts fluff.
_Avoid_: compress, shorten, trim

**grill-with-docs**:
Triggered when Distributor detects a task gap (no matching skill found). Interrogates the user about design intent (what should the missing skill do), then writes a new ADR + glossary entry. The design-to-docs pipeline.
_Avoid_: gap handler, design interrogator

## The Five LLM Capabilities

| Category | What it covers | Seed skills |
|---|---|---|
| **Understanding** | Read input, parse context, recognize intent | comprehend-code, comprehend-doc |
| **Generation** | Produce output — code, docs, contracts, architecture, schemas, visual specs | generate-api, generate-doc, api-design, system-design, database-design, ui-design, ux-design, writing-great-skills, handoff, teach |
| **Retrieval** | Find information, query data, call APIs (incl. analysis) | retrieve-rag, retrieve-sql |
| **Execution** | Run commands, manipulate files, invoke tools | execute-bash, execute-git |
| **Decision** | Plan, choose, weigh tradeoffs (incl. analysis) | decide-invest, decide-product |

**Governance** (lifecycle management) belongs to Review (horizontal), not to Domain — maintaining a clean separation of concerns.
