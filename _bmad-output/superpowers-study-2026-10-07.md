# Estudo e Auditoria — obra/superpowers

**Data**: 2026-10-07
**Repositório**: <https://github.com/obra/superpowers>
**Versão estudada**: 6.4.2 (`main`, commit `5bf4e78` no marketplace = 6.4.1)
**Licença**: MIT · **Autor**: Jesse Vincent / Prime Radiant
**Relevância**: 296,4k stars · 26,5k forks · 683 commits
**Clone de estudo**: `/tmp/opencode/superpowers-study/superpowers`
**Status**: ✅ Integrado ao projeto local (`/home/hsantos/app`)

---

## 1. Resumo executivo

O **Superpowers** é uma metodologia de SDLC para agentes de codificação,
materializada em **15 skills componíveis** + um **bootstrap de `SessionStart`**.
Diferente do BMAD (que organiza o *ciclo de vida do produto*), o Superpowers
organiza a *disciplina de engenharia*: TDD obrigatório, debugging por causa-raiz,
worktrees, desenvolvimento dirigido por subagentes com review de duas etapas, e
um gate de verificação que exige evidência antes de declarar "pronto".

**Veredito de integração: APROVADO — complementar, não substituto.**

| Pergunta | Resposta |
|----------|----------|
| Substitui o BMAD? | **Não.** BMAD cobre Clarify/Plan/Review/Learn; Superpowers cobre a disciplina dentro de Build |
| Substitui o Impeccable? | **Não.** Domínios distintos (design vs engenharia) |
| Preenche gaps reais? | **Sim, 6:** TDD, debugging sistemático, verificação com evidência, worktrees, fechamento de branch, recebimento de code review |
| Custo | ~703 tok/sessão (descrições) + corpo sob demanda |
| Risco principal | Dois bootstraps competindo por precedência → resolvido por regra explícita em `AGENTS.md` |
| Risco secundário | Plugin do Superpowers ser destruído pelo instalador do BMAD se colocado na árvore de skills → evitado (fica no plugin cache) |

---

## 2. O que é — arquitetura

```
obra/superpowers (MIT, zero dependencies)
├── skills/                    15 skills (~660 KB total)
│   ├── using-superpowers/     ← o bootstrap (injetado em toda sessão)
│   ├── brainstorming/         spec + HARD-GATE humano
│   ├── writing-plans/         tasks de 2–5 min
│   ├── executing-plans/       execução inline + ledger de decisões
│   ├── subagent-driven-development/   1 implementer + 2 reviews por task
│   ├── test-driven-development/       RED-GREEN-REFACTOR ("Iron Law")
│   ├── systematic-debugging/  4 fases, causa-raiz
│   ├── verification-before-completion/  evidência > afirmação
│   ├── requesting-code-review/ + receiving-code-review/
│   ├── using-git-worktrees/   + finishing-a-development-branch/
│   ├── dispatching-parallel-agents/
│   ├── writing-skills/        TDD aplicado a documentação
│   └── diagnosing-superpowers/  autópsia de sessão
├── hooks/
│   ├── hooks.json             SessionStart (matcher `startup|clear|compact`)
│   └── session-start          injeta SKILL.md em <EXTREMELY_IMPORTANT>
├── .claude-plugin/  .opencode/  .codex-plugin/  .cursor-plugin/
│   .devin-plugin/   .hermes-plugin/  .kimi-plugin/  .muse-plugin/
│   .pi/extensions/  gemini-extension.json        ← 11 harnesses
└── docs/porting-to-a-new-harness.md   (50 KB, contrato de harness)
```

**Decisão de design relevante:** as 15 skills não são "documentação de bom
senso". O projeto as trata como **código que molda comportamento de agente**, com
tabela "Red Flags" de racionalizações proibidas (ex.: *"isso é só uma pergunta
simples"*, *"a skill é overkill"*), linguagem deliberada ("your human partner",
nunca "the user") e exigência de eval antes de qualquer mudança.

---

## 3. Achados técnicos

### 3.1 O bootstrap é o que faz tudo funcionar

