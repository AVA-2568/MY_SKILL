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
- **Registry**: `meta/distributor/INDEX.yaml` registering 8 meta + 18 domain skills with routing thresholds and lifecycle governance.
- **Docs**: `README.md` (architecture diagram), `CONTEXT.md`, `AGENTS.md` (agent read order), `GLOSSARY.md`.
- **Repo meta**: `LICENSE` (MIT), `CHANGELOG.md`, `.github/workflows/validate.yaml` (frontmatter + YAML lint), `.github/SECURITY.md`, `CONTRIBUTING.md`.

### Fixed
- YAML frontmatter validity: `description` values containing `: ` or inner quotes are now double-quoted with inner `"` escaped as `\"`; adapter `target` / `field` values quoted. All SKILL.md frontmatter now parse cleanly.
- **2026-07-27 audit fixes**:
  - CI `validate.yaml`: registration check accepts `path` or `id` field (was `id`-only, silently failed all 27 skills)
  - `CONTRIBUTING.md`: documented `path` field instead of `id`
  - `meta/domain-entry/SKILL.md`: repaired broken markdown table (prose between Generation and Retrieval rows)
  - 9 meta skills: added `category: meta` to frontmatter (was INDEX-only)
  - 10 domain seed skills: removed "skeleton — Builder will expand" placeholder + added `agent_created: true`
  - CI dry-run: 27/27 SKILL.md pass full validation

## [Unreleased]

- Placeholder for future work (Phase 1: enrich 6 core seed skills)
