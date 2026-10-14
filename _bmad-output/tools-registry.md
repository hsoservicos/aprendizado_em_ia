# Tools Registry — Inventário de Ferramentas do Projeto

**Last Updated**: 2026-10-12T00:00:00Z
**Maintainer**: Hsantos
**Version**: 1.6.0

---

## Overview

Este artefato rastrea todas as ferramentas, dependências e recursos instalados no projeto `/home/hsantos/app`. Deve ser atualizado sempre que uma nova ferramenta for instalada, implementada ou interagida.

---

## 1. Runtime Environment

### 1.1 Node.js Runtime

| Property | Value |
|----------|-------|
| **Name** | Node.js |
| **Version** | v24.21.0 |
| **Path** | System PATH |
| **Purpose** | JavaScript runtime, package management, BMAD installer |
| **Installed** | Pre-existing |
| **Used By** | BMAD Method, npm packages, OpenCode |

### 1.2 npm (Node Package Manager)

| Property | Value |
|----------|-------|
| **Name** | npm |
| **Version** | 12.2.0 |
| **Path** | System PATH |
| **Purpose** | Package management, script execution |
| **Installed** | With Node.js |
| **Used By** | BMAD Method, `npx bmad-method install` |

### 1.3 Python Runtime

| Property | Value |
|----------|-------|
| **Name** | Python |
| **Version** | 3.14.4 |
| **Path** | System PATH |
| **Purpose** | Script execution, BMAD skill rendering |
| **Installed** | System |
| **Used By** | BMAD scripts (`render_skill.py`, validators) |

### 1.4 uv (Python Package Manager)

| Property | Value |
|----------|-------|
| **Name** | uv |
| **Version** | 0.12.23 |
| **Path** | `~/.local/bin/uv` |
| **Purpose** | Fast Python package installation, script execution |
| **Installed** | Manual |
| **Used By** | BMAD skill rendering (`uv run`) |
| **Status** | ✅ Active |

### 1.5 Git

| Property | Value |
|----------|-------|
| **Name** | Git |
| **Version** | 2.53.0 |
| **Path** | System PATH |
| **Purpose** | Version control, repository management |
| **Installed** | System |
| **Used By** | All version control operations |

### 1.6 CrewAI

| Property | Value |
|----------|-------|
| **Name** | CrewAI |
| **Version** | 1.15.25 |
| **Path** | `~/.local/bin/crewai` |
| **Purpose** | Multi-agent orchestration framework |
| **Installed** | 2026-09-03 via `uv tool install crewai` |
| **Used By** | BMAD-CrewAI integration, automated workflows |
| **Status** | ✅ Active |
| **Python** | >= 3.12 |
| **Dependencies** | 134 packages (auto-installed) |
| **Available to** | OpenCode + Claude Code (allow-listed in `.claude/settings.json`) |

### 1.7 GitHub CLI (`gh`)

| Property | Value |
|----------|-------|
| **Name** | GitHub CLI |
| **Version** | 2.102.0 |
| **Path** | `~/.local/bin/gh` |
| **Purpose** | Repository, PR, issue and release operations against GitHub |
| **Installed** | Manual |
| **Used By** | Repo sync, `gh repo`, `gh pr`, `gh release` |
| **Status** | ✅ Active |
| **Available to** | OpenCode + Claude Code (allow-listed in `.claude/settings.json`) |

### 1.8 Coding Agents

| Agent | Version | Path | Config surface | RTK integration |
|-------|---------|------|----------------|-----------------|
| **OpenCode** | 1.18.35 | `~/.opencode/bin/opencode` | `AGENTS.md`, `.opencode/commands/`, `.agents/skills/` | `~/.config/opencode/plugins/rtk.ts` |
| **Claude Code** | 2.1.289 | `~/.local/bin/claude` | `CLAUDE.md`, `.claude/settings.json`, `.claude/skills/` | `PreToolUse` hook in `.claude/settings.json` (`rtk hook claude`) + `.claude/RTK.md` |

