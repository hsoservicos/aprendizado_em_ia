# BMAD Method — Agile AI-Driven Development

![Version](https://img.shields.io/badge/version-6.11.0-blue)
![Skills](https://img.shields.io/badge/skills-57-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

---

## Overview

BMAD Method (Breakthrough Method for Agile Development) is an AI-powered development framework that integrates specialized agents and skills into your development workflow. This project provides a complete environment for agile software development using AI assistants.

**Key Features:**
- 57 specialized skills for different development tasks
- 4 technology-specific agents (Docker, Python 3.14, PHP 8.4, PostgreSQL 18)
- Integration with OpenCode and Claude Code IDEs
- Automated validation and rendering scripts
- Token compression via RTK

---

## Quick Start

### Prerequisites

| Tool | Required Version | Purpose |
|------|-----------------|---------|
| Node.js | >= 20.12 | JavaScript runtime |
| Python | >= 3.10 | Script execution |
| uv | >= 0.12 | Python package management |
| Git | Any | Version control |
| RTK | >= 0.47 | Token compression (optional) |
| ripgrep | >= 14.0 | Fast search (recommended) |

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
│   ├── scripts/             # Installation scripts
│   └── *.md                 # Documentation
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

| Document | Location | Description |
|----------|----------|-------------|
| AGENTS.md | `/AGENTS.md` | Project instructions |
| Tools Registry | `_bmad-output/tools-registry.md` | Tools inventory |
| Replication Guide | `_bmad-output/project-replication-guide.md` | Full setup guide |
| Docker Implementation | `_bmad-output/docker-skill-implementation.md` | Docker docs |
| Python 3.14 Implementation | `_bmad-output/python314-skill-implementation.md` | Python docs |
| PHP 8.4 Implementation | `_bmad-output/php84-skill-implementation.md` | PHP docs |
| PostgreSQL 18 Implementation | `_bmad-output/postgres18-skill-implementation.md` | Postgres docs |
| RTK Installation | `_bmad-output/rtk-installation-guide.md` | RTK setup |

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
