# CLAUDE.md

Claude Code's entry point for this repository. It is the Claude Code counterpart
of `AGENTS.md` (which OpenCode reads). **Both coding agents are first-class here**
and share one source of truth, the same 57 BMAD skills, and the same tooling.

@AGENTS.md

---

## Coding agent parity

| Concern | OpenCode | Claude Code |
|---------|----------|-------------|
| Instructions | `AGENTS.md` | `CLAUDE.md` → imports `AGENTS.md` |
| BMAD skills | `.agents/skills/` (57) via `.opencode/commands/*.md` | `.claude/skills/` (57), auto-discovered |
| Slash commands | `/bmad-*` (command files) | `/bmad-*` (native skill discovery) |
| Tool allow-list | inherits shell | `.claude/settings.json` → `permissions.allow` |
| RTK token compression | `~/.config/opencode/plugins/rtk.ts` | `.claude/settings.json` → `PreToolUse` hook (`rtk hook claude`) |
| RTK reference | — | `.claude/RTK.md` |

The `.agents/skills/` and `.claude/skills/` trees are kept byte-identical — a
change to one must be mirrored to the other (BMAD's installer does this on
`npx bmad-method install`).

## Claude Code specifics

- **Skills**: invoke with `/bmad-help`, `/bmad-build`, `/bmad-code-review`, the
  technology agents (`/bmad-agent-docker`, `/bmad-agent-python314`,
  `/bmad-agent-php84`, `/bmad-agent-postgres18`), etc. — or let the model pick.
- **Skill rendering** (never run workflow files directly):
  ```bash
  uv run _bmad/scripts/render_skill.py --project-root /home/hsantos/app --skill .claude/skills/<skill-name>
  ```
  On failure (including a missing `uv`), report the output and HALT.
- **Tooling**: `uv`, `rtk`, `rg`, `gh`, `crewai`, `npx bmad-method` are
  pre-approved in `.claude/settings.json`. All live under `~/.local/bin`
  (except `node`/`npm` via nvm) and must be on `PATH`.
- **RTK**: Bash output is auto-compressed by the `PreToolUse` hook. See
  `@.claude/RTK.md`. For a raw command: `RTK_DISABLED=1 <cmd>`.
- **Per-machine setup** for both agents at once:
  `rtk init -g --auto-patch --opencode`.

## Attribution

End commit messages with:

```
Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
```
