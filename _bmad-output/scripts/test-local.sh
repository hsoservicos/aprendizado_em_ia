#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# BMAD Method — Local Installation Test Script
# ═══════════════════════════════════════════════════════════════════
# Purpose: Validate install-linux.sh without Docker
# ═══════════════════════════════════════════════════════════════════

set -euo pipefail

# ─── Colors ────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ─── Counters ──────────────────────────────────────────────────────
TOTAL=0
PASSED=0
FAILED=0
WARNINGS=0

# ─── Test Functions ────────────────────────────────────────────────
test_pass() {
    ((TOTAL++))
    ((PASSED++))
    echo -e "${GREEN}[PASS]${NC} $1"
}

test_fail() {
    ((TOTAL++))
    ((FAILED++))
    echo -e "${RED}[FAIL]${NC} $1"
}

test_warn() {
    ((TOTAL++))
    ((WARNINGS++))
    echo -e "${YELLOW}[WARN]${NC} $1"
}

check_command() {
    local cmd=$1
    local name=${2:-$1}
    if command -v "$cmd" >/dev/null 2>&1; then
        test_pass "$name found: $(command -v $cmd)"
        return 0
    else
        test_fail "$name not found"
        return 1
    fi
}

check_version() {
    local cmd=$1
    local name=$2
    local min_version=$3
    
    if ! command -v "$cmd" >/dev/null 2>&1; then
        test_fail "$name not installed"
        return 1
    fi
    
    local version
    version=$("$cmd" --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1)
    
    if [ -z "$version" ]; then
        test_warn "$name version could not be determined"
        return 0
    fi
    
    # Compare versions
    if printf '%s\n%s' "$min_version" "$version" | sort -V | head -1 | grep -q "$min_version"; then
        test_pass "$name version $version (>= $min_version)"
    else
        test_fail "$name version $version (< $min_version required)"
    fi
}

check_directory() {
    local dir=$1
    local name=${2:-$1}
    if [ -d "$dir" ]; then
        test_pass "Directory exists: $name"
        return 0
    else
        test_fail "Directory not found: $name"
        return 1
    fi
}

