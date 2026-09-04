# Tools Registry — Inventário de Ferramentas do Projeto

**Last Updated**: 2026-09-04T01:30:00Z  
**Maintainer**: Hsantos  
**Version**: 1.2.0

---

## Overview

Este artefato rastrea todas as ferramentas, dependências e recursos instalados no projeto `/home/hsantos/app`. Deve ser atualizado sempre que uma nova ferramenta for instalada, implementada ou interagida.

---

## 1. Runtime Environment

### 1.1 Node.js Runtime

| Property | Value |
|----------|-------|
| **Name** | Node.js |
| **Version** | v24.20.0 |
| **Path** | System PATH |
| **Purpose** | JavaScript runtime, package management, BMAD installer |
| **Installed** | Pre-existing |
| **Used By** | BMAD Method, npm packages, OpenCode |

### 1.2 npm (Node Package Manager)

| Property | Value |
|----------|-------|
| **Name** | npm |
| **Version** | 12.0.2 |
| **Path** | System PATH |
| **Purpose** | Package management, script execution |
| **Installed** | With Node.js |
| **Used By** | BMAD Method, `npx bmad-method install` |

### 1.3 Python Runtime

| Property | Value |
|----------|-------|
| **Name** | Python |
| **Version** | 3.12.3 |
| **Path** | System PATH |
| **Purpose** | Script execution, BMAD skill rendering |
| **Installed** | System |
| **Used By** | BMAD scripts (`render_skill.py`, validators) |

### 1.4 uv (Python Package Manager)

| Property | Value |
|----------|-------|
| **Name** | uv |
| **Version** | 0.12.9 |
| **Path** | `~/.local/bin/uv` |
| **Purpose** | Fast Python package installation, script execution |
| **Installed** | Manual |
| **Used By** | BMAD skill rendering (`uv run`) |
| **Status** | ✅ Active |

### 1.5 Git

| Property | Value |
|----------|-------|
| **Name** | Git |
| **Version** | 2.43.0 |
| **Path** | System PATH |
| **Purpose** | Version control, repository management |
| **Installed** | System |
| **Used By** | All version control operations |

### 1.6 CrewAI

| Property | Value |
|----------|-------|
| **Name** | CrewAI |
| **Version** | 1.15.18 |
| **Path** | `~/.local/bin/crewai` |
| **Purpose** | Multi-agent orchestration framework |
| **Installed** | 2026-09-03 via `uv tool install crewai` |
| **Used By** | BMAD-CrewAI integration, automated workflows |
| **Status** | ✅ Active |
| **Python** | >= 3.10, < 3.14 |
| **Dependencies** | 134 packages (auto-installed) |

---

## 2. BMAD Method Framework

### 2.1 BMAD Core

| Property | Value |
|----------|-------|
| **Name** | BMAD Method |
| **Version** | 6.11.0 |
| **Install Date** | 2026-09-02T13:16:32.974Z |
| **Modules** | `core` (6.11.0), `bmm` (6.11.0) |
| **IDEs** | opencode, claude-code |
| **Config** | `_bmad/config.toml`, `_bmad/config.user.toml` |
| **Manifest** | `_bmad/_config/manifest.yaml` |
| **Status** | ✅ Active |

### 2.2 BMAD Skills (57 Total)

| Category | Count | Location |
|----------|-------|----------|
| **Core Skills** | 24 | `_bmad/core/` |
| **BMM Skills** | 25 | `_bmad/bmm/` |
| **Custom Skills** | 8 | `.agents/skills/`, `.claude/skills/` |
| **Total** | 57 | `.agents/skills/`, `.claude/skills/` |

#### Custom Skills Created (Technology Agents)

| Skill | Agent | Features |
|-------|-------|----------|
| `bmad-docker` | `bmad-agent-docker` | Dockerfile, Compose, BuildKit, security |
| `bmad-python314` | `bmad-agent-python314` | Free-threading, t-strings, subinterpreters |
| `bmad-php84` | `bmad-agent-php84` | Property Hooks, Asymmetric Visibility, DOM API |
| `bmad-postgres18` | `bmad-agent-postgres18` | AIO, Skip Scan, UUIDv7, pgvector |

### 2.3 BMAD Scripts

| Script | Purpose | Size |
|--------|---------|------|
| `render_skill.py` | Render skill markdown to snapshot | 15.2K |
| `validate_dockerfile.py` | Validate Dockerfiles (15 rules) | 15.4K |
| `validate_compose.py` | Validate docker-compose (7 rules) | 13.6K |
| `docsync_docker.py` | Sync Docker documentation | 12.0K |
| `memlog.py` | Memory logging utility | 9.0K |
| `config_utils.py` | Configuration utilities | 4.1K |
| `resolve_config.py` | Config resolution | 1.9K |
| `resolve_customization.py` | Customization resolution | 2.7K |

### 2.4 BMAD Configurations

