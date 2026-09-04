# Guia Completo: Deploy Local no Coolify (Sem Git)

**Versão**: 1.0.0  
**Data**: 2026-09-04  
**Coolify**: v4.3.14 (self-hosted)  
**Autor**: Hsantos

---

## 1. Visão Geral — Métodos de Deploy Local

O Coolify suporta deploy de ambientes locais **sem necessidade de repositório Git**. Existem 4 métodos principais:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Deploy Local (Sem Git)                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │
│  │  🐳 DOCKER IMAGE │  │  📄 DOCKERFILE   │  │  📦 DOCKER       │   │
│  │                  │  │  (sem Git)       │  │  COMPOSE (Empty) │   │
│  │  Imagem pronta   │  │  Colar no UI     │  │  Colar no UI     │   │
│  │  Docker Hub/GHCR │  │  Sem build ctx   │  │  Multi-service   │   │
│  │                  │  │                  │  │                  │   │
│  │  Melhor para:    │  │  Melhor para:    │  │  Melhor para:    │   │
│  │  • Imagem CI/CD  │  │  • Scripts simples│ │  • Stacks complexas│
│  │  • Imagem pública│  │  • Sem arquivo   │  │  • Sem Git        │   │
│  │  • Deploy rápido │  │                  │  │  • Serviços       │   │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘   │
│                                                                      │
│  ┌──────────────────┐                                               │
│  │  ⚡ SERVICE      │                                               │
│  │  (One-Click)     │                                               │
│  │  Templates 300+  │                                               │
│  │  Prontos para    │                                               │
│  │  usar            │                                               │
│  │                  │                                               │
│  │  Melhor para:    │                                               │
│  │  • WordPress     │                                               │
│  │  • Plausible     │                                               │
│  │  • n8n, Ghost    │                                               │
│  └──────────────────┘                                               │
└─────────────────────────────────────────────────────────────────────┘
```

### Comparativo dos Métodos

| Critério | Docker Image | Dockerfile | Compose Empty | Service |
|----------|-------------|------------|---------------|---------|
| **Fonte** | Registry externo | Colado no UI | Colado no UI | Template |
| **Build** | ❌ Não | ✅ Sim | ✅ Sim | ✅ Sim |
| **Multi-service** | ❌ Não | ❌ Não | ✅ Sim | ✅ Sim |
| **Git necessário** | ❌ Não | ❌ Não | ❌ Não | ❌ Não |
| **Complexidade** | Baixa | Média | Alta | Baixa |
| **Controle total** | Baixo | Médio | Alto | Baixo |
| **Setup** | 1 min | 3 min | 5 min | 1 min |

---

## 2. Docker Image (Imagem Pré-construída)

### 2.1 Quando Usar

- Imagem já construída por CI/CD (GitHub Actions, GitLab CI, etc.)
- Imagem pública do Docker Hub ou GHCR
- Deploy rápido sem necessidade de build
- Deploy de versões específicas (tags ou digests)

### 2.2 Pré-requisitos

- Nome completo da imagem (ex: `nginx:alpine`, `ghcr.io/user/app:1.0`)
- Porta que a aplicação escuta

### 2.3 Passo a Passo Detalhado

#### Passo 1: Criar Recurso no Coolify

```
1. Acesse o Dashboard do Coolify
2. Selecione o Projeto
3. Clique em "+ New" (Novo Recurso)
4. Selecione "Docker Image"
```

#### Passo 2: Configurar a Imagem

```
1. Em "Image Name", insira o nome completo da imagem:
   - Docker Hub: nginx:alpine
   - GHCR: ghcr.io/usuario/app:1.0
   - Docker Hub (formato longo): docker.io/library/nginx:alpine

2. Se necessário, configure:
   - Tag: versão da imagem (ex: 1.25, latest)
   - Digest: SHA256 específico (imutável)

3. Clique em "Save"
```

#### Passo 3: Configurar Runtime

```
1. Vá em Configuration > General
2. Configure "Ports Exposes":
   - Porta interna que a aplicação escuta
   - Ex: 80 para nginx, 3000 para Node.js, 8000 para Python

3. Configure Domains:
   - Adicione o domínio: app.seudominio.com
   - SSL será gerado automaticamente via Let's Encrypt
