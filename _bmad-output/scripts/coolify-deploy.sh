#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# Coolify Deploy Script — BMAD Method
# ═══════════════════════════════════════════════════════════════════
# Deploy automatizado de projetos para Coolify
# Suporta: Git (público/privado), Docker Image, Docker Compose local
# Uso: ./coolify-deploy.sh --name <app> --repo <url> [opções]
#      ./coolify-deploy.sh --name <app> --docker-image <image> [opções]
# ═══════════════════════════════════════════════════════════════════

set -euo pipefail

# ─── Configuração Padrão ──────────────────────────────────────────
COOLIFY_URL="${COOLIFY_URL:-}"
COOLIFY_TOKEN="${COOLIFY_TOKEN:-}"
APP_NAME=""
GIT_REPO=""
GIT_BRANCH="main"
BUILD_PACK="nixpacks"
PORT="3000"
ENV_FILE=".env.production"
FORCE_DEPLOY=false
WAIT_FOR_DEPLOY=true
MAX_WAIT=300
REPO_TYPE="public"           # public | deploy-key | github-app | docker-image
PRIVATE_KEY_UUID=""          # UUID da chave privada no Coolify
GITHUB_APP_UUID=""           # UUID do GitHub App no Coolify
DOCKER_IMAGE=""              # Nome da imagem Docker (ex: nginx:alpine)

# ─── Cores ────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ─── Helpers ──────────────────────────────────────────────────────
log_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()    { echo -e "\n${CYAN}═══ $1 ═══${NC}"; }

# ─── Parse Arguments ──────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case $1 in
        --name)         APP_NAME="$2"; shift 2 ;;
        --repo)         GIT_REPO="$2"; shift 2 ;;
        --branch)       GIT_BRANCH="$2"; shift 2 ;;
        --build-pack)   BUILD_PACK="$2"; shift 2 ;;
        --port)         PORT="$2"; shift 2 ;;
        --env-file)     ENV_FILE="$2"; shift 2 ;;
        --repo-type)    REPO_TYPE="$2"; shift 2 ;;
        --private-key)  PRIVATE_KEY_UUID="$2"; shift 2 ;;
        --github-app)   GITHUB_APP_UUID="$2"; shift 2 ;;
        --docker-image) DOCKER_IMAGE="$2"; shift 2 ;;
        --force)        FORCE_DEPLOY=true; shift ;;
        --no-wait)      WAIT_FOR_DEPLOY=false; shift ;;
        --max-wait)     MAX_WAIT="$2"; shift 2 ;;
        --url)          COOLIFY_URL="$2"; shift 2 ;;
        --token)        COOLIFY_TOKEN="$2"; shift 2 ;;
        --help|-h)
            cat << 'EOF'
Coolify Deploy Script — BMAD Method

Uso: ./coolify-deploy.sh --name <app> --repo <url> [opções]
     ./coolify-deploy.sh --name <app> --docker-image <image> [opções]

Opções Obrigatórias (uma das duas):
  --name         Nome da aplicação
  --repo         URL do repositório Git (para deploy via Git)
  --docker-image Nome da imagem Docker (para deploy local, ex: nginx:alpine)

Opções de Repositório (quando usando --repo):
  --repo-type    public|deploy-key|github-app (default: public)
  --private-key  UUID da chave privada (requerido para deploy-key)
  --github-app   UUID do GitHub App (requerido para github-app)

Opções Opcionais:
  --branch       Branch (default: main)
  --build-pack   nixpacks|dockerfile|static|dockercompose (default: nixpacks)
  --port         Porta da aplicação (default: 3000)
  --env-file     Arquivo .env para sync (default: .env.production)
  --url          URL do Coolify (ou defina COOLIFY_URL)
  --token        Token API (ou defina COOLIFY_TOKEN)
  --force        Forçar deploy mesmo sem mudanças
  --no-wait      Não aguardar conclusão do deploy
  --max-wait     Timeout em segundos (default: 300)

Modos de Deploy:
  # Repositório Git público
  ./coolify-deploy.sh --name app --repo https://github.com/user/repo

  # Repositório Git privado com Deploy Key
  ./coolify-deploy.sh --name api --repo git@github.com:user/api.git \
    --repo-type deploy-key --private-key <uuid>

  # Repositório Git privado com GitHub App
  ./coolify-deploy.sh --name web --repo https://github.com/user/web \
    --repo-type github-app --github-app <uuid>

  # Imagem Docker (local/registry)
  ./coolify-deploy.sh --name nginx --docker-image nginx:alpine --port 80

Variáveis de Ambiente:
  COOLIFY_URL    URL do Coolify Dashboard
  COOLIFY_TOKEN  Token de API do Coolify
EOF
            exit 0
            ;;
        *) log_error "Opção desconhecida: $1"; exit 1 ;;
    esac
done

# ─── Validações ───────────────────────────────────────────────────
echo -e "\n${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   Coolify Deploy — BMAD Method                              ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}\n"

