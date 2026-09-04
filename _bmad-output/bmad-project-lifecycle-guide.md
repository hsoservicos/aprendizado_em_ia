# Guia Completo: Ciclo de Vida de Projetos com BMAD + CrewAI

**Versão**: 1.1.0  
**Data**: 2026-09-04  
**Autor**: Hsantos  
**Público-alvo**: Operadores e membros da equipe

> **Antes de começar:** conclua o pré-flight em
> **`_bmad-output/getting-started.md`** (ambiente + os dois agentes + RTK +
> configuração do projeto). Este guia cobre a **execução** — a Trilha A
> (projeto novo). Para **projeto legado a modernizar**, comece pela Trilha B do
> `getting-started.md` (`/bmad-project-context` → `/bmad-code-review` →
> `/bmad-build`) e volte para as Fases 2–5 abaixo nas features maiores.

---

## Visão Geral

Este guia apresenta o **passo a passo completo** para criação de novos projetos utilizando o **BMAD Method** (Breakthrough Method for Agile Development) combinado com **CrewAI** (orquestração de agentes). Cobre todas as fases: desde a ideação até a entrega e deploy em produção.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CICLO DE VIDA DO PROJETO                             │
│                                                                         │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────┐ │
│  │  FASE 1  │──▶│  FASE 2  │──▶│  FASE 3  │──▶│  FASE 4  │──▶│FASE 5│ │
│  │ CLARIFY  │   │   PLAN   │   │  BUILD   │   │  REVIEW  │   │LEARN │ │
│  │          │   │          │   │          │   │          │   │      │ │
│  │ Ideação  │   │ Planej.  │   │ Código   │   │ Validac. │   │ Retro│ │
│  │ 30min    │   │ 1-2h     │   │ variável │   │ 30min    │   │30min │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────┘ │
│       │              │              │              │              │      │
│       ▼              ▼              ▼              ▼              ▼      │
│  brainstorming    PRD.md       código limpo   relatório     lições     │
│  forge-idea       SPINE.md     commits        aprovado      aprendidas │
│  idea-validation  UX specs     features       code review   próximo    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Pré-requisitos

### Ambiente de Desenvolvimento

| Ferramenta | Versão Mínima | Comando de Verificação | Propósito |
|------------|---------------|------------------------|-----------|
| Node.js | >= 20.12 | `node --version` | Runtime JavaScript |
| Python | >= 3.10, < 3.14 | `python3 --version` | Scripts BMAD |
| uv | >= 0.12 | `uv --version` | Gerenciador de pacotes Python |
| Git | Qualquer | `git --version` | Controle de versão |
| Agente de codificação | OpenCode >= 1.18 **e/ou** Claude Code >= 2.1 | `opencode --version` / `claude --version` | Roda os comandos `/bmad-*` |
| RTK | >= 0.47 | `rtk --version` | Compressão de tokens (ativo nos dois agentes) |
| ripgrep | >= 14.0 | `rg --version` | Busca rápida (recomendado) |
| CrewAI | >= 1.15 | `crewai --version` | Orquestração de agentes (opcional) |

### Instalação Rápida

```bash
# Instalar BMAD Method
npx bmad-method install

# Instalar CrewAI (opcional)
uv tool install crewai

# Verificar ambiente
rtk node --version && rtk python3 --version && uv --version
```

---

## FASE 1: CLARIFY — Ideação e Validação (30 min)

**Objetivo:** Transformar uma ideia vaga em um conceito validado e pronto para planejamento.

### Passo 1.1: Iniciar com `bmad-help`

```bash
# No OpenCode, execute:
/bmad-help
```

**O que acontece:**
- O agente analisa o estado atual do projeto (artefatos existentes)
- Recomenda o próximo skill a ser utilizado
- Apresenta o menu de opções disponível

**Saída esperada:** Orientação sobre por onde começar.

### Passo 1.2: Brainstorming Estruturado

