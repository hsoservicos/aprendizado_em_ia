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

Este projeto inclui **CrewAI** para orquestração de múltiplos agentes, permitindo fluxos de trabalho automatizados.

### O que é CrewAI?

CrewAI é um framework Python open-source para orquestrar agentes de IA autônomos com papéis definidos. Oferece:

- **Crews**: Equipes de agentes com papéis, objetivos, ferramentas e tarefas
- **Flows**: Workflows orientados por eventos com gerenciamento de estado
- **Padrões prontos para produção**: Human-in-the-loop, execução assíncrona, checkpointing

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

## Documentação

### Documentação Principal

| Documento | Localização | Descrição |
|-----------|-------------|-----------|
| **Primeiros Passos** | `_bmad-output/getting-started.md` | **Primeiros passos antes de um projeto novo ou modernização de legado — pré-flight + trilhas A/B** |
| **Manual de Implementação** | `_bmad-output/implementation-playbook.md` | **Passo a passo detalhado e sem jargão para projeto novo OU legado — conceitos, comandos, portões de qualidade, FAQ (qualquer nível)** |
| **Guia do Ciclo de Vida** | `_bmad-output/bmad-project-lifecycle-guide.md` | **Passo a passo completo: 5 fases da ideia à produção** |
| AGENTS.md / CLAUDE.md | `/AGENTS.md`, `/CLAUDE.md` | Instruções do projeto (OpenCode / Claude Code) |
| Registro de Ferramentas | `_bmad-output/tools-registry.md` | Inventário de ferramentas (v1.3.1) |
| Guia de Replicação | `_bmad-output/project-replication-guide.md` | Guia completo de setup (v1.1.0) |
| Integração CrewAI | `_bmad-output/crewai-integration-guide.md` | Integração CrewAI + BMAD |

### Agentes de Tecnologia

| Documento | Localização | Descrição |
|-----------|-------------|-----------|
| Implementação Docker | `_bmad-output/docker-skill-implementation.md` | Docs do agente Docker |
| Python 3.14 | `_bmad-output/python314-skill-implementation.md` | Docs Python 3.14 |
| PHP 8.4 | `_bmad-output/php84-skill-implementation.md` | Docs PHP 8.4 |
| PostgreSQL 18 | `_bmad-output/postgres18-skill-implementation.md` | Docs PostgreSQL 18 |
| Instalação RTK | `_bmad-output/rtk-installation-guide.md` | Setup do RTK |

### Deploy Coolify

| Documento | Localização | Descrição |
|-----------|-------------|-----------|
| Guia de Deploy | `_bmad-output/coolify-deploy-guide.md` | Visão geral, preparação, CLI (12 seções) |
| Deploy GitHub | `_bmad-output/coolify-github-deploy-guide.md` | Repo público, Deploy Key, GitHub App (9 seções) |
| Deploy Local | `_bmad-output/coolify-local-deploy-guide.md` | Docker Image, Dockerfile, Compose Empty (10 seções) |
| Script de Deploy | `_bmad-output/scripts/coolify-deploy.sh` | Automação CLI (Git + Docker Image) |

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

- **Documentação**: Veja `_bmad-output/` para guias detalhados
- **Issues**: Abra uma issue no repositório do projeto
- **BMAD Method**: https://github.com/bmadmethod/bmad-method

---

## Licença

Licença MIT — Veja `_bmad/core/config.yaml` para detalhes.

---

## Contribuidores

- **Hsantos** — Mantenedor do projeto
- **BMAD Method** — Autores do framework
