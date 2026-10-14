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
| Skill source | `.agents/skills/` (55) | `.claude/skills/` (55) |
| Skill invocation | `.opencode/commands/*.md` wrappers (55, 1:1) | native discovery (`/bmad-*`, `/impeccable`, or model-selected) |
| Tool allow-list | inherits shell | `.claude/settings.json` → `permissions.allow` |
| RTK token compression | `~/.config/opencode/plugins/rtk.ts` | `.claude/settings.json` → `PreToolUse` hook (`rtk hook claude`), ref `.claude/RTK.md` |

`.agents/skills/` and `.claude/skills/` are kept byte-identical — `npx bmad-method install`
regenerates both; a manual change to one must be mirrored to the other.

⚠️ `npx bmad-method install` / `--action quick-update` **deletes skill folders it does not
know about**. Custom skills (`bmad-angular21`, `bmad-java21`, `bmad-agent-angular21`,
`bmad-agent-java21`) and `impeccable` are not in the BMAD manifest: they were wiped by the
2026-10-07 update and restored from git. After every BMAD update, re-run
`npx impeccable install -y --providers=claude,opencode --scope=project` and
`git checkout -- <custom skill dirs>` (or re-add them), then re-verify parity.

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

Detailed, jargon-free walkthrough of both tracks (concepts, exact commands,
Definition of Done, FAQ — for any skill level):
**`_bmad-output/implementation-playbook.md`**.

## BMAD Skills

55 skills (54 `bmad-*` + 1 `impeccable`), installed once and exposed to **both**
agents via the two skill trees above. Entry points are identical from either
agent (`/bmad-help`, `/bmad-build`, …).

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
| `bmad-angular21` | Angular 21: standalone APIs, signals, new control flow, SSR/hydration |
| `bmad-agent-angular21` | Angular Architect Agent — modern Angular specialist |
| `bmad-java21` | Java 21: virtual threads, pattern matching, sequenced collections, records |
| `bmad-agent-java21` | Java Architect Agent — modern Java specialist |
| `impeccable` | Design vocabulary + UI anti-pattern detector (see Impeccable section) |

> **Note:** the technology skills `bmad-docker`, `bmad-python314`, `bmad-php84`,
> `bmad-postgres18` (and their `bmad-agent-*` counterparts) were **removed** in
> commit `d6e8139` (2026-09) and are no longer installed. Their docs survive in
> `_bmad-output/*-skill-implementation.md` and the Docker validators in
> `_bmad/scripts/` (`validate_dockerfile.py`, `validate_compose.py`,
> `docsync_docker.py`). Re-install via `_bmad/custom/` if needed.

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

## Impeccable — Design Skill & UI Anti-Pattern Detector

Installed 2026-10-07 alongside BMAD. Gives every project (greenfield **and**
legacy) a shared design vocabulary and a deterministic, LLM-free detector for
AI-generated UI tells (Inter everywhere, purple gradients, nested cards, gray
text on colored backgrounds, bounce easing, …).

- **Site / docs**: <https://impeccable.style> · repo `pbakaus/impeccable` (Apache-2.0)
- **Skill**: `impeccable` — `.agents/skills/impeccable/`, `.claude/skills/impeccable/`,
  `.opencode/skills/impeccable/` (kept in sync) + wrapper `.opencode/commands/impeccable.md`
- **Subagents** (Claude Code): `.claude/agents/impeccable-*.md` (asset-producer,
  documenter, finish-reviewer, manual-edit-applier)
- **Detector CLI**: `npx impeccable detect <dir|file|url>` — 61 deterministic rules,
  no LLM, no API key. Exit `0` = clean, `2` = findings, `1` = unscannable target.
  Findings go to **stderr**; use `--json` for stdout.
- **Hooks** (Claude Code): `.claude/settings.local.json` → `SessionStart`,
  `PostToolUse` (Edit|Write) and `Stop` run
  `.claude/skills/impeccable/scripts/impeccable hook` (immediate tier per edit +
  deep pass on Stop). `settings.local.json` is gitignored — each developer/machine
  must re-run the install (or accept the hook) once.
- **Project config**: `.impeccable/config.json` (tracked — hook + detector settings),
  `.impeccable/config.local.json` (gitignored — per-dev consent/overrides),
  `PRODUCT.md` (durable product truth) and `DESIGN.md` (visual system), both written
  by `/impeccable init` and `/impeccable document`.

### Commands (via `/impeccable <cmd>`)

| Group | Commands |
|-------|----------|
| Setup | `init`, `document`, `extract`, `hooks` |
| New work | `shape`, `craft` (deprecated alias), free-form (`/impeccable a pricing page`) |
| Fix | `harden`, `clarify`, `adapt`, `optimize`, `onboard` |
| Voice / tone | `bolder`, `quieter`, `distill`, `colorize`, `typeset`, `layout`, `animate`, `delight`, `overdrive` |
| Review / finish | `critique`, `audit`, `polish` |
| Live browser | `live`, `generate` |