Both agents run the **same 55 skills** and the **same toolchain**. See §3.

> **Atualizado em 2026-10-05** (sessão de transferência de conhecimento):
> toolchain validado — Node **v24.21.0** · npm **12.2.0** · uv **0.12.23** ·
> CrewAI **1.15.23** · gh **2.102.0** · RTK **0.51.0** · OpenCode **1.18.34** ·
> Claude Code **2.1.289** · ripgrep 15.2.0 · Git 2.43.0.
> Instância Coolify **4.3.23** · Traefik **v3.7**.


---

## 2. BMAD Method Framework

### 2.1 BMAD Core

| Property | Value |
|----------|-------|
| **Name** | BMAD Method |
| **Version** | 6.12.1 |
| **Install Date** | 2026-09-02T13:16:32.974Z |
| **Last Update** | 2026-10-07 (`--action quick-update`) |
| **Modules** | `core` (6.12.1), `bmm` (6.12.1) |
| **IDEs** | opencode, claude-code |
| **Config** | `_bmad/config.toml`, `_bmad/config.user.toml` |
| **Manifest** | `_bmad/_config/manifest.yaml` |
| **Status** | ✅ Active |

### 2.2 Skills (55 Total)

| Category | Count | Location |
|----------|-------|----------|
| **Official BMAD skills** | 50 | `_bmad/core/`, `_bmad/bmm/` (incl. 21 deprecated v6-shims) |
| **Custom skills (Technology Agents)** | 4 | `.agents/skills/`, `.claude/skills/` |
| **Impeccable (design)** | 1 | `.agents/skills/`, `.claude/skills/`, `.opencode/skills/` |
| **Total** | 55 | `.agents/skills/`, `.claude/skills/` (byte-identical, parity verified 2026-10-07) |

#### Custom Skills Created (Technology Agents)

| Skill | Agent | Features |
|-------|-------|----------|
| `bmad-angular21` | `bmad-agent-angular21` | Standalone APIs, signals, new control flow, SSR/hydration |
| `bmad-java21` | `bmad-agent-java21` | Virtual threads, pattern matching, sequenced collections, records |

> **Removed in `d6e8139` (2026-09):** `bmad-docker`, `bmad-python314`,
> `bmad-php84`, `bmad-postgres18` and their `bmad-agent-*` counterparts. Their
> implementation docs survive in `§5.1`; the Docker validators survive in
> `§2.3`. `_bmad/render/bmad-docker/` is a stale gitignored render artifact.

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
| `_bmad/_config/skill-manifest.csv` | All registered skills (50 entries) |
| `_bmad/_config/files-manifest.csv` | File tracking (36.6K) |
| `_bmad/_config/bmad-help.csv` | Help system data |
| `_bmad/_config/manifest.yaml` | Installation metadata |

---

## 3. Coding Agent Integration

Every capability in this registry is reachable from **both** OpenCode and Claude Code.

| Surface | OpenCode | Claude Code |
|---------|----------|-------------|
| Instructions file | `AGENTS.md` | `CLAUDE.md` (imports `AGENTS.md`) |
| Skill tree | `.agents/skills/` (55) | `.claude/skills/` (55) — byte-identical mirror |
| Skill invocation | `.opencode/commands/*.md` (`/bmad-*`) | native skill discovery (`/bmad-*`) |
| Tool allow-list | shell `PATH` | `.claude/settings.json` → `permissions.allow` |
| RTK compression | `~/.config/opencode/plugins/rtk.ts` | `.claude/settings.json` → `PreToolUse` hook |
| RTK reference | — | `.claude/RTK.md` |

### 3.1 OpenCode Commands (55 Total)

| Category | Count |
|----------|-------|
| **Core Commands** | 50 |
| **Custom Commands** | 5 |
| **Total** | 55 |

