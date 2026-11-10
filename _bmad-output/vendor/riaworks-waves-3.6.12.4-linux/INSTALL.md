# Installing riaworks-waves 3.6.12.4 from this bundle

This bundle carries everything the module is, as files: the orchestrator wheel, the
skills, and the module tree the BMAD installer reads. No git remote, no package index,
no account, no token.

```text
riaworks-waves-3.6.12.4-bundle/
├── install.sh          Linux, macOS, WSL
├── install.ps1         native Windows (experimental tier — see below)
├── INSTALL.md          this file
├── SHA256SUMS          checksums for the wheel and the two installers
├── wheels/             the orchestrator wheel (the skills are inside it)
└── riaworks-waves-3.6.12.4/          the module tree, for `npx bmad-method install --custom-source`
```

## Before you start

Install the **BMAD Method** first — this module drives it, and does not replace it:

```bash
npx bmad-method install          # select the BMad Method (bmm) module
```

waves requires **BMAD-METHOD 6.12.4 or newer** and the `bmad-build-auto` skill that the
bmm module installs. Wiring up the project (`waves init`) checks the version first and
installs nothing into a project below 6.12.4 — upgrade it with
`npx bmad-method@latest install` and run the installer again. The preflight at the end
of the install checks both and tells you what is missing.

**That is the only thing you install by hand.** The installer brings the rest itself:

| What                             | Where it comes from                                     |
| -------------------------------- | ------------------------------------------------------- |
| [uv](https://docs.astral.sh/uv/) | the publisher's own installer, into your home directory |
| Python 3.11+                     | uv downloads a managed one when your system has none    |
| git                              | your system's package manager / winget                  |
| tmux (Linux, macOS, WSL)         | your system's package manager                           |
| psmux + pwsh (native Windows)    | the psmux GitHub release / winget                       |

Anything it cannot install without privilege is reported with the exact command to run,
and the install carries on rather than stopping. `--no-bootstrap` (`-NoBootstrap`) turns
the whole thing off if you would rather manage prerequisites yourself.

## Install

Linux, macOS, WSL — from inside the project you want to wire up:

```bash
sh /path/to/riaworks-waves-3.6.12.4-bundle/install.sh
```

Native Windows (PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Project C:\code\my-project
```

**It asks which project before it installs anything.** The current directory is the
default — press Enter to accept it — and the prompt says whether it found a `_bmad/`
there. Two directories it refuses outright, however you point it at them: **its own bundle
folder** (the slip of extracting the zip and running it in place — the skills would land
next to the installer and your project would get nothing) and **your home directory**,
where `.claude/` is not a project's but the coding CLI's _global_ configuration: installing
there would register the hook relay for every project you ever open. And where the current
directory is neither a BMAD project nor a git repository, there is **no Enter default** at
all — you type a path or nothing happens. With no terminal to ask on it stops and asks for
`--project` instead of guessing. Passing `--project` / `-Project` yourself is an answer, so it does
not ask.

That is both levels at once:

| Level   | What lands                                                                       | Scope            |
| ------- | -------------------------------------------------------------------------------- | ---------------- |
| Machine | the `waves` command and the `waves tui` dashboard, in uv's managed tool env      | once per machine |
| Project | the `waves-*` skills, the coding-CLI hooks, `.waves/loop/policy.toml`, gitignore | once per project |

Useful flags (`--help` lists them all):

| Flag                       | Why                                                              |
| -------------------------- | ---------------------------------------------------------------- |
| `--project <dir>`          | wire up a project other than the current directory               |
| `--cli codex` (repeatable) | register hooks for another coding CLI (default: `claude`)        |
| `--tool-only`              | machine level only — the first of several projects comes later   |
| `--project-only`           | second and later projects on a machine that already has the tool |
| `--via-bmad`               | also register the module so `/bmad-help` lists it (needs `npx`)  |
| `--no-tui`                 | skip the dashboard's dependencies                                |
| `--force`                  | refresh skill copies you have edited locally                     |

On Windows the same flags are PowerShell parameters: `-Project`, `-Cli`, `-ToolOnly`,
`-ProjectOnly`, `-ViaBmad`, `-NoTui`, `-Force`, `-NoBootstrap`.

## Upgrading

Take the newer bundle and run the same command again. The installer replaces the tool
from the new wheel, notices the project already has skills, and refreshes them against
the new version. Your `.waves/loop/policy.toml` and your runs are left untouched.

There is no `uv tool upgrade` path for a bundle install: a wheel is a fixed version, so a
new version means a new bundle. `waves --version` tells you which one you are on.

## Offline installs

The bundle carries the whole of waves, but its dependencies (`pyyaml`, `regex`, and for
the dashboard `textual`, `rich`, `tomlkit`, `pyte`) come from PyPI on first install. For a
machine with no network, download those wheels **on a machine of the same OS and Python
version** and hand the directory to the installer:

```bash
pip download "riaworks-waves[tui]" -d wheels/deps     # on a connected machine, same platform
sh install.sh --find-links wheels/deps                 # on the offline machine
```

`--find-links` implies `--offline`, so nothing reaches for the network.

## Windows: WSL is the supported path

Native Windows is the module's **experimental** tier. Runs there are driven by the
`psmux` backend — the installer fetches psmux from its own GitHub release (the same
source this project's CI uses) and pwsh through winget, and puts psmux on your user
`PATH` — but window hosting and attach/detach are still incomplete.

**WSL is not a workaround — it is Linux**, it uses tmux, and everything in the supported
tier works there unchanged. Inside a WSL shell, install with `install.sh` and the
distribution's own Python. One trap worth knowing: WSL appends the Windows `PATH` to its
own, so a Windows-installed `waves` is reachable from the bash prompt and silently
behaves as Windows. `waves mux` should read `platform default for linux`; if it names
`win32`, you are running the Windows build from a Linux shell.

## Living next to other tools

waves keeps its whole footprint under its own names — the `waves` command, `.waves/`,
`_waves/`, `WAVES_*`, the `waves-*` skills, `_bmad/waves/` — so it never collides with another
orchestrator's state, and `waves init` only ever appends its own hook relay to a coding
CLI's config, leaving every other registration in place. What it writes under `_bmad/` is
deliberately almost nothing: its own `_bmad/waves/module-help.csv`, and — only on a
project that has the Test Architect module — the managed test-location facts in
`_bmad/custom/bmad-testarch-*.toml`, through the per-skill override channel the BMAD
Method itself designed. A file there that you have taken ownership of is reported, never
overwritten. The `waves-*` skills' own overrides are not BMAD's and live in `_waves/custom/`
(`<skill>.toml` versioned, `<skill>.user.toml` gitignored); `waves init` moves an older team
file out of `_bmad/custom/`.

## Verifying the download

```bash
cd riaworks-waves-3.6.12.4-bundle && sha256sum -c SHA256SUMS      # Linux / WSL
shasum -a 256 -c SHA256SUMS                                        # macOS
Get-FileHash .\wheels\*.whl -Algorithm SHA256                      # Windows
```
