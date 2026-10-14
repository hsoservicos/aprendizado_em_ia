# Guia de Instalação, Ativação e Uso da Toolchain Integrada

**Versão**: 1.0.0
**Data**: 2026-10-07
**Autor**: Hsantos
**Status**: Production Ready
**Público-alvo**: qualquer membro da equipe que precise **montar a máquina do
zero**, **replicar o ambiente** ou **conduzir um projeto novo ou legado** com os
agentes de codificação OpenCode e Claude Code.

> **Escopo deste documento** — instalar, ativar e usar **três ferramentas
> integradas** que juntas cobrem o ciclo completo de desenvolvimento:
>
> | # | Ferramenta | Papel | Autor / Licença |
> |---|-----------|-------|-----------------|
> | 1 | **BMAD Method** | Metodologia de SDLC (Clarify→Plan→Build→Review→Learn), agentes especializados e artefatos | bmadcode · `npx bmad-method` |
> | 2 | **Impeccable** | Vocabulário de design + detector determinístico de anti-padrões de UI | Paul Bakaus · Apache-2.0 |
> | 3 | **Superpowers** | Metodologia de engenharia: TDD, debugging sistemático, worktrees, subagent-driven development | obra / Prime Radiant · MIT |
>
> Para o passo a passo narrado de um projeto (fases, stories, entregáveis), use
> `implementation-playbook.md`. Para só colocar a máquina de pé, use
> `project-replication-guide.md`. Este guia cobre **as ferramentas em si**.

---

## Sumário

