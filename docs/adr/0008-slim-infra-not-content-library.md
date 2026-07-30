# Slim Infrastructure, Not Content Library

**Status**: accepted
**Date**: 2026-07-30

## Context

MY_SKILL v0.1 shipped as a 27-skill content library (8 meta modules + 18 domain seeds + installer-bootstrap) with a 4-vertical + 1-horizontal architecture. After evaluating the 2026 skill ecosystem, three facts became clear:

1. **Content is a solved problem.** `obra/superpowers` (259k stars, 13 skills, 7+ platforms) and `mattpocock/skills` cover the common skill surface better than a personal repo can. 15 of MY_SKILL's 18 domain seeds have direct equivalents in superpowers or platform-native tooling.

2. **The architecture was over-engineered for actual usage.** The 4 horizontal components (thinking-first / caveman / grill-with-docs / review) and the Builder vertical added structural overhead without solving the user's actual pain point: *skills get installed but the model forgets to use them*.

3. **The user's real intent was infrastructure**, not content: "a pluggable skill library because there are too many agent platforms and configuring skills on each is annoying, plus models hallucinate and ignore installed skills."

## Decision

Reposition MY_SKILL from **content library** to **skill infrastructure** (registry + installer + router + review). Specifically:

### Remove (not infrastructure)

- **15 domain seeds** with ecosystem equivalents (execute-bash, execute-git, generate-doc, generate-api, api-design, system-design, database-design, writing-great-skills, handoff, teach, comprehend-code, comprehend-doc, retrieve-rag, retrieve-sql, decide-product).
- **4 meta modules** that were over-engineered for personal use:
  - `thinking-first` / `caveman` — cognitive discipline is the model's own responsibility (extended thinking, system prompt). Wrapping as forced skills added overhead without quality gain.
  - `grill-with-docs` — design interrogation covered by superpowers `brainstorming`.
  - `builder` — auto-generating skills on gap was over-engineered; on gap, report and let the user import or hand-write.

### Keep + reposition (is infrastructure)

| Module | Old role | New role |
|---|---|---|
| **Distributor** | Router + forced-trigger scheduler | **Discoverability guarantor** + router. Session-start injection of all skill descriptions into context (anti-hallucination layer 1/2). |
| **Installer** | 3-platform adapter | 3-platform adapter + **source-agnostic importer** (pull skills from any GitHub repo or local path). |
| **Review** | 3 per-task gates + lifecycle | **Reflection Gate only** (catch "routed but skipped" — anti-hallucination layer 3/3) + lifecycle governance. Code Review / Task Recheck removed (ecosystem's job). |
| **domain-entry** | 5-category browser | Browsing entrypoint for the remaining skills. |
| **3 domain seeds** | Part of 18-skill library | The only skills with no ecosystem equivalent: `decide-invest` (financial), `ui-design` + `ux-design` (visual/UX specs — superpowers does engineering flow, not visual design). |

### Add

- **`importer.py`** — source-agnostic skill importer. Pulls SKILL.md from any GitHub repo (`owner/repo/path`) or local path, normalizes frontmatter, installs to `domain/<category>/<name>/`, registers in INDEX.yaml. Works with superpowers, mattpocock, or any repo following the SKILL.md convention.

## The anti-hallucination triad

The repositioning clarifies MY_SKILL's unique value — solving "installed but ignored" via three layers:

| Cause of hallucination | Owner | Mechanism |
|---|---|---|
| Model never loaded skill description | Distributor | Session-start injection forces all descriptions into context |
| Model loaded but mis-routes | Distributor | Keyword routes (exact) + fuzzy score (semantic) pick the match |
| Model routed but skipped execution | Review | Reflection Gate re-injects "you mentioned X but did not execute it" |

No other layer in the stack (model, platform, superpowers) catches cause 3. This is MY_SKILL's defensible niche.

## Consequences

- **Skill count**: 27 → 8 (5 meta + 3 domain). Maintenance cost drops sharply.
- **No more Builder**: on gap, Distributor reports and suggests `installer import` or manual creation. The user decides, not the system.
- **No more forced discipline layer**: thinking-first / caveman / grill-with-docs removed. The model's own extended thinking handles cognitive discipline.
- **ADRs 0003/0004/0005/0006/0007 are partially superseded**: their descriptions of 4V+1H, Review's 3 gates, B-Chain, 5 capabilities, and MVP scope no longer match reality. They remain as historical context; ADR-0008 is the current truth.
- **Future skill growth**: skills are added via `importer.py` from external repos, not generated internally. MY_SKILL is a pipe, not a source.
