# Registro da Sessão — 2026-10-12

**Data**: 2026-10-12
**Duração**: ~40 min
**Usuário**: Hsantos
**Agente**: OpenCode (mimo-v2.6-pro)
**Objetivo**: Instalar e ativar o REA (MCP de engenharia reversa), documentar
requisito de providers nativos, auditar a configuração dos agentes e publicar o
estado atual no GitHub.

---

## Resumo

Instalação do [REA](https://github.com/morluto/rea) (`rea-agents` 6.4.0) — MCP
server + skill de engenharia reversa (170 tools) — registrada nos dois agentes
de codificação (OpenCode e Claude Code). Documentado que **análises nativas
(binários) exigem a configuração prévia de um provider** (Hopper, Ghidra ou IDA)
— nenhum instalado nesta máquina. Auditoria da configuração dos agentes sem
quebras encontradas; push do estado completo (inclui o trabalho da sessão
2026-10-07, até então não commitado).

---

## Ações Realizadas

### 1. Instalação do REA (MCP de engenharia reversa)

| Etapa | Comando | Resultado |
|-------|---------|-----------|
| Pré-requisito | `node --version` | v24.21.0 (suportado: 24.x ≥ 24.11) |
| Dry-run | `npx -y rea-agents@latest setup --client opencode --client claude_code --dry-run --json` | `status: planned` — plano revisado (4 ações) |
| Apply | `npx -y rea-agents@latest setup --client opencode --client claude_code --yes --json` | `status: ready` — tudo aplicado |
| Verificação | `rea doctor --client opencode --client claude_code --skill --json` | `scope_checks` 4/4 OK |

**Plano aplicado:**

| Ação | Alvo | Operação |
|------|------|----------|
| MCP registration (OpenCode) | `~/.config/opencode/opencode.jsonc` → `mcp.rea` | update (backup `.rea.backup`) |
| MCP registration (Claude Code) | `~/.claude.json` → `mcpServers.rea` | update (backup `.rea.backup`) |
| Skill (shared / OpenCode) | `~/.agents/skills/reverse-engineer-anything/` | install |
| Skill (Claude Code) | `~/.claude/skills/reverse-engineer-anything/` | install |

- Comando registrado (pinado): `npx -y rea-agents@6.4.0 mcp`
- Skill: versão 37, 170 tools, estado `aligned`
- Skills instaladas em **home** (`~/.agents/skills/`, `~/.claude/skills/`) —
  **fora** das árvores BMAD do projeto; o `npx bmad-method install` não as apaga
- MCP só é carregado após **reiniciar** os agentes (OpenCode e Claude Code)

### 2. Providers nativos — requisito registrado

Como os providers **não serão utilizados no momento**, ficou registrado (em
`AGENTS.md` seção REA e `_bmad-output/tools-registry.md` §3.5) que, na
utilização do MCP REA para **análise nativa de binários**, deve ser realizada a
**configuração e ativação de ao menos um provider** — Hopper, Ghidra ou IDA (ou
todos):

| Provider | Configuração | Validação |
|----------|--------------|-----------|
| Hopper | `rea setup --install-hopper` (aprovação explícita; demo ou licença do operador) | `rea doctor --provider hopper --json` |
| Ghidra 12.1.x | `export GHIDRA_INSTALL_DIR=...` (+ JDK 21+) | `rea doctor --provider ghidra --json` |
| IDA | `export REA_IDA_MCP_CONFIG=...` | `rea doctor --provider ida --json` |

Sem provider ativo, `open_binary`/decompilação/assembly não funcionam; as
análises estáticas (JS/Electron, .NET, Go/Rust/WASM/EVM/SQLite, APK, websites)
operam normalmente.

### 3. Revisão do agente de codificação (evitar problemas/quebras)

| Verificação | Comando | Resultado |
|-------------|---------|-----------|
| Paridade de skills (`.agents` × `.claude`) | `diff <(ls .agents/skills) <(ls .claude/skills)` | ✅ `PARITY_OK` (55 = 55) |
| Contagem de commands | `ls .opencode/commands \| wc -l` | ✅ 55 |
| Config global OpenCode (JSONC) | parse com strip de comentários | ✅ válido; `mcp.rea` shape correto (`type: local`, `command` array) |
| Config projeto OpenCode | `json.load(.opencode/opencode.json)` | ✅ válido (plugin superpowers) |
| Registro Claude Code | `~/.claude.json` → `mcpServers.rea` | ✅ shape correto (`command` + `args`) |
| Varredura de segredos no diff | grep por key/token/secret/password | ✅ limpo (apenas falsos positivos: RTK "Token Killer", docs BMAD) |
| `rea doctor` | escopo opencode + claude_code + skill | ✅ 4/4 checks OK |

**Achados corrigidos:**

1. Deriva de contagens no `tools-registry.md` (dizia 57 skills/commands; real: 55
   skills, 55 commands) — §1.8, §3 e §3.1 corrigidos.
2. `render_skill.py` falhou para `bmad-project-context`:
   `HALT: render entry is missing: .agents/skills/bmad-project-context/workflow.md`
   — o skill tem `SKILL.md` + `references/` + `customize.toml`, sem `workflow.md`.
   Pela regra do AGENTS.md, o workflow não foi executado por outro caminho;
   a auditoria prosseguiu com verificações diretas. **Pendência:** alinhar o
   `render_skill.py` com skills cujo entrypoint é `SKILL.md`.

### 4. Registro e documentação

| Artefato | Ação |
|----------|------|
| `AGENTS.md` | Nova seção "REA — MCP de engenharia reversa" + bullet em Prerequisites (requisito de provider em destaque) |
| `_bmad-output/tools-registry.md` | v1.6.0 — seção 3.5 REA + requisito obrigatório de provider + correção de contagens |
| `_bmad-output/session-log-2026-10-12.md` | Este registro |

### 5. Atualização do repositório GitHub

Push para `origin/main` (`hsoservicos/aprendizado_em_ia`) refletindo o estado
atual do projeto — inclui o acumulado da sessão 2026-10-07 (BMAD 6.12.1,
Impeccable, Superpowers, telemetria desligada), que estava alterado porém não
commitado desde `6544458` (2026-09-09).

---

## Estado Final do Toolchain

| Ferramenta | Versão | Status |
|------------|--------|--------|
| REA (`rea-agents`) | 6.4.0 (skill v37, 170 tools) | ✅ novo — MCP ativo nos 2 agentes |
| BMAD Method | 6.12.1 | ✅ |
| Impeccable | CLI 4.1.0 (engine v0.1.11) | ✅ |
| Superpowers | 6.4.1 (Claude) / 6.4.2 (OpenCode) | ✅ |
| RTK | 0.51.0 | ✅ |
| OpenCode / Claude Code | 1.18.x / 2.1.x | ✅ |

---

## Próximos Passos Sugeridos

1. **Reiniciar OpenCode e Claude Code** para carregar o MCP REA
2. Configurar um provider (Hopper, Ghidra ou IDA) quando for necessário
   analisar binários nativos — ver `AGENTS.md` (seção REA)
3. Corrigir `render_skill.py` para aceitar skills com entrypoint `SKILL.md`
   (ex.: `bmad-project-context`)
4. Testar o MCP REA numa análise estática (JS/Electron ou .NET) que não exige
   provider

---

## Notas

- Backups criados pelo setup: `~/.config/opencode/opencode.jsonc.rea.backup` e
  `~/.claude.json.rea.backup`
- Telemetria Superpowers permanece desligada (`.claude/settings.json` env)
- `.claude/settings.local.json` (hooks Impeccable) segue gitignored — cada
  máquina re-executa o install se quiser os hooks

---

**Fim da sessão. Boa noite!**
