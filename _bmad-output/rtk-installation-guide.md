# RTK (Rust Token Killer) — Installation & Configuration Report

**Author:** Hsantos  
**Date:** 2026-09-04  
**Version:** RTK 0.47.0  
**Platform:** Ubuntu 24.04.4 LTS (x86_64)

---

## 1. Executive Summary

RTK (Rust Token Killer) is a high-performance CLI proxy written in Rust that intercepts and compresses command outputs sent to AI coding assistants (Claude Code, Codex CLI, Cursor, Opencode, etc.). It reduces input token volume by **60-90%**, mitigating context window limits and accelerating agent response times.

**Status:** ✅ Installed, configured, and validated for **both** coding agents used in
this project:

| Agent | Integration | Location |
|-------|-------------|----------|
| **OpenCode** | Plugin (`tool.execute.before` hook) | `~/.config/opencode/plugins/rtk.ts` |
| **Claude Code** | `PreToolUse` hook (`rtk hook claude`) | `.claude/settings.json` (in-repo, committed) |

Both delegate to the same rewrite engine, so `git status` → `rtk git status`
transparently regardless of which agent is driving. One command wires both on a
fresh machine: `rtk init -g --auto-patch --opencode`.

---

## 2. System Requirements

| Component | Required | Installed |
|-----------|----------|-----------|
| OS | Linux, macOS, or Windows | Ubuntu 24.04.4 LTS |
| Architecture | x86_64, aarch64, arm64 | x86_64 |
| Rust toolchain | Optional (for cargo install) | Not installed |
| ripgrep (`rg`) | Recommended for fast search | v14.1.1 ✅ |
| curl | For script installation | Available ✅ |

---

## 3. Installation Steps Performed

### 3.1 RTK Binary — Pre-existing

RTK was already installed at:
```
/home/hsantos/.local/bin/rtk
```
Version: **0.47.0**

### 3.2 Ripgrep Dependency — Installed Locally

ripgrep was not present and `sudo` was unavailable. Installed manually without root:

```bash
curl -LO https://github.com/BurntSushi/ripgrep/releases/download/14.1.1/ripgrep-14.1.1-x86_64-unknown-linux-musl.tar.gz
tar xzf ripgrep-14.1.1-x86_64-unknown-linux-musl.tar.gz
mkdir -p ~/.local/bin
cp ripgrep-14.1.1-x86_64-unknown-linux-musl/rg ~/.local/bin/
rm -rf ripgrep-14.1.1-x86_64-unknown-linux-musl*
```

Result: `rg` v14.1.1 available at `~/.local/bin/rg`

### 3.3 OpenCode Plugin — Pre-existing

Plugin file located at:
```
/home/hsantos/.config/opencode/plugins/rtk.ts
```

The plugin hooks into `tool.execute.before` events and rewrites Bash commands via `rtk rewrite`.

### 3.4 Claude Code Hook — Added 2026-09-04

To give Claude Code the same transparent compression OpenCode already had, a
`PreToolUse` hook was added to the **in-repo** settings file
`/home/hsantos/app/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "rtk hook claude" }
        ]
      }
    ]
  }
}
```

`rtk hook claude` reads the Claude Code PreToolUse JSON on stdin and returns an
`updatedInput.command` with the RTK-rewritten command. It is **idempotent** — a
command that is already `rtk …` is returned unchanged — so this project hook and
an optional global hook (`rtk init -g`) can coexist without double-wrapping.

The same file also carries a `permissions.allow` list so `uv`, `rtk`, `rg`, `gh`,
`crewai` and `npx bmad-method` run without prompting. A companion reference,
`.claude/RTK.md`, documents the meta commands (`rtk gain`, `rtk discover`, …).

**One-shot wiring for both agents** (per machine, global):

```bash
rtk init -g --auto-patch --opencode   # global Claude hook + OpenCode plugin
rtk init --show                        # verify
```

---

## 4. Validation & Testing

### 4.1 Version Check
```bash
$ rtk --version
rtk 0.47.0
```
✅ **PASS**

### 4.2 Rewrite Engine
```bash
$ rtk rewrite "git status"
rtk git status

$ rtk rewrite "pytest"
rtk pytest

$ rtk rewrite "ls -la"
rtk ls -la
```
✅ **PASS** — All commands correctly rewritten.

### 4.3 Git Commands
```bash
$ rtk git status
* master
clean — nothing to commit

$ rtk git log -n 5
3c26a19 initial commit (3 seconds ago) <Hsantos>

$ rtk git diff
(no output — clean tree)
```
✅ **PASS** — Condensed output, stripped noise.

### 4.4 File System Commands
```bash
$ rtk ls
_bmad/
_bmad-output/
AGENTS.md  2.6K

$ rtk find "*.toml"
_bmad/config.toml
_bmad/config.user.toml
_bmad/custom/config.toml
```
✅ **PASS** — Compact directory listings.

### 4.5 File Reading
```bash
$ rtk read AGENTS.md
# AGENTS.md
BMAD Method project — Agile AI-Driven Development workflow...

$ rtk read AGENTS.md -l aggressive
# AGENTS.md
BMAD Method project — Agile AI-Driven Development workflow...
```
✅ **PASS** — Both normal and aggressive modes functional.

### 4.6 Smart Summary
```bash
$ rtk smart AGENTS.md
Data code (71 lines)
General purpose code file
```
✅ **PASS**

### 4.7 Environment Variable Bypass
```bash
$ RTK_DISABLED=1 git status
On branch master
nothing to commit, working tree clean
```
✅ **PASS** — Raw output returned when disabled.

