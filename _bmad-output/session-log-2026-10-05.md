# Registro da Sessão — 2026-10-05

**Data**: 2026-10-05
**Duração**: ~2 horas
**Usuário**: Hsantos
**Agente**: OpenCode (mimo-v2.6-pro)
**Objetivo**: Transferir para este repositório o conhecimento desenvolvido em
publicação real no Coolify (projeto `servicetec`), mantendo o template atualizado
para futuras elaborações.

---

## Resumo

Sessão de **transferência de conhecimento**. Um projeto real (web SaaS
`servicetec`) foi publicado em instância Coolify self-hosted com túnel
Cloudflare. Durante a execução surgiram **lacunas práticas** não cobertas pelos
guias existentes deste repositório. O objetivo desta sessão é **registrar o
aprendizado** de forma reutilizável, sem contaminar o template com conteúdo
específico do projeto.

---

## Conhecimento desenvolvido no projeto real

| Área | Aprendizado |
|------|-------------|
| Túnel Cloudflare + Traefik | Domínio no Coolify deve ser `http://` — `https://` gera loop de redirect 307 |
| API do Coolify | Vem desabilitada (`is_api_enabled`); token Sanctum exige `team_id` e `tokenable_type` correto |
| CLI | `app create github --base-directory /web` (barra inicial obrigatória, senão 422) |
| Auto-deploy | Flag não existe no CLI — desativar via `PATCH` na API |
| Empacotamento | Padrão Docker/nginx com `/healthz` na porta 80 é portável para estáticos e APIs |
| Validação | Checklist HTTP + headers + status no Coolify + teste em navegador externo |

---

## Ações Realizadas neste repositório

### 1. Verificação de sincronização

| Comando | Resultado |
|---------|-----------|
| `git status` | Repo limpo, `main` em dia com `origin/main` |
| `git log --oneline -3` | `6544458` (session log 2026-09-09) |

### 2. Análise de lacunas nos guias existentes

| Guia | Lacuna identificada |
|------|---------------------|
| `coolify-deploy-guide.md` | Sem o esquema `http://`; versões desatualizadas (4.3.14 → 4.3.23) |
| `coolify-github-deploy-guide.md` | Passo de domínio não menciona o protocolo com túnel Cloudflare |
| `coolify-local-deploy-guide.md` | Sem cobertura de API/token |

### 3. Conteúdo registrado

| Arquivo | Tipo | Conteúdo |
|---------|------|----------|
| `coolify-cloudflare-tunnel-deploy-playbook.md` | **NOVO** | Playbook reutilizável: topologia, API/token, CLI, regra do esquema `http://`, empacotamento Docker/nginx, deploy, checklist, solução de problemas |
| `coolify-deploy-guide.md` | **ATUALIZADO** | Nova seção 13 "Errata e aprendizados de execução" (7 aprendizados críticos) |
| `tools-registry.md` | **ATUALIZADO** | Versões do toolchain atualizadas |
| `session-log-2026-10-05.md` | **NOVO** | Este registro |

---

## Atualização do toolchain (versões validadas)

| Ferramenta | Antes | Agora |
|------------|-------|-------|
| Node.js | v24.20.0 | **v24.21.0** (LTS Krypton) |
| npm | 12.0.2 | **12.2.0** |
| uv | 0.12.9 | **0.12.23** |
| CrewAI | 1.15.18 | **1.15.23** |
| GitHub CLI | 2.73.0 | **2.102.0** |
| RTK | — | **0.51.0** |
| Claude Code | — | **2.1.289** |
| Coolify (instância) | 4.3.14 | **4.3.23** |
| Traefik (proxy) | v3.6 | **v3.7** |

---

## O que NÃO foi registrado (e por quê)

Conteúdo **específico do projeto `servicetec`** ficou no repositório do projeto,
para não contaminar este template:

- Escopo, domínios e regras de negócio do produto
- URLs e nomes de aplicações do projeto
- Conteúdo da página de apresentação
- Estrutura de `controle/`, `backups/` e `docs/conhecimento/` do projeto

> A **estrutura de governança** (controle sequencial + backups permanentes +
> artefatos de conhecimento) é reutilizável e está documentada nos artefatos do
> projeto; se adotada em outros projetos, pode ser extraída como template futuro.

---

## Resultado

✅ Template atualizado com conhecimento de execução real.
✅ Guias de Coolify complementados com aprendizados críticos ausentes.
✅ Toolchain documentado nas versões vigentes.
✅ Conteúdo específico de projeto mantido fora do template.

**Próximo passo**: usar `coolify-cloudflare-tunnel-deploy-playbook.md` como
referência de publicação em novos projetos.


---

## Adendo — mesma data, segunda rodada (proxy layer)

**Objetivo:** registrar a análise **Traefik × nginx** (redundância, boas práticas,
desempenho) e a decisão de camada de proxy para publicações no Coolify.

### Aprendizado consolidado

| Tema | Achado |
|------|--------|
| `fileServer` no Traefik | **Não existe** em v3.7 — Traefik não serve estáticos |
| Build pack `static` do Coolify | Gera configuração **nginx** (`defaultNginxConfiguration`) |
| Custo do hop Traefik | ~0,7 ms · ~21% de throughput (1072 → 845 req/s) |
| Custo do nginx | ~3 MiB RAM · imagem ~75 MB |
| Gargalo real | **Rede/Cloudflare (~200 ms)** — não a pilha de proxy |
| Redundância real | **Somente** em aplicações dinâmicas com nginx no meio |
| Anti-padrão comum | `gzip` no nginx **e** `compress` no Traefik = compressão duplicada |

### Conteúdo registrado nesta rodada

| Arquivo | Tipo | Conteúdo |
|---------|------|----------|
| `proxy-layer-traefik-nginx-guide.md` | **NOVO** | Guia de camada de proxy: papéis, evidências, medições, regra de ouro "cada função uma vez", matriz de decisão, checklist de auditoria |
| `README.md` / `README.pt-BR.md` / `README.es.md` | **ATUALIZADOS** | Referência ao novo guia |

### Decisão de padrão adotada

```text
ESTÁTICO:   Cloudflare → Traefik → nginx (arquivos)
API:        Cloudflare → Traefik → aplicação            ← sem nginx
SPA + API:  Cloudflare → Traefik → nginx (SPA) / app (/api)
```

Funções de proxy centralizadas no **Traefik**: redirect, headers, compressão.
nginx mantido **somente** para estáticos (cache de assets, `try_files`, `/healthz`).