```bash
/bmad-brainstorming
```

**O que acontece:**
- Sessão de brainstorming com 3 modos:
  - **Facilitador** — guia o usuário por técnicas criativas
  - **Creative Partner** — contribui com ideias próprias
  - **Ideate-for-me** — gera ideias automaticamente
- Usa um memlog para manter memória da sessão

**Saída esperada:**
- Arquivo `.memlog.md` com decisões registradas
- Documento de síntese com as ideias finalizadas

**Dicas:**
- Comece com uma ideia vaga, mesmo que incompleta
- O agente fará perguntas para refinar
- Não pule esta fase — ela evita retrabalho futuro

### Passo 1.3: Pressure-Test da Ideia

```bash
/bmad-forge-idea
```

**O que acontece:**
- Persona-driven interrogation da ideia
- Testa pressão sob diferentes perspectivas
- A ideia "endurece" ou "morre barato"

**Saída esperada:** Ideia validada ou pivot necessária.

### Passo 1.4: Validação Profunda (Opcional)

```bash
# Para pesquisa de mercado
/bmad-market-research

# Para pesquisa técnica
/bmad-technical-research

# Para pesquisa de domínio
/bmad-domain-research

# Para pesquisa profunda multi-tipo
/bmad-deep-recon
```

**Saída esperada:** Relatório de pesquisa com evidências.

### Checklist da Fase 1

- [ ] `bmad-help` executado e orientação recebida
- [ ] Brainstorming completo com memlog
- [ ] Ideia pressure-tested com `bmad-forge-idea`
- [ ] (Opcional) Pesquisa de mercado/técnica realizada
- [ ] Ideia validada e pronta para planejamento

---

## FASE 2: PLAN — Planejamento e Arquitetura (1-2 horas)

**Objetivo:** Criar todos os artefatos de planejamento necessários antes de escrever código.

### Passo 2.1: Criar PRD (Product Requirements Document)

```bash
/bmad-create-prd
```

**O que acontece:**
- Cria um PRD completo e estruturado
- Define: objetivos, escopo, funcionalidades, restrições
- Lista de user stories com critérios de aceitação

**Saída esperada:** Arquivo PRD.md em `_bmad-output/`

**Dicas:**
- Seja específico sobre o que NÃO fazer (anti-features)
- Defina métricas de sucesso mensuráveis
- Inclua exemplos concretos de uso

### Passo 2.2: Definir Arquitetura

```bash
/bmad-architecture
```

**O que acontece:**
- Cria o **ARCHITECTURE-SPINE.md** — decisions invariantes
- Define: paradigma, limites, regras de dependência
- Registra decisões como AD-n (Architecture Decisions)

**Saída esperada:** `ARCHITECTURE-SPINE.md` com decisões registradas

**Dicas:**
- Preferir tecnologia "boring" (testada e confiável)
- Cada decisão deve ter justificativa
- O spine deve ser mínimo — apenas o que impede divergência

### Passo 2.3: Criar UX Design

```bash
/bmad-ux
```

**O que acontece:**
- Elicita (não impõe) a visão do usuário
- Produz dois contratos:
  - **DESIGN.md** — identidade visual (cores, tipografia, componentes)
  - **EXPERIENCE.md** — arquitetura de informação, interações, acessibilidade
- Gera mocks HTML das telas principais (opcional)

**Saída esperada:** `DESIGN.md` + `EXPERIENCE.md` em pasta de run

**Dicas:**
- Form-factor primeiro: mobile, web, desktop, multi-superfície
- Jornadas com protagonista nomeado (ex: "Maria, mãe de 3 filhos")
- Feche a superfície antes de fechar a IA

### Passo 2.4: Criar Épicas e Histórias

```bash
/bmad-create-epics-and-stories
```

**O que acontece:**
- Quebra o PRD em épicos e user stories
- Cada story tem critérios de aceitação claros
- Histórias são estimadas e priorizadas