#### Custom Commands Created

| Command | File | Purpose |
|---------|------|---------|
| `bmad-angular21` | `.opencode/commands/bmad-angular21.md` | Angular 21 skill |
| `bmad-agent-angular21` | `.opencode/commands/bmad-agent-angular21.md` | Angular 21 agent |
| `bmad-java21` | `.opencode/commands/bmad-java21.md` | Java 21 skill |
| `bmad-agent-java21` | `.opencode/commands/bmad-agent-java21.md` | Java 21 agent |
| `impeccable` | `.opencode/commands/impeccable.md` | Design skill + UI anti-pattern detector |

Removed in `d6e8139`: `bmad-docker`, `bmad-python314`, `bmad-php84`,
`bmad-postgres18` + their `bmad-agent-*` wrappers.

### 3.2 Claude Code Integration

| Component | Location | Purpose |
|-----------|----------|---------|
| **Instructions** | `CLAUDE.md` | Entry point; `@AGENTS.md` import + Claude-specific notes |
| **Settings** | `.claude/settings.json` | Tool allow-list (`uv`, `rtk`, `rg`, `gh`, `crewai`, `npx bmad-method`) + RTK `PreToolUse` hook |
| **Settings (local)** | `.claude/settings.local.json` | Impeccable hooks (gitignored, per-machine) |
| **RTK reference** | `.claude/RTK.md` | RTK command reference for the agent |
| **Skills** | `.claude/skills/` (55) | Auto-discovered; invoked as `/bmad-*`, `/impeccable`, or model-selected |
| **Subagents** | `.claude/agents/impeccable-*.md` (4) | asset-producer, documenter, finish-reviewer, manual-edit-applier |

Skills are **not** duplicated as command files for Claude Code — it discovers
`.claude/skills/` natively, so `/bmad-help`, `/bmad-build`, `/impeccable`, etc.
work with no wrapper. The 55 skills in `.claude/skills/` are kept identical
to `.agents/skills/`; `npx bmad-method install` regenerates both (but drops
custom skills — see §8).

**Per-machine RTK wiring (both agents):** `rtk init -g --auto-patch --opencode`

### 3.3 Impeccable — Design Skill & UI Anti-Pattern Detector

| Property | Value |
|----------|-------|
| **Name** | Impeccable (Paul Bakaus) |
| **Version** | CLI 4.1.0 · engine v0.1.11 · skill 11.8K |
| **License** | Apache-2.0 |
| **Site / Repo** | <https://impeccable.style> · `pbakaus/impeccable` |
| **Install Date** | 2026-10-07 (`npx impeccable install -y --providers=claude,opencode --scope=project`) |
| **Purpose** | Shared design vocabulary + deterministic (LLM-free) detector of AI-generated UI anti-patterns |
| **Detector rules** | 61 deterministic, no API key |
| **Status** | ✅ Active |

**Layout:**

| Component | Location |
|-----------|----------|
| Skill (parity tree) | `.agents/skills/impeccable/`, `.claude/skills/impeccable/` |
| Skill (OpenCode native) | `.opencode/skills/impeccable/` |
| OpenCode wrapper | `.opencode/commands/impeccable.md` |
| Subagents (Claude Code) | `.claude/agents/impeccable-{asset-producer,documenter,finish-reviewer,manual-edit-applier}.md` |
| Hook manifest | `.claude/settings.local.json` (`SessionStart`, `PostToolUse` Edit\|Write, `Stop`) |
| Project config | `.impeccable/config.json` (tracked), `.impeccable/config.local.json` (gitignored) |
| Product / design truth | `PRODUCT.md`, `DESIGN.md` (written by `/impeccable init`, `/impeccable document`) |

**Detector CLI exit codes:** `0` clean · `2` primary findings · `1` target not
scannable. Findings → stderr; `--json` → stdout.

