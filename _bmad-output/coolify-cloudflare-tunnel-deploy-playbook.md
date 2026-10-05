# Playbook: Publicação no Coolify com Túnel Cloudflare

**Versão**: 1.0.0
**Data**: 2026-10-05
**Autor**: Hsantos
**Coolify validado em**: v4.3.23 (self-hosted) · Traefik v3.7
**Status**: conhecimento prático validado em publicação real (deploy + teste em navegador)

---

## 0. Para que serve este playbook

Conhecimento **reutilizável** para publicar aplicações (estáticas, web, API REST)
em uma instância **Coolify self-hosted** encaminhada por **túnel Cloudflare**.
Complementa os guias `coolify-deploy-guide.md`, `coolify-github-deploy-guide.md`
e `coolify-local-deploy-guide.md`, registrando **aprendizados de execução real**
que os guias originais não cobrem.

> **Leia a seção 4 antes de qualquer deploy** — o erro de esquema do domínio
> gera um loop de redirect silencioso que parece problema de aplicação.

---

## 1. Topologia de referência

| Componente | Papel | Portas |
| --- | --- | --- |
| `coolify` | Painel + API (Laravel) | 8000→8080 |
| `coolify-proxy` | **Traefik** — roteamento das aplicações | 80, 443, 8080 |
| `coolify-db` | PostgreSQL | 5432 (interna) |
| `coolify-redis` | Redis | 6379 (interna) |
| `coolify-sentinel` / `coolify-realtime` | Métricas / tempo real | — |
| `cloudflared-*` | Conector do túnel nomeado Cloudflare | — |

Fluxo do tráfego:

```text
Navegador → https://app.seudominio.tld
          → Cloudflare (termina TLS)
          → túnel → http://localhost:80   (Traefik / coolify-proxy)
          → container da aplicação (porta exposta, ex.: 80)
```

**Consequência direta:** o Traefik recebe **HTTP** do túnel. Configurar o
domínio como `https://` faz o Traefik redirecionar para HTTPS, o túnel volta a
mandar HTTP e o resultado é **loop de redirect**.

---

## 2. Pré-requisitos

| Item | Verificar |
| --- | --- |
| Coolify rodando | `docker ps` → `coolify`, `coolify-proxy`, `coolify-db` |
| Túnel Cloudflare ativo | `docker ps` → `cloudflared-*` |
| DNS do app apontando para o túnel | `dig +short app.seudominio.tld` |
| GitHub App configurado (repo privado) | Dashboard → Sources → GitHub |
| Docker / Git / `gh` na máquina | `docker --version`, `git --version` |
| CLI do Coolify (opcional) | `coolify --version` |

---

## 3. Acesso à API (para automação)

A API do Coolify vem **desabilitada** e **sem token**. Três passos:

### 3.1. Habilitar a API

Sem acesso ao painel, via banco:

```bash
docker exec coolify-db psql -U coolify -d coolify \
  -c "update instance_settings set is_api_enabled=true;"
```

Confirmação: `GET /api/v1/version` passa a responder a versão (ex.: `4.3.23`)
em vez de `{"message":"API is disabled."}`.

### 3.2. Criar o token de API

Token do tipo **Laravel Sanctum** (`personal_access_tokens`).

> **Armadilhas conhecidas:**
> - `team_id` é **NOT NULL** — omitir gera `422/violação de constraint`.
> - `tokenable_type` deve ser `App\Models\User` com **barra única**. No `psql`,
>   aspas normais não escapam barra; é comum acabar gravando `App\\Models\\User`
>   e receber `Class "App\Models\User" not found` (HTTP 500).
> - O campo `token` guarda `sha256(plaintext)`; o `Bearer` é `{id}|{plaintext}`.

```bash
PLAIN=$(openssl rand -hex 20)
HASH=$(printf '%s' "$PLAIN" | sha256sum | awk '{print $1}')
docker exec coolify-db psql -U coolify -d coolify \
  -c "insert into personal_access_tokens (tokenable_id, tokenable_type, name, token, abilities, team_id, created_at, updated_at) values (0, 'App\Models\User', 'meu-cli', '$HASH', '[\"*\"]'::json, 0, now(), now()) returning id;"
# Bearer = "{id-gerado}|$PLAIN"
```

### 3.3. Configurar o CLI

```bash
coolify context add meu-contexto http://localhost:8000 "{id}|{PLAIN}" --default
coolify context verify     # esperar: Connection + Authentication + Version OK
```

> Guardar o token **fora de repositórios** (`~/.config/coolify/config.json`).
> Rotacionar/limitar escopo quando houver gestão de tokens no painel.

---

## 4. Regra crítica — esquema do domínio

| Esquema registrado no Coolify | Resultado |
| --- | --- |
| `https://app.seudominio.tld` | ❌ **Loop de redirect 307** (Traefik força HTTPS; o túnel encaminha HTTP) |
| `http://app.seudominio.tld` | ✅ Funciona — **o TLS é terminado pelo Cloudflare** |

> **Sempre use `http://` no domínio configurado no Coolify** quando o acesso
> público passar por túnel Cloudflare. O `https://` que o usuário digita é
> garantido pelo Cloudflare, não pelo Traefik.
> Comportamento observado em todos os apps desta instância.

---

## 5. Criar a aplicação

### 5.1. Via CLI (repositório privado / GitHub App)

