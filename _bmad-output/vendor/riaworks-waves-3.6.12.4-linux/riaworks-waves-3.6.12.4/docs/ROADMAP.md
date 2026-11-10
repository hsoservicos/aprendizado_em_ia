# waves roadmap

Forward-looking work for the orchestrator itself — design intent and rationale for features
we've deliberately deferred, so the "why" survives between sessions.

Status legend: **planned** (agreed, not started) · **in progress** (started; some pieces shipped, the headline goal not yet met) · **exploring** (shape still open) · **blocked** (waiting on an external dependency).

---

## Native Windows multiplexer backend

**Status:** in progress — the platform seams and a native-Windows backend (`psmux`, held by a real-Windows live gate) have **shipped in-tree**; still open are the second tmux-family backend `tmux-windows` (#85), herdr's win32 launch path, and the open questions at the end of this section · **Foundation:** the full platform-seam series landed (multiplexer registry + `BaseTmuxBackend` + `ProcessHost` + hook interpreter + validate preflight, v0.7.6; availability-aware backend selection + `waves mux`, #87; out-of-tree backend discovery via `riaworks_waves_loop.mux_backends` entry points; original seam v0.7.0) · a first non-tmux-family, native-Windows-capable backend — **herdr** — ships end-to-end on POSIX as the external [bmad-loop-adapter-herdr](https://github.com/pbean/bmad-loop-adapter-herdr) (the win32 `agent.start` launch path is tracked there)

The orchestrator no longer fuses tmux into the engine. All session/window/pane operations
go through a single `TerminalMultiplexer` ABC (`src/riaworks_waves_loop/adapters/multiplexer.py`),
obtained from `get_multiplexer()`; the tmux backend — argv + spawn primitive in
`BaseTmuxBackend` (`adapters/tmux_base.py`), POSIX leaf `TmuxMultiplexer`
(`adapters/tmux_backend.py`) — is the **only** place allowed to shell out to `tmux`, and it
quarantines the POSIX `sh -c` parked-window trailer. Backends now self-**register**
(`register_multiplexer`) rather than being hardcoded into `get_multiplexer()`, and selection
(#87) is availability-aware with a dev-choosable persisted pick: `WAVES_MUX_BACKEND` env
var → the machine-scoped `[mux] backend` policy key (`waves mux set <name>`; policy.toml
is gitignored) → the platform default (win32: `psmux`, elsewhere: `tmux`) when installed →
the first registered platform match that is `available()`. The process-lifecycle POSIX-isms moved behind a
matching seam, `ProcessHost` (`src/riaworks_waves_loop/process_host.py`): `terminate` / `force_kill` /
`is_alive` / `identity` (a PID-reuse guard) plus `hook_interpreter()` (so hook registration
never branches on platform), registered the same way (`register_process_host`,
`WAVES_PROCESS_HOST`); `WindowsProcessHost` already ships. `waves validate` runs a
`platform_preflight(project)` (`runsetup.py`) that reports the selected backend's readiness and names the process
host — so a new OS surfaces in preflight by registering, not by a `validate` edit. The Unity
plugin's `/proc`/`/tmp`/`cp -a`/symlink primitives degrade off Linux (with `psutil` from the
optional `non-linux` extra) and its pid lifecycle now delegates to `ProcessHost`; everything is
held by a CI portability guard (`tests/test_portability_guard.py`). **WSL already works today**
— it _is_ Linux, so it takes every fast path unchanged; this is purely about a future _native_
Windows host.

Three native-Windows candidates now exist, and they are **not stages of one plan**.
Two are **sibling tmux-family backends**: `psmux` has **shipped in-tree** (drives
psmux's tmux-compatible CLI through its own `psmux` binary, via pwsh) while
`tmux-windows` (#85; drives the tmux-windows port) is still in flight — both subclass
`BaseTmuxBackend` and both register for `win32`, which is why selection is
availability-aware with discriminating `available()` probes (psmux →
`which("psmux") and which("pwsh")` plus a version gate requiring psmux 3.3.8 or newer
([why](multiplexer-backends.md#psmux-native-windows-experimental)); tmux-windows →
`which("tmux") and not which("psmux")`) and an explicit `waves mux set <name>` tie-break.

The third — **herdr** — has **shipped** end-to-end on POSIX (engine run path +
TUI-launch surface), and now lives **out-of-tree** as the reference external adapter,
[pbean/bmad-loop-adapter-herdr](https://github.com/pbean/bmad-loop-adapter-herdr)
(developed in-tree in #136/#137, extracted pre-release per core-team direction; it
co-installs with waves and self-registers via the `riaworks_waves_loop.mux_backends`
entry-point group). It is a different-binary-family backend: it implements
`TerminalMultiplexer` fresh over herdr's workspace/tab/pane model rather than
subclassing `BaseTmuxBackend`, and probes `which("herdr")`, so it is
pairwise-discriminating against the tmux family by construction (no `mux set`
tie-break needed to tell them apart). It registers with `matches = True` (all
platforms), which keeps the door open for native Windows without disturbing POSIX. On
POSIX, tmux stays the platform default, so herdr activates only on an explicit
`WAVES_MUX_BACKEND=herdr` / `waves mux set herdr`. On **win32**,
`_PLATFORM_DEFAULTS` is **untouched** — psmux remains the declared win32 default — so
herdr is picked only by **first-match** (the fourth precedence step) when installed and
`available()` and no higher-priority backend is: once psmux (or tmux-windows) ships and
registers for win32, the win32 default reasserts and outranks herdr's first-match
automatically, no code change. herdr's `exec` launch is POSIX-only for now; the Windows
launch path (herdr's `agent.start`) is tracked in
[the adapter repo's issues](https://github.com/pbean/bmad-loop-adapter-herdr/issues),
and the Phase-0 characterization must be re-run on a real Windows host before #92 is claimed.

The seams are designed so each backend slots in as **new files plus one registration line,
with no change to the adapters, `runs.py`, `tui/launch.py`, `probe.py`, `tui/data.py`, or
`cli.py`'s `validate`** (`WindowsProcessHost` and its hook interpreter are already in place
and registered; herdr proved this end to end — one registration line and one sanctioned
`probe.py` gate fix, zero portability-guard allowlist changes; the extraction then proved
the **fully external** path — the same registration arriving via entry-point discovery,
zero core files). The end-to-end port path —
both build options, the test-override env vars, and exactly what a native-Windows port costs —
is documented in [Porting waves to a new OS](porting-to-a-new-os.md); the deep transport
contract is in the
[adapter authoring guide](adapter-authoring-guide.md#the-transport-contract-for-a-backend-author).

**Open questions:** what hosts the windows on native Windows (Windows Terminal panes, a
ConPTY-based manager, a headless process supervisor?); how attach/detach and the parked
exit-status window map without a POSIX shell; and the Windows-Unity cache-path correctness
left as a documented follow-up in Phase 4.

---

## Parallel unit execution (`[scm] max_parallel`)

**Status:** shipped (phases 1–7, 2026-09-07; see the Unreleased changelog) · **Foundation:** worktree isolation (v0.4.0); the LLM control loop and the
`unit` verbs (2.0.0); the wave plan `waves-master-parallelism` writes — collision matrix, waves and
fronts, merge grid, machine-readable block (3.0 layout) · **Measured 2026-09-07:** a project's own
per-front provisioning (`easychef-provisioning`: compose project and port range per worktree,
database cloned from the owner's installation, own `.env`, idempotent `front.sh up`, give-back at
the end) proves fronts can contend on machine capacity alone, never on data.

### What shipped

Every phase below landed. One design decision differs from the sketch: the deterministic
engine's fan-out (phase 7) is by PROCESS, not by thread — `Engine.workspace` is one per
process by construction (seventy-odd sites in the engine, the sweep and the recovery flow
read it), so the run that carries a `--plan` and a `max_parallel` above one becomes the
**wave master** and launches one child run per front (`waves run --deterministic --plan …
--front <name> --wave <n>`), each child the ordinary engine holding integration; the master
adopts, rebases, re-verifies and lands in the grid's order (`wavemaster.py`). The rest is as
planned: `--plan` as scope, `unit pick --wave` / `await` on several sessions, `close` in
merge order with `unit rebase`, the provisioning contract with `waves-provisioning` as its
author, the two knobs (`max_parallel`, `[verify] concurrency`), the dashboard's plan line,
merge queue and `wave` column. The section below is the state that motivated it, kept for
the record.

### Where it stood

- `max_parallel` is parsed and validated (`ScmPolicy`) and **clamped to `1` in `loads()`**: no fan-out
  scheduler, merge-back one unit at a time.
- Each unit already has its own worktree and branch with a pinned baseline. In the LLM loop
  `unit open` refuses only the _same_ story twice, `unit finish` refuses while stories are in flight,
  and the dashboard's tasks table is per task — nothing structural forbids two stories in flight.
- What the engine cannot invent is the **plan**: which stories collide, which may run together,
  in what order they merge, who rebases. That is judgment, and the control loop makes no LLM call.
  The planner door already produces it and asks the owner one question at a time.
- Provisioning is copy-only: `[scm] worktree_seed` and the plugins' `seed_globs` put gitignored
  paths into a fresh worktree. No command runs at open, and no plugin stage exists there (the
  stages stop at `pre_dev_phase`), so projects provision **LLM-side, per story** — tokens spent and
  a rule the session has to remember.
- Verification shares resources: the parallelism skills queue the suite (`suite-queue.sh`) because
  two suites on one database corrupt each other.

**Design principle:** plan in the door, execute in the engine. The skills' "one master per project"
becomes "one run per project". Cross-model fronts come for free — the adapter per role is the
policy's — which the subagent fronts of `waves-core-parallelism` can never have.

### Phases

1. **Scope by plan.** `waves run --plan <epic-N-plan-<date>.md>`: the plan's machine-readable block
   becomes the run's story set — any epics, since the plan's unit is the story — with waves, fronts
   and grid recorded in `state.json`. `--epic` / `--story` stay as they are. The epic boundary keeps
   firing when an epic's last story closes, so a cross-epic set works and merely leaves epics half
   open, which the planner already warns is not ideal. The door's `[V]` (plan vs tracker) is the
   validation to reuse before launch.
2. **Fan-out in the LLM loop.** Doctrine plus two verbs: `unit pick --wave` answers the current wave's
   dispatchable fronts, and `max_parallel` is lifted for `source: llm` as the cap on sessions in
   flight. A front is a task; the supervisor and the turn classification do not change. The pulse
   watcher's per-task signals (`sessao-muda`) already read per task.
3. **Merge-back serialized by the grid.** Under the run lock, in the grid's order. When a later
   front's merge conflicts: a rebase-and-reverify path — `reopen_unit`, rebase on the target,
   the verify ladder again, merge — with bounded attempts, then the plan's fallback (defer the
   story, with its question in the ledger). The journal records the grid position of every merge;
   `head-compartilhado-mexeu` learns that several merges per wave are normal.
4. **Provisioning contract.** `[scm] provision = "<cmd>"` and `teardown = "<cmd>"` — or a plugin
   stage pair, `post_unit_open` / `pre_unit_close`, so a project plugin can own it — run by the
   engine after the worktree is mounted and after integration **and after rollback**, with a
   timeout and a journal entry. Provisioning that fails parks the story before a session is spent;
   teardown always runs, so no stack outlives its story. `worktree_seed` stays the copy layer
   underneath. Alongside, an authoring skill (an extension of `waves-setup`, or a
   `waves-provisioning` of its own) run once per project: it discovers compose, ports, database,
   environment files, install, migrate and the smoke check, writes the `front.sh`-shaped script, the
   policy keys and the `worktree_seed` list, and leaves a consult skill in the project in the
   `easychef-provisioning` shape (what is fixed, what is never done, what each failure means). The
   pattern of the superpowers worktree skill — a standard location, ignored config copied in,
   dependencies installed, a green baseline before work starts — is the reference; read its text
   before borrowing its shape.
5. **Two knobs, not one.** `[scm] max_parallel` bounds sessions in flight; `[verify] concurrency =
"queue" | "parallel"` bounds the suite. `queue` is the default and moves the skills'
   `suite-queue.sh` into the engine as a run-level lock around the verify ladder; `parallel` is
   allowed only when the provisioning recipe declares `isolated_data = true`, and `validate` refuses
   it otherwise. Capacity is the operator's call, per machine.
6. **Dashboard.** Tasks grouped by wave and front, the merge queue with grid positions, per-run
   counters (in flight · merged · waiting on the grid). The sprint tree already renders several
   `in-progress` stories.
7. **Deterministic engine.** The Phase 5 scheduler reads the same plan and lifts the clamp for the
   deterministic source, with the same merge-back and provisioning contract. No LLM in the control
   loop: the plan's judgment stays in the planner; what the plan does not settle parks the story.

**Open questions:** token and cost budgets for N concurrent sessions beyond the cap; conflict
resolution past a rebase (the skills' "integrate two implementations that collided" is judgment:
the orchestrator's in the LLM loop, a park in the deterministic one); what `heartbeat.py` measures
per front in a deterministic run; whether the door's `[E]` should launch `waves run --plan` directly
once phase 2 lands, leaving `waves-core-parallelism` for harnesses without the engine.

---

## Automate epic retro action items

**Status:** planned · **Blocked-by:** retro-item detail isn't standardized yet

The parser now recognizes `epic-{N}-retro-item-{M}-{slug}` keys in `sprint-status.yaml`
(`src/riaworks_waves_loop/sprintstatus.py` → `RetroItem` / `SprintStatus.retro_items`), so the
`sprint-status-unknown-keys` warning no longer fires. They are tracked but **not driven** as work.

The goal is to run actionable (`backlog`) retro items through the dev → review → commit pipeline,
the same way deferred-work sweeps already run.

**Approach (designed, not built):** a separate `waves retro` run type that mirrors the
`SweepEngine` (`src/riaworks_waves_loop/sweep.py`) end-to-end — `RetroEngine`, a `retro` CLI command + resume
branch, a retro-item intent fed to the `bmad-build-auto` primitive, and `verify` helpers paralleling
the bundle verifiers. Story runs stay untouched.

**Why blocked:** retro-item _detail_ is scattered — some lives in the epic retro-doc Action-Items
table (`epic-N-retro-YYYY-MM-DD.md`), some in `deferred-work.md` (DW-N) entries, some in ad-hoc
`spec-*.md` files; only one epic has an `epic-N-action-items.md`. A deterministic key→file map isn't
viable, so automation needs an LLM triage step (like sweep's) to locate/extract each item's intent
**and** classify out the non-code items (research, docs). **Prerequisite:** standardize where
retro-item detail is written at retrospective time (a future BMAD update) — that makes the triage
reliable enough to trust unattended.

---

## Integrate BMAD test-design + test-automation runs (TEA / testarch)

**Status:** exploring · **Foundation:** the bundled `waves-tea` plugin

The bundled `waves-tea` plugin (`[plugins] enabled = ["waves-tea"]`, see the
[TEA plugin guide](tea-plugin-guide.md)) now wires the BMAD Test Architect (TEA) suite —
`bmad-testarch-test-design`, `-automate`, `-atdd`, `-nfr`, `-trace`, `-test-review`, and the
`bmad-tea` agent — into runs and sweeps at the cadence each step pays for: a red-phase
acceptance scaffold before every story, the four analyses once per epic, and optional
commit-time gates (`<step>_enforce`). The workflows ride the generic
`[workflows.<name>]` session-injection layer rather than being first-class orchestrated runs.

The remaining work is to drive **test design** (derive a test plan / coverage map for a feature or
backlog) and **test automation** (generate + run the actual tests) as first-class orchestrated runs —
closing the loop that retro items like `epic-5-retro-item-1-test-design-and-backfill-prior-epics`
currently call out by hand.

**Open questions:** is this a new `test` run type, or a phase wired into the existing story/review
pipeline? How does generated-test output feed verification (gate a story on its test plan / coverage)?
Which testarch skills become orchestrated vs. stay interactive?

---

## Verification parity in the loop: ATDD proof and scoped verification

**Status:** planned · **Foundation:** the tests config (`waves-tests`, `_waves/tests_memory.toml`)
and its tool `tests_memory.py`, shipped for `waves-core-parallelism` only

The parallelism core gates what it merges with one command: wave 0 records every story's
acceptance scaffolds RED at the base; a story's gate runs the test files it created or changed
plus its acceptance files, under a queue per type of test, and ANY red sends it back; the merge
refuses without a matching green report; the whole tree runs once, at the close. No story ever
falls back to the whole suite, and nothing decides a scope but the owner's config. **The loop has
none of it**, in either of the
modes `waves-master-tui` launches — deterministic (`waves run --deterministic`) or LLM
orchestration (`waves llm-run`, whose orchestrator acts only through the same `waves unit`
verbs):

- **ATDD is fire-and-forget.** `waves-tea` runs `bmad-testarch-atdd` at `pre_dev_phase`, on
  a story's first attempt, `blocking = false`. Nothing afterwards checks that the scaffold
  exists, was red, was un-skipped or turned green — and a test that stays `skip` fails no
  `[verify]` command, so a story can merge with its acceptance tests switched off. The
  orchestrator skill is told, for a failed `atdd`, to "dispatch dev anyway".
- **Verification is `[verify] commands`**: one flat ladder per story — the whole suite per
  story when a project fills it, no deterministic gate at all when it leaves it empty.
- **`--plan` reads only the grid.** `waveplan.py` takes waves, fronts and merge order; wave 0
  "contributes nothing" and the plan's `tests:` / `verify:` blocks are ignored, so the SAME
  approved plan verifies differently depending on which executor runs it.

**The work** — deterministic, in the engine and the `waves unit` verbs, so one
implementation serves both modes (no LLM in the control loop; git through `_run_git`;
transitions only in `statemachine.py`; new task fields are persisted data and need a
compatibility story; `tests_memory.py`'s logic is ported into the package rather than shelled out
to, since a skill payload is not the package's code):

1. **Capture the scaffold.** After the `atdd` workflow, the files it created (untracked, new
   during that session, matching the config's `[[kind]]` globs) are recorded on the
   task and journaled. An empty set means ATDD produced nothing.
2. **Hand it to the dev session**: the list goes into the dev prompt — un-skip these before
   implementing; they must pass.
3. **Green at the end.** Post-session verification runs those files with their kind's command
   and JUnit: every case passed, none skipped — otherwise a fixable verify failure, back to
   dev through the transitions that already exist.
4. **Red for real.** Revert the story's non-test changes to `baseline_commit` (the rollback
   reference the engine already keeps), run the cases — each must FAIL as an assertion —
   restore. A case that passes with the story's code undone does not test the story. In the
   loop this beats a wave-0 record: dev has already un-skipped the cases.
5. **Gated verification.** With the config, the gate's set (the test files the story touched
   plus its acceptance files, one queue per type of test) replaces `[verify] commands` per
   story, a red already there on the story's base still sends it back, and the whole tree runs
   at the epic boundary (`epic`).
6. **`--plan` honors the plan**: the `tests:` block.
7. **LLM mode**: a verb (`waves unit verify atdd --story <key>`), and `waves-core-orchestrator`
   stops saying "dispatch dev anyway".

**Configuration, not rigidity.** Every one of these is a policy setting, editable in the TUI
Settings, with a `core.toml` / `plugin.toml` entry — never hard-coded:

- `atdd_enabled` (exists, `[plugins.waves-tea]`) — generate the scaffold at all;
- `atdd_required` — `off | warn | block`: may a story start when ATDD produced no red test;
- `atdd_proof` — `off | warn | enforce`: the green check (3) and the red check (4);
- the verification source per story — `commands` (today) or the tests config.

The parallelism side reads the SAME settings: they become the defaults of the planner's
question 10/12 and of its Step 6 (today ATDD there is a per-plan answer), so one project gets one ATDD policy
whichever executor runs its stories.

**Open decisions:** a story whose ATDD produced no red test — blocked or warned? A case that
passes with the story's code undone — fail or warn? A project with no tests config — enforcement
off with a `validate` warning pointing at `waves-tests [D]`, or the run refused? Should
`--plan` in the loop honor the plan's `tests:` block (recommended: yes, so one plan verifies
the same in all three executors)?

---

## Integrate BMAD GDS game-test items

**Status:** exploring · **Foundation:** opt-in game-engine layer landed (Unity, shared + per_worktree), now riding the general plugin system

The opt-in Unity plugin (`docs/FEATURES.md` → "Game-engine projects"), enabled with
`[plugins] enabled = ["unity"]`, already lets a Unity project run its dev/sweep cycle against a
live Editor MCP in **shared** mode (agent works in place on the operator's open Editor; a readiness
gate blocks until the Editor + MCP are up) and in **per_worktree** mode (one managed Editor per
worktree, with reflink/CoW `Library` priming, setup/teardown hooks, and MCP-skill seeding via
`seed_globs`). The game-engine layer is no longer bespoke core code — it's a plugin built on the
general [plugin system](plugin-authoring-guide.md) (the legacy `[engine]` block is a deprecated
compatibility shim, folded onto `[plugins.unity]` at load time). Next steps: batchmode `verify_cmd`
and Godot/Unreal plugins on the same `plugin.toml`+scripts shape — the authoring path is documented
in [Writing a Game Engine plugin](game-engine-plugin-guide.md) and
[Writing a plugin for a specific Editor MCP](game-engine-mcp-guide.md).

The BMAD **GDS** module (game dev — Unity / Unreal / Godot) carries its own testing track via the
`gametest` workflow (`_bmad/gds/workflows/gametest`). For game projects, the testarch/TEA pipeline
above doesn't map cleanly; GDS has its own design → technical → production → gametest flow.

The goal is to let waves recognize and drive GDS game-test items the same way it drives
sprint stories and (eventually) retro items, so game projects get the same unattended
implement → test → review loop.

**Open questions:** how do GDS workflow artifacts map onto the orchestrator's sprint-status/work-item
model? Does GDS need its own run type, or can the test-design/automation integration above generalize
to cover it? Depends on the testarch integration landing first.
