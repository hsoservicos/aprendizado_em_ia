# Setup guide

This module is two things: the bundled `waves-*` skills and the `waves`
orchestrator tool (the Python program that actually drives the loop). The skills do
nothing on their own — the orchestrator is what spawns the fresh coding-CLI sessions
that invoke the upstream `bmad-build-auto` skill (which implements and, re-invoked on
the done spec, runs the follow-up review) plus `waves-core-sweep` and
`waves-resolve`, watches their hook signals, and verifies
their artifacts. Installing the tool is part of setup, not
an optional extra.

There are two ways the skills land in a project. The orchestrator's wheel **bundles**
the three skills, so the simplest path is **pip + `waves init`**, which installs them
itself. Alternatively the **BMAD-method installer** copies them. Either way the
`/waves-setup` skill installs the orchestrator tool, picks which coding CLIs to
drive, and bootstraps the project. For the one-page summary,
see the [Installing the skill module](../README.md#installing-the-skill-module) section
of the README.

## Platform prerequisites

- **Python 3.11+** and a supported coding CLI (`claude` by default).
- **git 2.34 or newer** — every unit of work moves through git, so this one is enforced
  rather than advised: `waves run`, `sweep` and `resume` refuse to start below it, and
  `waves validate` reports it as a problem (`git.version`, exit 1). It is a **support**
  floor rather than a capability one — no git command waves issues needs 2.34 — set so
  the project stops carrying accommodations for releases it does not test against. 2.34 is
  Ubuntu 22.04 LTS's stock git; Ubuntu 20.04 (2.25) and Debian 11 (2.30) are below it.
  `git --version` reports what is on your `PATH`.
- **A terminal multiplexer** — the orchestrator drives agent sessions through a terminal
  multiplexer: **tmux** (POSIX) and the experimental **psmux** (native Windows) ship
  bundled, and further backends install as separate packages that register themselves
  (e.g. the [herdr adapter](https://github.com/pbean/bmad-loop-adapter-herdr), then
  `waves mux set herdr` — see
  [Terminal multiplexer backends](multiplexer-backends.md)). A backend is required for
  launching, attaching, and driving runs (pure TUI observation works without one). The
  multiplexer sits behind a pluggable seam (`TerminalMultiplexer`), so a new backend slots
  in without changing the engine — contributors should start with
  [Porting waves to a new OS](porting-to-a-new-os.md). `waves mux` lists the
  registered backends and shows which is selected (and why); `waves mux set <name>` —
  or the `[mux] backend` policy key, or the `WAVES_MUX_BACKEND` env var — forces the
  choice per machine.
- **OS** — Linux or macOS. **Windows is supported via WSL**, which _is_ Linux: tmux and
  every POSIX path work unchanged there, so no special setup is needed. **Native Windows is
  experimental** — the bundled `psmux` backend (a ConPTY tmux re-implementation) drives runs
  there and is selected automatically as the win32 default when its prerequisites are present:
  the `psmux` and `pwsh` (PowerShell) binaries on `PATH`, with `psmux` 3.3.8 or newer (older
  releases read as unavailable — see
  [multiplexer backends](multiplexer-backends.md#psmux-native-windows-experimental) for why). It is
  not yet at the Linux/macOS/WSL support tier — the remaining native-Windows work (window
  hosting, attach/detach, Unity cache paths) is tracked in
  [the roadmap](ROADMAP.md#native-windows-multiplexer-backend); the port path is in
  [Porting waves to a new OS](porting-to-a-new-os.md). Stopping a run is not part of
  that gap: `waves stop` lodges its request in a control file the engine reads itself,
  at item boundaries and mid-session, so it no longer depends on Windows signal delivery
  (#319). Inside WSL, install with the
  **Linux** interpreter — a Windows-installed waves is reachable from the bash prompt
  and silently behaves as Windows
  ([why](multiplexer-backends.md#psmux-native-windows-experimental)). To check:
  `waves mux` should read `platform default for linux`; if it names `win32` you are
  running the Windows build, and `waves validate` says so too. (A forced choice —
  `WAVES_MUX_BACKEND` or `[mux] backend` — is reported as the reason _instead_ of the
  platform, so clear it before reading that line as a platform check.)

## Installed via the BMAD-method installer? (recommended)

The BMAD-method installer copies the bundled skill directories (`waves-setup`,
`waves-core-sweep`, `waves-resolve` and the rest of the module) into your project. It does **not** carry the orchestrator tool — the installer copies only skill
directories, not their sibling files, so the tool can't ride along in the skill folder.
It is installed separately from Git by the setup skill. The canonical source is
<https://github.com/riaworks/waves>. (Going the other way, the tool's wheel
bundles the skills, so `waves init` can install them without the BMAD installer —
when the installer already placed them, `init` simply skips the existing copies.)

After the installer runs, complete setup with one command:

```bash
claude "/waves-setup accept all defaults"
```

`/waves-setup` handles both first-time setup and later upgrades — re-run it any time. It:

1. Installs **or upgrades** the `waves` tool from Git (see
   [Installing the tool and TUI](#installing-the-tool-and-tui)). On an upgrade it runs
   `uv tool upgrade riaworks-waves --reinstall`.
2. Asks **which coding CLI(s)** the orchestrator should drive, then runs `waves init`
   to install the `waves-*` skills + register hooks + write the `.waves/loop/policy.toml`
   template + add gitignore entries (including policy.toml itself — policy is per-machine; repos initialized before this run `git rm --cached .waves/loop/policy.toml` once if theirs is already committed) (see [Choosing which CLIs to drive](#choosing-which-clis-to-drive)
   and [Initializing CLIs other than claude](#initializing-clis-other-than-claude)). On an
   upgrade it passes `--force-skills` so the per-project skill copies are refreshed.
3. Runs `waves validate` as a preflight (see [Verify](#verify)).
4. Refreshes `_bmad/waves/module-help.csv`, the module's help entries. That is the
   only file it writes under `_bmad/` — module registration, the central `config.toml`,
   and the `/bmad-help` catalog are owned by the BMAD installer, which regenerates them
   on every run.

Run `/waves-setup` with plain prompts if you want to choose interactively — e.g.
`claude "/waves-setup cli: claude, codex"` to preselect the CLIs.

### Upgrading a project from 1.x

`riaworks-waves-loop` became `waves` in 2.0.0 — command, skill names, state directory,
environment prefix (the CHANGELOG's `2.0.0` entry carries the mapping). The layer that
migrated a 1.x project and kept it running meanwhile — the `riaworks-waves-loop` alias, the
`RIAWORKS_WAVES_LOOP_*` double export, the read-only listing of `.riaworks-waves/` runs and
`init`'s migration of that directory, the old relay and the old skill and override names —
**retired in 3.1**, on the date it had set for itself. A project still on 1.x (or on the
2.0 skill names) upgrades in two hops:

1. Install a 3.0.x release (`uv tool install 'riaworks-waves==3.0.*'`, or its bundle) and
   run `waves init --force-skills`: it moves `.riaworks-waves/` to `.waves/` with every run
   intact, removes the old relay's registrations, retires the old-named skill directories
   and renames the old overrides. Commit.
2. Install the current release and run `waves init --force-skills` again: it refreshes the
   skills and the relay and moves the overrides to `_waves/custom/`
   (see [Skill overrides](#skill-overrides-live-in-_wavescustom)). Commit.

On a BMAD-installer project, re-register the module afterwards with the **explicit** module
list — `npx bmad-method install --action update --modules bmm,waves --custom-source <package>`
— which is what drops a stale `riaworks-waves` entry (`quick-update` keeps it). The 1.x
out-of-tree control plane, `~/.local/state/riaworks-waves-loop/`, is needed by nothing; remove
it when you like.

## Installed from a bundle? (no Git remote, no index)

The module is also distributed as a single ZIP — `riaworks-waves-<version>-bundle.zip`,
produced by `scripts/build-dist.py --bundle` — for handing a class or a client an install
that needs no Git remote, no package index, no account and no token. It is the only
artifact that carries the Python side: the orchestrator **wheel** (which bundles the
skills), the module tree the BMAD installer reads, `INSTALL.md`, and two installers that
do **both levels** in one run.

```bash
# Linux, macOS, WSL — from inside the project
sh /path/to/riaworks-waves-<version>-bundle/install.sh

# native Windows (PowerShell)
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Project C:\code\my-project
```

Each run does the machine level (`uv tool install <wheel>[tui]` into uv's managed tool
environment) and then the project level (`waves init` + `waves validate`), and both are
idempotent. `--tool-only` and `--project-only` split them when one machine carries several
projects; `--cli <name>` is repeatable; `--via-bmad` additionally registers the module with
`npx bmad-method install --custom-source` so `/bmad-help` lists it. Install the **BMAD
Method first** — waves drives it and does not replace it.

**The target project is confirmed before anything is installed.** The current directory
is the default and Enter accepts it; the prompt says whether a `_bmad/` was found there.
Two directories are refused outright, however the installer is pointed at them: its own
bundle directory (the slip of extracting the zip and running it in place, which would
otherwise leave the skills, `.waves/` and a `.gitignore` beside the installer with no error
and nothing in the project) and the **home directory**, where `.claude/` is not a project's
but the coding CLI's global configuration — `waves init` there registers the hook relay in
the settings every project reads and drops the skills into the personal skills tree, and
nothing says so until every later session runs a relay for a project that has none. Where
the current directory is neither a BMAD project nor a git repository there is no Enter
default at all: a path must be typed. With no terminal to ask on it stops and asks for
`--project` rather than guessing. `--project` / `-Project` on the command line is an answer, so it does not ask.

**The installer brings the prerequisites, it does not demand them.** A machine that has
never run any of this has no uv, and possibly no python 3.11+, git, tmux — or, on native
Windows, no psmux and no pwsh. uv is installed from the publisher's own installer, python
through uv, and the rest through the system's package manager (winget on Windows, with
psmux taken from its GitHub release exactly as this project's CI does). What cannot be
installed without privilege is reported with the exact command and the install carries on
rather than stopping; `--no-bootstrap` / `-NoBootstrap` turns all of it off. Note that
`uv tool install` is given `--python ">=3.11"`: without it, uv resolves against the
system's default interpreter and refuses outright on a host whose `python3` predates the
floor, which is the common case on a fresh machine.

**Upgrades are a new bundle, not `uv tool upgrade`.** A wheel is a fixed version, so there
is nothing newer for uv to fetch; `uv tool upgrade` would report success and change
nothing. Running the newer bundle's installer replaces the tool and refreshes the project's
skill copies (it detects the existing install and passes `--force-skills` itself).

The bundle carries the whole of waves, but its dependencies still come from PyPI on first
install. For a machine with no network at all, download those wheels on a machine of the
same OS and Python version (`pip download "riaworks-waves[tui]" -d deps`) and pass
`--find-links deps`, which implies `--offline`.

On Windows, prefer WSL: it _is_ Linux, it uses tmux, and it is the supported tier — native
Windows runs on the experimental `psmux` backend and needs `psmux` 3.3.8+ and `pwsh` on
`PATH` (`install.ps1` checks for both and says so). See
[Platform prerequisites](#platform-prerequisites) above.

## Manual install (repo clone / dev setup)

If you are working from a clone of this repo, sync the project env and let
`waves init` lay down the skills (the canonical skills live at
`src/riaworks_waves_loop/data/skills/` and are bundled into the package):

```bash
uv sync --extra tui                                             # the orchestrator tool + TUI
uv run waves init --project /path/to/project --cli claude   # installs skills + hooks + policy
claude "/waves-setup accept all defaults"                   # install the tool + wire the project
```

Add `--cli codex --cli gemini` to also populate `.agents/skills/`. `init` always
installs all the bundled skills together (`waves-resolve`, `waves-core-sweep`,
`waves-setup`, and the operator monitors); `waves-core-sweep` owns the canonical `deferred-work-format.md`
the orchestrator normalizes the ledger to. The dev primitive `bmad-build-auto`
(spelled `bmad-dev-auto` before the 6.10.1 rename — the orchestrator resolves
whichever name is on disk and invokes that one) is
**not** bundled: it is the upstream skill the orchestrator drives (for both
implementation and the follow-up review), installed by the BMad Method (bmm)
module. `waves validate` checks it — plus any review skills its layers
invoke — are present before a run starts.

**Minimum BMAD-METHOD: 6.12.4**, enforced. `waves validate` reads the version
the BMAD installer recorded in `_bmad/_config/manifest.yaml` and reports it as
`bmad-config.version`: ok at or above the floor, a problem (exit 1) below it, a warning
when the manifest is absent or names no dotted version (a tree the installer never
wrote). `waves init` checks the same finding before its first write and installs
nothing below the floor; `run`, `sweep` and `resume` refuse on it too, so the install,
the preflight and the launch never disagree. 6.12 rewrote the primitive's review
step — the diff and the spec reach the reviewers as files, triage renders a verdict per
finding, `maybe-false` findings defer as `medium (unverified)` — and that is the protocol
this tool reads. 6.12.4 is the floor because every BMAD skill there reads its config
through `_bmad/scripts/resolve_config.py` (the four central TOML layers, custom
overrides included) instead of the legacy `_bmad/bmm/config.yaml`, and the bundled
skills read it the same way — on an older tree the two would resolve a
`_bmad/custom/config.toml` override differently. Its installer also pins the Test
Architect module to v1.27.2: TEA v2 and later install only through the BMAD v7
installer, which this release does not support. Older trees are still _resolved_ (both
primitive names, both review topologies below) but no longer supported. Upgrade a
project with `npx bmad-method@latest install` (quick update).

Beyond the primitive itself (with its `customize.toml`), `waves validate`
holds you to no fixed list of review skills: it reads the primitive you actually have
installed and requires the reviewers that copy will actually invoke — which on current
sources is none at all.

- **Layer-driven (6.10.1 onward — every supported release)** — `customize.toml` defines
  `[[workflow.review_layers]]`, and a layer's `instruction` may name a skill to hand
  off to. Since 6.11 the sources define four layers — `blind-hunter`,
  `edge-case-hunter`, `verification-gap` and `intent-alignment` — and none of them
  invokes a skill: each is a self-contained prompt — `edge-case-hunter` and
  `verification-gap` read the primitive's own `review-prompts/*.md`, `blind-hunter`
  and `intent-alignment` carry their prompt inline. Since 6.12 the reviewers receive
  paths rather than pasted text: `{diff_file}` (the unified diff) for every layer and
  `{claims_file}` (the spec) for the edge-case layer alone. Such a tree requires no
  review skill at all. An intermediate release whose layers invoke the merged `bmad-review`
  with one lens each needs `bmad-review`; an earlier one naming the standalone hunters
  needs exactly those instead.
- **v6.10.0 (below the floor — resolved, not supported)** — no `review_layers` section
  at all; `step-04-review.md` names `bmad-review-adversarial-general` and
  `bmad-review-edge-case-hunter` inline, so those two are what is required.

A layer disabled with an empty `instruction`, or replaced in
`_bmad/custom/bmad-build-auto.toml` by a recipe that runs something else, requires
nothing. If the shape cannot be read at all, `validate` falls back to requiring the two
v6.10.0 hunters — which a tree carrying `bmad-review` satisfies.

`bmad-review-verification-gap` is no longer required unconditionally (#260): no tagged
release ships it as a standalone skill, and on current sources it is only a thin
forwarder to `bmad-review`. It is required exactly when your installed layers name it.

### Skill overrides live in `_waves/custom/`

The `waves-*` skills that ship a `customize.toml` — `waves-master-parallelism`,
`waves-core-parallelism` and `waves-tests` — read your overrides from a directory of their
own, beside `_bmad/` and not inside it:

- `_waves/custom/<skill>.toml` — the team layer, versioned; commit it.
- `_waves/custom/<skill>.user.toml` — your personal layer; `init` gitignores it.

Each skill resolves them with its own `assets/resolve_customization.py`, using the BMAD
Method's merge rules (tables merge; arrays of tables merge by `code`, else `id`; other arrays
append; a scalar from the override wins). Until 3.1 these files lived in `_bmad/custom/`.
`waves init` moves a team file from there and prints `commit the move`; a personal file is
yours and is never moved for you — `waves validate` names it (`customize.location`). A skill
whose team file is still at the old location refuses to start and prints the `git mv`,
because running on the shipped defaults would drop your settings without a word.

### Customizing the review layers

Your project overrides in `_bmad/custom/bmad-build-auto.toml` (team) and
`_bmad/custom/bmad-build-auto.user.toml` (personal, gitignored by the bmm installer) are
applied before the requirement is computed. (Overrides are keyed by skill directory
name, so a pre-6.10.1 install spells both files `bmad-dev-auto*.toml`; the deprecated
shim offers to rename them when you first invoke the old name.) The merge follows the
same rules BMAD's own resolver uses: an array of tables merges by key only when
_every_ entry — default and
override alike — carries the same `code` or `id`; otherwise the override appends. So
adding a layer with a new `id` adds a requirement, and replacing one by `id` moves it.

Two things `validate` reports but never blocks on, because neither can be decided
without running the review:

- a layer gated by a `when` condition, which the model evaluates against the diff;
- a layer naming a skill in a phrasing that is not recognizably a handoff (the
  convention is ``Invoke the `skill-name` skill``).

Both come back as `skills.review-layer-unresolved` warnings, so a customized layer can
never block a run the way the old fixed catalog did. What _is_ a problem: every layer
disabled at once (`skills.review-layers-empty`), which makes the primitive HALT
blocked with `no active review layers`.

Under `isolation = "worktree"` the skills your layers name are copied into each unit's
worktree along with `_bmad/custom/`, so an isolated run resolves the same layers
`validate` checked — including from the gitignored `*.user.toml`, which a fresh checkout
would not carry.

### BMAD-METHOD 6.12: `project-context.md` is no longer auto-loaded

Up to 6.11 the dev primitive's `customize.toml` shipped
`persistent_facts = ["file:{project-root}/**/project-context.md"]`, so every dev and review
session started with that file in context. 6.12 ships `persistent_facts = []` in
`bmad-build-auto`, `bmad-review` and `bmad-sprint-planning`: the upstream direction is
`bmad-project-context` writing a managed block into `AGENTS.md`, which the coding CLI loads
on its own. The orchestrator does not paper over this — `_bmad/custom/` is a deliberate
boundary, and the only facts `init` manages there are the TEA test-location ones. Pick one:

- run `/bmad-project-context` once so the facts land in `AGENTS.md` (recommended — it is what
  the sessions read anyway), or
- re-add the fact yourself in `_bmad/custom/bmad-build-auto.toml`:

  ```toml
  [workflow]
  persistent_facts = ["file:{project-root}/**/project-context.md"]
  ```

Two more 6.12 changes worth knowing when you customize the primitive. A review-layer
override that still writes `{diff_output}` sends its reviewer an empty prompt — the
placeholders are `{diff_file}` and `{claims_file}` now, both paths. And a fresh 6.12 install
carries no `bmad-dev-auto` shim (`--shims` restores it); nothing here needs it, the
orchestrator drives `bmad-build-auto`.

### Pointing retrospectives at run journals

`bmad-retrospective` reads session logs as evidence for its process lessons: why a
session stalled, what it tried and dropped. It doesn't know where waves keeps them,
so on an epic waves drove it finds none and skips that analysis. waves ships no
override for this (DW-387). To point the skill at the run records, create
`_bmad/custom/bmad-retrospective.toml` yourself, or `bmad-retrospective.user.toml` for a
personal copy:

```toml
[workflow]
persistent_facts = [
  "Session logs for waves-driven stories are the waves run directories, .waves/loop/runs/<run-id>/ under {project-root}. journal.jsonl is one JSON event per line: a session-start (task_id, role, story_key, adapter, model) and a session-end (task_id, tokens, and a status of completed, stalled, timeout, crashed, over_budget or aborted) per coding-CLI session, joined on task_id since session-end carries no story_key, plus review results and retries, rollbacks, pauses and escalations. logs/<task-id>.log is that session's raw terminal capture (tmux pane output including escape sequences and repaints; for the hookless opencode profile, a readable transcript), and the journal's log_task / log_pos fields give the log file and byte offset each event lines up with. state.json records the run's stories and their outcome. Find the runs for this epic by grepping journal.jsonl files for its story keys. Runs archived by waves archive or waves clean are .waves/loop/archive/<run-id>.tar.gz and still hold journal.jsonl, state.json and logs/: search inside them as well. Record a session-log gap only for runs that were deleted.",
]
```

`persistent_facts` appends to the skill's defaults, so this fact adds to any others you
already set. Don't use a `file:` glob such as `file:.waves/loop/runs/*/journal.jsonl`
instead: it would load every run's full journal into the retro's context.

The records last only as long as the run directory or its archive. `waves clean`
compresses finished runs outside the retention window to `.waves/loop/archive/` (with
`--hard`, or with `[cleanup] archive_old = false`, it deletes them), and `waves archive`
does the same for a single run. Both the retro and the fact above can still read an
archived run. `delete`, and a `clean` that deletes, remove a run for good.
`clean --keep <run-id>` protects a run for that one invocation only, so pass it every
time or retro the epic before its runs are deleted.

## Choosing which CLIs to drive

The supported adapters are `claude` (the default), `codex`, `gemini`, `copilot`,
`antigravity` (Google's `agy`, experimental — `isolation = "none"` only), and `opencode`
(OpenCode ≥ 1.18 over HTTP/SSE, profile `opencode-http` — no tmux window; needs the
`riaworks-waves[opencode]` extra and `model` set as `provider/model`). You can pick more
than one — register every CLI you intend to use for dev, review, or sweep triage.

There are **two layers** here, and confusing them is the usual stumbling block:

- `waves init --cli <name>` registers the orchestrator's **hooks** for that CLI. Without
  registered hooks, a CLI can't signal the engine.
- `.waves/loop/policy.toml` `[adapter]` selects which CLI actually **runs** each stage.

So a mixed setup — say `claude` for dev and `codex` for review — needs _both_: the hooks
registered for each CLI (`--cli claude --cli codex`) **and** the role pointed at that CLI in
`policy.toml`:

```toml
[adapter]
name = "claude"        # default for every stage

[adapter.review]
name = "codex"         # the review pass runs on codex instead
```

Any CLI named in `policy.toml` must also have been registered with `--cli`. To add one later,
re-run `waves init --cli <name>`. If you only use a single CLI, leave `policy.toml`
untouched — the default is correct.

## Installing the tool and TUI

The `[tui]` extra pulls in the Textual dashboard (`textual` + `tomlkit` + `pyte`) so
`waves tui` works. The core tool needs only `pyyaml`.

**Together (recommended):**

```bash
uv tool install "riaworks-waves[tui] @ git+https://github.com/riaworks/waves.git"
```

**Tool first, TUI later (separately):** install the core without the extra, then add the
dashboard whenever you want it by re-running the same command **with** `[tui]`:

```bash
# core tool only
uv tool install "riaworks-waves @ git+https://github.com/riaworks/waves.git"

# add the TUI later — re-run with the extra (uv upgrades the install in place)
uv tool install --upgrade "riaworks-waves[tui] @ git+https://github.com/riaworks/waves.git"
```

Until the extra is present, `waves tui` prints a clear error
(`the TUI requires optional dependencies — uv tool install 'riaworks-waves[tui]'`) rather than
failing obscurely.

`uv tool install` drops `waves` into uv's own managed tool environment, so there's no
PEP 668 externally-managed conflict and no need for a virtualenv, `--user`, or `--break-system-packages`.

To upgrade later, the simplest path is to re-run `/waves-setup` (or `/waves-setup
upgrade`) — it detects the existing install, upgrades the tool with `uv tool upgrade
riaworks-waves --reinstall` (the `--reinstall` is **required** for a git source — a plain
`uv tool upgrade` reuses the cached commit and won't pull new code), and re-lays the
per-project skills with `waves init --force-skills`. To do it by hand, run those two
commands yourself (see the [Upgrading](../README.md#upgrading) section of the README).

Confirm with `waves --version`.

## Initializing CLIs other than claude

`waves init` registers hooks and installs the bundled `waves-*` skills per CLI. The
`--cli` flag is repeatable — pass it once per CLI you want to drive:

```bash
# claude only (default)
waves init --project <project-root> --cli claude

# multiple, e.g. claude + codex + gemini
waves init --project <project-root> --cli claude --cli codex --cli gemini
```

Run with no `--cli` and `init` registers hooks for every CLI the `policy.toml` references,
so a dual-client setup that's already configured in policy needs no extra flags. Names must
be exactly `claude`, `codex`, `gemini`, `copilot`, `antigravity`, or `opencode-http` (alias
`opencode`) — `init` errors on an unknown profile and lists the valid ones. A hookless
profile like `opencode-http` installs its skills but registers no hooks (it signals over
HTTP/SSE).

### First-run notes

Each CLI needs a one-time interactive setup before the first `waves run`, because
spawned sessions can't answer first-run dialogs. `init` prints the relevant notes; relay
them to whoever owns the machine:

- **claude** — run `claude` once in the project and accept the workspace-trust + hooks-approval
  dialogs.
- **codex** — run `codex` once in the project and accept **both** prompts: workspace trust,
  then "Hooks need review → Trust all and continue" (untrusted hooks silently never fire).
  Requires Codex ≥ 0.139.
- **gemini** — authenticate once (browser OAuth or `GEMINI_API_KEY`). Requires Gemini CLI
  ≥ 0.46.
- **copilot** — run `copilot` once in the project and authenticate (`gh` / a Copilot
  subscription). Requires the Copilot **CLI** GA (≥ 2026-02) — _not_ the VS Code extension.
  **Pin a capable model**: the free default (GPT-5 mini) silently skips steps in the
  multi-step dev/review skills; set `[adapter] model = "claude-sonnet-4-6"` (→ `--model`).
- **antigravity** — run `agy` once in the project, authenticate, and answer
  **"Yes, I trust this folder"** before `waves run`; spawned sessions can't answer that
  dialog, and a pending one reads as a session timeout. Requires Antigravity CLI
  (`agy` ≥ 1.1.3). Two limitations to know, both verified against 1.1.3:
  - **Trust is exact-path.** `settings.json` `trustedWorkspaces` matches whole paths —
    trusting a parent does _not_ cover its subdirectories, and
    `--dangerously-skip-permissions` does not bypass the dialog (it covers tool
    permissions only). `isolation = "none"` (the default) works once the project root
    is trusted. **`isolation = "worktree"` works too**, as long as the project root is
    trusted: after provisioning each unit worktree, waves appends its path to
    `~/.gemini/antigravity-cli/settings.json` `trustedWorkspaces` before any session
    launches (journaled `worktree-trust-seeded`). It only ever extends a grant you
    already made — with the root untrusted nothing is written
    (`worktree-trust-unseeded`) and the session will hang on the dialog. Check a path
    with `waves probe-adapter antigravity --workspace <path>` (exit `0` = trusted).
    **Known limitation:** entries are never removed when a worktree is torn down, so
    `trustedWorkspaces` accumulates one entry per unit — prune stale
    `.waves/loop/runs/` paths by hand if the list grows. See
    [#169](https://github.com/riaworks/waves/issues/169) / DW-390.
  - **Token usage is not recorded** (`usage_parser = "none"`) — and this is permanent,
    not a gap: agy's transcript carries no usage data at all (it counts tokens only in
    an internal SQLite/protobuf store). Runs work; the token columns stay empty.
- **opencode** — install the HTTP client extra (`pip install 'riaworks-waves[opencode]'`) and
  authenticate once, **globally**, with `opencode auth login` (not per-project — there is no
  workspace-trust dialog to answer). Requires OpenCode ≥ 1.18. Set the model as
  `provider/model` (e.g. `[adapter] model = "anthropic/claude-haiku-4-5"`). A reasoning
  `effort` (e.g. `[adapter.review] effort = "max"`) is sent as the per-prompt variant and is
  opencode-only — the tmux CLIs ignore it. No hooks are
  registered — the adapter drives a headless `opencode serve` over HTTP/SSE, so there is no
  tmux window to attach to; watch a session via its `logs/<task-id>.log` — a curated
  transcript of the agent's prose, tool calls, file edits and permission decisions — or the
  TUI Log tab. The server's own stdout lands beside it in `<task-id>.server.out`, and a
  structured trace of the raw SSE frames in `<task-id>.sse.jsonl`.

### Skill location

`claude` reads skills from `.claude/skills/`; `codex`, `gemini`, `copilot`, and `antigravity`
read from `.agents/skills/`. `init` installs the bundled `waves-*` skills into the right tree
for each CLI you pass via `--cli`, so selecting any of the `.agents/skills/` CLIs populates it automatically. It skips skill
dirs that already exist — pass `--force-skills` to overwrite a stale copy, or `--no-skills` to
manage them yourself.

## Verify

Preflight the project — config, sprint-status, git, tmux, and the coding CLI:

```bash
waves validate --project <project-root>
```

`validate` exits non-zero when the project isn't fully ready (e.g. no `sprint-status.yaml`
yet, or `bmad-sprint-planning` hasn't run). On a fresh project that is **expected** — read its
output as a readiness checklist, not an install failure.

For the dashboard itself, see [docs/tui-guide.md](tui-guide.md). For the full policy
reference, see the [Policy section](../README.md#policy-wavespolicytoml) of the README.

## Uninstalling

Removing waves is the inverse of [`waves init`](#initializing-clis-other-than-claude):
undo what it laid down (the `.waves/loop/` state, the per-CLI hooks and skills, the gitignore
lines), then uninstall the tool. There is no `waves uninstall` command — the steps below
are the documented manual procedure. Work **inside the project root**, and reclaim disk
**before** deleting state so no worktrees or archives are orphaned.

Two paths overlap: every project does steps 1–5 and 7; only projects with a `_bmad/` tree
also need step 6.

### 1. Reclaim run disk first

Tear down any leftover worktrees, tmux sessions, and archived runs while the tool is still
installed — once `.waves/loop/` is gone these are unreachable:

```bash
waves clean --hard --project <project-root>   # delete every concluded run + its worktrees
waves cleanup --project <project-root>         # kill leftover tmux sessions/windows
```

`clean --hard` permanently deletes runs instead of archiving them (we're removing the tool, so
there's nothing to keep). Running it **first** also matters for the out-of-tree half: each run's
control-plane directory lives under the user-scoped state root, and `clean` is what collects it
(step 2 covers what is left over). See the disk-reclamation coverage in
[docs/FEATURES.md](FEATURES.md) and the [command reference](../README.md#command-reference) for
what each command touches. Make sure no run is still live (Editor open, session attached) first.

### 2. Remove the orchestrator state

Delete the `.waves/loop/` directory. This removes the `policy.toml` template,
legacy relay copies from older installs, and all per-run state
(`runs/`, `cache/`, `archive/`) in one step:

```bash
rm -rf .waves/loop/
```

One piece is **not** under `.waves/loop/`: each run's hook-event channel lives in a user-scoped
state root outside the project (#494) — `$XDG_STATE_HOME/waves`, else
`~/.local/state/waves`; `%LOCALAPPDATA%\waves\state` on Windows; or whatever
`BMAD_LOOP_STATE_DIR` names. Step 1 collected this project's runs from it, leaving an empty
per-project directory whose name is a digest of the project path — not something to pick out by
hand. That root is shared by **every** project on this machine, so delete the whole thing only if
you are removing waves everywhere:

```bash
# all projects on this machine — same cascade the orchestrator resolves
rm -rf "${BMAD_LOOP_STATE_DIR:-${XDG_STATE_HOME:-$HOME/.local/state}/waves}"
```

### 3. Remove the bundled skills

`init` installed the bundled `waves-*` skill directories — delete only those. **Leave
the standard BMAD skills alone** (`bmad-*`); install never touched them.

```bash
# claude reads from .claude/skills/ ; codex/gemini read from .agents/skills/
rm -rf .claude/skills/waves-*
rm -rf .agents/skills/waves-*
```

(Run only the line for the skill tree your CLIs use — drop the other. A project set up
before the 2.0.0 rename may still carry old-named directories, `riaworks-waves-loop-*` and
`riaworks-waves-plan*`; remove those too.)

### 4. Deregister the hooks

`init` **merged** its Stop-hook registration into each CLI's existing hook config, so these
files must be **edited, not deleted** (they hold your own settings too). In each config below,
remove the hook entry whose `command` ends in `waves relay <Event>` (or, on
older installs, is a Python or `uv run --no-project python` command whose script
path ends in `.waves/loop/waves_hook.py` and whose event argument matches
that hook event):

- **claude** — `.claude/settings.json`
- **codex** — `.codex/hooks.json`
- **gemini** — `.gemini/settings.json`
- **copilot** — `.github/copilot/settings.json`
- **antigravity** — `.agents/hooks.json` (the `waves` hook group)

Edit only the registered CLIs. Match the full relay command and event; leave every
other hook in place. The installed `waves` executable is shared with other projects,
so remove it only when uninstalling the package itself.

### 5. Drop the gitignore lines

`init` appended `.waves/loop/runs/`, `.waves/loop/cache/`, `.waves/loop/policy.toml` and
`_waves/custom/*.user.toml` to `.gitignore`. Remove those lines (skip any your project relies on for other reasons). If
you had run `git rm --cached .waves/loop/policy.toml` to stop sharing the per-machine policy, the
file is untracked — re-add it (`git add .waves/loop/policy.toml`) only if you want it back in version control.

### 6. Remove the BMAD module (BMAD-installer projects only)

There is nothing to hand-unregister: waves writes no BMAD config. If you installed the
module through the BMAD installer, remove it there — the installer owns `_bmad/waves/`,
the central `config.toml`, and the `/bmad-help` catalog, and regenerates all three on its
next run.

If you only ever ran `/waves-setup`, delete `_bmad/waves/module-help.csv` (the one
file it refreshes) — or the whole `_bmad/waves/` directory if the installer never
created it. uv + `init`-only projects that have no `_bmad/` can skip this step.

### 7. Uninstall the tool

```bash
uv tool uninstall riaworks-waves
```

The name is the **package's**, not the command's: `uv tool list` shows `riaworks-waves`
with the `waves` command under it, and `uv tool uninstall waves` finds nothing to remove.

Confirm removal: `waves --version` should now fail with a command-not-found error. Repeat
steps 1–6 in every project that used the tool — the tool install is machine-wide, but the
state, skills, and hooks are per-project.
