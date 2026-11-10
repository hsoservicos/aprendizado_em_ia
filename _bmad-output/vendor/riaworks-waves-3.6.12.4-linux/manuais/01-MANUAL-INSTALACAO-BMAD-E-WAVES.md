# Manual de Instalação — BMAD Method 6.12.4 + Riaworks Waves 3.6.12.4

> **Para quem é este manual:** para qualquer pessoa, inclusive quem nunca usou um terminal.
> Siga os passos **na ordem**, sem pular. Cada comando está pronto para copiar e colar.
> Quando um passo for diferente em cada sistema operacional, ele aparece separado em
> **Windows**, **macOS** e **Linux**: faça só o do seu sistema.
>
> **Novidade desta versão:** o Waves 3.6.12.4 exige o **BMAD Method 6.12.4 ou mais novo**. Em
> um projeto com BMAD mais antigo, o instalador do Waves para e **não instala nada** — ele
> mostra o comando para atualizar o BMAD. Já tem o Waves 3.0.0 ou 3.1.0? Vá direto para
> [Atualizar o Waves](#11-atualizar-o-waves-no-futuro).

---

## Sumário

1. [O que você vai instalar (em linguagem simples)](#1-o-que-você-vai-instalar-em-linguagem-simples)
2. [Antes de começar: o que é um terminal e como abrir](#2-antes-de-começar-o-que-é-um-terminal-e-como-abrir)
3. [Windows: escolha o caminho (WSL recomendado)](#3-windows-escolha-o-caminho-wsl-recomendado)
4. [Instalar os pré-requisitos](#4-instalar-os-pré-requisitos)
5. [Criar a pasta do projeto](#5-criar-a-pasta-do-projeto)
6. [Instalar o BMAD Method 6.12.4](#6-instalar-o-bmad-method-6124)
7. [Instalar o Riaworks Waves 3.6.12.4](#7-instalar-o-riaworks-waves-36124)
8. [Primeira abertura do Claude Code no projeto](#8-primeira-abertura-do-claude-code-no-projeto)
9. [Conferir se ficou tudo certo](#9-conferir-se-ficou-tudo-certo)
10. [Próximo passo: planejar o projeto com o BMAD](#10-próximo-passo-planejar-o-projeto-com-o-bmad)
11. [Atualizar o Waves no futuro](#11-atualizar-o-waves-no-futuro)
12. [Problemas comuns e soluções](#12-problemas-comuns-e-soluções)
13. [Desinstalar](#13-desinstalar)
14. [Resumo de uma página](#14-resumo-de-uma-página)

---

## 1. O que você vai instalar (em linguagem simples)

| Nome                        | O que é                                                                                                                                                   | Precisa?                        |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| **Git**                     | Guarda o histórico do seu código (cada mudança vira um "commit"). O Waves depende dele para tudo.                                                         | Sim (versão 2.34 ou mais nova)  |
| **Node.js**                 | Programa que roda o instalador do BMAD (o comando `npx`).                                                                                                 | Sim (versão 20.12 ou mais nova) |
| **uv**                      | Gerenciador de Python. O BMAD usa para rodar scripts; o Waves é instalado por ele.                                                                        | Sim                             |
| **tmux**                    | "Multiplexador de terminal": deixa várias janelas de terminal rodando escondidas. É onde o Waves abre as sessões do Claude. (No Windows nativo: `psmux`.) | Sim                             |
| **Claude Code**             | O assistente de programação (a IA) que escreve o código. O Waves abre sessões dele automaticamente.                                                       | Sim                             |
| **BMAD Method 6.12.4**      | O "método": agentes e skills que ajudam a planejar (PRD, arquitetura, épicos, stories) e a implementar.                                                   | Sim (6.12.4 ou mais novo)       |
| **Riaworks Waves 3.6.12.4** | O "piloto automático": pega as stories planejadas pelo BMAD e as constrói sozinho, uma a uma ou em paralelo.                                              | Sim                             |

**Glossário rápido**

- **Projeto**: a pasta onde fica o código do seu sistema.
- **Story (história)**: uma pequena funcionalidade a construir ("cadastro de usuário", "tela de login").
- **Épico**: um grupo de stories relacionadas.
- **Sprint status** (`sprint-status.yaml`): a lista de stories e em que estado cada uma está. O BMAD cria; o Waves lê e atualiza.
- **Commit**: uma "foto" salva do código no Git.

> 💡 **Tem pressa?** Vá direto ao [Resumo de uma página](#14-resumo-de-uma-página). Mas, se é a primeira vez, siga tudo.

---

## 2. Antes de começar: o que é um terminal e como abrir

O **terminal** é uma janela onde você digita comandos. Todos os passos deste manual são
comandos para colar nele.

| Sistema                            | Como abrir o terminal                                                                                                                |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Windows (WSL, recomendado)**     | Menu Iniciar → digite **Ubuntu** → Enter (depois de instalar o WSL no passo 3).                                                      |
| **Windows (nativo, experimental)** | Menu Iniciar → digite **PowerShell** → Enter. Para "modo administrador": clique com o botão direito → _Executar como administrador_. |
| **macOS**                          | `Cmd + Espaço` → digite **Terminal** → Enter.                                                                                        |
| **Linux**                          | `Ctrl + Alt + T` (Ubuntu) ou procure **Terminal** no menu de aplicativos.                                                            |

**Como colar um comando:**

- Windows (Ubuntu/WSL ou PowerShell): botão direito do mouse, ou `Ctrl + Shift + V`.
- macOS: `Cmd + V`.
- Linux: `Ctrl + Shift + V`.

Depois de colar, aperte **Enter**. Espere o comando terminar (o cursor volta a piscar
numa linha nova) antes de colar o próximo.

> ⚠️ Quando um comando pedir **senha** (`[sudo] password for ...`), digite a senha do seu
> usuário e aperte Enter. **Nada aparece enquanto você digita** — isso é normal.

---

## 3. Windows: escolha o caminho (WSL recomendado)

> Usuários de **macOS** e **Linux**: pulem para o [passo 4](#4-instalar-os-pré-requisitos).

O Waves funciona de dois jeitos no Windows:

| Caminho                            | Situação                            | Recomendação                                                                                        |
| ---------------------------------- | ----------------------------------- | --------------------------------------------------------------------------------------------------- |
| **WSL (Ubuntu dentro do Windows)** | **Suportado** — é Linux de verdade. | ✅ **Use este.** Tudo funciona igual ao Linux.                                                      |
| **Windows nativo (PowerShell)**    | **Experimental**                    | Só se você não puder usar WSL. Algumas funções (anexar à janela da sessão) ainda estão incompletas. |

### 3.1 Instalar o WSL (uma vez só)

1. Abra o **PowerShell como administrador** (Menu Iniciar → digite PowerShell → botão direito → _Executar como administrador_).
2. Cole e aperte Enter:

   ```powershell
   wsl --install -d Ubuntu
   ```

3. **Reinicie o computador** quando pedir.
4. Depois de reiniciar, abra **Ubuntu** pelo Menu Iniciar. Na primeira vez ele pede para
   criar um **usuário** e uma **senha** (anote a senha — ela será pedida nos comandos `sudo`).

A partir daqui, **quem usa WSL segue sempre as instruções de "Linux"** deste manual,
digitando os comandos na janela do **Ubuntu**.

> ⚠️ **Regra de ouro do WSL:** crie o seu projeto **dentro do Linux** (por exemplo
> `~/projetos/meu-app`), e **não** em `C:\...` (que no WSL aparece como `/mnt/c/...`).
> Dentro de `/mnt/c` tudo fica muito lento e o Git se confunde com permissões.

---

## 4. Instalar os pré-requisitos

> O instalador do Waves tenta instalar sozinho o que faltar (uv, Python, Git, tmux e, no
> Windows nativo, psmux e pwsh). Mesmo assim, instale tudo aqui antes: o BMAD precisa de
> Node.js e uv **antes** do Waves, e assim você vê cada peça funcionando.

### 4.1 Linux (Ubuntu/Debian) — e também **Windows com WSL**

```bash
# 1) Ferramentas básicas: Git, tmux, curl e unzip
sudo apt update
sudo apt install -y git tmux curl unzip

# 2) uv (gerenciador de Python)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3) Node.js (pelo nvm — a versão do apt costuma ser antiga demais)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```

**Feche o terminal e abra de novo** (para ele "enxergar" o uv e o nvm). Depois:

```bash
# 4) Instala a versão LTS do Node.js
nvm install --lts

# 5) Claude Code
curl -fsSL https://claude.ai/install.sh | bash
```

Outras distribuições: Fedora → `sudo dnf install -y git tmux curl unzip`; Arch →
`sudo pacman -S git tmux curl unzip`. O resto é igual.

### 4.2 macOS

```bash
# 1) Homebrew (o "loja de programas" do terminal). Pule se já tiver: teste com `brew --version`
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Ao final, o Homebrew mostra dois comandos em "Next steps" (começam com `echo` e `eval`).
**Copie e rode esses dois comandos** — eles colocam o `brew` no seu terminal. Depois:

```bash
# 2) Git, tmux, Node.js e uv
brew install git tmux node uv

# 3) Claude Code
curl -fsSL https://claude.ai/install.sh | bash
```

Feche e abra o Terminal de novo.

### 4.3 Windows nativo (PowerShell) — só se você NÃO for usar WSL

Abra o **PowerShell** (normal, não precisa ser administrador) e rode:

```powershell
# 1) Git, Node.js LTS, uv e PowerShell 7 (pwsh)
winget install --id Git.Git -e
winget install --id OpenJS.NodeJS.LTS -e
winget install --id astral-sh.uv -e
winget install --id Microsoft.PowerShell -e

# 2) Claude Code
irm https://claude.ai/install.ps1 | iex
```

**Feche o PowerShell e abra de novo.** O `psmux` (o "tmux do Windows") é instalado
automaticamente pelo instalador do Waves no passo 7.

### 4.4 Conferir as versões (todos os sistemas)

Cole um por vez. Cada um deve mostrar um número de versão, **não** um erro:

```bash
git --version      # precisa ser 2.34 ou maior
node --version     # precisa ser v20.12 ou maior
uv --version
claude --version
tmux -V            # Linux, macOS e WSL (no Windows nativo, pule este)
```

Se algum disser "command not found" / "não é reconhecido", feche e abra o terminal e tente
de novo. Persistindo, veja [Problemas comuns](#12-problemas-comuns-e-soluções).

### 4.5 Entrar na sua conta do Claude (uma vez só)

```bash
claude
```

Na primeira vez ele pede para fazer login (abre o navegador). Faça o login, volte ao
terminal e digite `/exit` para sair.

### 4.6 Dizer ao Git quem você é (uma vez só)

Troque pelo seu nome e e-mail:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "voce@exemplo.com"
git config --global init.defaultBranch main
```

---

## 5. Criar a pasta do projeto

Se você **já tem** um projeto com Git, só entre na pasta dele (`cd caminho/do/projeto`) e
pule para o passo 6.

### Linux, macOS e Windows com WSL

```bash
mkdir -p ~/projetos/meu-app
cd ~/projetos/meu-app
git init
```

### Windows nativo (PowerShell)

```powershell
mkdir C:\projetos\meu-app
cd C:\projetos\meu-app
git init
```

> Troque `meu-app` pelo nome do seu projeto (sem espaços e sem acentos é mais seguro).
> **Todos os próximos comandos são rodados de dentro desta pasta.**

---

## 6. Instalar o BMAD Method 6.12.4

O comando é **o mesmo em todos os sistemas**. Ele fixa a versão **6.12.4**, a mínima que o
Waves 3.6.12.4 aceita:

```bash
npx bmad-method@6.12.4 install
```

Se aparecer `Need to install the following packages ... Ok to proceed? (y)`, digite `y` e
Enter.

### 6.1 As perguntas do instalador, tela por tela

Use as **setas ↑/↓** para mover, **Espaço** para marcar/desmarcar e **Enter** para confirmar.

| #   | O instalador pergunta                                                              | O que responder                                                                                                                                                                                                                                                                                                     |
| --- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `Installation directory:` (mostra o caminho da pasta atual)                        | **Enter** (aceita a pasta onde você está).                                                                                                                                                                                                                                                                          |
| 2   | `Install to this directory?  ● Yes / ○ No`                                         | **Enter** (Yes).                                                                                                                                                                                                                                                                                                    |
| 3   | `Select official modules to install:` — lista com ◼/◻                              | **BMad Method (v6.12.4)** já vem marcado ◼. **Deixe só ele** e aperte **Enter**. Opcional: marque também **BMad Test Architect** (TEA) com Espaço, se quiser os testes de aceitação automáticos — o instalador avisa `tea is pinned to v1.27.2`, e isso é normal. **NÃO marque "BMad Loop"** (veja o aviso abaixo). |
| 4   | `Do you want to install custom or community modules?  ○ Yes / ● No`                | **Enter** (No). O Waves é instalado depois, pelo instalador próprio dele.                                                                                                                                                                                                                                           |
| 5   | `Integrate with:` — lista de ferramentas                                           | Com a seta em **Claude Code ⭐**, aperte **Espaço** (fica ◼) e depois **Enter**.                                                                                                                                                                                                                                    |
| 6   | `What should agents call you?`                                                     | Seu nome, Enter.                                                                                                                                                                                                                                                                                                    |
| 7   | `What is your project called?`                                                     | Enter (usa o nome da pasta) ou digite outro.                                                                                                                                                                                                                                                                        |
| 8   | `What language should agents use when chatting with you?`                          | Digite `Portuguese (Brazil)` e Enter.                                                                                                                                                                                                                                                                               |
| 9   | `Preferred document output language?`                                              | Digite `Portuguese (Brazil)` e Enter (ou `English`, se os documentos devem sair em inglês).                                                                                                                                                                                                                         |
| 10  | `Where should output files be saved?`                                              | **Enter** (`_bmad-output`).                                                                                                                                                                                                                                                                                         |
| 11  | `Module configuration  ● Express Setup / ○ Customize`                              | **Enter** (Express Setup).                                                                                                                                                                                                                                                                                          |
| 12  | `Install N deprecated compatibility shim skill(s)?  ○ Yes / ● No` (o número varia) | **Enter** (No).                                                                                                                                                                                                                                                                                                     |

No final aparece um quadro **"BMAD is ready to use!"** com `BMad Method (v6.12.4, installed)`
e `claude-code (29 skills → .claude/skills)`. Pronto.

> ⚠️ **O aviso `🚀 BMad v7 is close` (no começo e no fim da instalação) não é para você agora.**
> Ele convida a testar o BMAD v7 com `npx skills add ...` e `bmad migrate`. **Não rode esses
> comandos:** o Waves 3.6.12.4 funciona com o BMAD **6.12.4** (a linha v6) e ainda não com o v7.

> ⚠️ **Por que NÃO marcar "BMad Loop"?** O BMad Loop é o `bmad-loop` original — o mesmo
> motor que o Waves já traz dentro dele (no Waves ele se chama `waves run --deterministic`).
> Instalar os dois no mesmo projeto não quebra nada (cada um guarda seus arquivos em pastas
> próprias), mas cria dois pilotos automáticos disputando a mesma lista de stories. Se você
> um dia rodar os dois **ao mesmo tempo** no mesmo projeto, eles vão brigar. O Manual de Uso
> explica a diferença entre eles.

### 6.2 Alternativa: instalar o BMAD sem perguntas (um comando só)

Se preferir não responder às telas, este comando faz as mesmas escolhas da tabela acima.

**Linux, macOS e WSL:**

```bash
npx -y bmad-method@6.12.4 install --yes --directory . \
  --modules bmm --tools claude-code \
  --user-name "Seu Nome" \
  --communication-language "Portuguese (Brazil)" \
  --document-output-language "Portuguese (Brazil)"
```

**Windows nativo (PowerShell)** — no PowerShell a quebra de linha é com crase (`` ` ``):

```powershell
npx -y bmad-method@6.12.4 install --yes --directory . `
  --modules bmm --tools claude-code `
  --user-name "Seu Nome" `
  --communication-language "Portuguese (Brazil)" `
  --document-output-language "Portuguese (Brazil)"
```

Para incluir o Test Architect (opcional), troque `--modules bmm` por `--modules bmm,tea`. O BMAD
6.12.4 instala o TEA na versão **v1.27.2**, a última que funciona com o instalador da linha v6 —
não tente instalar um TEA mais novo.

### 6.3 Salvar (commit) a instalação do BMAD

```bash
git add -A
git commit -m "instala BMAD Method 6.12.4"
```

> No Windows você pode ver avisos `LF will be replaced by CRLF` — são normais, ignore.

---

## 7. Instalar o Riaworks Waves 3.6.12.4

### 7.1 Qual ZIP baixar

| Seu sistema                 | Arquivo                               |
| --------------------------- | ------------------------------------- |
| Windows (WSL **ou** nativo) | `riaworks-waves-3.6.12.4-windows.zip` |
| macOS                       | `riaworks-waves-3.6.12.4-macos.zip`   |
| Linux                       | `riaworks-waves-3.6.12.4-linux.zip`   |

Dentro de cada ZIP há uma pasta com:

```text
riaworks-waves-3.6.12.4-<sistema>/
├── install.sh        instalador para Linux, macOS e WSL
├── install.ps1       instalador para Windows nativo (só no ZIP de Windows)
├── INSTALL.md        guia técnico do instalador (em inglês)
├── SHA256SUMS        "impressões digitais" para conferir que o download não veio corrompido
├── manuais/          ESTES manuais
├── wheels/           o programa Waves (arquivo .whl)
└── riaworks-waves-3.6.12.4/   o módulo (skills) no formato que o instalador do BMAD entende,
                            o README.md com as telas e a documentação completa em docs/ (em inglês)
```

### 7.2 Descompactar

A regra é: **descompacte o ZIP numa pasta FORA do seu projeto** (por exemplo, na pasta de
Downloads ou na sua pasta pessoal). O instalador **se recusa** a rodar se você tentar
instalar dentro da própria pasta do ZIP — isso é proposital.

**Linux:**

```bash
cd ~
unzip ~/Downloads/riaworks-waves-3.6.12.4-linux.zip
```

**macOS:**

```bash
cd ~
unzip ~/Downloads/riaworks-waves-3.6.12.4-macos.zip
```

(Ou dê dois cliques no ZIP no Finder e mova a pasta criada para a sua pasta pessoal.)

**Windows com WSL** — o ZIP baixado pelo navegador fica no Windows; copie para o Linux.
Troque `SEU_USUARIO_WINDOWS` pelo nome da sua pasta em `C:\Users\`:

```bash
cd ~
cp /mnt/c/Users/SEU_USUARIO_WINDOWS/Downloads/riaworks-waves-3.6.12.4-windows.zip ~/
unzip riaworks-waves-3.6.12.4-windows.zip
```

**Windows nativo (PowerShell):**

```powershell
cd $HOME\Downloads
Expand-Archive .\riaworks-waves-3.6.12.4-windows.zip -DestinationPath $HOME
```

(Ou botão direito no ZIP → _Extrair Tudo..._ → escolha `C:\Users\<você>`.)

### 7.3 (Opcional) Conferir que o download está íntegro

Entre na pasta descompactada e rode:

```bash
# Linux e WSL
cd ~/riaworks-waves-3.6.12.4-linux     # ou ~/riaworks-waves-3.6.12.4-windows no WSL
sha256sum -c SHA256SUMS
```

```bash
# macOS
cd ~/riaworks-waves-3.6.12.4-macos
shasum -a 256 -c SHA256SUMS
```

```powershell
# Windows nativo — compare o número mostrado com a linha do .whl dentro de SHA256SUMS
cd $HOME\riaworks-waves-3.6.12.4-windows
Get-FileHash .\wheels\*.whl -Algorithm SHA256
Get-Content .\SHA256SUMS
```

Cada linha deve terminar em `OK` (Linux/macOS/WSL).

### 7.4 Rodar o instalador

**Primeiro entre na pasta do SEU PROJETO** e rode o instalador de lá, apontando para o
arquivo dentro da pasta descompactada.

**Linux:**

```bash
cd ~/projetos/meu-app
sh ~/riaworks-waves-3.6.12.4-linux/install.sh
```

**macOS:**

```bash
cd ~/projetos/meu-app
sh ~/riaworks-waves-3.6.12.4-macos/install.sh
```

**Windows com WSL** (na janela do Ubuntu):

```bash
cd ~/projetos/meu-app
sh ~/riaworks-waves-3.6.12.4-windows/install.sh
```

**Windows nativo (PowerShell)** — experimental:

```powershell
cd C:\projetos\meu-app
powershell -ExecutionPolicy Bypass -File $HOME\riaworks-waves-3.6.12.4-windows\install.ps1 -Project C:\projetos\meu-app
```

### 7.5 O que o instalador faz e pergunta

1. **Pergunta qual é o projeto.** Mostra a pasta atual e diz se encontrou um `_bmad/` lá.
   Se estiver certo, aperte **Enter**. (Se você passou `--project` / `-Project`, ele não
   pergunta.)
2. **Instala o que faltar** (uv, Python 3.11+, Git, tmux; no Windows nativo, psmux e pwsh).
   Se algo precisar de senha de administrador e não conseguir, ele **mostra o comando exato**
   para você rodar e continua.
3. **Nível máquina:** instala o comando `waves` (e o painel `waves tui`). Isso vale para
   todos os projetos deste computador.
4. **Nível projeto:** roda `waves init`. **A primeira coisa que ele faz é conferir a versão do
   BMAD do projeto.** Se for mais antiga que a 6.12.4, ele mostra
   `FAIL: BMAD-METHOD ... is below the 6.12.4 floor`, diz `nothing was installed` e o instalador para — veja
   [Problemas comuns](#12-problemas-comuns-e-soluções). Com o BMAD certo, ele coloca no seu
   projeto:
   - as 11 skills `waves-*` em `.claude/skills/`;
   - o agente do Waves em `.claude/agents/` (`waves-agent`), usado pelo paralelismo por ondas;
   - os "ganchos" (hooks) do Claude Code em `.claude/settings.json` (é por eles que o Waves
     sabe quando uma sessão do Claude terminou);
   - o arquivo de configuração `.waves/loop/policy.toml`;
   - linhas novas no `.gitignore`.
5. **Preflight:** roda `waves validate` e lista o que está `ok` e o que falta.

No final você verá algo como (saída real de uma instalação de teste, encurtada):

```text
  installed: waves 3.6.12.4
==> wiring up the project: ~/projetos/meu-app
  ok: BMAD-METHOD 6.12.4 (floor 6.12.4)
  hooks registered (claude): ~/projetos/meu-app/.claude/settings.json
  skills -> .claude/skills/: installed waves-resolve, waves-core-sweep, waves-setup,
            waves-core-orchestrator, waves-master-tui, waves-deferred,
            waves-master-parallelism, waves-core-parallelism, waves-provisioning,
            waves-tests, waves-config
  policy written: ~/projetos/meu-app/.waves/loop/policy.toml
  agents -> .claude/agents/: rendered waves-agent
init complete. One-time setup before `waves run` — ...
  claude: run `claude` once in the project to accept workspace trust and hooks approval
==> preflight
FAIL: sprint status file not found: ~/projetos/meu-app/_bmad-output/implementation-artifacts/sprint-status.yaml
FAIL: git worktree is not clean — commit or stash before running
  ok: BMAD-METHOD 6.12.4 (floor 6.12.4)
  ok: upstream skills present (bmad-build-auto + review layers)
  ok: bundled skills up to date: 11 in .claude/skills
  ...
Installed, but the preflight above found problems to fix before the first run.
Next:  /waves-master-tui in your coding CLI launches a run; /waves-master-parallelism plans an epic.
```

> ✅ **Os dois `FAIL` acima são esperados num projeto novo** e não são erro de instalação:
>
> - `sprint status file not found` → você ainda não planejou o projeto com o BMAD
>   (é o [passo 10](#10-próximo-passo-planejar-o-projeto-com-o-bmad)).
> - `git worktree is not clean` → a instalação criou arquivos novos que ainda não foram
>   salvos no Git. Resolva com o commit abaixo.

### 7.6 Opções úteis do instalador

| Linux / macOS / WSL (`install.sh`) | Windows nativo (`install.ps1`) | Para que serve                                                            |
| ---------------------------------- | ------------------------------ | ------------------------------------------------------------------------- |
| `--project <pasta>`                | `-Project <pasta>`             | Instalar num projeto que não é a pasta atual.                             |
| `--cli codex` (pode repetir)       | `-Cli claude,codex`            | Registrar também outra IA (codex, gemini, copilot…). Padrão: só `claude`. |
| `--tool-only`                      | `-ToolOnly`                    | Só instala o comando `waves` na máquina (sem mexer em projeto).           |
| `--project-only`                   | `-ProjectOnly`                 | Só prepara mais um projeto, numa máquina que já tem o `waves`.            |
| `--via-bmad`                       | `-ViaBmad`                     | Também registra o módulo no BMAD, para ele aparecer no `/bmad-help`.      |
| `--force`                          | `-Force`                       | Regrava as skills do projeto (use ao atualizar se você editou alguma).    |
| `--no-tui`                         | `-NoTui`                       | Não instala o painel `waves tui`.                                         |
| `--no-bootstrap`                   | `-NoBootstrap`                 | Não instala pré-requisitos sozinho; só avisa o que falta.                 |
| `--help`                           | `Get-Help .\install.ps1`       | Mostra todas as opções.                                                   |

### 7.7 Salvar (commit) a instalação do Waves

```bash
git add -A
git commit -m "instala Riaworks Waves 3.6.12.4"
```

> Se o `waves validate` avisar `_bmad/render/ is tracked by git`, rode uma vez:
>
> ```bash
> git rm -r --cached _bmad/render
> git commit -m "para de versionar _bmad/render"
> ```

---

## 8. Primeira abertura do Claude Code no projeto

O Waves abre sessões do Claude **sozinho**, e essas sessões automáticas **não conseguem
responder** às perguntas de primeira vez do Claude ("você confia nesta pasta?", "aprovar
hooks?"). Por isso você precisa abrir o Claude **uma vez**, à mão, dentro do projeto:

```bash
cd ~/projetos/meu-app      # Windows nativo: cd C:\projetos\meu-app
claude
```

1. Ele pergunta se você confia na pasta → escolha **Yes, proceed** (Sim).
2. Se perguntar sobre **hooks**, aprove.
3. Digite `/exit` para sair.

> Se você pular este passo, o primeiro run do Waves vai parecer "travado" e terminar por
> tempo esgotado depois de muitos minutos.

---

## 9. Conferir se ficou tudo certo

```bash
waves --version        # deve mostrar 3.6.12.4
waves validate         # checklist completo
waves mux              # mostra o multiplexador escolhido
```

- `waves --version` → `3.6.12.4`.
- `waves mux` → no Linux/macOS/WSL deve dizer **`platform default for linux`** (ou
  `darwin` no macOS). **No WSL, se aparecer `win32`, você está usando o Waves do Windows
  por engano** — veja [Problemas comuns](#12-problemas-comuns-e-soluções).
- `waves validate` → tudo `ok` — inclusive `BMAD-METHOD 6.12.4 (floor 6.12.4)` —, **exceto**
  o `sprint status file not found`, que só some depois do passo 10.

Avisos que você **pode ignorar**:

- `the BMAD Method's Test Architect (TEA) module is not installed` — só importa se você quiser
  o TEA (opcional).

---

## 10. Próximo passo: planejar o projeto com o BMAD

O Waves **constrói** stories; quem **cria** as stories é o BMAD. Até existir o arquivo
`sprint-status.yaml`, não há o que construir. Abra o Claude no projeto (`claude`) e use as
skills do BMAD, nesta ordem (cada uma conversa com você):

| Ordem | Digite no Claude                 | O que produz                                                                                                                                                                                          |
| ----- | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0     | `/bmad-help`                     | Pergunte "o que eu faço agora?" a qualquer momento — ele guia o caminho.                                                                                                                              |
| 1     | `/bmad-product-brief` (opcional) | Um resumo do produto.                                                                                                                                                                                 |
| 2     | `/bmad-prd`                      | O PRD: o que o sistema deve fazer.                                                                                                                                                                    |
| 3     | `/bmad-ux` (se tiver telas)      | O desenho da experiência do usuário.                                                                                                                                                                  |
| 4     | `/bmad-architecture`             | As decisões técnicas (linguagem, banco, estrutura).                                                                                                                                                   |
| 5     | `/bmad-create-epics-and-stories` | Os épicos e as stories. No BMAD 6.12.4, se alguma checagem falhar ele salva o `epics.md` como **rascunho** (`status: draft`) e lista o que falta: aceite a correção que ele oferece antes do passo 6. |
| 6     | `/bmad-sprint-planning`          | **O `sprint-status.yaml`** — a lista que o Waves vai seguir.                                                                                                                                          |
| 7     | `/bmad-project-context`          | Recomendado: grava o contexto do projeto no `AGENTS.md`, que as sessões leem.                                                                                                                         |

Depois de cada etapa, salve no Git:

```bash
git add -A
git commit -m "planejamento BMAD"
```

Rode `waves validate` de novo: agora o `sprint status` deve aparecer como `ok`. A partir
daqui, siga o **Manual de Uso** (`02-MANUAL-USO-WAVES.md`).

---

## 11. Atualizar o Waves no futuro

Uma versão nova do Waves vem num ZIP novo. Não existe `uv tool upgrade` para esse tipo de
instalação: basta **rodar o instalador do ZIP novo**, do mesmo jeito do passo 7.4. Ele:

- troca o programa `waves` pela versão nova;
- percebe que o projeto já tinha as skills e as **atualiza** sozinho;
- **não mexe** no seu `.waves/loop/policy.toml` nem nos seus runs.

Tem mais de um projeto na mesma máquina? Rode o instalador completo em um deles e, nos
outros, só a parte do projeto:

```bash
sh ~/riaworks-waves-<nova-versão>-linux/install.sh --project-only --project ~/projetos/outro-app
```

> ⚠️ **Nunca atualize com um run em andamento.** Termine ou pare o run antes (`waves stop <id>`).

### 11.1 Vindo do Waves 3.0.0 ou 3.1.0: atualize o BMAD PRIMEIRO

O Waves 3.6.12.4 exige o BMAD 6.12.4. Um projeto instalado com o manual anterior está no
BMAD 6.12.0 — e, se você rodar o instalador novo nele, o Waves **para sem instalar nada**:

```text
FAIL: BMAD-METHOD 6.12.0 is below the 6.12.4 floor waves supports — upgrade the project with `npx bmad-method@latest install` (quick update), then re-run `waves validate`
  nothing was installed — upgrade first, then re-run `waves init`
```

Nada se perde: é só seguir esta ordem, **de dentro da pasta do projeto**.

1. Atualize o BMAD do projeto para a 6.12.4 (o mesmo comando em todos os sistemas):

   ```bash
   npx -y bmad-method@6.12.4 install --directory . --action quick-update --yes
   ```

2. Salve no Git:

   ```bash
   git add -A
   git commit -m "atualiza BMAD Method para 6.12.4"
   ```

3. Rode o instalador do ZIP novo, como no passo 7.4.

4. Salve de novo (`git add -A` e `git commit -m "atualiza Riaworks Waves para 3.6.12.4"`).

> Se o instalador mostrar `commit the move`, é porque você tinha personalizações das skills do
> Waves em `_bmad/custom/`. Desde a 3.1.0 elas ficam em `_waves/custom/`, e o instalador as
> **move** sozinho — o commit do passo 4 registra a mudança.

### 11.2 Atualizar só o BMAD

Rode de dentro do projeto `npx bmad-method@<versão> install` e escolha a ação de
atualização quando ele perguntar (ou use `--action quick-update --yes`, como acima). Fique na
linha **6.12.x**: o BMAD v7 ainda não é suportado pelo Waves 3.6.12.4.

---

## 12. Problemas comuns e soluções

| Sintoma                                                                        | Causa provável                                                                              | Solução                                                                                                                                                                                                                             |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `waves: command not found` / `waves não é reconhecido`                         | O terminal ainda não conhece a pasta onde o `uv` instala programas.                         | Feche e abra o terminal. Se continuar: `uv tool update-shell` e abra de novo.                                                                                                                                                       |
| `warning: a different waves is ahead on your PATH`                             | Existe uma instalação antiga do `waves` que aparece antes.                                  | Veja qual é com `which -a waves` (Linux/macOS/WSL) ou `Get-Command waves -All` (Windows). Remova a antiga com `uv tool uninstall riaworks-waves` e rode o instalador de novo.                                                       |
| `git worktree is not clean — commit or stash before running`                   | Há arquivos modificados sem commit.                                                         | `git add -A` e `git commit -m "..."`. O Waves só roda com a árvore limpa, para nunca misturar o trabalho dele com o seu.                                                                                                            |
| `sprint status file not found`                                                 | O planejamento do BMAD ainda não foi feito.                                                 | Faça o [passo 10](#10-próximo-passo-planejar-o-projeto-com-o-bmad).                                                                                                                                                                 |
| `FAIL: BMAD-METHOD 6.12.0 is below the 6.12.4 floor` e `nothing was installed` | O projeto tem um BMAD mais antigo que o 6.12.4. O Waves não instala nada nele.              | `npx -y bmad-method@6.12.4 install --directory . --action quick-update --yes` dentro do projeto, `git commit`, e rode o instalador do Waves de novo (veja a [seção 11.1](#111-vindo-do-waves-300-ou-310-atualize-o-bmad-primeiro)). |
| `node: command not found` ou versão abaixo de 20.12                            | Node.js ausente ou antigo.                                                                  | Refaça o passo 4 do seu sistema. No Linux/WSL, `nvm install --lts`.                                                                                                                                                                 |
| `tmux: command not found`                                                      | tmux ausente.                                                                               | Linux/WSL: `sudo apt install -y tmux`. macOS: `brew install tmux`.                                                                                                                                                                  |
| No WSL, `waves mux` mostra `win32`                                             | O WSL está usando o `waves` instalado no **Windows**.                                       | Instale o Waves **dentro do Ubuntu** com o `install.sh` (passo 7.4, WSL). O WSL "empresta" o PATH do Windows e isso engana.                                                                                                         |
| PowerShell: `execution of scripts is disabled on this system`                  | Política de segurança do PowerShell.                                                        | Use exatamente `powershell -ExecutionPolicy Bypass -File ...\install.ps1 ...` como no passo 7.4.                                                                                                                                    |
| O instalador diz que se recusa a instalar na própria pasta / na pasta pessoal  | Proteção de segurança.                                                                      | Rode o instalador **de dentro da pasta do projeto**, ou passe `--project <pasta-do-projeto>`.                                                                                                                                       |
| O primeiro run "trava" e termina por tempo esgotado                            | O Claude nunca foi aberto no projeto (diálogo de confiança pendente).                       | Faça o [passo 8](#8-primeira-abertura-do-claude-code-no-projeto).                                                                                                                                                                   |
| Aviso sobre o TEA (Test Architect) não instalado                               | O módulo opcional não foi instalado.                                                        | Ignore, ou instale: `npx bmad-method@6.12.4 install` e marque **BMad Test Architect**.                                                                                                                                              |
| O instalador do BMAD mostra `🚀 BMad v7 is close`                              | É só um convite para testar o BMAD v7.                                                      | **Ignore.** Não rode `npx skills add` nem `bmad migrate`: o Waves 3.6.12.4 é para o BMAD 6.12.4 (linha v6).                                                                                                                         |
| O instalador do BMAD diz `tea is pinned to v1.27.2`                            | O BMAD 6.12.4 fixa o Test Architect na última versão que o instalador v6 consegue instalar. | Normal, nada a fazer. Não tente instalar um TEA mais novo: ele exige o BMAD v7.                                                                                                                                                     |
| Computador sem internet                                                        | O Waves baixa algumas dependências do PyPI na primeira instalação.                          | Veja a seção _Offline installs_ do `INSTALL.md` dentro do ZIP.                                                                                                                                                                      |

Para relatar um problema, rode `waves diagnose` e envie o arquivo gerado (ele remove
código, caminhos e dados pessoais antes de salvar).

---

## 13. Desinstalar

Resumo (o guia completo, em inglês, está dentro do ZIP em `riaworks-waves-3.6.12.4/docs/setup-guide.md`, seção _Uninstalling_):

```bash
# dentro do projeto
waves clean --hard           # apaga runs terminados e suas worktrees
waves cleanup                # fecha sessões tmux que sobraram
rm -rf .waves/loop/          # estado do Waves no projeto
# remova as pastas .claude/skills/waves-* (e .agents/skills/waves-*, se usou --cli codex),
# os arquivos .claude/agents/waves-agent*.md e, em .claude/settings.json, as entradas
# de hook cujo comando contém "waves relay" (em instalações antigas, "waves_hook.py").
# A pasta _waves/ guarda a configuração de testes e as personalizações da equipe:
# apague só se não for mais usar o Waves neste projeto.

# na máquina (vale para todos os projetos)
uv tool uninstall riaworks-waves
```

O BMAD **não** é afetado por nada disso.

---

## 14. Resumo de uma página

**Linux / macOS / Windows com WSL** (no WSL, tudo dentro da janela do Ubuntu):

```bash
# pré-requisitos (Linux/WSL; no macOS: brew install git tmux node uv)
sudo apt update && sudo apt install -y git tmux curl unzip
curl -LsSf https://astral.sh/uv/install.sh | sh
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
# feche e abra o terminal
nvm install --lts
curl -fsSL https://claude.ai/install.sh | bash
claude            # faça login, depois /exit

# projeto
mkdir -p ~/projetos/meu-app && cd ~/projetos/meu-app && git init

# BMAD 6.12.4 (responda: Enter, Enter, só "BMad Method", No, Claude Code, nome, idioma...)
# o aviso "BMad v7 is close" no fim pode ser ignorado
npx bmad-method@6.12.4 install
git add -A && git commit -m "instala BMAD Method 6.12.4"

# Waves 3.6.12.4 (troque "linux" por "macos" ou "windows" conforme o ZIP)
cd ~ && unzip ~/Downloads/riaworks-waves-3.6.12.4-linux.zip
cd ~/projetos/meu-app && sh ~/riaworks-waves-3.6.12.4-linux/install.sh
git add -A && git commit -m "instala Riaworks Waves 3.6.12.4"

# confiança do Claude no projeto (Yes + aprovar hooks, depois /exit)
claude

# conferir
waves --version && waves validate
```

**Windows nativo (PowerShell, experimental):**

```powershell
winget install --id Git.Git -e
winget install --id OpenJS.NodeJS.LTS -e
winget install --id astral-sh.uv -e
winget install --id Microsoft.PowerShell -e
irm https://claude.ai/install.ps1 | iex
# feche e abra o PowerShell
claude            # login, depois /exit

mkdir C:\projetos\meu-app; cd C:\projetos\meu-app; git init
npx bmad-method@6.12.4 install
git add -A; git commit -m "instala BMAD Method 6.12.4"

Expand-Archive $HOME\Downloads\riaworks-waves-3.6.12.4-windows.zip -DestinationPath $HOME
powershell -ExecutionPolicy Bypass -File $HOME\riaworks-waves-3.6.12.4-windows\install.ps1 -Project C:\projetos\meu-app
git add -A; git commit -m "instala Riaworks Waves 3.6.12.4"

claude            # Yes + aprovar hooks, depois /exit
waves --version; waves validate
```

Próximo: planejar com o BMAD ([passo 10](#10-próximo-passo-planejar-o-projeto-com-o-bmad)) e
depois o **Manual de Uso**.
