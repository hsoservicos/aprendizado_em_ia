# Migração OpenCode v1 → v2 — Guia de Continuidade

**Versão**: 1.0.0
**Data**: 2026-11-09
**Autor**: Hsantos
**Público-alvo**: colaboradores do projeto que usam **OpenCode v1** (ainda) e **OpenCode v2** (já migrados), simultaneamente.

---

## 1. Resumo executivo

Este repositório roda o mesmo conjunto de **55 skills** (`bmad-*`, `impeccable` e
as 4 skills de tecnologia) e a mesma toolchain em **dois agentes** (OpenCode e
Claude Code). Com a migração do OpenCode de **v1 → v2**, o *agente* mudou, mas o
**conteúdo das skills e a configuração do projeto permanecem compatíveis**.

A regra de ouro da migração (documentação oficial):

> **OpenCode 1 e OpenCode 2 usam o mesmo comando `opencode`.** As únicas quebras
> intencionais são a **API de plugins**, a **API do servidor/clients** e a
> **configuração do terminal (`tui.json` → `cli.json`)**. Todo o resto — arquivos
> `.opencode/`, skills, comandos, agentes, configuração — **continua funcionando
> sem alterações**.

Ou seja: **não é preciso converter nada para usar a v2**. Os terminais ainda em
v1 continuam funcionando como antes; os que já migraram para v2 usam as mesmas
skills de forma nativa.

---

## 2. Estado atual do projeto (2026-11-09)

| Item | Valor |
|------|-------|
| **OpenCode nesta máquina (Hsantos)** | **v2.2.6** (linha v2) |
| **Terminais ainda em v1** | compatíveis — sem ação obrigatória |
| **Skills** | 55 (50 BMAD + 4 tecnologia + 1 impeccable), idênticas nas duas árvores |
| **Toolchain** | Node v24.22.2 · npm 12.2.2 · Python 3.14.4 · uv 0.13.7 · Git 2.53.0 · gh 2.103.3 · ripgrep 15.2.0 · RTK 1.1.0 · CrewAI 1.15.39 |
| **Frameworks** | BMAD 6.12.4 · Impeccable 4.8.1 · Superpowers 7.0.x · REA 6.8.0 |

---

## 3. O que muda de verdade (breaking changes)

