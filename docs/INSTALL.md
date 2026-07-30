# Deploying MY_SKILL (AI-driven)

Deployment is **AI-driven**. MY_SKILL's `installer` module is the operator —
you do not deploy skills by typing shell commands. You ask the agent, and it
runs the `installer` skill. A human running `sync.py` directly is only an
escape hatch (see [Manual fallback](#manual-fallback-no-agent-available)).

## Sync workflow (the core contract)

MY_SKILL repo is the canonical source. GitHub is the cloud relay. Platform directories are read-only consumers.

```
Platform A (edit in repo) ──git push──▶ GitHub ──git clone──▶ Platform B (one-shot install)
```

**Key contracts** (see [README sync workflow](../README.md#sync-workflow-cross-machine--cross-platform)):

| Contract | Why |
|---|---|
| Edit only in the repo | Keeps canonical source clean; no platform-format pollution flows back |
| Platform dir is read-only | Synced derivatives are overwritten on next sync |
| GitHub is the only relay | Don't transfer skills via USB / email; always go through GitHub |

## One-shot install (new machine)

On a new machine, tell the agent "install MY_SKILL", or run:

```bash
curl -fsSL https://raw.githubusercontent.com/AVA-2568/MY_SKILL/main/meta/installer/scripts/install.sh | bash
```

This will:
1. `git clone` (or `git pull`) the repo to `~/MY_SKILL`
2. Auto-detect the installed platform (workbuddy / codex / hermes)
3. Run `sync.py --auto-detect` to install all skills
4. Report the result

## How it works

- **Bootstrap (automatic, every session start)** — `meta/installer/bootstrap/`
  verifies the Distributor is always-active and that `INDEX.yaml` matches the
  `domain/` + `meta/` filesystem; it rebuilds the index on drift and reports
  status. You never run this manually.
- **Installer (on demand)** — the `installer` skill reads `INDEX.yaml`, runs the
  per-platform adapter (`meta/installer/adapters/<platform>.yaml`), and writes
  the translated `SKILL.md` files into the target platform's skill directory.
- **Auto-detect** — `sync.py --auto-detect` probes `~/.workbuddy/`, `~/.codex/`,
  `~/.hermes/` and picks the first match. Override with `--target` if needed.
- **Field translation** — core fields (`name`, `description`) pass through
  unchanged (ADR-0002); extension fields are adapted per platform (e.g.
  `user-invocable: false` is preserved as-is for WorkBuddy — it is a native
  WorkBuddy field meaning "hidden from /slash menu but callable by the AI /
  other skills", exactly what Distributor's internal use needs;
  `risk_level` → trailing `[risk=...]` tag in `description`).

## Trigger a deployment

You invoke the agent; the agent runs the skill. Either:

- **One-shot install**: "install MY_SKILL" → runs `install.sh` (clone + sync).
- **Slash command**: `/installer sync` — install every registered skill to the
  detected platform.
- **Natural language**: "把 MY_SKILL 装到 WorkBuddy" / "install MY_SKILL to
  WorkBuddy" — the Distributor routes to `installer`.
- **Single skill**: `/installer install <skill-name> --platform=workbuddy`.

The agent reports what it wrote, skipped, and any conflicts.

## Safety rules (enforced by the agent)

1. **同名不覆盖** — if a skill already exists at the target with the same name,
   the agent skips and warns. Use `--force` to overwrite.
2. **冲突技能黑名单** — these default to skip (overlap with your existing skills):
   - `decide-invest` — financial-decision guard; withhold from auto-deploy.
3. **金融类技能** — `decision/` skills default to `mid` risk; the agent warns
   before installing.
4. **冲突解决** — on a name clash the agent compares `source` / `agent_created`
   (or `agent_adapted`) and preserves your customized version unless you pass
   `--force`. It always reports conflicts; it never silently overwrites.

## Uninstall

```bash
rm -rf ~/.workbuddy/skills/<skill-name>
# This does NOT affect the MY_SKILL source repository
```

## `--force`

```
/installer install <skill-name> --platform=workbuddy --force
# or, for the whole library: /installer sync --force
```

Overrides the skip-list and the exists-check.

## Manual fallback (no agent available)

The installer's translator is `meta/installer/scripts/sync.py`. Run it directly
only when no agent is available:

```bash
cd /path/to/MY_SKILL

# Auto-detect platform and target directory:
python meta/installer/scripts/sync.py --auto-detect --dry-run
python meta/installer/scripts/sync.py --auto-detect

# Or specify target explicitly:
python meta/installer/scripts/sync.py --target ~/.workbuddy/skills
```

## Verification

After deployment, the agent prints an installation-status summary. To check
yourself:

```bash
ls ~/.workbuddy/skills/
head -5 ~/.workbuddy/skills/<skill-name>/SKILL.md
```

The Distributor and Review carry `user-invocable: false` after translation,
so they load automatically every session. Domain skills remain user-invocable.