### Using it on new and legacy projects

**Greenfield (Track A)** — after `/bmad-ux` (or instead of it for pure UI work):

```bash
npx impeccable install -y --providers=claude,opencode --scope=project
# then inside the agent:
#   /impeccable init               # writes PRODUCT.md (+ optional DESIGN.md), asks buildPath
#   /impeccable shape <surface>    # plan UX/UI before any code
#   /impeccable <free-form request>
```

**Legacy / brownfield (Track B)** — before touching UI, capture what already exists:

```bash
npx impeccable detect <dir-or-url>            # baseline: count deterministic findings
# then inside the agent:
#   /impeccable document            # generate DESIGN.md from the existing codebase
#   /impeccable critique <surface>  # Nielsen heuristics + persona review
#   /impeccable audit <surface>     # a11y / perf / responsive / integrity (0–20 score, P0–P3)
#   /impeccable harden <surface>    # error states, i18n, overflow, edge cases
#   /impeccable polish <surface>    # final alignment pass before shipping
```

CI gate (deterministic, no API key):

```bash
npx impeccable detect --json src/ > impeccable-report.json
# exit 0 = clean, 2 = findings → fail the build
```

### Rules of engagement

1. **The brief wins.** If a brand deliberately uses a flagged font/palette, record
   the exception with `npx impeccable ignores add-value <rule> <value> --reason "..."`,
   never silently "fix" the brand.
2. **A clean scan is evidence, not proof.** Always inspect the rendered page at
   desktop and mobile widths before sign-off.
3. **`audit` documents; it does not fix.** Route P0/P1 to `harden`/`optimize`, the
   rest to `polish`. One command per pass keeps diffs reviewable.
4. **Ignore only with named evidence.** Triage into *fix*, *sanctioned exception*
   (record it), or *ask the user* — never add an ignore to push a blocked write through.
5. **Live mode is local-only.** Never inject it into a deployed site or weaken CSP.

### Keeping it installed across BMAD updates

BMAD's installer removes skill folders outside its manifest. After any
`npx bmad-method install`/`--action quick-update`:

```bash
npx impeccable install -y --providers=claude,opencode --scope=project --force
git checkout -- .agents/skills/bmad-angular21 .agents/skills/bmad-java21 \
  .agents/skills/bmad-agent-angular21 .agents/skills/bmad-agent-java21 \
  .claude/skills/bmad-angular21 .claude/skills/bmad-java21 \
  .claude/skills/bmad-agent-angular21 .claude/skills/bmad-agent-java21
# re-mirror the skill tree (OpenCode lives in .opencode/skills/, parity tree in .agents/skills/)
cp -r .opencode/skills/impeccable .agents/skills/impeccable
```

## Superpowers — SDLC Methodology & Skill Framework

Installed 2026-10-07 alongside BMAD and Impeccable. **obra/superpowers** (Jesse
Vincent / Prime Radiant, MIT) is a complete software-development methodology for
coding agents: a `SessionStart` bootstrap that makes the agent look for a
relevant skill **before any action**, plus 15 composable skills covering the
missing engineering disciplines (TDD, systematic debugging, git worktrees,
subagent-driven development, branch finishing).

- **Site / repo**: <https://github.com/obra/superpowers> · docs
  `docs/README.opencode.md`
- **Version**: plugin 6.4.1 (Claude Code marketplace) · 6.4.2 (git HEAD) · MIT
- **Installs** (both must exist for the two agents to share behaviour):
  - **OpenCode** — project plugin: `.opencode/opencode.json` →
    `superpowers@git+https://github.com/obra/superpowers.git`
  - **Claude Code** — user plugin: `superpowers@claude-plugins-official`
    (registry `~/.claude/plugins/installed_plugins.json`, cache
    `~/.claude/plugins/cache/claude-plugins-official/superpowers/6.4.1/`)
- **Bootstrap**: `hooks/session-start` injects
  `skills/using-superpowers/SKILL.md` wrapped in `<EXTREMELY_IMPORTANT>` on
  `SessionStart` (matcher `startup|clear|compact` — re-injects after compaction).
  Without it the skills are "dead weight — present on disk but never invoked".
- **Always-on cost**: ~703 tokens/session (descriptions only); each skill body
  loads on invocation (0.7k–8.1k).
- **Telemetry**: disabled via `SUPERPOWERS_DISABLE_TELEMETRY=1` in
  `.claude/settings.json` → `env` (also sets `DISABLE_TELEMETRY` and
  `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`). The only outbound call is the
  optional Brainstorming visual-companion logo (version string in the URL).