Apenas **três** mudanças intencionais da v2 (fonte:
<https://opencode.ai/v2/docs/migrate-v1>):

1. **Plugins** — nova API de plugin. **Implementações de plugin da v1 NÃO rodam
   na v2.** (Não é só mover arquivo ou renomear a entrada de config.)
2. **Server API e clients** — novos contratos; integrações que chamam a API v1
   precisam migrar para a v2 (pacote `@opencode/client`).
3. **Config do terminal** — `tui.json(c)` em camadas vira **um único**
   `~/.config/opencode/cli.json` (auto-migrado na primeira execução).

**Nenhum destes três afeta o uso diário das skills BMAD deste projeto**, porque
o projeto não usa plugins próprios da v1 nem chama a server API v1. O
Superpowers (plugin) foi instalado via mecanismo nativo e já está na v7, em
ambos os agentes.

---

## 4. O que continua compatível

Confirmado pela documentação oficial de migração:

- **Configuração JSON/JSONC** (`opencode.json(c)`) — os campos suportados da v1
  continuam lidos (normalizados em memória, sem reescrever o arquivo).
- **Skills** — arquivos `SKILL.md` e a descoberta automática **não mudam**.
- **Comandos** — `.opencode/commands/*.md` (Markdown) continua suportado; a v2
  descobre tanto `command/` quanto `commands/`.
- **Arquivos de agente** — `agent/`, `agents/`, `mode/`, `modes/` são todos
  descobertos pela v2.
- **`AGENTS.md`** — continua no lugar; a v2 descobre o `~/.config/opencode/AGENTS.md`
  global e os `AGENTS.md` ambientais.

> ⚠️ **Nota sobre `CLAUDE.md`**: a v2 só descobre `AGENTS.md` (não faz fallback
> para `CLAUDE.md`). Neste projeto o `CLAUDE.md` é o ponto de entrada do
> **Claude Code** (que importa `AGENTS.md`); para o OpenCode v2 o `AGENTS.md` é o
> arquivo descoberto — nenhuma mudança é necessária.

---

## 5. Descoberta de skills: v1 vs v2

### Fontes de descoberta na v2 (documentação oficial)

| Escopo | Fonte nativa | Fonte de compatibilidade |
|--------|-------------|--------------------------|
| Global | `~/.config/opencode/skills` | `~/.claude/skills`, `~/.agents/skills` |
| Projeto | `.opencode/skills` | `.claude/skills`, `.agents/skills` |

### Onde ficam as skills deste projeto

| Skill(s) | Local | Descoberta na v2 |
|----------|-------|------------------|
| 55 skills BMAD (paridade) | `.agents/skills/` **e** `.claude/skills/` (idênticas) | ✅ fonte de compatibilidade (projeto) |
| Impeccable (OpenCode nativo) | `.opencode/skills/impeccable/` | ✅ fonte nativa (projeto) |
| reverse-engineer-anything (REA) | `~/.agents/skills/` e `~/.claude/skills/` | ✅ compatibilidade (global) |
| asd-ste100 | `~/.agents/skills/` e `~/.claude/skills/` | ✅ compatibilidade (global) |
| mercado-livre-pagamentos | `~/.config/opencode/skills/` | ✅ nativa (global) |

### Precedência (menor → maior prioridade)

1. Skills built-in
2. `.claude/skills` (global → projeto)
3. `.agents/skills` (global → projeto)
4. `~/.config/opencode/skills`
5. `.opencode/skills` (projeto)
6. Entradas explícitas do campo `skills`

> Como `.agents/skills/` tem precedência sobre `.claude/skills/`, e ambas as
> árvores são mantidas **byte-idênticas** (ver §6), o conteúdo é o mesmo — não há
> ambiguidade de ID.

---

## 6. Layout de arquivos (v1 e v2)

```
/home/hsantos/app/
├── AGENTS.md                       # instruções do agente (OpenCode v2 descobre; Claude Code via CLAUDE.md)
├── CLAUDE.md                       # entrada do Claude Code (importa AGENTS.md)
├── .agents/skills/                 # 55 skills BMAD (árvore de paridade — OpenCode)
│   └── <skill>/SKILL.md
├── .claude/skills/                 # 55 skills BMAD (espelho byte-idêntico — Claude Code)
│   └── <skill>/SKILL.md
├── .opencode/
│   ├── opencode.json               # config do projeto (plugin Superpowers)
│   ├── commands/                   # 55 comandos slash v1 (wrappers @skills/<name>)
│   │   └── bmad-<skill>.md
│   └── skills/                     # skills nativas v2
│       └── impeccable/
└── _bmad/                          # framework BMAD (core + bmm)
```

### Diferença entre as duas versões

| Aspecto | OpenCode v1 | OpenCode v2 |
|---------|-------------|-------------|
| Invocação de skill | `/bmad-<skill>` (comando slash em `.opencode/commands/`) | skill nativa (`skill` tool / auto-descoberta) **e** `/bmad-<skill>` ainda funciona |
| Conteúdo da skill | `.agents/skills/<skill>/SKILL.md` | `.agents/skills/<skill>/SKILL.md` (mesmo arquivo) |
| Referência | corpo `@skills/<skill>` no comando | `@<skill-id>` no prompt (ex.: `@bmad-help`) |
| Config do terminal | `tui.json(c)` | `~/.config/opencode/cli.json` |
| Plugins | API v1 (`plugin`) | API v2 (`plugins`) — v1 não roda |

---

## 7. Uso no dia a dia

### Terminais em OpenCode v1 (continuidade)

Nada muda. Continuam usando os **comandos slash**:

```
/bmad-help            /bmad-build        /bmad-code-review
/bmad-brainstorming   /bmad-create-prd   /bmad-retrospective
/impeccable <cmd>     ...
```

As 55 entradas em `.opencode/commands/` são preservadas exatamente para isso.

### Terminais em OpenCode v2 (já migrados)

As **mesmas skills** são descobertas nativamente e podem ser invocadas de duas
formas:

1. **Auto-invocação**: o modelo seleciona a skill pelo `description` quando
   relevante (não precisa de comando slash).
2. **Manual**: menção `@<skill-id>` no prompt (ex.: `@bmad-build`) ou a tool
   `skill`.

Os comandos slash `/bmad-*` também continuam disponíveis (a v2 descobre
`.opencode/commands/`), então o fluxo mental é o mesmo.

### Fluxo comum às duas versões

O ciclo de vida BMAD (`Clarify → Plan → Build → Review → Learn`) e as regras de
precedência BMAD × Superpowers × Impeccable são **idênticos** nas duas versões —
não há diferença de workflow, só de mecanismo de invocação.

---

## 8. Migração de configuração (opcional)

A conversão para o formato nativo v2 é **opcional**. A v2 normaliza os campos v1
em memória sem reescrever o arquivo. As mudanças de nome relevantes, se/quando
for converter:

| v1 | v2 |
|----|----|
| `command` (mapa) | `commands` |
| `plugin` (array) | `plugins` (array de objetos) |
| `agent` (singular) / `mode` | `agents` |
| `skills.paths` / `skills.urls` | `skills` (array único) |
| `snapshot` | `snapshots` |
| `attachment` | `media` |
| `reference` | `references` |
| `permission` (por tool) | `permissions` (array ordenado) |
| `bash` / `task` / `write|patch` | `shell` / `subagent` / `edit` |

> **Recomendação deste projeto:** não converter ainda. Manter a config v1
> preserva a compatibilidade com os terminais v1. A conversão pode ser feita
> depois, quando todos os colaboradores estiverem na v2. Se for converter, use o
> próprio OpenCode: *"Migrate my OpenCode configuration from V1 to native V2,
> preserving behavior"*.

---

## 9. Checklist para colaboradores

### Quem ainda está na v1
- [ ] Nenhuma ação obrigatória. Continuar usando `/bmad-*`.
- [ ] Ao atualizar o repo (`git pull`), as skills de `.agents/skills/` e
      `.claude/skills/` já vêm atualizadas (BMAD 6.12.4, Impeccable 4.8.1).

### Quem já está na v2 (ou vai migrar)
- [ ] Instalar a v2: `curl -fsSL https://opencode.ai/install | bash` (substitui o binário v1).
- [ ] Verificar modelo/credenciais/agentes/MCP: `opencode` → `/mcps`, `/models`.
- [ ] Confirmar que as 55 skills aparecem (auto-descoberta de `.agents/skills/`).
- [ ] Toolchain da máquina: rodar o pré-flight do `getting-started.md` (Passo 0)
      e os updates de máquina listados em §10.

### Ambos
- [ ] Após `git pull`, rodar `npx bmad-method install` se as skills BMAD mudaram
      de versão no manifest (`_bmad/_config/manifest.yaml`).
- [ ] Manter `.agents/skills/` e `.claude/skills/` byte-idênticas:
      `diff <(ls .agents/skills) <(ls .claude/skills) && echo PARITY_OK`.

---

## 10. Atualizações aplicadas nesta máquina (2026-11-09)

### Repositório (commit — chega via `git pull` a todos)

- BMAD 6.12.1 → **6.12.4** (skills core+bmm regeradas).
- Impeccable 4.1.0 → **4.8.1** (engine v0.1.19) — skill + hooks + subagentes.
- `tools-registry.md` v1.7.0 (versões auditadas + log de instalação).
- `AGENTS.md` (referências de versão atualizadas + seção REA v6.8.0).

### Máquina (cada colaborador executa localmente)

| Ferramenta | Para | Comando |
|-----------|------|---------|
| Node.js | v24.22.2 | `nvm install 24 && nvm alias default 24` |
| npm | 12.2.2 | `npm install -g npm@latest` |
| uv | 0.13.7 | `uv self update` |
| CrewAI | 1.15.39 | `uv tool upgrade crewai` |
| gh | 2.103.3 | baixar release oficial do `cli/cli` |
| REA | 6.8.0 | `npx rea-agents@latest setup --client opencode --client claude_code --yes` |
| Superpowers (Claude) | 7.0.0 | `claude plugin update superpowers` |
| Superpowers (OpenCode) | 7.0.2 | já em git HEAD; `opencode plugin update` |

> As ferramentas de máquina (Node, npm, uv, CrewAI, gh, registros MCP, plugins)
> **não vivem no repositório** — cada colaborador precisa atualizá-las uma vez.
> O `getting-started.md` (Passo 0) cobre o pré-flight completo.

---

## Referências

- Migração oficial v1→v2: <https://opencode.ai/v2/docs/migrate-v1>
- Skills na v2: <https://opencode.ai/v2/docs/skills>
- Config na v2: <https://opencode.ai/v2/docs/config>
- Comandos na v2: <https://opencode.ai/v2/docs/commands>
- Registro de ferramentas: `_bmad-output/tools-registry.md`
- Onboarding do projeto: `_bmad-output/getting-started.md`