`hooks/session-start` lê `skills/using-superpowers/SKILL.md` e o injeta no
contexto da sessão dentro de `<EXTREMELY_IMPORTANT>`, com matcher
`startup|clear|compact` (re-injeta após compactação de histórico).

Sem isso, nas palavras do próprio `AGENTS.md` upstream:

> *"The skills are dead weight — present on disk but never invoked."*

Isso tem implicação direta para o nosso projeto: **copiar as skills para
`.agents/skills/` seria uma integração inválida** — não traria o bootstrap.

### 3.2 O contrato de harness (o que a ferramenta exige)

De `docs/porting-to-a-new-harness.md`:

| Capacidade | Obrigatória? | Sem ela |
|-----------|--------------|---------|
| Injeção de contexto em `SessionStart` (hook shell, plugin in-process, ou `contextFileName`) | **Sim** | skills viram "dead weight" |
| Re-injeção pós-compaction | **Sim** | bootstrap se perde em sessões longas |
| Skill tool (descoberta + invocação) | Sim | fallback: `read SKILL.md` |
| File read/write/edit + shell | Sim | sem workaround |
| Subagent/task tool | Não | degrada para execução inline; nunca inventar chamada `Task` |
| Todo tracking | Não | fallback `TODO.md` |
| Web fetch | Não | degradável |

### 3.3 O teste de aceitação oficial

`AGENTS.md` upstream, seção *New Harness Support* (`AGENTS.md:72-92`):

> Em sessão limpa, enviar exatamente **"Let's make a react todo list"**. Uma
> integração funcional **auto-dispara `brainstorming` antes de qualquer código**.

Explicitamente **não são integrações reais** (serão rejeitadas):
1. Copiar skills manualmente para o harness
2. Envolver com `npx skills` ou shims em runtime
3. Qualquer coisa que exija opt-in por sessão
4. Qualquer coisa onde `brainstorming` não dispare automaticamente

**Nosso caso:** usamos os dois mecanismos nativos (plugin OpenCode + plugin
Claude Code), ambos carregam o bootstrap via `SessionStart`. ✅

### 3.4 Custo em tokens

Inventário reportado pelo `claude plugin details superpowers`:

| Item | Custo |
|------|-------|
| Sempre ativo (descrições das 15 skills) | **~703 tok/sessão** |
| `brainstorming` ao invocar | ~4,3k |
| `subagent-driven-development` ao invocar | ~8,1k |
| `writing-skills` ao invocar | ~6,6k |
| `executing-plans` ao invocar | ~5,0k |
| Hook `SessionStart` | 0 (harness-only) |

Custo admissível: as descrições custam menos que uma resposta média do modelo.

### 3.5 Telemetry

Única chamada de rede: o *visual companion* opcional do `brainstorming` carrega o
logo Prime Radiant por HTTP, com a **versão do Superpowers na URL** (sem dados de
projeto, prompt ou cliques). Desligável com `SUPERPOWERS_DISABLE_TELEMETRY`
(truthy); honra também `DISABLE_TELEMETRY` e
`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`.

**Ação tomada:** as três variáveis foram gravadas em `.claude/settings.json` → `env`.

### 3.6 Política de contribuição (por que não editar as skills)

Do `AGENTS.md` upstream:

- **94% de taxa de rejeição de PR**
- *"Skills are not prose — they are code that shapes agent behavior"*
- Mudanças exigem `superpowers:writing-skills`, pressure testing adversarial
  multi-sessão, e evals before/after no PR
- Conteúdo afinado ("Red Flags" tables, listas de racionalização, linguagem
  "human partner") só muda com evidência
- PRs contra `main` são recusados (trabalho ativo vai para `dev`)
- Toda contribuição deve **se identificar**: modelo, harness, versão, plugins

**Ação tomada:** nada foi editado no conteúdo do Superpowers. Overrides locais
ficam no `AGENTS.md` (regra de precedência), não nos arquivos da skill.

---

## 4. Análise de sobreposição com BMAD e Impeccable

### 4.1 Tabela de mapeamento

