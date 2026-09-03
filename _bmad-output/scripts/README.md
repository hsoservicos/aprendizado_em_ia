# Installation Scripts

**Version**: 1.0.0  
**Last Updated**: 2026-09-03

---

## Overview

This directory contains automated installation scripts for setting up the BMAD Method development environment on different operating systems.

---

## Available Scripts

### Linux (Ubuntu/Debian)

**File**: `install-linux.sh`

**Usage**:
```bash
# Make executable
chmod +x install-linux.sh

# Run with default project directory (~/app)
./install-linux.sh

# Run with custom project directory
./install-linux.sh --project-dir /path/to/project

# Show help
./install-linux.sh --help
```

**Requirements**:
- Ubuntu 22.04+ or Debian 11+
- sudo privileges
- Internet connection

**What it installs**:
1. System build tools (build-essential, curl, wget, git)
2. Node.js v24 (via nvm)
3. Python 3.x
4. Git
5. uv (Python package manager)
6. ripgrep (fast search)
7. RTK (token compression)
8. OpenCode (IDE)
9. Claude Code (AI assistant)
10. BMAD Method v6.11.0
11. Project structure and configuration

---

### Windows (10/11)

**File**: `install-windows.ps1`

**Usage**:
```powershell
# Right-click → Run with PowerShell (as Administrator)
# Or run in PowerShell as Administrator:
powershell -ExecutionPolicy Bypass -File install-windows.ps1

# With custom project directory:
powershell -ExecutionPolicy Bypass -File install-windows.ps1 -ProjectDir "C:\projects\myapp"
```

**Requirements**:
- Windows 10 (21H2+) or Windows 11
- Administrator privileges
- Internet connection

**What it installs**:
1. Chocolatey (package manager)
2. Node.js LTS
3. Python
4. Git
5. uv (Python package manager)
6. ripgrep (fast search)
7. OpenCode (IDE)
8. Claude Code (AI assistant)
9. BMAD Method v6.11.0
10. Project structure and configuration

---

## Post-Installation

After running the installation script:

1. **Configure API Keys**:
   ```bash
   # Anthropic (for Claude Code)
   export ANTHROPIC_API_KEY="your-key-here"
   
   # Or set in config
   claude config set apiKey YOUR_API_KEY
   ```

2. **Start Development**:
   ```bash
   cd ~/app  # or your custom directory
   opencode
   ```

3. **Use BMAD Commands**:
   ```
   /bmad-help          — Get started
   /bmad-build         — Build features
   /bmad-code-review   — Review code
   ```

---

## Troubleshooting

### Common Issues

| Issue | Linux Solution | Windows Solution |
|-------|---------------|------------------|
| Permission denied | Use `sudo` | Run as Administrator |
| Command not found | Restart terminal or `source ~/.bashrc` | Restart PowerShell |
| Network error | Check proxy settings | Check firewall/proxy |
| Version conflict | Use nvm to manage Node.js versions | Reinstall via Chocolatey |

### Manual PATH Setup

**Linux** (`~/.bashrc`):
```bash
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/.npm-global/bin:$PATH"
```

**Windows** (PowerShell):
```powershell
# Add to system PATH via Environment Variables
# Or use:
[System.Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Users\$env:USERNAME\.local\bin", "User")
```

---

## Uninstallation

To remove the BMAD environment:

**Linux**:
```bash
# Remove project directory
rm -rf ~/app

# Remove BMAD globally (if installed)
npm uninstall -g bmad-method

# Remove tools
rm ~/.local/bin/rtk
rm ~/.local/bin/rg
```

**Windows**:
```powershell
# Remove project directory
Remove-Item -Recurse -Force "$env:USERPROFILE\app"

# Uninstall tools via Chocolatey
choco uninstall nodejs-lts python git ripgrep -y
```

---

## Support

For issues with installation:
1. Check the troubleshooting section above
2. Review `_bmad-output/project-replication-guide.md`
3. Consult BMAD Method documentation
4. Open an issue on the project repository