**Saída esperada:** Lista de épicos e stories em formato rastreável

### Passo 2.5: Planejar Sprint

```bash
/bmad-sprint-planning
```

**O que acontece:**
- Valida prontidão para sprint
- Gera status de rastreamento
- Define o que será implementado no sprint atual

**Saída esperada:** Sprint status com stories selecionadas

### Checklist da Fase 2

- [ ] PRD criado com escopo definido
- [ ] Arquitetura definida com decisions registradas
- [ ] UX design completo (DESIGN.md + EXPERIENCE.md)
- [ ] Épicos e stories criados com AC
- [ ] Sprint planejado com stories selecionadas

---

## FASE 3: BUILD — Implementação (variável)

**Objetivo:** Implementar o código de forma limpa, testada e seguindo a arquitetura definida.

### Passo 3.1: Implementar por Story

```bash
/bmad-build
```

**O que acontece:**
- Recebe a intent do usuário (feature, bug, refactor)
- Segue workflow: clarificar → planejar → implementar → revisar → apresentar
- Respeita arquitetura e convenções do projeto
- Código limpo, testado, pronto para commit

**Fluxo interno do bmad-build:**
```
1. Clarify/Route  → Entende o que fazer
2. Plan           → Define abordagem
3. Implement      → Escreve código
4. Review         → Revisa próprio código
5. Present        → Apresenta resultado
```

**Dicas:**
- Implemente uma story por vez
- Cada implementação deve ser um commit atômico
- Não pule a fase de review interno

### Passo 3.2: Build Autônomo (Opcional)

```bash
/bmad-build-auto
```

**O que acontece:**
- Loop de build não-assistido
- Implementa múltiplas stories automaticamente
- Útil para sprints grandes com stories bem definidas

**Cuidado:** Use apenas quando as stories estão muito bem especificadas.

### Passo 3.3: Invocar Agentes de Tecnologia

Para projetos com stack específica:

```bash
# Docker (Dockerfile, Compose, segurança)
/bmad-agent-docker

# Python 3.14 (free-threading, t-strings, subinterpreters)
/bmad-agent-python314

# PHP 8.4 (Property Hooks, Asymmetric Visibility)
/bmad-agent-php84

# PostgreSQL 18 (AIO, Skip Scan, UUIDv7, pgvector)
/bmad-agent-postgres18
```

**Dicas:**
- Use agentes de tecnologia para decisões de stack
- Eles conhecem as melhores práticas das versões mais recentes
- Combine com `bmad-build` para implementação

### Passo 3.4: Usar CrewAI para Automação

Para projetos quebeneficiam de múltiplos agentes trabalhando em paralelo:

```bash
# Criar projeto CrewAI
crewai create crew meu-projeto

# Configurar agentes e tasks
cd meu-projeto
crewai install

# Executar crew
crewai run
```

**Integração BMAD-CrewAI:**

```python
from bmad_crewai_bridge import BMADBridge

bridge = BMADBridge(project_root="/caminho/do/projeto")

# Usar skills BMAD via CrewAI
skills = bridge.list_skills()
output = bridge.render_skill("bmad-build")
```

**Casos de uso para CrewAI:**
- Múltiplos agentes revisando código simultaneamente
- Pipelines de CI/CD automatizados
- Geração de documentação em paralelo
- Análise de código por múltiplas perspectivas

### Checklist da Fase 3

- [ ] Cada story implementada como commit atômico
- [ ] Código segue a arquitetura definida
- [ ] Testes escritos antes ou durante implementação
- [ ] Agentes de tecnologia consultados para decisões de stack
- [ ] (Opcional) CrewAI configurado para automação

---

## FASE 4: REVIEW — Validação e Qualidade (30 min)

**Objetivo:** Garantir que o código está correto, seguro e pronto para produção.

### Passo 4.1: Code Review Adversarial

```bash
/bmad-code-review
```