| File | Purpose |
|------|---------|
| `_bmad/_config/skill-manifest.csv` | All registered skills (57 entries) |
| `_bmad/_config/files-manifest.csv` | File tracking (36.6K) |
| `_bmad/_config/bmad-help.csv` | Help system data |
| `_bmad/_config/manifest.yaml` | Installation metadata |

---

## 3. OpenCode IDE Integration

### 3.1 OpenCode Commands (57 Total)

| Category | Count |
|----------|-------|
| **Core Commands** | 49 |
| **Custom Commands** | 8 |
| **Total** | 57 |

#### Custom Commands Created

| Command | File | Purpose |
|---------|------|---------|
| `bmad-docker` | `.opencode/commands/bmad-docker.md` | Docker skill |
| `bmad-agent-docker` | `.opencode/commands/bmad-agent-docker.md` | Docker agent |
| `bmad-python314` | `.opencode/commands/bmad-python314.md` | Python 3.14 skill |
| `bmad-agent-python314` | `.opencode/commands/bmad-agent-python314.md` | Python 3.14 agent |
| `bmad-php84` | `.opencode/commands/bmad-php84.md` | PHP 8.4 skill |
| `bmad-agent-php84` | `.opencode/commands/bmad-agent-php84.md` | PHP 8.4 agent |
| `bmad-postgres18` | `.opencode/commands/bmad-postgres18.md` | PostgreSQL 18 skill |
| `bmad-agent-postgres18` | `.opencode/commands/bmad-agent-postgres18.md` | PostgreSQL 18 agent |

---

## 4. RTK (Rust Token Killer)

### 4.1 RTK Binary

| Property | Value |
|----------|-------|
| **Name** | RTK |
| **Version** | 0.47.0 |
| **Path** | `~/.local/bin/rtk` |
| **Purpose** | CLI proxy for token compression (60-90% savings) |
| **Platform** | Ubuntu 24.04.4 LTS (x86_64) |
| **Status** | ✅ Active |

### 4.2 RTK Dependencies

| Dependency | Version | Path |
|------------|---------|------|
| ripgrep (`rg`) | 14.1.1 | `~/.local/bin/rg` |

### 4.3 RTK Integration

| Component | Location |
|-----------|----------|
| **OpenCode Plugin** | `~/.config/opencode/plugins/rtk.ts` |
| **Global Config** | `~/.config/rtk/config.toml` |
| **Project Filters** | `<project-root>/.rtk/filters.toml` |
| **Tee Logs** | `~/.local/share/rtk/tee/` |

### 4.4 RTK Commands Reference

| Command | Description | Token Savings |
|---------|-------------|---------------|
| `rtk ls [dir]` | Compact directory tree | ~70-85% |
| `rtk read <file>` | Smart file reading | ~50-80% |
| `rtk find "<pattern>"` | Concise file search | ~75% |
| `rtk grep "<pattern>"` | Grouped search results | ~70-90% |
| `rtk git status` | Condensed git status | ~60% |
| `rtk git log -n <N>` | Compact commit log | ~70% |
| `rtk git diff` | Focused diff output | ~80-85% |
| `rtk gain` | Token savings dashboard | — |

---

## 5. Output Artifacts

### 5.1 Implementation Documentation

| File | Size | Description |
|------|------|-------------|
| `docker-skill-implementation.md` | 7.1K | Docker Agent & Skill docs |
| `python314-skill-implementation.md` | 5.5K | Python 3.14 Agent & Skill docs |
| `php84-skill-implementation.md` | 3.8K | PHP 8.4 Agent & Skill docs |
| `postgres18-skill-implementation.md` | 3.8K | PostgreSQL 18 Agent & Skill docs |
| `rtk-installation-guide.md` | 7.1K | RTK installation & config docs |
| `coolify-deploy-guide.md` | 26.0K | Coolify deploy guide (12 sections) |
| `coolify-github-deploy-guide.md` | 18.5K | GitHub repo types: public, deploy-key, github-app |
| `coolify-local-deploy-guide.md` | 18.8K | Local deploy: Docker Image, Dockerfile, Compose Empty, Service |

### 5.2 Deployment Scripts

| File | Executable | Description |
|------|------------|-------------|
| `scripts/coolify-deploy.sh` | ✅ | Coolify deploy automation (public + private repos) |

### 5.3 Project Documentation

| File | Purpose |
|------|---------|
| `AGENTS.md` | Project instructions, skills, workflow |

---

