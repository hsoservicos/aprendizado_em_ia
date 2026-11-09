# Relatório de Auditoria — Ferramentas de Apoio e Suporte — 2026-11-09

**Escopo**: `aprendizado_em_ia` (hub de ferramentas BMAD — repo
`hsoservicos/aprendizado_em_ia`, checkout em `/home/hsantos/app`) + atualização das
ferramentas de apoio e suporte usadas pelo projeto.
**Executado por**: OpenCode (DeepSeek V4 Pro)
**Estado do repo**: `main`, em `ddec463` no início; alterações aplicadas e
committadas ao final (documentação + relatório).

---

## 1. Resumo executivo

| # | Achado | Severidade | Ação |
|---|--------|------------|------|
| 1 | RTK `1.1.0` → **1.2.0** disponível (release `rtk-ai/rtk` v1.2.0, 2026-11-08) | Média | ✅ Atualizado (binário, backup preservado) |
| 2 | OpenCode v2.2.6 — verificar se há versão mais nova | Baixa | ✅ Confirmado já na última (`opencode upgrade` → "already installed") |
| 3 | Superpowers (Claude) 7.0.0 — verificar 7.0.2 | Baixa | ✅ Marketplace já no último (7.0.0); v7.0.2 ainda não publicado no marketplace |
| 4 | Node declarado v24.22.2 mas shell ativo reportava v24.21.0 | Baixa | ✅ Falso positivo — artefato de shell sem `nvm`; `nvm use 24` → v24.22.2/npm 12.2.2 |
| 5 | **Drift de documentação**: `README.md`, `README.pt-BR.md`, `README.es.md` e `CLAUDE.md` referenciando agentes removidos (Docker/Python 3.14/PHP 8.4/PostgreSQL 18) e versões antigas | Alta | ✅ Corrigidos (badges, contagem 57→55, tabelas, exemplos, versões) |
| 6 | `project-replication-guide.md` §5 com `mkdir` das skills removidas | Média | ✅ Reescrito para Angular 21/Java 21 |
| 7 | `tools-registry.md` com RTK defasado (1.1.0) | Baixa | ✅ Atualizado (v1.7.0 → v1.8.0) |

---

## 2. Versões — instalada × mais recente (resultado da verificação)

| Ferramenta | Instalada | Mais recente | Resultado |
|---|---|---|---|
| BMAD Method | 6.12.4 | 6.12.4 | ✅ atual |
| Impeccable | 4.8.1 (engine v0.1.19) | 4.8.1 | ✅ atual |
| REA (`rea-agents`) | 6.8.0 (skill v49) | 6.8.0 | ✅ atual |
| Claude Code | 2.1.319 | 2.1.319 | ✅ atual |
| OpenCode | v2.2.6 | v2.2.6 | ✅ atual |
| CrewAI | 1.15.39 | 1.15.39 | ✅ atual |
| uv | 0.13.7 | 0.13.7 | ✅ atual |
| GitHub CLI (`gh`) | 2.103.3 | 2.103.3 | ✅ atual |
| ripgrep (`rg`) | 15.2.0 | 15.2.0 | ✅ atual |
| npm | 12.2.2 | 12.2.2 | ✅ atual |
| Superpowers (OpenCode) | 7.0.2 | v7.0.2 | ✅ atual |
| Superpowers (Claude) | 7.0.0 | v7.0.2 (GitHub) / 7.0.0 (marketplace) | ✅ atual no marketplace |
| **RTK** | **1.2.0** | v1.2.0 | ✅ **atualizado nesta auditoria** |
| Node.js | v24.22.2 | LTS v26.13.0 (Lithium) | 🔵 salto major disponível (não aplicado) |
| Python | 3.14.4 | 3.14.10 / 3.15.2 / 3.16.0 | 🔵 opcional (não aplicado) |
| Git | 2.53.0 | 2.56.0 | 🔵 opcional (não aplicado) |

