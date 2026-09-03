# AGENTS.md

BMAD Method project — Agile AI-Driven Development workflow with OpenCode and Claude Code.

## Project Setup

- **User**: Hsantos
- **Communication language**: English
- **Artifacts output**: `_bmad-output/`
- **Project knowledge**: `docs/` (not yet populated)
- **Config files**: `_bmad/config.toml`, `_bmad/config.user.toml` (do not edit; re-run `npx bmad-method install` to change)

## BMAD Skills

49 skills installed in `.agents/skills/` and `.claude/skills/`. Skills are invoked through OpenCode commands in `.opencode/commands/`.

### Entry Points

| Command | Purpose |
|---------|---------|
| `bmad-help` | Start here — orient to workflow, get next-step recommendations |
| `bmad-build` | Main code implementation: fix, feature, refactor |
| `bmad-build-auto` | Autonomous unattended build loop |
| `bmad-brainstorming` | Ideation and creative exploration |
| `bmad-forge-idea` | Pressure-test an idea through persona interrogation |
| `bmad-create-prd` | Product requirements document |
| `bmad-architecture` | System architecture design |
| `bmad-ux` | UX patterns and design specs |
| `bmad-create-epics-and-stories` | Break work into trackable stories |
| `bmad-sprint-planning` | Sprint readiness and status |
| `bmad-code-review` | Adversarial code review |
| `bmad-retrospective` | Epic retrospective with evidence-based verdict |

### Skill Invocation Rule

Skills must be rendered via the shared script — **do not** invoke workflow files directly:

```bash
uv run _bmad/scripts/render_skill.py --project-root /home/hsantos/app --skill .claude/skills/<skill-name>
```

On failure (including missing `uv`), report output and HALT. Do not run any workflow source directly.

### BMAD Workflow Phases

1. **Clarify** — `bmad-help`, `bmad-brainstorming`, `bmad-forge-idea`
2. **Plan** — `bmad-create-prd`, `bmad-architecture`, `bmad-ux`, `bmad-create-epics-and-stories`
3. **Build** — `bmad-build`, `bmad-build-auto`
4. **Review** — `bmad-code-review`, `bmad-checkpoint-preview`
5. **Learn** — `bmad-retrospective`

Small changes can skip straight to build. Complex work follows the full path.

## Prerequisites

- **Node.js** >= 20.12 (currently v24.20)
- **Python** >= 3.10 (currently 3.12)
- **uv** (0.12.9) — required for rendering skills; install at `~/.local/bin/uv`
- **Git** — required for updates and external modules

## Updating BMAD

```bash
npx bmad-method install
```

Detects existing installation and offers update/modification. Remove any stale `bmad-*` entries from legacy command directories if the installer warns about duplicates.

## Project State

This is a **greenfield** project — no application code exists yet. Use `bmad-help` to begin.