**Usage — greenfield:** `npx impeccable install …` → `/impeccable init` →
`/impeccable shape <surface>` → `/impeccable <free-form>`.
**Usage — legacy:** `npx impeccable detect <dir|url>` (baseline) →
`/impeccable document` → `/impeccable critique|audit|harden|polish <surface>`.
**CI gate:** `npx impeccable detect --json src/ > impeccable-report.json`
(exit 2 fails the build).

**Maintenance:** BMAD's installer deletes skill folders outside its manifest.
After every `npx bmad-method install`/`quick-update`, re-run
`npx impeccable install -y --providers=claude,opencode --scope=project --force`,
restore the 4 custom skills from git and re-mirror
`.opencode/skills/impeccable` → `.agents/skills/impeccable`. See `AGENTS.md`.

### 3.4 Superpowers — SDLC Methodology & Skill Framework

| Property | Value |
|----------|-------|
| **Name** | Superpowers (obra / Prime Radiant) |
| **Version** | plugin 6.4.1 (Claude marketplace) / 6.4.2 (git HEAD) |
| **License** | MIT |
| **Repo** | <https://github.com/obra/superpowers> |
| **Install Date** | 2026-10-07 |
| **Purpose** | Engineering methodology for coding agents (TDD, debugging, worktrees, subagent-driven development) |
| **Skills** | 15 |
| **Always-on cost** | ~703 tok/sessão |
| **Status** | ✅ Active |

**Layout:**

| Component | Location |
|-----------|----------|
| Plugin OpenCode | `.opencode/opencode.json` (`superpowers@git+https://github.com/obra/superpowers.git`) |
| Plugin Claude Code | `~/.claude/plugins/cache/claude-plugins-official/superpowers/6.4.1/` |
| Registry | `~/.claude/plugins/installed_plugins.json` |
| Hook | `SessionStart` (matcher `startup\|clear\|compact`) |
| Telemetry | off via `.claude/settings.json` env (`SUPERPOWERS_DISABLE_TELEMETRY=1`) |
| Docs | `AGENTS.md` (seção Superpowers) |

**Skills (15) e triggers:**

| Skill | Trigger |
|-------|---------|
| `using-superpowers` | Bootstrap do SessionStart — escolher skill antes de agir |
| `brainstorming` | Antes de qualquer trabalho criativo |
| `writing-plans` | Spec aprovada, antes do código — tasks de 2–5 min |
| `executing-plans` | Executar um plano inline (loop de execução) |
| `subagent-driven-development` | Tasks independentes via subagentes (review de 2 etapas) |
| `test-driven-development` | Feature/bugfix — ciclo RED-GREEN-REFACTOR |
| `systematic-debugging` | Bug/comportamento inesperado — causa-raiz |
| `verification-before-completion` | Antes de dizer "pronto" — citar saída real dos comandos |
| `requesting-code-review` | Tarefa completa, pré-merge |
| `receiving-code-review` | Ao receber feedback de review |
| `using-git-worktrees` | Feature que precisa de isolamento |
| `finishing-a-development-branch` | Implementação completa, testes verdes |
| `dispatching-parallel-agents` | 2+ problemas independentes |
| `writing-skills` | Autorar/editar skills |
| `diagnosing-superpowers` | Sessão do Superpowers com mau comportamento |

**Precedence:** BMAD owns the SDLC phase; Superpowers owns TDD/debug/worktree/
branch-finish/verification; Impeccable owns design. Never run
`subagent-driven-development` and `bmad-build-auto` in the same session.
See `AGENTS.md` (seção "Precedence — BMAD × Superpowers × Impeccable").

**Maintenance:** after `npx bmad-method install`, Superpowers is unaffected (it
lives outside the skill trees) — but confirm with `claude plugin list` and
`cat .opencode/opencode.json`. Never copy it into `.agents/skills/` /
`.claude/skills/` (the BMAD installer deletes unknown folders).

### 3.5 REA — Reverse Engineer Anything (MCP)

