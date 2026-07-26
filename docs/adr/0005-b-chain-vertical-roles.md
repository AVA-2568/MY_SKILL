# B-Chain Trigger + Vertical Roles

The four verticals' trigger relationship is the **B-Chain (with builder feedback)**:

```
User task
  ↓
[Distributor] route + risk-score
  ↓ (matched)
[Domain] execute skill  ←— [Review] horizontal
  ↓
Task complete

  ↑ (gap: no skill matched)
[Builder] confirm → plan → generate
  ↓
[Distributor] re-route
```

Vertical role specifics:
- **Distributor**: route (description matching) + risk scoring (soft constraint core) + gap detection → trigger Builder. 3 mandatory responsibilities.
- **Builder**: 3 internal sub-modules — `confirm` (clarify user intent) → `plan` (design skill structure) → `generate` (write SKILL.md + bundled resources). Decoupled from domain.
- **Installer**: adapter (per-platform translation) + bootstrap (only Distributor is `user-invocable: false` always-active; other skills are on-demand) + a lightweight `INDEX.yaml` inside Distributor for fast skill lookup.
- **Domain**: 5 LLM-capability categories of actual-working skills.

**Status**: accepted
**Considered Options**:
- A. Simple chain (Distributor → Domain)
- B. B-chain with builder feedback (adopted)
- C. State machine
- D. Event-driven
**Why B**: Self-evolution is MY_SKILL's core value — encountering a task with no matching skill triggers automatic creation. This matches the "rebuild + self-use" semantics. A simple chain (A) leaves gap tasks deadlocked. State machine (C) and event-driven (D) are over-engineering for the self-use scale. The Distributor's 3 mandatory responsibilities (route + risk-score + gap-trigger-builder) are the minimum complete set for B-Chain + soft constraint.
