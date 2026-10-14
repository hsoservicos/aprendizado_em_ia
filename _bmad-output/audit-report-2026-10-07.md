# Relatório de Auditoria Completa — 2026-10-07

**Escopo**: `/home/hsantos/app` (hub de ferramentas BMAD) + inventário dos projetos
que consomem a mesma ferramenta em `/home/hsantos`.
**Executado por**: OpenCode (mimo-v2.6-pro)
**Estado do repo**: `main`, limpo antes da auditoria; 108 arquivos modificados +
5 novos ao final (relatório, Impeccable, docs).

---

## 1. Resumo executivo

| # | Achado | Severidade | Ação |
|---|--------|------------|------|
| 1 | CrewAI CLI corrompido (`Failed find package 'crewai' in tool environment`) | **Crítica** | ✅ Reparado — `uv tool install crewai --force` → v1.15.25 |
| 2 | BMAD 6.12.0 → **6.12.1** disponível | Média | ✅ Atualizado via `--action quick-update` |
| 3 | **O instalador do BMAD apagou 4 skills customizadas** durante o update | **Crítica** | ✅ Restauradas via `git checkout`; procedimento de recuperação documentado |
| 4 | Docs desatualizadas: `AGENTS.md` dizia Python 3.12 e "57 skills"; real é 3.14.4 e 55 | Média | ✅ Corrigidas (`AGENTS.md`, `CLAUDE.md`, `tools-registry.md`) |
| 5 | Docs listavam `bmad-docker`/`python314`/`php84`/`postgres18` como instalados — **foram removidos em `d6e8139` (2026-09)** | Média | ✅ Corrigidas + nota de remoção |
| 6 | `tools-registry.md` com 12 versões de ferramentas defasadas | Baixa | ✅ Atualizado (v1.3.3 → v1.4.0) |
| 7 | `markdown-studio-live` com BMAD **6.11.0** (2 versões atrás dos irmãos) | Média | ⚠️ Relatado (fora do escopo de atualização) |
| 8 | `markdown-studio-live`: `package.json` posterior ao `package-lock.json` | Média | ⚠️ Relatado |
| 9 | Impeccable ausente em 3 de 4 projetos | Alta | ✅ Instalado e documentado em todos |

---

## 2. Projeto local — `/home/hsantos/app`

### 2.1 Estrutura (auditoria)

| Item | Estado |
|------|--------|
| Git | `main`, rastreando `origin/main`, limpo |
| Último commit antes | `6544458` (2026-09-09) — ~1 mês sem commits |
| `_bmad/` | core + bmm 6.12.1, 21 v6-shims, scripts (render/validate/docsync/memlog) |
| `_bmad-output/` | 18 artefatos de documentação + scripts de deploy |
| Skills | **55** (54 `bmad-*` + `impeccable`) em `.agents/skills/` e `.claude/skills/` |
| Paridade de skills | ✅ `diff` limpo entre as duas árvores |
| Comandos OpenCode | **55** em `.opencode/commands/` — mapeamento 1:1 sem órfãos |
| Harness Claude Code | `.claude/settings.json` (allow-list + hook RTK) + `settings.local.json` (hooks Impeccable) |
| Estado do projeto | **greenfield** — nenhuma aplicação, só infraestrutura de ferramentas |

### 2.2 Ferramentas — versões antes/depois

