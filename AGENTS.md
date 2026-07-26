# AGENTS.md

Entry point for AI agents operating in this repository.

## Mandatory read order

1. **[CONTEXT.md](./CONTEXT.md)** — terminology and ubiquitous language. Read this first to understand what each term means in MY_SKILL's domain.
2. **[docs/adr/](./docs/adr/)** — read all 7 ADRs to understand the architectural decisions and their rationale.
3. **[README.md](./README.md)** — high-level architecture diagram and layout.

## Skills (when implemented)

### 4 Verticals (on-demand)

- **Distributor** (always-active, `user-invocable: false`) — the only always-active vertical; routes tasks and force-triggers the horizontal layer.
- **Builder, Installer, Domain-entry** — loaded on demand by the agent or by Distributor.

### Horizontal Layer (4 components, force-triggered by Distributor)

All 4 are `user-invocable: false`; they cannot be /slash-called directly. Distributor invokes them at specific flow points.

- **thinking-first** — pre-route cognitive discipline (5 rules: understand / source-anchor / uncertainty / pre-delivery check / minimal intervention)
- **Review** — per-task (Code Review / Task Recheck / Security Review) + per-skill (Lifecycle Governance)
- **caveman** — pre-think (constrains *thinking* to 3-5 short points) + post-output (compresses residual verbosity). Two trigger points; pre-think is the primary lever.
- **grill-with-docs** — on-gap design interrogation + ADR/glossary landing

## Conventions

- SKILL.md core fields (name, description) must conform to the Anthropic Agent Skills standard (see ADR-0002).
- Extension fields (risk_level, verifiable, etc.) follow MY_SKILL's own convention; per-platform adapters handle translation.
- Every skill in `domain/` declares its capability category via frontmatter `category:` (one of understanding / generation / retrieval / execution / decision).

## Local-first development

This repository is built locally first; do not assume the GitHub remote is up to date. When contributing, check `git log` and `git diff` to understand the current state before making changes.