```bash
coolify project create --name "meu-projeto"

coolify app create github \
  --server-uuid <UUID_DO_SERVIDOR> \
  --project-uuid <UUID_DO_PROJETO> \
  --environment-name production \
  --github-app-uuid <UUID_DO_GITHUB_APP> \
  --git-repository "org/meu-repo" \
  --git-branch main \
  --build-pack dockerfile \
  --base-directory /web \
  --ports-exposes 80 \
  --domains "http://app.seudominio.tld" \
  --name minha-app \
  --health-check-enabled --health-check-path /healthz
```

| Aprendizado | Detalhe |
| --- | --- |
| **`--base-directory` exige barra inicial** | `web` → `422 Validation failed`; `/web` → `201` criado |
| Repositório privado | `app create github` (não `public`) |
| Dockerfile fora da raiz | `--base-directory /web` → build em `web/` com `web/Dockerfile` |
| Porta | usar a porta que o container escuta (padrão útil: **80**) |
| `--instant-deploy` | opcional; para publicação manual, omitir |

### 5.2. Desativar auto-deploy (publicação manual)

O CLI **não expõe** essa flag. Usar a API:

```bash
curl -X PATCH \
  -H "Authorization: Bearer {token}" -H "Content-Type: application/json" \
  -d '{"is_auto_deploy_enabled": false}' \
  http://localhost:8000/api/v1/applications/<UUID>
```

Validar: `GET /api/v1/applications/<UUID>` → `settings.is_auto_deploy_enabled == false`.

---

## 6. Empacotamento Docker/nginx recomendado (arquivos estáticos)

```text
web/
├── Dockerfile        # nginx:alpine · EXPOSE 80 · HEALTHCHECK /healthz
├── nginx.conf        # /healthz, gzip, headers de segurança, cache de assets
├── .dockerignore     # .git, logs, docs fora do contexto
└── <conteudo>/
```

`Dockerfile` mínimo:

```dockerfile
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY <conteudo>/ /usr/share/nginx/html/
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -q -O /dev/null http://127.0.0.1/healthz || exit 1
CMD ["nginx", "-g", "daemon off;"]
```

`nginx.conf` mínimo:

```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;
    charset utf-8;

    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    gzip on;
    gzip_types text/plain text/css application/javascript application/json image/svg+xml;

    location = /healthz {
        access_log off;
        default_type text/plain;
        return 200 "ok\n";
    }

    location / { try_files $uri $uri/ =404; }
}
```

Para aplicações com backend/API: mesma lógica — build Docker → porta exposta →
domínio `http://` → healthcheck que responda `200` sem autenticação.

---

## 7. Deploy e verificação

```bash
coolify deploy uuid <UUID_DA_APP>       # enfileira
coolify deploy get <UUID_DO_DEPLOY>     # status → finished
coolify app get <UUID_DA_APP>           # status → running:healthy
```

### Checklist de validação

| Verificação | Esperado |
| --- | --- |
| `GET https://app.seudominio.tld/` | `200` + conteúdo esperado |
| Assets (`/css`, `/js`, imagens) | `200` |
| `GET /healthz` | `200` |
| `GET /rota-inexistente` | `404` (não `200` genérico) |
| Headers de segurança | `nosniff` · `SAMEORIGIN` · `strict-origin-when-cross-origin` |
| Header `server` | `cloudflare` |
| Status no Coolify | `running:healthy` |
| Teste em navegador externo | Página renderiza corretamente |

---

## 8. Solução de problemas

| Sintoma | Causa provável | Correção |
| --- | --- | --- |
| `307` redirecionando para a mesma URL | Domínio registrado como `https://` | Trocar para `http://` e redeployar |
| `{"message":"API is disabled."}` | `is_api_enabled = false` | Habilitar em `instance_settings` |
| `401 Unauthenticated` | Token ausente/errado | Recriar token; conferir `Bearer {id}\|{plaintext}` |
| `500` + `Class "App\Models\User" not found` | `tokenable_type` com barra duplicada | Corrigir para `App\Models\User` |
| `422` ao criar app | `base-directory` sem barra | Usar `/web` (barra inicial) |
| `422` ao criar token | `team_id` nulo | Informar o `team_id` do usuário |
| Build não acha o Dockerfile | `base-directory` errado | Conferir `/web` + `web/Dockerfile` |
| Página não publica após `git push` | Auto-deploy desativado | Deploy manual (botão ou CLI) |

---

## 9. Comandos de referência

| Ação | Comando |
| --- | --- |
| Contexto | `coolify context list` · `use` · `verify` |
| Projetos | `coolify project list` · `create` |
| Apps | `coolify app list` · `get <uuid>` · `create github` |
| Deploy | `coolify deploy uuid <uuid>` · `deploy get <id>` · `deploy list` |
| Logs | `coolify app logs <uuid>` |
| GitHub Apps | `coolify github list` · `github repos <app-uuid>` |
| Servidores | `coolify server list` |
| Versão | `coolify context version` |

---

## 10. Referências

| Documento | Uso |
| --- | --- |
| `coolify-deploy-guide.md` | Visão geral do Coolify + CLI + passo a passo |
| `coolify-github-deploy-guide.md` | Fontes GitHub (público, Deploy Key, GitHub App) |
| `coolify-local-deploy-guide.md` | Deploy local sem Git |
| `coolify-deploy.sh` (`scripts/`) | Automação de deploy |
| Coolify Docs | https://coolify.io/docs |