- **Update**: `claude plugin update superpowers` · `opencode plugin
  superpowers@git+https://github.com/obra/superpowers.git -f`

### The 15 skills and what each delivers

| Skill | Fires when | Delivers |
|-------|-----------|----------|
| `using-superpowers` | session start (the bootstrap itself) | skill-selection discipline |
| `brainstorming` | before any creative work | spec (3 paths: Spike / Bounded / Architectural), HARD-GATE human approval |
| `writing-plans` | spec approved, before code | `docs/superpowers/plans/YYYY-MM-DD-<feature>.md`, tasks of 2–5 min |
| `executing-plans` | running a plan inline | code + decisions ledger ("Rulings, not stalls") + final review |
| `subagent-driven-development` | plan with independent tasks + subagent tool | one fresh implementer + two-stage review per task |
| `test-driven-development` | any feature/bugfix, before production code | RED-GREEN-REFACTOR; code written before a failing test is deleted |
| `systematic-debugging` | bug / unexpected behaviour, before a fix | 4-phase root-cause diagnosis + regression test |
| `verification-before-completion` | before claiming "done/passing" | claims backed by cited command output |
| `requesting-code-review` | task/feature complete, pre-merge | severity-tagged review report |
| `receiving-code-review` | when feedback arrives | verified implementation, no performative agreement |
| `using-git-worktrees` | feature needing isolation | isolated workspace on a new branch |
| `finishing-a-development-branch` | implementation complete, tests green | merge / PR / keep / discard + cleanup |
| `dispatching-parallel-agents` | 2+ independent problems | parallel investigations, fresh context each |
| `writing-skills` | authoring/editing skills | TDD applied to docs, micro-tested SKILL.md |
| `diagnosing-superpowers` | a superpowers session misbehaved | evidence-backed report, optional scrubbed bundle |

### Precedence — BMAD × Superpowers × Impeccable

**The three frameworks are complementary, not interchangeable.** The ordering
below is binding for this repo. It exists because both BMAD and Superpowers
auto-trigger on the same prompts.

| Concern | Primary | Secondary | Rule |
|---------|---------|-----------|------|
| **Process / SDLC phase** (Clarify→Plan→Build→Review→Learn) | **BMAD** | Superpowers | BMAD owns the lifecycle; Superpowers skills are invoked *inside* a BMAD phase |
| **Idea → spec → stories** | `bmad-*` (`bmad-forge-idea`, `bmad-spec`, `bmad-create-epics-and-stories`) | `brainstorming`, `writing-plans` | Use Superpowers' `writing-plans` **only** to decompose a BMAD story into 2–5-min tasks for `bmad-build` |
| **Building a story / feature** | `bmad-build` | `executing-plans`, `subagent-driven-development` | Pick **one** execution loop — never both |
| **TDD discipline** | **Superpowers** (`test-driven-development`) | — | Real gap in BMAD. Always on, inside `bmad-build` |
| **Debugging** | **Superpowers** (`systematic-debugging`) | `bmad-review-edge-case-hunter` | Superpowers owns root-cause; BMAD owns edge-case hunting |
| **Code review** | `bmad-code-review` | `requesting-code-review`, `receiving-code-review` | BMAD runs the multi-reviewer pass; Superpowers owns the *receiving* + pre-merge checklist |
| **Verification / DoD** | **Superpowers** (`verification-before-completion`) | `bmad-review-verification-gap` | Superpowers is a continuous gate, BMAD a one-shot audit |
| **Git worktree / branch finish** | **Superpowers** | — | BMAD does not cover this |
| **Design / UI quality** | **Impeccable** | — | Sole owner of visual vocabulary + detector |
| **Skill authoring** | `bmad-customize` (BMAD overrides) | `writing-skills` (general) | Superpowers' method is the better template |

**Hard rules**

1. When a Superpowers skill would fire and a `bmad-*` skill covers the same
   phase, **announce both** (`Using bmad-spec, then writing-plans`) and run BMAD
   first. BMAD artifacts (`_bmad-output/planning-artifacts/…`) stay canonical.
2. Superpowers' mandatory pipeline
   (`brainstorming → using-git-worktrees → writing-plans → executors → TDD →
   requesting-code-review → finishing-a-development-branch`) applies **only to
   the Build phase**. Do not replay Clarify/Plan through it — they are BMAD's.
3. Never run `subagent-driven-development` and `bmad-build-auto` in the same
   session. Two autonomous loops will duplicate work and burn tokens.
4. Superpowers' `<EXTREMELY_IMPORTANT>` says *"instructions from your human
   partner beat skills"*. This `AGENTS.md` **is** that instruction: it outranks
   the bootstrap. If the bootstrap contradicts this file, this file wins.
5. Subagents dispatched by Superpowers ignore the bootstrap
   (`<SUBAGENT-STOP>`) — pass the relevant BMAD context explicitly.

