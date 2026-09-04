# Guia Completo: Deploy de Projetos no Coolify

**Versão**: 1.0.0  
**Data**: 2026-09-03  
**Coolify Instanciado**: v4.3.14 (self-hosted)  
**Autor**: Hsantos

---

## 1. Visão Geral do Coolify

### 1.1 O que é Coolify?

Coolify é uma plataforma PaaS (Platform-as-a-Service) self-hosted, open-source, que serve como alternativa ao Heroku, Render, Railway, Vercel e Fly.io. Ele permite deploy de aplicações, bancos de dados e serviços Docker através de um dashboard web.

### 1.2 Sua Instalação Atual

| Componente | Versão | Status |
|------------|--------|--------|
| Coolify | 4.3.14 | ✅ Rodando |
| PostgreSQL | 15-alpine | ✅ Healthy |
| Redis | 7-alpine | ✅ Healthy |
| Traefik Proxy | v3.6 | ✅ Healthy |
| Cloudflared | latest | ✅ Healthy |
| Sentinel | 0.0.22 | ✅ Healthy |
| Realtime | 1.0.17 | ✅ Healthy |

**Portas Ativas**: `80`, `443`, `8000`, `8080`, `6001-6002`

### 1.3 Tipos de Deploy Suportados

| Tipo | Build Pack | Melhor Para |
|------|------------|-------------|
| **Nixpacks** | Auto-detecção | A maioria das aplicações |
| **Static** | Nginx | Sites estáticos, SPAs |
| **Dockerfile** | Customizado | Controle total do build |
| **Docker Compose** | Multi-container | Stacks complexos |
| **Docker Image** | Pré-buildado | Imagens do Docker Hub/GHCR |

---

## 2. Tipos de Aplicação Coolify

### 2.1 Aplicações Baseadas em Git

```
┌─────────────────────────────────────────────────────────────┐
│                    Git Repository                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Público    │  │  GitHub App  │  │ Deploy Key   │       │
│  │  (sem auth)  │  │ (permissões) │  │  (SSH key)   │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         └─────────────────┼─────────────────┘               │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Build Packs Disponíveis                │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │    │
│  │  │Nixpacks  │ │Dockerfile│ │  Static  │ │Compose │ │    │
│  │  │(default) │ │          │ │  (Nginx) │ │        │ │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └────────┘ │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Aplicações Docker Image

Para imagens pré-construídas do Docker Hub, GHCR, ou registry privado.

### 2.3 Serviços One-Click

Templates pré-configurados (Plausible, n8n, Ghost, WordPress, etc.)

---

## 3. Preparação do Projeto para Coolify

### 3.1 Estrutura de Diretórios Recomendada

```
meu-projeto/
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD (opcional)
├── src/                         # Código fonte
├── public/                      # Arquivos estáticos
├── tests/                       # Testes
├── Dockerfile                   # Para build customizado
├── docker-compose.yml           # Para stacks multi-container
├── .env.example                 # Variáveis de ambiente (template)
├── .env.production              # Variáveis de produção (não committar)
├── coolify.json                 # Configuração Coolify (opcional)
├── package.json                 # Dependências Node.js
├── requirements.txt             # Dependências Python
├── README.md
└── .gitignore
```

### 3.2 Dockerfile Otimizado (Exemplo Node.js)

```dockerfile
# ─── Build Stage ──────────────────────────────────────────────
FROM node:24-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# ─── Production Stage ─────────────────────────────────────────
FROM node:24-alpine AS production
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./package.json
USER nextjs
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
CMD ["node", "dist/server.js"]
```

### 3.3 Docker Compose para Coolify

```yaml
version: "3.8"

services:
  app:
    image: ${DOCKER_IMAGE:-my-app:latest}
    restart: always
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://postgres:postgres@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:16-alpine
    restart: always
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: always
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres-data:
  redis-data:
```

### 3.4 Variáveis de Ambiente (`.env.example`)

```bash
# ─── Application ────────────────────────────────────────────────
NODE_ENV=production
PORT=3000
APP_URL=https://app.seudominio.com

# ─── Database ───────────────────────────────────────────────────
DATABASE_URL=postgres://user:password@host:5432/dbname

# ─── Redis ──────────────────────────────────────────────────────
REDIS_URL=redis://host:6379

