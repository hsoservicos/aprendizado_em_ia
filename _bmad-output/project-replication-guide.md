# Project Replication Guide — Guia Completo de Replicação

**Version**: 1.1.0  
**Last Updated**: 2026-09-04  
**Author**: Hsantos  
**Status**: Production Ready

> **v1.1.0** — full parity between the two coding agents: OpenCode **and**
> Claude Code share the same 57 skills, the same toolchain, and RTK token
> compression (`.claude/settings.json` hook mirrors the OpenCode plugin).

> **Escopo:** este guia = preparar a **máquina**. Para os **primeiros passos de
> um projeto** (novo ou legado a modernizar) depois que a máquina está pronta,
> siga **`_bmad-output/getting-started.md`**.

---

## 1. Overview

Este guia documenta o processo completo para replicar o ambiente de desenvolvimento do projeto `/home/hsantos/app` em uma nova máquina. O ambiente inclui:

- **BMAD Method v6.11.0** — Framework de desenvolvimento ágil com IA
- **OpenCode** — IDE para agentes de IA
- **Claude Code** — Assistente de IA Anthropic
- **RTK** — Proxy de compressão de tokens
- **57 Skills** — Habilidades especializadas
- **8 Scripts** — Validação e renderização
- **4 Agentes Technology** — Docker, Python 3.14, PHP 8.4, PostgreSQL 18

---

## 2. System Requirements

### 2.1 Minimum Hardware

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 2 cores | 4+ cores |
| RAM | 4 GB | 8+ GB |
| Storage | 10 GB free | 20+ GB free |
| Network | Internet connection | Broadband |

### 2.2 Operating Systems

| OS | Version | Status |
|----|---------|--------|
| Ubuntu | 22.04+ / 24.04 | ✅ Supported |
| Debian | 11+ / 12 | ✅ Supported |
| Windows | 10 (21H2+) / 11 | ✅ Supported |
| macOS | 12+ (Monterey) | ⚠️ Partial |

### 2.3 Required Software

| Software | Minimum Version | Purpose |
|----------|----------------|---------|
| Node.js | >= 20.12 | JavaScript runtime, BMAD installer |
| Python | >= 3.10, < 3.14 | Script execution, skill rendering |
| Git | >= 2.30 | Version control |
| uv | >= 0.12 | Python package management |
| GitHub CLI (`gh`) | any | Repo / PR / release operations |
| RTK | >= 0.47 | Token compression for both agents (optional) |
| ripgrep | >= 14.0 | Fast search, RTK dependency (recommended) |
| CrewAI | >= 1.15 | Multi-agent orchestration (optional) |

Every tool above works from **both** OpenCode and Claude Code.

---

## 3. Pre-Installation Checklist

Before starting, ensure you have:

- [ ] Access to terminal/command prompt with admin privileges
- [ ] Internet connection for downloading packages
- [ ] GitHub account (for repository access)
- [ ] Anthropic API key (for Claude Code)
- [ ] OpenCode installed (or will be installed)

---

## 4. Installation Steps

### Phase 1: System Dependencies

#### Linux (Ubuntu/Debian)

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install essential build tools
sudo apt install -y build-essential curl wget git unzip software-properties-common apt-transport-https

# Install Node.js (via nvm)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
source ~/.bashrc
nvm install 24
nvm use 24
nvm alias default 24

# Install Python
sudo apt install -y python3 python3-pip python3-venv

# Verify installations
node --version   # Should show v24.x.x
python3 --version # Should show 3.10+
git --version    # Should show 2.30+
```

#### Windows (10/11)

```powershell
# Run PowerShell as Administrator

# Install Chocolatey (package manager)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Node.js
choco install nodejs-lts -y

# Install Python
choco install python -y

# Install Git
choco install git -y

# Refresh environment
refreshenv

# Verify installations
node --version
python --version
git --version
```

### Phase 2: Developer Tools

#### Linux

```bash
# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Install ripgrep
curl -LO https://github.com/BurntSushi/ripgrep/releases/download/14.1.1/ripgrep-14.1.1-x86_64-unknown-linux-musl.tar.gz
tar xzf ripgrep-14.1.1-x86_64-unknown-linux-musl.tar.gz
mkdir -p ~/.local/bin
cp ripgrep-14.1.1-x86_64-unknown-linux-musl/rg ~/.local/bin/
rm -rf ripgrep-14.1.1-x86_64-unknown-linux-musl*

