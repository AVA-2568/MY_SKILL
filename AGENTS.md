# AGENTS.md

Entry point for AI agents operating in this repository.

## Mandatory read order

1. **[docs/adr/0008-slim-infra-not-content-library.md](./docs/adr/0008-slim-infra-not-content-library.md)** — read this first. It explains why MY_SKILL shifted from content library to skill infrastructure, and supersedes parts of ADRs 0003-0007.
2. **[CONTEXT.md](./CONTEXT.md)** — terminology and ubiquitous language.
3. **[docs/adr/](./docs/adr/)** — read all 8 ADRs for full architectural history. ADRs 0001-0007 are historical context; ADR-0008 is the current truth.
4. **[README.md](./README.md)** — high-level architecture diagram and layout.

## Current architecture (post-v0.2.0)

MY_SKILL is **skill infrastructure** (registry + installer + router + review), not a content library. It solves two problems:
1. **N platforms × M skills adaptation** — write/import once, install anywhere.
2. **Model hallucination** ("installed but ignored") — three-layer anti-hallucination triad.

### Modules (5 meta + 3 domain = 8 total)

- **Distributor** (`always_active`, `user-invocable: false`) — discoverability guarantor (session-start injection) + skill router.
- **Installer** (`user-invocable: true`) — source-agnostic importer (`importer.py`) + 3-platform adapters + session bootstrap.
- **domain-entry** (`user-invocable: true`) — browsing entrypoint for the skill registry.
- **Review** (`user-invocable: false`, `horizontal: true`) — Reflection Gate (catch "routed but skipped") + Lifecycle Governance.
- **installer-bootstrap** (`user-invocable: false`) — session-start verification.
- **decide-invest** / **ui-design** / **ux-design** — the only 3 domain seeds (no ecosystem equivalent).

### What was removed in v0.2.0

- 15 domain seeds with ecosystem equivalents (use `installer import` from superpowers/mattpocock instead).
- 4 meta modules: `thinking-first`, `caveman`, `grill-with-docs`, `builder`.
- Review's Code Review + Task Recheck gates (ecosystem's job).

See ADR-0008 for the full rationale.

## Conventions

- SKILL.md core fields (`name`, `description`) conform to the Anthropic Agent Skills standard (see ADR-0002).
- Extension fields (`risk_level`, `user-invocable`, etc.) follow MY_SKILL's own convention; per-platform adapters handle translation.
- Every skill in `domain/` declares its category via frontmatter `category:` (one of understanding / generation / retrieval / execution / decision).
- New skills are added via `importer.py` (from GitHub repos or local paths), not generated internally.

## Local-first development

This repository is built locally first; do not assume the GitHub remote is up to date.