```

#### Passo 4: Variáveis de Ambiente (Opcional)

```
1. Vá em Configuration > Environment Variables
2. Adicione variáveis necessárias:
   - DATABASE_URL=postgres://...
   - API_KEY=xxx
   - NODE_ENV=production
```

#### Passo 5: Deploy

```
1. Clique em "Deploy"
2. O Coolify puxará a imagem do registry
3. Iniciará o container com as configurações
4. Verifique os logs em Deployments
```

### 2.4 Deploy via CLI

```bash
# Configurar contexto
coolify context add -d production https://coolify.seudominio.com <TOKEN>

# Criar aplicação Docker Image
coolify app create docker-image \
  --server-uuid <SERVER_UUID> \
  --project-uuid <PROJECT_UUID> \
  --environment-name production \
  --docker-image nginx:alpine \
  --ports-exposes 80

# Deploy
coolify deploy name <app-name>
```

### 2.5 Exemplos de Imagens

```bash
# Nginx (servidor web)
nginx:alpine
nginx:1.25-alpine

# Node.js
node:24-alpine
node:24-slim

# Python
python:3.12-slim
python:3.12-alpine

# PostgreSQL
postgres:16-alpine

# Redis
redis:7-alpine

# Imagem do GitHub Container Registry
ghcr.io/usuario/meu-app:1.0.0

# Imagem do Docker Hub (formato longo)
docker.io/library/nginx:alpine
```

### 2.6 Atualização de Imagem

```
1. Vá em Configuration > General
2. Atualize a Tag ou Digest
3. Clique em "Redeploy"
4. O Coolify puxará a nova versão
```

---

## 3. Dockerfile sem Git

### 3.1 Quando Usar

- Dockerfile simples que não precisa de arquivos do repositório
- Testes rápidos de configuração
- Scripts que não precisam de build context

### 3.2 Limitações

**⚠️ IMPORTANTE:** Um Dockerfile colado no Coolify **NÃO tem build context**:
- `COPY` e `ADD` **NÃO funcionam** com arquivos do repositório
- Apenas comandos que não dependem de arquivos locais
- Para `COPY`, use Docker Compose com Git ou suba a imagem para um registry

### 3.3 Passo a Passo Detalhado

#### Passo 1: Criar Recurso

```
1. Dashboard > Projeto > "+ New"
2. Selecione "Dockerfile"
```

#### Passo 2: Colar o Dockerfile

```
1. Na aba "Dockerfile", cole o conteúdo:

# Exemplo: Script Python simples
FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir requests flask
COPY <<EOF /app/main.py
from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Coolify!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF
EXPOSE 5000
CMD ["python", "main.py"]

2. Clique em "Save"
```

#### Passo 3: Configurar Runtime

```
1. Configuration > General > Ports Exposes: 5000
2. Configuration > Networking > Domains: app.seudominio.com
3. Variáveis de ambiente (se necessário)
```

#### Passo 4: Deploy

```
1. Clique em "Deploy"
2. O Coolify construirá a imagem a partir do Dockerfile
3. Criará e iniciará o container
```

### 3.4 Dockerfile Multi-Stage (Sem Git)

```dockerfile
# Build stage
FROM node:24-alpine AS builder
RUN npm install -g pnpm
RUN mkdir /app && cd /app && pnpm init -y && pnpm add express

# Production stage
FROM node:24-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules

# Criar servidor inline
RUN echo 'const express = require("express"); const app = express(); app.get("/", (req, res) => res.send("Hello!")); app.listen(3000, "0.0.0.0");' > /app/server.js

EXPOSE 3000
CMD ["node", "/app/server.js"]
```

---

## 4. Docker Compose Empty (Serviço Customizado)

### 4.1 Quando Usar

- Stacks multi-container sem Git
- Compose complexo com múltiplos serviços
- Testes locais antes de colocar em produção
- Serviços que precisam de banco + cache + app

### 4.2 Como Funciona

```
┌─────────────────────────────────────────────────────────────┐
│                  Docker Compose Empty                        │
│                                                              │
│  Você cola o docker-compose.yml no Coolify                  │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │    App       │    │  PostgreSQL  │    │    Redis     │   │
│  │  (service 1) │    │  (service 2) │    │  (service 3) │   │
│  │  :3000       │    │  :5432       │    │  :6379       │   │
│  └──────────────┘    └──────────────┘    └──────────────┘   │
│                                                              │
│  Coolify:                                                     │
│  • Cria containers                                           │
│  • Configura networking                                      │
│  • Gera variáveis mágicas                                    │
│  • Gerencia lifecycle                                        │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Passo a Passo Detalhado