if [ -z "$APP_NAME" ]; then
    log_error "Parâmetro --name é obrigatório"
    echo "Use --help para ver opções disponíveis"
    exit 1
fi

# Verificar se tem repo OU docker-image
if [ -z "$GIT_REPO" ] && [ -z "$DOCKER_IMAGE" ]; then
    log_error "Especifique --repo (Git) ou --docker-image (Docker)"
    exit 1
fi

if [ -n "$GIT_REPO" ] && [ -n "$DOCKER_IMAGE" ]; then
    log_error "Use --repo OU --docker-image, não ambos"
    exit 1
fi

if [ -z "$COOLIFY_TOKEN" ]; then
    log_error "Token não configurado. Use --token ou COOLIFY_TOKEN"
    exit 1
fi

if [ -z "$COOLIFY_URL" ]; then
    log_error "URL do Coolify não configurada. Use --url ou COOLIFY_URL"
    exit 1
fi

# Validações por tipo de deploy
if [ -n "$DOCKER_IMAGE" ]; then
    REPO_TYPE="docker-image"
    log_info "Modo: Docker Image"
    log_info "Imagem: $DOCKER_IMAGE"
else
    case "$REPO_TYPE" in
        public)
            if [[ ! "$GIT_REPO" =~ ^https:// ]]; then
                log_warn "Repositório público deve usar URL HTTPS"
            fi
            ;;
        deploy-key)
            if [ -z "$PRIVATE_KEY_UUID" ]; then
                log_error "Repositório privado requer --private-key <uuid>"
                exit 1
            fi
            if [[ ! "$GIT_REPO" =~ ^git@ ]]; then
                log_warn "Deploy Key requer URL SSH (git@github.com:...)"
            fi
            ;;
        github-app)
            if [ -z "$GITHUB_APP_UUID" ]; then
                log_error "GitHub App requer --github-app <uuid>"
                exit 1
            fi
            ;;
        *)
            log_error "Tipo de repositório inválido: $REPO_TYPE (use: public|deploy-key|github-app)"
            exit 1
            ;;
    esac
    log_info "Tipo de repositório: $REPO_TYPE"
fi

# ─── Verificar CLI ────────────────────────────────────────────────
log_step "Phase 1: Verificação do Ambiente"

if ! command -v coolify &>/dev/null; then
    log_error "Coolify CLI não encontrado"
    echo "Instale com: curl -fsSL https://raw.githubusercontent.com/coollabsio/coolify-cli/main/scripts/install.sh | bash"
    exit 1
fi
log_success "Coolify CLI: $(coolify version 2>/dev/null || echo 'instalado')"

if ! command -v jq &>/dev/null; then
    log_warn "jq não encontrado — output pode não ser parseado corretamente"
fi

# ─── Verificar Conexão ────────────────────────────────────────────
log_step "Phase 2: Conexão com Coolify"

if ! coolify context verify 2>/dev/null; then
    log_error "Falha na conexão com: $COOLIFY_URL"
    exit 1
fi
log_success "Conexão verificada: $COOLIFY_URL"

# ─── Obter UUIDs ──────────────────────────────────────────────────
log_step "Phase 3: Obtendo Recursos"

if ! command -v jq &>/dev/null; then
    log_error "jq é necessário para parse de JSON. Instale: apt install jq"
    exit 1
fi

SERVER_UUID=$(coolify server list --format=json 2>/dev/null | jq -r '.[0].uuid // empty' 2>/dev/null)
if [ -z "$SERVER_UUID" ]; then
    log_error "Nenhum servidor encontrado no Coolify"
    exit 1
fi
log_success "Server UUID: $SERVER_UUID"

PROJECT_UUID=$(coolify project list --format=json 2>/dev/null | jq -r '.[0].uuid // empty' 2>/dev/null)
if [ -z "$PROJECT_UUID" ]; then
    log_error "Nenhum projeto encontrado no Coolify"
    exit 1
fi
log_success "Project UUID: $PROJECT_UUID"

# ─── Criar Aplicação ──────────────────────────────────────────────
log_step "Phase 4: Criando Aplicação"

log_info "Nome: $APP_NAME"
log_info "Port: $PORT"
log_info "Tipo: $REPO_TYPE"

# Comando base
CREATE_CMD=""

if [ "$REPO_TYPE" = "docker-image" ]; then
    # Deploy via Docker Image (local/registry)
    log_info "Imagem: $DOCKER_IMAGE"
    CREATE_CMD="coolify app create docker-image \
        --server-uuid $SERVER_UUID \
        --project-uuid $PROJECT_UUID \
        --environment-name production \
        --docker-image $DOCKER_IMAGE \
        --ports-exposes $PORT"