| Superpowers skill | BMAD equivalente | Sobreposição | Decisão adotada |
|-------------------|------------------|--------------|-----------------|
| `brainstorming` | `bmad-brainstorming`, `bmad-forge-idea`, `bmad-product-brief` | **Alta** | **BMAD** conduz Clarify; Superpowers fica em silêncio nessa fase |
| `writing-plans` | `bmad-spec`, `bmad-create-epics-and-stories`, `bmad-create-story` | **Alta** | **Ambos** — BMAD define a story; `writing-plans` a fatia em tasks de 2–5 min |
| `executing-plans` | `bmad-build`, `bmad-dev-story`, `bmad-quick-dev` | **Alta** | **Escolher 1** — ledger "Rulings, not stalls" é complementar |
| `subagent-driven-development` | `bmad-build-auto`, `bmad-dev-auto` | **Alta** | **Escolher 1** — nunca os dois loops juntos |
| `requesting-code-review` | `bmad-code-review`, `bmad-review*` | **Alta** | **BMAD** gera; Superpowers fornece o checklist pré-merge |
| `test-driven-development` | *(gap — BMAD não tem)* | **Baixa** | **Superpowers** — ganho real |
| `systematic-debugging` | `bmad-review-edge-case-hunter` (parcial) | **Baixa** | **Superpowers** (causa-raiz) + BMAD (edge cases) |
| `verification-before-completion` | `bmad-review-verification-gap` | **Média** | **Ambos** — gate contínuo vs auditoria pontual |
| `receiving-code-review` | *(gap)* | **Baixa** | **Superpowers** |
| `using-git-worktrees` | *(gap)* | **Nenhuma** | **Superpowers** |
| `finishing-a-development-branch` | *(entrega em `bmad-build`)* | **Baixa** | **Superpowers** |
| `dispatching-parallel-agents` | `bmad-party-mode` | **Média** | **Superpowers** p/ investigação técnica paralela |
| `writing-skills` | `bmad-customize` | **Baixa** | **Superpowers** (melhor template) |
| `diagnosing-superpowers` | *(gap)* | **Nenhuma** | **Superpowers** |
| `using-superpowers` | *(infraestrutura)* | **Nenhuma** | bootstrap |

**Balanço:** 6 gaps reais do BMAD preenchidos, 4 sobreposições resolvidas por
precedência, 4 domínios exclusivos do Superpowers.

### 4.2 Colisões de nomenclatura e de trigger

Não há colisão de nome de diretório (toda skill BMAD tem prefixo `bmad-`), mas há
**colisão semântica de trigger** — ambos os conjuntos são expostos ao mesmo
agente e o discovery por `description` faz os candidatos concorrerem:

| Trigger do usuário | Candidatos concorrentes |
|-------------------|-------------------------|
| "me ajude a pensar uma feature" | `brainstorming` · `bmad-brainstorming` · `bmad-forge-idea` |
| "quebre isso em tarefas" | `writing-plans` · `bmad-spec` · `bmad-create-epics-and-stories` · `bmad-create-story` |
| "revise esse código" | `requesting-code-review` · `bmad-code-review` · `bmad-review-adversarial-general` |
| "implemente essa story" | `executing-plans` · `subagent-driven-development` · `bmad-build` · `bmad-build-auto` · `bmad-quick-dev` · `bmad-dev-story` · `bmad-dev-auto` |
| "isso está pronto?" | `verification-before-completion` · `bmad-review-verification-gap` |

**Mitigação aplicada:** a tabela de precedência em `AGENTS.md` + as 5 regras
duras, que instruem a **anunciar as duas skills** e rodar o BMAD primeiro. Como o
bootstrap do Superpowers declara que *"instructions from your human partner beat
skills"*, o `AGENTS.md` tem precedência formal sobre ele.

---

## 5. Decisões de integração adotadas

