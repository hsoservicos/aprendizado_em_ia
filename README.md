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

## Quick Start

### Prerequisites

| Tool | Required Version | Purpose |
|------|-----------------|---------|
| Node.js | >= 20.12 | JavaScript runtime |
| Python | >= 3.10, < 3.14 | Script execution |
| uv | >= 0.12 | Python package management |
| Git | Any | Version control |
| RTK | >= 0.47 | Token compression (optional) |
| ripgrep | >= 14.0 | Fast search (recommended) |
| CrewAI | >= 1.15 | Multi-agent orchestration (optional) |

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
# Install BMAD Method
npx bmad-method install

# Start OpenCode
opencode

# In OpenCode, use BMAD commands
/bmad-help
```

---

## Project Structure

```
/home/hsantos/app/
├── .agents/skills/          # 57 BMAD skills
├── .claude/skills/          # 57 BMAD skills (mirror)
├── .opencode/commands/      # 57 OpenCode commands
├── .git/                    # Git repository
├── _bmad/                   # BMAD framework
│   ├── _config/             # Manifests & configs
│   ├── core/                # Core skills
│   ├── bmm/                 # BMM skills
│   ├── scripts/             # Python scripts
│   ├── config.toml          # Main config
│   └── config.user.toml     # User config
├── _bmad-output/            # Implementation artifacts
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
├── AGENTS.md                # Project instructions
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

This project includes **CrewAI** for multi-agent orchestration, enabling automated development workflows.

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

## Documentation

### Core Documentation

| Document | Location | Description |
|----------|----------|-------------|
| **Project Lifecycle Guide** | `_bmad-output/bmad-project-lifecycle-guide.md` | **Complete step-by-step: 5 phases from idea to production** |
| **README (Português)** | `README.pt-BR.md` | Documentação em Português do Brasil |
| **README (Español)** | `README.es.md` | Documentación en Español |
| AGENTS.md | `/AGENTS.md` | Project instructions |
| Tools Registry | `_bmad-output/tools-registry.md` | Tools inventory (v1.2.0) |
| Replication Guide | `_bmad-output/project-replication-guide.md` | Full setup guide |
| CrewAI Integration | `_bmad-output/crewai-integration-guide.md` | CrewAI + BMAD integration |

### Technology Agents

| Document | Location | Description |
|----------|----------|-------------|
| Docker Implementation | `_bmad-output/docker-skill-implementation.md` | Docker agent docs |
| Python 3.14 Implementation | `_bmad-output/python314-skill-implementation.md` | Python 3.14 docs |
| PHP 8.4 Implementation | `_bmad-output/php84-skill-implementation.md` | PHP 8.4 docs |
| PostgreSQL 18 Implementation | `_bmad-output/postgres18-skill-implementation.md` | PostgreSQL 18 docs |
| RTK Installation | `_bmad-output/rtk-installation-guide.md` | RTK setup |

### Coolify Deployment

| Document | Location | Description |
|----------|----------|-------------|
| Coolify Deploy Guide | `_bmad-output/coolify-deploy-guide.md` | Overview, preparation, CLI, step-by-step (12 sections) |
| GitHub Deploy Guide | `_bmad-output/coolify-github-deploy-guide.md` | Public repo, Deploy Key, GitHub App (9 sections) |
| Local Deploy Guide | `_bmad-output/coolify-local-deploy-guide.md` | Docker Image, Dockerfile, Compose Empty, Service (10 sections) |
| Deploy Script | `_bmad-output/scripts/coolify-deploy.sh` | Automatizado CLI (Git + Docker Image) |

### Installation & Validation

| Document | Location | Description |
|----------|----------|-------------|
| Linux Installation | `_bmad-output/scripts/install-linux.sh` | Automated Linux setup |
| Windows Installation | `_bmad-output/scripts/install-windows.ps1` | Automated Windows setup |
| Windows Validation | `_bmad-output/scripts/windows-script-validation-report.md` | 73 test cases for Windows script |
| Installation Validation | `_bmad-output/scripts/installation-validation-report.md` | Environment validation |
| Local Test | `_bmad-output/scripts/test-local.sh` | Local installation testing |

---

## Usage Examples

### Start a New Project

```bash
# Clone the repository
git clone https://github.com/your-org/your-repo.git
cd your-repo

# Run installation script
chmod +x _bmad-output/scripts/install-linux.sh
./_bmad-output/scripts/install-linux.sh

# Start OpenCode
opencode

# In OpenCode
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

- **Documentation**: See `_bmad-output/` for detailed guides
- **Issues**: Open an issue on the project repository
- **BMAD Method**: https://github.com/bmadmethod/bmad-method

---

## License

MIT License — See `_bmad/core/config.yaml` for details.

---

## Contributors

- **Hsantos** — Project maintainer
- **BMAD Method** — Framework authors