| Property | Value |
|----------|-------|
| **Name** | REA (Reverse Engineer Anything) |
| **Version** | `rea-agents` 6.4.0 (npm) · skill v37 · 170 tools |
| **License** | MIT |
| **Repo / Site** | <https://github.com/morluto/rea> · <https://rea.tools> |
| **Install Date** | 2026-10-12 (`npx rea-agents@latest setup --client opencode --client claude_code --yes`) |
| **Purpose** | MCP server + skill de engenharia reversa: binários nativos, JS/Electron, .NET, APK/Android, websites, capturas de rede, SQLite, WASM/EVM, etc. — análise local, resultados com evidências |
| **Status** | ✅ Active (registrations aligned; providers nativos não configurados) |

**Layout (user-level — fora do repo, imune ao `bmad-method install`):**

| Component | Location |
|-----------|----------|
| MCP registration (OpenCode) | `~/.config/opencode/opencode.jsonc` → `mcp.rea` (`npx -y rea-agents@6.4.0 mcp`) |
| MCP registration (Claude Code) | `~/.claude.json` → `mcpServers.rea` (mesmo comando, pinado em 6.4.0) |
| Skill (shared / OpenCode) | `~/.agents/skills/reverse-engineer-anything/` |
| Skill (Claude Code) | `~/.claude/skills/reverse-engineer-anything/` |
| Backups | `*.rea.backup` ao lado de cada config alterada |
| Cache / state | `~/.rea` (removível com `rea uninstall --purge-data`) |

**Providers nativos (opcionais, não instalados):** Hopper (comercial/demo —
instalável via setup com aprovação explícita `--install-hopper`), Ghidra
(`GHIDRA_INSTALL_DIR`), IDA (`REA_IDA_MCP_CONFIG`). Sem eles, JS/Electron,
.NET, Go/Rust/WASM/EVM/SQLite, APK e websites continuam funcionando.

> ⚠️ **Requisito obrigatório para operações nativas (binários):** antes de usar
> o MCP REA em qualquer análise de binário nativo, é **obrigatório configurar e
> ativar ao menos um provider** — **Hopper**, **Ghidra** ou **IDA** (ou todos).
> Sem um provider ativo, `open_binary`/decompilação/assembly **não funcionam**;
> apenas as análises estáticas (JS/Electron, .NET, Go/Rust/WASM/EVM/SQLite,
> APK, websites) operam sem provider. Nenhum provider está configurado nesta
> máquina (2026-10-12) — configurar antes de qualquer trabalho nativo:
>
> | Provider | Configuração | Validação |
> |----------|--------------|-----------|
> | Hopper | `npx rea-agents@latest setup --install-hopper` (aprovação explícita; demo ou licença do operador) | `rea doctor --provider hopper --json` |
> | Ghidra 12.1.x | `export GHIDRA_INSTALL_DIR=/abs/path/ghidra_12.1.x_PUBLIC` (+ JDK 21+) | `rea doctor --provider ghidra --json` |
> | IDA | `export REA_IDA_MCP_CONFIG=/path/ida-mcp.json` (ver `docs/ida-provider.md`) | `rea doctor --provider ida --json` |
>
> Depois de configurar, rodar `npx rea-agents@latest doctor --json` e
> **reiniciar o agente**. Também registrado em `AGENTS.md` (seção REA).

**CLI:** `npx rea-agents@latest <cmd>` ou `npm install --global rea-agents` →
`rea <cmd>`. Diagnóstico: `rea doctor --json` (read-only). Update:
`npx rea-agents@latest setup` (re-registra e atualiza a skill). Uninstall:
`rea uninstall` (preserva Hopper/skills de terceiros).

**Maintenance:** as skills do REA ficam em `~/.agents/skills/` e
`~/.claude/skills/` (home), **não** em `.agents/skills/`/`.claude/skills/` do
projeto — logo, o `npx bmad-method install` não as apaga. Para atualizar,
re-executar o setup e reiniciar os agentes.