# Install RTK (optional but recommended)
curl -LO https://github.com/anomalyco/rtk/releases/latest/download/rtk-linux-x64
chmod +x rtk-linux-x64
mv rtk-linux-x64 ~/.local/bin/rtk

# Add to PATH if not already
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### Windows

```powershell
# Install uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install ripgrep
choco install ripgrep -y

# Install RTK (if available for Windows)
# Download from GitHub releases and add to PATH

# Refresh environment
refreshenv
```

### Phase 3: IDE Setup

#### OpenCode

```bash
# Install OpenCode via npm
npm install -g opencode

# Or use npx (no global install)
npx opencode --version

# Configure OpenCode (first run)
opencode init
```

#### Claude Code

```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Or use npx
npx @anthropic-ai/claude-code --version

# Configure with API key
claude config set apiKey YOUR_API_KEY
```

#### Wire RTK into BOTH agents (one command)

```bash
# Global Claude Code PreToolUse hook + OpenCode plugin
rtk init -g --auto-patch --opencode

# Verify
rtk init --show
#   [ok] OpenCode: plugin installed ...
#   [ok] Hook: rtk hook claude
```

> The project already ships an **in-repo** Claude Code hook in
> `.claude/settings.json`, so RTK compression works in this repo even before the
> global step. `rtk hook claude` is idempotent — project + global hooks coexist.

#### Agent parity checklist

| Item | OpenCode | Claude Code |
|------|----------|-------------|
| Instructions | `AGENTS.md` | `CLAUDE.md` (imports `AGENTS.md`) |
| Skills (57) | `.agents/skills/` + `.opencode/commands/` | `.claude/skills/` (native discovery) |
| Tool allow-list | shell `PATH` | `.claude/settings.json` → `permissions.allow` |
| RTK | `~/.config/opencode/plugins/rtk.ts` | `.claude/settings.json` `PreToolUse` hook |

### Phase 4: BMAD Method Installation

```bash
# Navigate to project directory
cd /path/to/your/project

# Initialize git repository (if new project)
git init
git remote add origin https://github.com/your-org/your-repo.git

# Install BMAD Method
npx bmad-method install

# The installer will:
# 1. Create _bmad/ directory structure
# 2. Install core and bmm modules
# 3. Generate config files
# 4. Set up skills and commands
```

### Phase 5: Project Configuration

#### 5.1 Customize Config Files

Edit `_bmad/custom/config.toml` for team settings:

```toml
# Team overrides (committed to repo)
[core]
project_name = "my-project"
document_output_language = "English"
output_folder = "_bmad-output"

[agents.bmad-agent-pm]
description = "Custom PM description"
```

Edit `_bmad/config.user.toml` for personal settings (gitignored):

```toml
# Personal overrides (not committed)
[core]
user_name = "YourName"
communication_language = "English"
```

#### 5.2 Create Project Structure

```bash
# Create required directories
mkdir -p docs
mkdir -p _bmad-output
mkdir -p .claude

# Create .gitignore
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
__pycache__/
*.pyc
.venv/
venv/

# BMAD personal configs
_bmad/config.user.toml
_bmad/custom/config.user.toml

# Output artifacts (optional - commit if needed)
_bmad-output/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
EOF
```

#### 5.3 Agent Instruction & Settings Files

`AGENTS.md` is created by earlier steps / the reference repo. Add the Claude Code
counterparts so both agents are configured identically:

```bash
# CLAUDE.md — Claude Code entry point; imports AGENTS.md
cat > CLAUDE.md << 'EOF'
# CLAUDE.md

Claude Code's entry point. Counterpart of AGENTS.md (OpenCode). Both agents share
one source of truth, the same 57 BMAD skills, and the same toolchain.

@AGENTS.md

## Claude Code specifics
- Skills: .claude/skills/ (mirror of .agents/skills/), invoked as /bmad-*
- Settings: .claude/settings.json (tool allow-list + RTK PreToolUse hook)
- Render: uv run _bmad/scripts/render_skill.py --project-root "$PWD" --skill .claude/skills/<name>
EOF

# .claude/settings.json — tool allow-list + RTK hook (mirrors the OpenCode plugin)
cat > .claude/settings.json << 'EOF'
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(uv run:*)", "Bash(uvx:*)", "Bash(rtk:*)", "Bash(rg:*)",
      "Bash(gh:*)", "Bash(npx bmad-method:*)", "Bash(crewai:*)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [ { "type": "command", "command": "rtk hook claude" } ] }
    ]
  }
}
EOF
```