# ─── API Keys ───────────────────────────────────────────────────
ANTHROPIC_API_KEY=sk-ant-xxx
OPENAI_API_KEY=sk-xxx

# ─── Coolify Magic Variables (auto-injected) ────────────────────
# $SERVICE_FQDN_APP   → Domínio completo do serviço
# $SERVICE_URL_APP    → URL interna do serviço
# $SERVICE_TCP_APP    → TCP do serviço
```

---

## 4. Configuração do Coolify CLI

### 4.1 Instalação

```bash
# Linux/macOS (recomendado)
curl -fsSL https://raw.githubusercontent.com/coollabsio/coolify-cli/main/scripts/install.sh | bash

# Homebrew
brew install coollabsio/coolify-cli/coolify-cli

# Windows (PowerShell)
irm https://raw.githubusercontent.com/coollabsio/coolify-cli/main/scripts/install.ps1 | iex

# Go
go install github.com/coollabsio/coolify-cli/coolify@latest
```

### 4.2 Autenticação

```bash
# 1. Obter token do Coolify Dashboard → /security/api-tokens
# 2. Configurar contexto
coolify context add -d production https://coolify.seudominio.com <TOKEN>

# 3. Verificar conexão
coolify context verify

# 4. Listar recursos disponíveis
coolify project list
coolify server list
```

### 4.3 Comandos Essenciais

```bash
# ─── Recursos ──────────────────────────────────────────────────
coolify resource list                    # Listar todos os recursos
coolify project list                     # Listar projetos
coolify server list                      # Listar servidores

# ─── Aplicações ────────────────────────────────────────────────
coolify app create public \
  --server-uuid <uuid> \
  --project-uuid <uuid> \
  --environment-name production \
  --git-repository https://github.com/user/repo \
  --git-branch main \
  --build-pack nixpacks \
  --ports-exposes 3000

# ─── Variáveis de Ambiente ─────────────────────────────────────
coolify app env create <app-uuid> --key API_KEY --value secret
coolify app env sync <app-uuid> --file .env.production

# ─── Deploy ────────────────────────────────────────────────────
coolify deploy name <app-name>           # Deploy por nome
coolify deploy uuid <app-uuid>           # Deploy por UUID
coolify deploy batch api,worker,frontend # Deploy em lote
coolify deploy list                      # Listar deploys
coolify deploy get <deploy-uuid>         # Detalhes do deploy

# ─── Logs ──────────────────────────────────────────────────────
coolify app logs <app-uuid> --lines 100 --show-timestamps
coolify app logs <app-uuid> --follow     # Stream em tempo real

# ─── Databases ─────────────────────────────────────────────────
coolify database create postgresql \
  --server-uuid <uuid> \
  --project-uuid <uuid> \
  --environment-name production

# ─── Serviços ──────────────────────────────────────────────────
coolify service create --list-types      # Tipos disponíveis
coolify service create wordpress-with-mysql \
  --server-uuid=<uuid> \
  --project-uuid=<uuid> \
  --environment-name=production
```

---

## 5. Roteiro de Deploy Passo a Passo

### Fase 1: Preparação (Antes do Deploy)

```bash
# 1.1 Instalar Coolify CLI
curl -fsSL https://raw.githubusercontent.com/coollabsio/coolify-cli/main/scripts/install.sh | bash

# 1.2 Configurar autenticação
coolify context add -d production https://coolify.seudominio.com <SEU_TOKEN>

# 1.3 Verificar conexão
coolify context verify

# 1.4 Listar recursos existentes
coolify project list
coolify server list
```

### Fase 2: Criar Estrutura no Coolify

```bash
# 2.1 Criar projeto (se não existir)
coolify project create --name "Meu Projeto"

# 2.2 Listar projetos para obter UUID
coolify project list --format=json

# 2.3 Listar servidores para obter UUID
coolify server list --format=json
```

### Fase 3: Criar Aplicação

```bash
# 3.1 Criar aplicação (Nixpacks - auto-detecção)
coolify app create public \
  --server-uuid <SERVER_UUID> \
  --project-uuid <PROJECT_UUID> \
  --environment-name production \
  --git-repository https://github.com/usuario/meu-projeto \
  --git-branch main \
  --build-pack nixpacks \
  --ports-exposes 3000