#### Passo 1: Criar Recurso

```
1. Dashboard > Projeto > "+ New"
2. Selecione "Docker Compose Empty"
```

#### Passo 2: Colar o Docker Compose

```yaml
# Exemplo: App + PostgreSQL + Redis
version: "3.8"

services:
  app:
    image: node:24-alpine
    restart: always
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://postgres:${SERVICE_PASSWORD_DB}@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    command: >
      sh -c "npm install -g express &&
             echo 'const express=require(\"express\");const{Pool}=require(\"pg\");const redis=require(\"redis\");
             const app=express();const pool=new Pool({connectionString:process.env.DATABASE_URL});
             app.get(\"/\",async(req,res)=>{const {rows}=await pool.query(\"SELECT NOW()\");res.json({time:rows[0].now})});
             app.listen(3000,\"0.0.0.0\",()=>console.log(\"Running on :3000\"));' > /app/server.js &&
             npm install express pg redis &&
             node /app/server.js"
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:3000/"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:16-alpine
    restart: always
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${SERVICE_PASSWORD_DB}
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

#### Passo 3: Configurar Variáveis Mágicas

O Coolify gera automaticamente variáveis com o padrão `SERVICE_<TYPE>_<ID>`:

| Variável | Tipo | Resultado |
|----------|------|-----------|
| `${SERVICE_FQDN_APP}` | FQDN | `app-xyz.seudominio.com` |
| `${SERVICE_URL_APP}` | URL | `http://app-xyz.seudominio.com` |
| `${SERVICE_PASSWORD_DB}` | Password | `xYz123abc456def789` (32 chars) |
| `${SERVICE_USER_DB}` | User | `abc123def456ghi789` (16 chars) |
| `${SERVICE_PASSWORD_64_DB}` | Password 64 | `...` (64 chars) |

**Tipos disponíveis:**

```
SERVICE_URL_<ID>        → URL completa
SERVICE_FQDN_<ID>       → Apenas domínio
SERVICE_USER_<ID>       → Usuário aleatório (16 chars)
SERVICE_PASSWORD_<ID>   → Senha aleatória (32 chars)
SERVICE_PASSWORD_64_<ID>→ Senha aleatória (64 chars)
SERVICE_BASE64_<ID>     → String base64 (32 chars)
```

#### Passo 4: Configurar Domínio

```
1. Vá em Configuration > Networking > Domains
2. Adicione o domínio: app.seudominio.com
3. O Coolify configura Traefik automaticamente
```

#### Passo 5: Deploy

```
1. Clique em "Deploy"
2. O Coolify processará o Compose
3. Criará e iniciará todos os containers
4. Configurará networking entre serviços
```

### 4.4 Variáveis Mágicas — Aninhamento

```yaml
services:
  frontend:
    environment:
      SERVICE_URL_FRONTEND: /
      API_URL: ${SERVICE_URL_API_3000}

  api:
    environment:
      SERVICE_URL_API_3000: /v1
      DB_URL: postgres://postgres:${SERVICE_PASSWORD_DB}@db:5432/app

  db:
    environment:
      POSTGRES_PASSWORD: ${SERVICE_PASSWORD_DB}
```

### 4.5 Anotações Coolify

#### `is_directory: true`

```yaml
services:
  filebrowser:
    image: filebrowser/filebrowser:latest
    volumes:
      - type: bind
        source: ./data
        target: /srv
        is_directory: true  # Coolify cria o diretório antes de montar
```

#### `content:` (injetar arquivos inline)

```yaml
services:
  nginx:
    image: nginx:alpine
    volumes:
      - type: content
        content: |
          server {
            listen 80;
            location / {
              proxy_pass http://app:3000;
            }
          }
        target: /etc/nginx/conf.d/default.conf
```