---

## 4. RTK (Rust Token Killer)

### 4.1 RTK Binary

| Property | Value |
|----------|-------|
| **Name** | RTK |
| **Version** | 0.51.0 |
| **Path** | `~/.local/bin/rtk` |
| **Purpose** | CLI proxy for token compression (60-90% savings) |
| **Platform** | Ubuntu 24.04.4 LTS (x86_64) |
| **Status** | ✅ Active |

### 4.2 RTK Dependencies

| Dependency | Version | Path |
|------------|---------|------|
| ripgrep (`rg`) | 15.2.0 | `~/.local/bin/rg` |

### 4.3 RTK Integration

| Component | Location | Agent |
|-----------|----------|-------|
| **OpenCode Plugin** | `~/.config/opencode/plugins/rtk.ts` | OpenCode |
| **Claude Code Hook** | `.claude/settings.json` → `hooks.PreToolUse[matcher=Bash]` → `rtk hook claude` | Claude Code (project) |
| **Claude Code Hook (global, optional)** | `~/.claude/settings.json` via `rtk init -g` | Claude Code (all repos) |
| **Claude Code RTK reference** | `.claude/RTK.md` | Claude Code |
| **Global Filters** | `~/.config/rtk/filters.toml` | both |
| **Global Config** | `~/.config/rtk/config.toml` | both |
| **Project Filters** | `<project-root>/.rtk/filters.toml` | both |
| **Tee Logs** | `~/.local/share/rtk/tee/` | both |

Both integrations delegate to the same engine (`rtk rewrite` / `rtk hook`), so
`git status` → `rtk git status` transparently in either agent. `rtk hook claude`
is idempotent — a project hook and a global hook may coexist safely.
One-liner to wire both agents on a new machine: `rtk init -g --auto-patch --opencode`.

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
| `getting-started.md` | ~9K | First steps / onboarding — pre-flight + Track A (greenfield) & Track B (legacy modernization) |
| `implementation-playbook.md` | ~30K | Detailed, jargon-free step-by-step for a new OR legacy project (Parts A & B) — concepts, commands, Definition of Done, FAQ; for any skill level |
| `bmad-project-lifecycle-guide.md` | ~20K | 5-phase lifecycle, step by step |
| `project-replication-guide.md` | ~16K | Environment replication for a new machine (v1.1.0) |
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
| `AGENTS.md` | Project instructions, skills, workflow (OpenCode) |
| `CLAUDE.md` | Claude Code entry point — imports `AGENTS.md` + agent-specific notes |
| `.claude/settings.json` | Claude Code tool allow-list + RTK `PreToolUse` hook |
| `.claude/RTK.md` | RTK command reference surfaced to Claude Code |

---

