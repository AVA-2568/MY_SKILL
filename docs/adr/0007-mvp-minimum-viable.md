# MVP: Minimum Viable Repository

MVP scope:
- **8 metadata modules** (4 verticals + 1 horizontal layer with 4 components):
  - 4 verticals (on-demand): Distributor / Builder / Installer / Domain-entry
  - 1 horizontal layer (force-triggered by Distributor):
    - Review (per-task + per-skill scopes; see ADR-0004)
    - thinking-first (pre-route cognitive discipline)
    - caveman (pre-think constraint + post-output compression)
    - grill-with-docs (on-gap design interrogation + ADR landing)
  - Installer has 2 internal sub-modules: `adapters/` (per-platform translation) + `bootstrap/` (session activation)
- **18-22 seed skills**: 5 original capability pairs + 5 core design skills under Generation (`api-design`, `system-design`, `database-design`, `ui-design`, `ux-design`) + 3 productivity skills forked from `mattpocock/skills@productivity` (`writing-great-skills`, `handoff`, `teach`)
- **3 platform adapters**: workbuddy, codex, hermes
- **1 INDEX.yaml** for fast skill lookup (inside Distributor)

Estimated effort: 1-2 weeks for a fully runnable skeleton.

**Status**: accepted
**Considered Options**:
- A. Minimum viable (10-15 seeds) (original baseline)
- B. Expanded MVP (15-20 seeds, including 5 core design skills) (intermediate)
- C. Expanded MVP with productivity fork (18-22 seeds, adding 3 mattpocock productivity skills) (adopted)
**Why C**: Options A and B covered common design work via dedicated skills but did not address session-spanning productivity needs — writing skills well, handing off between sessions, and teaching the user. The mattpocock/skills repository provides battle-tested skills for all three under the `productivity` module. Forking them under Generation (rather than spawning a sixth category) keeps the architecture tight while bringing the seed total to 18, well within the medium-scale 25-40 range.