**O que acontece:**
- Review usando subagents paralelos
- Múltiplas camadas de análise simultâneas
- Triagem estruturada dos resultados

**Saída esperada:** Relatório de review com:
- Issues categorizados (crítico, alto, médio, baixo)
- Riscos identificados
- Sugestões de melhoria
- Referências ao código fonte

**Dicas:**
- Execute após cada sprint significativo
- Não ignore issues críticos — corrija antes de prosseguir
- Use o relatório para aprender padrões

### Passo 4.2: Checkpoint Preview (Opcional)

```bash
/bmad-checkpoint-preview
```

**O que acontece:**
- Revisão assistida por LLM com humano no loop
- Foca atenção onde importa
- Valida testes e comportamento esperado

### Passo 4.3: Validação Técnica

```bash
# Validação de Docker
/bmad-docker

# Validação de PRD
/bmad-validate-prd

# Revisão editorial
/bmad-review
```

### Passo 4.4: Testes Automatizados

```bash
# Gerar testes E2E
/bmad-qa-generate-e2e-tests
```

**Dicas:**
- Execute testes antes de cada merge
- Mantenha cobertura mínima de 80%
- Testes E2E para fluxos críticos do usuário

### Checklist da Fase 4

- [ ] Code review adversarial completo
- [ ] Todos os issues críticos corrigidos
- [ ] Testes passando (unit + E2E)
- [ ] Validação de Docker/Compose OK
- [ ] Documentação atualizada

---

## FASE 5: LEARN — Retrospectiva e Entrega (30 min)

**Objetivo:** Extrair lições aprendidas e preparar para a próxima iteração.

### Passo 5.1: Retrospectiva

```bash
/bmad-retrospective
```

**O que acontece:**
- Lê diff completo do épico, commits, spec, sprint status
- Analisa evidências em 5 fases:
  1. **Gather** — coleta dados
  2. **Analyze** — analisa padrões
  3. **Discuss** — discute descobertas
  4. **Decide** — define ações
  5. **Finalize** — renderiza veredicto

**Saída esperada:** `RETROSPECTIVE.md` com:
- Descobertas com referências às fontes
- Itens de ação
- Veredicto de aceitação (accepted / accepted-with-open-items / rejected)

**Dicas:**
- Seja honesto sobre o que deu errado
- Foque em ações concretas para o próximo sprint
- Registre lições no `docs/` para referência futura

### Passo 5.2: Documentar Projeto

```bash
/bmad-project-context
```

**O que acontece:**
- Atualiza AGENTS.md com contexto do projeto
- Registra erros observados como pitfall lines
- Prepara o repositório para novos agentes

### Passo 5.3: Deploy em Produção

```bash
# Deploy via Coolify (GUI)
# Siga: _bmad-output/coolify-deploy-guide.md

# Deploy via CLI
./_bmad-output/scripts/coolify-deploy.sh \
  --name meu-app \
  --repo https://github.com/org/repo \
  --port 3000
```

**Dicas:**
- Sempre deployar em staging antes de produção
- Verificar health checks após deploy
- Monitorar logs nas primeiras horas

### Checklist da Fase 5

- [ ] Retrospectiva completa com veredicto
- [ ] Lições documentadas em `docs/`
- [ ] AGENTS.md atualizado
- [ ] Deploy executado com sucesso
- [ ] Health checks passando
- [ ] Monitoramento configurado

---

## Fluxo de Trabalho Diário

### Rotina do Operador

```
08:30  Verificar status do sprint
       /bmad-sprint-planning (status view)

09:00  Selecionar story do dia
       Definir escopo da implementação

09:15  Implementar story
       /bmad-build

11:30  Review interno
       /bmad-code-review (após cada feature)

12:00  Commit e push
       git add . && git commit -m "feat: ..."

14:00  Continuar implementação
       /bmad-build (próxima story)

16:30  Review final do dia
       /bmad-code-review

17:00  Documentar progresso
       Atualizar sprint status

17:30  Preparar para próximo dia
       /bmad-sprint-planning (next steps)
```

