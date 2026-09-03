# AGENTS.md

BMAD Method project — Agile AI-Driven Development workflow with OpenCode and Claude Code.

## Project Setup

- **User**: Hsantos
- **Communication language**: Português do Brasil (PT-BR)
- **Artifacts output**: `_bmad-output/`
- **Project knowledge**: `docs/` (not yet populated)
- **Config files**: `_bmad/config.toml`, `_bmad/config.user.toml` (do not edit; re-run `npx bmad-method install` to change)
- **Tools Registry**: `_bmad-output/tools-registry.md` (update when installing new tools)

## BMAD Skills

57 skills installed in `.agents/skills/` and `.claude/skills/`. Skills are invoked through OpenCode commands in `.opencode/commands/`.

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
| `bmad-docker` | Docker containerization: Dockerfile, Compose, BuildKit, security |
| `bmad-agent-docker` | Docker Architect Agent — container infrastructure specialist |
| `bmad-python314` | Python 3.14+: free-threading, subinterpreters, t-strings, compression |
| `bmad-agent-python314` | Python Architect Agent — modern Python specialist |
| `bmad-php84` | PHP 8.4: Property Hooks, Asymmetric Visibility, DOM API, array functions |
| `bmad-agent-php84` | PHP Architect Agent — multi-role (Arch-PHP, CodeRefactor-PHP, WebSec-PHP) |
| `bmad-postgres18` | PostgreSQL 18: AIO, Skip Scan, UUIDv7, pgvector, RETURNING OLD/NEW |
| `bmad-agent-postgres18` | PostgreSQL Architect Agent — 5 SKILLs (DDL, OPT, VEC, CONC, SEC) |

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
- **RTK** (0.47.0) — token compression proxy; install at `~/.local/bin/rtk`
- **ripgrep** (14.1.1) — fast search; install at `~/.local/bin/rg`

## Updating BMAD

```bash
npx bmad-method install
```

Detects existing installation and offers update/modification. Remove any stale `bmad-*` entries from legacy command directories if the installer warns about duplicates.

## Automated Installation

For new environments, use the installation scripts:

```bash
# Linux (Ubuntu/Debian)
chmod +x _bmad-output/scripts/install-linux.sh
./_bmad-output/scripts/install-linux.sh

# Windows (PowerShell as Administrator)
powershell -ExecutionPolicy Bypass -File _bmad-output/scripts/install-windows.ps1
```

See `_bmad-output/scripts/README.md` for detailed instructions.

## Project State

This is a **greenfield** project — no application code exists yet. Use `bmad-help` to begin.
