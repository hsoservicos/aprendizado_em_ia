#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# BMAD Method — Automated Installation Script for Linux (Ubuntu/Debian)
# ═══════════════════════════════════════════════════════════════════
# Version: 1.0.0
# Author: Hsantos
# Date: 2026-09-03
# Usage: bash install-linux.sh [--project-dir /path/to/project]
# ═══════════════════════════════════════════════════════════════════

set -euo pipefail

# ─── Configuration ─────────────────────────────────────────────────
NODE_VERSION="24"
PYTHON_MIN_VERSION="3.10"
UV_VERSION="0.12.9"
RTK_VERSION="0.47.0"
RIPGREP_VERSION="14.1.1"
BMAD_VERSION="6.11.0"

# ─── Colors ────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ─── Helpers ───────────────────────────────────────────────────────
log_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()    { echo -e "\n${CYAN}═══ $1 ═══${NC}"; }

check_command() {
    command -v "$1" >/dev/null 2>&1
}

get_version() {
    "$1" --version 2>/dev/null | head -1 | grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1
}

# ─── Parse Arguments ──────────────────────────────────────────────
PROJECT_DIR="${HOME}/app"
while [[ $# -gt 0 ]]; do
    case $1 in
        --project-dir)
            PROJECT_DIR="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [--project-dir /path/to/project]"
            echo ""
            echo "Options:"
            echo "  --project-dir DIR  Project directory (default: ~/app)"
            echo "  --help, -h         Show this help"
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# ─── Main ──────────────────────────────────────────────────────────
echo -e "\n${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   BMAD Method — Automated Installation for Linux            ║${NC}"
echo -e "${CYAN}║   Version: ${BMAD_VERSION}                                          ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}\n"

# ─── Phase 1: System Dependencies ─────────────────────────────────
log_step "Phase 1: System Dependencies"

if check_command apt; then
    log_info "Detected Debian/Ubuntu system"
    
    log_info "Updating package lists..."
    sudo apt update -qq
    
    log_info "Installing build essentials..."
    sudo apt install -y -qq \
        build-essential \
        curl \
        wget \
        git \
        unzip \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release
    
    log_success "System dependencies installed"
else
    log_warn "Non-Debian system detected. Manual installation may be required."
fi

# ─── Phase 2: Node.js ─────────────────────────────────────────────
log_step "Phase 2: Node.js (v${NODE_VERSION})"

if check_command node; then
    CURRENT_NODE=$(get_version node)
    log_info "Node.js already installed: v${CURRENT_NODE}"
    
    if [[ "$(echo "$CURRENT_NODE" | cut -d. -f1)" -ge "$NODE_VERSION" ]]; then
        log_success "Node.js version OK"
    else
        log_warn "Node.js version too old. Upgrading..."
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
        nvm install "$NODE_VERSION"
        nvm use "$NODE_VERSION"
        nvm alias default "$NODE_VERSION"
    fi
else
    log_info "Installing Node.js via nvm..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    nvm install "$NODE_VERSION"
    nvm use "$NODE_VERSION"
    nvm alias default "$NODE_VERSION"
fi

log_success "Node.js: $(node --version)"
log_success "npm: $(npm --version)"

# ─── Phase 3: Python ──────────────────────────────────────────────
log_step "Phase 3: Python (>= ${PYTHON_MIN_VERSION})"

if check_command python3; then
    CURRENT_PY=$(get_version python3)
    log_info "Python already installed: ${CURRENT_PY}"
else
    log_info "Installing Python3..."
    sudo apt install -y -qq python3 python3-pip python3-venv
fi

log_success "Python: $(python3 --version)"

# ─── Phase 4: Git ──────────────────────────────────────────────────
log_step "Phase 4: Git"

if check_command git; then
    log_info "Git already installed: $(git --version)"
else
    log_info "Installing Git..."
    sudo apt install -y -qq git
fi

log_success "Git: $(git --version)"

# ─── Phase 5: uv (Python Package Manager) ─────────────────────────
log_step "Phase 5: uv v${UV_VERSION}"

if check_command uv; then
    log_info "uv already installed: $(uv --version)"
else
    log_info "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add to PATH for current session
    export PATH="$HOME/.local/bin:$PATH"
    
    # Add to bashrc if not present
    if ! grep -q '.local/bin' "$HOME/.bashrc" 2>/dev/null; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    fi
fi

log_success "uv: $(uv --version)"

# ─── Phase 6: ripgrep ─────────────────────────────────────────────
log_step "Phase 6: ripgrep v${RIPGREP_VERSION}"

if check_command rg; then
    log_info "ripgrep already installed: $(rg --version | head -1)"
else
    log_info "Installing ripgrep..."
    cd /tmp
    curl -LO "https://github.com/BurntSushi/ripgrep/releases/download/${RIPGREP_VERSION}/ripgrep-${RIPGREP_VERSION}-x86_64-unknown-linux-musl.tar.gz"
    tar xzf "ripgrep-${RIPGREP_VERSION}-x86_64-unknown-linux-musl.tar.gz"
    mkdir -p "$HOME/.local/bin"
    cp "ripgrep-${RIPGREP_VERSION}-x86_64-unknown-linux-musl/rg" "$HOME/.local/bin/"
    rm -rf "ripgrep-${RIPGREP_VERSION}-x86_64-unknown-linux-musl"*
    cd -
fi

log_success "ripgrep: $(rg --version | head -1)"

# ─── Phase 7: RTK (Optional) ──────────────────────────────────────
log_step "Phase 7: RTK v${RTK_VERSION} (Optional)"

if check_command rtk; then
    log_info "RTK already installed: $(rtk --version)"
else
    log_info "Installing RTK..."
    cd /tmp
    
    # Try to download RTK
    if curl -LO "https://github.com/anomalyco/rtk/releases/latest/download/rtk-linux-x64" 2>/dev/null; then
        chmod +x rtk-linux-x64
        mv rtk-linux-x64 "$HOME/.local/bin/rtk"
        cd -
        log_success "RTK installed"
    else
        log_warn "RTK download failed. You can install it manually later."
        log_warn "Visit: https://github.com/anomalyco/rtk"
        cd -
    fi
fi

if check_command rtk; then
    log_success "RTK: $(rtk --version)"
else
    log_warn "RTK not installed (optional)"
fi

# ─── Phase 8: IDE Setup ───────────────────────────────────────────
log_step "Phase 8: IDE Setup"

# OpenCode
if check_command opencode; then
    log_info "OpenCode already installed"
else
    log_info "Installing OpenCode..."
    npm install -g opencode 2>/dev/null || log_warn "OpenCode install failed (optional)"
fi

# Claude Code
if check_command claude; then
    log_info "Claude Code already installed"
else
    log_info "Installing Claude Code..."
    npm install -g @anthropic-ai/claude-code 2>/dev/null || log_warn "Claude Code install failed (optional)"
fi

# ─── Phase 9: Project Directory ───────────────────────────────────
log_step "Phase 9: Project Directory"

log_info "Setting up project at: ${PROJECT_DIR}"

if [ -d "$PROJECT_DIR" ]; then
    log_info "Project directory already exists"
else
    mkdir -p "$PROJECT_DIR"
    log_success "Created project directory"
fi

cd "$PROJECT_DIR"

# Initialize git if needed
if [ ! -d ".git" ]; then
    log_info "Initializing git repository..."
    git init
    git branch -M main
fi

# ─── Phase 10: BMAD Method Installation ───────────────────────────
log_step "Phase 10: BMAD Method v${BMAD_VERSION}"

if [ -d "_bmad" ]; then
    log_info "BMAD already installed"
else
    log_info "Installing BMAD Method..."
    npx "bmad-method@${BMAD_VERSION}" install
fi

# ─── Phase 11: Project Structure ──────────────────────────────────
log_step "Phase 11: Project Structure"

# Create required directories
mkdir -p docs
mkdir -p _bmad-output

# Create .gitignore if not exists
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'GITIGNORE'
# Dependencies
node_modules/
__pycache__/
*.pyc
.venv/
venv/
venv*/

# BMAD personal configs
_bmad/config.user.toml
_bmad/custom/config.user.toml

# Output artifacts (optional)
_bmad-output/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
.env.*.local

# Logs
*.log
logs/
GITIGNORE
    log_success "Created .gitignore"
fi

# ─── Phase 12: Validation ─────────────────────────────────────────
log_step "Phase 12: Validation"

echo ""
echo -e "${CYAN}═══ Installation Summary ═══${NC}"
echo ""

ERRORS=0

# Check Node.js
if check_command node; then
    log_success "Node.js: $(node --version)"
else
    log_error "Node.js not found"
    ((ERRORS++))
fi

# Check npm
if check_command npm; then
    log_success "npm: $(npm --version)"
else
    log_error "npm not found"
    ((ERRORS++))
fi

# Check Python
if check_command python3; then
    log_success "Python: $(python3 --version)"
else
    log_error "Python not found"
    ((ERRORS++))
fi

# Check uv
if check_command uv; then
    log_success "uv: $(uv --version)"
else
    log_error "uv not found"
    ((ERRORS++))
fi

# Check Git
if check_command git; then
    log_success "Git: $(git --version)"
else
    log_error "Git not found"
    ((ERRORS++))
fi

# Check RTK
if check_command rtk; then
    log_success "RTK: $(rtk --version)"
else
    log_warn "RTK: Not installed (optional)"
fi

# Check ripgrep
if check_command rg; then
    log_success "ripgrep: $(rg --version | head -1)"
else
    log_warn "ripgrep: Not installed (recommended)"
fi

# Check BMAD
if [ -d "_bmad" ]; then
    log_success "BMAD Method: Installed"
else
    log_error "BMAD Method: Not installed"
    ((ERRORS++))
fi

# Count skills
SKILLS_COUNT=$(ls -d .agents/skills/bmad-* 2>/dev/null | wc -l)
COMMANDS_COUNT=$(ls .opencode/commands/bmad-*.md 2>/dev/null | wc -l)

echo ""
echo -e "${CYAN}═══ Skills Installed ═══${NC}"
echo "Skills: ${SKILLS_COUNT}"
echo "Commands: ${COMMANDS_COUNT}"

echo ""
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   Installation Complete — All checks passed!                ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
else
    echo -e "${YELLOW}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║   Installation Complete — ${ERRORS} error(s) found               ║${NC}"
    echo -e "${YELLOW}╚═══════════════════════════════════════════════════════════════╝${NC}"
fi

echo ""
echo -e "${CYAN}Next Steps:${NC}"
echo "1. Configure your API keys (Anthropic, OpenAI, etc.)"
echo "2. Run: cd ${PROJECT_DIR}"
echo "3. Run: opencode"
echo "4. In OpenCode, use: /bmad-help"
echo ""
echo -e "${CYAN}Documentation:${NC}"
echo "- AGENTS.md: Project documentation"
echo "- _bmad-output/tools-registry.md: Tools inventory"
echo "- _bmad-output/project-replication-guide.md: Full replication guide"
echo ""

exit $ERRORS