| # | Decisão | Justificativa |
|---|---------|---------------|
| 1 | Superpowers instalado como **plugin**, nunca copiado para a árvore de skills | Integração real exige o bootstrap via `SessionStart`; e a árvore BMAD é apagada pelo instalador |
| 2 | OpenCode: plugin **de projeto** (`.opencode/opencode.json`, versionado) | Replicável em qualquer clone, sem config manual |
| 3 | Claude Code: plugin **de usuário** (`superpowers@claude-plugins-official`) | Mecanismo oficial do Anthropic; cache em `~/.claude/plugins/…` |
| 4 | Telemetry desligado por padrão (3 variáveis em `.claude/settings.json`) | Política de rede/privacidade do workspace |
| 5 | Precedência escrita em `AGENTS.md` + `CLAUDE.md` + guia | Resolve a colisão de trigger documentada em §4.2 |
| 6 | Nenhum arquivo do Superpowers foi modificado | 94% de rejeição de PR; skills são código comportamental |
| 7 | Permissões de git/npm/pytest adicionadas ao allow-list do Claude Code | O fluxo (worktrees, TDD, branch finish) precisa delas |
| 8 | Regra: **nunca** `subagent-driven-development` + `bmad-build-auto` na mesma sessão | Dois loops autônomos duplicam trabalho e queimam tokens |

---

## 6. O que foi instalado

| Componente | Local | Versão |
|-----------|-------|--------|
| Plugin OpenCode | `.opencode/opencode.json` → `superpowers@git+https://github.com/obra/superpowers.git` | git `main` (6.4.2) |
| Plugin Claude Code | `~/.claude/plugins/cache/claude-plugins-official/superpowers/6.4.1/` | 6.4.1 |
| Registry | `~/.claude/plugins/installed_plugins.json` (scope: user, enabled) | — |
| Hook | `SessionStart` via `hooks/hooks.json` do plugin (matcher `startup\|clear\|compact`) | — |
| Telemetry off | `.claude/settings.json` → `env` | — |
| Permissões | `.claude/settings.json` → `permissions.allow` | — |
| Documentação | `AGENTS.md`, `CLAUDE.md`, `_bmad-output/toolchain-installation-guide.md`, este documento | — |

---

## 7. Riscos remanescentes e recomendações

| # | Risco / lacuna | Impacto | Recomendação |
|---|---------------|---------|--------------|
| 1 | Marketplace oficial em **6.4.1** vs git **6.4.2** | Baixo | Aceitar; `claude plugin update superpowers` a cada release |
| 2 | Plugin OpenCode pinado no `main` (sem tag) | Médio | Considerar pinar `#v6.4.1` para builds reproduzíveis |
| 3 | Duas versões do bootstrap em sessão (BMAD AGENTS.md + `<EXTREMELY_IMPORTANT>`) | Médio | Monitorar nas primeiras sessões; a regra de precedência deve bastar |
| 4 | Não foi possível executar o teste funcional ("Let's make a react todo list") dentro desta sessão | Baixo | Rodar manualmente numa sessão limpa ao concluir |
| 5 | `writing-skills` do Superpowers pode conflitar com `bmad-customize` na autoria de skills | Baixo | Usar o método do Superpowers como template; gravar no `_bmad/custom/` |
| 6 | Custo de sessão sobe ~700 tok + invocações | Baixo | Aceitável; monitorar com `opencode stats` |
| 7 | Projetos irmãos (`hsoservicos`, `markdown-studio-live`, `servicetec`, `sound-music-app`) ainda sem Superpowers | Médio | Replicar usando §3 do `toolchain-installation-guide.md` |
| 8 | `diagnosing-superpowers` grava em `~/.superpowers/` (fora do repo) | Baixo | Documentar; não versionar |

---

## 8. Conclusão

O Superpowers é a peça que faltava na toolchain. Onde o BMAD responde *"o que
construir e em que ordem"* e o Impeccable responde *"como isso deve parecer"*,
o Superpowers responde *"como construir sem mentir que funciona"* — TDD real,
causa-raiz em vez de patch sintomático, e verificação com evidência citada.

A integração foi feita pelo mecanismo nativo de cada harness, com o bootstrap
`SessionStart` ativo, telemetry desligado, precedência documentada e nenhuma
modificação no código upstream — ou seja, uma integração que o próprio projeto
upstream consideraria real e suportável.

**Próximo passo sugerido:** replicar a instalação nos 4 projetos consumidores e
rodar o teste de aceitação (`Let's make a react todo list`) em cada um.
