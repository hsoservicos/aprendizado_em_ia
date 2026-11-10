# Manual de Uso — Riaworks Waves 3.6.12.4

> **Pré-requisito:** ter seguido o **Manual de Instalação** (`01-MANUAL-INSTALACAO-BMAD-E-WAVES.md`)
> até o fim, inclusive o passo 10 — ou seja, o seu projeto já tem o BMAD 6.12.4, o Waves 3.6.12.4
> e um `sprint-status.yaml` com stories prontas.
>
> **Sobre os comandos por sistema:** os comandos `waves ...` são **idênticos** no Linux, no
> macOS e no Windows com WSL. No **Windows nativo** (PowerShell, experimental) também são os
> mesmos; o que muda está sinalizado com **Windows nativo** quando for o caso.

## O que mudou desde a 3.0.0

| Novidade                                                                                                                                                           | Onde ler                                                            |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------- |
| O Waves exige o **BMAD Method 6.12.4** ou mais novo; abaixo disso, a instalação não instala nada e o `waves validate` acusa.                                       | Manual de Instalação, seção 11.1                                    |
| **`/waves-tests`**: a configuração de testes do projeto (`_waves/tests_memory.toml`), escrita com você uma vez. É **obrigatória** para executar um plano de ondas. | [7.2a](#72a-antes-de-planejar-a-configuração-de-testes-waves-tests) |
| **`/waves-config`** e **`waves config`**: o mapa de toda a configuração que um run lê, com o estado de cada arquivo e quem cuida de cada um.                       | [2](#2-checklist-antes-de-qualquer-uso)                             |
| **Quem roda cada papel** das ondas — qual IA (CLI), qual modelo e qual **esforço** — vem do `policy.toml` e aparece no plano.                                      | [7.2b](#72b-quem-roda-cada-papel-cli-modelo-e-esforço)              |
| A **retrospectiva de fim de épico** agora também funciona no run por LLM (`[gates] retrospective`).                                                                | [4.2](#42-como-funciona) e [5.1](#51-como-funciona)                 |
| As personalizações das skills do Waves ficam em **`_waves/custom/`** (antes, `_bmad/custom/`); a instalação move as antigas sozinha.                               | [7.6](#76-projeto-sem-repositório-remoto-githubgitlab)              |
| O painel `waves tui` ganhou as colunas `wave`, `atdd` e `agent`.                                                                                                   | [8](#8-acompanhar-o-painel-waves-tui)                               |

---

## Sumário

1. [Conceitos em 2 minutos](#1-conceitos-em-2-minutos)
2. [Checklist antes de qualquer uso](#2-checklist-antes-de-qualquer-uso)
3. [O mapa: os quatro jeitos de construir](#3-o-mapa-os-quatro-jeitos-de-construir)
4. [Jeito A — o "bmad-loop normal" e o equivalente no Waves (determinístico, por CLI)](#4-jeito-a--o-bmad-loop-normal-e-o-equivalente-no-waves-determinístico-por-cli)
5. [Jeito B — `waves run`: orquestração por LLM, por CLI comum](#5-jeito-b--waves-run-orquestração-por-llm-por-cli-comum)
6. [Jeito C — `/waves-master-tui`: a porta conversacional (LLM ou determinístico)](#6-jeito-c--waves-master-tui-a-porta-conversacional-llm-ou-determinístico)
7. [Jeito D — `/waves-master-parallelism`: ondas e frentes](#7-jeito-d--waves-master-parallelism-ondas-e-frentes)
8. [Acompanhar: o painel `waves tui`](#8-acompanhar-o-painel-waves-tui)
9. [Quando o run para: retomar, resolver, parar](#9-quando-o-run-para-retomar-resolver-parar)
10. [Qual jeito usar? (tabela de decisão)](#10-qual-jeito-usar-tabela-de-decisão)
11. [Colinha de comandos](#11-colinha-de-comandos)
12. [Problemas comuns no uso](#12-problemas-comuns-no-uso)

---

## 1. Conceitos em 2 minutos

| Termo              | O que significa                                                                                                                                                                        |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Story**          | Uma funcionalidade pequena, escrita pelo BMAD. Ex.: `1-2-cadastro-de-usuario`.                                                                                                         |
| **Épico**          | Um grupo de stories (o épico 1 tem as stories `1-1`, `1-2`, ...).                                                                                                                      |
| **Sprint status**  | O arquivo `sprint-status.yaml`: cada story e seu estado (`backlog`, `ready-for-dev`, `in-progress`, `review`, `done`...). É a "lista de tarefas" que o Waves segue.                    |
| **Run**            | Uma execução do Waves: ele pega stories e as constrói, uma após a outra. Cada run tem um **id** (ex.: `20260925-101500-a1b2`) e um **apelido curto** (`a1b2`).                         |
| **Sessão**         | Uma janela do Claude Code que o Waves abre sozinho para fazer um trabalho (implementar, revisar). Ela nasce, trabalha e é fechada.                                                     |
| **Ciclo da story** | `escolher → implementar (dev) → verificar → revisar (review) → verificar de novo → commit`. É o mesmo em todos os jeitos de uso.                                                       |
| **Worktree**       | Uma "cópia de trabalho" separada do mesmo repositório Git. Permite construir uma story sem mexer na sua pasta principal — e construir várias ao mesmo tempo.                           |
| **Onda**           | Um grupo de stories que **podem ser construídas ao mesmo tempo** sem pisar uma na outra. As ondas rodam **uma depois da outra**: a onda 2 só começa depois da onda 1 entrar no código. |
| **Frente**         | Uma "fila" dentro de uma onda. Cada frente tem a sua worktree e constrói as suas stories em ordem. **As frentes de uma mesma onda rodam em paralelo.**                                 |
| **Merge**          | Juntar o trabalho de uma frente (ou story) de volta ao branch principal.                                                                                                               |

**O ciclo de uma story, em desenho:**

```text
 sprint-status.yaml: 1-2-cadastro: ready-for-dev
   │
   ├─ DEV      o Waves abre uma sessão do Claude: "/bmad-build-auto 1-2-cadastro"
   │           (planeja, implementa, se autorrevisa e faz commit)
   ├─ VERIFY   o Waves confere no disco: spec existe, status done, diff não vazio,
   │           e roda os SEUS testes ([verify] commands)
   ├─ REVIEW   sessão NOVA do Claude, sem memória da anterior, revisa o que foi feito
   ├─ VERIFY   confere tudo de novo
   └─ COMMIT   um commit por story; a story vira "done" no sprint-status.yaml
```

---

## 2. Checklist antes de qualquer uso

Rode dentro da pasta do projeto:

```bash
git status          # tem que dizer "nothing to commit, working tree clean"
waves validate      # tudo "ok" (avisos de TEA podem ser ignorados)
waves run --dry-run # mostra QUAIS stories seriam construídas, sem construir nada
```

Se o `git status` mostrar arquivos modificados, salve antes:

```bash
git add -A
git commit -m "antes do run"
```

**Por que a árvore precisa estar limpa?** O Waves faz commits sozinho. Se houver mudanças
suas pendentes, ele não saberia separar o seu trabalho do dele — então ele se recusa a
começar.

**Recomendado: diga ao Waves como testar o seu projeto.** Abra `.waves/loop/policy.toml`
(ou use o painel: `waves tui` e tecla `g`) e preencha os comandos de teste. Exemplo para
um projeto Python e um Node:

```toml
[verify]
commands = ["pytest -q"]              # Python
# commands = ["npm test", "npm run lint"]   # Node.js
```

Sem isso, o Waves confia só na revisão da IA; com isso, **nenhuma story vira `done` com
teste quebrado**.

**Para ver toda a configuração de uma vez** (novo na 3.6.12.4):

```bash
waves config
```

Ele mostra, sem mudar nada: o `policy.toml`, quem roda cada papel das ondas (IA, modelo,
esforço), a configuração de testes, o ambiente por frente, as personalizações das skills e
a versão das skills do projeto. No fim, cada pendência vem com o comando que a resolve. No
Claude, `/waves-config` faz o mesmo explicando cada linha (e, com `[A]`, ajuda a escolher
quem roda cada papel).

> Num projeto que ainda não rodou o `/waves-tests`, o `waves config` mostra
> `problem tests _waves/tests_memory.toml is missing`. Isso só impede o **paralelismo por
> ondas** (Jeito D) — veja a [seção 7.2a](#72a-antes-de-planejar-a-configuração-de-testes-waves-tests).

---

## 3. O mapa: os quatro jeitos de construir

Todos usam o **mesmo ciclo da story** (seção 1). O que muda é **quem decide quando algo sai
do previsto** e **quantas stories andam ao mesmo tempo**.

```text
                         ┌───────────────────────────────────────────────┐
                         │   UMA STORY POR VEZ (loop)                     │
                         │                                                │
   Você digita           │   A. waves run --deterministic                 │  ← = "bmad-loop normal"
   no terminal  ───────► │      roteiro fixo; para e espera você          │
                         │   B. waves run                                 │
                         │      uma IA "gerente" decide e segue sozinha   │
                         └───────────────────────────────────────────────┘
                                          ▲
   Você conversa         C. /waves-master-tui  ── pergunta tudo e lança A ou B,
   no Claude Code  ────►                          e vigia o run para você

                         ┌───────────────────────────────────────────────┐
   Você conversa         │   VÁRIAS STORIES AO MESMO TEMPO (ondas)        │
   no Claude Code  ────► │   D. /waves-master-parallelism                 │
                         │      [P] planeja ondas e frentes               │
                         │      executa em SÉRIE (1 frente)               │
                         │      ou em PARALELO (2+ frentes por onda)      │
                         └───────────────────────────────────────────────┘
```

| Jeito | Como você usa                              | Quem decide no imprevisto               | Stories ao mesmo tempo | Ideal para                                                        |
| ----- | ------------------------------------------ | --------------------------------------- | ---------------------- | ----------------------------------------------------------------- |
| **A** | `waves run --deterministic` no terminal    | Ninguém: o run **para** e espera você   | 1                      | Quem quer previsibilidade e custo mínimo, e vai estar por perto.  |
| **B** | `waves run` no terminal                    | Uma **IA orquestradora**, dentro do run | 1 (ou mais, com plano) | Rodar sozinho por horas, à noite.                                 |
| **C** | `/waves-master-tui` no Claude Code         | A ou B (você escolhe) + um **vigia**    | igual a A ou B         | Quem prefere conversar a decorar comandos; quem quer vigilância.  |
| **D** | `/waves-master-parallelism` no Claude Code | O **master** da onda (IA)               | 1 por frente           | Épicos grandes, para terminar mais rápido sem conflitos de merge. |

---

## 4. Jeito A — o "bmad-loop normal" e o equivalente no Waves (determinístico, por CLI)

### 4.1 O que é o "bmad-loop normal"

O **bmad-loop** é o projeto original da BMad Code (aparece como **"BMad Loop"** no instalador
do BMAD). O Waves é um **fork** dele: o motor do bmad-loop continua dentro do Waves,
**sem alterações**, e se chama **modo determinístico**.

|                       | **bmad-loop (original)** | **Waves — modo determinístico** |
| --------------------- | ------------------------ | ------------------------------- |
| Comando               | `bmad-loop run`          | `waves run --deterministic`     |
| Painel                | `bmad-loop tui`          | `waves tui`                     |
| Pasta de estado       | `.bmad-loop/`            | `.waves/loop/`                  |
| Skills                | `bmad-loop-*`            | `waves-*`                       |
| Quem decide           | roteiro fixo em Python   | o mesmo roteiro fixo            |
| Orquestração por IA   | não existe               | existe (é o Jeito B)            |
| Paralelismo por ondas | não existe               | existe (é o Jeito D)            |

**Resumo:** se você conhece o `bmad-loop`, o `waves run --deterministic` é o mesmo
comportamento com outro nome. **Não há motivo para instalar os dois** no mesmo projeto — e,
se instalar, **nunca rode os dois ao mesmo tempo**: eles disputariam o mesmo
`sprint-status.yaml`.

### 4.2 Como funciona

Um **roteiro fixo, em Python** (sem IA no controle) decide o próximo passo. A IA só trabalha
dentro das sessões (implementar, revisar). Quando acontece algo que o roteiro não prevê —
uma revisão que não converge, uma contradição na spec, uma sessão que morreu sem resultado —
o run **pausa** e espera uma pessoa.

- ✅ Previsível, auditável e o mais barato.
- ⚠️ Precisa de alguém por perto (ou do vigia do Jeito C) para destravar as pausas.
- ⚠️ Por padrão, pausa **ao final de cada épico** (`[gates] mode = "per-epic"`), para você
  conferir antes de seguir.
- No fim de cada épico, o run também cuida da **retrospectiva** do BMAD, conforme
  `[gates] retrospective` no `policy.toml`: `"notify"` (padrão) só sugere rodar
  `/bmad-retrospective`; `"auto"` roda a retrospectiva sozinho numa sessão e faz commit do
  documento; `"never"` desliga.

### 4.3 Comandos (Linux, macOS, WSL e Windows nativo)

```bash
# ver o que seria feito, sem fazer
waves run --deterministic --dry-run

# construir todo o backlog pronto
waves run --deterministic

# só o épico 2
waves run --deterministic --epic 2

# só uma story
waves run --deterministic --story 2-3

# no máximo 3 stories (bom para um primeiro teste)
waves run --deterministic --max-stories 3
```

O comando fica "preso" ao terminal enquanto o run acontece. **Não feche a janela.** Para
poder fechar, veja [Rodar sem prender o terminal](#43a-rodar-sem-prender-o-terminal).

### 4.3a Rodar sem prender o terminal

**Linux, macOS e WSL — com tmux** (recomendado):

```bash
tmux new -s waves                  # abre uma "janela escondível"
waves run --deterministic          # roda lá dentro
# para sair SEM parar o run: aperte Ctrl+b, solte, e aperte d
tmux attach -t waves               # para voltar a ver depois
```

**Windows nativo:** deixe a janela do PowerShell aberta enquanto o run acontece (ou use o
painel `waves tui`, tecla `r`, que lança o run numa sessão própria que sobrevive ao
fechamento do painel).

### 4.4 Quando ele pausa

```bash
waves list                 # lista os runs, com o apelido curto (ex.: a1b2)
waves status a1b2          # por que parou
waves resume a1b2          # continua (pausa de fim de épico, interrupção)
waves resolve a1b2         # escalação CRÍTICA: abre uma conversa para corrigir a spec
```

> ⚠️ Run **determinístico** retoma com `waves resume <id>`. Run **por LLM** retoma com
> `waves run --resume <id>`. Cada comando recusa o run do outro e diz qual usar.

---

## 5. Jeito B — `waves run`: orquestração por LLM, por CLI comum

### 5.1 Como funciona

Desde a 3.0.0, **`waves run` sem nada é a orquestração por LLM** — o padrão do Waves.

Além das sessões de trabalho, o Waves abre uma **sessão orquestradora** (uma IA "gerente")
que vive dentro do run. Quando algo sai do previsto, ela **lê o log** da sessão que falhou,
**forma uma hipótese**, decide (refazer, corrigir, adiar uma parte) e **segue sem esperar
ninguém**, registrando cada decisão e o motivo no diário do run (o _journal_).

Tudo o que é irreversível (git, commits, o quadro do sprint) continua nas mãos do código
Python: a IA gerente só age por comandos controlados.

- ✅ Anda sozinho por horas; atravessa a noite.
- ⚠️ Gasta mais tokens (uma sessão a mais, a do gerente).
- ⚠️ Pausa só em 4 casos: decisão de produto genuinamente ambígua, risco de destruir
  trabalho, falha sistemática, ou você pediu para parar.
- Novo na 3.6.12.4: a **retrospectiva de fim de épico** (`[gates] retrospective`, veja o
  Jeito A) também vale aqui — no fim de cada épico concluído, o gerente sugere ou roda a
  `/bmad-retrospective`, conforme o `policy.toml`.

### 5.2 Comandos

```bash
waves run --dry-run            # prévia
waves run                      # todo o backlog pronto
waves run --epic 2             # só o épico 2
waves run --story 2-3          # só uma story
waves run --max-stories 3      # no máximo 3
waves run --resume a1b2        # retomar um run POR LLM que pausou
```

`llm-run` é o nome antigo do mesmo comando e continua funcionando.

### 5.3 Escolher qual modelo é o "gerente" (opcional)

Em `.waves/loop/policy.toml` (ou `waves tui` → `g`):

```toml
[adapter.orchestrator]
model = "opus"        # o modelo que segura o controle do run
effort = "high"       # (opcional) esforço de raciocínio: low, medium, high, xhigh ou max

[adapter.dev]
model = "sonnet"      # (opcional) o modelo que implementa
```

O `effort` é novo na 3.6.12.4 e vale para qualquer papel; uma IA (CLI) que não aceita
esforço simplesmente o ignora.

Para **desligar** a orquestração por LLM no projeto (e obrigar o modo determinístico):

```toml
[llm]
enabled = false
```

---

## 6. Jeito C — `/waves-master-tui`: a porta conversacional (LLM ou determinístico)

### 6.1 O que é

Uma **skill** (um comando do Claude Code) que faz, por conversa, tudo que os Jeitos A e B
fazem por comando — e ainda **vigia o run** para você. Ela pergunta **uma coisa de cada vez**,
explica cada opção, mostra o comando exato que vai rodar e **só lança depois que você
confirma**.

**"Por LLM" x "por CLI comum" — a diferença em uma frase:**

- **Por CLI comum** = você mesmo digita `waves run` (Jeito B) ou `waves run --deterministic`
  (Jeito A) no terminal, e acompanha por conta própria.
- **Pela `/waves-master-tui`** = você conversa com o Claude, ele lança **o mesmo comando** e
  arma um **vigia** que mede a saúde do run de tempos em tempos.

Dentro da skill, a **primeira pergunta** é o modo do run:

| Na skill você escolhe                 | Ela lança                   | O vigia...                                                                                                         |
| ------------------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **[O] Orquestração por LLM** (padrão) | `waves run`                 | **só observa** (a cada ~10 min): supervisor vivo? turnos avançando? pausou sem ninguém ver? Nunca escreve no run.  |
| **[D] Determinístico**                | `waves run --deterministic` | **age**: quando o run para, executa o "runbook" certo (retomar, resolver, limpar) — ou só avisa, se você preferir. |

### 6.2 Como abrir

```bash
cd ~/projetos/meu-app       # Windows nativo: cd C:\projetos\meu-app
claude
```

Dentro do Claude, digite:

```text
/waves-master-tui
```

> ⚠️ **Mantenha essa janela do Claude aberta** enquanto quiser o vigia: ele vive nessa
> conversa. O run em si continua mesmo que você feche o Claude — só o vigia para.

### 6.3 As perguntas, uma por vez

São **5 perguntas** no modo por LLM e **6** no determinístico. Em cada uma, **o padrão
vem primeiro** (no painel de perguntas do Claude Code, é só apertar Enter).

| #   | Pergunta                                     | Opções (padrão em **negrito**)                                                                                                                                                                                                   |
| --- | -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Modo do run**                              | **[O] Orquestração por LLM** · [D] Determinístico. _Não dá para trocar no meio do run._                                                                                                                                          |
| 2   | **Escopo**                                   | **[B] Backlog inteiro** · [E] Um épico (`--epic N`) · [S] Uma story (`--story`) · [N] No máximo N stories · [P] Um plano de ondas (`--plan <arquivo>`, veja o Jeito D).                                                          |
| 3   | **Vigias**                                   | LLM: **armar o `pulse.py`** (só observa). Determinístico: **armar os dois** — o _watch_ (a cada 2 min, reage na hora a mudanças) e o _loop por LLM_ (a cada 10 min, percebe o que **deixou** de acontecer); ou só um, ou nenhum. |
| 4   | **Autonomia do vigia** _(só determinístico)_ | **[A] Agir** — executa o runbook sozinho (só pergunta antes de apagar trabalho) · [S] Só avisar — diz o que viu e qual runbook resolve, e para.                                                                                  |
| 5   | **Limiares**                                 | **Manter os do `rules.toml`** · ou mudar algum (ex.: quantos minutos de log parado antes de suspeitar de travamento).                                                                                                            |
| 6   | **Resumo e confirmação**                     | Mostra modo, escopo, vigia, limiares e **o comando exato**. **[L] Lançar** · [M] Mudar algo · [C] Cancelar.                                                                                                                      |

Exemplo de resumo que ela mostra antes de lançar:

```text
modo:      orquestração por LLM            (waves run)
escopo:    backlog inteiro
vigia:     pulse.py em laço, a cada 10 min
limiares:  os do rules.toml
comando:   setsid nohup waves run --project /home/voce/projetos/meu-app > .../engine-run.out 2>&1 < /dev/null &
```

### 6.4 O menu de atalhos

Você pode chamar a skill já com uma letra (ex.: `/waves-master-tui P`):

| Letra | Faz                                                                                             |
| ----- | ----------------------------------------------------------------------------------------------- |
| `[P]` | **Padrão em tudo**: LLM, backlog inteiro, vigia armado. Mostra o resumo e lança sem perguntar.  |
| `[R]` | **Retomar** o run pausado/parado, no modo em que ele nasceu.                                    |
| `[V]` | **Vigiar** um run que já existe (arma o vigia certo para o modo dele).                          |
| `[1]` | **Uma leitura**: mede a saúde do run uma vez e responde.                                        |
| `[F]` | **Falar** com a sessão viva (manda uma linha para o Claude que está trabalhando, com registro). |
| `[T]` | Mostra o comando do **painel** (`waves tui`) para **você** rodar no seu terminal.               |

Frases que ela também entende: _"o run travou"_, _"retoma o run"_, _"diz em andamento mas nada
acontece"_, _"qual a diferença entre determinístico e por LLM"_.

> **Windows nativo:** a skill lança o run com `setsid nohup`, que é de Linux/macOS. No
> Windows nativo, prefira o WSL; ou lance você mesmo pelo painel (`waves tui`, tecla `r`) e
> use a skill com `[V]`, `[1]` e `[R]`.

---

## 7. Jeito D — `/waves-master-parallelism`: ondas e frentes

### 7.1 A ideia

Construir várias stories **ao mesmo tempo** é rápido, mas perigoso: duas IAs mexendo no mesmo
arquivo geram **conflito de merge**. A `waves-master-parallelism` resolve isso **antes de
escrever qualquer código**: lê todas as stories do épico, mede **onde cada par de stories
colide** (mesmo arquivo, mesma função, uma depende da outra) e monta um **plano de ondas e
frentes** em que stories que colidem **nunca** rodam juntas.

```text
  ONDA 0  ── preparo: testes de aceitação "esqueleto" (ATDD), documentação
     │
  ONDA 1  ── Frente A: 1-1 → 1-3          ┐
     │       Frente B: 1-2                ├─ rodam AO MESMO TEMPO (paralelo)
     │       Frente C: 1-4                ┘
     │       merge na ordem da grade: A, depois B, depois C
     ▼
  ONDA 2  ── Frente A: 1-5 → 1-6          ┐  só começa depois que a onda 1
             Frente B: 1-7                ┘  entrou inteira no código
```

**Ponto importante:** "multi-ondas em paralelo" quer dizer **várias frentes em paralelo
dentro de cada onda**. As **ondas** em si são sempre uma depois da outra — é isso que garante
zero conflito.

São **duas fases**:

1. **Planejar** (`[P]`): conversa com você, mede, escreve o plano, colhe aprovações.
2. **Executar**: com o plano aprovado, alguém vira o **master** e conduz as ondas.

### 7.2 Fase 1 — Planejar

> ⚠️ **Antes do primeiro plano, rode `/waves-tests` uma vez no projeto** (veja a
> [seção 7.2a](#72a-antes-de-planejar-a-configuração-de-testes-waves-tests)). Sem a configuração
> de testes, o planejador para na pergunta 6b e o plano não pode ser executado.

```bash
cd ~/projetos/meu-app
claude
```

```text
/waves-master-parallelism 1
```

(`1` = o número do épico. Também aceita um conjunto de stories de épicos diferentes, ex.:
`/waves-master-parallelism 15.2, 16.2, 19.1`. Sem argumento, ela mostra o menu.)

Ela anuncia o que **não** vai perguntar e faz **12 perguntas, uma por mensagem** (mais a 6b,
só se faltar a configuração de testes, e a 10b, que mostra quem roda cada papel). Você pode
responder `defaults` a qualquer momento para aceitar o padrão desta e de todas as seguintes.

| #   | Pergunta                                           | Padrão e o que significa                                                                                                                                                                                                                                                   |
| --- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0   | Como responder                                     | **Uma por vez** · ou todos os padrões direto.                                                                                                                                                                                                                              |
| 1   | **Onde o master trabalha**                         | **Worktree própria** (`waves-<épico>`), com um branch de integração só dela — permite rodar vários planos na mesma máquina; você junta ao branch principal depois · ou **a worktree ativa** (integra direto no seu branch atual; o mais simples, mas só um plano por vez). |
| 2   | Onde fica a fila de testes                         | _(só com worktree própria)_ **Uma fila para o projeto** (dois testes completos nunca rodam juntos) · ou uma por master (só se cada frente tiver banco de dados próprio). Ela mede os núcleos da sua máquina e sugere.                                                      |
| 3   | **Máximo de frentes**                              | **2** · 1 (**série**: sem paralelismo) · 3 · outro número.                                                                                                                                                                                                                 |
| 4   | Recurso de teste por frente                        | **Próprio por frente** (ex.: um banco para cada) · ou compartilhado (as frentes fazem fila).                                                                                                                                                                               |
| 5   | Stories fora do escopo                             | **Nenhuma** · ou liste as que ficam de fora.                                                                                                                                                                                                                               |
| 6   | Fatiar stories ou concentrar um recurso sequencial | **Sim, propor** (cada proposta vai para sua aprovação) · não, manter cada story inteira.                                                                                                                                                                                   |
| 6b  | Configuração de testes _(só se faltar)_            | **Parar e rodar `/waves-tests` [D] agora** (depois, commite o arquivo e retome o plano com `[A]`) · ou deixar o plano em `draft` até a configuração existir.                                                                                                               |
| 7   | Batimento no chat                                  | **A cada 30 min** o master diz como está · outro intervalo.                                                                                                                                                                                                                |
| 8   | Objetivo do run                                    | **Todas as stories `done` + testes verdes** · outro.                                                                                                                                                                                                                       |
| 9   | Merge                                              | **O master faz merge por story e push por merge** · merge só no fim · ou **você** faz os merges (o master para cada story em `ready-to-merge`).                                                                                                                            |
| 10  | Testes de aceitação (ATDD)                         | **Sim, na onda 0** (um teste por critério de aceite) quando a skill de ATDD do TEA está instalada · **não**, quando não está (ela avisa e não promete uma etapa que nada executa).                                                                                         |
| 10b | Quem roda cada papel                               | **Como está no `policy.toml`** — ela mostra uma tabela por papel (IA, modelo, esforço) e grava no plano · ou "vou editar a política antes" (ela relê e mostra de novo). Veja a [seção 7.2b](#72b-quem-roda-cada-papel-cli-modelo-e-esforço).                               |
| 11  | TEA _(só se instalado)_                            | **Uma vez por épico concluído** · pular.                                                                                                                                                                                                                                   |
| 12  | Aceite visual _(só se houver telas)_               | **Há ferramenta de navegador** (Playwright MCP) · dispensar para certas stories (vai para aprovação) · não despachar essas stories sem navegador.                                                                                                                          |

Depois ela trabalha **em silêncio** (uma linha por fase: `phase 1: ...`), e no fim:

1. **Aprovações** — cada proposta (fatiar story, dispensar aceite visual...) vem numa
   pergunta: **aprovar** · rejeitar · ajustar.
2. **Decisão de despacho** — com os números do plano na tela:

   | Opção                     | Significado                                      |
   | ------------------------- | ------------------------------------------------ |
   | **`autonomous`** (padrão) | Todas as ondas de uma vez, **0 paradas**.        |
   | `checkpoint-per-wave`     | Para **ao fim de cada onda** para você conferir. |
   | `human-in-the-loop`       | Para **a cada story**.                           |

3. **Teto de horas** — padrão **24 h**. (Se o teto for menor que a estimativa, ela avisa: é
   uma parada agendada, não segurança.)

Resultado: um arquivo de plano em `_bmad-output/planning-artifacts/`, com nome
`<data-hora>-epic-<N>-plan.md` e `status: approved`. A última mensagem é:

```text
plan: <caminho> · status: approved · dispatch: autonomous/24h · generated: <data>
Ready. Run: [E] (hands over to waves-core-parallelism)
```

**Outras letras do menu de planejamento:**

| Letra | Faz                                                                                         |
| ----- | ------------------------------------------------------------------------------------------- |
| `[A]` | Retoma um plano do ponto onde parou (aprovações → despacho → pronto).                       |
| `[R]` | Re-mede o plano contra o código de hoje (se o branch andou desde o plano, faça isso antes). |
| `[V]` | Valida o plano contra o sprint-status (o que já mudou de estado?).                          |

### 7.2a Antes de planejar: a configuração de testes (`/waves-tests`)

Quem decide **quais testes uma story roda** e **quantas frentes podem testar ao mesmo tempo**
é você, uma vez por projeto, num arquivo versionado: `_waves/tests_memory.toml`. Nenhuma
sessão adivinha isso no meio do run. No Claude, dentro do projeto:

```text
/waves-tests
```

Escolha `[D]` (descobrir). Ela lê como o seu projeto roda os testes e pergunta, uma coisa por
mensagem:

- qual é o **tipo** de cada conjunto de testes — unit, integration, API ou E2E —, decidido pelo
  que o teste usa (só o próprio processo · um recurso de fora, como um banco · um servidor por
  HTTP · um navegador de verdade), nunca pela ferramenta;
- **quantas frentes podem rodar cada tipo ao mesmo tempo** (o padrão é 1 sempre que um recurso
  é compartilhado ou desconhecido);
- se uma story roda **só os testes que ela tocou** ou a suíte inteira;
- se o **fechamento do épico** roda a suíte inteira.

Ela escreve o arquivo, **testa cada comando de verdade** e mostra o que achou. Depois, salve:

```bash
git add _waves/tests_memory.toml
git commit -m "configuração de testes do Waves"
```

> O commit precisa estar no **branch de integração** (o que o plano usa): as frentes nascem
> dele, e um arquivo que só existe na sua pasta não chega a nenhuma delas.

Com a configuração, cada story passa por um **portão de testes**: roda os testes que ela
criou ou mudou, mais os testes de aceitação dela (ATDD), na fila de cada tipo, e **qualquer
vermelho devolve a story** para a frente. O merge só entra com um relatório verde, e a suíte
inteira roda uma vez, no fechamento do épico.

`/waves-tests C` (conferir) compara a configuração com o código de hoje — use depois de mudar
a forma de rodar os testes do projeto.

### 7.2b Quem roda cada papel: CLI, modelo e esforço

Num run de ondas, o master despacha **papéis**: `story` (a frente que constrói a story),
`close` (partes do fechamento do épico), `diagnosis`, `lens`, `repair` e `judge`. Para cada
um, o `.waves/loop/policy.toml` diz **qual IA** (CLI: `claude`, `codex`...), **qual modelo** e
**qual esforço**:

```toml
[adapter]
name = "claude"        # padrão para todos os papéis

[adapter.story]
model = "sonnet"
effort = "medium"      # low, medium, high, xhigh ou max

[adapter.judge]
name = "codex"         # este papel roda no Codex
```

O jeito mais fácil de mexer é `/waves-config A`: uma pergunta por papel; ela grava no
`policy.toml` e regenera os agentes do Waves (`.claude/agents/waves-agent*.md`). Para
conferir, `waves config`. O planejador mostra essa tabela na pergunta 10b e a grava no plano —
durante o run, o master segue o plano e não relê a política.

> Um papel numa **outra** IA (ex.: `codex` num master que roda no Claude) exige essa IA
> instalada e registrada no projeto — no instalador, `--cli codex` (Windows nativo:
> `-Cli claude,codex`).

### 7.3 Fase 2 — Executar: SÉRIE (1 onda por vez, 1 story por vez)

**"Série"** = uma story de cada vez, na ordem do plano — sem paralelismo. É o jeito mais
seguro de usar um plano, e o certo quando:

- é a primeira vez que você usa o Waves no projeto;
- as stories usam **um único banco de dados** compartilhado;
- a máquina é modesta.

Duas formas de ter série:

**(a) No plano:** na pergunta **3/12**, responda **1 front**. O plano vira um cronograma: cada
onda tem uma frente só.

**(b) No loop, com qualquer plano:** mande o `waves run` seguir o plano **com
`max_parallel = 1`** (que já é o padrão do `policy.toml`):

```toml
[scm]
max_parallel = 1
```

```bash
# troque pelo caminho do seu plano
PLANO=_bmad-output/planning-artifacts/2026-09-25-1030-epic-1-plan.md

waves run --plan "$PLANO" --dry-run               # mostra o cronograma: onda, frente, story
waves run --plan "$PLANO"                          # LLM (padrão)
waves run --deterministic --plan "$PLANO"          # ou determinístico
```

**Windows nativo (PowerShell):**

```powershell
$PLANO = "_bmad-output\planning-artifacts\2026-09-25-1030-epic-1-plan.md"
waves run --plan $PLANO --dry-run
waves run --plan $PLANO
```

O run pega as stories **onda por onda, frentes na ordem de merge**, uma de cada vez. Uma
story de uma onda posterior nunca começa antes da anterior.

### 7.4 Fase 2 — Executar: PARALELO (várias frentes por onda)

Três formas. Todas respeitam a regra: **ondas em sequência, frentes da onda em paralelo,
merge na ordem da grade**.

#### Forma 1 — `[E]`: o próprio Claude vira o master (sem o orquestrador Python)

Abra uma sessão **nova** do Claude (o plano está no disco; uma sessão limpa tem mais
"fôlego") e digite:

```text
/waves-master-parallelism E
```

A sessão carrega a `waves-core-parallelism` e **se torna o master**: cria a worktree,
despacha cada frente como um **subagente** do Claude, faz os merges na ordem da grade, roda
os testes gerais, atualiza o sprint-status e **não pergunta nada** — todas as perguntas foram
feitas no planejamento. Decisões de detalhe ela toma sozinha e registra; o que for decisão de
produto ela **não** decide: constrói com uma frente extra, adia a story, ou deixa a story
esperando você (`awaiting-owner`) enquanto o resto segue.

- ✅ Não precisa do `waves run`; só do Claude Code (com subagentes).
- ⚠️ **Mantenha essa janela do Claude aberta** até o fim. Se ela morrer, abra outra e use:

  ```text
  /waves-master-parallelism C      ← continua o run de onde parou (lê o estado do disco)
  /waves-master-parallelism S      ← só mostra o status, sem mexer em nada
  ```

- O estado fica em arquivos ao lado do plano: `<data-hora>-epic-<N>-run.yaml` e um relatório
  por onda `<data-hora>-epic-<N>-wave-<n>.md`.

#### Forma 2 — `waves run --plan` por LLM, com várias frentes

No `.waves/loop/policy.toml`:

```toml
[scm]
isolation = "worktree"   # cada story na sua própria worktree — NECESSÁRIO para paralelo
max_parallel = 2         # quantas stories ao mesmo tempo (use o nº de frentes do plano)
```

> ⚠️ **Não esqueça o `isolation = "worktree"`.** Sem ele, cada story em paralelo
> precisaria de uma pasta só para ela e não teria — então o Waves roda o plano **em série**
> (uma story por vez), nos dois modos, e o `waves validate` avisa com
> `policy.parallel-needs-worktree`.

```bash
waves run --plan "$PLANO"
```

A IA orquestradora abre até `max_parallel` stories da onda atual ao mesmo tempo (uma por
frente), espera, e só avança para a próxima onda quando a atual estiver toda integrada. O
merge segue a ordem da grade; se uma frente anterior mudou o código, a story é **rebaseada e
retestada** antes de entrar.

#### Forma 3 — `waves run --deterministic --plan`, com várias frentes

Mesma configuração da Forma 2 (`isolation = "worktree"` e `max_parallel > 1`):

```bash
waves run --deterministic --plan "$PLANO"
```

O run vira o **master da onda** e lança **um run filho por frente** (eles aparecem em
`waves list`). Cada filho constrói as stories da sua frente; o master integra na ordem da
grade, retesta o que precisou de rebase e **estaciona** (adia com o motivo, branch guardado)
uma story cujo rebase conflita ou cujos testes ficam vermelhos. Uma onda que não avança
**pausa** em vez de tentar para sempre.

#### Testes em paralelo e banco de dados por frente (opcional, avançado)

Por padrão, **os testes nunca rodam dois ao mesmo tempo** (`[verify] concurrency = "queue"`):
as frentes **escrevem código** em paralelo, mas fazem **fila para testar**. Isso evita que
dois testes corrompam o mesmo banco de dados.

Se cada frente tiver o **seu próprio** banco/serviços, dá para testar em paralelo também.
Para montar isso, rode **uma vez por projeto**:

```text
/waves-provisioning
```

Ela lê o seu projeto (docker-compose, `.env`, migrações), pergunta uma coisa de cada vez,
escreve o script `scripts/waves-front.sh` (sobe/derruba o ambiente de cada frente), grava no
`policy.toml` as chaves `[scm] provision`, `teardown` e `isolated_data = true` e **testa numa
worktree de rascunho**. Só então você pode usar:

```toml
[verify]
concurrency = "parallel"   # recusado se [scm] isolated_data não for true
```

### 7.5 Série x Paralelo — resumo

|                           | **Série**                                          | **Paralelo**                                                                       |
| ------------------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Stories ao mesmo tempo    | 1                                                  | até o nº de frentes / `max_parallel`                                               |
| Como configurar           | pergunta 3/12 = **1 front**, ou `max_parallel = 1` | pergunta 3/12 = **2 ou 3**, `isolation = "worktree"`, `max_parallel = 2..3`        |
| Velocidade                | a do loop comum                                    | mais rápido (o ganho real é estimado no plano)                                     |
| Risco de conflito         | nenhum                                             | nenhum **se** o plano foi seguido (a colisão foi medida antes)                     |
| Custo de máquina / tokens | baixo                                              | maior (várias sessões do Claude ao mesmo tempo)                                    |
| Banco de dados            | um só, sem problema                                | um só funciona (testes em fila); banco por frente é melhor (`/waves-provisioning`) |
| Recomendado para          | primeira vez, projeto pequeno                      | épicos grandes, depois de um run em série bem-sucedido                             |

### 7.6 Projeto sem repositório remoto (GitHub/GitLab)

O planejador descobre o branch de integração pelo remoto (`origin`). Se o seu projeto é só
local, diga qual é o branch criando o arquivo `_waves/custom/waves-master-parallelism.toml`
(desde a 3.1.0 as personalizações das skills do Waves ficam em `_waves/custom/`, não mais em
`_bmad/custom/`):

```toml
[workflow]
integration_branch = "main"
```

E, na pergunta **9/12**, prefira **"merge só no fim"** ou **"você faz os merges"**, já que
não há para onde fazer push.

---

## 8. Acompanhar: o painel `waves tui`

Abra num terminal **seu** (não peça para o Claude abrir — é tela cheia):

```bash
waves tui
```

À esquerda: runs, árvore do sprint e itens adiados. À direita: o run selecionado, a tabela
das stories (fase, onda, aceite ATDD, agente, tentativas, tokens), o diário (_journal_) e o
log da sessão. Num run por
LLM aparece uma coluna com o raciocínio da IA gerente ao vivo. Num run com plano aparece a
linha `plan <escopo> · wave n/total · in flight k · merged k`.

| Tecla     | Ação                                                         |
| --------- | ------------------------------------------------------------ |
| `r`       | lançar um run (a janela tem o seletor de modo: LLM primeiro) |
| `s`       | lançar uma varredura de itens adiados (_sweep_)              |
| `e`       | retomar o run selecionado                                    |
| `p`       | revisar um run pausado                                       |
| `R`       | resolver uma escalação crítica                               |
| `a`       | anexar à sessão viva (ver o Claude trabalhando)              |
| `i`       | falar uma linha com a sessão em foco                         |
| `x` / `S` | parar agora / parar ao fim da story atual                    |
| `g`       | editar o `policy.toml` num formulário                        |
| `v`       | rodar o `waves validate`                                     |
| `q`       | sair (**fechar o painel NÃO para o run**)                    |

---

## 9. Quando o run para: retomar, resolver, parar

| Situação                                                | Determinístico (A)                             | Por LLM (B)                                                    |
| ------------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------------------- |
| Ver os runs                                             | `waves list`                                   | `waves list`                                                   |
| Ver por que parou                                       | `waves status <id>`                            | `waves status <id>`                                            |
| Retomar                                                 | `waves resume <id>`                            | `waves run --resume <id>`                                      |
| Escalação crítica (a spec tem contradição)              | `waves resolve <id>`                           | a IA gerente decide ou pausa; depois `waves run --resume <id>` |
| Parar agora                                             | `waves stop <id>`                              | `waves stop <id>`                                              |
| Parar ao terminar a story atual (continua retomável)    | `waves stop <id> --graceful`                   | `waves stop <id> --graceful`                                   |
| Story que depende de ação humana (comprar domínio, DNS) | `waves confirm <story>` depois de fazer a ação | idem                                                           |
| Decisões pendentes de itens adiados                     | `waves decisions`                              | `waves decisions`                                              |
| Limpar sessões tmux antigas                             | `waves cleanup`                                | `waves cleanup`                                                |

`<id>` pode ser só o apelido curto que o `waves list` mostra (ex.: `a1b2`).

Ou, sem decorar nada: abra o Claude e diga `/waves-master-tui R` (retomar) ou
`/waves-master-tui` e descreva o problema ("o run travou").

---

## 10. Qual jeito usar? (tabela de decisão)

| Se você...                                                   | Use                                                      |
| ------------------------------------------------------------ | -------------------------------------------------------- |
| está começando e quer ver uma story sendo feita              | **A** com `--max-stories 1`, acompanhando no `waves tui` |
| já usava o `bmad-loop` e quer o mesmo comportamento          | **A** — `waves run --deterministic`                      |
| quer deixar rodando à noite, sozinho                         | **B** — `waves run` (ou **C** com `[P]`)                 |
| prefere conversar a decorar comandos, e quer alguém vigiando | **C** — `/waves-master-tui`                              |
| tem um épico grande e quer terminar mais rápido              | **D** — planejar com `[P]`, executar em paralelo         |
| quer usar um plano, mas sem paralelismo                      | **D** em **série** (1 front, ou `max_parallel = 1`)      |
| não quer depender do `waves run` para o paralelismo          | **D** com `[E]` (o Claude vira o master)                 |

**Caminho sugerido para o primeiro projeto:**

1. `waves run --deterministic --max-stories 1` → veja uma story completa no `waves tui`.
2. `/waves-master-tui` com as respostas padrão → um épico inteiro por LLM, com vigia.
3. `/waves-tests` (uma vez) e `/waves-master-parallelism <épico>` → plano; primeiro em **série**,
   depois em **paralelo**.

---

## 11. Colinha de comandos

Válidos em **Linux, macOS, WSL e Windows nativo** (sempre de dentro da pasta do projeto,
ou com `--project <pasta>`):

```bash
# preparar e conferir
waves validate
waves config              # mapa de toda a configuração (não muda nada)
waves run --dry-run

# Jeito A — determinístico ("bmad-loop normal")
waves run --deterministic [--epic N | --story 2-3] [--max-stories N]
waves resume <id>
waves resolve <id>

# Jeito B — por LLM
waves run [--epic N | --story 2-3] [--max-stories N]
waves run --resume <id>

# Jeito D — plano de ondas executado pelo loop
waves run --plan <arquivo-do-plano> [--dry-run]
waves run --deterministic --plan <arquivo-do-plano>

# acompanhar e controlar
waves tui
waves list
waves status [<id>]
waves stop <id> [--graceful]
waves cleanup
waves diagnose            # relatório sem dados sensíveis, para pedir ajuda
```

No **Claude Code** (digite `claude` na pasta do projeto):

```text
/waves-master-tui              perguntas → lança o run (LLM ou determinístico) + vigia
/waves-master-tui P            tudo no padrão, lança direto
/waves-master-tui R            retomar
/waves-master-parallelism 1    planejar o épico 1 (12 perguntas)
/waves-master-parallelism E    executar o plano aprovado (a sessão vira o master)
/waves-master-parallelism C    continuar um run de ondas interrompido
/waves-master-parallelism S    status do run de ondas
/waves-tests                   (uma vez) configuração de testes — obrigatória para ondas
/waves-config                  mapa da configuração; [A] quem roda cada papel
/waves-provisioning            (uma vez) ambiente/banco próprio por frente
/waves-deferred                resolver a fila de decisões de itens adiados
/waves-resolve <story>         resolver uma escalação com você
```

Só **Linux/macOS/WSL** — rodar sem prender o terminal:

```bash
tmux new -s waves      # depois: waves run ...   | sair: Ctrl+b, d   | voltar: tmux attach -t waves
```

---

## 12. Problemas comuns no uso

| Sintoma                                                                                        | O que fazer                                                                                                                                                                          |
| ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `git worktree is not clean`                                                                    | `git add -A && git commit -m "..."` e rode de novo.                                                                                                                                  |
| O run termina "vazio", sem construir nada                                                      | Não há story `ready-for-dev` no escopo. Veja com `waves run --dry-run` e confira o `sprint-status.yaml`.                                                                             |
| A primeira sessão "trava" e dá timeout                                                         | Abra `claude` uma vez no projeto e aceite a confiança da pasta e os hooks.                                                                                                           |
| Parou no fim do épico (determinístico)                                                         | É o portão padrão (`[gates] mode = "per-epic"`). Confira e rode `waves resume <id>`. Para não parar: `mode = "none"` no `policy.toml`.                                               |
| `waves resume` recusa o run                                                                    | É um run por LLM: use `waves run --resume <id>` (e vice-versa).                                                                                                                      |
| `waves run --plan` recusa o plano                                                              | O plano está `draft`, tem aprovação pendente, foi medido em outro branch, ou cita story que o sprint-status não tem. Rode `/waves-master-parallelism A` (retomar) ou `R` (re-medir). |
| O planejador para na pergunta 6b / `waves config` mostra `_waves/tests_memory.toml is missing` | Falta a configuração de testes. Rode `/waves-tests` (opção `[D]`), faça o commit do arquivo no branch de integração e retome o plano com `/waves-master-parallelism A`.              |
| `waves init` ou o instalador dizem `below the 6.12.4 floor` / `nothing was installed`          | O BMAD do projeto é anterior ao 6.12.4. Siga a seção 11.1 do Manual de Instalação (atualizar o BMAD primeiro).                                                                       |
| `concurrency = "parallel"` é recusado                                                          | Falta `[scm] isolated_data = true` — rode `/waves-provisioning`.                                                                                                                     |
| Paralelo não paraleliza (uma story por vez)                                                    | Confira `[scm] isolation = "worktree"` **e** `max_parallel` maior que 1. O `waves validate` avisa (`policy.parallel-needs-worktree`) quando falta o `isolation`.                     |
| Quer ver o Claude trabalhando                                                                  | `waves tui` → selecione o run → `a` (anexar). Para sair sem atrapalhar: `Ctrl+b`, `d`. Para falar com ele sem risco: tecla `i`.                                                      |
| Muitas pausas no determinístico                                                                | Use o Jeito C com autonomia **Agir**, ou passe para o modo por LLM.                                                                                                                  |

Para pedir ajuda: `waves diagnose` gera um relatório sem código, caminhos nem dados pessoais.