| Ferramenta | Registrado | Real (pré-auditoria) | Após auditoria |
|------------|-----------|----------------------|----------------|
| Node.js | v24.20.0 | v24.21.0 | v24.21.0 |
| npm | 12.0.2 | 12.2.0 | 12.2.0 |
| Python | 3.12.3 (AGENTS.md: "3.12") | **3.14.4** | 3.14.4 |
| uv | 0.12.9 | 0.12.23 | 0.12.23 |
| Git | 2.43.0 | 2.53.0 | 2.53.0 |
| GitHub CLI | 2.73.0 / 2.99.0 | 2.102.0 | 2.102.0 |
| ripgrep | 14.1.1 | 15.2.0 | 15.2.0 |
| RTK | 0.47.0 / 0.48.0 | 0.51.0 | 0.51.0 |
| CrewAI | 1.15.18 | **❌ corrompido** | **1.15.25** ✅ |
| OpenCode | 1.18.27 | 1.18.35 | 1.18.35 |
| Claude Code | 2.1.260 | 2.1.289 | 2.1.289 |
| BMAD Method | 6.11.0 (módulos) / 6.12.0 | 6.12.0 | **6.12.1** |
| Impeccable CLI | — | ausente | **4.1.0** (engine v0.1.11) |

### 2.3 Ações executadas

1. **CrewAI** — o venv em `~/.local/share/uv/tools/crewai` estava inconsistente
   (o shim `/home/hsantos/.local/bin/crewai` apontava para um pacote inexistente).
   `uv tool install crewai --force` reinstalou 100+ pacotes e restaurou o binário.
2. **BMAD 6.12.0 → 6.12.1** — `npx bmad-method@6.12.1 install --action quick-update
   --tools claude-code,opencode -y`. Módulos `core` e `bmm` atualizados, 50 skills
   oficiais atualizadas, configurações preservadas.
3. **Restauração de skills customizadas** — ver §2.4.
4. **Impeccable** — instalação completa, ver §4.
5. **Documentação** — `AGENTS.md`, `CLAUDE.md` e `tools-registry.md` corrigidos e
   estendidos.

### 2.4 Regressão detectada e corrigida: o instalador do BMAD apaga skills customizadas

O `--action quick-update` **removeu 32 arquivos** correspondentes a 4 skills que
não constam no manifesto oficial do BMAD:

```
.agents/skills/bmad-angular21/          .claude/skills/bmad-angular21/
.agents/skills/bmad-java21/             .claude/skills/bmad-java21/
.agents/skills/bmad-agent-angular21/    .claude/skills/bmad-agent-angular21/
.agents/skills/bmad-agent-java21/       .claude/skills/bmad-agent-java21/
.opencode/commands/bmad-{angular21,java21,agent-angular21,agent-java21}.md
```

Foram restauradas com `git checkout`. **Procedimento de recuperação** documentado
em `AGENTS.md` (seção *Keeping it installed across BMAD updates*) e em
`tools-registry.md` §8 (*After every `npx bmad-method install`*).

> Mesma classe de risco afeta o `impeccable` (também fora do manifesto BMAD).
> Após qualquer update do BMAD: `npx impeccable install -y --providers=claude,opencode
> --scope=project --force` + `cp -r .opencode/skills/impeccable .agents/skills/impeccable`.

### 2.5 Documentação corrigida

| Arquivo | Correções |
|---------|-----------|
| `AGENTS.md` | 57→55 skills; Python 3.12→3.14.4; Node v24.20→v24.21; tabela de Entry Points (remove docker/python314/php84/postgres18, adiciona angular21/java21/impeccable); nova seção *Impeccable* completa; aviso de regressão do instalador |
| `CLAUDE.md` | 57→55 skills; paridade de slash commands com `/impeccable`; seção *Impeccable* nos específicos do Claude Code |
| `tools-registry.md` | v1.3.3→v1.4.0; 12 versões de ferramentas; §2.2 skills (55); §2.4 manifest (50 entradas); §3.1 comandos custom; §3.2 Claude Code; **nova §3.3 Impeccable**; §7 log (10 entradas novas); §8 checklist pós-update; §10 pré-requisitos |
| `.gitignore` | Bloco `# impeccable-ignore-start/end` (mantém `config.json`, `design.json`, `critique/`, `surfaces/`, `live/config.json`) |

---

## 3. Projetos que consomem a ferramenta (`/home/hsantos`)

### 3.1 Inventário comparativo

