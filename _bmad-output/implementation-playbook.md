# Manual de Implementação — Passo a Passo para Projetos Novos e Legados

**Versão**: 1.0.0
**Data**: 2026-09-04
**Autor**: Hsantos
**Público-alvo**: **Qualquer membro da equipe** — inclusive quem não tem formação
ou afinidade com Engenharia de Software. Ao seguir este manual você consegue
conduzir a construção de um projeto **novo** ou a modernização de um projeto
**legado** de forma **profissional, moderna e eficiente**.

---

## Sumário

1. [Como usar este manual](#1-como-usar-este-manual)
2. [Conceitos essenciais (sem jargão)](#2-conceitos-essenciais-sem-jargão)
3. [Antes de tudo: o pré-flight](#3-antes-de-tudo-o-pré-flight)
4. [Princípios de um projeto profissional](#4-princípios-de-um-projeto-profissional)
5. [PARTE A — Projeto Novo (Greenfield)](#parte-a--projeto-novo-greenfield)
6. [PARTE B — Projeto Legado (Brownfield)](#parte-b--projeto-legado-brownfield)
7. [Tabela de decisão rápida](#7-tabela-de-decisão-rápida)
8. [Padrões de qualidade (Definition of Done)](#8-padrões-de-qualidade-definition-of-done)
9. [Fluxo de trabalho diário e convenções](#9-fluxo-de-trabalho-diário-e-convenções)
10. [Solução de problemas (FAQ)](#10-solução-de-problemas-faq)
11. [Glossário de comandos](#11-glossário-de-comandos)
12. [Referências](#12-referências)

---

## 1. Como usar este manual

Este projeto usa o **BMAD Method**: um conjunto de *skills* (assistentes
especializados) que você chama por comandos `/bmad-*` dentro de um **agente de
codificação** (OpenCode **ou** Claude Code — os dois funcionam igual). Cada skill
conduz você por uma etapa do trabalho fazendo perguntas e gerando documentos ou
código.

**Você não precisa saber programar para começar.** O agente escreve o código; o
seu papel é: descrever o que precisa, responder às perguntas, revisar o que foi
gerado e aprovar. Este manual ensina exatamente o que digitar, o que esperar de
volta e o que fazer quando algo dá errado.

### Escolha o seu caminho

| A sua situação | Vá para |
|----------------|---------|
| Vou **criar um sistema/produto do zero**, ainda não há código | **[PARTE A](#parte-a--projeto-novo-greenfield)** |
| Já **existe um sistema** e preciso corrigir, atualizar, adicionar coisas ou modernizá-lo | **[PARTE B](#parte-b--projeto-legado-brownfield)** |
| Não tenho certeza | Leia a [Tabela de decisão rápida](#7-tabela-de-decisão-rápida) |

### Como ler

- Faça **uma etapa por vez, na ordem**. Cada etapa tem: **Objetivo**, **O que
  fazer**, **O que o agente vai pedir**, **Resultado esperado**, **Checklist de
  qualidade** e **Erros comuns**.
- Onde aparecer `>` seguido de um comando, digite-o **dentro do agente**
  (OpenCode/Claude Code). Onde aparecer um bloco `bash`, rode no **terminal**.
- Não pule etapas. As etapas puladas viram retrabalho mais caro depois.

---

## 2. Conceitos essenciais (sem jargão)

Leia uma vez. Volte aqui sempre que um termo aparecer.

| Termo | O que é, em uma frase | Analogia |
|-------|-----------------------|----------|
| **Greenfield** | Projeto novo, "terreno baldio" — nada construído ainda. | Construir uma casa em um lote vazio. |
| **Brownfield** | Projeto legado — já existe um sistema em uso que será mudado. | Reformar uma casa habitada sem derrubá-la. |
| **PRD** (Product Requirements Document) | Documento que descreve **o que** o produto faz e **por quê**, não *como*. | A planta e o memorial descritivo da casa. |
| **Arquitetura / Spine** | As decisões técnicas centrais e invariáveis (linguagem, banco, como as partes conversam). O "spine" é a lista enxuta dessas decisões. | A estrutura (fundação, pilares) que tudo o resto respeita. |
| **Épico** | Um bloco grande de trabalho com um objetivo. | "Reformar a cozinha". |
| **Story (história)** | Uma fatia pequena e entregável de um épico, com um resultado verificável. | "Instalar a pia da cozinha". |
| **Critério de aceite** | A definição objetiva de "esta story está pronta". | "A torneira abre, fecha e não vaza". |
| **Code review** | Revisão crítica do código em busca de bugs e problemas antes de considerar pronto. | Vistoria da obra antes de liberar o cômodo. |
| **Testes** | Código que verifica automaticamente se o sistema faz o que deveria. | Ligar todas as tomadas para ver se funcionam. |
| **Teste de caracterização** | Teste que "fotografa" o comportamento atual de um sistema legado antes de mexer, para garantir que você não quebrou nada. | Fotografar cada cômodo antes da reforma. |
| **Retrospectiva** | Conversa estruturada no fim de um épico: o que funcionou, o que repetir, o que evitar. | Reunião pós-obra para a próxima ficar melhor. |
| **Branch** | Uma "cópia paralela" do projeto onde você trabalha sem afetar a versão principal. | Uma bancada separada para montar a peça antes de instalar. |
| **Commit** | Um ponto de salvamento com descrição do que mudou. | Anotar no diário de obra cada etapa concluída. |
| **PR (Pull Request)** | Pedido para juntar o seu branch na versão principal, geralmente após revisão. | Pedir aprovação do engenheiro para integrar a peça à casa. |
| **Definition of Done** | A lista fixa de condições que **toda** entrega precisa cumprir. | O checklist de vistoria final, igual para todo cômodo. |
| **Deploy** | Publicar a versão para uso real (produção). | Entregar as chaves e liberar a casa para morar. |
| **Skill BMAD** | Um assistente especializado que você chama por `/bmad-...`. | Um profissional específico: eletricista, encanador, arquiteto. |
| **Technology Agent** | Skill especialista em uma tecnologia (Docker, Python 3.14, PHP 8.4, PostgreSQL 18). | O especialista que você consulta antes de decidir material/técnica. |
| **RTK** | Ferramenta que comprime a saída dos comandos para o agente gastar menos "memória". Já vem ligada nos dois agentes. | Um resumo automático dos relatórios longos. |

---

## 3. Antes de tudo: o pré-flight

Faça **uma única vez** por máquina/projeto, na ordem. O detalhe completo está em
**`_bmad-output/getting-started.md`**; o resumo:

```bash
# 0. Toolchain + os dois agentes (script faz tudo)
./_bmad-output/scripts/install-linux.sh --project-dir "$PWD"      # Linux
# Windows: powershell -ExecutionPolicy Bypass -File _bmad-output/scripts/install-windows.ps1

# 1. Repositório + branch de trabalho
git clone https://github.com/hsoservicos/aprendizado_em_ia.git meu-projeto
cd meu-projeto
git checkout -b feat/setup

# 2. Instalar/atualizar o BMAD
npx bmad-method install

# 3. Verificar
diff -rq .agents/skills .claude/skills && echo "skills OK"   # árvores idênticas
rtk init --show                                              # RTK nos 2 agentes
node --version && python3 --version && uv --version && git --version && rtk --version

# 4. Configurar o projeto
#    _bmad/custom/config.toml   -> project_name, document_output_language, output_folder
#    _bmad/config.user.toml     -> user_name, communication_language, user_skill_level
#    + chaves de API do agente (Anthropic / OpenAI conforme o uso)

# 5. Abrir o agente
opencode      # ou: claude
```

Dentro do agente, o **primeiro comando é sempre**:

```
> /bmad-help
```

Ele lê o estado atual do repositório e recomenda o próximo passo.

---

## 4. Princípios de um projeto profissional

Estes seis princípios são o que separa um resultado amador de um profissional.
Eles valem para **projeto novo e legado**.

1. **Nunca pule fases.** Ideia → Requisitos → Arquitetura → UX → Stories → Código
   → Review → Entrega. Pular etapa não economiza tempo: transfere o custo (maior)
   para depois.
2. **Uma story por vez.** Selecione → implemente → revise → só então a próxima.
   Trabalhar em cinco frentes ao mesmo tempo gera retrabalho e bugs.
3. **Revise sempre.** Rode `/bmad-code-review` depois de cada feature relevante.
   Código sem revisão é dívida técnica com juros.
4. **Documente as decisões.** Cada commit referencia a story/issue. Cada decisão
   técnica fica no *architecture spine*. Cada épico termina em retrospectiva.
5. **Teste.** Nenhuma entrega é "pronta" sem teste automático que a comprove. Em
   legado, primeiro escreva testes de caracterização, depois mude.
6. **Consulte os especialistas primeiro.** Antes de decidir stack ou técnica,
   chame o Technology Agent correspondente (`/bmad-agent-docker`,
   `/bmad-agent-python314`, `/bmad-agent-php84`, `/bmad-agent-postgres18`).

> **Regra de ouro do commit pequeno:** se você não consegue descrever a mudança
> em uma frase, ela está grande demais — quebre em partes menores.

---

## PARTE A — Projeto Novo (Greenfield)

> **Quando usar:** não existe código ainda. Você tem uma ideia, um problema a
> resolver ou um produto a criar.
>
> **Tempo típico:** Fase 1 ~30 min · Fase 2 ~1–2 h · Fase 3 variável ·
> Fase 4 ~30 min · Fase 5 ~30 min.
>
> **Exemplo usado abaixo:** *"um app web simples para uma equipe registrar e
> acompanhar despesas de projeto"*.

### Visão geral das 5 fases

```
FASE 1          FASE 2              FASE 3         FASE 4          FASE 5
CLARIFY   ───▶  PLAN         ───▶  BUILD    ───▶  REVIEW    ───▶  LEARN
ideia           PRD + Arqui-        código        code review     retrospectiva
validada        tetura + UX +       funcionando   + testes        + deploy
                Stories
```

---

### A0 — Preparar o repositório

**Objetivo:** ter um lugar limpo e versionado para trabalhar.

**O que fazer** (terminal):

```bash
cd meu-projeto
git status                       # deve estar limpo
git checkout -b feat/mvp         # branch de trabalho
mkdir -p docs                    # conhecimento do projeto
```

Confirme no `_bmad/custom/config.toml` que `project_name` e
`document_output_language` estão como você quer.

**Resultado esperado:** `git status` limpo, você está no branch `feat/mvp`.

**Erros comuns:** trabalhar direto no branch `main`; esquecer de configurar o
idioma (os documentos saem no idioma errado).

---

### A1 — Fase CLARIFY: transformar a ideia em conceito validado

#### A1.1 — Orientação

- **Objetivo:** entender por onde começar.
- **O que fazer:** `> /bmad-help`
- **O que o agente vai pedir:** nada; ele analisa o repositório.
- **Resultado esperado:** uma recomendação de próximo passo (provavelmente
  `bmad-brainstorming`).

#### A1.2 — Brainstorming estruturado

- **Objetivo:** explorar o problema e as possibilidades antes de decidir.
- **O que fazer:** `> /bmad-brainstorming`
- **O que o agente vai pedir:** o tema/assunto, e o modo (facilitador, parceiro
  ou autônomo). Descreva em 2–3 frases o problema: *"Equipes lançam despesas em
  planilhas soltas; ninguém sabe o total por projeto em tempo real."*
- **Resultado esperado:** um documento em `_bmad-output/` com ideias organizadas,
  agrupadas e uma seleção das mais promissoras.
- **Checklist de qualidade:** há pelo menos 2–3 direções distintas consideradas;
  a ideia escolhida resolve o problema declarado.
- **Erros comuns:** pular direto para a solução favorita sem explorar; brief vago
  ("quero um app de finanças").

#### A1.3 — Pressure-test da ideia

- **Objetivo:** achar as fraquezas da ideia agora, quando é barato.
- **O que fazer:** `> /bmad-forge-idea`
- **O que o agente vai pedir:** a ideia escolhida. Ele a interroga por personas
  (cético, usuário, investidor…).
- **Resultado esperado:** a ideia **refinada** ou a constatação de que ela não se
  sustenta (o que também é um bom resultado — falhou barato).
- **Checklist de qualidade:** você sabe responder "para quem é", "qual dor
  resolve", "por que agora", "o que acontece se ninguém usar".

#### A1.4 — (Opcional) Pesquisa mais profunda

- **Quando:** mercado desconhecido, decisão técnica arriscada, domínio novo.
- **O que fazer:** `> /bmad-deep-recon` (escolha o tipo: market, technical,
  domain, competitive…).
- **Resultado esperado:** um resumo citado e arquivado que as próximas fases
  consomem sem reprocessar.

> ✅ **Saída da Fase 1:** uma ideia validada, com público, dor e proposta claros.

---

### A2 — Fase PLAN: planejar antes de construir

#### A2.1 — PRD (o que o produto faz e por quê)

- **Objetivo:** um documento único que todos entendem, sem ambiguidade.
- **O que fazer:** `> /bmad-create-prd`
- **O que o agente vai pedir:** objetivo do produto, usuários, jobs-to-be-done,
  funcionalidades essenciais (MVP) vs. desejáveis, restrições, o que está **fora**
  de escopo.
- **Resultado esperado:** `_bmad-output/.../PRD.md` com problema, objetivos,
  personas, requisitos funcionais e não-funcionais, escopo e não-escopo.
- **Checklist de qualidade:** cada requisito é testável ("o usuário consegue X");
  o não-escopo está explícito; nada de "etc.".
- **Erros comuns:** PRD que descreve *como* (tecnologia) em vez de *o quê*;
  escopo aberto (tudo é "essencial").
- **Validar:** `> /bmad-prd` (modo validação) ou rode o checklist que a skill
  oferece.

#### A2.2 — Arquitetura (as decisões técnicas centrais)

- **Objetivo:** fixar as poucas decisões das quais tudo o resto depende.
- **O que fazer:** `> /bmad-architecture`
- **Antes:** se houver decisão de container, linguagem ou banco, chame o
  Technology Agent (`/bmad-agent-docker`, `/bmad-agent-postgres18`, etc.) e leve
  a recomendação para a conversa.
- **O que o agente vai pedir:** requisitos não-funcionais (escala, prazo,
  time-size), preferências e restrições.
- **Resultado esperado:** um **architecture spine** — lista enxuta de invariantes
  (ex.: "Frontend: HTML+JS simples; Backend: Python + FastAPI; Banco:
  PostgreSQL 18; Deploy: Docker no Coolify").
- **Checklist de qualidade:** cada decisão tem uma justificativa de 1 linha ligada
  a valor de negócio; tecnologia "chata" e estável preferida à moda.
- **Erros comuns:** over-engineering (microserviços para um app interno de 5
  usuários); nenhuma decisão registrada.

#### A2.3 — UX (as telas e o fluxo)

- **Objetivo:** definir a experiência antes de existir código.
- **O que fazer:** `> /bmad-ux`
- **O que o agente vai pedir:** telas principais, o que o usuário faz em cada
  uma, tom visual.
- **Resultado esperado:** `DESIGN.md` + `EXPERIENCE.md` (padrões, telas-chave,
  fluxo).
- **Checklist de qualidade:** todo requisito do PRD tem uma tela ou fluxo
  correspondente; o caminho principal ("cadastrar despesa") tem no máximo 3
  passos.

#### A2.4 — Épicos e Stories (quebrar o trabalho)

- **Objetivo:** transformar o plano em fatias pequenas e rastreáveis.
- **O que fazer:** `> /bmad-create-epics-and-stories`
- **Pré-requisito:** PRD + Arquitetura prontos (a skill valida isso).
- **O que o agente vai pedir:** confirmação do escopo; ele propõe épicos e as
  stories dentro deles.
- **Resultado esperado:** `epics.md` + stories, cada uma com **critérios de
  aceite** objetivos.
- **Checklist de qualidade:** cada story cabe em ~1 dia; tem critério de aceite
  verificável; não depende de outra story ainda não feita.
- **Erros comuns:** stories gigantes ("fazer o backend"); critérios de aceite
  vagos ("funcionar bem").

#### A2.5 — Planejar o sprint

- **Objetivo:** confirmar que dá para começar a construir.
- **O que fazer:** `> /bmad-sprint-planning`
- **Resultado esperado:** um arquivo de status do sprint com as stories
  priorizadas e um "portão de prontidão" verde.

> ✅ **Saída da Fase 2:** PRD + Architecture Spine + DESIGN/EXPERIENCE + Épicos e
> Stories + sprint pronto.

---

### A3 — Fase BUILD: construir, uma story por vez

#### A3.1 — Implementar uma story

- **Objetivo:** código funcionando para **uma** story, seguindo a arquitetura.
- **O que fazer:** `> /bmad-build` e informe qual story.
- **O que o agente faz:** clareia e roteia → planeja → implementa → revisa →
  apresenta. Ele escreve o código, cria/atualiza testes e mostra o diff.
- **O seu papel:** responder dúvidas de escopo, revisar o diff, pedir ajustes,
  aprovar.
- **Resultado esperado:** código + testes passando + a story marcada como feita
  no status do sprint.
- **Checklist de qualidade (Definition of Done — ver §8):** testes passam;
  critérios de aceite atendidos; sem `TODO` solto; diff pequeno e coeso.
- **Erros comuns:** aceitar um diff enorme sem entender; pedir "faça tudo de uma
  vez".

#### A3.2 — Registrar o progresso (commit)

```bash
git add -A
git commit -m "feat: cadastro de despesa (story 1.2)"
```

Uma story ≈ um (ou poucos) commits, cada um descrito em uma frase.

#### A3.3 — Consultar Technology Agents quando necessário

| Decisão | Comando |
|---------|---------|
| Dockerfile / Compose / segurança de container | `> /bmad-agent-docker` |
| Python 3.14 (free-threading, t-strings, subinterpreters) | `> /bmad-agent-python314` |
| PHP 8.4 (Property Hooks, Asymmetric Visibility) | `> /bmad-agent-php84` |
| PostgreSQL 18 (índices, UUIDv7, pgvector, tuning) | `> /bmad-agent-postgres18` |

#### A3.4 — (Opcional) Build autônomo

- **Quando:** várias stories bem definidas e de baixo risco, sem necessidade de
  decisão humana a cada passo.
- **O que fazer:** `> /bmad-build-auto`
- **Cuidado:** revise os commits gerados ao final como se fossem seus.

> ✅ **Saída da Fase 3:** todas as stories do sprint implementadas, com testes,
> commitadas.

---

### A4 — Fase REVIEW: garantir qualidade

#### A4.1 — Code review adversarial

- **Objetivo:** encontrar bugs e problemas antes do usuário.
- **O que fazer:** `> /bmad-code-review`
- **Resultado esperado:** uma lista **triada** de achados (bug / simplificação /
  eficiência), do mais grave ao menos.
- **O seu papel:** para cada achado — corrigir agora, agendar (virar story), ou
  descartar com justificativa. Não deixe achado grave em aberto.
- **Aplicar correções:** rode `/bmad-build` para os itens que viram mudança, ou
  peça à própria review para aplicar.

#### A4.2 — (Opcional) Checkpoint preview

- **Quando:** a mudança é grande ou sensível e você quer um passo a passo
  explicado do que mudou.
- **O que fazer:** `> /bmad-checkpoint-preview`

#### A4.3 — Testes automatizados de ponta a ponta

- **Objetivo:** provar que os fluxos principais funcionam de verdade.
- **O que fazer:** `> /bmad-qa-generate-e2e-tests` e indique a feature.
- **Resultado esperado:** testes E2E versionados que rodam no CI/local.
- **Checklist de qualidade:** o caminho principal do PRD tem teste E2E; os testes
  passam localmente.

> ✅ **Saída da Fase 4:** achados críticos resolvidos, testes E2E passando.

---

### A5 — Fase LEARN: aprender e entregar

#### A5.1 — Retrospectiva do épico

- **O que fazer:** `> /bmad-retrospective` e indique o épico.
- **Resultado esperado:** documento com o que o épico produziu, verificação
  contra as fontes e um **veredito de aceite** (aceito / aceito com ressalvas /
  não aceito).

#### A5.2 — Documentar o projeto

- **O que fazer:** `> /bmad-project-context` (atualiza `AGENTS.md`/`CLAUDE.md` com
  o estado real: stack, comandos de build/test, convenções).

#### A5.3 — Deploy em produção

- **O que fazer:** siga **`_bmad-output/coolify-deploy-guide.md`** (visão geral),
  ou `coolify-github-deploy-guide.md` / `coolify-local-deploy-guide.md` conforme
  a origem. Script: `_bmad-output/scripts/coolify-deploy.sh`.
- **Checklist de qualidade:** deploy testado em staging antes de produção;
  rollback conhecido.

> ✅ **Saída da Fase 5:** épico aceito, projeto documentado, versão em produção.

---

### Checklist final — PARTE A

```
[ ] A0  Branch de trabalho criado, config do projeto conferida
[ ] A1  Ideia validada (brainstorming + forge-idea)
[ ] A2  PRD.md aprovado e validado
[ ] A2  Architecture spine registrado (com Technology Agents consultados)
[ ] A2  DESIGN.md + EXPERIENCE.md
[ ] A2  Épicos + Stories com critérios de aceite; sprint pronto (portão verde)
[ ] A3  Cada story: /bmad-build -> testes passam -> commit descrito em 1 frase
[ ] A4  /bmad-code-review -> achados críticos resolvidos
[ ] A4  Testes E2E do caminho principal passando
[ ] A5  /bmad-retrospective -> veredito de aceite
[ ] A5  /bmad-project-context -> AGENTS.md/CLAUDE.md atualizados
[ ] A5  Deploy validado em staging -> produção
```

---

## PARTE B — Projeto Legado (Brownfield)

> **Quando usar:** já existe um sistema (em uso ou não) que precisa ser
> corrigido, atualizado, estendido ou modernizado.
>
> **Regra número um:** **não quebre o que funciona.** Toda mudança em legado é
> feita em ciclos pequenos, com rede de segurança (testes) e sempre reversível.

### Visão geral

```
B0 entrar    B1 mapear      B2 diagnos-   B3 planejar    B4 executar     B5 conso-
com          o legado       ticar         a moderni-     em ciclos       lidar
segurança    (contexto)     (qualidade)   zação          curtos
```

---

### B0 — Entrar com segurança

**Objetivo:** poder mexer sem risco de perder trabalho ou derrubar produção.

**O que fazer** (terminal):

```bash
git clone <repo-do-legado> legado && cd legado
git status                          # tem que estar limpo
git checkout -b feat/modernizacao   # todo trabalho vai aqui
```

Integre o material BMAD ao repositório legado (copie `_bmad/`, `.agents/`,
`.claude/`, `.opencode/`, `AGENTS.md`, `CLAUDE.md` e `_bmad-output/scripts/`,
depois rode `npx bmad-method install`). Faça o **pré-flight** da [§3](#3-antes-de-tudo-o-pré-flight).

**Entenda o mínimo do que roda hoje** — anote:
- Como se sobe o sistema localmente? (comando de build / start)
- Como se roda os testes existentes (se houver)?
- Onde ele está publicado e como se faz deploy hoje?

**Erros comuns:** trabalhar no `main`; começar a alterar antes de saber como
rodar e testar o sistema.

---

### B1 — Mapear o legado (capturar o contexto)

**Objetivo:** dar ao agente (e a você) um retrato fiel do sistema: linguagem,
frameworks, estrutura de pastas, comandos, convenções e armadilhas.

- **O que fazer:** `> /bmad-project-context`
  (alias: `bmad-document-project`)
- **O que ele faz:** varre o repositório e escreve/atualiza o bloco de instruções
  em `AGENTS.md` / `CLAUDE.md` — stack detectada, comandos de build/test,
  convenções do código, e "pitfalls" (erros que agentes cometem nesse repo).
- **Resultado esperado:** `AGENTS.md`/`CLAUDE.md` com uma seção que descreve o
  sistema **como ele é hoje**.
- **O seu papel:** ler e corrigir imprecisões. Este documento guia todo o resto.
- **Checklist de qualidade:** o comando para subir o sistema e o comando para
  rodar os testes estão documentados e você os executou com sucesso.

---

### B2 — Diagnosticar (linha de base de qualidade)

**Objetivo:** saber o estado de saúde do código **antes** de mexer, para
priorizar e para medir progresso depois.

- **O que fazer:** `> /bmad-code-review`
  (opcionalmente aponte para as áreas que você vai modernizar primeiro)
- **Resultado esperado:** lista triada de bugs, riscos de segurança e dívida
  técnica.
- **Priorize nesta ordem:**
  1. **Segurança** (dados expostos, injeção, credenciais no código)
  2. **Bugs que afetam o usuário**
  3. **Bloqueadores da modernização** (o que impede atualizar a stack)
  4. **Dívida técnica geral** (duplicação, código morto)
- **Registre a linha de base:** guarde esse relatório em `_bmad-output/`. Você vai
  rodar de novo depois de cada bloco para comparar.

---

### B3 — Planejar a modernização

**Objetivo:** decidir **o que** modernizar, **em que ordem** e **em fatias
seguras** — sem um "big bang".

#### B3.1 — Escolher a estratégia por incremento

| Situação | Caminho |
|----------|---------|
| Correção pontual / ajuste pequeno | Vá direto para **B4** com `/bmad-build`. |
| Feature nova sobre o legado | `> /bmad-create-prd` (só a feature) → `> /bmad-architecture` (só o **delta**, respeitando o que já existe) → `> /bmad-create-epics-and-stories` → **B4**. |
| Atualização de stack (ex.: Python 3.9 → 3.14, PHP 7 → 8.4, Postgres 12 → 18, "dockerizar") | Consulte o Technology Agent (`/bmad-agent-python314`, `/bmad-agent-php84`, `/bmad-agent-postgres18`, `/bmad-agent-docker`) para o plano de migração; quebre em stories pequenas; **B4**. |
| Reescrita de um módulo grande | Padrão **incremental (strangler)**: crie o novo ao lado do antigo, migre um fluxo por vez, remova o antigo só quando o novo cobrir tudo. Uma story por fluxo migrado. |
| Mudança de rumo no meio do trabalho | `> /bmad-correct-course` |

#### B3.2 — Rede de segurança antes de mudar comportamento

Se a área que você vai mexer **não tem testes**, crie **testes de
caracterização** primeiro: `> /bmad-qa-generate-e2e-tests` apontando para o
comportamento atual. Eles "fotografam" o que o sistema faz hoje. Só então mude o
código — se um teste quebrar, você saberá exatamente o que mudou.

#### B3.3 — Definir o "pronto" de cada incremento

Use a mesma [Definition of Done da §8](#8-padrões-de-qualidade-definition-of-done),
mais dois itens específicos de legado:
- o comportamento pré-existente continua idêntico (testes de caracterização
  passam), **ou** a mudança de comportamento é intencional e documentada;
- há caminho de rollback (o incremento pode ser revertido sozinho).

---

### B4 — Executar em ciclos curtos

**Objetivo:** modernizar em passos pequenos, cada um verificado e reversível.

**O loop, para cada incremento:**

```
1. Selecionar UM incremento pequeno (uma story / um fluxo / um arquivo)
2. (se faltar rede) gerar testes de caracterização da área
3. > /bmad-build            — implementar o incremento
4. rodar os testes          — os antigos + os novos passam
5. > /bmad-code-review      — revisar só o que mudou
6. corrigir achados críticos
7. git commit -m "refactor: <1 frase> (incremento N)"
8. repetir
```

**Regras do ciclo:**
- **Um incremento por vez.** Se o diff passou de ~alguns arquivos, você agrupou
  demais.
- **Verde antes de seguir.** Não comece o próximo incremento com teste quebrado.
- **Commits pequenos e descritos.** `refactor:`, `fix:`, `feat:`, `chore:`,
  `test:` no início da mensagem.
- **Não misture** refatoração (mudar forma, mesmo comportamento) com feature
  (mudar comportamento) no mesmo commit.

**A cada bloco concluído:** rode `/bmad-code-review` na área toda e compare com a
linha de base da [B2](#b2--diagnosticar-linha-de-base-de-qualidade). O número de
achados deve cair.

---

### B5 — Consolidar e entregar

- **Retrospectiva:** `> /bmad-retrospective` — o que a modernização entregou,
  verificado contra evidências, com veredito de aceite.
- **Atualizar o retrato:** `> /bmad-project-context` de novo — o `AGENTS.md` /
  `CLAUDE.md` agora descreve o sistema **modernizado**.
- **Deploy gradual:** publique por partes se possível (feature flags, canário).
  Siga os guias Coolify em `_bmad-output/`. Tenha o rollback à mão.
- **Comunique:** registre no PR o antes/depois (achados da review, versões de
  stack, testes adicionados).

---

### Checklist final — PARTE B

```
[ ] B0  Clone + branch feat/modernizacao; pré-flight feito
[ ] B0  Sei subir o sistema e rodar os testes existentes (executei)
[ ] B1  /bmad-project-context -> AGENTS.md/CLAUDE.md descreve o legado atual
[ ] B2  /bmad-code-review -> linha de base salva em _bmad-output/
[ ] B2  Achados priorizados (segurança > bugs > bloqueadores > dívida)
[ ] B3  Estratégia por incremento definida (pontual | feature | stack | strangler)
[ ] B3  Áreas sem teste -> testes de caracterização criados
[ ] B4  Loop por incremento: build -> testes verdes -> review -> commit pequeno
[ ] B4  A cada bloco: review comparada à linha de base (achados caindo)
[ ] B5  /bmad-retrospective -> veredito de aceite
[ ] B5  /bmad-project-context -> docs refletem o sistema modernizado
[ ] B5  Deploy gradual validado + rollback conhecido
```

---

## 7. Tabela de decisão rápida

| A minha situação… | O que fazer |
|-------------------|-------------|
| Tenho só uma ideia, nada construído | **PARTE A** desde a Fase 1 (`/bmad-help` → `/bmad-brainstorming`) |
| Ideia já validada, quero planejar | **PARTE A** a partir de A2 (`/bmad-create-prd`) |
| Já tenho PRD e arquitetura, quero construir | **PARTE A** a partir de A3 (`/bmad-sprint-planning` → `/bmad-build`) |
| Preciso corrigir 1 bug num sistema existente | **PARTE B**: B0 → B1 → `/bmad-build` (com teste de caracterização se faltar) |
| Preciso adicionar uma feature a um sistema existente | **PARTE B** B0–B2, depois B3.1 linha "feature nova" |
| Preciso atualizar a versão de linguagem/banco / dockerizar | **PARTE B** B0–B2, depois B3.1 linha "atualização de stack" + Technology Agent |
| Preciso reescrever um módulo grande | **PARTE B** com padrão incremental (strangler), B3.1 |
| Mudou o objetivo no meio do caminho | `/bmad-correct-course` |
| Não sei em que fase estou | `/bmad-help` (ele lê o repositório e recomenda) |
| Um comando falhou | [§10 — FAQ](#10-solução-de-problemas-faq) |

---

## 8. Padrões de qualidade (Definition of Done)

**Nenhuma entrega — nova ou de legado — é "pronta" sem cumprir TODOS os itens:**

```
[ ] Faz o que os critérios de aceite da story pedem (verificado, não presumido)
[ ] Testes automáticos cobrindo o comportamento novo/alterado — e passam
[ ] Testes pré-existentes continuam passando
[ ] Code review executada; achados graves resolvidos
[ ] Sem código morto, sem `TODO`/`FIXME` solto, sem segredo no código
[ ] Diff pequeno e coeso; uma responsabilidade por commit
[ ] Mensagem de commit descreve a mudança em 1 frase, referencia a story/issue
[ ] Decisões técnicas relevantes registradas (architecture spine / PR)
[ ] Documentação afetada atualizada (README, AGENTS.md/CLAUDE.md, guias)
[ ] Roda localmente do zero seguindo só o que está documentado
```

Itens extras **para legado**:

```
[ ] Comportamento pré-existente preservado (testes de caracterização passam)
    OU mudança de comportamento intencional e documentada
[ ] O incremento é reversível sozinho (rollback conhecido)
```

---

## 9. Fluxo de trabalho diário e convenções

### Rotina sugerida do operador

Detalhe completo em **`_bmad-output/bmad-project-lifecycle-guide.md`**
(seção "Fluxo de Trabalho Diário"). Resumo:

```
Início do dia   /bmad-sprint-planning (ver status) -> escolher UMA story
Manhã           /bmad-build (implementar) -> testes -> commit
Meio do dia     /bmad-code-review (após a feature) -> corrigir
Tarde           próxima story: /bmad-build -> testes -> commit
Fim do dia      /bmad-code-review final -> atualizar status do sprint
```

### Convenções de branch

| Tipo | Nome do branch |
|------|----------------|
| Nova feature | `feat/<curto-descritivo>` |
| Correção | `fix/<curto-descritivo>` |
| Modernização de legado | `feat/modernizacao-<área>` ou `refactor/<área>` |

### Convenções de commit (prefixos)

| Prefixo | Quando |
|---------|--------|
| `feat:` | comportamento novo visível ao usuário |
| `fix:` | correção de bug |
| `refactor:` | muda a forma do código, **não** o comportamento |
| `test:` | adiciona/ajusta testes |
| `docs:` | só documentação |
| `chore:` | build, dependências, configuração |

Uma frase, no imperativo: `fix: impedir despesa com valor negativo (story 2.3)`.

### Renderizar uma skill (se precisar manualmente)

```bash
# Claude Code
uv run _bmad/scripts/render_skill.py --project-root "$PWD" --skill .claude/skills/<skill>
# OpenCode
uv run _bmad/scripts/render_skill.py --project-root "$PWD" --skill .agents/skills/<skill>
```

Nunca execute os arquivos de workflow diretamente. Se falhar (ou faltar `uv`),
reporte a saída e **pare**.

---

## 10. Solução de problemas (FAQ)

| Sintoma | Causa provável | O que fazer |
|---------|----------------|-------------|
| `uv: command not found` | PATH não carregou | `source ~/.bashrc` ou reabra o terminal; confirme `~/.local/bin` no PATH |
| `rtk: command not found` | idem | idem; ou reinstale via `project-replication-guide.md` |
| Skill não encontrada / `/bmad-...` não existe | BMAD desatualizado ou árvores divergentes | `npx bmad-method install`; depois `diff -rq .agents/skills .claude/skills` |
| Render de skill: `HALT: ...` | `uv` ausente ou entrada de render faltando | Reporte a saída e pare; verifique `uv --version`; rode `npx bmad-method install` |
| Árvores de skills diferentes (`diff` acusou) | edição manual em uma só | `npx bmad-method install` regenera as duas |
| Agente não comprime a saída (RTK) | hook não carregado | `rtk init --show`; se faltar, `rtk init -g --auto-patch` (Claude) e `--opencode` (plugin); reinicie o agente |
| Preciso da saída crua de um comando | RTK está resumindo | prefixe: `RTK_DISABLED=1 <comando>` |
| Documentos saem no idioma errado | config de idioma | ajuste `document_output_language` em `_bmad/custom/config.toml` e `communication_language` em `_bmad/config.user.toml` |
| `git push` pede usuário/senha | credencial não configurada | `gh auth login` e `gh auth setup-git` |
| O agente propôs um diff enorme | escopo grande demais | peça para dividir; implemente 1 story/1 arquivo por vez |
| Testes do legado não rodam | comando/deps ausentes | documente e resolva no B1 **antes** de mexer no código |
| Não sei qual é o próximo passo | — | `> /bmad-help` |

---

## 11. Glossário de comandos

| Comando | Para quê | Fase / Parte |
|---------|----------|--------------|
| `/bmad-help` | Orientar, recomendar o próximo passo | qualquer |
| `/bmad-brainstorming` | Explorar o problema e ideias | A1 |
| `/bmad-forge-idea` | Pressure-test da ideia | A1 |
| `/bmad-deep-recon` | Pesquisa profunda (mercado, técnica, domínio…) | A1 (opcional) |
| `/bmad-create-prd` | Criar o PRD | A2 / B3 |
| `/bmad-architecture` | Definir o architecture spine | A2 / B3 |
| `/bmad-ux` | DESIGN.md + EXPERIENCE.md | A2 |
| `/bmad-create-epics-and-stories` | Quebrar em épicos e stories | A2 / B3 |
| `/bmad-sprint-planning` | Prontidão e status do sprint | A2 / A3 |
| `/bmad-build` | Implementar uma story/incremento | A3 / B4 |
| `/bmad-build-auto` | Loop de build autônomo | A3 (opcional) |
| `/bmad-code-review` | Revisão adversarial de código | A4 / B2 / B4 |
| `/bmad-checkpoint-preview` | Passo a passo explicado de uma mudança | A4 (opcional) |
| `/bmad-qa-generate-e2e-tests` | Gerar testes E2E / de caracterização | A4 / B3 |
| `/bmad-correct-course` | Mudança de rumo no meio do sprint | qualquer |
| `/bmad-retrospective` | Retrospectiva do épico + veredito | A5 / B5 |
| `/bmad-project-context` | Gerar/atualizar `AGENTS.md`/`CLAUDE.md` do repo | A5 / B1 / B5 |
| `/bmad-agent-docker` | Especialista Docker | A2–A3 / B3–B4 |
| `/bmad-agent-python314` | Especialista Python 3.14 | A2–A3 / B3–B4 |
| `/bmad-agent-php84` | Especialista PHP 8.4 | A2–A3 / B3–B4 |
| `/bmad-agent-postgres18` | Especialista PostgreSQL 18 | A2–A3 / B3–B4 |

---

## 12. Referências

| Documento | Localização | Para quê |
|-----------|-------------|----------|
| Primeiros Passos / Onboarding | `_bmad-output/getting-started.md` | Pré-flight + seleção de trilha |
| **Este manual** | `_bmad-output/implementation-playbook.md` | Passo a passo detalhado (novo + legado) |
| Guia do Ciclo de Vida | `_bmad-output/bmad-project-lifecycle-guide.md` | Referência de operação e rotina diária |
| Guia de Replicação | `_bmad-output/project-replication-guide.md` | Preparar a máquina em detalhe |
| Registro de Ferramentas | `_bmad-output/tools-registry.md` | Inventário do que está instalado |
| Integração CrewAI | `_bmad-output/crewai-integration-guide.md` | Orquestração multi-agente |
| Deploy Coolify | `_bmad-output/coolify-deploy-guide.md` (+ github / local) | Entrega em produção |
| Instruções dos agentes | `AGENTS.md` (OpenCode) / `CLAUDE.md` (Claude Code) | Contrato de trabalho dos agentes |

---

**Próximo passo:** identifique a sua situação na
[Tabela de decisão rápida](#7-tabela-de-decisão-rápida) e comece pela
**PARTE A** ou **PARTE B**. Na dúvida, abra o agente e rode `> /bmad-help`.
