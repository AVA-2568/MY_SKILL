# Four Verticals + One Horizontal Layer

The metadata layer adopts a "4 verticals + 1 horizontal layer" architecture:
- **4 verticals** (on-demand): Distributor / Builder / Installer / Domain-entry
- **1 horizontal layer** (always-active, force-triggered by Distributor at specific flow points):
  - **Review** — per-task (code/task/security) + per-skill (lifecycle governance)
  - **thinking-first** — pre-route cognitive discipline
  - **caveman** — pre-think constraint + post-output compression
  - **grill-with-docs** — on-gap design interrogation + ADR/glossary landing

The horizontal layer is force-triggered by Distributor at specific flow points (pre-route / post-route / on-gap), not loaded on-demand and not user-invocable. This guarantees that every task passes through the discipline layer.

Verticals are triggered by specific events (routing, building, installing, executing). The horizontal layer intercepts every task at input / process / output points.

**Status**: accepted
**Considered Options**:
- A. 5 pieces in parallel (the original "5-piece suite" framing)
- B. 4 verticals + 1 horizontal layer (originally "1 horizontal" = Review only; expanded to 4 components when meta-cognition skills were added) (adopted)
- C. Review embedded inside Distributor
- D. 3 meta-cognition skills as on-demand verticals (rejected — meta-cognition should be always-on discipline, not optional)
**Why B**: Review's three features — "every-task trigger" + "safety hardline" + "classified by task type" — are categorically different from the verticals' "on-demand" pattern. Parallel 5-piece design forces awkward questions like "when does Review trigger?"; the horizontal layer is the more honest topology. The 3 meta-cognition skills (thinking-first, caveman, grill-with-docs) share the same horizontal pattern: they're force-triggered at specific flow points, not user-invocable, and they enforce discipline on every task that reaches them. Naming "1 horizontal layer (4 components)" preserves the 4V+1H simplicity while admitting that the layer has internal structure.