Commit all three (`AGENTS.md`, `CLAUDE.md`, `.claude/settings.json`, plus
`.claude/RTK.md` if used) so a clone is agent-ready with no extra steps.

---

## 5. Custom Skills Installation

The project includes 4 custom technology agents. To replicate them:

### 5.1 Docker Agent & Skill

```bash
# Files to copy (from reference project)
mkdir -p .agents/skills/bmad-docker/references
mkdir -p .agents/skills/bmad-agent-docker
mkdir -p .claude/skills/bmad-docker/references
mkdir -p .claude/skills/bmad-agent-docker
mkdir -p .opencode/commands

# Copy files from reference project or create new
# See: _bmad-output/docker-skill-implementation.md
```

### 5.2 Python 3.14 Agent & Skill

```bash
mkdir -p .agents/skills/bmad-python314/references
mkdir -p .agents/skills/bmad-agent-python314
mkdir -p .claude/skills/bmad-python314/references
mkdir -p .claude/skills/bmad-agent-python314

# See: _bmad-output/python314-skill-implementation.md
```

### 5.3 PHP 8.4 Agent & Skill

```bash
mkdir -p .agents/skills/bmad-php84/references
mkdir -p .agents/skills/bmad-agent-php84
mkdir -p .claude/skills/bmad-php84/references
mkdir -p .claude/skills/bmad-agent-php84

# See: _bmad-output/php84-skill-implementation.md
```

### 5.4 PostgreSQL 18 Agent & Skill

```bash
mkdir -p .agents/skills/bmad-postgres18/references
mkdir -p .agents/skills/bmad-agent-postgres18
mkdir -p .claude/skills/bmad-postgres18/references
mkdir -p .claude/skills/bmad-agent-postgres18

# See: _bmad-output/postgres18-skill-implementation.md
```

---

## 6. Validation

After installation, verify everything works:

```bash
# Run validation script
cat << 'EOF' > validate-setup.sh
#!/bin/bash
echo "=== BMAD Environment Validation ==="
echo ""

# Check Node.js
echo -n "Node.js: "
node --version 2>/dev/null || echo "❌ NOT FOUND"

# Check npm
echo -n "npm: "
npm --version 2>/dev/null || echo "❌ NOT FOUND"

# Check Python
echo -n "Python: "
python3 --version 2>/dev/null || echo "❌ NOT FOUND"

# Check uv
echo -n "uv: "
uv --version 2>/dev/null || echo "❌ NOT FOUND"

# Check Git
echo -n "Git: "
git --version 2>/dev/null || echo "❌ NOT FOUND"

# Check RTK
echo -n "RTK: "
rtk --version 2>/dev/null || echo "⚠️ NOT FOUND (optional)"

# Check ripgrep
echo -n "ripgrep: "
rg --version 2>/dev/null | head -1 || echo "⚠️ NOT FOUND (recommended)"

# Check GitHub CLI
echo -n "gh: "
gh --version 2>/dev/null | head -1 || echo "⚠️ NOT FOUND"

# Check BMAD
echo -n "BMAD Method: "
npx bmad-method --version 2>/dev/null || echo "❌ NOT FOUND"

# Check coding agents
echo -n "OpenCode: "
opencode --version 2>/dev/null || echo "⚠️ NOT FOUND"
echo -n "Claude Code: "
claude --version 2>/dev/null || echo "⚠️ NOT FOUND"

# Check skills count (both trees must match)
echo ""
echo "=== Skills Count ==="
echo "Skills in .agents/skills/: $(ls -d .agents/skills/bmad-* 2>/dev/null | wc -l)"
echo "Skills in .claude/skills/: $(ls -d .claude/skills/bmad-* 2>/dev/null | wc -l)"
echo "Commands in .opencode/commands/: $(ls .opencode/commands/bmad-*.md 2>/dev/null | wc -l)"
diff -rq .agents/skills .claude/skills >/dev/null 2>&1 \
  && echo "Skill trees: ✅ identical" || echo "Skill trees: ⚠️ DIVERGED — re-run 'npx bmad-method install'"

# Check agent config files
echo ""
echo "=== Agent Config ==="
[ -f AGENTS.md ] && echo "AGENTS.md: ✅" || echo "AGENTS.md: ❌"
[ -f CLAUDE.md ] && echo "CLAUDE.md: ✅" || echo "CLAUDE.md: ❌"
[ -f .claude/settings.json ] && echo ".claude/settings.json: ✅" || echo ".claude/settings.json: ❌"
grep -q "rtk hook claude" .claude/settings.json 2>/dev/null \
  && echo "RTK hook (Claude Code): ✅" || echo "RTK hook (Claude Code): ⚠️ not configured"
[ -f "$HOME/.config/opencode/plugins/rtk.ts" ] \
  && echo "RTK plugin (OpenCode): ✅" || echo "RTK plugin (OpenCode): ⚠️ not configured"

echo ""
echo "=== Validation Complete ==="
EOF

chmod +x validate-setup.sh
./validate-setup.sh
```

