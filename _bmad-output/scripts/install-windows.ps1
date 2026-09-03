# ═══════════════════════════════════════════════════════════════════
# BMAD Method — Automated Installation Script for Windows 10/11
# ═══════════════════════════════════════════════════════════════════
# Version: 1.0.0
# Author: Hsantos
# Date: 2026-09-03
# Usage: Right-click → Run with PowerShell (as Administrator)
#        Or: powershell -ExecutionPolicy Bypass -File install-windows.ps1
# ═══════════════════════════════════════════════════════════════════

#Requires -RunAsAdministrator

param(
    [string]$ProjectDir = "$env:USERPROFILE\app"
)

# ─── Configuration ─────────────────────────────────────────────────
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

$NodeVersion = "24"
$UVVersion = "0.12.9"
$BMADVersion = "6.11.0"

# ─── Colors ────────────────────────────────────────────────────────
function Write-Step    { param([string]$Msg) Write-Host "`n═══ $Msg ═══" -ForegroundColor Cyan }
function Write-Info    { param([string]$Msg) Write-Host "[INFO] $Msg" -ForegroundColor Blue }
function Write-OK      { param([string]$Msg) Write-Host "[OK] $Msg" -ForegroundColor Green }
function Write-Warn    { param([string]$Msg) Write-Host "[WARN] $Msg" -ForegroundColor Yellow }
function Write-Error   { param([string]$Msg) Write-Host "[ERROR] $Msg" -ForegroundColor Red }
function Write-Summary { param([string]$Msg) Write-Host "[SUMMARY] $Msg" -ForegroundColor Magenta }

# ─── Check Commands ────────────────────────────────────────────────
function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

# ─── Main ──────────────────────────────────────────────────────────
Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   BMAD Method — Automated Installation for Windows 10/11    ║" -ForegroundColor Cyan
Write-Host "║   Version: $BMADVersion                                          ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ─── Phase 1: Chocolatey ──────────────────────────────────────────
Write-Step "Phase 1: Chocolatey Package Manager"

if (Test-Command choco) {
    Write-Info "Chocolatey already installed: $(choco --version)"
} else {
    Write-Info "Installing Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    
    # Refresh environment
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
}

Write-OK "Chocolatey: $(choco --version)"

# ─── Phase 2: Node.js ─────────────────────────────────────────────
Write-Step "Phase 2: Node.js (v$NodeVersion)"

if (Test-Command node) {
    $currentNode = (node --version) -replace 'v', '' -split '\.' | Select-Object -First 1
    Write-Info "Node.js already installed: v$currentNode"
    
    if ([int]$currentNode -lt [int]$NodeVersion) {
        Write-Warn "Node.js version too old. Upgrading..."
        choco upgrade nodejs-lts -y
    }
} else {
    Write-Info "Installing Node.js..."
    choco install nodejs-lts -y
}

# Refresh environment
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")

Write-OK "Node.js: $(node --version)"
Write-OK "npm: $(npm --version)"

# ─── Phase 3: Python ──────────────────────────────────────────────
Write-Step "Phase 3: Python"

if (Test-Command python) {
    Write-Info "Python already installed: $(python --version)"
} else {
    Write-Info "Installing Python..."
    choco install python -y
}

# Refresh environment
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")

Write-OK "Python: $(python --version)"

# ─── Phase 4: Git ──────────────────────────────────────────────────
Write-Step "Phase 4: Git"

if (Test-Command git) {
    Write-Info "Git already installed: $(git --version)"
} else {
    Write-Info "Installing Git..."
    choco install git -y
}

# Refresh environment
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")

Write-OK "Git: $(git --version)"

# ─── Phase 5: uv ──────────────────────────────────────────────────
Write-Step "Phase 5: uv"

if (Test-Command uv) {
    Write-Info "uv already installed: $(uv --version)"
} else {
    Write-Info "Installing uv..."
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
}

# Refresh environment
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")

Write-OK "uv: $(uv --version)"

# ─── Phase 6: ripgrep ─────────────────────────────────────────────
Write-Step "Phase 6: ripgrep"

if (Test-Command rg) {
    Write-Info "ripgrep already installed: $(rg --version | Select-Object -First 1)"
} else {
    Write-Info "Installing ripgrep..."
    choco install ripgrep -y
}

# Refresh environment
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")

Write-OK "ripgrep: $(rg --version | Select-Object -First 1)"

# ─── Phase 7: IDE Setup ───────────────────────────────────────────
Write-Step "Phase 7: IDE Setup"