# 3.2 OU criar com Dockerfile customizado
coolify app create public \
  --server-uuid <SERVER_UUID> \
  --project-uuid <PROJECT_UUID> \
  --environment-name production \
  --git-repository https://github.com/usuario/meu-projeto \
  --git-branch main \
  --build-pack dockerfile \
  --ports-exposes 3000

# 3.3 Salvar UUID da aplicação
APP_UUID="<app-uuid-da-resposta>"
```

### Fase 4: Configurar Variáveis de Ambiente

```bash
# 4.1 Criar variáveis individuais
coolify app env create $APP_UUID --key NODE_ENV --value production
coolify app env create $APP_UUID --key DATABASE_URL --value "postgres://..."
coolify app env create $APP_UUID --key REDIS_URL --value "redis://..."

# 4.2 OU sincronizar de arquivo .env
coolify app env sync $APP_UUID --file .env.production

# 4.3 Listar variáveis configuradas
coolify app env list $APP_UUID
```

### Fase 5: Configurar Domínio e SSL

```bash
# 5.1 Configurar domínio (via Dashboard ou API)
# O Coolify gera SSL automaticamente via Let's Encrypt
# Acesse: Dashboard → App → Networking → Domains
```

### Fase 6: Executar Deploy

```bash
# 6.1 Deploy inicial
coolify deploy uuid $APP_UUID

# 6.2 OU deploy por nome
coolify deploy name "meu-app"

# 6.3 Monitorar deploy
coolify deploy list
coolify deploy get <deploy-uuid>
```

### Fase 7: Verificação Pós-Deploy

```bash
# 7.1 Verificar status da aplicação
coolify app get $APP_UUID

# 7.2 Verificar logs
coolify app logs $APP_UUID --lines 50 --show-timestamps

# 7.3 Testar endpoint de saúde
curl -s https://app.seudominio.com/health
```

---

## 6. Script de Deploy Automatizado

### 6.1 Script Bash para Linux/macOS

```bash
#!/bin/bash
# coolify-deploy.sh — Deploy automatizado para Coolify
# Uso: ./coolify-deploy.sh --repo <url> --name <app-name>

set -euo pipefail

# ─── Configuração ─────────────────────────────────────────────────
COOLIFY_URL="${COOLIFY_URL:-https://coolify.seudominio.com}"
COOLIFY_TOKEN="${COOLIFY_TOKEN:-}"
APP_NAME=""
GIT_REPO=""
GIT_BRANCH="main"
BUILD_PACK="nixpacks"
PORT="3000"
ENV_FILE=".env.production"

# ─── Cores ────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }

# ─── Parse Arguments ──────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case $1 in
        --name) APP_NAME="$2"; shift 2 ;;
        --repo) GIT_REPO="$2"; shift 2 ;;
        --branch) GIT_BRANCH="$2"; shift 2 ;;
        --build-pack) BUILD_PACK="$2"; shift 2 ;;
        --port) PORT="$2"; shift 2 ;;
        --env-file) ENV_FILE="$2"; shift 2 ;;
        --help)
            echo "Uso: $0 --name <app-name> --repo <git-url> [opções]"
            echo ""
            echo "Opções:"
            echo "  --name         Nome da aplicação (obrigatório)"
            echo "  --repo         URL do repositório Git (obrigatório)"
            echo "  --branch       Branch (default: main)"
            echo "  --build-pack   Build pack: nixpacks|dockerfile|static (default: nixpacks)"
            echo "  --port         Porta da aplicação (default: 3000)"
            echo "  --env-file     Arquivo .env para sync (default: .env.production)"
            exit 0
            ;;
        *) log_error "Opção desconhecida: $1"; exit 1 ;;
    esac
done

# ─── Validações ───────────────────────────────────────────────────
if [ -z "$APP_NAME" ] || [ -z "$GIT_REPO" ]; then
    log_error "Parâmetros --name e --repo são obrigatórios"
    exit 1
fi

if [ -z "$COOLIFY_TOKEN" ]; then
    log_error "COOLIFY_TOKEN não configurado"
    exit 1
fi

# ─── Verificar CLI ────────────────────────────────────────────────
if ! command -v coolify &>/dev/null; then
    log_error "Coolify CLI não encontrado. Instale com:"
    echo "  curl -fsSL https://raw.githubusercontent.com/coollabsio/coolify-cli/main/scripts/install.sh | bash"
    exit 1
fi