### 4.8 Trust System
```bash
$ rtk trust
rtk: No custom filters found (.rtk/filters.toml or ~/.config/rtk/filters.toml)
```
✅ **PASS** — Correctly reports no custom filters.

### 4.9 Token Savings Dashboard
```bash
$ rtk gain
Total commands:    15
Tokens saved:      200 (11.9%)
```
✅ **PASS** — Telemetry tracking active.

---

## 5. Architecture: How RTK Integrates with the Coding Agents

### 5.0 Claude Code flow

```
Claude Code ──(Bash tool call)──▶ PreToolUse hook ──▶ rtk hook claude
     ▲                                                      │
     │                                             updatedInput.command
     │                                                      ▼
 Filtered output ◀── RTK Core (Rust) ◀── native command (git, pytest, …)
```

1. Claude Code emits a `PreToolUse` event for every `Bash` call.
2. `.claude/settings.json` routes it to `rtk hook claude` (stdin JSON).
3. RTK returns `{"hookSpecificOutput":{"updatedInput":{"command":"rtk …"}}}`.
4. Claude Code runs the rewritten command; RTK Core filters the output.
5. On failure the raw output is tee-logged to `~/.local/share/rtk/tee/`.

### 5.1 OpenCode flow

```
+------------------+     (Bash command)      +-------------------+
|     Opencode     | ----------------------> |   RTK Plugin      |
|   (AI Agent)     |                         |   (rtk.ts)        |
+------------------+                         +-------------------+
          ^                                            |
          |                                   rtk rewrite <cmd>
          |                                            v
   Filtered Output    +-------------------+   +-------------------+
   (-60% to -90%) <--- |  RTK Core (Rust) | < | Native Command    |
                       +-------------------+   | (git, pytest, etc)|
                                ^              +-------------------+
                                |                       |
                        [Tee Log on Failure]       Real Execution
                       (~/.local/share/rtk)
```

**Flow:**
1. Agent (Opencode) executes a Bash command
2. RTK plugin intercepts via `tool.execute.before` hook
3. `rtk rewrite` transforms the command (e.g., `git status` → `rtk git status`)
4. RTK Core applies deterministic filters (grouping, truncation, deduplication)
5. Filtered output is returned to the agent
6. On failure, raw output is saved to `~/.local/share/rtk/tee/` for audit

---

## 6. Key Commands Reference

| Command | Description | Token Savings |
|---------|-------------|---------------|
| `rtk ls [dir]` | Compact directory tree | ~70-85% |
| `rtk read <file>` | Smart file reading | ~50-80% |
| `rtk read <file> -l aggressive` | Function signatures only | ~85-95% |
| `rtk smart <file>` | 2-line code summary | ~90% |
| `rtk find "<pattern>"` | Concise file search | ~75% |
| `rtk grep "<pattern>"` | Grouped search results | ~70-90% |
| `rtk git status` | Condensed git status | ~60% |
| `rtk git log -n <N>` | Compact commit log | ~70% |
| `rtk git diff` | Focused diff output | ~80-85% |
| `rtk pytest` / `rtk jest` | Test output (failures only) | ~85-95% |
| `rtk tsc` / `rtk lint` | Grouped errors | ~70-80% |
| `rtk gain` | Token savings dashboard | — |

---

## 7. Configuration Files

### 7.1 Global Config
```
~/.config/rtk/config.toml
```

### 7.2 Project-level Filters
```
<project-root>/.rtk/filters.toml
```

### 7.3 OpenCode Plugin
```
~/.config/opencode/plugins/rtk.ts
```

### 7.4 Claude Code Hook + Reference (in-repo)
```
<project-root>/.claude/settings.json   # hooks.PreToolUse[matcher=Bash] → rtk hook claude
<project-root>/.claude/RTK.md          # RTK command reference for the agent
~/.claude/settings.json                # optional global hook via `rtk init -g`
```

### 7.5 Environment Variables

| Variable | Purpose |
|----------|---------|
| `RTK_DISABLED=1` | Bypass RTK for a single command |
| `RTK_TELEMETRY_DISABLED=1` | Disable anonymous telemetry |
| `RTK_HOOK_AUDIT=1` | Enable hook debug logging |

---

## 8. Troubleshooting

| Issue | Solution |
|-------|----------|
| `Binary 'rg' not found` | Install ripgrep: download from GitHub releases to `~/.local/bin/` |
| Agent not using RTK | Run `rtk init -g --opencode` and restart the agent |
| Need raw output | Prefix with `RTK_DISABLED=1` |
| Custom filter not loading | Run `rtk trust` to authorize project filters |
| Plugin not loading (OpenCode) | Verify `~/.config/opencode/plugins/rtk.ts` exists and `rtk` is in PATH |
| Hook not firing (Claude Code) | Check `.claude/settings.json` has the `PreToolUse`/`Bash` hook; restart Claude Code; `rtk init --show` |
| Both agents at once | `rtk init -g --auto-patch --opencode` |
| Verify rewrite | `echo '{"tool_name":"Bash","tool_input":{"command":"git status"}}' \| rtk hook claude` |

---

## 9. Conclusion

RTK is fully operational in this environment for **both** coding agents. OpenCode
uses the plugin system (`tool.execute.before`); Claude Code uses a `PreToolUse`
hook committed to the repo in `.claude/settings.json`. Both provide automatic
command rewriting with immediate token savings and no manual intervention. The
dashboard (`rtk gain`) confirms ongoing telemetry tracking and savings metrics.

**Next Steps:**
- Monitor `rtk gain` over time to quantify savings in production workflows
- Create `.rtk/filters.toml` for project-specific custom filters as needed
- Consider adding RTK configuration to CI/CD pipelines for consistent developer experience
