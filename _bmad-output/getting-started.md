# Primeiros Passos — Onboarding do Repositório

**Versão**: 1.0.0
**Data**: 2026-09-04
**Autor**: Hsantos
**Público-alvo**: Membro da equipe que vai usar este repositório para **implementar um projeto novo** ou **modernizar/atualizar um projeto legado**.

---

## Para que serve este guia

Este é o **ponto de entrada único**. Ele coloca você do zero até a primeira tarefa
produtiva, seja qual for a trilha:

| Trilha | Quando usar | Vai para |
|--------|-------------|----------|
| **A — Projeto Novo (Greenfield)** | Não existe código ainda; ideia/produto a ser criado | [Trilha A](#trilha-a--projeto-novo-greenfield) |
| **B — Projeto Legado (Brownfield)** | Já existe uma base de código a ser modernizada, corrigida ou estendida | [Trilha B](#trilha-b--projeto-legado-brownfield) |

Os dois **agentes de codificação** — **OpenCode** e **Claude Code** — são
equivalentes: todo comando `/bmad-*`, toda skill e toda ferramenta funcionam
igual nos dois. Escolha um e siga.

> **Ordem obrigatória:** faça os **Passos 0 a 5** uma única vez. Só depois entre
> na Trilha A ou B. Não pule fases.

> **Precisa do passo a passo detalhado, explicado sem jargão?** Depois do
> pré-flight, use o **Manual de Implementação**:
> **`_bmad-output/implementation-playbook.md`** — conceitos, comandos exatos,
> entradas/saídas esperadas, Definition of Done e FAQ, para **qualquer nível de
> conhecimento**, cobrindo projeto novo (Parte A) e legado (Parte B).

---

## Passo 0 — Pré-requisitos da máquina

Ambiente exigido (instale o que faltar — o script automatizado faz tudo):

| Ferramenta | Versão | Verificar |
|------------|--------|-----------|
| Node.js | >= 20.12 | `node --version` |
| Python | >= 3.10, < 3.14 | `python3 --version` |
| uv | >= 0.12 | `uv --version` |
| Git | >= 2.30 | `git --version` |
| GitHub CLI (`gh`) | qualquer | `gh --version` |
| ripgrep (`rg`) | >= 14.0 | `rg --version` |
| RTK | >= 0.47 | `rtk --version` |
| CrewAI | >= 1.15 (opcional) | `crewai version` |
| Agente | OpenCode >= 1.18 **e/ou** Claude Code >= 2.1 | `opencode --version` / `claude --version` |

**Setup automatizado (recomendado):**

```bash
# Linux (Ubuntu/Debian)
chmod +x _bmad-output/scripts/install-linux.sh
./_bmad-output/scripts/install-linux.sh --project-dir "$PWD"

# Windows (PowerShell como Administrador)
powershell -ExecutionPolicy Bypass -File _bmad-output/scripts/install-windows.ps1 -ProjectDir "C:\projetos\app"
```

O script instala toolchain + os dois agentes, roda `npx bmad-method install` e
conecta o RTK aos dois agentes. Setup manual detalhado:
**`_bmad-output/project-replication-guide.md`**.

---

## Passo 1 — Obter o repositório

```bash
# Novo projeto a partir deste material
git clone https://github.com/hsoservicos/aprendizado_em_ia.git meu-projeto
cd meu-projeto

# OU, projeto legado: adicione este material ao repo existente
# (copie _bmad/, .agents/, .claude/, .opencode/, AGENTS.md, CLAUDE.md
#  e _bmad-output/scripts/, depois rode `npx bmad-method install`)
```

Crie uma branch de trabalho antes de qualquer alteração:

```bash
git checkout -b feat/onboarding-setup
```

---

## Passo 2 — Instalar / atualizar o BMAD

```bash
npx bmad-method install
```

Detecta instalação existente e oferece update. Regenera as duas árvores de skills
(`.agents/skills/` e `.claude/skills/`) e os comandos do OpenCode.

---

## Passo 3 — Verificar toolchain + os dois agentes + RTK

```bash
# Toolchain
node --version && python3 --version && uv --version && git --version \
  && rg --version | head -1 && rtk --version && gh --version | head -1

# Agentes
opencode --version ; claude --version

# Skills idênticas nos dois agentes
diff -rq .agents/skills .claude/skills && echo "OK: árvores idênticas"

# RTK conectado aos dois agentes
rtk init --show
#   esperado: [ok] OpenCode: plugin installed
#             [ok] settings.json: RTK hook configured   (global)
#   + o repo já traz o hook de projeto em .claude/settings.json

# Se algo faltar, conecte o RTK aos dois de uma vez (uma vez por máquina):
rtk init -g --auto-patch          # hook global do Claude Code
rtk init -g --auto-patch --opencode  # plugin do OpenCode
```

Checklist rápido: **`_bmad-output/scripts/installation-validation-report.md`**.

---

## Passo 4 — Configurar o projeto

Edite os overrides (o `_bmad/config.toml` é gerado pelo instalador — **não edite**):

**`_bmad/custom/config.toml`** — configuração da equipe, **commitada**:

```toml
[core]
project_name = "meu-projeto"
document_output_language = "Português do Brasil"   # ou "English"
output_folder = "_bmad-output"
```

**`_bmad/config.user.toml`** — pessoal, **no gitignore**:

```toml
[core]
user_name = "SeuNome"
communication_language = "Português do Brasil"

[modules.bmm]
user_skill_level = "intermediate"   # beginner | intermediate | advanced
```

Configure as chaves de API do agente (Anthropic / OpenAI conforme o uso) e
confirme o idioma de comunicação.

---

## Passo 5 — Escolher o agente e abrir

```bash
opencode      # OU
claude
```

Dentro do agente, o **primeiro comando é sempre**:

```
/bmad-help
```

Ele lê o estado atual do repositório e recomenda o próximo passo. A partir daqui,
siga a trilha correspondente.

---

## Trilha A — Projeto Novo (Greenfield)

Você tem uma ideia e nenhum código. Siga o **ciclo de vida de 5 fases**:

| # | Fase | Skills | Saída |
|---|------|--------|-------|
| 1 | **Clarify** | `/bmad-help` → `/bmad-brainstorming` → `/bmad-forge-idea` | Ideia validada |
| 2 | **Plan** | `/bmad-create-prd` → `/bmad-architecture` → `/bmad-ux` → `/bmad-create-epics-and-stories` | PRD + Arquitetura + UX + Stories |
| 3 | **Build** | `/bmad-sprint-planning` → `/bmad-build` (uma story por vez) | Código funcionando |
| 4 | **Review** | `/bmad-code-review` → `/bmad-qa-generate-e2e-tests` | Código validado |
| 5 | **Learn** | `/bmad-retrospective` → deploy (Coolify) | Lições + Produção |

**Mudanças pequenas** podem ir direto para `/bmad-build`.

📖 **Passo a passo detalhado, sem jargão, com exemplos e checklists de qualidade:**
**`_bmad-output/implementation-playbook.md`** → Parte A.
Referência de operação e rotina diária: **`_bmad-output/bmad-project-lifecycle-guide.md`**.

---

## Trilha B — Projeto Legado (Brownfield)

Já existe código. **Antes de modernizar, capture o contexto** — nunca comece a
alterar às cegas.

### B.1 — Linha de base segura

```bash
git status                       # árvore limpa
git checkout -b feat/modernizacao
```

### B.2 — Capturar o contexto do repositório legado

```
/bmad-project-context
```

Audita/gera o bloco de instruções do repo (`AGENTS.md` / `CLAUDE.md`): stack,
comandos de build/test, convenções, e registra "pitfalls" observados. É o que faz
os agentes trabalharem bem num código que eles não conhecem.
> Alias: `bmad-document-project`.

### B.3 — Diagnóstico de qualidade da base atual

```
/bmad-code-review
```

Gera uma linha de base de bugs e dívida técnica **antes** de mexer. Repita depois
de cada bloco de modernização para medir o progresso.

### B.4 — Enquadrar o trabalho

| Situação | Caminho |
|----------|---------|
| Correção/ajuste pontual | direto `/bmad-build` |
| Feature nova sobre o legado | `/bmad-create-prd` (escopo) → `/bmad-architecture` (só o delta) → `/bmad-create-epics-and-stories` → `/bmad-build` |
| Migração de stack (Docker, Python 3.14, PHP 8.4, PostgreSQL 18) | `/bmad-agent-docker` / `/bmad-agent-python314` / `/bmad-agent-php84` / `/bmad-agent-postgres18` para decidir, depois `/bmad-build` |
| Mudança de rumo no meio do sprint | `/bmad-correct-course` |

### B.5 — Modernizar em ciclos curtos

```
Selecionar escopo → /bmad-build → /bmad-code-review → commit → repetir
```

Uma unidade de mudança por vez. Cada commit referencia a story/issue.
Ao fechar um épico: `/bmad-retrospective`.

📖 **Passo a passo detalhado do trabalho em legado** (mapear, diagnosticar,
estratégia por incremento, testes de caracterização, ciclos curtos):
**`_bmad-output/implementation-playbook.md`** → Parte B. As Fases 2–5 do
`bmad-project-lifecycle-guide.md` valem para features maiores em legado.

---

## Checklist de Onboarding (copie e marque)

```
Pré-flight (uma vez)
[ ] Passo 0  Pré-requisitos instalados (node, python, uv, git, gh, rg, rtk)
[ ] Passo 1  Repositório clonado/integrado + branch de trabalho criada
[ ] Passo 2  npx bmad-method install executado
[ ] Passo 3  diff .agents/skills .claude/skills == idêntico
[ ] Passo 3  rtk init --show → OpenCode plugin + Claude hook OK
[ ] Passo 4  _bmad/custom/config.toml (projeto) e config.user.toml (pessoal) ajustados
[ ] Passo 4  Chaves de API do agente configuradas
[ ] Passo 5  Agente aberto (opencode | claude) e /bmad-help executado

Trilha A — Novo projeto
[ ] Fase 1 Clarify concluída (ideia validada)
[ ] Fase 2 Plan concluída (PRD + Arquitetura + UX + Stories)
[ ] Fase 3 Build — stories implementadas uma a uma
[ ] Fase 4 Review — code review + testes E2E
[ ] Fase 5 Learn — retrospectiva + deploy

Trilha B — Projeto legado
[ ] B.1 Linha de base git limpa + branch
[ ] B.2 /bmad-project-context executado (AGENTS.md/CLAUDE.md do legado gerado)
[ ] B.3 /bmad-code-review — linha de base de qualidade registrada
[ ] B.4 Trabalho enquadrado (pontual | feature | migração | correct-course)
[ ] B.5 Modernização em ciclos curtos build → review → commit
```

---

## Referências

| Documento | Localização | Para quê |
|-----------|-------------|----------|
| **Este guia** | `_bmad-output/getting-started.md` | Primeiros passos (você está aqui) |
| **Manual de Implementação** | `_bmad-output/implementation-playbook.md` | Passo a passo detalhado e sem jargão — Parte A (novo) e Parte B (legado) |
| Guia de Replicação | `_bmad-output/project-replication-guide.md` | Preparar a máquina em detalhe |
| Ciclo de Vida (5 fases) | `_bmad-output/bmad-project-lifecycle-guide.md` | Referência de operação e rotina diária |
| Registro de Ferramentas | `_bmad-output/tools-registry.md` | Inventário de tudo que está instalado |
| Integração RTK | `_bmad-output/rtk-installation-guide.md` | RTK nos dois agentes |
| Instruções do projeto | `AGENTS.md` (OpenCode) / `CLAUDE.md` (Claude Code) | Contrato dos agentes |
| Scripts de instalação | `_bmad-output/scripts/README.md` | Automação Linux/Windows |
| Deploy | `_bmad-output/coolify-deploy-guide.md` | Entrega em produção |

---

**Próximo passo:** conclua os Passos 0–5, depois abra o agente e execute `/bmad-help`.
