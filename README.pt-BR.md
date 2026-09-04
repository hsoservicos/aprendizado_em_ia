# BMAD Method — Desenvolvimento Ágil com Inteligência Artificial

![Versão](https://img.shields.io/badge/version-6.11.0-blue)
![Skills](https://img.shields.io/badge/skills-57-green)
![CrewAI](https://img.shields.io/badge/CrewAI-1.15.18-purple)
![Coolify](https://img.shields.io/badge/Coolify-4.3.14-orange)
![Licença](https://img.shields.io/badge/license-MIT-yellow)

**Idiomas:** [English](README.md) | Português Brasil | [Español](README.es.md)

---

## Visão Geral

BMAD Method (Breakthrough Method for Agile Development) é um framework de desenvolvimento impulsado por IA que integra agentes especializados e skills no seu fluxo de trabalho. Este projeto fornece um ambiente completo para desenvolvimento ágil com assistentes de IA, com suporte a **deploy via Coolify** para infraestrutura PaaS self-hosted.

**Funcionalidades Principais:**
- 57 skills especializadas para diferentes tarefas de desenvolvimento
- 4 agentes específicos por tecnologia (Docker, Python 3.14, PHP 8.4, PostgreSQL 18)
- Integração com IDEs OpenCode e Claude Code
- Scripts automatizados de validação e renderização
- Compressão de tokens via RTK
- **Integração CrewAI** para orquestração de múltiplos agentes
- **Guias de deploy Coolify** e scripts de automação

---

## Primeiros Passos (comece aqui)

Se você é um membro da equipe que vai usar este repositório para **implementar um
projeto novo** ou para **modernizar/atualizar um projeto legado**, siga primeiro o
guia de onboarding:

**➡️ [`_bmad-output/getting-started.md`](_bmad-output/getting-started.md)**

Pré-flight (faça uma vez, nesta ordem):

| # | Passo | Comando |
|---|-------|---------|
| 0 | Instalar toolchain + os dois agentes | `./_bmad-output/scripts/install-linux.sh --project-dir "$PWD"` |
| 1 | Obter o repo + branch de trabalho | `git clone … && cd … && git checkout -b feat/setup` |
| 2 | Instalar/atualizar o BMAD | `npx bmad-method install` |
| 3 | Verificar toolchain, os dois agentes e o RTK | `diff -rq .agents/skills .claude/skills && rtk init --show` |
| 4 | Configurar o projeto | editar `_bmad/custom/config.toml` + `_bmad/config.user.toml` |
| 5 | Abrir um agente e se orientar | `opencode` ou `claude` → `/bmad-help` |

Depois escolha a trilha:

| Trilha | Quando | Para onde vai |
|--------|--------|---------------|
| **A — Projeto novo (greenfield)** | ainda não há código | `/bmad-help` → ciclo de vida de 5 fases |
| **B — Projeto legado (brownfield)** | base de código a modernizar | `/bmad-project-context` → `/bmad-code-review` → `/bmad-build` |

### Passo a passo detalhado (qualquer nível de conhecimento)

Para um guia **totalmente documentado e sem jargão** das duas trilhas —
conceitos, comandos exatos, entradas/saídas esperadas, portões de qualidade e
solução de problemas — use o **Manual de Implementação**. Ele foi escrito para
membros da equipe **independente de formação em Engenharia de Software**:

**➡️ [`_bmad-output/implementation-playbook.md`](_bmad-output/implementation-playbook.md)**

| Guia | Use para |
|------|----------|
| [`getting-started.md`](_bmad-output/getting-started.md) | Orientação de 5 min + pré-flight + seletor de trilha |
| [`implementation-playbook.md`](_bmad-output/implementation-playbook.md) | **O passo a passo detalhado para projeto novo ou legado (Partes A e B), glossário, Definition of Done, FAQ** |
| [`bmad-project-lifecycle-guide.md`](_bmad-output/bmad-project-lifecycle-guide.md) | Referência do operador: as 5 fases e a rotina diária |

---

## Início Rápido

### Pré-requisitos

| Ferramenta | Versão Mínima | Propósito |
|------------|---------------|-----------|
| Node.js | >= 20.12 | Runtime JavaScript |
| Python | >= 3.10, < 3.14 | Execução de scripts |
| uv | >= 0.12 | Gerenciador de pacotes Python |
| Git | Qualquer | Controle de versão |
| GitHub CLI (`gh`) | Qualquer | Operações de repositório / PR / release |
| RTK | >= 0.47 | Compressão de tokens para ambos os agentes (opcional) |
| ripgrep | >= 14.0 | Busca rápida, dependência do RTK (recomendado) |
| CrewAI | >= 1.15 | Orquestração de agentes (opcional) |
| Agente de codificação | — | OpenCode >= 1.18 e/ou Claude Code >= 2.1 |

> Todas as ferramentas acima funcionam a partir de **ambos** os agentes, OpenCode
> e Claude Code. Veja [Agentes de Codificação](#agentes-de-codificação).

### Instalação Automatizada

```bash
# Linux (Ubuntu/Debian)
chmod +x _bmad-output/scripts/install-linux.sh
./_bmad-output/scripts/install-linux.sh

# Windows (PowerShell como Administrador)
powershell -ExecutionPolicy Bypass -File _bmad-output/scripts/install-windows.ps1
```

### Instalação Manual

```bash
# Instalar BMAD Method (regenera as duas árvores de skills + comandos OpenCode)
npx bmad-method install

# Conectar o RTK aos dois agentes (por máquina)
rtk init -g --auto-patch --opencode

# Iniciar qualquer um dos agentes — os comandos BMAD são idênticos
opencode        # ou: claude

# No agente escolhido
/bmad-help
```

---

## Agentes de Codificação

Este projeto está configurado para **dois agentes de codificação intercambiáveis**.
Cada skill, comando e ferramenta funciona igual nos dois.

| Aspecto | OpenCode | Claude Code |
|---------|----------|-------------|
| Instruções | `AGENTS.md` | `CLAUDE.md` (importa `AGENTS.md`) |
| Skills (57) | `.agents/skills/` + `.opencode/commands/*.md` | `.claude/skills/` (descoberta nativa) |
| Invocação | `/bmad-help`, `/bmad-build`, … | `/bmad-help`, `/bmad-build`, … |
| Allow-list de ferramentas | `PATH` do shell | `.claude/settings.json` → `permissions.allow` |
| Compressão de tokens RTK | `~/.config/opencode/plugins/rtk.ts` | hook `PreToolUse` em `.claude/settings.json` (`rtk hook claude`) |
| Referência RTK | — | `.claude/RTK.md` |

`.agents/skills/` e `.claude/skills/` são mantidas byte a byte idênticas;
`npx bmad-method install` regenera ambas. Um comando conecta o RTK aos dois
agentes em uma máquina nova: `rtk init -g --auto-patch --opencode`.

---

## Estrutura do Projeto

```
/home/hsantos/app/
├── .agents/skills/          # 57 skills BMAD (OpenCode)
├── .claude/                 # Integração Claude Code
│   ├── skills/              # 57 skills BMAD (espelho idêntico)
│   ├── settings.json        # allow-list de ferramentas + hook RTK PreToolUse
│   └── RTK.md               # referência de comandos RTK para o agente
├── .opencode/commands/      # 57 wrappers de comando OpenCode
├── .git/                    # Repositório Git
├── AGENTS.md                # Instruções OpenCode
├── CLAUDE.md                # Instruções Claude Code (importa AGENTS.md)
├── _bmad/                   # Framework BMAD
│   ├── _config/             # Manifests e configs
│   ├── core/                # Skills core
│   ├── bmm/                 # Skills BMM
│   ├── scripts/             # Scripts Python
│   ├── config.toml          # Config principal
│   └── config.user.toml     # Config do usuário
├── _bmad-output/            # Artefatos de implementação
│   ├── getting-started.md               # Primeiros passos / onboarding (novo + legado)
│   ├── implementation-playbook.md       # Passo a passo detalhado, qualquer nível (Partes A e B)
│   ├── bmad-project-lifecycle-guide.md  # Guia completo do ciclo de vida
│   ├── coolify-deploy-guide.md         # Visão geral do deploy Coolify
│   ├── coolify-github-deploy-guide.md  # Deploy via GitHub
│   ├── coolify-local-deploy-guide.md   # Deploy local (sem Git)
│   ├── crewai-integration-guide.md     # Integração CrewAI + BMAD
│   ├── docker-skill-implementation.md  # Docs do agente Docker
│   ├── php84-skill-implementation.md   # Docs do agente PHP 8.4
│   ├── postgres18-skill-implementation.md  # Docs PostgreSQL 18
│   ├── project-replication-guide.md    # Guia completo de setup
│   ├── python314-skill-implementation.md   # Docs Python 3.14
│   ├── rtk-installation-guide.md       # Setup do RTK
│   ├── tools-registry.md              # Inventário de ferramentas
│   └── scripts/
│       ├── coolify-deploy.sh           # Automação de deploy Coolify
│       ├── install-linux.sh            # Instalação Linux
│       ├── install-windows.ps1         # Instalação Windows
│       └── ...
├── docs/                    # Conhecimento do projeto
└── README.md                # Este arquivo
```

---

## Skills BMAD (57 Total)

### Skills Core (24)

| Skill | Propósito |
|-------|-----------|
| `bmad-help` | Orientar no workflow, obter recomendações |
| `bmad-build` | Implementação principal de código |
| `bmad-build-auto` | Loop de build autônomo |
| `bmad-brainstorming` | Ideação e exploração criativa |
| `bmad-forge-idea` | Testar ideias sob pressão |
| `bmad-create-prd` | Documento de requisitos do produto |
| `bmad-architecture` | Design de arquitetura do sistema |
| `bmad-ux` | Padrões UX e specs de design |
| `bmad-create-epics-and-stories` | Quebrar trabalho em stories |
| `bmad-sprint-planning` | Prontidão do sprint |
| `bmad-code-review` | Review adversarial de código |
| `bmad-retrospective` | Retrospectiva do épico |
| `bmad-docker` | Containerização Docker |
| `bmad-python314` | Funcionalidades Python 3.14 |
| `bmad-php84` | Funcionalidades PHP 8.4 |
| `bmad-postgres18` | Funcionalidades PostgreSQL 18 |
| ... | e mais |

### Agentes de Tecnologia (4)

| Agente | Skills | Foco |
|--------|--------|------|
| `bmad-agent-docker` | 1 | Containerização, Dockerfile, Compose |
| `bmad-agent-python314` | 1 | Free-threading, t-strings, subinterpreters |
| `bmad-agent-php84` | 3 | Arch-PHP, CodeRefactor-PHP, WebSec-PHP |
| `bmad-agent-postgres18` | 5 | DDL, OPT, VEC, CONC, SEC |

---

## Fases do Workflow BMAD

1. **Clarify** — `bmad-help`, `bmad-brainstorming`, `bmad-forge-idea`
2. **Plan** — `bmad-create-prd`, `bmad-architecture`, `bmad-ux`, `bmad-create-epics-and-stories`
3. **Build** — `bmad-build`, `bmad-build-auto`
4. **Review** — `bmad-code-review`, `bmad-checkpoint-preview`
5. **Learn** — `bmad-retrospective`

Alterações pequenas podem pular direto para build. Trabalhos complexos seguem o caminho completo.

---

## Integração CrewAI

**O CrewAI está integrado à estrutura do projeto para uso conjunto com o BMAD
Method.** Não é uma ferramenta opcional à parte — é a **camada de orquestração
multi-agente** sobre as skills do BMAD:

- Instalado como CLI gerenciada (`uv tool install crewai` → `~/.local/bin/crewai`,
  v1.15.18) e registrado em `_bmad-output/tools-registry.md`.
- Acessível a partir dos **dois** agentes de codificação (OpenCode e Claude Code)
  — `crewai` está na lista de ferramentas pré-aprovadas em `.claude/settings.json`.
- Conectado ao BMAD pelo **bridge BMAD-CrewAI** (`BMADBridge`), que permite a um
  crew do CrewAI listar e renderizar skills do BMAD como etapas de um fluxo
  automatizado.
- Design, padrões e exemplos completos: **`_bmad-output/crewai-integration-guide.md`**.

**Como os dois se encaixam:** o BMAD fornece o *método* (57 skills, ciclo de vida
de 5 fases, agentes de tecnologia); o CrewAI fornece a *automação* (agentes por
papel, fluxos orientados a eventos, human-in-the-loop, checkpointing). Use as
skills do BMAD de forma interativa no trabalho que exige julgamento, e encapsule
sequências repetíveis e bem definidas dessas mesmas skills em um fluxo CrewAI.

### O que é CrewAI?

CrewAI é um framework Python open-source para orquestrar agentes de IA autônomos com papéis definidos. Oferece:

- **Crews**: Equipes de agentes com papéis, objetivos, ferramentas e tarefas
- **Flows**: Workflows orientados por eventos com gerenciamento de estado
- **Padrões prontos para produção**: Human-in-the-loop, execução assíncrona, checkpointing

### Benefícios da Integração

| Força do BMAD | Força do CrewAI | Benefício combinado |
|---------------|-----------------|---------------------|
| Expertise em workflow de desenvolvimento | Orquestração multi-agente | Pipelines de desenvolvimento automatizados |
| 57 skills especializadas | Colaboração de agentes por papel | Times de agentes especializados |
| Agentes específicos por tecnologia | Workflows orientados a eventos | Fluxos de automação complexos |

### Início Rápido com CrewAI

```bash
# Instalar CrewAI (se ainda não instalado)
uv tool install crewai

# Criar novo projeto CrewAI
crewai create crew bmad-project

# Navegar até o projeto e instalar dependências
cd bmad-project
crewai install

# Executar o crew
crewai run
```

### Bridge BMAD-CrewAI

```python
from bmad_crewai_bridge import BMADBridge

bridge = BMADBridge(project_root="/home/hsantos/app")
skills = bridge.list_skills()
output = bridge.render_skill("bmad-docker")
```

Veja o guia completo em `_bmad-output/crewai-integration-guide.md`.

---

## Deploy via Coolify

Deploy self-hosted usando **Coolify v4.3.14**. Deploy de aplicações via repositórios Git ou localmente sem Git.

### Métodos de Deploy

| Método | Fonte | Auth | Melhor Para |
|--------|-------|------|-------------|
| **Repositório Público** | URL HTTPS Git | Nenhum | Projetos open source |
| **Deploy Key** | URL SSH Git | Chave SSH | Repo privado único |
| **GitHub App** | Git (multi-repo) | OAuth + Webhook | Equipes, múltiplos repos |
| **Imagem Docker** | Registry (Docker Hub/GHCR) | Nenhum/Token | Imagens pré-construídas |
| **Dockerfile** | Colado no UI do Coolify | Nenhum | Apps simples sem Git |
| **Docker Compose Empty** | Colado no UI do Coolify | Nenhum | Stacks multi-serviço |
| **Service One-Click** | Templates Coolify | Nenhum | Apps populares (300+) |

### Deploy Rápido via CLI

```bash
# Instalar CLI do Coolify
curl -fsSL https://raw.githubusercontent.com/coollabsio/coolify-cli/main/scripts/install.sh | bash

# Configurar contexto
coolify context add -d production https://coolify.seudominio.com <TOKEN>

# Deploy de repo Git público
./_bmad-output/scripts/coolify-deploy.sh \
  --name meu-app \
  --repo https://github.com/usuario/repo \
  --port 3000

# Deploy de imagem Docker
./_bmad-output/scripts/coolify-deploy.sh \
  --name nginx \
  --docker-image nginx:alpine \
  --port 80
```

### Guias

- **Visão geral**: `_bmad-output/coolify-deploy-guide.md` (12 seções, 26K)
- **Repos GitHub**: `_bmad-output/coolify-github-deploy-guide.md` (9 seções, 18.5K)
- **Deploy local**: `_bmad-output/coolify-local-deploy-guide.md` (10 seções, 18.8K)

---

## Stack Tecnológica

### Agente Docker

- **Validação Dockerfile**: 15 regras (D001-D015)
- **Validação Compose**: 7 regras (C001-C007)
- **Otimização BuildKit**: Builds multi-stage
- **Hardening de segurança**: Usuários non-root, filesystem read-only

### Agente Python 3.14

- **Free-threading**: Modo No-GIL para paralelismo real
- **Subinterpreters**: Ambientes de execução isolados
- **t-strings**: Interpolação de strings com tipos
- **compression.zstd**: Suporte built-in ao Zstandard

### Agente PHP 8.4

- **Property Hooks**: Hooks get/set substituindo boilerplate
- **Asymmetric Visibility**: Padrões `public private(set)`
- **DOM API**: Parsing HTML5 nativo
- **Array Functions**: `array_find`, `array_any`, `array_all`

### Agente PostgreSQL 18

- **AIO**: `io_method = io_uring` para 3x de performance
- **B-Tree Skip Scan**: Otimização de índice multi-coluna
- **UUIDv7**: Primary keys ordenadas
- **pgvector**: Indexação HNSW, busca híbrida

---

## Scripts de Instalação

| Script | Sistema | Uso |
|--------|---------|-----|
| `install-linux.sh` | Ubuntu/Debian | `./install-linux.sh --project-dir /caminho` |
| `install-windows.ps1` | Windows 10/11 | `powershell -ExecutionPolicy Bypass -File install-windows.ps1` |

Veja `_bmad-output/scripts/README.md` para instruções detalhadas.

---

## Materiais e Ferramentas do Projeto (Índice)

Todo documento, script, arquivo de configuração e ferramenta deste repositório,
com **o que é** e **quando usar** — para qualquer membro da equipe localizar
rapidamente o material de estudo e referência. O inventário detalhado e
autoritativo (versões, caminhos, histórico) é **`_bmad-output/tools-registry.md`**
(v1.3.3).

### 1. Guias para começar (leia nesta ordem)

| # | Documento | O que é | Leia quando |
|---|-----------|---------|-------------|
| 1 | `_bmad-output/getting-started.md` | Onboarding de 5 min: pré-flight (Passos 0–5: toolchain, os dois agentes, RTK, config do projeto) + seletor de Trilha A/B. | Você acabou de clonar o repo e precisa começar. |
| 2 | `_bmad-output/implementation-playbook.md` | **Manual de Implementação (PT-BR)** — o passo a passo detalhado e sem jargão: glossário, 6 princípios, **Parte A (projeto novo / greenfield)** e **Parte B (modernização de legado / brownfield)**, Definition of Done, tabela de decisão, FAQ. Para **qualquer nível de conhecimento**. | Você está de fato construindo — sistema novo ou modernizando um existente. |
| 3 | `_bmad-output/bmad-project-lifecycle-guide.md` | Referência de operação: as 5 fases (Clarify → Plan → Build → Review → Learn), checklists por fase, rotina diária, cola de comandos, regras de ouro. | Você já conhece o fluxo e quer uma referência rápida. |
| 4 | `_bmad-output/project-replication-guide.md` (v1.1.0) | Como reproduzir o ambiente em uma **máquina nova**: requisitos de hardware/SO, instalação por ferramenta, setup dos agentes, script de validação, troubleshooting. | Configurando uma segunda máquina ou a máquina de um novo colega. |

### 2. Guias de integração e ferramentas

| Documento | O que é | Leia quando |
|-----------|---------|-------------|
| `_bmad-output/crewai-integration-guide.md` | Como o **CrewAI** está integrado ao projeto para uso conjunto com o BMAD — o `BMADBridge`, crews/flows, human-in-the-loop, exemplos. | Automatizando sequências repetíveis de skills do BMAD. |
| `_bmad-output/rtk-installation-guide.md` | Relatório completo do **RTK** (compressão de tokens): instalação, o plugin do OpenCode **e** o hook `PreToolUse` do Claude Code, diagramas, referência de comandos, troubleshooting. | Verificar/consertar o RTK ou entender o que ele faz. |
| `_bmad-output/tools-registry.md` | **Inventário canônico** — todo runtime, framework, agente, script e integração com versão, caminho, "usado por", mapa de diretórios e log de instalação datado. | Você precisa da versão/caminho exatos de algo, ou de um histórico. |

### 3. Referências dos agentes de tecnologia

| Documento | O que é |
|-----------|---------|
| `_bmad-output/docker-skill-implementation.md` | Agente & Skill Docker: regras de validação de Dockerfile/Compose (D001–D015, C001–C007), BuildKit, hardening, doc-sync. |
| `_bmad-output/python314-skill-implementation.md` | Agente & Skill Python 3.14: free-threading, subinterpreters, t-strings, `compression.zstd`, deferred annotations. |
| `_bmad-output/php84-skill-implementation.md` | Agente & Skill PHP 8.4: Property Hooks, Asymmetric Visibility, DOM API, novas funções de array. |
| `_bmad-output/postgres18-skill-implementation.md` | Agente & Skill PostgreSQL 18: AIO (`io_uring`), B-Tree Skip Scan, UUIDv7, `RETURNING OLD/NEW`, pgvector. |

### 4. Deploy (Coolify)

| Documento | O que é |
|-----------|---------|
| `_bmad-output/coolify-deploy-guide.md` | Visão geral + preparação + CLI + passo a passo (12 seções). Comece por aqui. |
| `_bmad-output/coolify-github-deploy-guide.md` | Fontes GitHub: repo público, Deploy Key, GitHub App (9 seções). |
| `_bmad-output/coolify-local-deploy-guide.md` | Fontes sem Git: Docker Image, Dockerfile colado, Compose Empty, Service one-click (10 seções). |
| `_bmad-output/scripts/coolify-deploy.sh` | Executável — deploy Coolify automatizado via CLI (repos públicos + privados, imagem Docker). |

### 5. Scripts de instalação e validação

| Arquivo | O que é |
|---------|---------|
| `_bmad-output/scripts/install-linux.sh` (v1.1.0) | Setup Linux/Ubuntu de uma vez: toolchain + os dois agentes + `npx bmad-method install` + RTK nos dois agentes + checagens de paridade. |
| `_bmad-output/scripts/install-windows.ps1` (v1.1.0) | O mesmo para Windows 10/11 (PowerShell como Administrador). |
| `_bmad-output/scripts/README.md` | Como rodar os scripts, passos pós-instalação, troubleshooting, desinstalação. |
| `_bmad-output/scripts/test-local.sh` | Validação/dry-run local do fluxo de instalação. |
| `_bmad-output/scripts/installation-validation-report.md` | Resultado da validação de ambiente. |
| `_bmad-output/scripts/windows-script-validation-report.md` | 73 casos de teste executados contra o script Windows. |

### 6. Instruções dos agentes e configuração

| Arquivo | O que é |
|---------|---------|
| `AGENTS.md` | Contrato do projeto lido pelo **OpenCode**: setup, paridade entre agentes, skills, onboarding, pré-requisitos. |
| `CLAUDE.md` | Ponto de entrada lido pelo **Claude Code** — importa `AGENTS.md` + notas específicas. |
| `.claude/settings.json` | Allow-list de ferramentas do Claude Code (`uv`, `rtk`, `rg`, `gh`, `crewai`, `npx bmad-method`) + hook RTK `PreToolUse`. |
| `.claude/RTK.md` | Referência de comandos RTK para o Claude Code. |
| `.opencode/commands/*.md` | 57 wrappers de comando do OpenCode (`/bmad-*`) apontando para `.agents/skills/`. |
| `_bmad/config.toml` | Config base gerenciada pelo instalador. **Não editar.** |
| `_bmad/config.user.toml` | Suas respostas pessoais de instalação (nome, idioma, nível). No gitignore. |
| `_bmad/custom/config.toml` | Overrides da equipe, commitado — o lugar para fixar configurações do projeto. |
| `_bmad/_config/manifest.yaml` | Metadados da instalação (módulos, IDEs alvo, versões). |

### 7. Scripts do motor BMAD (`_bmad/scripts/`)

| Script | O que faz |
|--------|-----------|
| `render_skill.py` | Renderiza o workflow de uma skill para um snapshot executável. **Única** forma suportada de rodar uma skill: `uv run _bmad/scripts/render_skill.py --project-root "$PWD" --skill .claude/skills/<nome>` (ou `.agents/skills/<nome>`). |
| `validate_dockerfile.py` | Valida Dockerfiles contra 15 regras (D001–D015). |
| `validate_compose.py` | Valida arquivos `docker-compose` contra 7 regras (C001–C007). |
| `docsync_docker.py` | Mantém a documentação Docker sincronizada. |
| `memlog.py` | Utilitário de log de memória das execuções de skill. |
| `config_utils.py` / `resolve_config.py` / `resolve_customization.py` | Helpers de resolução de config usados pelas skills. |

### 8. Ferramentas instaladas

| Ferramenta | Versão | Caminho | Propósito | Saiba mais |
|------------|--------|---------|-----------|------------|
| **Node.js** | v24.20.0 | nvm | Runtime JS; roda `npx bmad-method`, OpenCode | `project-replication-guide.md` |
| **npm** | 12.0.2 | com o Node | Gerenciador de pacotes | — |
| **Python** | 3.12.3 | sistema | Scripts BMAD e renderização de skills (precisa `>=3.10,<3.14`) | `project-replication-guide.md` |
| **uv** | 0.12.9 | `~/.local/bin/uv` | Runner Python rápido — `uv run` renderiza skills; `uv tool install` | `tools-registry.md` §1.4 |
| **Git** | 2.43.0 | sistema | Controle de versão | — |
| **GitHub CLI (`gh`)** | 2.73.0 | `~/.local/bin/gh` | Ops de repo / PR / release; `gh auth setup-git` para push | `tools-registry.md` §1.7 |
| **ripgrep (`rg`)** | 14.1.1 | `~/.local/bin/rg` | Busca rápida; dependência do RTK | `rtk-installation-guide.md` |
| **RTK** | 0.47.0 | `~/.local/bin/rtk` | Proxy de compressão de tokens — ativo nos **dois** agentes (plugin OpenCode + hook `PreToolUse` do Claude). `RTK_DISABLED=1 <cmd>` para saída crua. | `rtk-installation-guide.md` |
| **CrewAI** | 1.15.18 | `~/.local/bin/crewai` | Orquestração multi-agente integrada ao BMAD via `BMADBridge` | `crewai-integration-guide.md` |
| **OpenCode** | 1.18.27 | `~/.opencode/bin/opencode` | Agente de codificação — lê `AGENTS.md`, `.opencode/commands/`, `.agents/skills/` | `AGENTS.md` |
| **Claude Code** | 2.1.260 | `~/.local/bin/claude` | Agente de codificação — lê `CLAUDE.md`, `.claude/settings.json`, `.claude/skills/` | `CLAUDE.md` |
| **BMAD Method** | 6.11.0 | `_bmad/` | O framework — 57 skills, ciclo de 5 fases, agentes de tecnologia | `AGENTS.md`, `tools-registry.md` §2 |

### 9. "Eu quero… → leia isto"

| Objetivo | Comece por |
|----------|-----------|
| Fazer o onboarding | `getting-started.md` |
| Construir um projeto **novo** de ponta a ponta | `implementation-playbook.md` → Parte A |
| Modernizar / atualizar um projeto **legado** | `implementation-playbook.md` → Parte B |
| Referência rápida de operação das 5 fases | `bmad-project-lifecycle-guide.md` |
| Preparar uma máquina nova | `project-replication-guide.md` + `scripts/install-*.sh` |
| Automatizar sequências repetidas de skills | `crewai-integration-guide.md` |
| Entender / consertar a compressão de tokens | `rtk-installation-guide.md` |
| Fazer deploy em produção | `coolify-deploy-guide.md` (+ variantes github / local) |
| Consultar versão, caminho ou histórico exatos | `tools-registry.md` |
| Trabalhar com Docker / Python 3.14 / PHP 8.4 / PostgreSQL 18 | o `*-skill-implementation.md` correspondente + `/bmad-agent-*` |
| Visão geral em outro idioma | `README.md` (EN) · `README.es.md` |

---

## Exemplos de Uso

### Iniciar um Novo Projeto

```bash
# Clonar o repositório
git clone https://github.com/usuario/seu-repo.git
cd seu-repo

# Executar script de instalação (instala os dois agentes + conecta o RTK aos dois)
chmod +x _bmad-output/scripts/install-linux.sh
./_bmad-output/scripts/install-linux.sh

# Iniciar qualquer um dos agentes
opencode        # ou: claude

# No agente escolhido
/bmad-help
```

### Ciclo de Vida Completo (Recomendado)

Para novos projetos, siga o **ciclo de vida de 5 fases** documentado no guia:

| Fase | Skills | Duração | Saída |
|------|--------|---------|-------|
| **1. Clarify** | `bmad-help` → `bmad-brainstorming` → `bmad-forge-idea` | 30 min | Ideia validada |
| **2. Plan** | `bmad-create-prd` → `bmad-architecture` → `bmad-ux` → `bmad-create-epics-and-stories` | 1-2h | PRD + Arquitetura + UX + Stories |
| **3. Build** | `bmad-build` (por story) | Variável | Código funcional |
| **4. Review** | `bmad-code-review` → `bmad-qa-generate-e2e-tests` | 30 min | Código validado |
| **5. Learn** | `bmad-retrospective` → Deploy no Coolify | 30 min | Lições aprendidas + Produção |

**📖 Guia completo:** `_bmad-output/bmad-project-lifecycle-guide.md`

### Referência Rápida: Todas as Fases

```
/bmad-help              → Comece aqui, obtenha orientação
/bmad-brainstorming     → Sessão de ideação estruturada
/bmad-forge-idea        → Teste sua ideia sob pressão
/bmad-create-prd        → Criar Documento de Requisitos do Produto
/bmad-architecture      → Definir spine de arquitetura
/bmad-ux                → Criar DESIGN.md + EXPERIENCE.md
/bmad-create-epics-and-stories → Quebrar trabalho em stories rastreáveis
/bmad-sprint-planning   → Planejar execução do sprint
/bmad-build             → Implementar código (uma story por vez)
/bmad-build-auto        → Loop de build autônomo
/bmad-code-review       → Review adversarial de código
/bmad-retrospective     → Retrospectiva do épico com evidências
```

### Usar Agentes de Tecnologia

```
# Tarefas Docker
/bmad-docker
/bmad-agent-docker

# Tarefas Python 3.14
/bmad-python314
/bmad-agent-python314

# Tarefas PHP 8.4
/bmad-php84
/bmad-agent-php84

# Tarefas PostgreSQL 18
/bmad-postgres18
/bmad-agent-postgres18
```

### Renderizar uma Skill

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

## Configuração

### Config Principal

`_bmad/config.toml` — Gerenciado pelo instalador, não editar diretamente.

### Config da Equipe

`_bmad/custom/config.toml` — Overrides da equipe, commitado no repo.

### Config do Usuário

`_bmad/config.user.toml` — Configurações pessoais, no gitignore.

### Config dos Agentes de Codificação

| Arquivo | Agente | Commitado | Propósito |
|---------|--------|-----------|-----------|
| `AGENTS.md` | OpenCode | ✅ | Instruções do projeto |
| `CLAUDE.md` | Claude Code | ✅ | Ponto de entrada; importa `AGENTS.md` |
| `.claude/settings.json` | Claude Code | ✅ | Allow-list de ferramentas + hook RTK `PreToolUse` |
| `.claude/RTK.md` | Claude Code | ✅ | Referência de comandos RTK |
| `~/.config/opencode/plugins/rtk.ts` | OpenCode | local da máquina | Plugin RTK |

---

## Atualização

```bash
# Atualizar BMAD Method
npx bmad-method install

# Atualizar ferramentas
npm update -g opencode @anthropic-ai/claude-code
```

---

## Suporte

- **Documentação**: Veja `_bmad-output/` para guias detalhados — comece pelo
  [Índice de Materiais e Ferramentas](#materiais-e-ferramentas-do-projeto-índice)
- **Issues**: Abra uma issue no repositório do projeto
- **BMAD Method**: https://github.com/bmadmethod/bmad-method — o framework
  (57 skills, ciclo de vida de 5 fases, agentes de tecnologia); instalado em
  `_bmad/`, atualizado com `npx bmad-method install`
- **CrewAI**: https://github.com/crewAIInc/crewAI · docs https://docs.crewai.com
  — a camada de orquestração multi-agente **integrada ao BMAD** neste projeto
  (v1.15.18 em `~/.local/bin/crewai`, conectada via `BMADBridge`); veja
  [`_bmad-output/crewai-integration-guide.md`](_bmad-output/crewai-integration-guide.md)

---

## Licença

Licença MIT — Veja `_bmad/core/config.yaml` para detalhes.

---

## Contribuidores

- **Hsantos** — Mantenedor do projeto
- **BMAD Method** — Autores do framework