## 6. Directory Structure

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
│   ├── scripts/             # Python scripts (8 files)
│   ├── config.toml          # Main config
│   └── config.user.toml     # User config
├── _bmad-output/            # Implementation artifacts
│   ├── getting-started.md          # First steps / onboarding (new + legacy)
│   ├── implementation-playbook.md  # Detailed step-by-step, any skill level (Parts A & B)
│   ├── bmad-project-lifecycle-guide.md  # 5-phase lifecycle
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
| 2026-09-04 | gh (GitHub CLI) 2.73.0 | Registered (pre-existing at `~/.local/bin/gh`) | Hsantos |
| 2026-09-04 | Claude Code 2.1.260 | Registered as coding agent | Hsantos |
| 2026-09-04 | OpenCode 1.18.27 | Version bump (was implicit) | Hsantos |
| 2026-09-04 | `CLAUDE.md` | Created — Claude Code entry point, imports `AGENTS.md` | Hsantos |
| 2026-09-04 | `.claude/settings.json` | Created — tool allow-list + RTK `PreToolUse` hook | Hsantos |
| 2026-09-04 | `.claude/RTK.md` | Created — RTK reference for Claude Code | Hsantos |
| 2026-09-04 | RTK ↔ Claude Code | Integrated (project hook `rtk hook claude`) for parity with OpenCode plugin | Hsantos |
| 2026-09-04 | RTK global (both agents) | `rtk init -g --auto-patch` (Claude hook) + `--opencode` (plugin) — machine-level | Hsantos |
| 2026-09-04 | `getting-started.md` | Created — onboarding: pre-flight + Track A (greenfield) & Track B (legacy modernization) | Hsantos |
| 2026-09-04 | `implementation-playbook.md` | Created — detailed jargon-free step-by-step for new & legacy projects (Parts A & B), any skill level | Hsantos |
| 2026-09-04 | README (EN/PT-BR/ES) | Added "Project Materials & Tools" index; CrewAI stated as integrated with BMAD; CrewAI registered in the Support section (upstream repo + docs); trilingual parity restored | Hsantos |
| 2026-10-07 | BMAD Method v6.12.1 | `--action quick-update` (core 6.11.0→6.12.1, bmm 6.11.0→6.12.1); 50 official skills refreshed | OpenCode |
| 2026-10-07 | Custom skills (angular21/java21) | Restored from git after BMAD installer deleted them (they are not in the BMAD manifest) | OpenCode |
| 2026-10-07 | CrewAI v1.15.25 | Repaired — uv tool env was corrupted (`Failed find package 'crewai'`); `uv tool install crewai --force` | OpenCode |
| 2026-10-07 | Python 3.14.4 / Node v24.21.0 / uv 0.12.23 / Git 2.53.0 / gh 2.102.0 / rg 15.2.0 / RTK 0.51.0 | Version audit — registry refreshed | OpenCode |
| 2026-10-07 | Impeccable CLI 4.1.0 + engine v0.1.11 | Installed via `npx impeccable install -y --providers=claude,opencode --scope=project` | OpenCode |
| 2026-10-07 | Impeccable skill | Mirrored to `.agents/skills/` for tree parity (installer only wrote `.claude/` + `.opencode/`) | OpenCode |
| 2026-10-07 | Impeccable hooks | `.claude/settings.local.json` — SessionStart + PostToolUse(Edit\|Write) + Stop | OpenCode |
| 2026-10-07 | `bmad-docker` / `bmad-python314` / `bmad-php84` / `bmad-postgres18` | Confirmed **removed** in `d6e8139` (2026-09); docs corrected (were still listed as installed) | OpenCode |
| 2026-10-07 | Registry v1.4.0 | Full audit + Impeccable section (§3.3) | OpenCode |
| 2026-10-07 | Superpowers plugin (OpenCode) | Instalado via `opencode plugin` em `.opencode/opencode.json` (projeto) | OpenCode |
| 2026-10-07 | Superpowers plugin (Claude Code) | Instalado via `claude plugin install superpowers@claude-plugins-official` (usuário, v6.4.1) | OpenCode |
| 2026-10-07 | Superpowers telemetry | Desligado (`SUPERPOWERS_DISABLE_TELEMETRY=1`) em `.claude/settings.json` env | OpenCode |
| 2026-10-07 | toolchain-installation-guide.md | Criado — instalação/ativação/uso de BMAD + Impeccable + Superpowers | OpenCode |
| 2026-10-07 | superpowers-study-2026-10-07.md | Criado — estudo/auditoria do obra/superpowers | OpenCode |
| 2026-10-07 | Registry v1.5.0 | Seção 3.4 Superpowers + toolchain completa | OpenCode |
| 2026-10-12 | REA (`rea-agents` 6.4.0) | Instalado via `npx rea-agents@latest setup --client opencode --client claude_code --yes` — MCP registrado em `~/.config/opencode/opencode.jsonc` e `~/.claude.json`; skill v37 (170 tools) em `~/.agents/skills/` + `~/.claude/skills/` | OpenCode |
| 2026-10-12 | Registry v1.6.0 | Seção 3.5 REA | OpenCode |

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

