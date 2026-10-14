# CLAUDE.md

Claude Code's entry point for this repository. It is the Claude Code counterpart
of `AGENTS.md` (which OpenCode reads). **Both coding agents are first-class here**
and share one source of truth, the same 55 skills (54 BMAD + 1 Impeccable), and
the same tooling.

@AGENTS.md

---

## Coding agent parity

| Concern | OpenCode | Claude Code |
|---------|----------|-------------|
| Instructions | `AGENTS.md` | `CLAUDE.md` → imports `AGENTS.md` |
| BMAD skills | `.agents/skills/` (55) via `.opencode/commands/*.md` | `.claude/skills/` (55), auto-discovered |
| Slash commands | `/bmad-*`, `/impeccable` (command files) | `/bmad-*`, `/impeccable` (native skill discovery) |
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
- **Impeccable** (design skill + UI anti-pattern detector): skill at
  `.claude/skills/impeccable/`, four helper subagents in `.claude/agents/
  impeccable-*.md`, and hooks in `.claude/settings.local.json`
  (`SessionStart` / `PostToolUse` on Edit|Write / `Stop`) running
  `.claude/skills/impeccable/scripts/impeccable hook`. Invoke as
  `/impeccable <cmd>` (`init`, `document`, `critique`, `audit`, `harden`,
  `polish`, …) or scan from the shell with `npx impeccable detect <dir|url>`.
  Full usage, greenfield/brownfield recipes and the post-BMAD-update restore
  steps live in `@AGENTS.md` → *Impeccable* section. `settings.local.json` is
  gitignored — re-run `npx impeccable install -y --providers=claude,opencode
  --scope=project` on a new machine to get the hooks.
- **Superpowers** (SDLC methodology + 15 skills): user plugin
  `superpowers@claude-plugins-official` (cache
  `~/.claude/plugins/cache/claude-plugins-official/superpowers/6.4.1/`).
  Its `SessionStart` hook injects `skills/using-superpowers/SKILL.md` in
  `<EXTREMELY_IMPORTANT>` (matcher `startup|clear|compact`) — that bootstrap is
  what makes `brainstorming`, `test-driven-development`, `systematic-debugging`,
  etc. auto-trigger. **Precedence with BMAD is binding**: `@AGENTS.md` →
  *Precedence — BMAD × Superpowers × Impeccable*. Short version — BMAD owns the
  SDLC phase; Superpowers owns TDD, root-cause debugging, worktrees, branch
  finish and the verification gate; Impeccable owns design. Never run
  `subagent-driven-development` and `bmad-build-auto` in the same session.
  Telemetry is disabled via `env.SUPERPOWERS_DISABLE_TELEMETRY=1` in
  `.claude/settings.json`. Update with `claude plugin update superpowers`.
- **Per-machine setup** for both agents at once:
  `rtk init -g --auto-patch --opencode`.

## Attribution

End commit messages with:

```
Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
```