check_file() {
    local file=$1
    local name=${2:-$1}
    if [ -f "$file" ]; then
        test_pass "File exists: $name"
        return 0
    else
        test_fail "File not found: $name"
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════
# TEST SUITE
# ═══════════════════════════════════════════════════════════════════

echo -e "\n${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   BMAD Method — Local Installation Validation              ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}\n"

# ─── Test 1: System Information ────────────────────────────────────
echo -e "\n${CYAN}═══ Test 1: System Information ═══${NC}"
echo "OS: $(cat /etc/os-release 2>/dev/null | grep PRETTY_NAME | cut -d'"' -f2 || echo 'Unknown')"
echo "Kernel: $(uname -r)"
echo "Architecture: $(uname -m)"
echo "User: $(whoami)"
echo "Home: $HOME"

# ─── Test 2: Node.js ──────────────────────────────────────────────
echo -e "\n${CYAN}═══ Test 2: Node.js ═══${NC}"
check_command "node" "Node.js"
check_version "node" "Node.js" "20.12"
check_command "npm" "npm"

# ─── Test 3: Python ───────────────────────────────────────────────
echo -e "\n${CYAN}═══ Test 3: Python ═══${NC}"
check_command "python3" "Python3"
check_version "python3" "Python3" "3.10"

# ─── Test 4: Git ──────────────────────────────────────────────────
echo -e "\n${CYAN}═══ Test 4: Git ═══${NC}"
check_command "git" "Git"
if command -v git >/dev/null 2>&1; then
    echo "  Version: $(git --version)"
fi

# ─── Test 5: uv (Python Package Manager) ─────────────────────────
echo -e "\n${CYAN}═══ Test 5: uv ═══${NC}"
check_command "uv" "uv"
if command -v uv >/dev/null 2>&1; then
    echo "  Version: $(uv --version)"
fi

# ─── Test 6: ripgrep ─────────────────────────────────────────────
echo -e "\n${CYAN}═══ Test 6: ripgrep ═══${NC}"
check_command "rg" "ripgrep"
if command -v rg >/dev/null 2>&1; then
    echo "  Version: $(rg --version | head -1)"
fi

# ─── Test 7: RTK (Optional) ──────────────────────────────────────
echo -e "\n${CYAN}═══ Test 7: RTK (Optional) ═══${NC}"
if check_command "rtk" "RTK"; then
    echo "  Version: $(rtk --version 2>/dev/null || echo 'unknown')"
else
    test_warn "RTK is optional - can be installed later"
fi

# ─── Test 8: BMAD Method ─────────────────────────────────────────
echo -e "\n${CYAN}═══ Test 8: BMAD Method ═══${NC}"
check_directory "$HOME/app/_bmad" "BMAD Framework (_bmad)"
check_directory "$HOME/app/.agents" "Agents Directory (.agents)"
check_directory "$HOME/app/.claude" "Claude Skills Directory (.claude)"
check_directory "$HOME/app/.opencode" "OpenCode Directory (.opencode)"
check_file "$HOME/app/AGENTS.md" "AGENTS.md"

# ─── Test 9: Skills Count ────────────────────────────────────────
echo -e "\n${CYAN}═══ Test 9: Skills Count ═══${NC}"
if [ -d "$HOME/app/.agents/skills" ]; then
    SKILLS_COUNT=$(ls -d $HOME/app/.agents/skills/bmad-* 2>/dev/null | wc -l)
    if [ "$SKILLS_COUNT" -ge 50 ]; then
        test_pass "Skills installed: $SKILLS_COUNT (expected: 57)"
    elif [ "$SKILLS_COUNT" -gt 0 ]; then
        test_warn "Skills installed: $SKILLS_COUNT (expected: 57)"
    else
        test_fail "No BMAD skills found"
    fi
else
    test_fail "Skills directory not found"
fi

# ─── Test 10: OpenCode Commands ──────────────────────────────────
echo -e "\n${CYAN}═══ Test 10: OpenCode Commands ═══${NC}"
if [ -d "$HOME/app/.opencode/commands" ]; then
    COMMANDS_COUNT=$(ls $HOME/app/.opencode/commands/bmad-*.md 2>/dev/null | wc -l)
    if [ "$COMMANDS_COUNT" -ge 50 ]; then
        test_pass "Commands installed: $COMMANDS_COUNT (expected: 57)"
    elif [ "$COMMANDS_COUNT" -gt 0 ]; then
        test_warn "Commands installed: $COMMANDS_COUNT (expected: 57)"
    else
        test_fail "No BMAD commands found"
    fi
else
    test_fail "Commands directory not found"
fi

# ─── Test 11: Project Structure ──────────────────────────────────
echo -e "\n${CYAN}═══ Test 11: Project Structure ═══${NC}"
check_directory "$HOME/app/docs" "docs directory"
check_directory "$HOME/app/_bmad-output" "_bmad-output directory"
check_file "$HOME/app/.gitignore" ".gitignore"
check_file "$HOME/app/README.md" "README.md"

# ─── Test 12: Git Configuration ──────────────────────────────────
echo -e "\n${CYAN}═══ Test 12: Git Configuration ═══${NC}"
if [ -d "$HOME/app/.git" ]; then
    test_pass "Git repository initialized"
    cd "$HOME/app"
    BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
    if [ "$BRANCH" = "main" ]; then
        test_pass "Default branch: main"
    else
        test_warn "Default branch: $BRANCH (expected: main)"
    fi
else
    test_fail "Git repository not initialized"
fi

# ─── Test 13: BMAD Scripts ───────────────────────────────────────
echo -e "\n${CYAN}═══ Test 13: BMAD Scripts ═══${NC}"
check_file "$HOME/app/_bmad/scripts/render_skill.py" "render_skill.py"

# ─── Test 14: PATH Configuration ─────────────────────────────────
echo -e "\n${CYAN}═══ Test 14: PATH Configuration ═══${NC}"
if echo "$PATH" | grep -q ".local/bin"; then
    test_pass ".local/bin in PATH"
else
    test_warn ".local/bin not in PATH (may need shell restart)"
fi

# ─── Test 15: Network Connectivity ───────────────────────────────
echo -e "\n${CYAN}═══ Test 15: Network Connectivity ═══${NC}"
if curl -s --max-time 5 https://api.github.com >/dev/null 2>&1; then
    test_pass "GitHub API reachable"
else
    test_warn "GitHub API not reachable (may affect some features)"
fi

# ═══════════════════════════════════════════════════════════════════
# TEST SUMMARY
# ═══════════════════════════════════════════════════════════════════

echo -e "\n${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                    TEST SUMMARY                             ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Total Tests:  ${TOTAL}"
echo -e "${GREEN}Passed:       ${PASSED}${NC}"
echo -e "${RED}Failed:       ${FAILED}${NC}"
echo -e "${YELLOW}Warnings:     ${WARNINGS}${NC}"
echo ""

# Calculate pass rate
if [ $TOTAL -gt 0 ]; then
    PASS_RATE=$(( (PASSED * 100) / TOTAL ))
    echo -e "Pass Rate:    ${PASS_RATE}%"
fi

echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   ALL TESTS PASSED — Installation Validated Successfully!   ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    exit 0
else
    echo -e "${RED}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║   SOME TESTS FAILED — Review issues above                  ║${NC}"
    echo -e "${RED}╚═══════════════════════════════════════════════════════════════╝${NC}"
    exit 1
fi