1. [Arquitetura da toolchain](#1-arquitetura-da-toolchain)
2. [Pré-requisitos](#2-pré-requisitos)
3. [Instalação — máquina nova (passo a passo)](#3-instalação--máquina-nova-passo-a-passo)
4. [Ativação e verificação](#4-ativação-e-verificação)
5. [Precedência — como as três convivem](#5-precedência--como-as-três-convivem)
6. [Uso em projeto NOVO (greenfield)](#6-uso-em-projeto-novo-greenfield)
7. [Uso em projeto LEGADO (brownfield)](#7-uso-em-projeto-legado-brownfield)
8. [Manutenção e atualização](#8-manutenção-e-atualização)
9. [Solução de problemas](#9-solução-de-problemas)
10. [Checklist de aceite](#10-checklist-de-aceite)

---

## 1. Arquitetura da toolchain

### 1.1 O que cada ferramenta resolve

| Ferramenta | Problema que resolve | Entregável típico |
|-----------|----------------------|-------------------|
| **BMAD Method** | "Por onde começo? O que escrevo antes de codar? Como divido o trabalho?" | PRD, architecture, epics/stories, sprint status, retrospective |
| **Impeccable** | "A UI gerada por IA tem cara de UI gerada por IA" (Inter em tudo, gradientes roxo, cards dentro de cards) | `PRODUCT.md`, `DESIGN.md`, relatório de audit 0–20, detector de 61 regras |
| **Superpowers** | "O agente escreveu código sem teste, sem plano, e alegou que funciona" | spec validada, plano de tasks de 2–5 min, código TDD, verificação com evidência |

### 1.2 Como cada uma se conecta ao agente

| Camada | BMAD | Impeccable | Superpowers |
|--------|------|------------|-------------|
| Skills | `.agents/skills/` + `.claude/skills/` (54 `bmad-*`) | `.agents/skills/`, `.claude/skills/`, `.opencode/skills/` (1) | **plugin cache** (15) — *nunca* na árvore BMAD |
| Comandos | `/bmad-*` (55 wrappers em `.opencode/commands/`) | `/impeccable <cmd>` | `/superpowers:*` ou via Skill tool |
| Hooks | — | `SessionStart`, `PostToolUse` (Edit\|Write), `Stop` | `SessionStart` (`startup\|clear\|compact`) |
| CLI de shell | `npx bmad-method`, `uv run _bmad/scripts/render_skill.py` | `npx impeccable detect` | — (só plugin) |
| Subagents | `bmad-agent-*` | `impeccable-*` (4) | — (usa `task`/`subagent` tool) |
| Onde vive | `_bmad/` (repo) | `.impeccable/` + skill trees (repo) | `~/.claude/plugins/cache/…` + `~/.config/opencode/…` (máquina) |

### 1.3 Dependências de runtime por ferramenta

| Componente | Necessário para | Se faltar |
|-----------|-----------------|-----------|
| Node.js ≥ 22 | `npx bmad-method`, `npx impeccable` | instalação impossível |
| Python ≥ 3.12 + `uv` | renderizar skills BMAD (`uv run _bmad/scripts/render_skill.py`) | HALT na regra de invocação de skill |
| Git | updates, worktrees do Superpowers, custom modules | Superpowers degrada |
| ripgrep (`rg`) | RTK e buscas | buscas lentas |
| RTK | compressão de tokens (60–90%) | sem compressão, custo sobe |
| Chrome/Chromium/Edge | `impeccable detect <url>` (renderização) | scan de URL indisponível (arquivos locais continuam ok) |

---

## 2. Pré-requisitos

Rode **antes de qualquer coisa**:

```bash
node --version && python3 --version && uv --version && git --version \
  && rtk --version && rg --version && gh --version | head -1 \
  && opencode --version && claude --version
```

Esperado nesta máquina (2026-10-07):

| Ferramenta | Versão mínima | Versão atual |
|-----------|---------------|--------------|
| Node.js | ≥ 22 | v24.21.0 |
| Python | ≥ 3.12 | 3.14.4 |
| uv | ≥ 0.12 | 0.12.23 |
| Git | qualquer | 2.53.0 |
| ripgrep | qualquer | 15.2.0 |
| RTK | qualquer | 0.51.0 |
| GitHub CLI | qualquer | 2.102.0 |
| OpenCode | ≥ 1.18 | 1.18.35 |
| Claude Code | ≥ 2.1 | 2.1.289 |
| CrewAI (opcional) | ≥ 1.15 | 1.15.25 |

Se `crewai` falhar com `Failed find package 'crewai' in tool environment`,
repare com `uv tool install crewai --force` (aconteceu em 2026-10-07).

---

## 3. Instalação — máquina nova (passo a passo)

> Rode os comandos **na raiz do projeto**. Em `/home/hsantos/app` (o hub), tudo
> já está instalado; esta seção serve para replicar em um projeto novo.

### Passo 1 — Obter o repositório

```bash
git clone <url-do-projeto> && cd <projeto>
```

### Passo 2 — BMAD Method (metodologia + agentes)

```bash
npx bmad-method install
# interativo: escolha os módulos (bmm) e os tools (claude-code, opencode)
# não-interativo / script:
npx bmad-method install --directory . --modules bmm \
  --tools claude-code,opencode --action install -y
```

Verifica:

```bash
rtk grep "Version:" _bmad/bmm/config.yaml   # → 6.12.1
ls .agents/skills | wc -l                    # → 50 (skills oficiais)
diff <(ls .agents/skills) <(ls .claude/skills) && echo PARITY_OK
```

### Passo 3 — Impeccable (design + detector de UI)

```bash
npx impeccable install -y --providers=claude,opencode --scope=project
# espelhar na árvore de paridade (o instalador só grava .claude/ e .opencode/)
cp -r .opencode/skills/impeccable .agents/skills/impeccable
```

O que aparece:

```
.claude/skills/impeccable/     .opencode/skills/impeccable/    .agents/skills/impeccable/
.claude/agents/impeccable-{asset-producer,documenter,finish-reviewer,manual-edit-applier}.md
.opencode/commands/impeccable.md
.claude/settings.local.json    # hooks SessionStart + PostToolUse + Stop  (gitignored)
```

Adicionar ao `.gitignore` (bloco já pronto — manter `config.json`, `design.json`,
`critique/`, `surfaces/`, `live/config.json` versionados):

```
# impeccable-ignore-start
.impeccable/config.local.json
.impeccable/hook.cache.json
.impeccable/hook.pending.json
.impeccable/*.png
.impeccable/live/server.json
.impeccable/live/sessions/
.impeccable/live/previews/
.impeccable/live/annotations/
.impeccable/live/cache/
.impeccable/live/manual-edit-apply-transaction.json
.impeccable/live/manual-edit-events.jsonl
.impeccable/live/manual-edit-evidence/
.impeccable/live/pending-manual-edits.json
.impeccable/live/deferred-svelte-component-accepts.json
.impeccable/live/*.png
# impeccable-ignore-end

# Hooks do Claude Code (Impeccable) — por máquina/desenvolvedor
.claude/settings.local.json
```

### Passo 4 — Superpowers (metodologia de engenharia)

**OpenCode** (plugin de projeto — versionado no repositório):

```bash
opencode plugin superpowers@git+https://github.com/obra/superpowers.git
# grava em .opencode/opencode.json:
#   { "plugin": ["superpowers@git+https://github.com/obra/superpowers.git"] }
```

**Claude Code** (plugin de usuário — por máquina):

```bash
claude plugin marketplace list                  # claude-plugins-official já vem registrado
claude plugin install superpowers@claude-plugins-official
claude plugin list                              # deve listar superpowers (enabled)
```

Versões: o marketplace oficial publica **6.4.1**; o `main` do git está em
**6.4.2**. Para pinar uma tag específica no OpenCode:

```json
{ "plugin": ["superpowers@git+https://github.com/obra/superpowers.git#v6.4.1"] }
```

**Não copie as skills do Superpowers para `.agents/skills/` ou `.claude/skills/`** —
ver §8.2.

### Passo 5 — Desligar telemetry do Superpowers

O único chamado de rede é o logo do *visual companion* do `brainstorming` (carrega
a versão na URL; sem dados de projeto). Desligue por política de privacidade em
`.claude/settings.json`:

```json
{
  "env": {
    "SUPERPOWERS_DISABLE_TELEMETRY": "1",
    "DISABLE_TELEMETRY": "1",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  }
}
```

### Passo 6 — Permissões do Claude Code

Em `.claude/settings.json` → `permissions.allow`, além do que o RTK/uv já usam,
inclua o que o fluxo de engenharia precisa:

```json
"Bash(npx bmad-method:*)", "Bash(npx bmad-method@*:*)", "Bash(npx impeccable:*)",
"Bash(git worktree:*)", "Bash(git switch:*)", "Bash(git checkout:*)",
"Bash(git merge:*)", "Bash(git rebase:*)", "Bash(git add:*)", "Bash(git commit:*)",
"Bash(git stash:*)", "Bash(git branch:*)", "Bash(git status:*)", "Bash(git diff:*)",
"Bash(git log:*)", "Bash(npm test:*)", "Bash(npm run:*)", "Bash(pytest:*)"
```

---

## 4. Ativação e verificação

### 4.1 Comandos de verificação (rode todos)

```bash
# BMAD
rtk grep "Version:" _bmad/bmm/config.yaml _bmad/core/config.yaml
diff <(ls .agents/skills) <(ls .claude/skills) && echo "BMAD parity OK"

# Impeccable
npx impeccable detect --version
find .agents/skills/impeccable .claude/skills/impeccable .opencode/skills/impeccable \
  -maxdepth 1 -mindepth 1 | wc -l          # → 3 (cada)
test -f .claude/settings.local.json && echo "Impeccable hooks OK"

# Superpowers
cat .opencode/opencode.json
claude plugin list | grep -i superpowers   # → enabled
```

### 4.2 Teste funcional (o que realmente prova que está ativo)

| Ferramenta | Teste | Esperado |
|-----------|-------|----------|
| **Superpowers** | Em sessão limpa, mande exatamente: `Let's make a react todo list` | `brainstorming` dispara **antes** de qualquer código |
| **Superpowers** | Pergunte: `Tell me about your superpowers` | lista as 15 skills |
| **BMAD** | Rode `/bmad-help` | orienta o próximo passo do workflow |
| **Impeccable** | Rode `npx impeccable detect <dir-com-html>` | saída com achados ou "clean", exit `0`/`2` |
| **Impeccable** | Rode `/impeccable init` | propõe gravar `PRODUCT.md` |

> O teste do Superpowers não é cosmético: ele é a **definição oficial de
> integração real** do projeto upstream (`AGENTS.md` de `obra/superpowers`).
> Integrações que exigem opt-in por sessão, ou onde `brainstorming` não dispara,
> são consideradas inválidas pela comunidade do projeto.

### 4.3 Custo em tokens

| Item | Custo |
|------|-------|
| Superpowers (descrições, sempre ativo) | ~703 tok/sessão |
| Superpowers (corpo de uma skill, ao invocar) | 0,7k – 8,1k |
| Impeccable (skill, ao invocar) | ~4k – 12k |
| BMAD (skill, ao invocar) | 3k – 15k |
| Hook `SessionStart` do Superpowers | 0 (harness-only) |

---

## 5. Precedência — como as três convivem

**Isto é obrigatório.** BMAD e Superpowers disparam nos mesmos prompts; sem regra
de precedência o agente gera artefatos duplicados.

| Preocupação | Primária | Secundária | Regra |
|------------|----------|-----------|-------|
| **Fase de SDLC** (Clarify→Plan→Build→Review→Learn) | **BMAD** | Superpowers | BMAD dono do ciclo de vida; Superpowers roda *dentro* de uma fase BMAD |
| **Ideia → spec → stories** | `bmad-forge-idea`, `bmad-spec`, `bmad-create-epics-and-stories` | `brainstorming`, `writing-plans` | `writing-plans` só para decompor uma story BMAD em tasks de 2–5 min |
| **Construir uma story** | `bmad-build` | `executing-plans`, `subagent-driven-development` | escolher **um** loop de execução, nunca os dois |
| **Disciplina de TDD** | **Superpowers** | — | gap real do BMAD; sempre ativo dentro de `bmad-build` |
| **Debug** | **Superpowers** (`systematic-debugging`) | `bmad-review-edge-case-hunter` | Superpowers = causa-raiz; BMAD = caça a edge cases |
| **Code review** | `bmad-code-review` | `requesting-code-review`, `receiving-code-review` | BMAD gera o review; Superpowers cuida de *receber* + checklist pré-merge |
| **Verificação / DoD** | **Superpowers** (`verification-before-completion`) | `bmad-review-verification-gap` | Superpowers é gate contínuo; BMAD é auditoria pontual |
| **Worktree / fechar branch** | **Superpowers** | — | BMAD não cobre |
| **Design / UI** | **Impeccable** | — | dono único do vocabulário visual + detector |
| **Autoria de skills** | `bmad-customize` | `writing-skills` | o método do Superpowers é o melhor template |

**Cinco regras duras**

1. Quando uma skill Superpowers fosse disparar e uma `bmad-*` cobre a mesma fase,
   **anuncie as duas** (`Using bmad-spec, then writing-plans`) e rode o BMAD
   primeiro. Os artefatos BMAD (`_bmad-output/planning-artifacts/…`) são canônicos.
2. O pipeline mandatório do Superpowers
   (`brainstorming → using-git-worktrees → writing-plans → executors → TDD →
   requesting-code-review → finishing-a-development-branch`) vale **só para a fase
   Build**. Não refaça Clarify/Plan por ele.
3. Nunca rode `subagent-driven-development` e `bmad-build-auto` na mesma sessão.
4. O bootstrap do Superpowers diz que *instruções do parceiro humano vencem
   skills*. O `AGENTS.md` do projeto **é** essa instrução e tem precedência.
5. Subagentes do Superpowers ignoram o bootstrap (`<SUBAGENT-STOP>`) — passe o
   contexto BMAD explicitamente.

---

## 6. Uso em projeto NOVO (greenfield)

Fluxo completo das 5 fases com as três ferramentas. Detalhe narrado em
`implementation-playbook.md` PARTE A.

### CLARIFY — BMAD conduz

```
/bmad-help                    # onde estou, qual o próximo passo
/bmad-brainstorming           # explorar a ideia
/bmad-forge-idea              # pressionar a ideia com personas
/bmad-prfaq                   # (opcional) Working Backwards
/bmad-product-brief           # consolidar
```

> **Não** dispare o `brainstorming` do Superpowers aqui. Se ele aparecer,
> responda "Use bmad-brainstorming; Superpowers is deferred to the Build phase."

### PLAN — BMAD conduz; Superpowers refina a granularidade

```
/bmad-prd                     # requisitos
/bmad-architecture            # decisões de arquitetura
/bmad-ux                      # DESIGN.md + EXPERIENCE.md (ou /impeccable para UI pura)
/bmad-create-epics-and-stories
/bmad-sprint-planning
```

Se for construir UI, **nesta fase** (e não depois):

```
/impeccable init              # PRODUCT.md (+ DESIGN.md), escolhe buildPath (comp|code)
/impeccable shape <surface>   # planeja a UX antes do código
```

Para fatiar uma story em tasks executáveis de 2–5 minutos:

```
use skill tool to load writing-plans
# → docs/superpowers/plans/YYYY-MM-DD-<feature>.md
```

### BUILD — escolha **um** loop

**Opção A — BMAD direto** (menos overhead, boa para mudanças pequenas):

```
/bmad-build
```

**Opção B — BMAD + Superpowers em subagentes** (mais rigor, histórias maiores):

```
use skill tool to load using-git-worktrees        # isolamento
use skill tool to load subagent-driven-development
```

Em **qualquer** opção, dentro da implementação:

```
use skill tool to load test-driven-development    # RED-GREEN-REFACTOR, sempre
use skill tool to load verification-before-completion   # antes de dizer "pronto"
```

E para UI, ao editar superfícies visuais: `/impeccable polish <surface>` +
`npx impeccable detect <dir>`.

### REVIEW — BMAD gera, Superpowers recebe

```
/bmad-code-review                       # revisores adversariais
use skill tool to load receiving-code-review     # como trazer o feedback
use skill tool to load requesting-code-review    # checklist pré-merge
npx impeccable detect --json src/ > impeccable-report.json   # gate determinístico
/impeccable audit <surface>             # 0–20 + P0–P3
```

### LEARN — BMAD

```
/bmad-retrospective
```

### Checklist PARTE A

- [ ] `PRODUCT.md` e `DESIGN.md` existem (Impeccable)
- [ ] Plano em `docs/superpowers/plans/` tem tasks de 2–5 min
- [ ] Todo código de produção passou por RED-GREEN-REFACTOR
- [ ] `verification-before-completion` citou a saída real dos comandos
- [ ] `npx impeccable detect` exit `0` (ou achados registrados como exceção)
- [ ] Retrospectiva gerada

---

## 7. Uso em projeto LEGADO (brownfield)

Fluxo detalhado em `implementation-playbook.md` PARTE B. O que cada ferramenta
adiciona no legado:

### B0 — Entrar com segurança

```
git worktree add ../<projeto>-audit -b audit/baseline   # Superpowers
# ou: use skill tool to load using-git-worktrees
```

Nunca rode mudança em `main` de legado sem isolamento.

### B1 — Mapear o legado (BMAD)

```
/bmad-project-context         # grava stack + convenções em AGENTS.md/CLAUDE.md
```

### B2 — Linha de base de qualidade (as três)

```
/bmad-code-review             # qualidade de código da base existente

npx impeccable detect <dir|url>          # baseline determinístico (sem LLM)
# guarde o JSON: é a métrica "antes"

use skill tool to load systematic-debugging   # para os bugs conhecidos da base
```

### B3 — Capturar o design que já existe (Impeccable)

```
/impeccable document          # gera DESIGN.md a partir do código atual
/impeccable critique <surface>    # heurísticas de Nielsen + personas
/impeccable audit <surface>       # a11y / perf / responsive / integrity (0–20, P0–P3)
```

> **Importante:** o detector do Impeccable pode acusar o design legado como
> "anti-padrão". Se a marca usa isso de propósito, **não conserte** — registre a
> exceção: `npx impeccable ignores add-value <rule> <value> --reason "..."`.

### B4 — Planejar e executar a modernização

```
/bmad-spec                    # ou /bmad-create-epics-and-stories
use skill tool to load writing-plans     # tasks de 2–5 min por ciclo
use skill tool to load using-git-worktrees
/bmad-build                   # OU subagent-driven-development (escolher 1)
use skill tool to load test-driven-development    # testes ANTES do refactor
```

### B5 — Fechar e entregar

```
use skill tool to load finishing-a-development-branch   # merge/PR/keep/discard
/bmad-retrospective
npx impeccable detect --json src/ > impeccable-report-after.json   # "depois"
```

### Checklist PARTE B

- [ ] Worktree isolado antes de qualquer mudança
- [ ] `AGENTS.md` do legado populado por `/bmad-project-context`
- [ ] Baselines guardadas: detector Impeccable "antes" + code review BMAD
- [ ] `DESIGN.md` gerado por `/impeccable document` (não inventado)
- [ ] Exceções de design registradas com `ignores add-value` + reason
- [ ] Todo refactor passou por TDD (teste antes)
- [ ] Branch finalizada via `finishing-a-development-branch`

---

## 8. Manutenção e atualização

### 8.1 Comandos de update

```bash
# BMAD
npx bmad-method install --action quick-update --tools claude-code,opencode -y

# Impeccable
npx impeccable install -y --providers=claude,opencode --scope=project --force

# Superpowers
claude plugin update superpowers
opencode plugin superpowers@git+https://github.com/obra/superpowers.git -f
```

### 8.2 ⚠️ O instalador do BMAD apaga skills que não conhece

**Provado em 2026-10-07**: o `quick-update` removeu 32 arquivos das skills
customizadas `bmad-angular21`, `bmad-java21`, `bmad-agent-angular21`,
`bmad-agent-java21`. Por isso o Superpowers **não** pode ficar em
`.agents/skills/` — ele fica no plugin cache.

Sequência de recuperação obrigatória após **todo** `npx bmad-method install`:

```bash
# 1. restaurar skills customizadas
git checkout -- .agents/skills/bmad-angular21 .agents/skills/bmad-java21 \
  .agents/skills/bmad-agent-angular21 .agents/skills/bmad-agent-java21 \
  .claude/skills/bmad-angular21 .claude/skills/bmad-java21 \
  .claude/skills/bmad-agent-angular21 .claude/skills/bmad-agent-java21 \
  .opencode/commands/bmad-angular21.md .opencode/commands/bmad-java21.md \
  .opencode/commands/bmad-agent-angular21.md .opencode/commands/bmad-agent-java21.md

# 2. reinstalar Impeccable e espelhar a árvore
npx impeccable install -y --providers=claude,opencode --scope=project --force
cp -r .opencode/skills/impeccable .agents/skills/impeccable

# 3. verificar paridade
diff <(ls .agents/skills) <(ls .claude/skills) && echo PARITY_OK

# 4. Superpowers não se afeta (está fora da árvore), mas confirme:
claude plugin list | grep -i superpowers
cat .opencode/opencode.json
```

### 8.3 Política de modificação de skills

| Ferramenta | Pode editar localmente? | Como |
|-----------|------------------------|------|
| BMAD | Sim, via `_bmad/custom/` | `bmad-customize` — nunca editar `_bmad/` direto |
| Impeccable | Sim, via `.impeccable/config.json` (ignores) | `npx impeccable ignores add-value …` |
| Superpowers | **Não** | Upstream: *"skills are not prose — they are code that shapes agent behavior"*, 94% de rejeição de PR. Sobrescreva só via `AGENTS.md` (precedência) |

---

## 9. Solução de problemas

| Sintoma | Causa provável | Correção |
|---------|----------------|----------|
| `Failed find package 'crewai' in tool environment` | venv uv corrompido | `uv tool install crewai --force` |
| Skills BMAD não aparecem | paridade quebrada / update apagou | §8.2 |
| `/impeccable` não responde | skill fora de `.claude/skills/` | `npx impeccable install … --force` + espelhar |
| Hooks do Impeccable não disparam | `settings.local.json` gitignored, ausente na máquina | `npx impeccable install -y --providers=claude,opencode --scope=project` |
| `brainstorming` do Superpowers não dispara | bootstrap `SessionStart` não carregou | `claude plugin list` (enabled?); reiniciar sessão; `opencode run --standalone --print-logs "hello" 2>&1 \| grep -i superpowers` |
| Superpowers dispara e atrapalha o BMAD | falta a regra de precedência | §5 deste guia + `AGENTS.md` |
| `npx impeccable detect <url>` falha | sem Chrome/Chromium/Edge | instalar browser ou varrer arquivos locais |
| `impeccable detect` acusa o design de propósito | marca intencional | `npx impeccable ignores add-value <rule> <value> --reason "…"` |
| OpenCode não acha as skills do Superpowers | plugin não instalado / cache velho | `opencode plugin … -f`; limpar cache de pacotes |
| Atualização do Superpowers não aparece | lockfile/cache de pacote pinado | reinstalar o plugin ou pinar `#vX.Y.Z` |

Logs: OpenCode → `~/.local/share/opencode/log/opencode.log` (`role=server`).

---

## 10. Checklist de aceite

Rode ao terminar qualquer instalação ou atualização. Tudo precisa dar ✓.

```bash
echo "== 1. Toolchain =="
node --version && python3 --version && uv --version && git --version && rtk --version

echo "== 2. BMAD =="
rtk grep "Version:" _bmad/bmm/config.yaml _bmad/core/config.yaml
diff <(ls .agents/skills) <(ls .claude/skills) && echo "  parity OK"
test -f _bmad/scripts/render_skill.py && echo "  render_skill OK"

echo "== 3. Impeccable =="
npx impeccable detect --version
for d in .agents/skills .claude/skills .opencode/skills; do
  test -d "$d/impeccable" && echo "  $d/impeccable OK"
done
test -f .claude/settings.local.json && echo "  hooks OK"
rtk grep -q "impeccable-ignore-start" .gitignore && echo "  gitignore OK"

echo "== 4. Superpowers =="
cat .opencode/opencode.json
claude plugin list | grep -i superpowers
rtk grep -q "SUPERPOWERS_DISABLE_TELEMETRY" .claude/settings.json && echo "  telemetry OFF"

echo "== 5. Precedência documentada =="
rtk grep -q "Precedence — BMAD" AGENTS.md && echo "  AGENTS.md OK"
```

**Teste funcional manual** (não automatizável): abrir sessão limpa e mandar
`Let's make a react todo list` → `brainstorming` precisa disparar antes de
qualquer código.

---

## Referências

| Recurso | Caminho |
|---------|---------|
| Onboarding da máquina | `_bmad-output/getting-started.md` |
| Passo a passo de projeto (fases, stories) | `_bmad-output/implementation-playbook.md` |
| Replicação de máquina | `_bmad-output/project-replication-guide.md` |
| Inventário de ferramentas | `_bmad-output/tools-registry.md` |
| Auditoria 2026-10-07 | `_bmad-output/audit-report-2026-10-07.md` |
| Achados do estudo Superpowers | `_bmad-output/superpowers-study-2026-10-07.md` |
| Precedência e uso por agente | `AGENTS.md` (seções *Superpowers*, *Impeccable*) |
| Superpowers — OpenCode | <https://github.com/obra/superpowers/blob/main/docs/README.opencode.md> |
| Superpowers — repositório | <https://github.com/obra/superpowers> |
| Impeccable | <https://impeccable.style> |
| BMAD Method | <https://bmadcode.com/> |