# ─── Verificar Conexão ────────────────────────────────────────────
log_info "Verificando conexão com Coolify..."
if ! coolify context verify 2>/dev/null; then
    log_error "Falha na conexão com Coolify"
    exit 1
fi
log_success "Conexão verificada"

# ─── Obter UUIDs ──────────────────────────────────────────────────
log_info "Obtendo projetos e servidores..."

SERVER_UUID=$(coolify server list --format=json | jq -r '.[0].uuid // empty')
PROJECT_UUID=$(coolify project list --format=json | jq -r '.[0].uuid // empty')

if [ -z "$SERVER_UUID" ] || [ -z "$PROJECT_UUID" ]; then
    log_error "Não foi possível obter UUIDs do servidor/projeto"
    exit 1
fi

log_success "Server: $SERVER_UUID"
log_success "Project: $PROJECT_UUID"

# ─── Criar Aplicação ──────────────────────────────────────────────
log_info "Criando aplicação: $APP_NAME"

APP_UUID=$(coolify app create public \
    --server-uuid "$SERVER_UUID" \
    --project-uuid "$PROJECT_UUID" \
    --environment-name production \
    --git-repository "$GIT_REPO" \
    --git-branch "$GIT_BRANCH" \
    --build-pack "$BUILD_PACK" \
    --ports-exposes "$PORT" \
    --format=json | jq -r '.uuid // empty')

if [ -z "$APP_UUID" ]; then
    log_error "Falha ao criar aplicação"
    exit 1
fi

log_success "Aplicação criada: $APP_UUID"

# ─── Sincronizar Variáveis ────────────────────────────────────────
if [ -f "$ENV_FILE" ]; then
    log_info "Sincronizando variáveis de: $ENV_FILE"
    coolify app env sync "$APP_UUID" --file "$ENV_FILE"
    log_success "Variáveis sincronizadas"
else
    log_warn "Arquivo $ENV_FILE não encontrado — pulando sync"
fi

# ─── Deploy ───────────────────────────────────────────────────────
log_info "Iniciando deploy..."
DEPLOY_UUID=$(coolify deploy uuid "$APP_UUID" --format=json | jq -r '.uuid // empty')

if [ -z "$DEPLOY_UUID" ]; then
    log_error "Falha ao iniciar deploy"
    exit 1
fi

log_success "Deploy iniciado: $DEPLOY_UUID"

# ─── Monitorar Deploy ─────────────────────────────────────────────
log_info "Monitorando deploy..."
MAX_WAIT=300  # 5 minutos
ELAPSED=0

while [ $ELAPSED -lt $MAX_WAIT ]; do
    STATUS=$(coolify deploy get "$DEPLOY_UUID" --format=json | jq -r '.status // empty')
    
    case "$STATUS" in
        "finished"|"completed")
            log_success "Deploy concluído com sucesso!"
            break
            ;;
        "failed"|"error")
            log_error "Deploy falhou"
            coolify deploy get "$DEPLOY_UUID" --format=json
            exit 1
            ;;
        *)
            echo -ne "\r${CYAN}[${ELAPSED}s]${NC} Status: ${STATUS:-pendente}..."
            ;;
    esac
    
    sleep 5
    ELAPSED=$((ELAPSED + 5))
done

if [ $ELAPSED -ge $MAX_WAIT ]; then
    log_warn "Timeout aguardando deploy (${MAX_WAIT}s)"
fi

# ─── Verificação Final ────────────────────────────────────────────
echo ""
log_info "Verificando aplicação..."
coolify app get "$APP_UUID" --format=pretty