## 6. Directory Structure

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
│   ├── scripts/             # Python scripts (8 files)
│   ├── config.toml          # Main config
│   └── config.user.toml     # User config
├── _bmad-output/            # Implementation artifacts
│   ├── coolify-deploy-guide.md      # Coolify deploy guide
│   ├── coolify-github-deploy-guide.md  # GitHub repo deploy guide
│   ├── coolify-local-deploy-guide.md   # Local deploy guide (no Git)
│   ├── crewai-integration-guide.md
│   ├── docker-skill-implementation.md
│   ├── php84-skill-implementation.md
│   ├── postgres18-skill-implementation.md
│   ├── project-replication-guide.md
│   ├── python314-skill-implementation.md
│   ├── rtk-installation-guide.md
│   ├── tools-registry.md
│   └── scripts/
│       ├── coolify-deploy.sh     # Deploy automation script
│       ├── install-linux.sh
│       ├── install-windows.ps1
│       ├── installation-validation-report.md
│       ├── README.md
│       ├── test-local.sh
│       └── windows-script-validation-report.md
├── AGENTS.md                # Project instructions
└── docs/                    # Project knowledge (empty)
```

---

## 7. Installation Log

| Date | Tool | Action | By |
|------|------|--------|-----|
| 2026-09-02 | BMAD Method v6.11.0 | Initial install | Hsantos |
| 2026-09-02 | Node.js v24.20.0 | Pre-existing | — |
| 2026-09-02 | Python 3.12.3 | Pre-existing | — |
| 2026-09-02 | Git 2.43.0 | Pre-existing | — |
| 2026-09-02 | uv 0.12.9 | Pre-existing | — |
| 2026-09-02 | RTK 0.47.0 | Pre-existing | — |
| 2026-09-02 | ripgrep 14.1.1 | Installed | Hsantos |
| 2026-09-03 | bmad-docker | Created | Hsantos |
| 2026-09-03 | bmad-agent-docker | Created | Hsantos |
| 2026-09-03 | bmad-python314 | Created | Hsantos |
| 2026-09-03 | bmad-agent-python314 | Created | Hsantos |
| 2026-09-03 | bmad-php84 | Created | Hsantos |
| 2026-09-03 | bmad-agent-php84 | Created | Hsantos |
| 2026-09-03 | bmad-postgres18 | Created | Hsantos |
| 2026-09-03 | bmad-agent-postgres18 | Created | Hsantos |
| 2026-09-03 | CrewAI v1.15.18 | Installed via uv | Hsantos |
| 2026-09-03 | coolify-deploy-guide.md | Created (26K) | Hsantos |
| 2026-09-04 | coolify-github-deploy-guide.md | Created (18.5K) | Hsantos |
| 2026-09-04 | coolify-deploy.sh | Updated (private repos) | Hsantos |
| 2026-09-04 | coolify-local-deploy-guide.md | Created (18.8K) | Hsantos |

---

## 8. Update Protocol

### When to Update This Registry

1. **New Tool Installation** — Add entry to appropriate section
2. **Version Upgrade** — Update version and date
3. **New Skill/Agent Creation** — Add to Skills section
4. **Configuration Change** — Update config files section
5. **Deprecation** — Mark as deprecated with date

### Update Checklist

- [ ] Add entry to Installation Log
- [ ] Update relevant section table
- [ ] Increment version if major change
- [ ] Update `Last Updated` timestamp
- [ ] Commit with descriptive message

---

## 9. Installation Scripts

| Script | OS | Purpose |
|--------|-----|---------|
| `_bmad-output/scripts/install-linux.sh` | Ubuntu/Debian | Automated installation for Linux |
| `_bmad-output/scripts/install-windows.ps1` | Windows 10/11 | Automated installation for Windows |
| `_bmad-output/scripts/README.md` | All | Documentation for scripts |

### Usage

```bash
# Linux
chmod +x _bmad-output/scripts/install-linux.sh
./_bmad-output/scripts/install-linux.sh --project-dir /path/to/project

# Windows (PowerShell as Administrator)
powershell -ExecutionPolicy Bypass -File _bmad-output/scripts/install-windows.ps1 -ProjectDir "C:\projects\myapp"
```

---

## 10. Team Usage

### Quick Reference

```bash
# Check all installed tools
node --version && python3 --version && uv --version && git --version && rtk --version && crewai --version

# List all BMAD skills
rtk ls .agents/skills/

# List all OpenCode commands
rtk ls .opencode/commands/

# Check RTK savings
rtk gain

# Render a skill
uv run _bmad/scripts/render_skill.py --project-root /home/hsantos/app --skill .agents/skills/<skill-name>

# Install/update BMAD
npx bmad-method install

# CrewAI commands
crewai --version
crewai create crew <project-name>
crewai run
```

### Prerequisites

| Tool | Required Version | Status |
|------|-----------------|--------|
| Node.js | >= 20.12 | ✅ v24.20.0 |
| Python | >= 3.10, < 3.14 | ✅ 3.12.3 |
| uv | >= 0.12 | ✅ 0.12.9 |
| Git | Any | ✅ 2.43.0 |
| RTK | Any | ✅ 0.47.0 |
| ripgrep | Any | ✅ 14.1.1 |
| CrewAI | >= 1.15 | ✅ 1.15.18 |