---

## 3. Atualizações de máquina aplicadas

| Ferramenta | Antes | Depois | Comando / método | Backup |
|---|---|---|---|---|
| RTK | 1.1.0 | **1.2.0** | download do asset `rtk-x86_64-unknown-linux-musl.tar.gz` (variante full) | `~/.local/share/rtk/backups/rtk-1.1.0` |

**Verificações (sem mudança necessária):**

- `opencode upgrade` → "OpenCode upgrade skipped: 2.2.6 is already installed".
- `claude plugin update superpowers` → "already at the latest version (7.0.0)".
- `nvm use 24` → `node v24.22.2`, `npm 12.2.2` (o desvio para v24.21.0/npm 12.2.0
  era apenas o shell não-login sem carregar o `nvm`).

---

## 4. Correções de documentação aplicadas

| Arquivo | Correção |
|---|---|
| `README.md` | Badges (6.12.4, 55 skills, CrewAI 1.15.39); "4 → 2 technology-specific agents (Angular 21, Java 21)"; tabela de skills (removidas → `bmad-angular21`/`bmad-java21`); seção de agentes (4→2); contagem "57→55" em todos os pontos; tabela "Installed tools" com versões atuais; exemplos de uso e render (`bmad-docker` → `bmad-angular21`). |
| `README.pt-BR.md` | Mesmas correções, texto em português. |
| `README.es.md` | Mesmas correções, texto em espanhol. |
| `CLAUDE.md` | Agentes de tecnologia listados (`/bmad-agent-angular21`, `/bmad-agent-java21`); cache Superpowers `6.4.1` → `7.0.0`. |
| `_bmad-output/project-replication-guide.md` | §5 reescrito: Angular 21/Java 21 no lugar de Docker/Python/PHP/PostgreSQL + nota de remoção (`d6e8139`). |
| `_bmad-output/tools-registry.md` | RTK 1.1.0 → 1.2.0 (§4.1, nota de versão, §10); entrada no log de instalação; versão v1.7.0 → v1.8.0. |

---

## 5. Atualizações opcionais recomendadas (não aplicadas)

Estas são atualizações maiores de runtime/plataforma, fora do toolchain ativo e
que exigem validação antes de aplicar:

| Ferramenta | Atual → Disponível | Risco | Quando aplicar |
|---|---|---|---|
| Node.js | v24.22.2 | **v26.13.0** (LTS Lithium) | Salto major de linha LTS; validar REA (≥ 24.22.1) e CrewAI | Próximo ciclo, com teste |
| Python | 3.14.4 | 3.14.10 (patch) / 3.15.2 / 3.16.0 | 3.14.10 é seguro (patch); 3.15/3.16 exigem testar scripts BMAD (`render_skill.py`, validators) | Patch a qualquer momento |
| Git | 2.53.0 | 2.56.0 | Baixo (minor) | Quando conveniente (PPA/compilação) |

---

## 6. Referências de atualização (checklist)

```bash
# Toolchain (já aplicado nesta auditoria)
rtk --version                                   # → 1.2.0

# Verificações recorrentes
npx bmad-method install                         # BMAD (6.12.4)
npx impeccable install -y --providers=claude,opencode --scope=project --force
npx rea-agents@latest setup --client opencode --client claude_code --yes
opencode upgrade                                # OpenCode v2
claude plugin update superpowers                # Superpowers (Claude)
uv self update && uv tool upgrade crewai        # uv + CrewAI
nvm install 24 && nvm alias default 24          # Node 24 LTS (ou 26 quando validado)
npm install -g npm@latest                       # npm
```

**Após qualquer `npx bmad-method install`/`--action quick-update`:** rodar a
sequência de recuperação documentada em `AGENTS.md` (restaurar skills
customizadas + re-instalar Impeccable + re-mirror `impeccable`), pois o
instalador apaga pastas fora do manifest.
