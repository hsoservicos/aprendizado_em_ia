# AGENTS.md

BMAD Method project — Agile AI-Driven Development workflow. This file is read by
**OpenCode**; **Claude Code** reads `CLAUDE.md`, which imports this file. Both
coding agents are first-class and share one configuration, skill set, and toolchain.

## Project Setup

- **User**: Hsantos
- **Communication language**: Português do Brasil (PT-BR)
- **Artifacts output**: `_bmad-output/`
- **Project knowledge**: `docs/` (not yet populated)
- **Config files**: `_bmad/config.toml`, `_bmad/config.user.toml` (do not edit; re-run `npx bmad-method install` to change)
- **Agent instructions**: `AGENTS.md` (OpenCode) + `CLAUDE.md` (Claude Code — imports `AGENTS.md`)
- **Claude Code settings**: `.claude/settings.json` (tool allow-list + RTK `PreToolUse` hook)
- **Tools Registry**: `_bmad-output/tools-registry.md` (update when installing new tools)

## Coding Agents

| Concern | OpenCode | Claude Code |
|---------|----------|-------------|
| Instructions | `AGENTS.md` | `CLAUDE.md` → `@AGENTS.md` |
| Skill source | `.agents/skills/` (57) | `.claude/skills/` (57) |
| Skill invocation | `.opencode/commands/*.md` wrappers (`/bmad-*`) | native discovery (`/bmad-*`, or model-selected) |
| Tool allow-list | inherits shell | `.claude/settings.json` → `permissions.allow` |
| RTK token compression | `~/.config/opencode/plugins/rtk.ts` | `.claude/settings.json` → `PreToolUse` hook (`rtk hook claude`), ref `.claude/RTK.md` |

`.agents/skills/` and `.claude/skills/` are kept byte-identical — `npx bmad-method install`
regenerates both; a manual change to one must be mirrored to the other.

## Onboarding — first steps

Anyone using this repo to **start a new project** or to **work on a legacy
codebase being modernized** must run the pre-flight in
**`_bmad-output/getting-started.md`** first (environment + both agents + RTK check
+ project config), then follow one of two tracks:

- **Track A — greenfield**: `/bmad-help` → the 5-phase lifecycle
  (`_bmad-output/bmad-project-lifecycle-guide.md`).
- **Track B — brownfield / legacy**: `/bmad-project-context` (capture the repo's
  stack + conventions into `AGENTS.md`/`CLAUDE.md`) → `/bmad-code-review`
  (quality baseline) → `/bmad-build` for scoped changes.

## BMAD Skills

57 skills, installed once and exposed to **both** agents via the two skill trees
above. Entry points are identical from either agent (`/bmad-help`, `/bmad-build`, …).

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
# Claude Code
uv run _bmad/scripts/render_skill.py --project-root /home/hsantos/app --skill .claude/skills/<skill-name>
# OpenCode
uv run _bmad/scripts/render_skill.py --project-root /home/hsantos/app --skill .agents/skills/<skill-name>
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
- **Python** >= 3.10, < 3.14 (currently 3.12)
- **uv** (0.12.9) — required for rendering skills; install at `~/.local/bin/uv`
- **Git** — required for updates and external modules
- **GitHub CLI** (`gh`, 2.73.0) — repo / PR / release operations; `~/.local/bin/gh`
- **ripgrep** (14.1.1) — fast search, RTK dependency; `~/.local/bin/rg`
- **CrewAI** (1.15.18) — multi-agent orchestration; `~/.local/bin/crewai`
- **RTK** (0.47.0) — token compression proxy; `~/.local/bin/rtk`. Wired into
  **both** agents — OpenCode via `~/.config/opencode/plugins/rtk.ts`, Claude Code
  via the `PreToolUse` hook in `.claude/settings.json`. Per-machine setup for
  both at once: `rtk init -g --auto-patch --opencode`.
- **Coding agent**: OpenCode (1.18.27) and/or Claude Code (2.1.260)

Every tool above is available from **both** OpenCode and Claude Code. Claude Code
pre-approves `uv`, `rtk`, `rg`, `gh`, `crewai`, and `npx bmad-method` in
`.claude/settings.json`; OpenCode inherits them from the shell `PATH`.

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

Both scripts install the full toolchain, both agents, and wire RTK into OpenCode
**and** Claude Code (`rtk init -g --auto-patch --opencode`). See
`_bmad-output/scripts/README.md` for detailed instructions.

## Project State

This is a **greenfield** project — no application code exists yet. New here? Run
the pre-flight in `_bmad-output/getting-started.md`, then `/bmad-help` to begin.