---

## 7. Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `uv: command not found` | Run `source ~/.bashrc` or restart terminal |
| `rtk: command not found` | Ensure `~/.local/bin` is in PATH |
| BMAD install fails | Ensure Node.js >= 20.12 and npm >= 10 |
| Skills not rendering | Check `uv` is installed and in PATH |
| OpenCode plugin not loading | Verify `~/.config/opencode/plugins/rtk.ts` exists |
| Claude Code RTK hook not firing | `.claude/settings.json` must have the `PreToolUse`/`Bash` hook; restart Claude Code; check with `rtk init --show` |
| Claude Code prompts for every tool | Ensure `.claude/settings.json` `permissions.allow` is present and valid JSON |
| Skill trees diverged | Re-run `npx bmad-method install` (regenerates `.agents/skills/` **and** `.claude/skills/`) |
| Wire RTK for both agents | `rtk init -g --auto-patch --opencode` |

### PATH Configuration

Add to `~/.bashrc` or `~/.zshrc`:

```bash
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/.npm-global/bin:$PATH"
```

---

## 8. Quick Start

After installation, start developing with **either** agent — the BMAD commands
are identical:

```bash
cd /path/to/your/project

# Option A — OpenCode
opencode

# Option B — Claude Code
claude

# In either agent, use BMAD commands:
# /bmad-help          — Get started
# /bmad-build         — Build features
# /bmad-code-review   — Review code
# /bmad-docker        — Docker tasks
# /bmad-python314     — Python 3.14 tasks
# /bmad-php84         — PHP 8.4 tasks
# /bmad-postgres18    — PostgreSQL 18 tasks
```

**Próximo:** siga o onboarding do projeto em `_bmad-output/getting-started.md`
(pré-flight + Trilha A projeto novo / Trilha B projeto legado).

---

## 9. References

| Document | Location |
|----------|----------|
| Getting Started (onboarding) | `_bmad-output/getting-started.md` |
| Implementation Playbook (detailed, new & legacy) | `_bmad-output/implementation-playbook.md` |
| Project Lifecycle (5 phases) | `_bmad-output/bmad-project-lifecycle-guide.md` |
| Tools Registry | `_bmad-output/tools-registry.md` |
| Docker Implementation | `_bmad-output/docker-skill-implementation.md` |
| Python 3.14 Implementation | `_bmad-output/python314-skill-implementation.md` |
| PHP 8.4 Implementation | `_bmad-output/php84-skill-implementation.md` |
| PostgreSQL 18 Implementation | `_bmad-output/postgres18-skill-implementation.md` |
| RTK Installation | `_bmad-output/rtk-installation-guide.md` |

---

## 10. Support

For issues or questions:
- Check `AGENTS.md` for project documentation
- Review `_bmad-output/tools-registry.md` for tool details
- Consult BMAD Method documentation at https://github.com/bmadmethod/bmad-method