### Comandos Rápidos de Referência

| Ação | Comando |
|------|---------|
| Iniciar projeto | `/bmad-help` |
| Brainstormar | `/bmad-brainstorming` |
| Testar ideia | `/bmad-forge-idea` |
| Criar PRD | `/bmad-create-prd` |
| Definir arquitetura | `/bmad-architecture` |
| Criar UX | `/bmad-ux` |
| Quebrar em stories | `/bmad-create-epics-and-stories` |
| Planejar sprint | `/bmad-sprint-planning` |
| Implementar código | `/bmad-build` |
| Build autônomo | `/bmad-build-auto` |
| Revisar código | `/bmad-code-review` |
| Retrospectiva | `/bmad-retrospective` |
| Docker | `/bmad-agent-docker` |
| Python 3.14 | `/bmad-agent-python314` |
| PHP 8.4 | `/bmad-agent-php84` |
| PostgreSQL 18 | `/bmad-agent-postgres18` |

---

## Regras de Ouro

### 1. Nunca Pule Fases

```
❌  Ideia → Código → Deploy
✅  Ideia → PRD → Arquitetura → UX → Stories → Código → Review → Deploy
```

### 2. Documente Tudo

```
❌  Código sem contexto
✅  Cada commit referencia story/issue
✅  Cada decisão registrada no architecture spine
✅  Cada retrospectiva documenta lições
```

### 3. Revise Sempre

```
❌  Code after code after code
✅  Código → Review → Fix → Merge
✅  Use /bmad-code-review após cada feature significativa
```

### 4. Uma Story por Vez

```
❌  Implementar 5 stories ao mesmo tempo
✅  Selecionar → Implementar → Review → Próxima
```

### 5. Technology Agents Primeiro

```
❌  Decidir stack sem consultar especialistas
✅  /bmad-agent-docker para decisões de container
✅  /bmad-agent-python314 para decisões de Python
✅  /bmad-agent-php84 para decisões de PHP
✅  /bmad-agent-postgres18 para decisões de banco
```

---

## Erros Comuns e Como Evitar

| Erro | Consequência | Como Evitar |
|------|-------------|-------------|
| Pular brainstorming | Ideia mal definida, retrabalho | Sempre executar Fase 1 completa |
| PRD incompleto | Features faltando, scope creep | Usar bmad-create-prd com cuidado |
| Arquitetura sem spine | Código divergente, manutenção difícil | Registrar decisions no ARCHITECTURE-SPINE.md |
| Código sem review | Bugs em produção, dívida técnica | Executar bmad-code-review regularmente |
| Deploy sem testes | Falhas em produção | Testar em staging primeiro |
| Sem retrospectiva | Repetir mesmos erros | Documentar lições em cada sprint |

---

## Referências

| Documento | Localização | Descrição |
|-----------|-------------|-----------|
| Primeiros Passos / Onboarding | `_bmad-output/getting-started.md` | Pré-flight + trilhas A (novo) e B (legado) |
| Guia de Replicação | `_bmad-output/project-replication-guide.md` | Preparar a máquina em detalhe |
| Guia de Deploy Coolify | `_bmad-output/coolify-deploy-guide.md` | Visão geral do deploy |
| Deploy GitHub | `_bmad-output/coolify-github-deploy-guide.md` | Repositórios GitHub |
| Deploy Local | `_bmad-output/coolify-local-deploy-guide.md` | Deploy sem Git |
| CrewAI Integration | `_bmad-output/crewai-integration-guide.md` | Integração BMAD-CrewAI |
| Tools Registry | `_bmad-output/tools-registry.md` | Inventário de ferramentas |
| AGENTS.md | `/AGENTS.md` | Instruções do projeto |

---

**Próximo passo:** Executar `/bmad-help` para iniciar o primeiro projeto following this lifecycle.