else
    # Deploy via Git
    log_info "Repo: $GIT_REPO"
    log_info "Branch: $GIT_BRANCH"
    log_info "Build Pack: $BUILD_PACK"

    # Comando base
    CREATE_CMD="coolify app create public \
        --server-uuid $SERVER_UUID \
        --project-uuid $PROJECT_UUID \
        --environment-name production \
        --git-repository $GIT_REPO \
        --git-branch $GIT_BRANCH \
        --build-pack $BUILD_PACK \
        --ports-exposes $PORT"

    # Ajustar tipo de repositório
    case "$REPO_TYPE" in
        deploy-key)
            log_info "Configurando Deploy Key: $PRIVATE_KEY_UUID"
            CREATE_CMD="coolify app create deploy-key \
                --server-uuid $SERVER_UUID \
                --project-uuid $PROJECT_UUID \
                --environment-name production \
                --git-repository $GIT_REPO \
                --git-branch $GIT_BRANCH \
                --build-pack $BUILD_PACK \
                --ports-exposes $PORT \
                --private-key-uuid $PRIVATE_KEY_UUID"
            ;;
        github-app)
            log_info "Configurando GitHub App: $GITHUB_APP_UUID"
            CREATE_CMD="coolify app create github-app \
                --server-uuid $SERVER_UUID \
                --project-uuid $PROJECT_UUID \
                --environment-name production \
                --git-repository $GIT_REPO \
                --git-branch $GIT_BRANCH \
                --build-pack $BUILD_PACK \
                --ports-exposes $PORT \
                --github-app-uuid $GITHUB_APP_UUID"
            ;;
    esac
fi

APP_UUID=$(eval "$CREATE_CMD --format=json 2>/dev/null" | jq -r '.uuid // empty' 2>/dev/null)

if [ -z "$APP_UUID" ]; then
    log_error "Falha ao criar aplicação"
    log_info "Comando executado: $CREATE_CMD"
    exit 1
fi

log_success "Aplicação criada: $APP_UUID"

# ─── Sincronizar Variáveis ────────────────────────────────────────
log_step "Phase 5: Configurando Variáveis"

if [ -f "$ENV_FILE" ]; then
    log_info "Sincronizando: $ENV_FILE"
    coolify app env sync "$APP_UUID" --file "$ENV_FILE"
    log_success "Variáveis sincronizadas"
else
    log_warn "Arquivo $ENV_FILE não encontrado — pulando"
fi

# ─── Deploy ───────────────────────────────────────────────────────
log_step "Phase 6: Executando Deploy"

DEPLOY_FLAGS=""
if [ "$FORCE_DEPLOY" = true ]; then
    DEPLOY_FLAGS="--force"
fi

DEPLOY_UUID=$(coolify deploy uuid "$APP_UUID" $DEPLOY_FLAGS --format=json 2>/dev/null | jq -r '.uuid // empty' 2>/dev/null)

if [ -z "$DEPLOY_UUID" ]; then
    log_error "Falha ao iniciar deploy"
    exit 1
fi

log_success "Deploy iniciado: $DEPLOY_UUID"

# ─── Monitorar Deploy ─────────────────────────────────────────────
if [ "$WAIT_FOR_DEPLOY" = true ]; then
    log_step "Phase 7: Monitorando Deploy"
    
    ELAPSED=0
    while [ $ELAPSED -lt $MAX_WAIT ]; do
        STATUS=$(coolify deploy get "$DEPLOY_UUID" --format=json 2>/dev/null | jq -r '.status // empty' 2>/dev/null)
        
        case "$STATUS" in
            "finished"|"completed"|"success")
                log_success "Deploy concluído com sucesso!"
                break
                ;;
            "failed"|"error")
                log_error "Deploy falhou"
                exit 1
                ;;
            *)
                echo -ne "\r${CYAN}[${ELAPSED}s]${NC} Status: ${STATUS:-pendente}...   "
                ;;
        esac
        
        sleep 5
        ELAPSED=$((ELAPSED + 5))
    done
    
    if [ $ELAPSED -ge $MAX_WAIT ]; then
        log_warn "Timeout após ${MAX_WAIT}s"
    fi
    echo ""
fi

# ─── Verificação Final ────────────────────────────────────────────
log_step "Phase 8: Resultado"

echo ""
log_success "═══════════════════════════════════════════════════"
log_success "  Deploy Concluído!"
log_success ""
log_success "  App:       $APP_NAME"
log_success "  UUID:      $APP_UUID"
log_success "  Deploy:    $DEPLOY_UUID"
log_success "  Repo:      $GIT_REPO"
log_success "  Branch:    $GIT_BRANCH"
log_success "  Build:     $BUILD_PACK"
log_success "  Port:      $PORT"
log_success "  Tipo:      $REPO_TYPE"
log_success "═══════════════════════════════════════════════════"
echo ""
log_info "Próximos passos:"
log_info "  1. Verificar logs: coolify app logs $APP_UUID --lines 50"
log_info "  2. Configurar domínio: Dashboard → App → Networking"
log_info "  3. Verificar SSL: Dashboard → App → Networking → Domains"
echo ""

exit 0