| Projeto | BMAD | Skills `.agents`/`.claude` | Paridade | Stack | Impeccable (pré) |
|---------|------|---------------------------|----------|-------|------------------|
| **app** (hub) | ~~6.12.0~~ → **6.12.1** | 55 / 55 | ✅ | greenfield (sem app) | ❌ → ✅ |
| **servicetec** | **6.12.1** | 51 / 51 | ✅ | HTML/CSS/JS + nginx | ✅ completo |
| **hsoservicos** | 6.12.0 | 29 / 29 | ✅ | Django 6.1.1 + htmx | ❌ → ✅ |
| **markdown-studio-live** | **6.11.0** ⚠️ | 57 / 57 | ✅ | Node/Vite, Mermaid, Monaco | ⚠️ parcial → ✅ |
| **sound-music-app** | — (não usa) | — | — | vanilla JS + Python | ❌ → ✅ |

### 3.2 Oportunidades de aprimoramento do hub (`app`)

Extraídas do que os projetos irmãos já aprenderam:

| # | Oportunidade | Origem | Prioridade |
|---|--------------|--------|------------|
| 1 | **Detector como gate de CI** — `npx impeccable detect --json` com exit code 2 falhando o build | terminalskills / doc oficial | Alta |
| 2 | **`PRODUCT.md` + `DESIGN.md` como artefatos de primeira classe** do fluxo BMAD (Track A e Track B) | servicetec, markdown-studio-live | Alta |
| 3 | **Receita de "projeto legado"** formalizada: `detect` (baseline) → `document` → `critique` → `audit` → `harden` → `polish` | servicetec (§ UX/UI proposta) | Alta |
| 4 | **Registro de exceções de design** (`npx impeccable ignores add-value`) versionado, para não "consertar" marcas intencionais | doc oficial | Média |
| 5 | **Checklist de pós-update do BMAD** automatizado como script (`_bmad/scripts/post-update-restore.sh`) | regressão de hoje | Alta |
| 6 | **`markdown-studio-live` desatualizado** (BMAD 6.11.0 + lockfile defasado) — candidato a `quick-update` | auditoria | Média |
| 7 | **Padronizar `.claude/settings.local.json` gitignored** em todos os projetos (hoje só `app` e `markdown-studio-live`) | auditoria | Média |
| 8 | **Skill de Angular 21 / Java 21** poderiam virar módulo `_bmad/custom/` para sobreviverem a updates | regressão de hoje | Média |
| 9 | **hsoservicos** tem 210 achados `low-contrast` — candidato a `/impeccable harden` | baseline Impeccable | Alta |
| 10 | **sound-music-app** não usava harness de agente — o Impeccable criou `.claude/`, `.opencode/`, `.agents/`; considerar adotar AGENTS.md/CLAUDE.md | instalação de hoje | Baixa |

---

## 4. Impeccable — implementação e instalação

### 4.1 O que é

Skill de design para agentes de codificação + detector determinístico de
anti-padrões de UI, de **Paul Bakaus** (Apache-2.0). Evoluiu do
`frontend-design` da Anthropic. Resolve o "AI slop": Inter em tudo, gradientes
roxo→azul, cards dentro de cards, texto cinza sobre fundo colorido, easing
elástico.

- **Site**: <https://impeccable.style> · **Repo**: `pbakaus/impeccable`
- **npm**: `impeccable@4.1.0` · **engine**: v0.1.11 (binário auto-contido)
- **1 skill + 24 comandos + 61 regras determinísticas** (sem LLM, sem API key)
- **Subagents Claude Code**: asset-producer, documenter, finish-reviewer,
  manual-edit-applier

### 4.2 O que foi instalado (por projeto)

