# Protocol Compatible + Adapters

SKILL.md core fields (name + description) are compatible with the Anthropic Agent Skills standard. Extension fields (risk_level, verifiable, disable-model-invocation, etc.) are self-designed. Three target platforms (workbuddy / codex / hermes) each get a lightweight adapter that translates platform-specific field conventions.

**Status**: accepted
**Considered Options**:
- A. Fully autonomous SKILL.md specification
- B. Protocol-compatible + adapters (adopted)
- C. Pure distribution: three independent copies per platform
**Why B**: The intersection of three platforms' SKILL.md formats is the Anthropic standard (name + description). Trading 4 fields' naming for 95% design space and zero-friction cross-platform loading is the right deal. The three platforms' differing extension fields (workbuddy `disable-model-invocation`, hermes `platforms`/`metadata.hermes.requires_tools`, etc.) are absorbed by per-platform adapters.
