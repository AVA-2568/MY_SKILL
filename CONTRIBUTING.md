# Contributing to MY_SKILL (AI Agent Guidelines)

## Prerequisites

- **INDEX.yaml addition**: Every skill must be registered in `meta/distributor/INDEX.yaml` with a `path` field (relative path from repo root to the skill directory).
- **SKILL.md**: Must have valid YAML frontmatter with `name` and `description`.
- **Code review**: All generated content must pass the Review layer's Code Review gate.

## Guidelines

1. **Never bypass responsibility**: Don't say "only the user can do that" — help the user complete the task.
2. **Don't skip based on tool capabilities**: Use `domain-entry` first before saying "I can't do this".
3. **Write skills that transfer**: A skill should be actionable by another agent or the user, not depend on the original creator's knowledge.
4. **Bundle non-textual resources**: Scripts, configs, and references belong in `scripts/`, `configs/`, or `references/` subdirectories within the skill directory, not inline in the SKILL.md.