| Componente | app | hsoservicos | markdown-studio-live | sound-music-app |
|------------|-----|-------------|----------------------|-----------------|
| Skill em `.claude/skills/impeccable/` | ✅ | ✅ | ✅ | ✅ |
| Skill em `.opencode/skills/impeccable/` | ✅ | ✅ | ✅ | ✅ |
| Skill espelhada em `.agents/skills/impeccable/` | ✅ | ✅ | ✅ | ✅ |
| Subagents `.claude/agents/impeccable-*.md` (4) | ✅ | ✅ | ✅ | ✅ |
| Wrapper `.opencode/commands/impeccable.md` | ✅ | ✅ | ✅ | ✅ |
| Hooks `.claude/settings.local.json` | ✅ | ✅ | ✅ | ✅ |
| Bloco `.gitignore` impeccable | ✅ | ✅ | ✅ (já tinha) | ✅ |
| Documentação em AGENTS.md/AGENT.md | ✅ | ✅ | ✅ | ✅ |

Comando de instalação usado:

```bash
npx impeccable install -y --providers=claude,opencode --scope=project
```

Hooks instalados (Claude Code, via `.claude/settings.local.json`):
`SessionStart`, `PostToolUse` (matcher `Edit|Write`) e `Stop` — todos apontando
para `.claude/skills/impeccable/scripts/impeccable hook`. Tier imediato por
edição + deep pass no Stop.

### 4.3 Linha de base — detector nos projetos (2026-10-07)

| Projeto | Achados | Warnings | Advisory | Regras dominantes |
|---------|---------|----------|----------|-------------------|
| **hsoservicos** | 264 | 264 | 0 | `low-contrast` (210), `side-tab` (54) |
| **markdown-studio-live** | 1553 | 421 | 1132 | `design-system-color` (1017), `undersized-ui-text` (320), `design-system-font` (93) |
| **servicetec** | 246 | 122 | 124 | `gpt-thin-border-wide-shadow` (110), `low-contrast` (75), `cramped-padding` (41) |
| **sound-music-app** | 25 | 14 | 11 | `side-tab` (9), `gpt-thin-border-wide-shadow` (6), `codex-grid-background` (5), `low-contrast` (3), `layout-transition` (2) |
| **app** | 0 | 0 | 0 | (sem superfícies de UI — greenfield) |
| **TOTAL** | **2088** | 821 | 1267 | — |

> `markdown-studio-live` tem volume alto porque possui `DESIGN.md` ativo: as
> regras `design-system-*` detectam **deriva em relação ao design system
> declarado** (1017 `design-system-color`). É sinal de drift, não de "slop".

> **Nota sobre `markdown-studio-live` (103 arquivos deletados):** o `git status`
> mostra 103 deleções em `.opencode/skills/impeccable/scripts/`. Não é dano — é
> a mudança de arquitetura upstream do Impeccable: a versão anterior entregava o
> engine como **108 arquivos `.mjs`**; a v4.5.0/CLI 4.1.0 entrega um **binário
> compilado** (`scripts/bin/linux-x64/impeccable`, 18,5 MB) + launcher. Verificado:
> o engine standalone roda (`impeccable detect index.html`, exit 0) e todos os 5
> projetos estão em skill **4.5.0** / engine **0.1.11**.

**Recomendações priorizadas por projeto** (para os agentes dos projetos seguirem):

| Projeto | Próximo passo |
|---------|---------------|
| hsoservicos | `/impeccable harden` no frontend (210 `low-contrast` são WCAG AA) |
| markdown-studio-live | `/impeccable extract` para reconciliar tokens com `DESIGN.md`; `/impeccable typeset` (320 `undersized-ui-text`) |
| servicetec | `/impeccable polish` (110 `gpt-thin-border-wide-shadow` + 75 `low-contrast`) |
| sound-music-app | `/impeccable polish` nas 4 telas HTML; `/impeccable harden` p/ `low-contrast` |

### 4.4 Fluxos documentados

**Projeto novo (Track A):**

```bash
npx impeccable install -y --providers=claude,opencode --scope=project
# no agente:
/impeccable init              # PRODUCT.md (+ DESIGN.md), escolhe buildPath
/impeccable shape <surface>   # planeja UX/UI antes do código
/impeccable <pedido livre>
```

**Projeto legado (Track B):**