---

## 5. Service (One-Click Templates)

### 5.1 Quando Usar

- Aplicações populares prontas para deploy
- Setup rápido sem configuração manual
- 300+ templates disponíveis

### 5.2 Templates Disponíveis (Exemplos)

| Categoria | Serviços |
|-----------|----------|
| **Analytics** | Plausible, Umami, Matomo |
| **Automação** | n8n, Activepieces, Node-RED |
| **Blogs** | Ghost, WordPress, Grav |
| **CI/CD** | Gitea, Drone CI, Woodpecker |
| **Comunicação** | Rocket.Chat, Mattermost, Revolt |
| **Databases** | PostgreSQL, MySQL, MongoDB, Redis |
| **DevOps** | Portainer, Traefik, Coolify |
| **IDE** | Code-Server, Gitpod |
| **Mídia** | Jellyfin, Navidrome, Photoprism |
| **Monitoring** | Grafana, Uptime Kuma, Healthchecks |
| **Storage** | MinIO, Nextcloud, Seafile |

### 5.3 Passo a Passo Detalhado

#### Passo 1: Criar Recurso

```
1. Dashboard > Projeto > "+ New"
2. Selecione "Service"
3. Pesquise o serviço desejado
4. Clique no template
```

#### Passo 2: Configurar

```
1. O Coolify pré-configura o Compose
2. Ajuste variáveis de ambiente:
   - Senhas
   - Domínios
   - Portas
3. Clique em "Deploy"
```

### 5.4 Exemplo: Plausible Analytics

```yaml
# O Coolify gera isso automaticamente
services:
  plausible:
    image: ghcr.io/plausible/community-edition:v2.1
    command: sh -c "sleep 10 && /entrypoint.sh db createdb && /entrypoint.sh db migrate && /entrypoint.sh run"
    ports:
      - "8000:8000"
    environment:
      BASE_URL: https://analytics.seudominio.com
      DATABASE_URL: postgres://postgres:${SERVICE_PASSWORD_DB}@plausible-db:5432/plausible
      CLICKHOUSE_DATABASE_URL: http://plausible-events-db:8123/plausible_events
    depends_on:
      - plausible-db
      - plausible-events-db

  plausible-db:
    image: postgres:16-alpine
    volumes:
      - plausible-db-data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: ${SERVICE_PASSWORD_DB}

  plausible-events-db:
    image: clickhouse/clickhouse-server:24.3-alpine

volumes:
  plausible-db-data:
```

---

## 6. Fluxograma de Decisão

```
Quer deploy local (sem Git)?
│
├─ Tem uma imagem Docker pronta?
│  │
│  └─ SIM → Use "Docker Image"
│           (registry externo, tag ou digest)
│           Setup: 1 minuto
│
│  └─ NÃO → Tem um Dockerfile?
│     │
│     ├─ SIM → O Dockerfile usa COPY/ADD?
│     │  │
│     │  ├─ NÃO → Use "Dockerfile" (sem Git)
│     │  │        (cole o Dockerfile no UI)
│     │  │        Setup: 3 minutos
│     │  │
│     │  └─ SIM → Use "Docker Compose" com Git
│     │           (precisa de repositório)
│     │
│     └─ NÃO → Tem docker-compose.yml?
│        │
│        ├─ SIM → Use "Docker Compose Empty"
│        │        (cole o Compose no UI)
│        │        Setup: 5 minutos
│        │
│        └─ NÃO → Use "Service" (One-Click)
│                 (escolha template)
│                 Setup: 1 minuto
```

---

## 7. Boas Práticas para Deploy Local

### 7.1 Variáveis de Ambiente

| Prática | Recomendação |
|---------|--------------|
| **Senhas** | ✅ Usar `${SERVICE_PASSWORD_XX}` do Coolify |
| **Hardcoded** | ❌ NUNCA colar senhas no Compose |
| **.env** | ✅ Template sem valores reais |
| **Secrets** | ✅ Usar Coolify Environment Variables |

### 7.2 Networking

| Prática | Recomendação |
|---------|--------------|
| **ports:** | ❌ Evitar publicar portas diretamente |
| **Domains** | ✅ Usar domínios do Coolify (proxy) |
| **Internal** | ✅ Comunicação via nomes de serviço |
| **0.0.0.0** | ✅ App deve escutar em 0.0.0.0 (não 127.0.0.1) |

