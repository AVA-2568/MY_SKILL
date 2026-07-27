---
name: installer-bootstrap
description: "Session-activation sub-module of Installer. Verifies Distributor is always-loaded and INDEX.yaml matches the filesystem; rebuilds on drift."
user-invocable: false
risk_level: low
---

# Bootstrap (启动器)

Runs once at session start. Part of Installer's `bootstrap/` sub-module (see ADR-0007).

## Procedure

1. **Verify Distributor** — confirm `meta/distributor/SKILL.md` carries `user-invocable: false` + `always_active: true`. If not, warn the user: routing is broken.
2. **Verify on-demand scope** — confirm all other meta skills (builder / installer / domain-entry) and every domain skill stay `user-invocable: true` (horizontal components stay `false`). They load on demand, not always.
3. **Verify INDEX.yaml** — list actual `domain/` + `meta/` SKILL.md files; compare against `meta/distributor/INDEX.yaml`. On drift, rebuild INDEX.yaml from frontmatter and report.
4. **Report** — print an installation-status summary; surface any mismatch before the session proceeds.

## Drift handling

- Skill present on disk but missing in INDEX.yaml → add entry from its frontmatter.
- Entry in INDEX.yaml but skill deleted → remove the entry.
- Stale `risk_level` / `category` → overwrite from frontmatter.
- Never silently proceed on drift; report and resolve first.