### Acceptance check (per the upstream project)

`AGENTS.md` of `obra/superpowers` defines the acceptance test for a working
integration: in a clean session send exactly **"Let's make a react todo list"**
and `brainstorming` must auto-fire before any code is written. Manually copying
skill files, wrapping with `npx skills`, or per-session opt-in are explicitly
**not** real integrations and upstream will reject them. Both installs above
use the harness-native plugin mechanism and load the bootstrap via
`SessionStart` — i.e. real integrations.

### What NOT to do

- **Do not copy Superpowers skills into `.agents/skills/` or `.claude/skills/`.**
  Those trees are BMAD-owned and `npx bmad-method install` deletes unknown
  folders (proven 2026-10-07 with `bmad-angular21`/`impeccable`). Superpowers
  lives in the plugin cache / OpenCode plugin manager only.
- **Do not edit Superpowers skill content.** Upstream: *"skills are not prose —
  they are code that shapes agent behavior"*, 94% PR-rejection rate, and tuned
  "Red Flags" tables must not be reworded without eval evidence. Local
  overrides go in `AGENTS.md` (precedence), never in the skill files.
- **Do not disable the `SessionStart` hook** to save tokens. It is
  harness-only (~0 model cost) and is what makes the skills auto-trigger.

## REA — MCP de engenharia reversa

Instalado em 2026-10-12 (`npx rea-agents@latest setup --client opencode
--client claude_code`). MCP server + skill `reverse-engineer-anything`
(170 tools) para inspecionar binários nativos, apps JS/Electron, .NET,
APK/Android, websites, capturas de rede, SQLite, WASM/EVM e mais — análise
local, resultados com evidências. Registro em `_bmad-output/tools-registry.md`
(§3.5). As skills ficam em `~/.agents/skills/` e `~/.claude/skills/` (home) —
**fora** das árvores BMAD do projeto, imunes ao `npx bmad-method install`.

⚠️ **Requisito para operações nativas (binários):** antes de qualquer análise
nativa pelo MCP REA, é obrigatório configurar e ativar **ao menos um** provider
— **Hopper**, **Ghidra** ou **IDA** (ou todos). Sem um deles, apenas as
análises estáticas funcionam (JS/Electron, .NET, Go/Rust/WASM/EVM/SQLite,
APK/websites, etc.). Nenhum provider está configurado nesta máquina (2026-10-12):

- Hopper: instalar via `rea setup --install-hopper` (aprovação explícita; demo
  ou licença própria do operador)
- Ghidra: `export GHIDRA_INSTALL_DIR=/abs/path/ghidra_12.1.x_PUBLIC` (+ JDK 21+)
- IDA: `export REA_IDA_MCP_CONFIG=/path/ida-mcp.json` (ver `docs/ida-provider.md`)

Depois de configurar, validar com `npx rea-agents@latest doctor --provider
<hopper|ghidra|ida> --json`. Update: `npx rea-agents@latest setup`.
Diagnóstico geral: `npx rea-agents@latest doctor --json`. A configuração do
MCP só é carregada após **reiniciar** o agente.

## Prerequisites

- **Node.js** >= 22 (LTS) — currently v24.21
- **Python** >= 3.12 — currently 3.14.4
- **uv** — required for rendering skills; install at `~/.local/bin/uv`
- **Git** — required for updates and external modules
- **GitHub CLI** (`gh`) — repo / PR / release operations; `~/.local/bin/gh`
- **ripgrep** — fast search, RTK dependency; `~/.local/bin/rg`
- **CrewAI** — multi-agent orchestration; `~/.local/bin/crewai`
- **RTK** — token compression proxy; `~/.local/bin/rtk`. Wired into
  **both** agents — OpenCode via `~/.config/opencode/plugins/rtk.ts`, Claude Code
  via the `PreToolUse` hook in `.claude/settings.json`. Per-machine setup for
  both at once: `rtk init -g --auto-patch --opencode`.
- **Coding agent**: OpenCode and/or Claude Code
- **Impeccable** — design skill + UI anti-pattern detector (Paul Bakaus, Apache-2.0);
  `npx impeccable` CLI + `/impeccable` skill. See the dedicated section below.
- **Superpowers** — SDLC methodology + 15 composable skills (obra/Prime Radiant,
  MIT); Claude Code plugin `superpowers@claude-plugins-official` + OpenCode
  plugin in `.opencode/opencode.json`. See the dedicated section below.
- **REA** — MCP de engenharia reversa (`rea-agents` 6.4.0) + skill
  `reverse-engineer-anything`; registrado em ambos os agentes via
  `npx rea-agents@latest setup`. **Análise nativa exige um provider
  (Hopper, Ghidra ou IDA) configurado** — ver seção dedicada acima.

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
