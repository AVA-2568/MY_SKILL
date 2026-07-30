# Changelog

All notable changes to MY_SKILL are documented here. This project follows a
lightweight `vMAJOR.MINOR.PATCH` scheme; MVP is tagged `v0.1.0-mvp`.

## [v0.1.0-mvp] - 2026-07-27

First runnable skeleton — the MVP minimum viable library.

### Added
- **Architecture**: 4 verticals (Distributor / Builder / Installer / Domain-entry) + 1 horizontal layer (Review / thinking-first / caveman / grill-with-docs). See `docs/adr/0003`.
- **Protocol**: A-protocol compatible (Anthropic `SKILL.md` standard `name` + `description`) with per-platform adapters (`workbuddy` / `codex` / `hermes`). See `docs/adr/0002`.
- **ADRs**: 7 accepted architecture decision records (`docs/adr/0001`–`0007`) covering Q1–Q7.
- **Meta modules**: 8 skills — `distributor`, `builder`, `installer` (+ `adapters` + `bootstrap`), `domain-entry`, `review`, `thinking-first`, `caveman`, `grill-with-docs`.
- **Domain seeds**: 18 seed skills across 5 LLM capabilities — Understanding (2), Generation (10), Retrieval (2), Execution (2), Decision (2). Includes 3 productivity skills forked from `mattpocock/skills@productivity` (`writing-great-skills` / `handoff` / `teach`).
- **Registry**: `meta/distributor/INDEX.yaml` registering 8 meta modules + `installer-bootstrap` + 18 domain skills (27 total) with routing thresholds and lifecycle governance.
- **Docs**: `README.md` (architecture diagram, English), `README.zh-CN.md` (中文版), `CONTEXT.md` (glossary), `AGENTS.md` (agent read order), `docs/INSTALL.md` (deploy guide).
- **Repo meta**: `LICENSE` (MIT), `CHANGELOG.md`, `.github/workflows/validate.yaml` (frontmatter + YAML lint), `CONTRIBUTING.md`.

### Fixed
- YAML frontmatter validity: `description` values containing `: ` or inner quotes are now double-quoted with inner `"` escaped as `\"`; adapter `target` / `field` values quoted. All SKILL.md frontmatter now parse cleanly.
- **2026-07-27 audit fixes**:
  - CI `validate.yaml`: registration check accepts `path` or `id` field (was `id`-only, silently failed all 27 skills)
  - `CONTRIBUTING.md`: documented `path` field instead of `id`
  - `meta/domain-entry/SKILL.md`: repaired broken markdown table (prose between Generation and Retrieval rows)
  - 9 meta skills: added `category: meta` to frontmatter (was INDEX-only)
  - 10 domain seed skills: removed "skeleton — Builder will expand" placeholder + added `agent_created: true`
  - CI dry-run: 27/27 SKILL.md pass full validation

## [v0.2.0] - 2026-07-30

Repositioned from content library to skill infrastructure. See [ADR-0008](./docs/adr/0008-slim-infra-not-content-library.md).

### Removed
- **15 domain seeds** with ecosystem equivalents (execute-bash, execute-git, generate-doc, generate-api, api-design, system-design, database-design, writing-great-skills, handoff, teach, comprehend-code, comprehend-doc, retrieve-rag, retrieve-sql, decide-product). Use `obra/superpowers` or `mattpocock/skills` via the new importer instead.
- **4 meta modules**: `thinking-first`, `caveman`, `grill-with-docs`, `builder`. Cognitive discipline is the model's responsibility; design interrogation is covered by superpowers `brainstorming`; auto-generation on gap was over-engineered.
- **Review's Code Review + Task Recheck** gates — ecosystem covers these. Only Reflection Gate + Lifecycle Governance remain.

### Changed
- **Distributor** repositioned from "router + forced-trigger scheduler" to "discoverability guarantor + router". Session-start injection of all skill descriptions into context is now the primary anti-hallucination mechanism.
- **Review** repositioned to "Reflection Gate + Lifecycle Governance only". Catches "routed but skipped" (anti-hallucination layer 3).
- **INDEX.yaml** slimmed from 27 entries to 8 (5 meta + 3 domain).
- **score.py** KEYWORD_ROUTES slimmed from 28 to 12; removed `grill-with-docs` routable-despite-false exception.
- **skip.yaml** removed thinking-first/caveman entries (modules deleted).

### Added
- **`importer.py`** — source-agnostic skill importer. Pulls SKILL.md from any GitHub repo (`owner/repo/path`) or local path, normalizes frontmatter, installs to `domain/<category>/<name>/`, registers in INDEX.yaml.
- **ADR-0008** — documents the repositioning decision + the anti-hallucination triad.

### Stats
- Skill count: 27 → 8. Meta modules: 8 → 5. Domain seeds: 18 → 3.

## [v0.2.1] - 2026-07-30

GitHub-based sync workflow — one-shot install on any new machine.

### Added
- **`install.sh`** — one-shot installer. `curl ... | bash` clones the repo (or `git pull` if exists), auto-detects the platform, runs `sync.py --auto-detect`, reports the result.
- **`sync.py --auto-detect`** — `PLATFORMS` detection table probes `~/.workbuddy/`, `~/.codex/`, `~/.hermes/` and picks the first match. No more `--target` guessing.
- **Sync workflow docs** — README (EN + zh-CN) added a "Sync workflow" section explaining the core contract: edit only in repo, platform dir is read-only, GitHub is the only relay. INSTALL.md updated with one-shot install instructions.

### Key contract

| Contract | Why |
|---|---|
| Edit only in the repo | Keeps canonical source clean |
| Platform dir is read-only | Synced derivatives are overwritten on next sync |
| GitHub is the only relay | Don't transfer skills via USB / email |

This model needs **no "denormalization"** — editing always happens in the repo, so the repo stays clean.

## [Unreleased]

- **Adapter expansion**: port `sync.py` to more platforms (Claude Code, Cursor, Gemini CLI) to match superpowers' platform coverage.
- **Discoverability self-check**: automated test that verifies the model can "see" all installed skills after session-start injection.
- **Reflection Gate implementation**: codify Review's "routed but skipped" detection as a concrete check, not just a procedure.