### After every `npx bmad-method install` / `--action quick-update`

The BMAD installer **removes skill folders it does not know about** (proven on
2026-10-07: it wiped `bmad-angular21`, `bmad-java21`, `bmad-agent-angular21`,
`bmad-agent-java21`). Always run this recovery sequence, then re-verify parity:

```bash
# 1. restore the custom Technology-Agent skills the installer deleted
git checkout -- .agents/skills/bmad-angular21 .agents/skills/bmad-java21 \
  .agents/skills/bmad-agent-angular21 .agents/skills/bmad-agent-java21 \
  .claude/skills/bmad-angular21 .claude/skills/bmad-java21 \
  .claude/skills/bmad-agent-angular21 .claude/skills/bmad-agent-java21 \
  .opencode/commands/bmad-angular21.md .opencode/commands/bmad-java21.md \
  .opencode/commands/bmad-agent-angular21.md .opencode/commands/bmad-agent-java21.md

# 2. re-install Impeccable (skill + hooks + subagents) and re-mirror the tree
npx impeccable install -y --providers=claude,opencode --scope=project --force
cp -r .opencode/skills/impeccable .agents/skills/impeccable

# 3. verify parity between the two skill trees
diff <(ls .agents/skills) <(ls .claude/skills) && echo PARITY_OK
```

If a `git checkout` cannot recover a deleted custom skill (not committed),
re-create it from `_bmad/custom/` or restore from a backup before continuing.

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
node --version && python3 --version && uv --version && git --version \
  && rtk --version && crewai version && gh --version | head -1

# Check both coding agents
opencode --version && claude --version

# List all BMAD skills (either tree — kept identical)
rtk ls .claude/skills/          # Claude Code
rtk ls .agents/skills/          # OpenCode

# List all OpenCode commands
rtk ls .opencode/commands/

# Check RTK savings (works in both agents)
rtk gain

# Verify RTK wiring for both agents
rtk init --show

# Render a skill
uv run _bmad/scripts/render_skill.py --project-root /home/hsantos/app --skill .claude/skills/<skill-name>
uv run _bmad/scripts/render_skill.py --project-root /home/hsantos/app --skill .agents/skills/<skill-name>

# Install/update BMAD (regenerates both skill trees + OpenCode commands)
npx bmad-method install

# Wire RTK into both agents on a new machine
rtk init -g --auto-patch --opencode

# CrewAI commands
crewai version
crewai create crew <project-name>
crewai run
```

### Prerequisites

| Tool | Required Version | Status | Available to |
|------|-----------------|--------|--------------|
| Node.js | >= 22 | ✅ v24.21.0 | both agents |
| Python | >= 3.12 | ✅ 3.14.4 | both agents |
| uv | >= 0.12 | ✅ 0.12.23 | both agents |
| Git | Any | ✅ 2.53.0 | both agents |
| GitHub CLI (`gh`) | Any | ✅ 2.102.0 | both agents |
| RTK | Any | ✅ 0.51.0 | both agents (OpenCode plugin + Claude hook) |
| ripgrep | Any | ✅ 15.2.0 | both agents |
| CrewAI | >= 1.15 | ✅ 1.15.25 | both agents |
| OpenCode | Any | ✅ 1.18.35 | — |
| Claude Code | Any | ✅ 2.1.289 | — |
| Impeccable CLI | >= 4.1 | ✅ 4.1.0 (engine v0.1.11) | both agents + CI |
| Superpowers | >= 6.4 | ✅ 6.4.1 (Claude) / 6.4.2 (OpenCode) | both agents |
| REA (`rea-agents`) | >= 6.4 | ✅ 6.4.0 (skill v37) | both agents (MCP) |