### 7.3 Health Checks

| Prática | Recomendação |
|---------|--------------|
| **Definir** | ✅ Sempre incluir healthcheck |
| **Intervalo** | ✅ 10-30s (depende da app) |
| **Timeout** | ✅ 5-10s |
| **Retries** | ✅ 3-5 tentativas |

### 7.4 Volumes

| Prática | Recomendação |
|---------|--------------|
| **Dados persistentes** | ✅ Sempre usar volumes para DB |
| **is_directory** | ✅ Usar para bind mounts |
| **Backup** | ✅ Configurar backups do Coolify |

---

## 8. Troubleshooting

### 8.1 Container Não Inicia

```
Causa: Processo não escuta em 0.0.0.0
Solução: Verificar se o app escuta em 0.0.0.0 (não 127.0.0.1)

Causa: Porta incorreta
Solução: Verificar Ports Exposes na configuração

Causa: Health check falha
Solução: Verificar logs, ajustar healthcheck ou desabilitar
```

### 8.2 Docker Compose - Serviços Não Conectam

```
Causa: Serviços em redes diferentes
Solução: Usar "Connect to Predefined Network"

Causa: Nome do serviço incorreto
Solução: Usar nome do serviço como hostname

Causa: Porta interna errada
Solução: Verificar porta que cada serviço escuta
```

### 8.3 Variáveis Mágicas Não Funcionam

```
Causa: Formato incorreto
Solução: Usar SERVICE_<TYPE>_<ID> (maiúsculo)

Causa: Coolify antigo
Solução: Atualizar para v4.0.0-beta.411+

Causa: Compose sem labels
Solução: Não usar Raw Compose Deployment
```

### 8.4 Dockerfile com COPY Não Funciona

```
Causa: Dockerfile sem Git não tem build context
Solução: Usar Docker Compose com Git repository

OU

Solução: Subir arquivos para registry e usar COPY de URL
```

---

## 9. Checklist por Método

### Docker Image

- [ ] Nome completo da imagem verificado
- [ ] Tag ou digest confirmado
- [ ] Porta interna da aplicação identificada
- [ ] Variáveis de ambiente configuradas
- [ ] Domínio configurado
- [ ] Deploy executado com sucesso

### Dockerfile (sem Git)

- [ ] Dockerfile não usa COPY/ADD de arquivos locais
- [ ] Porta EXPOSE definida no Dockerfile
- [ ] Porta Exposes configurada no Coolify
- [ ] Variáveis de ambiente configuradas
- [ ] Domínio configurado
- [ ] Deploy executado com sucesso

### Docker Compose Empty

- [ ] Compose file válido (docker-compose.yml)
- [ ] Variáveis mágicas configuradas (${SERVICE_...})
- [ ] Portas internas corretas
- [ ] Health checks definidos
- [ ] Volumes para dados persistentes
- [ ] Domínio configurado para cada serviço público
- [ ] Deploy executado com sucesso

### Service (One-Click)

- [ ] Template escolhido
- [ ] Variáveis de ambiente personalizadas
- [ ] Senhas alteradas (não usar defaults)
- [ ] Domínio configurado
- [ ] Deploy executado com sucesso

---

## 10. Comandos CLI de Referência

```bash
# ─── Docker Image ───────────────────────────────────────────────
coolify app create docker-image \
  --server-uuid <uuid> \
  --project-uuid <uuid> \
  --environment-name production \
  --docker-image nginx:alpine \
  --ports-exposes 80

# ─── Listar imagens de um app ──────────────────────────────────
coolify app get <app-uuid>

# ─── Deploy ────────────────────────────────────────────────────
coolify deploy name <app-name>
coolify deploy uuid <app-uuid>

# ─── Logs ──────────────────────────────────────────────────────
coolify app logs <app-uuid> --lines 50 --show-timestamps
coolify app logs <app-uuid> --follow

# ─── Status ────────────────────────────────────────────────────
coolify deploy list
coolify deploy get <deploy-uuid>
```

---

**Próximo passo**: Escolher o método de deploy local e seguir o passo a passo