# OpenCode
if (Test-Command opencode) {
    Write-Info "OpenCode already installed"
} else {
    Write-Info "Installing OpenCode..."
    npm install -g opencode 2>$null
    if (-not (Test-Command opencode)) {
        Write-Warn "OpenCode install failed (optional)"
    }
}

# Claude Code
if (Test-Command claude) {
    Write-Info "Claude Code already installed"
} else {
    Write-Info "Installing Claude Code..."
    npm install -g @anthropic-ai/claude-code 2>$null
    if (-not (Test-Command claude)) {
        Write-Warn "Claude Code install failed (optional)"
    }
}

# ─── Phase 8: Project Directory ───────────────────────────────────
Write-Step "Phase 8: Project Directory"

Write-Info "Setting up project at: $ProjectDir"

if (Test-Path $ProjectDir) {
    Write-Info "Project directory already exists"
} else {
    New-Item -ItemType Directory -Path $ProjectDir -Force | Out-Null
    Write-OK "Created project directory"
}

Set-Location $ProjectDir

# Initialize git if needed
if (-not (Test-Path ".git")) {
    Write-Info "Initializing git repository..."
    git init
    git branch -M main
}

# ─── Phase 9: BMAD Method Installation ───────────────────────────
Write-Step "Phase 9: BMAD Method v$BMADVersion"

if (Test-Path "_bmad") {
    Write-Info "BMAD already installed"
} else {
    Write-Info "Installing BMAD Method..."
    npx "bmad-method@$BMADVersion" install
}

# ─── Phase 10: Project Structure ──────────────────────────────────
Write-Step "Phase 10: Project Structure"

# Create required directories
New-Item -ItemType Directory -Path "docs" -Force | Out-Null
New-Item -ItemType Directory -Path "_bmad-output" -Force | Out-Null

# Create .gitignore if not exists
if (-not (Test-Path ".gitignore")) {
    @"
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
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
    Write-OK "Created .gitignore"
}

# ─── Phase 11: Validation ─────────────────────────────────────────
Write-Step "Phase 11: Validation"

Write-Host ""
Write-Summary "Installation Summary"
Write-Host ""

$Errors = 0

# Check Node.js
if (Test-Command node) {
    Write-OK "Node.js: $(node --version)"
} else {
    Write-Error "Node.js not found"
    $Errors++
}

# Check npm
if (Test-Command npm) {
    Write-OK "npm: $(npm --version)"
} else {
    Write-Error "npm not found"
    $Errors++
}

# Check Python
if (Test-Command python) {
    Write-OK "Python: $(python --version)"
} else {
    Write-Error "Python not found"
    $Errors++
}

# Check uv
if (Test-Command uv) {
    Write-OK "uv: $(uv --version)"
} else {
    Write-Error "uv not found"
    $Errors++
}

# Check Git
if (Test-Command git) {
    Write-OK "Git: $(git --version)"
} else {
    Write-Error "Git not found"
    $Errors++
}

# Check ripgrep
if (Test-Command rg) {
    Write-OK "ripgrep: $(rg --version | Select-Object -First 1)"
} else {
    Write-Warn "ripgrep: Not installed (recommended)"
}

# Check BMAD
if (Test-Path "_bmad") {
    Write-OK "BMAD Method: Installed"
} else {
    Write-Error "BMAD Method: Not installed"
    $Errors++
}

# Count skills
$SkillsCount = (Get-ChildItem -Path ".agents\skills\bmad-*" -Directory -ErrorAction SilentlyContinue).Count
$CommandsCount = (Get-ChildItem -Path ".opencode\commands\bmad-*.md" -File -ErrorAction SilentlyContinue).Count

Write-Host ""
Write-Summary "Skills Installed"
Write-Host "Skills: $SkillsCount"
Write-Host "Commands: $CommandsCount"

Write-Host ""
if ($Errors -eq 0) {
    Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║   Installation Complete — All checks passed!                ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
} else {
    Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
    Write-Host "║   Installation Complete — $Errors error(s) found               ║" -ForegroundColor Yellow
    Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Configure your API keys (Anthropic, OpenAI, etc.)"
Write-Host "2. Open a new terminal and run: cd $ProjectDir"
Write-Host "3. Run: opencode"
Write-Host "4. In OpenCode, use: /bmad-help"
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Cyan
Write-Host "- AGENTS.md: Project documentation"
Write-Host "- _bmad-output\tools-registry.md: Tools inventory"
Write-Host "- _bmad-output\project-replication-guide.md: Full replication guide"
Write-Host ""

exit $Errors