```bash
npx impeccable detect <dir-or-url>        # baseline determinístico
# no agente:
/impeccable document                      # gera DESIGN.md do código existente
/impeccable critique <surface>            # heurísticas de Nielsen + personas
/impeccable audit <surface>               # a11y/perf/responsive/integrity (0–20, P0–P3)
/impeccable harden <surface>              # erros, i18n, overflow, edge cases
/impeccable polish <surface>              # alinhamento final
```

**Gate de CI (determinístico, sem API key):**

```bash
npx impeccable detect --json src/ > impeccable-report.json
# exit 0 = limpo, 2 = achados primários → falhar o build, 1 = alvo ilegível
```

### 4.5 Regras de engajamento

1. **O brief vence.** Se a marca usa fonte/paleta sinalizada de propósito,
   registre a exceção (`npx impeccable ignores add-value <rule> <value> --reason "..."`);
   não "conserte" a marca silenciosamente.
2. **Scan limpo é evidência, não prova.** Sempre inspecionar a página renderizada
   em desktop e mobile antes do sign-off.
3. **`audit` documenta; não corrige.** Roteia P0/P1 para `harden`/`optimize`,
   o resto para `polish`. Um comando por passo mantém diffs revisáveis.
4. **Ignore só com evidência nomeada.** Tríade: *corrigir*, *exceção sanccionada*
   (registrar), ou *perguntar ao usuário*. Nunca adicionar ignore para empurrar
   uma escrita bloqueada.
5. **Live mode é local-only.** Nunca injetar em site em produção nem enfraquecer CSP.

---

## 5. Recomendações pendentes (fora do escopo executado)

| # | Recomendação | Esforço | Impacto |
|---|--------------|---------|---------|
| 1 | Atualizar BMAD em `markdown-studio-live` 6.11.0 → 6.12.1 (`--action quick-update`) | Baixo | Alto |
| 2 | `npm install` em `markdown-studio-live` para realinhar `package-lock.json` | Baixo | Médio |
| 3 | Atualizar BMAD em `hsoservicos` 6.12.0 → 6.12.1 | Baixo | Médio |
| 4 | Script `_bmad/scripts/post-update-restore.sh` automatizando o §2.4 | Médio | Alto |
| 5 | Mover `bmad-angular21`/`bmad-java21` para `_bmad/custom/` (módulo custom) | Médio | Alto |
| 6 | Adicionar gate `impeccable detect` ao CI de cada projeto com UI | Baixo | Alto |
| 7 | Popular `docs/` do hub com as lições dos 4 projetos (hoje vazio) | Alto | Alto |
| 8 | Preencher `PRODUCT.md`/`DESIGN.md` do hub via `/impeccable init` quando houver UI | Baixo | Médio |
| 9 | Considerar adotar AGENTS.md/CLAUDE.md em `sound-music-app` (hoje só `AGENT.md`) | Baixo | Médio |
| 10 | Commit do estado atual (108 arquivos modificados + novos) | Baixo | — |

---

## 6. Verificação final executada

| Verificação | Resultado |
|-------------|-----------|
| Paridade `.agents/skills` ↔ `.claude/skills` (app) | ✅ `diff` limpo, 55 = 55 |
| Mapeamento skills ↔ `.opencode/commands` (app) | ✅ 55 = 55, sem órfãos |
| Skills customizadas restauradas | ✅ angular21/java21 nas 2 árvores + 4 wrappers |
| BMAD version | ✅ core 6.12.1, bmm 6.12.1 |
| CrewAI CLI | ✅ `crewai version` → 1.15.25 (exit 0) |
| Impeccable skill nas 3 árvores (4 projetos) | ✅ 3 entradas em cada |
| Impeccable subagents (4 projetos) | ✅ 4 por projeto |
| Impeccable hooks (4 projetos) | ✅ SessionStart + PostToolUse + Stop |
| `.gitignore` impeccable (4 projetos) | ✅ bloco start/end presente |
| Detector smoke test | ✅ `npx impeccable detect` roda em todos |
