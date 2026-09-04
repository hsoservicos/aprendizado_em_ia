# BMAD Method — Agile AI-Driven Development

![Version](https://img.shields.io/badge/version-6.11.0-blue)
![Skills](https://img.shields.io/badge/skills-57-green)
![CrewAI](https://img.shields.io/badge/CrewAI-1.15.18-purple)
![Coolify](https://img.shields.io/badge/Coolify-4.3.14-orange)
![License](https://img.shields.io/badge/license-MIT-yellow)

**Languages:** English | [Português Brasil](README.pt-BR.md) | [Español](README.es.md)

---

## Overview

BMAD Method (Breakthrough Method for Agile Development) is an AI-powered development framework that integrates specialized agents and skills into your development workflow. This project provides a complete environment for agile software development using AI assistants, with **Coolify deployment** support for self-hosted PaaS infrastructure.

**Key Features:**
- 57 specialized skills for different development tasks
- 4 technology-specific agents (Docker, Python 3.14, PHP 8.4, PostgreSQL 18)
- Integration with OpenCode and Claude Code IDEs
- Automated validation and rendering scripts
- Token compression via RTK
- **CrewAI integration** for multi-agent orchestration
- **Coolify deployment** guides and automation scripts

---

## First Steps (start here)

If you are a team member picking up this repository to **build a new project** or
to **modernize/update a legacy one**, follow the onboarding guide first:

**➡️ [`_bmad-output/getting-started.md`](_bmad-output/getting-started.md)**

The pre-flight (do once, in order):

| # | Step | Command |
|---|------|---------|
| 0 | Install the toolchain + both agents | `./_bmad-output/scripts/install-linux.sh --project-dir "$PWD"` |
| 1 | Get the repo + working branch | `git clone … && cd … && git checkout -b feat/setup` |
| 2 | Install/update BMAD | `npx bmad-method install` |
| 3 | Verify toolchain, both agents, RTK | `diff -rq .agents/skills .claude/skills && rtk init --show` |
| 4 | Configure the project | edit `_bmad/custom/config.toml` + `_bmad/config.user.toml` |
| 5 | Open an agent, then orient | `opencode` or `claude` → `/bmad-help` |

Then pick a track:

| Track | When | Where it goes |
|-------|------|---------------|
| **A — New project (greenfield)** | no code yet | `/bmad-help` → 5-phase lifecycle |
| **B — Legacy project (brownfield)** | existing codebase to modernize | `/bmad-project-context` → `/bmad-code-review` → `/bmad-build` |

### Detailed step-by-step (any skill level)

For a fully documented, jargon-free walkthrough of both tracks — concepts,
exact commands, expected inputs/outputs, quality gates, troubleshooting — use the
implementation playbook. It is written for team members **regardless of software
engineering background**:

**➡️ [`_bmad-output/implementation-playbook.md`](_bmad-output/implementation-playbook.md)** — *Manual de Implementação (PT-BR)*

| Guide | Use it for |
|-------|-----------|
| [`getting-started.md`](_bmad-output/getting-started.md) | 5-minute orientation + pre-flight + track selector |
| [`implementation-playbook.md`](_bmad-output/implementation-playbook.md) | **The detailed how-to for a new or legacy project (Parts A & B), glossary, Definition of Done, FAQ** |
| [`bmad-project-lifecycle-guide.md`](_bmad-output/bmad-project-lifecycle-guide.md) | Operator reference: the 5 phases and the daily routine |

---

## Quick Start

### Prerequisites

| Tool | Required Version | Purpose |
|------|-----------------|---------|
| Node.js | >= 20.12 | JavaScript runtime |
| Python | >= 3.10, < 3.14 | Script execution |
| uv | >= 0.12 | Python package management |
| Git | Any | Version control |
| GitHub CLI (`gh`) | Any | Repo / PR / release operations |
| RTK | >= 0.47 | Token compression for both agents (optional) |
| ripgrep | >= 14.0 | Fast search, RTK dependency (recommended) |
| CrewAI | >= 1.15 | Multi-agent orchestration (optional) |
| Coding agent | — | OpenCode >= 1.18 and/or Claude Code >= 2.1 |

> Every tool above is usable from **both** OpenCode and Claude Code. See
> [Coding Agents](#coding-agents).

### Automated Installation

```bash
# Linux (Ubuntu/Debian)
chmod +x _bmad-output/scripts/install-linux.sh
./_bmad-output/scripts/install-linux.sh

# Windows (PowerShell as Administrator)
powershell -ExecutionPolicy Bypass -File _bmad-output/scripts/install-windows.ps1
```

### Manual Installation

```bash
# Install BMAD Method (regenerates both skill trees + OpenCode commands)
npx bmad-method install

# Wire RTK into both coding agents (per machine)
rtk init -g --auto-patch --opencode

# Start either agent — the BMAD commands are identical
opencode        # or: claude

# In either agent
/bmad-help
```

---

## Coding Agents

This project is configured for **two interchangeable coding agents**. Every skill,
command and tool works the same in each.

| Concern | OpenCode | Claude Code |
|---------|----------|-------------|
| Instructions | `AGENTS.md` | `CLAUDE.md` (imports `AGENTS.md`) |
| Skills (57) | `.agents/skills/` + `.opencode/commands/*.md` | `.claude/skills/` (native discovery) |
| Invocation | `/bmad-help`, `/bmad-build`, … | `/bmad-help`, `/bmad-build`, … |
| Tool allow-list | shell `PATH` | `.claude/settings.json` → `permissions.allow` |
| RTK token compression | `~/.config/opencode/plugins/rtk.ts` | `.claude/settings.json` `PreToolUse` hook (`rtk hook claude`) |
| RTK reference | — | `.claude/RTK.md` |

`.agents/skills/` and `.claude/skills/` are kept byte-identical; `npx bmad-method
install` regenerates both. One command wires RTK into both agents on a new
machine: `rtk init -g --auto-patch --opencode`.

---

## Project Structure

```
/home/hsantos/app/
├── .agents/skills/          # 57 BMAD skills (OpenCode)
├── .claude/                 # Claude Code integration
│   ├── skills/              # 57 BMAD skills (byte-identical mirror)
│   ├── settings.json        # tool allow-list + RTK PreToolUse hook
│   └── RTK.md               # RTK command reference for the agent
├── .opencode/commands/      # 57 OpenCode command wrappers
├── .git/                    # Git repository
├── AGENTS.md                # OpenCode instructions
├── CLAUDE.md                # Claude Code instructions (imports AGENTS.md)
├── _bmad/                   # BMAD framework
│   ├── _config/             # Manifests & configs
│   ├── core/                # Core skills
│   ├── bmm/                 # BMM skills
│   ├── scripts/             # Python scripts
│   ├── config.toml          # Main config
│   └── config.user.toml     # User config
├── _bmad-output/            # Implementation artifacts
│   ├── getting-started.md              # First steps / onboarding (new + legacy)
│   ├── implementation-playbook.md      # Detailed step-by-step, any skill level (Parts A & B)
│   ├── bmad-project-lifecycle-guide.md # 5-phase lifecycle, step by step
│   ├── coolify-deploy-guide.md         # Coolify deploy overview
│   ├── coolify-github-deploy-guide.md  # GitHub repo deploy guide
│   ├── coolify-local-deploy-guide.md   # Local deploy guide (no Git)
│   ├── crewai-integration-guide.md     # CrewAI + BMAD integration
│   ├── docker-skill-implementation.md  # Docker agent docs
│   ├── php84-skill-implementation.md   # PHP 8.4 agent docs
│   ├── postgres18-skill-implementation.md  # PostgreSQL 18 docs
│   ├── project-replication-guide.md    # Full setup guide
│   ├── python314-skill-implementation.md   # Python 3.14 docs
│   ├── rtk-installation-guide.md       # RTK setup
│   ├── tools-registry.md              # Tools inventory
│   └── scripts/
│       ├── coolify-deploy.sh           # Coolify deploy automation
│       ├── install-linux.sh            # Linux installation
│       ├── install-windows.ps1         # Windows installation
│       ├── installation-validation-report.md
│       ├── README.md
│       ├── test-local.sh              # Local testing
│       └── windows-script-validation-report.md
├── docs/                    # Project knowledge
└── README.md                # This file
```

---

## BMAD Skills (57 Total)

### Core Skills (24)

| Skill | Purpose |
|-------|---------|
| `bmad-help` | Orient to workflow, get recommendations |
| `bmad-build` | Main code implementation |
| `bmad-build-auto` | Autonomous build loop |
| `bmad-brainstorming` | Ideation and creative exploration |
| `bmad-forge-idea` | Pressure-test ideas |
| `bmad-create-prd` | Product requirements document |
| `bmad-architecture` | System architecture design |
| `bmad-ux` | UX patterns and design specs |
| `bmad-create-epics-and-stories` | Break work into stories |
| `bmad-sprint-planning` | Sprint readiness |
| `bmad-code-review` | Adversarial code review |
| `bmad-retrospective` | Epic retrospective |
| `bmad-docker` | Docker containerization |
| `bmad-python314` | Python 3.14 features |
| `bmad-php84` | PHP 8.4 features |
| `bmad-postgres18` | PostgreSQL 18 features |
| ... | and more |

### Technology Agents (4)

| Agent | Skills | Focus |
|-------|--------|-------|
| `bmad-agent-docker` | 1 | Containerization, Dockerfile, Compose |
| `bmad-agent-python314` | 1 | Free-threading, t-strings, subinterpreters |
| `bmad-agent-php84` | 3 | Arch-PHP, CodeRefactor-PHP, WebSec-PHP |
| `bmad-agent-postgres18` | 5 | DDL, OPT, VEC, CONC, SEC |

---

## BMAD Workflow Phases

1. **Clarify** — `bmad-help`, `bmad-brainstorming`, `bmad-forge-idea`
2. **Plan** — `bmad-create-prd`, `bmad-architecture`, `bmad-ux`, `bmad-create-epics-and-stories`
3. **Build** — `bmad-build`, `bmad-build-auto`
4. **Review** — `bmad-code-review`, `bmad-checkpoint-preview`
5. **Learn** — `bmad-retrospective`

Small changes can skip straight to build. Complex work follows the full path.

---

## CrewAI Integration

**CrewAI is integrated into this project's structure for combined use with the
BMAD Method.** It is not an optional side tool — it is wired in as the
multi-agent **orchestration layer** on top of BMAD's skills:

- Installed as a managed CLI (`uv tool install crewai` → `~/.local/bin/crewai`,
  v1.15.18) and registered in `_bmad-output/tools-registry.md`.
- Reachable from **both** coding agents (OpenCode and Claude Code) — `crewai` is
  on the pre-approved tool list in `.claude/settings.json`.
- Connected to BMAD through the **BMAD-CrewAI bridge** (`BMADBridge`), which lets
  a CrewAI crew list and render BMAD skills as steps in an automated flow.
- Full design, patterns and examples: **`_bmad-output/crewai-integration-guide.md`**.

**How the two fit together:** BMAD provides the *method* (57 skills, the 5-phase
lifecycle, technology agents); CrewAI provides the *automation* (role-based
agents, event-driven flows, human-in-the-loop, checkpointing). Use BMAD skills
interactively for judgement-heavy work, and wrap well-defined, repeatable
sequences of those same skills in a CrewAI flow.

### What is CrewAI?

CrewAI is an open-source Python framework for orchestrating role-playing, autonomous AI agents. It provides:

- **Crews**: Teams of AI agents with roles, goals, tools, and tasks
- **Flows**: Event-driven workflows with state management
- **Production-ready patterns**: Human-in-the-loop, async execution, checkpointing

### Integration Benefits

| BMAD Strength | CrewAI Strength | Combined Benefit |
|---------------|-----------------|------------------|
| Development workflow expertise | Multi-agent orchestration | Automated development pipelines |
| 57 specialized skills | Role-based agent collaboration | Specialized agent teams |
| Technology-specific agents | Event-driven workflows | Complex automation flows |

### Quick Start with CrewAI

```bash
# Install CrewAI (if not already installed)
uv tool install crewai

# Create a new CrewAI project
crewai create crew bmad-project

# Navigate to project and install dependencies
cd bmad-project
crewai install

# Run the crew
crewai run
```

### BMAD-CrewAI Bridge

Use the bridge module to connect BMAD skills with CrewAI agents:

```python
from bmad_crewai_bridge import BMADBridge

# Initialize bridge
bridge = BMADBridge(project_root="/home/hsantos/app")

# List all BMAD skills
skills = bridge.list_skills()

# Render a skill
output = bridge.render_skill("bmad-docker")
```

For detailed integration guide, see `_bmad-output/crewai-integration-guide.md`.

---

## Coolify Deployment

Self-hosted PaaS deployment using **Coolify v4.3.14**. Deploy applications via Git repositories or locally without Git.

### Deployment Methods

| Method | Source | Auth | Best For |
|--------|--------|------|----------|
| **Public Repository** | Git HTTPS URL | None | Open source projects |
| **Deploy Key** | Git SSH URL | SSH key | Single private repo |
| **GitHub App** | Git (multi-repo) | OAuth + Webhook | Teams, multiple repos |
| **Docker Image** | Registry (Docker Hub/GHCR) | None/Token | Pre-built images |
| **Dockerfile** | Pasted in Coolify UI | None | Simple apps without Git |
| **Docker Compose Empty** | Pasted in Coolify UI | None | Multi-service stacks |
| **Service One-Click** | Coolify templates | None | Popular apps (300+) |

### Quick Deploy via CLI

```bash
# Install Coolify CLI
curl -fsSL https://raw.githubusercontent.com/coollabsio/coolify-cli/main/scripts/install.sh | bash

# Configure context
coolify context add -d production https://coolify.seudominio.com <TOKEN>

# Deploy from public Git repo
./_bmad-output/scripts/coolify-deploy.sh \
  --name my-app \
  --repo https://github.com/user/repo \
  --port 3000

# Deploy Docker image
./_bmad-output/scripts/coolify-deploy.sh \
  --name nginx \
  --docker-image nginx:alpine \
  --port 80
```

### Guides

- **Overview**: `_bmad-output/coolify-deploy-guide.md` (12 sections, 26K)
- **GitHub repos**: `_bmad-output/coolify-github-deploy-guide.md` (9 sections, 18.5K)
- **Local deploy**: `_bmad-output/coolify-local-deploy-guide.md` (10 sections, 18.8K)

---

## Technology Stack

### Docker Agent & Skill

- **Dockerfile validation**: 15 rules (D001-D015)
- **Compose validation**: 7 rules (C001-C007)
- **BuildKit optimization**: Multi-stage builds
- **Security hardening**: Non-root users, read-only filesystem
- **Documentation sync**: Automated updates

### Python 3.14 Agent & Skill

- **Free-threading**: No-GIL mode for true parallelism
- **Subinterpreters**: Isolated execution environments
- **t-strings**: Type-safe string interpolation
- **compression.zstd**: Built-in Zstandard support
- **Deferred annotations**: Runtime type resolution

### PHP 8.4 Agent & Skill

- **Property Hooks**: Get/set hooks replacing boilerplate
- **Asymmetric Visibility**: `public private(set)` patterns
- **DOM API**: HTML5 native parsing
- **Array Functions**: `array_find`, `array_any`, `array_all`
- **Expression Syntax**: `new Foo()->bar()` without parentheses

### PostgreSQL 18 Agent & Skill

- **AIO**: `io_method = io_uring` for 3x performance
- **B-Tree Skip Scan**: Multi-column index optimization
- **UUIDv7**: Ordered primary keys
- **Virtual Generated Columns**: Default in PG18
- **RETURNING OLD/NEW**: Direct delta extraction
- **pgvector**: HNSW indexing, hybrid search

---

## Installation Scripts

| Script | OS | Usage |
|--------|-----|-------|
| `install-linux.sh` | Ubuntu/Debian | `./install-linux.sh --project-dir /path` |
| `install-windows.ps1` | Windows 10/11 | `powershell -ExecutionPolicy Bypass -File install-windows.ps1` |

See `_bmad-output/scripts/README.md` for detailed instructions.

---

## Project Materials & Tools (Index)

Every document, script, config file and tool in this repository, with **what it
is** and **when to use it** — so any team member can locate study and reference
material quickly. The authoritative, detailed machine inventory (versions, paths,
install log) is **`_bmad-output/tools-registry.md`** (v1.3.3).

### 1. Start-here guides (read in this order)

| # | Document | What it is | Read it when |
|---|----------|-----------|--------------|
| 1 | `_bmad-output/getting-started.md` | 5-minute onboarding: the Steps 0–5 pre-flight (toolchain, both agents, RTK, project config) + Track A/B selector. | You just cloned the repo and need to get productive. |
| 2 | `_bmad-output/implementation-playbook.md` | **Manual de Implementação (PT-BR)** — the detailed, jargon-free walkthrough: glossary, 6 principles, **Part A (new project / greenfield)** and **Part B (legacy modernization / brownfield)** step by step, Definition of Done, decision table, FAQ. Written for **any skill level**. | You are actually building — new system or modernizing an existing one. |
| 3 | `_bmad-output/bmad-project-lifecycle-guide.md` | Operator reference: the 5 phases (Clarify → Plan → Build → Review → Learn), per-phase checklists, the daily routine, command cheat-sheet, golden rules. | You know the flow and want a quick operational reference. |
| 4 | `_bmad-output/project-replication-guide.md` (v1.1.0) | How to reproduce the full environment on a **new machine**: hardware/OS requirements, per-tool install, IDE setup, validation script, troubleshooting. | Setting up a second machine or a new team member's box. |

### 2. Integration & tooling guides

| Document | What it is | Read it when |
|----------|-----------|--------------|
| `_bmad-output/crewai-integration-guide.md` | How **CrewAI** is wired into the project for combined use with BMAD — the `BMADBridge`, crews/flows, human-in-the-loop, worked examples. | Automating repeatable sequences of BMAD skills. |
| `_bmad-output/rtk-installation-guide.md` | **RTK** (token compression) full report: install, the OpenCode plugin **and** the Claude Code `PreToolUse` hook, architecture diagrams, command reference, troubleshooting. | Verifying / fixing RTK, or understanding what it does. |
| `_bmad-output/tools-registry.md` | **Canonical inventory** — every runtime, framework, agent, script and integration with version, path, "used by", directory map and dated install log. | You need the exact version/path of something, or a change history. |

### 3. Technology agent references

| Document | What it is |
|----------|-----------|
| `_bmad-output/docker-skill-implementation.md` | Docker Agent & Skill: Dockerfile/Compose validation rules (D001–D015, C001–C007), BuildKit, security hardening, doc-sync. |
| `_bmad-output/python314-skill-implementation.md` | Python 3.14 Agent & Skill: free-threading, subinterpreters, t-strings, `compression.zstd`, deferred annotations. |
| `_bmad-output/php84-skill-implementation.md` | PHP 8.4 Agent & Skill: Property Hooks, Asymmetric Visibility, DOM API, new array functions. |
| `_bmad-output/postgres18-skill-implementation.md` | PostgreSQL 18 Agent & Skill: AIO (`io_uring`), B-Tree Skip Scan, UUIDv7, `RETURNING OLD/NEW`, pgvector. |

### 4. Deployment (Coolify)

| Document | What it is |
|----------|-----------|
| `_bmad-output/coolify-deploy-guide.md` | Overview + preparation + CLI + step-by-step (12 sections). Start here for deployment. |
| `_bmad-output/coolify-github-deploy-guide.md` | GitHub sources: public repo, Deploy Key, GitHub App (9 sections). |
| `_bmad-output/coolify-local-deploy-guide.md` | No-Git sources: Docker Image, pasted Dockerfile, Compose Empty, one-click Service (10 sections). |
| `_bmad-output/scripts/coolify-deploy.sh` | Executable — automated Coolify deploy via CLI (public + private repos, Docker image). |

### 5. Installation scripts & validation

| File | What it is |
|------|-----------|
| `_bmad-output/scripts/install-linux.sh` (v1.1.0) | One-shot Linux/Ubuntu setup: toolchain + both agents + `npx bmad-method install` + RTK wired into both agents + parity checks. |
| `_bmad-output/scripts/install-windows.ps1` (v1.1.0) | The same for Windows 10/11 (PowerShell as Administrator). |
| `_bmad-output/scripts/README.md` | How to run the install scripts, post-install steps, troubleshooting, uninstall. |
| `_bmad-output/scripts/test-local.sh` | Local dry-run/validation of the installation flow. |
| `_bmad-output/scripts/installation-validation-report.md` | Environment validation results. |
| `_bmad-output/scripts/windows-script-validation-report.md` | 73 test cases exercised against the Windows script. |

### 6. Agent instructions & configuration

| File | What it is |
|------|-----------|
| `AGENTS.md` | Project contract read by **OpenCode**: setup, coding-agent parity, skills, onboarding, prerequisites. |
| `CLAUDE.md` | Entry point read by **Claude Code** — imports `AGENTS.md` + Claude-specific notes. |
| `.claude/settings.json` | Claude Code tool allow-list (`uv`, `rtk`, `rg`, `gh`, `crewai`, `npx bmad-method`) + RTK `PreToolUse` hook. |
| `.claude/RTK.md` | RTK command reference surfaced to Claude Code. |
| `.opencode/commands/*.md` | 57 OpenCode command wrappers (`/bmad-*`) pointing at `.agents/skills/`. |
| `_bmad/config.toml` | Installer-managed base config (project name, output folder, agent descriptors). **Do not edit.** |
| `_bmad/config.user.toml` | Your personal install answers (name, language, skill level). Gitignored. |
| `_bmad/custom/config.toml` | Team overrides, committed — the place to pin project settings. |
| `_bmad/_config/manifest.yaml` | Installation metadata (modules, IDE targets, versions). |

### 7. BMAD engine scripts (`_bmad/scripts/`)

| Script | What it does |
|--------|--------------|
| `render_skill.py` | Renders a skill's workflow to a runnable snapshot. The **only** supported way to run a skill: `uv run _bmad/scripts/render_skill.py --project-root "$PWD" --skill .claude/skills/<name>` (or `.agents/skills/<name>`). |
| `validate_dockerfile.py` | Validates Dockerfiles against 15 rules (D001–D015). |
| `validate_compose.py` | Validates `docker-compose` files against 7 rules (C001–C007). |
| `docsync_docker.py` | Keeps Docker documentation in sync. |
| `memlog.py` | Memory-logging utility for skill runs. |
| `config_utils.py` / `resolve_config.py` / `resolve_customization.py` | Config resolution helpers used by the skills. |

### 8. Installed tools

| Tool | Version | Path | Purpose | Learn more |
|------|---------|------|---------|------------|
| **Node.js** | v24.20.0 | nvm | JS runtime; runs `npx bmad-method`, OpenCode | `project-replication-guide.md` |
| **npm** | 12.0.2 | with Node | Package manager | — |
| **Python** | 3.12.3 | system | Runs BMAD scripts & skill rendering (needs `>=3.10,<3.14`) | `project-replication-guide.md` |
| **uv** | 0.12.9 | `~/.local/bin/uv` | Fast Python runner — `uv run` renders skills; `uv tool install` | `tools-registry.md` §1.4 |
| **Git** | 2.43.0 | system | Version control | — |
| **GitHub CLI (`gh`)** | 2.73.0 | `~/.local/bin/gh` | Repo / PR / release ops; `gh auth setup-git` for push | `tools-registry.md` §1.7 |
| **ripgrep (`rg`)** | 14.1.1 | `~/.local/bin/rg` | Fast search; RTK dependency | `rtk-installation-guide.md` |
| **RTK** | 0.47.0 | `~/.local/bin/rtk` | Token compression proxy — active in **both** agents (OpenCode plugin + Claude `PreToolUse` hook). `RTK_DISABLED=1 <cmd>` for raw output. | `rtk-installation-guide.md` |
| **CrewAI** | 1.15.18 | `~/.local/bin/crewai` | Multi-agent orchestration integrated with BMAD via `BMADBridge` | `crewai-integration-guide.md` |
| **OpenCode** | 1.18.27 | `~/.opencode/bin/opencode` | Coding agent — reads `AGENTS.md`, `.opencode/commands/`, `.agents/skills/` | `AGENTS.md` |
| **Claude Code** | 2.1.260 | `~/.local/bin/claude` | Coding agent — reads `CLAUDE.md`, `.claude/settings.json`, `.claude/skills/` | `CLAUDE.md` |
| **BMAD Method** | 6.11.0 | `_bmad/` | The framework — 57 skills, 5-phase lifecycle, technology agents | `AGENTS.md`, `tools-registry.md` §2 |

### 9. "I want to… → read this"

| Goal | Start with |
|------|-----------|
| Get onboarded | `getting-started.md` |
| Build a **new** project end-to-end | `implementation-playbook.md` → Part A |
| Modernize / update a **legacy** project | `implementation-playbook.md` → Part B |
| Quick operational reference for the 5 phases | `bmad-project-lifecycle-guide.md` |
| Set up a new machine | `project-replication-guide.md` + `scripts/install-*.sh` |
| Automate repeated skill sequences | `crewai-integration-guide.md` |
| Understand / fix token compression | `rtk-installation-guide.md` |
| Deploy to production | `coolify-deploy-guide.md` (+ github / local variants) |
| Look up an exact version, path or change | `tools-registry.md` |
| Work on Docker / Python 3.14 / PHP 8.4 / PostgreSQL 18 | the matching `*-skill-implementation.md` + `/bmad-agent-*` |
| Translated overview | `README.pt-BR.md` · `README.es.md` |

---

## Usage Examples

### Start a New Project

```bash
# Clone the repository
git clone https://github.com/your-org/your-repo.git
cd your-repo

# Run installation script (installs both agents + wires RTK into both)
chmod +x _bmad-output/scripts/install-linux.sh
./_bmad-output/scripts/install-linux.sh

# Start either coding agent
opencode        # or: claude

# In either agent
/bmad-help
```

### Complete Project Lifecycle (Recommended)

For new projects, follow the **5-phase lifecycle** documented in the project lifecycle guide:

| Phase | Skills | Duration | Output |
|-------|--------|----------|--------|
| **1. Clarify** | `bmad-help` → `bmad-brainstorming` → `bmad-forge-idea` | 30 min | Validated idea |
| **2. Plan** | `bmad-create-prd` → `bmad-architecture` → `bmad-ux` → `bmad-create-epics-and-stories` | 1-2h | PRD + Architecture + UX + Stories |
| **3. Build** | `bmad-build` (per story) | Variable | Working code |
| **4. Review** | `bmad-code-review` → `bmad-qa-generate-e2e-tests` | 30 min | Validated code |
| **5. Learn** | `bmad-retrospective` → Deploy to Coolify | 30 min | Lessons learned + Production |

**📖 Full guide:** `_bmad-output/bmad-project-lifecycle-guide.md`

### Quick Reference: All Phases

```
/bmad-help              → Start here, get oriented
/bmad-brainstorming     → Structured ideation session
/bmad-forge-idea        → Pressure-test your idea
/bmad-create-prd        → Create Product Requirements Document
/bmad-architecture      → Define architecture spine
/bmad-ux                → Create DESIGN.md + EXPERIENCE.md
/bmad-create-epics-and-stories → Break work into trackable stories
/bmad-sprint-planning   → Plan sprint execution
/bmad-build             → Implement code (one story at a time)
/bmad-build-auto        → Autonomous build loop
/bmad-code-review       → Adversarial code review
/bmad-retrospective     → Epic retrospective with evidence
```

### Use Technology Agents

```
# Docker tasks
/bmad-docker
/bmad-agent-docker

# Python 3.14 tasks
/bmad-python314
/bmad-agent-python314

# PHP 8.4 tasks
/bmad-php84
/bmad-agent-php84

# PostgreSQL 18 tasks
/bmad-postgres18
/bmad-agent-postgres18
```

### Render a Skill

```bash
# Claude Code
uv run _bmad/scripts/render_skill.py \
  --project-root /home/hsantos/app \
  --skill .claude/skills/bmad-docker

# OpenCode
uv run _bmad/scripts/render_skill.py \
  --project-root /home/hsantos/app \
  --skill .agents/skills/bmad-docker
```

---

## Configuration

### Main Config

`_bmad/config.toml` — Managed by installer, do not edit directly.

### Team Config

`_bmad/custom/config.toml` — Team overrides, committed to repo.

### User Config

`_bmad/config.user.toml` — Personal settings, gitignored.

### Coding Agent Config

| File | Agent | Committed | Purpose |
|------|-------|-----------|---------|
| `AGENTS.md` | OpenCode | ✅ | Project instructions |
| `CLAUDE.md` | Claude Code | ✅ | Entry point; imports `AGENTS.md` |
| `.claude/settings.json` | Claude Code | ✅ | Tool allow-list + RTK `PreToolUse` hook |
| `.claude/RTK.md` | Claude Code | ✅ | RTK command reference |
| `~/.config/opencode/plugins/rtk.ts` | OpenCode | machine-local | RTK plugin |

---

## Updating

```bash
# Update BMAD Method
npx bmad-method install

# Update tools
npm update -g opencode @anthropic-ai/claude-code
```

---

## Support

- **Documentation**: See `_bmad-output/` for detailed guides — start with the
  [Project Materials & Tools index](#project-materials--tools-index)
- **Issues**: Open an issue on the project repository
- **BMAD Method**: https://github.com/bmadmethod/bmad-method — the framework
  (57 skills, 5-phase lifecycle, technology agents); installed at `_bmad/`,
  updated with `npx bmad-method install`
- **CrewAI**: https://github.com/crewAIInc/crewAI · docs https://docs.crewai.com
  — the multi-agent orchestration layer **integrated with BMAD** in this project
  (v1.15.18 at `~/.local/bin/crewai`, connected via the `BMADBridge`); see
  [`_bmad-output/crewai-integration-guide.md`](_bmad-output/crewai-integration-guide.md)

---

## License

MIT License — See `_bmad/core/config.yaml` for details.

---

## Contributors

- **Hsantos** — Project maintainer
- **BMAD Method** — Framework authors
