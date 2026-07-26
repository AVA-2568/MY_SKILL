# Review Subsystem (Code / Task / Security + Lifecycle Governance)

The horizontal Review layer has two scopes:

**Per-task scope (3 sub-types)**:
- **Code Review** — product view; soft gate; triggers when the task produces code, documents, or data
- **Task Recheck** — goal view; soft gate; triggers when the task has a verifiable outcome
- **Security Review** — risk view; mixed gate; triggers on every task

**Per-skill scope (Lifecycle Governance)**:
- The Review layer also governs the skill library itself: review, merge, split, retire. This is the *meta-governance* role (Q4) that no major public skill ecosystem (anthropics/skills, obra/superpowers, mattpocock/skills) abstracts as a first-class skill — MY_SKILL treats it as part of Review.

The Security Review uses a **Reflection Gate + extreme-risk Hard Gate**:
- Default: detected risks are injected back into system context; the model must explicitly process them (fix / explain / refuse) before continuing. Cannot be silently ignored.
- Extreme risk: hard-block; flow is interrupted pending manual / deeper review.

**Status**: accepted
**Considered Options**:
- A. Writing review / Task review / Meta-governance (3 sub-types, separates meta-governance)
- B. Code review / Task recheck / Security review + Lifecycle Governance (adopted, scopes merged)
- C. Single review + risk level as parameter
**Why B**: The three sub-types map to three LLM-native review viewpoints — *product* (what was produced), *goal* (was the user's intent met), *risk* (is anything dangerous). Options A splits meta-governance into a peer sub-type, but meta-governance is a different *scope* (per-skill, not per-task), so it belongs as a parallel scope rather than a peer sub-type. C collapses the three viewpoints into a single risk gradient that loses semantic precision. The Reflection Gate is the standard pattern in Self-Criticism / Constitutional AI; the extreme-risk hard gate is a fallback for situations the model genuinely cannot self-handle.