echo ""
log_success "═══════════════════════════════════════════════════"
log_success "  Deploy concluído!"
log_success "  App: $APP_NAME"
log_success "  UUID: $APP_UUID"
log_success "  Deploy: $DEPLOY_UUID"
log_success "═══════════════════════════════════════════════════"
```

---

## 7. CI/CD com GitHub Actions

### 7.1 Workflow de Deploy

```yaml
# .github/workflows/deploy-coolify.yml
name: Deploy to Coolify

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  COOLIFY_URL: ${{ secrets.COOLIFY_URL }}
  COOLIFY_TOKEN: ${{ secrets.COOLIFY_TOKEN }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install Coolify CLI
        run: |
          curl -fsSL https://raw.githubusercontent.com/coollabsio/coolify-cli/main/scripts/install.sh | bash

      - name: Configure Context
        run: |
          coolify context add -d production $COOLIFY_URL $COOLIFY_TOKEN

      - name: Deploy Application
        run: |
          coolify deploy name "my-app" --force

      - name: Verify Deployment
        run: |
          sleep 30
          coolify app logs "my-app" --lines 20 --show-timestamps
```

---

## 8. Templates de Dockerfile por Framework

### 8.1 Next.js

```dockerfile
FROM node:24-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:24-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
ENV PORT=3000
CMD ["node", "server.js"]
```

### 8.2 Django

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput

FROM python:3.12-slim AS production
WORKDIR /app
COPY --from=builder /app /app
RUN adduser --disabled-password --gecos '' django
USER django
EXPOSE 8000
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### 8.3 Laravel

```dockerfile
FROM php:8.4-fpm AS builder
WORKDIR /var/www/html
COPY composer.json composer.lock ./
RUN composer install --no-dev --optimize-autoloader
COPY . .
RUN php artisan config:cache && php artisan route:cache && php artisan view:cache

FROM php:8.4-fpm AS production
WORKDIR /var/www/html
COPY --from=builder /var/www/html /var/www/html
RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache
EXPOSE 9000
CMD ["php-fpm"]
```

### 8.4 Python FastAPI

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM python:3.12-slim AS production
WORKDIR /app
COPY --from=builder /app /app
RUN adduser --disabled-password --gecos '' appuser
USER appuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 9. Variáveis Mágicas do Coolify

O Coolify injeta automaticamente variáveis em cada container:

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `$COOLIFY_URL` | URL do dashboard | `https://coolify.example.com` |
| `$COOLIFY_FQDN` | Domínio do app | `app.example.com` |
| `$SERVICE_FQDN_<NAME>` | Domínio do serviço | `api.example.com` |
| `$SERVICE_URL_<NAME>` | URL interna | `http://service:3000` |
| `$SERVICE_TCP_<NAME>` | TCP do serviço | `service:3000` |

---

## 10. Checklist de Deploy

### Antes do Deploy

- [ ] Coolify CLI instalado e autenticado
- [ ] Repositório Git configurado
- [ ] Dockerfile ou Nixpacks configurado
- [ ] Variáveis de ambiente definidas
- [ ] Health check endpoint disponível
- [ ] Domínio DNS apontando para o servidor
- [ ] Portas 80/443 abertas no firewall

### Durante o Deploy

- [ ] Deploy sem erros no build
- [ ] Containers healthy
- [ ] Logs sem erros críticos
- [ ] Health check passando

### Após o Deploy

- [ ] Aplicação acessível via domínio
- [ ] SSL/HTTPS funcionando
- [ ] Variáveis de ambiente corretas
- [ ] Banco de dados conectando
- [ ] Redis conectando (se aplicável)
- [ ] Monitoramento configurado
- [ ] Backups agendados

---

## 11. Troubleshooting

### Problema: Deploy falha no build

```bash
# Verificar logs do build
coolify app logs <app-uuid> --lines 100

# Verificar se o Dockerfile está correto
docker build -t test .
```

### Problema: Container não inicia

```bash
# Verificar logs do container
coolify app logs <app-uuid> --lines 50 --show-timestamps

# Verificar health check
coolify app get <app-uuid>
```

### Problema: SSL não funciona

```bash
# Verificar domínio no Coolify Dashboard
# Networking → Domains
# Verificar DNS: dig app.seudominio.com
# Verificar certificado: openssl s_client -connect app.seudominio.com:443
```

### Problema: Variáveis de ambiente não aplicam

```bash
# Listar variáveis configuradas
coolify app env list <app-uuid>

# Sincronizar novamente
coolify app env sync <app-uuid> --file .env.production

# Redeploy após mudança de variáveis
coolify deploy uuid <app-uuid> --force
```

---

## 12. Referências

| Recurso | URL |
|---------|-----|
| Coolify Docs | https://coolify.io/docs |
| Coolify CLI GitHub | https://github.com/coollabsio/coolify-cli |
| API Reference | https://coolify.io/docs/api-reference |
| Discord | https://coollabs.io/discord |
| Self-hosted Install | `curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash` |

---

**Status**: Documento pronto para uso  
**Próximo passo**: Executar `coolify context verify` e iniciar o deploy
