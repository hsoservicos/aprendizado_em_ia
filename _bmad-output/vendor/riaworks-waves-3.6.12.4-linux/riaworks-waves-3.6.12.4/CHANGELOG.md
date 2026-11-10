# Changelog

All notable changes to `riaworks-waves` are documented here. Entries written before a
rename name the product as it was spelled at the time — `bmad-loop`, then
`riaworks-bmad-loop`, then `riaworks-loop-llm`, then `riaworks-waves-loop` — and the `1.0.0`
and `2.0.0` entries carry the mapping for the last two. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Releases up to `3.1.0` follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html); from `3.6.12.4` the number is the
waves major followed by the BMAD-METHOD release it requires.

## [Unreleased]

## [3.6.12.4] — 2026-10-15

### Added

- **`waves init` checks the BMAD-METHOD floor before its first write.** Below 6.12.4 it
  prints `FAIL:` with the upgrade command and installs nothing — no policy, hooks, skills or
  gitignore entry; with no readable `_bmad/_config/manifest.yaml` it warns and installs, as
  `validate` does. Every install path runs it: the bundle installers, `waves-setup` and a
  manual `init`.

- **`waves-config`, the configuration's door, and `waves config --json`, its instrument.** A
  waves run reads five kinds of file — the loop policy (adapters per role), the adapter agents
  rendered from it, the tests config, the provisioning recipe, each skill's override layers and
  the watcher's rules — and only three had a door. The skill shows the whole map with its state
  and the door that owns each surface (`[D]`, changes nothing), configures what had no door —
  the adapters per role (`[A]`: one question per role, written into `[adapter.<role>]`, agents
  re-rendered by `waves init`), a skill's customizations key by key in the team or the personal
  layer (`[S]`), the watcher's thresholds and autonomy (`[U]`) — and hands the rest to
  `waves-tests`, `waves-provisioning` and the settings screen. It never writes a sixth file and
  never asks what another door asks. `waves config --json` (schema 1) emits the map: every
  surface's state (present, missing, unreadable, tracked, dirty), the roles resolved the way the
  loop resolves them with the agent each would dispatch, the agents on disk against the
  expected ones (missing, stale, foreign), the tests config's kinds and capacities against the
  provisioning's data isolation, the provision/teardown pair, each override layer's keys
  against what the skill ships, the skill trees' version against the package, and a list of
  findings each naming its door; exit 1 when a finding is a problem, the document still owed.
- **Who runs each role of a wave run — CLI, model, effort — is the owner's, in the loop's own
  policy.** The parallelism master's roles (`story`, `close`, `diagnosis`, `lens`, `repair`,
  `judge`) are adapter stages like the loop's: `[adapter.<role>]` with `name`, `model` and the
  new `effort` (`low|medium|high|xhigh|max`, also at the base `[adapter]`; client-specific like
  `model`, validated at load, editable on the settings screen). A CLI profile says how it takes
  an effort (`effort_args`, with `{effort}`: claude and antigravity `--effort`, codex a config
  override) and where it reads agent definitions (`agents_dir`: claude). `waves init` renders
  the master's adapter agents there — `waves-agent` and one `waves-agent-<effort>` per distinct
  effort the roles resolve to, never one per role: an agent definition fixes what a harness
  takes only from a definition (the effort), says the brief is the whole instruction, and the
  master names the model at dispatch and the role in the brief (MEASURED 2026-10-03: a native
  subagent takes `model` at dispatch and `effort` only from its definition). Generated on every
  init from the policy; a file without the generated marker is the project's and is kept. The
  planner reads the resolution into the plan's `adapters:` block (question 10b, shown and
  confirmed, never guessed) and the master dispatches by it: a role on its own CLI as a native
  subagent, a role on another CLI launched in the role's tree with that CLI's flags. The loop's
  own sessions take the stage's effort at launch the same way.
- **The epic retrospective gate in the LLM loop: `unit retro start|settle`.**
  Upstream 0.13's `[gates] retrospective` existed only in the deterministic engine; a
  run the LLM held neither nudged (`notify`) nor ran (`auto`) a retrospective.
  - `unit retro start <epic>` fires what the policy names: nothing, the engine's
    nudge, or one `/bmad-retrospective -H <epic>` session on `[adapter.retro]`, which
    it dispatches unless one of the engine's refusals applies (`retro-auto-skipped`).
  - `--run-end` adds the engine's run-end refusals for the last epic, which never
    crossed a boundary.
  - `unit retro settle <epic> --task <id>` judges the settled session on disk, as the
    engine does, and commits exactly the board and the retro docs. It surfaces a
    `rejected` verdict and names any leftover dirt with the engine's epic-boundary
    pause reason; the pause itself is the orchestrator's routing.
  - The orchestrator skill fires the gate after the boundary's TEA steps and before
    `finish`.

### Changed

- **BMAD-METHOD 6.12.4 is the floor** (`bmadconfig.BMAD_METHOD_FLOOR`, was 6.12.0). Since
  6.12.4 every BMAD skill reads its config through `_bmad/scripts/resolve_config.py` — the
  four central TOML layers, custom overrides included — instead of the legacy
  `_bmad/bmm/config.yaml`; its installer also writes the user-scope keys' defaults into
  `_bmad/config.toml` and pins the Test Architect module to v1.27.2 (TEA v2 and later install
  only through the BMAD v7 installer). `validate` fails below the floor, `init` installs
  nothing, and `run`, `sweep` and `resume` refuse.
- **The bundled skills read the BMAD config through BMAD's own resolver.**
  `waves-master-parallelism`, `waves-core-parallelism`, `waves-core-sweep` (its fallback),
  `waves-tests` and `waves-config` run `resolve_config.py` instead of reading
  `_bmad/bmm/config.yaml`, so a `_bmad/custom/config.toml` override reaches them as it
  reaches the BMAD skills and the orchestrator.
- **This release is numbered `3.6.12.4`: the waves major, then the BMAD-METHOD release it
  requires.** `scripts/release.py` reads a fourth numeric component as part of the release, as
  PEP 440 does, never as a pre-release suffix, and orders it numerically (`3.6.12.10` above
  `3.6.12.9`); the skill contract accepts a four-part `module_version`.

- **The fork tracks upstream bmad-loop 0.13.1** (from 0.11.1, through 0.12.0). Each tag is
  ported in dependency-ordered commits through `scripts/upstream_merge.py` (namespace applied
  to both upstream sides before each 3-way, function-level merge for modules where whole tests
  moved, an audit that every fork-touched function survived), its merge recorded last.
  Upstream's own sections follow below, under `[0.13.1]`, `[0.13.0]` and `[0.12.0]`. What
  reached this fork's loops from 0.13:
  - **Hooks run the installed `waves relay <Event>` command**, registered by absolute path.
    Re-run `waves init` in each project (finish or abandon its runs first), then open each
    coding CLI once to accept the changed hooks. `init` removes the relay copy an older init
    left at `.waves/loop/waves_hook.py` once no CLI's hook config still runs it; while one
    does (an `init --cli` that named only some CLIs), the copy stays and `init` names the
    `--cli` that would move the rest.
  - **The automatic retrospective** (`[gates] retrospective = "auto"`, on `[adapter.retro]`)
    runs at an epic boundary after the TEA steps and the TEA plugin's boundary commit — so it
    meets the clean tree it requires and reads the `retro-prep` notes — and before the
    per-epic sweep, which then ingests its action items. A `--plan` front's child run leaves
    it to the wave master, which fires it between waves and at its own run end.
  - Session ids are pinned per launch (`session_id_flag`, claude's `--session-id`), so a
    nested CLI's events no longer end the parent session; a resume (`--resume <id>`) pins
    none and accepts the id the resumed session reports.
  - A hard `stop` kills a running verify command's tree (DW-353); this fork's verify queue
    gives up its wait under the same stop, and a `[scm] provision` it cuts short stops the
    run instead of parking the story.
  - `effort` keeps this fork's closed levels and its `effort_args` channel (opencode-http
    gets it as `variant`); `policy.effort-unsupported` warns only for a profile without
    `effort_args`.
  - Under the deterministic engine the deferred-work ledger is no longer tolerated as the
    run's own dirt at a merge: only the LLM loop's `unit ledger` writes it in the main
    checkout, and upstream's DW-354 refusal stands for a task that will commit it.
  - `CLIProfile`'s fork fields (`effort_args`, `agents_dir`, `resume_args`) now follow every
    upstream field, the order an entry-point provider constructing a profile positionally
    relies on.

  From 0.12:
  - Ledger and board writes are serialized across processes (#286/#469), and a run's
    `state.json` read-modify-writes hold one per-run lock (DW-93). The LLM loop's verbs and
    supervisor now take THAT lock (`llm.lock.state_run_lock`), with their 30 s `LockTimeout`,
    instead of a private `<run>/state.lock` nothing else honored — `stop`, `clean` and the
    dashboard could write between a verb's read and its write.
  - Integration receipts, confined no-follow writers, read-only operator files refused
    (#593/#597), ledger reads that degrade or pause instead of crashing (DW-146 family), the
    dev gate's proof-of-work and the review gates' `[verify] commands` on the git root
    (#695/#716), re-arm that refuses what it cannot reopen (#640), `sweep --only`,
    `--min-severity`, `--archive`.
  - Kept the fork's: `tolerate` now feeds `plan_incoming_collisions` (and so the receipt's
    tolerated set); the merge-base incoming diff gains `--no-renames`; the index-lock retry
    carries `reflog_action`; `work_root`/`commands_root` route into the new gates;
    `unit verify commands` goes through `verify.gate_commands_outcome` (the review gates' one
    sanctioned caller) and so runs on the git root.
  - `unit ledger list` reads through the observation arm and reports an unreadable ledger as
    `fault` instead of `[]`; story sessions the verbs dispatch take `engine._session_task_id`
    (a re-armed story's `-g<N>` suffix, #705) and the dev result is read for the current
    generation only.

- **Every tree a run opens, the run gives back.** MEASURED (2026-10-02): three runs on one machine
  left 65 worktrees (26 GB) and seven front stacks (~107 GB of databases) behind, every one of a
  story already merged, because no step of `waves-core-parallelism` gave them back. Now the
  invariant is written where the master reads it: a front's work lives on its branch and its tree
  is disposable; the sidecar carries each front's `worktree` and `branch` the moment the master
  knows them (and `released_at` or `kept` after); THE GIVE-BACK — the stack down by whoever
  brought it up (the front, inside its tree, before `ready-to-merge`; a re-drive provisions
  again), `git worktree remove`, `git branch -d` of the story's branch and never `-D` (the one
  `-D` is for a branch the tree came with, holding nothing of the story) — runs in the turn a
  front's last story leaves the run, on the close's trees, on a dead front's once its substitute
  took over, and `[C]` pays first the give-backs a dead master owed. A front re-driven by a
  session that did not dispatch it continues from its BRANCH in a tree it can work in, never from
  the old tree. The plan names `teardown` beside `provision`, read from the project, never
  invented; without one the stack stays and the run summary names it. How a tree is obtained is
  the harness's and the master's; the skill fixes only what git fixes.
- **The gate names what the run wrote; the front commits it as the story's evidence.** MEASURED
  (2026-10-02, a real browser suite): the project's tests rewrote three tracked files, the gate's
  base re-run refused with "commit first", and the story looped. `gate` and `epic` now list in
  `written` every tracked file the run changed and every file it created that git does not
  ignore, leave the tree as the run left it, and never refuse for it; the base re-run puts what
  the run wrote aside and drops what the old code wrote while detached; `merge` accepts the commit
  that adds exactly `written` on top of the gated one, through a rebase as well, and refuses any
  other difference. The front discipline says it: commit the evidence alone, on top, and report
  that commit — or restore it when the project does not version it. `waves-tests [D]`/`[C]` read
  `git status` after each trial run and settle with the owner what the command writes.
- **The close runs on as many trees as the capacities allow.** MEASURED (2026-10-02): ten kinds
  one after another in one tree, 1h47, on a machine whose config allowed two browser runs at once.
  The master does the arithmetic from the tests config and `[scm] max_parallel`, groups the kinds,
  and dispatches one close subagent per group, each in a tree of its own with a stack of its own,
  running `epic --kind <id> …` with `--report-dir` at the master's gate directory; one tree, every
  kind, is the floor. `epic --kind` (repeatable) runs a subset of the kinds; the report carries
  `kinds` and `written`.
- **The queue has no shortcut, and the cap accelerates nothing.** MEASURED (2026-10-02): a master
  opened four suites at once, blind, to make the run fit its hour cap. Named and forbidden, for
  the master and for the fronts: launching the project's runner by hand, or two runs of a type
  side by side outside the tool. A re-drive fixes and does not rebuild: it reruns, through the
  tool, only the tests that cover the files the fix touches, and the gate once more when done —
  the whole tree runs once, at the close, never for a fix.
- **The tests are the Waves', in three moments, and the owner's config decides them.** A story
  no longer runs a scope its plan or its front chose. Its test rung is ONE command,
  `tests_memory.py gate`: the test files the story created or changed plus its acceptance
  (ATDD) files, run under a queue per type of test. **Any red sends the story back** — one that
  was already red on the story's base too, in a file the story touched, included: the front
  fixes it and documents it in its spec, under the heading the config names, and the command
  checks that it did; an acceptance case has no such excuse. A story that changed
  no test and has no acceptance file passes as `no-tests` and is judged, with the diff, by an
  independent session at the close. The merge is `tests_memory.py merge`, which refuses unless
  a sealed green report matches the commit (the same commit, or after a rebase the same content
  of the story's files). The whole suite runs once, at the close (`tests_memory.py epic`): each
  red is re-run on the commit before the epic and classified — new (traced to the merge that
  broke it), old in a file a story changed, old and untouched — and a merge that did not go
  through the tool turns the close red.
- **`waves-tests` writes a config, not a memory.** `[D]` asks, one question per message: what
  TYPE each set of tests is (unit, integration, API, E2E — defined by what a test uses, never by
  its tool), how many fronts may run each type at the same time (with what each front has of its
  own and what all share, and a default of 1 whenever a resource is shared or unknown), whether a
  story runs what it touched or the whole suite, and whether the close runs the whole suite. It
  writes `_waves/tests_memory.toml`, versioned; the gate reads it from the story's merge-base, so
  a story cannot move it.
- **`tests_memory.py` replaces `memory.py`**: `gate`, `merge`, `epic`, `run`, `record`, `check`;
  the runner's output goes to a log and stdout carries the command, its rc and, on a red, the
  last lines — never the whole output.
  A command that fails and writes no report although one is configured (or that the shell cannot
  find) is class `runner`, not "the story broke it": the front is told to read the log and report
  `blocked`, never to change the project's dependency or build files. The project's commands run
  without the ephemeral environment `uv run` puts first on `PATH`, which would otherwise hide the
  project's own interpreter. Reports are sealed (HMAC, a key of the machine) and hash their logs, so a
  green typed by hand is refused by `merge`.
- The plan no longer carries a scope: `tests.verify` (scope modes, `max_candidates`,
  `flaky_reruns`, `queue_commands`), `tests.baseline` and `on_uncovered` are gone; it carries
  `tests.config_file` and `tests.memory_dir`, and a plan without the first does not run. The lock
  root default is `.waves/tests.lock`.
- **The gate trusts the record, not the front, on four points it used to take from prose.**
  Measured on a real gate with a real runner before the fix: an acceptance scaffold left in `skip`
  passed as GREEN, and a story that deleted its only test and broke the code passed as `no-tests`.
  Now: **the acceptance files come from wave 0's record** at the merge-base, and every case in it
  must PASS at the gate — `skipped`, missing or red is class `atdd` (`--atdd` only adds files),
  matched by `(test file, case name)` because a runner's dotted class prefix changes between the
  checkout where wave 0 recorded and the worktree where the gate runs (measured on a real runner);
  **a test file the story deleted** (not moved — renames are followed) is class `deleted`, owed to
  the spec under its own heading until the section names it; **`merge --branch <the front's branch>`**
  refuses when the branch's tip is not `--head`, so the master cannot merge an older, gated commit
  when the front moved on (the s5 case of the real run, which prose alone did not stop); and the
  `owed` entries carry their class (`{file, class}`).
- **The spec headings are the owner's, in the project's language:** `[spec] preexisting_heading` and
  `deleted_heading` in `tests_memory.toml`, asked by `waves-tests [D]` (question 5) and read from the
  story's merge-base; the tool's defaults are `Pre-existing reds fixed` and `Test files removed`, the
  gate prints the heading it expects with every red that owes one, and `check` refuses empty or
  identical headings. No skill spells a heading out any more (contract-tested).
- **A machine may lower a type's capacity, never raise it:** `[tests.capacity] <type> = n` in the
  machine's `.waves/loop/policy.toml`; the queue uses the smaller of the project's number and the
  machine's.
- `run` prints how long each command took, and `waves-tests [D]` (Phase 3) and `[C]` recommend
  `each = true` for a kind whose run takes a real share of the budget the plan gives the test rung:
  a runner writes its report at the END of an invocation, so a cut loses every case of that
  invocation — a red included (measured with a real runner); one invocation per file loses only the
  file the cut fell on.
- **A rung cut by its budget is `inconclusive`, and the story goes through on what did run — in
  the open.** `gate --budget <seconds>` (and `run --budget`) makes the tool cut the runner at the
  rung's budget of running time (queue waits and the tool's own base re-runs do not count) and
  write a SEALED report with verdict `inconclusive`: the units it cut are class `clock`, every
  case that did run is listed, and `inconclusive` is never green. `merge` refuses it unless the
  master says `--accept-inconclusive` — refused all the same when anything red is among what ran
  — and records the acceptance (`inconclusive`, `cut`) in the registry; `epic` lists those stories
  as `inconclusive_merges`, and the close's whole suite is their first complete measurement. The
  core's ladder says so (the owner's rule: the story is not at fault for the infrastructure's
  clock; a debt written is not a story out of the run), the brief carries `<GATE BUDGET>` from the
  plan's `clock_budgets`, and the front knows `INCONCLUSIVE` is neither red nor green.
- **"No browser" is resolved where the owner is, never discovered by the run.** The planner's
  visual-acceptance question now PROBES the harness's browser tool for real before asking (a page
  opened, its title read) and opens with the result; absent, the owner installs it now (re-probe),
  waives visual capture (pending approval → `waived-by-owner`), or takes the UI stories out of
  the plan's scope — the option that left them "not dispatched until one is installed" is gone.
  The dispatch decision (the boot) probes once more and never hands over `browser-required` with
  no browser. The master's pre-flight check becomes a confirmation, and a browser gone mid-run is
  the ENVIRONMENT's failure: the UI story is deferred with an `infra-debt` line and the run goes on.
- **Nothing waits for the owner during a run.** The master's doctrine loses its one exit that
  did — "park the story `awaiting-owner`" — everywhere it appeared: a contract gap is built or
  DEFERRED (the owner's question written in the ledger and the sidecar decision, the story's
  consumers deferred with it, the wave closes without them), the clock's inconclusive rung and
  the missing browser tool defer the same way, and whatever falls outside the verbs and the
  rules is documented in the ledger and the run continues. The reading tokens stay: an older
  sidecar's `parked:` list is read as deferred entries, never written; the plan's
  `contract_gap_policy` becomes `ledger-then-build-or-defer` and a plan on disk with the old
  value runs unchanged. Heartbeat, resume and status lines count `deferred` instead of `parked`.
  The owner's rule: a story parked for an answer is a producer its consumers wait for, and an
  exit that waits is the one a cautious master reaches for.
- **An acceptance case that contradicts its story's text is an ATDD DEFECT, never a story out
  of the run.** The core's resolution ladder gains a route between "execution detail" and "contract
  gap": precedence is fixed (the approved story text over the case wave 0 derived from it), the
  master writes the ledger line (`kind: atdd-defect`) and dispatches a REPAIR subagent — not the
  story's front, never its own hand — that rewrites the case to the text, re-records it red at
  the base and commits both on the integration branch; the front is re-driven on a rebase and its
  consumers wait for the re-drive, not for the owner. The front's `blocked` line gains the value
  `atdd` for exactly this, and the discipline forbids the front from resolving the contradiction
  in either direction. Measured with a real master BEFORE the rule: given only the old ladder,
  it did not park — it decided by the same precedence on its own, had a subagent correct the
  case and re-record, and re-drove the story; what it lacked was the route in writing (the
  ledger said `detail`, nothing was committed on the integration branch, and the text pointed
  every `blocked` at the contract-gap exits, one of which parks a producer its consumers wait
  for).
- `capacity = "all"` is now a value the config accepts — no queue for that type — matching the
  `[C] all` answer `waves-tests [D]` already offered and the format could not spell; a machine's
  `[tests.capacity]` still lowers it.
- **Runners that take one path per call, and globs that overlap.** A kind may say `each = true`:
  one invocation per file even with a report. `run` warns when a file it handed the runner came
  back with no case, and `waves-tests [D]` Phase 3 now tries TWO files per kind, which is how such
  a runner is found. `check` warns when a file at HEAD matches more than one kind (the first wins
  silently — before, only two identical glob strings were noticed).
- **The base re-run takes its queue slot before it detaches the worktree**, so the front's tree is
  off its branch only while the old code runs, never while it waits; the gate log says
  `=== base re-run: HEAD detached at …` and `=== restored … ===`, and the core's watch knows what a
  worktree showing the merge-base during the gate rung means.
- **uv's ephemeral environment is recognised by what every launch shares** — `UV_RUN_RECURSION_DEPTH`
  set, `VIRTUAL_ENV` equal to this interpreter's prefix, and that prefix outside the repository —
  instead of by the name uv gives its cache directory today. A project's own environment the tool
  was started from stays on `PATH`.

### Removed

- The verification memory's machinery: `affected`, `prove`, `baseline`, `classify`, `cases`,
  `replay`, the file→test `rules/`, `known-reds.toml`, `[[file_class]]`, seed rules, and the
  wave-0 baseline pass (the whole suite no longer runs before the stories).
- `suite-queue.sh` and its `suite_queue_script` key: the queue is per type of test, inside the
  tests tool. `suite-wait.sh` stays, and now tells a command queued for its next slot from one
  running.

### Fixed

- The tests gate no longer asks old code questions against state the new code left. To class a
  red (the story's base, the commit before the epic) and to trace it to a story (the close's
  bisection), `tests_memory.py` checks older code out and runs the test again; a checkout moves
  the code and nothing else. A kind whose tests read state outside the tree that the code moves
  forward — a schema the code migrates, data or an artifact it generates — had its regressions
  classed as old reds and its bisection pinned on the wrong story (MEASURED 2026-10-04, at an
  epic close after stories that migrated a database). Two optional `[[kind]]` keys:
  - `state_rebuild = "<command>"`: the project's command that rebuilds that state from the tree
    as it stands. It runs under the kind's slot after every move to an older commit and once
    after the branch is back; the journal carries it, so a kill mid-bisection is rebuilt by the
    next run, which refuses to measure until it passes. A failed rebuild after the restore is a
    failed restore (exit 3).
  - `outside_state = true` alone: the state exists and nothing rebuilds it. The kind is never
    compared with older code; its reds are `unattributed`, blocking, with a `reason`, and the
    master's diagnosis names the story.

  A bisection now holds one slot and one detached stretch per kind, restoring once at the end,
  not once per step. `waves-tests [D]` reads the state and asks (question 6), tries the rebuild
  with the owner's yes, and `[C]` flags a kind that reads such state and declares nothing.

- `waves validate` reports a broken plugin manifest once (`plugins.manifests`, upstream 0.13)
  instead of twice; the fork's `plugins.load` check id is gone, and the `[plugins] enabled`
  name check no longer lets a skipped manifest's warning reach stderr past `--json`.
- Exact-path publication (the sweep's ledger commits) works on git 2.34, the supported floor:
  `symbolic-ref --no-recurse` is younger than that, so every bound publication failed as
  "branch identity could not be validated". The option is probed once; without it the first
  hop is read off HEAD's own file. Upstream still asks for the option unconditionally.
- The wave master lands a rebased unit, not its pre-rebase commit: integration now merges
  the task's recorded commit, and `rebase_unit` records the rebased tip the ladder re-verifies.
- `waves run --resume` of an LLM-held run re-reads and publishes its state under the run lock,
  so a stop or pause written meanwhile is no longer overwritten.
- `waves run --spec` without `--deterministic` refuses in ASCII (a strict-ASCII stderr raised).
- A verify ladder whose cwd carries a NUL reports a spawn fault per command instead of the
  suite-queue probe crashing first.
- `decisions --answer` reports a written answer git could not commit instead of dropping the
  error, falling back to one commit per file when the batch's single commit fails.
- LLM loop: a `dev` or `review` dispatch always runs the dev primitive. The orchestrator's
  prompt file becomes its intent (`/<primitive> <story> — <text>`) unless it already starts
  with that invocation; a resume, triage and workflow sessions are unchanged. A free-form dev
  prompt got code with no spec, review or result, idled through its stall grace and failed
  `unit verify dev`.
- LLM loop: a finished or stopped run kills its `waves-<id>` session under
  `[adapter] cleanup_session_on_finish`, as the engine does; a paused one keeps it for the
  resume.
- LLM loop: `unit` verbs without `--run` address the run their session was launched for
  (`WAVES_RUN_DIR`), not the project's newest run — another run started in the same project
  (a deterministic run, a sweep, a wave master's child) no longer takes the orchestrator's
  calls. A session run outside the given `--project` is refused.
- LLM loop: the orchestrator's prompt names this installation's own `waves` for the verbs
  (`verbs:` line, resolved like the hook relay, independent of PATH); a bare `waves` from the
  session shell's PATH could reach another installation.
- LLM loop: each launched dev or review session is charged to its story (`attempt`,
  `review_cycle`), and a settled session's record carries its adapter and model — the
  dashboard showed `agent -` and `dev ×0` / `review ×0`, and `unit state` answered
  `attempt: 0`.
- LLM loop: an orchestrator turn completes on its own Stop. It ran on dev's shared
  adapter, which completes only when a new dev spec appears, so a turn that
  dispatched no dev — a retrospective-only run end — waited out the whole stall
  grace after `unit finish`. The turn now runs on its own result-file adapter, and
  its prompt ends with the completion signal (`tasks/<task_id>/result.json`).
- LLM loop: `unit rollback --preserve` parks each attempt under the engine's
  `attempt-preserve/<run>-<tip8>` name; the old per-story name was force-moved by the next
  preserved rollback of the same story.
- Skills: `waves-core-parallelism`, `waves-tests` and `waves-config` had invalid YAML
  frontmatter. Codex refused to load them, so the core skill was invisible to a Codex
  master. A contract test now parses every bundled skill's frontmatter strictly.
- Parallelism: the epic close is always a dispatch on `adapters.close`, the floor case
  included. A claude master had run it in its own shell, so the CLI the owner put on
  `close` never ran.
- Parallelism: a role on another CLI is launched by a literal argv from that CLI's
  profile. The new `headless_args` field holds the profile's non-interactive mode
  (claude `-p`, codex `exec`); `waves config --json` gives each `policy.roles` entry its
  `launch`; the planner copies it into `adapters:`, and the master runs it verbatim with
  the brief on stdin. An entry without one is a named failure, never an improvised command.
  `agent` is now `none` for a CLI that reads no agent definitions.
- Parallelism: the master flips `epic-<n>: done` for each epic that closed, matching the
  board's own definition. Two masters on one plan had disagreed.
- Parallelism: with the ATDD skill not installed, question 10 of the planner defaults to no
  ATDD, and `atdd: wave-0|none` is part of the plan contract. A headless plan had promised a
  wave 0 nothing could run.
- Codex under `isolation = "worktree"` no longer pauses once per unit. Upstream's gate
  (DW-341) escalated every new worktree, because Codex keeps hook trust per directory. A
  worktree now inherits the main checkout's grant when that grant is trusted, the hook
  config is identical, and the binary knows `--dangerously-bypass-hook-trust`. The session
  launches with the profile's new `hook_trust_bypass_args` for that one invocation, and
  nothing is written to Codex's trust state. The engine gate and the LLM loop apply the same
  check (`codex_trust.worktree_launch_trust`). The LLM loop, which had no gate, now refuses a
  worktree session Codex neither trusts nor lets inherit. `validate` passes and says so.

## [3.1.0] — 2026-09-28

### Added

- **`waves-tests`: the verification memory, versioned in the project.** A new bundled
  skill and a door run once per project. `[D]` reads how the project runs each kind of test
  and writes `_waves/tests/memory.toml` with the owner: a command per test kind (with the
  runner's JUnit option), the whole-tree command, the files that need other evidence
  (`skip`, `close_only`, `no_test` with a reason) and seed rules from source areas to tests.
  It tries every command on a real test and measures, with `replay`, how much of the last
  deliveries the memory covers; `[C]` checks it against today's tree. It does not replace
  the Test Architect skills — `bmad-testarch-atdd` still writes wave 0's scaffolds and the
  trace/test-review pair still reports at the close — it adds what they do not do.
- **`memory.py`, the memory's instrument** (`waves-tests/assets/`, stdlib Python run through
  `uv`, no language knowledge: git, the project's own commands, JUnit XML). `affected` gives
  every file of a diff a class and the literal commands that verify it, reading the ruler
  from the merge-base so a story cannot move it; `prove` undoes one changed file, runs the
  candidate tests, restores it and runs them again — a case that fails as an assertion undone
  and passes restored reaches the file (an error of loading does not count), with a journal
  that restores the tree after a killed run and a sabotage-patch mode for refactors;
  `record`, `baseline`, `classify`, `cases`, `replay` and `check` complete it. Proofs are
  matched to a story's commit by the proven file's content, so a story may commit its rule
  and rebase after proving.
- **`_waves/custom/`: the `waves-*` skills' own customization, beside `_bmad/` and not in
  it.** `waves-master-parallelism`, `waves-core-parallelism` and `waves-tests` each ship
  `assets/resolve_customization.py` (byte-identical copies) and resolve
  `customize.toml` → `_waves/custom/<skill>.toml` (team, versioned) →
  `_waves/custom/<skill>.user.toml` (personal; `init` gitignores it) with the BMAD Method's
  own merge rules. Every exit code has an action in the skill's Step 1: a broken layer stops
  the skill naming the file instead of being hand-merged, and a team layer left at the old
  location stops it with the `git mv` to run — running on the shipped defaults would drop the
  team's settings without a word. `validate` reports leftovers as `customize.location`.

### Changed

- **`waves init` moves the `waves-*` skills' team overrides from `_bmad/custom/` to
  `_waves/custom/`** and prints `commit the move`; a destination that exists is never
  overwritten (both files stay, "merge by hand"), and the personal `.user.toml` layer is
  never touched. This shrinks what the tool does inside `_bmad/`: the TEA-managed facts are
  the only files it still writes there. The move retires in 4.0
  (`namespace.OVERRIDES_MOVE_RETIRES_IN`).
- **A story never falls back to the whole suite.** MEASURED in a real run (2026-09-28): the
  static rule map in the plan sent seven stories of eleven to the whole-suite fallback —
  25–30 minutes of queue each, one out-of-memory with no summary, two hours proving reds that
  were not the story's — and learned nothing, since the map lived in a plan no later run
  reads. Now a file nothing covers is PROVEN by its front against the memory and its rule is
  committed with the story (the next wave inherits it by checkout, the next run by the
  branch); a file no proof reaches is a `scope-gap` ledger line judged by the close. The
  master runs `affected` itself at the merge gate. The whole tree runs twice per run: wave 0's
  baseline, which IS the wave-0 gate's pass and writes the run's `known-reds.toml` — excluded
  from every green check of that run — and the close. Wave 0 also records each story's
  acceptance scaffolds RED at the base, so "seen red, turned green" is checked instead of
  asserted. The scope ladder gains `waves-tests` as its first rung; `whole-tree` exists only
  as a mode the owner chose for a suite measured fast. Question 6b now defaults to building
  the memory. `[E]` refuses a plan with no `tests.verify.scope` (`[A]` resolves it); `[C]` of
  a run already in flight keeps its contract minus the fallback.

### Removed

- **The 1.x compatibility layer, on the date it set for itself (`LEGACY_RETIRES_IN =
"3.1"`).** Gone: the `riaworks-waves-loop` command alias and its entry point; the
  `RIAWORKS_WAVES_LOOP_*` double export into every session and plugin hook, and both relays'
  reading of that spelling — the copied `waves_hook.py` changes, so `validate` reports it
  stale until `waves init` refreshes it; the read-only listing of runs under
  `.riaworks-waves/` and the refusal to drive one; `init`'s migration of `.riaworks-waves/`,
  of the old relay's registrations, of the old-named skill directories (the 1.x names, the
  2.0 names and the first 3.0 cut) and of old-named `_bmad/custom` overrides; the
  `namespace.legacy` finding of `validate`; and the pointer from the 1.x plugin name
  `riaworks-waves-tea` to `waves-tea` — an enabled plugin nothing answers to is still
  reported, without a successor, and the `plugins.unknown` finding's detail no longer
  carries `renamed_to`. A project still on 1.x or on the 2.0 skill names upgrades through a
  3.0.x release first, whose `init` performs the migration, then to this one.
- **`verify.scope.fallback`.** A plan written before this release that still carries it is
  read without it: the key is not a rung, whatever command it names. The front-discipline
  slot `<FALLBACK>` is replaced by `<PROOF>`, `<MEMORY DIR>`, `<CANDIDATE CAP>` and
  `<ATDD SET>`.

### Fixed

- The root CI's suite-queue smoke pointed at `waves-master-parallelism/assets/`, where the
  script never lived; both CIs now also smoke the resolver and `memory.py`.

## [3.0.0] — 2026-09-25

### Added

- **A bundle distribution: install with no Git remote, no index and no credential
  (`scripts/build-dist.py --bundle`).** A third artifact beside the skills-only zip and sh
  self-installer, and the only one carrying the Python side: the orchestrator wheel (which
  bundles the skills), the module tree the BMAD installer reads, `INSTALL.md`, and two
  installers that do **both levels** in one idempotent run — `install.sh` (Linux/macOS/WSL)
  and `install.ps1` (native Windows). Machine level is `uv tool install <wheel>[tui]` into
  uv's managed tool environment; project level is `waves init` + `waves validate`.
  `--tool-only`/`--project-only` split them, `--cli` is repeatable, `--via-bmad` also
  registers the module with `npx bmad-method install --custom-source`, and `--find-links`
  resolves dependencies from a local wheel directory (implying `--offline`).
  **Prerequisites are installed, not demanded** — the machine a student is handed has none
  of them: uv comes from the publisher's own installer, python 3.11+ through uv, git and
  tmux through the system package manager, and on native Windows psmux from its GitHub
  release (the source this repository's CI uses) plus pwsh through winget, each bounded by
  a timeout because an unbounded fetch hangs with no status to react to. What needs
  privilege and cannot get it is reported with the exact command while the install carries
  on; `--no-bootstrap` / `-NoBootstrap` turns the bootstrap off. `uv tool install` is given
  `--python ">=3.11"`: without it uv resolves against the system default interpreter and
  refuses outright on a host whose python predates the wheel's floor. The installers
  The target project is confirmed before anything is installed — the current directory is
  the default, the prompt says whether a `_bmad/` is there, the bundle's own directory is
  refused (the slip that otherwise leaves the skills beside the installer, silently), the
  home directory is refused too (there `.claude/` is the coding CLI's GLOBAL config, so a
  wrong Enter registers the relay for every project the user will ever open), a directory
  that is neither a BMAD project nor a git repository offers no Enter default at all, and a
  run with no terminal to ask on stops for `--project` instead of guessing. The installers
  detect an existing project install and pass `--force-skills` themselves, so an upgrade
  never leaves yesterday's skill prose against today's tool, and they wire the project with
  the binary uv just wrote rather than whatever `waves` the `PATH` resolves to. The wheel is
  built with `SOURCE_DATE_EPOCH` pinned, so the bundle is byte-identical on a rebuild like
  the other two artifacts. `install.sh`, `install.ps1` and `INSTALL.md` live in
  `scripts/bundle/` as real files, with `@VERSION@`/`@WHEEL@`/`@PKG_DIR@` substituted at
  build time.

- **`waves run --plan <file>` — a wave plan as the run's scope.** The first phase of the
  roadmap's "Parallel unit execution": the approved plan `waves-master-parallelism` writes
  (`epic-<N>-plan-<stamp>.md`, its final YAML block) becomes the run's story set — any
  epics, since the plan's unit is the story — dispatched one at a time in the plan's order:
  wave by wave, fronts in the grid's `merge_order`, stories as each front lists them, so a
  later wave never starts before an earlier one. Waves already merged (`merged: true`,
  below `next_wave`, a front with `merged_in`) contribute nothing. Refused: beside
  `--epic`/`--story`/`--spec`; a `draft` plan or one with `pending_approval` (the door's
  `[A]` answers those); a plan measured against a branch other than the one the run merges
  into; a story the sprint status lacks. Both loops read one record: `RunState.plan`
  (`waveplan.WavePlan.to_dict`, with the derived `story_order`), which `resume` rebuilds
  the selector from; `unit pick` follows it and names each story's wave and front; the
  orchestrator's digest states it; `--dry-run` prints the schedule with wave and front.
  `sprintstatus.StorySelector.order` / `select_actionable(order=)` / `next_in_order` are
  the selector's side of it.

- **Fan-out in the LLM loop: a `--plan` run's wave runs its fronts in parallel, under
  `[scm] max_parallel`.** Phase 2 of the same roadmap item. `unit pick` in a `--plan` run
  keeps the plan's wave discipline — a story of a later wave is never offered while the
  current wave has a story in flight, a front holds one story at a time — and caps the
  stories in flight at `max_parallel`, which is live now (it used to clamp to `1`).
  `unit pick --wave` answers the whole current wave: each front, what it is working on,
  what it would take next, the stories dispatchable now within the cap and the ones
  waiting for capacity. `unit await <id> <id> …` returns when the FIRST of several
  sessions ends (one id keeps every condition). The orchestrator's doctrine gains the
  wave loop; the supervisor and the turn classification do not change.

- **Merge-back in a `--plan` run follows the grid, and only verified code lands.** Phase 3
  of the same item. `unit close` refuses, before the terminal move, a story whose front
  comes after a front still in flight in its wave's `merge_order` (naming the front and
  story to await; a deferred or escalated front counts as settled), and a story whose
  unit branch is behind the target because an earlier front merged. `unit rebase
<story-key>` is the rebase-and-reverify path: it rebases the unit branch onto the target
  in its own worktree (`WorktreeFlow.rebase_unit`, `verify.rebase_onto`) and answers
  `rebased: true` or the conflicting paths with the rebase already aborted and the tree
  clean; `StoryTask.rebases` counts the attempts and `StoryTask.integrated` records that
  a unit landed (a DONE story with a mounted worktree is still in flight until then).
  `unit-merged` carries the grid position (`plan: {wave, front, branch}`); `unit-rebased`
  / `unit-rebase-conflict` are new journal kinds. Outside a plan run nothing changes.

- **The provisioning contract: the run owns when a unit's stack exists.** Phase 4 of the
  same item. `[scm] provision` is a shell command the run executes in the unit's worktree
  right after it is mounted and seeded, before any session, with the run's coordinates in
  the environment (`WAVES_STORY_KEY`, `WAVES_WORKTREE`, `WAVES_BRANCH`,
  `WAVES_TARGET_BRANCH`, `WAVES_RUN_DIR`, `WAVES_EPIC`; `WAVES_WAVE` / `WAVES_FRONT` in a
  `--plan` run). A failure parks the story before a session is spent: the deterministic
  engine escalates with the worktree mounted for inspection, `unit open` answers `env` and
  leaves the story open for the orchestrator to repair or close. `[scm] teardown` runs when
  the unit leaves the run — after integration, after a deferred or failed close — best
  effort, journaled, never blocking; a paused story keeps its stack until it closes.
  `provision_timeout_s` bounds both; `isolated_data` is the recipe's declaration of a
  stack-per-unit that `[verify] concurrency = "parallel"` will require. Journal kinds
  `unit-provisioned`, `unit-provision-failed`, `unit-torn-down`, `unit-teardown-failed`.
  Both commands go through the hook bus's operator-command transport
  (`plugins.bus.run_operator_command`), so a timeout or a missing interpreter is a fact,
  not a crash; the plugin stages `post_worktree_setup` / `pre_worktree_teardown` remain the
  plugin-owned alternative. A story that never started (no session) may now `close` to
  `defer` or `escalate` straight from `pending`, so a failed provision is not a dead end.
  Until now projects provisioned LLM-side, per story, and only the session's memory tore
  the stack down. `waves-provisioning` is the contract's author, a new bundled skill and a
  door run once per project: it reads the tree (manifests, compose files, env templates,
  the migration tool, the test resources), asks the owner one numbered question at a time
  (data isolation, services, environment file, dependencies, give-back, capacity), writes
  `scripts/waves-front.sh` from its template with an idempotent `up` / tolerant `down`,
  sets the `[scm]` keys and `worktree_seed`, leaves a `<project>-provisioning` consult
  skill for the sessions, and tries the recipe on a scratch worktree before handing over;
  `[C]` checks an existing recipe against the tree.

- **Two knobs, not one: `[scm] max_parallel` bounds sessions, `[verify] concurrency`
  bounds the suite.** Phase 5 of the same item. `concurrency = "queue"` (the default) holds
  one project-wide lock around the whole verify ladder — under the repository's common git
  dir, shared by every worktree, so the engine's units, an LLM run's `unit verify`,
  `resolve --reverify` and the TEA plugin's boundary pass all wait on one queue — because
  two suites on one database corrupt each other; it is what the parallelism skills'
  `suite-queue.sh` did, moved into the engine. `"parallel"` drops the lock and is refused by
  the policy unless `[scm] isolated_data = true` declares a stack per unit. Capacity is the
  operator's call, per machine.

- **The dashboard reads a `--plan` run.** Phase 6 of the same item. The run header gains a
  plan line — `plan <scope> · wave n/total · in flight k · merged k · waiting k` — and,
  while the current wave has stories in flight, a `merge queue:` line in the grid's merge
  order (`✓` ready to land, `…` still working); the tasks table gains a `wave` column with
  each story's grid position (`w2·B`). Both read `waveplan.progress` / `waveplan.tag` off
  the run's own state, and "in flight" is `StoryTask.settled`'s reading — a DONE story with
  a mounted worktree is still in flight until it lands — the same the orchestrator's `pick
--wave` and `close` use, so the panel and the loop never disagree about a wave.

- **The deterministic engine drives a wave: the wave master.** Phase 7 of the same item,
  the last. A `--plan` run under worktree isolation with `[scm] max_parallel > 1` launches
  one child run per front of the current wave (`waves run --deterministic --plan … --front
<name> --wave <n> --parent <run>`), at most `max_parallel` at a time; each child is the
  ordinary engine driving its front's stories in order — provisioning, the verify queue,
  the whole pipeline — with one difference: it HOLDS integration, leaving every DONE unit on
  its branch with the worktree mounted (`unit-held`; the end-of-run worktree gc spares
  them). The master then adopts the children's tasks into its own state (`story-adopted`),
  lands them in the grid's `merge_order` — a unit the target moved past is rebased and the
  verify ladder runs again on the rebased tree before it merges; a rebase conflict confined
  to the sprint board and the deferred-work ledger takes the target's version and goes on,
  because those ride the post-merge carry, never the merge — parks a unit whose rebase
  conflicts or whose ladder goes red (deferred with the reason, branch kept,
  `story-parked`), fires epic boundaries toward a later epic after the wave, and pauses a
  wave that made no progress (`wave-stalled`) rather than relaunching it forever.
  `plan_children` in the master's state maps `w<wave>:<front>` to the child run id, so a
  resume re-adopts a finished child instead of relaunching it; a stop on the master is
  forwarded to its live children in the same mode. Fan-out is by process rather than by
  thread because the engine's `workspace` is one per process by construction; the child
  runner is a seam, and the simulations drive a two-front wave in one process — landed in
  grid order with A rebased behind B, and a same-line conflict parked with B landed. With
  this the roadmap item "Parallel unit execution" is complete: the plan is written in the
  door, executed by either loop, and shown by the dashboard.

- **Two new assets of `waves-core-parallelism`: `assets/suite-wait.sh` and
  `assets/front-discipline.md`** (`{workflow.suite_wait_script}`,
  `{workflow.suite_wait_budget_seconds}`, `{workflow.front_discipline_asset}`). The wait is a
  BOUNDED, returning wait for the queue's marker, and its exit code is the whole instruction:
  `0` green · `1` red (the suite's own rc travels in the printed tail, never encoded — `75` is
  reserved) · `75` still running, call it again in the same turn · `3` NO-PROGRESS, the queue
  process is gone, relaunch it. Given a liveness file it declares the front's liveness on every
  cycle as `suite queued|running`, so a front sitting in another front's lock never has to
  choose between waiting and looking alive. The discipline asset is the front's six sections in
  copy-ready form, with `<SLOTS>` the master fills; the brief now COPIES it instead of retyping
  it. Both are POSIX `sh` / plain Markdown, project-agnostic, and exercised by running them
  (`tests/test_suite_queue_scripts.py`, including a contended two-front queue).

- **A run can have a master worktree of its own, so several plans execute on one machine at
  once — `ONE MASTER PER INTEGRATION DOMAIN` replaces `ONE MASTER PER PROJECT AT A TIME`.**
  The domain is the three resources that must be single: the integration branch the grid
  merges into, the tracker as it exists on that branch, and the suite lock at its declared
  scope. Two masters that share none of them are concurrent runs; sharing any one is
  corruption (the same branch merged twice, the same tracker key flipped twice, a front
  rebased onto another run's half-merged state), and the executor's pre-flight HALTS naming
  what is shared — same `integration_branch`, a story both plans own, a different
  `suite_lock.scope`, or a workspace another run already holds. The rule had said "per
  project" while the practice on the reference machine was already five isolated masters at
  once: the skill forbade in writing what the owner did in fact.
  - **The door asks the topology FIRST** (`waves-master-parallelism`, questions `1/12` and
    `2/12`, with `1b` on a name collision), because how many fronts fit, where the suite
    queues and which branch the grid merges into all hang off it. Question 1 offers a run's
    own worktree named `{workflow.master_worktree_prefix}<scope slug>` (default), the active
    worktree, or a name of the owner's; a collision is resolved ONCE, with what was found
    (branch, clean/dirty, commits the base lacks) in the question, and a worktree holding a
    LIVE run is never offered — it is named as that run's. Scope disjointness against every
    live run is checked on the spot and an intersection REFUSES the plan.
  - **Question 2 carries its measurement**: usable cores (`getconf _NPROCESSORS_ONLN`),
    `[scm] isolated_data` read from the project's `policy.toml` (the key `waves-provisioning`
    writes; absent, false or unreadable all count as false — a recipe that isolates but never
    declared it gets the conservative scope and the remedy, because the question reads
    contracts and not intentions), how many masters are live, and
    the arithmetic `cores / {workflow.suite_cores_per_run}` = concurrent suites this machine
    serves. Lock at the project (serialized between masters) or per master (parallel
    suites); the recommendation follows the measurement and the owner decides. Two answers
    the skill refuses to carry out and writes the remedy for instead: a per-master lock
    without isolated data (ships `project` + an `open_questions` line naming
    `waves-provisioning`), and unmeasurable cores (ships `project`, and says the measurement
    was not possible rather than inventing a number).
  - **The plan carries it to the executor** — `master_workspace:` (`mode`, `name`, `path`,
    `branch`, `base`, `reuse: new|updated|recreated`, `seed[]`) and `suite_lock:` (`scope`,
    `dir`, `measured`) — and the sidecar mirrors both, so `[C]` learns which tree the run
    lives in instead of resuming against the wrong repository. `seed[]` exists because a run
    whose configuration, skills or environment files are gitignored has none of them in a
    fresh worktree.
  - **Resolved in the door, created in the executor.** The planner reads git and settles the
    name with the owner; it creates, updates and removes no worktree and no branch. The
    executor's pre-flight does that first, before any other check, then commits the plan onto
    the run's own branch as its first commit — the branch carries its own contract, and a
    `[C]` from a session that saw nothing finds it there. A state on disk that contradicts the
    plan is a halt pointing at `waves-master-parallelism [A]`, never a collision resolved
    mid-run.
  - **A run has TWO roots now**, and the mechanical trap is named in the Conventions:
    `{project-root}` is the tree the run works in, `{main-checkout}` is git's own answer
    (`dirname` of `--git-common-dir`) for what must be single for the MACHINE. A
    `project`-scoped lock resolved against a worktree is a per-master lock by accident.
  - An isolated run ends on its own green branch and says so: the union with the project's
    branch is the owner's step, because a master that landed it would be merging work a
    second master is still rebasing onto. `[P]` in `-H/--headless` names the worktree
    `<prefix><scope>-{stamp}`, which no earlier run can own, and adopts or removes nothing
    without a human.

- **The master's watch is ONE CLOCK, and the clock is a shipped script with a lock
  (`assets/watch-tick.sh`, `{workflow.watch_tick_script}`, `{workflow.watch_tick_lock_dir}`).**
  MEASURED 2026-09-18: the master armed a watch timer, a notification from an OLDER timer
  arrived, it read that as "time to tick" and armed another — and every extra timer multiplies
  the next round: 1, 2, 4, seven live timers in three rounds, several wake-ups per window, the
  owner's terminal full of duplicate heartbeats. The gap was an ASYMMETRY, and a measurable
  one: the front's waiting discipline is a six-section asset plus three `<action>` blocks, two
  scripts and four keys, and all six occurrences of "wake"/"notification" in the skill were
  about the front; the master's own watch was one parenthesis ("own timer — the harness's
  scheduling when available"). The sentence beside it had already found the right shape for the
  wrong sibling — "the heartbeat is NOT a process: it is a line it emits per turn" — and its
  counterpart was never written: the tick is not a memory, it is a lock.
  - **Both halves are guarded now.** `arm` refuses while a tick is pending (exit `75`), which
    is what stops the multiplication; `claim` answers whether a wake-up IS the round (`0`,
    and the tick is consumed) or an echo to DROP with no probe, no sidecar rewrite and no
    heartbeat line (`75`), or that no clock is running at all (`3`). A lock alone would have
    left one clock and N rounds per window, which is the same defect quieter — the duplicate
    heartbeats were the answering half.
  - **The tick's identity is a DEADLINE, not a process.** A live pid is honest proof for the
    suite queue, whose owner runs for the whole wait; a tick usually has NO process (it is the
    harness's scheduler), and where it has one it is the untracked background process a front
    is forbidden to depend on. A pid test would report "dead owner" on every check, break the
    lock every time and hand the storm back wearing a fix. The skill already said why, three
    paragraphs below, for the fronts: absence of a process does not prove death.
  - **The lock is PER RUN**, always under the master's own worktree, never under
    `{main-checkout}` and whatever `suite_lock.scope` says: the suite is a resource of the
    MACHINE, the clock is a resource of the RUN. A project-wide tick lock on a machine with
    three live masters — which yesterday's isolated-master feature makes ordinary — would
    leave two of them blind.
  - **The bias is to ARM**, because the two failures do not cost the same: seven clocks is
    loud and announces itself, zero clocks is silent and indistinguishable from a healthy
    quiet run (no probe, no sidecar rewrite, no stall detected, a dead front unnoticed for
    hours). Anything unreadable as a pending tick — absent, corrupt, or a deadline past its
    grace — is broken and re-armed, never honored.
  - Every entry point respects it: pre-flight proves that the second `arm` is refused ("a
    clock whose second arm succeeds is not a clock"), `[C]` arms its own instead of inheriting
    a dead master's pending tick, `[S]` may call only `status` (the one verb that changes
    nothing — a `[S]` that claimed would eat the round), the heartbeat is one line per CLAIMED
    tick, and the sidecar reports `watch_tick: {armed_at, due_at}`. **The same rule binds every
    other watcher the run arms** — a review's, a subagent's, anything that promises to wake
    somebody later.

- **A story's gate measures WHAT THE STORY CHANGED; the whole tree is measured once, at the
  close.** The skill already scoped three of the four places it verifies — the inner loop after
  a failure, the post-merge smoke, the closing ladder — and left the fourth, the one paid PER
  STORY, at "the whole-repository suite, through the queue". MEASURED in a real run: one
  package's suite at 1238 s, paid once per delivery across eleven deliveries (3.8 hours of
  clock in a single package), on top of a ~25-minute whole-repository pass queued behind up to
  19 minutes of other fronts. The 2026-09-17 merge-gate detector had made it worse by
  mechanizing the wrong half: it demanded the QUEUE's log, which made the whole-repository
  suite the only admissible evidence.
  - **The scope is resolved by the PLAN, never inferred by the executor**, because the same
    skill runs against Python, JS, PHP and Go and cannot know what a package is. Three rungs,
    best available, the same shape as the wait's: `affected-command` (the project's own
    diff→targets command), `rule-map` (`rules[]` of path glob → commands, with `dependents` and
    `whole_tree_triggers`), `whole-tree` (the fallback, named as the slowest). The planner
    DISCOVERS which one the project supports and writes `verify.scope`; it asks exactly one
    question, and only when the answer would be the expensive one (question `6b`).
  - **The gate proves the scope covered the diff.** Every changed source file must fall under a
    target the pass actually executed — without that second half, dropping the whole-suite
    demand would trade rigidity for a hole, and a map with a gap would read as a green gate. A
    file covered by nothing is a SCOPE GAP, not the story's fault: the master writes
    `scope gap · <story> · <file> · <map>` to the ledger (`kind: scope-gap`) and the story runs
    the plan's `verify.scope.fallback` for itself, once, so it still merges on real evidence
    and the map gets fixed by evidence rather than by audit.
  - **The queue is per command** (`verify.queue_commands[]`), not global. Its three reasons —
    does not fit one tool call, fights for CPU with the lock holder, knocks over time-sensitive
    cases — describe the whole-repository pass, not a target's; everything else runs free and in
    parallel across fronts, which is what fronts are for. A whole-repository pass run OUTSIDE
    the queue is still a gate failure.
  - **A rung that ran out of time is not a failed story.** `clock` is a reserved layer
    (`failure <story> clock <rung> <elapsed>/<budget>`) and it NEVER enters the resolution
    ladder: measured, one case at ~504 s against a 180 s ceiling turned nearly every delivery
    red by clock, and each of those bought a diagnosis subagent and an adversarial lens for a
    problem that was never in the story's code. Its route is its own — re-measure that rung
    ALONE once, free of contention; over budget again and it is INCONCLUSIVE, recorded as
    `kind: infra-debt`, with exactly two exits (raise the budget where `tests.clock_budgets`
    authorizes one, or park the story `awaiting-owner`). The forbidden third exit is merging on
    the cases that ran before the clock cut. Default ceiling:
    `{workflow.clock_budget_minutes}`.

### Changed

- **`/waves-setup` resolves the install SOURCE instead of assuming the public Git URL.**
  An existing uv install names its own origin in `uv-receipt.toml` (`path = …` for a wheel
  or checkout, `git = …` for a repository), a source the user hands it wins over that, and
  the canonical Git URL is only the fallback. A bundle-installed machine has no Git remote
  to fetch from, so the old prose sent it to a URL it could not reach; it now reinstalls
  from the local wheel and says that `uv tool upgrade` cannot advance a fixed-version
  install. The skill's steps renumber (install is 3, bootstrap 4, preflight 5).

- **`waves-master-parallelism` asks through the runtime's question panel, like the other two
  skills that talk to a human.** Its questions contract prescribed a numbered menu in prose
  ending in `answer: a number (Enter = default)` and forbade any other shape, so the ten
  planning questions, the approvals and the dispatch decision all reached the owner as
  paragraphs of running text — with an Enter that sends nothing outside a panel, which
  `waves-master-tui` had already documented as the trap it is. It now follows the same rule
  as `waves-master-tui` and `waves-deferred`: the panel where the runtime has one (in Claude
  Code, `AskUserQuestion`) — the title as the question, each option a labelled item, what is
  at stake in the body, the default first, `other: <…>` left to the panel's own free-text
  Other — and, with no panel, the numbered table `bmad-help` and the BMAD Method agent menus
  use, ending in `answer: a number (or "default")`. A menu wider than the panel's four
  options (Step 6's letters, a candidate-plan list) stays in text either way. The options,
  their wording and one-question-per-message are unchanged; what changed is that the `<ask>`
  blocks are now read as the option TEXT, never as the presentation.

- **`waves run` launches the LLM control loop; `--deterministic` is the engine.** The
  owner's rule: orchestration by LLM is the default inside Waves. `waves run` now does what
  `llm-run` did — a supervisor plus an orchestrator session that decides at every
  crossroads — with the same `--epic`, `--story`, `--max-stories`, and `--resume <ref>`
  for a paused LLM-held run; `waves run --deterministic` is the fixed-pipeline engine, the
  only mode stories mode (`--spec`) runs on. `--dry-run` previews the scope either way.
  `[llm] enabled` defaults to on and is now the opt-out: `false` makes `waves run` refuse
  and name `--deterministic`. `llm-run` stays as the old spelling of the same command; the
  TUI's start-run modal opens with the mode select, LLM first; a resume suggestion for an
  LLM-held run reads `waves run --resume <ref>`.

- **The skills are named by what they are: one door per domain, and everything a door
  dispatches is `core-`.** `waves-master-tui` drives the loop — it absorbs `waves-operate`
  and `waves-watch`, whose split by run mode was the trap: the old menu's `[L] Loop por LLM`
  was a WATCHER and the only launcher was deterministic, so an operator who wanted the LLM
  loop got the engine. It asks, one question per message and each with its explanation and
  default — the run mode (LLM orchestration by default, the deterministic engine on
  request), the scope, the watchers of that mode, in the deterministic mode whether the
  watcher acts on a finding or only reports it (`[autonomia] modo`, written to the project's
  `rules.toml`), the thresholds of that mode — shows the
  exact command in a summary and launches only after it is confirmed; `[P]` takes every
  default and still shows the summary. `[V]` arms the watcher of the run's own mode, `[1]`
  runs that mode's script once, `[F]` is `intervene`. Its `rules.toml` is the union of
  both: `[limiares]` and `[projeto]` for `heartbeat.py`, `[llm.limiares]` and
  `[llm.fronteira]` for `pulse.py` and the LLM-run doctrine, every `[[regra]]` tagged
  `modo = "deterministico" | "llm"`. `waves-master-parallelism` drives an epic's waves — the
  planner (was `waves-plan`) with the whole menu: `[P]` plan, asking one numbered question
  per message, `[A]` approvals, `[R]` re-measure, `[V]` validate, and `[E]`/`[C]`/`[S]`
  which hand over to `waves-core-parallelism`, the executor (was `waves-master`, briefly
  `waves-master-parallelism`), whose session becomes the master. `waves-core-orchestrator`
  (was `waves-orchestrator`) and `waves-core-sweep` (was `waves-sweep`) are the automation's
  as before. `waves-setup`, `waves-deferred`, `waves-resolve` stay.

  | Was                              | Is                                                     |
  | -------------------------------- | ------------------------------------------------------ |
  | `/waves-operate`, `/waves-watch` | `/waves-master-tui`                                    |
  | `/waves-plan`                    | `/waves-master-parallelism` (plan, approve, hand over) |
  | `/waves-master`                  | `waves-core-parallelism` (dispatched by the door)      |
  | `waves-orchestrator`             | `waves-core-orchestrator`                              |
  | `waves-sweep`                    | `waves-core-sweep`                                     |
  | `_bmad/custom/waves-plan.toml`   | `_bmad/custom/waves-master-parallelism.toml`           |
  | `_bmad/custom/waves-master.toml` | `_bmad/custom/waves-core-parallelism.toml`             |

  `waves init --force-skills` retires the old-named directories (every generation, the 1.x
  names included), carries a project's own `rules.toml` additions into the successor, and
  renames the overrides; `validate` names whatever is left (`namespace.legacy`). The legacy
  layer — the `riaworks-waves-loop` alias, the double env export, the read-only legacy state
  listing, the old skill names — now retires in 3.1 (`namespace.LEGACY_RETIRES_IN`).

### Fixed

- **The distribution carries what its README points at.** The zip, the sh self-installer
  and the bundle shipped `README.md` and nothing it linked: its eight screenshots and the
  demo (`docs/images/`), every guide (`docs/*.md`), `TRADEMARK.md`, `SECURITY.md`,
  `CONTRIBUTING.md` and `examples/`. A recipient with no access to the repository opened
  the README to broken images and dead links. The payload now includes them —
  `docs/superpowers/` (working notes) stays out, as it does from the public sync — and
  `test_dist` checks that every relative link and image in the shipped README resolves
  inside the unzipped tree.

- **`[scm] max_parallel > 1` without worktree isolation runs serially in both loops, and
  says so.** The LLM loop's `unit pick` honoured the cap in place, offering two stories of
  a wave for ONE checkout — two sessions editing it and each story's commit carrying the
  other's half-done work — while the deterministic engine quietly stayed serial. `unit pick`
  now caps at 1 unless `isolation = "worktree"`, reporting the cap in force as
  `max_parallel` and the reason as `serial`; `waves validate` warns
  `policy.parallel-needs-worktree`. The policy template's `max_parallel` comment, which
  still called fan-out unbuilt and said values above one clamp to one, the `run --plan`
  help and FEATURES now describe what runs.

- **`release.py prepare` works in a package nested inside a larger repository.**
  `dirty_paths` returned porcelain status paths, which git spells from the repository's
  top level, and compared them with package-relative names — so the promoted CHANGELOG,
  the one change a release requires, read as unexpected and the release was refused. The
  package's prefix is stripped; a path outside the package keeps git's `:/` spelling and
  still reads as unexpected; a rename's trailing original path is no longer misread as a
  status line.

- **The uninstall guide names the tool uv installed.** `uv tool uninstall waves` and `uv
tool upgrade waves` name the command, not the package, and find nothing: the tool is
  `riaworks-waves`. The skill-removal step listed pre-rename `riaworks-loop-*` directories;
  it now removes `waves-*`.

- **`unit finish` refuses a run holding a committed story that never merged, and the
  orchestrator's doctrine names the case.** Under isolation a DONE story whose merge-back
  has not landed lives only on its branch, and nothing closes a finished run's stories
  again; `finish` now names such stories and sends the caller back to `close`. The
  doctrine had no rule for the story everything left depends on failing to integrate for a
  cause only the owner can clear, and the orchestrator of run `20260922-210104-0885` had to
  pick between "never pause for one story" and "finish when no work is left":
  `judgment.md` now makes that one case a `story-gate` pause, and a transient cause (an
  index lock) a wait and a second `close`. `error-kinds.md` says who clears which
  merge-back cause and that an older escalation is reopened by `close`; `verbs.md`
  documents `committed` / `commit_skipped` and that a long gate should run detached from
  the turn (the same run spent a whole turn waiting on a review gate in the foreground);
  the `waves-master-tui` runbooks stop calling an escalated merge-back a dead end.

- **A checkout with no `policy.toml` says so, and a git worktree missing its main's is
  refused.** `policy.load` answers a missing file with every default, so `validate`
  printed `policy OK` for a checkout that never ran `init`, and a run there took no
  `[scm] provision`, no worktree seed and none of the project's gates. `init` gitignores
  the policy, so every new git worktree of an initialized repository is born that way —
  measured 2026-09-23 (run `20260922-210004-f4ac`), where `validate` named only the
  missing hook relay. `validate` now reports `policy.absent`: a warning when no checkout
  has a policy, a problem when this one is a linked worktree whose main checkout has one
  (`verify.main_worktree_of`), with the `cp` that fixes it. `run` (both loops), `resume`
  and `sweep` refuse the second case before anything launches and warn on the first.

- **The LLM loop's board and ledger writes commit themselves in the target checkout.**
  Under isolation, `unit sprint advance` and `unit ledger add`/`close` write the checkout
  every story merges into, and nothing in the LLM host committed that — the engine's
  post-merge carries are the engine's. The next story's `close` met the run's own dirt:
  refused over the board for every story after the first (measured 2026-09-23, run
  `20260922-210104-0885`), and with a branch that also touched the ledger the
  incoming-path cleanup would have reverted it, `DW-` entries included. Each write now
  lands as its own `chore(sprint-status)` / `chore(deferred-work)` commit, by pathspec,
  when the run is isolated, the checkout is on the target branch, and the file is tracked
  and clean before the write (or is created by it, as a project's first ledger is); any
  other case writes without committing and says why (`committed`, `commit_skipped` in
  the verb's answer; a refused commit is journaled `llm-bookkeeping-uncommitted`, never
  raised). In place, the story's own commit still carries both files. With no carry to
  protect, the LLM host's merge guard no longer refuses over board or ledger dirt
  (`WorktreeFlow(carries_bookkeeping=False)`). And `behind_target` no longer counts a
  target that moved only in those two files, so a `--plan` front is not sent to a rebase
  and a full re-verification by its own `awaiting-merge` advance.

- **Nothing the run launches takes git's optional index lock.** Every session and plugin
  hook now starts with `GIT_OPTIONAL_LOCKS=0` (`envvars.session_exports`, at the
  adapters' launch seam and the hook bus, and in every `build_spec` env so an adapter class
  a plugin registers carries it too; a profile that sets it keeps its value), and so does
  every git the run spawns (`verify._run_git`). The orchestrator's session runs with
  the target checkout as its cwd, so its statusline — on the host of run
  `20260922-210104-0885`, a `git status --porcelain` on every screen refresh, which a
  `unit close` call triggers — held the index lock the merge-back needed; with the
  variable, `git status` reads the index without writing it back. Hosts no longer have to
  configure each statusline, editor and hook to stay off that lock. The merge-back also
  retries through a lock (below), which this complements.

- **Another process's index lock is waited out, not reported as a refused commit.**
  Measured 2026-09-23 (git 2.34, run `20260922-210104-0885`): with the target checkout's
  `index.lock` held for a moment — a statusline's `git status` is the likely holder —
  `merge --no-ff` prints `Unable to write index.` and `Automatic merge failed`, writes
  MERGE_HEAD and stages nothing, which is the commit-refused state to the letter; the
  owner was sent after a `pre-merge-commit` hook the repository does not have, and the
  same merge by hand passed first try. A lock held from the start, which git reports
  as `File exists` on the lock file, read as a pre-flight clash. `merge_branch` now
  classifies both as `MergeIndexLockedError` — only with every reading live and nothing
  written — undoes the `--no-ff` attempt with `merge --quit`, which needs no lock where
  `--abort` exits 128, and retries after 0.25/0.5/1/2/4 s. Each retried attempt is
  journaled `merge-index-locked`; exhausted, the reason names the lock file and whether
  it is still there (held or stale) or gone (the index write itself failed). The undo
  writes (`merge --abort`, the squash commit step's `reset --hard`) retry through the
  lock too.

- **A failed merge-back leaves an LLM-held story retryable, as the doctrine said.**
  `unit close` promised that a merge-back failure leaves the story at its terminal phase
  and that calling `close` again retries the integration; `error-kinds.md` told the
  orchestrator the same. Neither was true: every merge-back failure went through
  `keep_branch_and_escalate`, which set ESCALATED — a phase with no way out — before
  raising, and the test of the promise stubbed `integrate_unit` and never met it.
  Measured 2026-09-23 on run `20260922-210104-0885`: an index lock held for 160 ms
  escalated the one story three others depended on, the retry met
  `escalated -> done (allowed: [])`, and the epic waited hours for a hand merge that
  passed first try. `WorktreeFlow` takes an optional `merge_back_failed` seam; the LLM
  host uses it to keep the story DONE with its worktree mounted, journal
  `unit-merge-failed`, and raise the `git` refusal `close` already describes. The engine
  keeps its escalation. A story an earlier version escalated this way is reopened by the
  same `close` when the journal pins the escalation on the merge (`story-done` for that
  commit and phase, then nothing but `story-escalated`, worktree still mounted) —
  journaled `story-merge-reopened`; a branch the owner already merged by hand closes as
  git's "Already up to date".

- **A merge-back refusal names the resume command the run actually has.** Every merge
  arm of `WorktreeFlow` spelled `waves resume <id>` by hand, while the notify beside them
  already asked `_resume_command()` — so on an LLM-held run the reason, which is the text
  the orchestrator copies into its owner's alert, named a command that exits 2 there.
  Measured 2026-09-23 on run `20260922-210104-0885`. The arms now call the helper, and a
  source guard keeps a hand-built spelling out of the module.

- **A merge no longer reverts the deferred-work ledger the target moved past.** Measured
  2026-09-08 on an LLM-held run with parallel fronts: `unit ledger add` filed three `DW-`
  entries in the main checkout at 19:04 and the next unit's merge pre-flight restored the
  file to its committed version 13 seconds later (`merge-target-cleaned`), after which
  `append_entry` reused the freed numbers. The pre-flight's "incoming set" was
  `git diff --name-only <target> <branch>` — the two TIPS — so every path the target
  advanced past while a front was in flight read as incoming, and inside that set neither
  `protected` nor `tolerate` is consulted: membership authorizes `git checkout -- <path>`
  outright. It is now the MERGE-BASE diff (`<target>...<branch>`), which is what a merge
  can actually write, so a path only the target moved is left alone and the ledger's
  documented promise — tolerated, never cleaned, never reverted — holds. Unrelated
  histories, which have no merge base and no legal merge either, now raise instead of
  answering "every path". The Editor-leak reconciliation the guard exists for is
  unchanged: a leaked copy is always a file the branch committed, which is in both sets.

- **A plugin workflow dispatched by the LLM loop is told how to end.** The deterministic
  engine appends `WORKFLOW_COMPLETION_CONTRACT` to every injected workflow prompt — write
  `<implementation-artifacts>/<dev primitive>-result-<task id>.md`, then end your turn —
  and `unit workflows dispatch` never did, though it already spent the workflow stall cap
  that exists to bound a missing marker. A TEA boundary step therefore finished its
  analysis, wrote its reports under `test-artifacts/` (which no adapter reads as a
  result), and sat at the prompt: every Stop scored `no-artifact`, one stall nudge each,
  ~28 minutes of dead wall clock per step until the cap — measured 2026-09-08, with the
  same shape on an earlier run's epic boundary. The contract moved to `devcontract`,
  beside the reader that accepts the marker, and both dispatchers now append it off the
  same discriminator (`label`); `devcontract.workflow_marker_path` is the single
  composition point for the filename the reader matches by prefix.

- **An enabled plugin name nothing answers to is reported, not swallowed.** Measured
  2026-09-07 on a project whose `policy.toml` still enabled the 1.x `riaworks-waves-tea`: the
  bundled `waves-tea` stayed untrusted, so no ATDD scaffold ran and no epic-boundary step
  appeared, while `validate` said `policy OK` and `unit workflows list` returned an empty
  list with an empty `inert`. The registry now records every `[plugins] enabled` entry no
  manifest matches (`plugin-unknown` in the journal, `PluginRegistry.unknown_plugins`);
  `validate` warns (`plugins.unknown`) naming the available plugins and, for a renamed one,
  the current name (`namespace.LEGACY_PLUGINS`); `unit workflows list` names it in `inert`
  with the same reason, so the orchestrator sees why nothing is due. Nothing rewrites the
  policy — the entry is the operator's.

- **A front waiting for the suite no longer freezes the run, because the brief now carries the
  instrument and not only the rule.** MEASURED 2026-09-17 on a live wave: a front ended its
  turn twice with prose ("waiting for lint/typecheck", "waiting to queue the suite") and the
  run lost it, with the story's work intact on disk. It was not a front ignoring the rule — the
  brief carried the freeze sentence verbatim, and the front, knowing it, armed a log watcher
  over its gate log before ending the turn. The watcher woke it ONCE, it reported progress and
  ended again: the wait was a ~25-minute suite queued behind another front for 19 minutes, and
  the watcher's default life was 5 minutes. The whole chain hung off one literal command in the
  brief, `nohup … &`, which detaches the work from the harness's completion tracking and so
  MAKES a hand-rolled waker necessary. Six changes, each mechanical where the old rule was
  prose: **(a)** the brief fixes HOW the front waits as ONE literal command, chosen by the
  master from what pre-flight now MEASURES — whether this harness re-invokes a session when a
  background job ends, recorded as `harness_wakes` in the sidecar so a `[C]` resume reads it
  instead of guessing; where it does, the queue script is launched that way and ending the turn
  is legal, because that process's exit IS the event; where it does not, the front calls
  `suite-wait.sh` in cycles inside its own turn. **(b)** `&`/`nohup` for a rung the front then
  depends on, and delegating liveness to any log watcher, are forbidden BY NAME with the
  measurement behind them. **(c)** a fourth watch classification, `INCOMPLETE` — a front that
  returned with text that is not one of the three report lines is neither working, suspect nor
  dead, and the silence-based watch could never see it; the master re-drives it in place at the
  rung its liveness file names, and that abort does not consume a rung of the resolution ladder
  (three aborted waits would have escalated a healthy story to the adversarial lens). **(d)**
  the merge gate now detects the sibling defect it could already see: a suite log without the
  queue's own header lines is `failure <story> suite outside the queue`, mechanical like the
  stub scan — the queue rule had a name but no detector. **(e)** `suite-queue.sh` heartbeats
  every 60 s while it queues, so the log ADVANCES during a wait (the measured log carried one
  line for 19 minutes, in which a queued front and a dead one are the same file), and a front
  whose liveness says `suite queued` is WORKING to the watch, not a stall suspect — 19 minutes
  of queue came within one minute of `stall_threshold_minutes` killing a healthy front.
  **(f)** the brief copies the discipline from the new asset: the master that retyped it
  delivered three of its five items. Also fixed in passing: the queue executes its arguments,
  so its usage header and the brief now show `env VAR=x <suite command>` rather than leaving a
  master to invent a wrapper script for a suite that needs an environment.

## [2.0.0] — 2026-09-06

### Added

- **`bmad-config.version`: the BMAD-METHOD floor is a preflight finding.** `validate` reads
  the version the BMAD installer recorded in `_bmad/_config/manifest.yaml` and compares it to
  `bmadconfig.BMAD_METHOD_FLOOR` (6.12.0): ok at or above it, a problem below it (exit 1), a
  warning when the manifest is absent or names no dotted version. `run`, `sweep` and `resume`
  refuse on the same finding through `_require_base_skills`, so the preflight and the launch
  cannot disagree about which trees are supported.

- **A BMAD-METHOD 6.12.0 review-layer fixture** in `tests/test_install.py`: four
  self-contained layers reading `{diff_file}` and `{claims_file}` derive an empty, satisfied
  requirement with every layer active — the shape a 6.12 sandbox install validated live on
  2026-09-05, pinned offline so a regression fails without a network.

- **`unit workflows`: the plugin workflows an LLM-held run can now run.** The deterministic
  engine injects every plugin-provided workflow itself — the TEA acceptance scaffold before a
  story's first dev session, the Test Architect's analyses at each epic boundary — and the
  LLM-held loop had no verb for either: the plugin was enabled, the sprint tree listed its
  boundary steps, and nothing ever dispatched them. `workflows list <stage> --story <key>`
  (or `--epic <n>` at `post_epic_boundary`) names what is due and what already ran, from the
  same registry the dashboard paints from, and names any enabled-but-inert plugin with its
  reason so an empty list is explained. `workflows dispatch <stage> --name <step>` launches one
  step exactly as the engine would — the manifest's prompt rendered for the scope, the step's
  own role and adapter, the `<plugin>.<step>` label, the `workflow-start` entry, a boundary
  step stamped `running` — and the watcher closes the pair with `workflow-end` and stamps the
  step `done`/`failed` in `boundary_progress`, so the sprint tree cannot tell the two loops
  apart. The handover carries the workflow record for that; a handover without one is a plain
  session, as before. The plugin's in-process hooks stay the engine's for now, and the
  orchestrator skill says so.

- **The `atdd` column, and the scaffold on the board.** The tasks table gains an `atdd`
  column — `…` while `bmad-testarch-atdd` runs before dev, `✓` when it completed, `✗` when it
  did not, `-` when it never ran here — and the sprint tree suffixes the story with the same
  mark (` ·atdd✓`). Both read the run's `workflow-start`/`workflow-end` pair, which the engine
  and `unit workflows` both write, so a deterministic run and an LLM-held one paint alike. The
  scaffold used to be visible only while its session was open, in the `agent` column, and
  then nowhere: a run could finish with every red test written and the board saying nothing.

- **`Plugin.inapplicable_reason`: a plugin that has nothing to do here says so, and stays
  out of the way.** Consulted once at registry build, right after construction and before
  `validate`: a reason makes the plugin inert — its workflows are not injected, its hooks
  (declarative and in-process) do not fire, its seeds do not travel, `validate` is not asked —
  while it stays listed, on, with the reason (`LoadedPlugin.inert`, journaled as
  `plugin-inert`, `PluginRegistry.inert_plugins()`). This is what lets a plugin ship enabled by
  default: an enabled plugin in a project missing its prerequisite used to have two states,
  refuse to start or run and fail every step, and neither is what a default may do to a project
  that never asked. A probe that raises is isolated like a failed constructor.

- **`[adapter.orchestrator]` on the settings screen.** `llm-run` chooses the CLI and model
  that hold the control loop from that one table, and it was the one stage the TUI's policy
  editor (`g`) could not reach: the form fans a section out per name in `STAGES`, the
  orchestrator was not listed, and the map it fell into is hidden by design — so the table
  that decides which LLM orchestrates was editable only by hand. It is a section now, between
  the engine's three phases and the plugin roles, and its header says what it is (the
  `llm-run` control-loop session, see `[llm]`) instead of the generic per-stage line: the one
  stage that runs no story work needed to say so. The stage template gained
  `stage_descriptions` for exactly that; every other stage keeps the generic line. Pinned
  against `llm.supervisor.ORCHESTRATOR_ROLE`, the name the supervisor actually resolves, so a
  rename on either side fails a test instead of splitting the editor from the run. The policy
  template documents the table beside the other stage examples.

- **`<name>_role`: one workflow step on its own adapter, without copying the plugin.** The
  settings overlay already had `<name>_enabled` and `<name>_blocking`; it gains `_role`,
  which chooses the `[adapter.<role>]` a step resolves — a cheap model for a sweep, an
  expensive one for an audit. It exists because the alternative is worse: plugin overlay is
  BY NAME, so a project changing one field had to drop a same-named manifest that replaces
  the bundled plugin whole, and then maintain a copy of every prompt in it. Measured
  downstream: 195 lines carried to move `atdd` off the `dev` adapter. A role outside the
  known set is ignored rather than raised — the manifest's load-time check is where a typo
  belongs, and a setting must not crash a run at dispatch time.

- **One TEA plugin, `waves-tea`, at the cadence each step pays for.** Two plugins
  used to ship side by side: `tea`, inherited from bmad-loop, which ran all six Test
  Architect steps per story, and an epic-boundary plugin of the same family. Enabled
  together they did five of the six twice; apart, each was wrong for half the work. They are
  one plugin now, and the shipped defaults ARE the measured configuration — a project needs
  no policy edit to behave correctly.

  **The scaffold runs before the code.** `bmad-testarch-atdd` refuses to emit a test without
  `test.skip()` because it is a RED-PHASE scaffold, meant to be written first and unskipped
  by the implementation. Bound to `post_dev_phase` — the only in-unit stage that existed —
  it produced a skipped scaffold for code already written, gating nothing. It now runs at
  the new `pre_dev_phase` stage.

  **The four analyses run once per epic.** `test-design`, `trace`, `nfr` and `test-review`
  analyse a BODY OF WORK; run per story they re-analyse the same ground once per story —
  measured at 48–77 minutes per story on the project this came from. Their per-story twins
  ship OFF, for a project willing to pay three extra agent sessions per commit for a
  commit-time gate.

  **Both gates are preserved**, in the form each stage allows: per story a FAIL/CONCERNS
  verdict `pause`-vetoes at `pre_commit` so the story escalates; per epic it makes the
  boundary red, and `gates.epic_gate = "on-failure"` turns that into a pause. Fail-open
  throughout — a missing, unparseable or unattributable artifact never stops anything. The
  flag is `<step>_enforce`, deliberately not `<step>_blocking`: the latter is the generic
  overlay and means "the SESSION must complete", which is a different question.

  Two guards carry a month of running this downstream: the boundary **commits its own
  output** (verified first with the project's own `[verify]` commands) — left in the tree,
  the reports get swept into the next story's commit under the wrong author and message —
  and `epic_automate`, the one step that writes, is skipped when the tree was already dirty
  **on entry to the boundary**. That measurement is the whole point: asking "is the tree
  dirty now" after four reports have written their artifacts vetoes the step at every
  boundary, deterministically. See [the TEA plugin guide](docs/tea-plugin-guide.md).

- **`pre_dev_phase` is a workflow injection stage.** The first one that fires BEFORE the
  work exists, added for the red-phase scaffold above. Two properties are positional and
  load-bearing: it is dispatched BEFORE `baseline_untracked` is captured, so what it writes
  survives the rollback of a failed attempt (that snapshot is exactly what a rollback
  subtracts), and only on a story's FIRST attempt, so a retry does not regenerate a net the
  previous attempt is midway through turning green. `blocking = true` is refused there — the
  story is still PENDING, and the state machine gives PENDING no terminal transition to
  defer into.

- **`ctx.report_step(name, status, ok=)`: an in-process plugin can make an epic boundary
  red.** A declarative hook could always say a boundary went badly — its exit code becomes a
  failed boundary step. An in-process plugin could not say it at all: `blocking` is refused
  at a stage with no unit to defer, a raise is isolated as a crash rather than read as a
  verdict, and the journal stops nothing. So a plugin that READ a quality gate's artifact
  and found FAIL had nowhere to put the finding. Deliberately not a veto: the epic's stories
  are already committed, and the only sanctioned outcome is a pause a human resolves.

- **`waves tea-config [--write] [--json]`, and the `teaconfig` module behind
  it.** One resolver for the TEA integration's whole configuration surface — where TEA
  writes, the per-scope artifact layout, and the `_bmad/custom` files this tool manages —
  read by the plugin at startup and before each step, by this tool's own skills on
  activation, and by the TUI. It mirrors the BMAD Method's own
  `_bmad/scripts/resolve_customization.py`: one resolver, JSON on stdout.

  It exists because the TEA skills all write to FIXED names directly under `test_artifacts`
  (`nfr-assessment.md`, `gate-decision.json`, `test-review.md`) with nothing in the name
  saying which story or epic the verdict describes — and their output path is not
  configurable, five of the six exposing only `persistent_facts` and friends. Two cadences
  therefore overwrite each other, and a gate discovering its artifact by glob or by "the
  newest file" would veto a commit on the other cadence's verdict. So attribution is
  MEASURED: snapshot the directory before a step's session, diff it after, and copy the
  delta into a directory computed from the scope. The gate reads a path it calculated.

- **`validate` reports the TEA configuration surface** when the plugin is enabled: whether
  the Test Architect module is installed and where it writes, and whether each managed
  `_bmad/custom` file is current, missing, stale or taken over by the project. Gated on the
  plugin being on — a project that runs no TEA has nothing to be told about it, and a
  standing "not installed" line is how one learns to skim a report. The plugin re-reads the
  same surface at startup and before each step; the preflight is where an operator sees a
  problem BEFORE a run reaches the step that depends on it.

- **`init` configures TEA when TEA is installed.** Detecting `_bmad/tea/config.yaml`, it
  enables the plugin in the policy template and writes
  `_bmad/custom/bmad-testarch-{atdd,automate}.toml` carrying one `persistent_facts` entry:
  an executable test belongs in the project's own suite, and only reports belong under
  `test_artifacts`. The fact names no path, framework or suite command — it restates the
  separation each skill's own `workflow.yaml` already encodes — and it is resolved on every
  activation of that skill, by the loop or by a human. Files are written idempotently under
  a managed header; one lacking that header belongs to the project and is reported, never
  overwritten. This is the first thing this tool writes inside `_bmad/`, and the exception
  is deliberate: configuration a run depends on must not live in a prompt.

### Changed

- **`riaworks-waves-loop` is now `waves`.** The third rename of the fork, written to be the
  last: brand where it is read, product where it is typed. "Riaworks" stays in the module's
  display name, the README title and the distribution — `uv tool install riaworks-waves`,
  typed once — and everything typed daily is the product alone. The command was 19
  characters before its first subcommand, and `riaworks-waves-loop-deferred` was four parts
  to say "deferred".

  | Was                                                                           | Is                                                            |
  | ----------------------------------------------------------------------------- | ------------------------------------------------------------- |
  | command `riaworks-waves-loop <cmd>`                                           | `waves <cmd>` (+ deprecated alias, one minor)                 |
  | distribution `riaworks-waves`, import `riaworks_waves_loop`                   | unchanged                                                     |
  | BMAD module code `riaworks-waves`, `_bmad/riaworks-waves/`                    | `waves`, `_bmad/waves/` (display name stays "Riaworks Waves") |
  | `/riaworks-waves-plan`, `/riaworks-waves-plan-run`                            | `/waves-plan`, `/waves-master`                                |
  | `/riaworks-waves-loop-setup`, `-resolve`, `-deferred`                         | `/waves-setup`, `/waves-resolve`, `/waves-deferred`           |
  | `/riaworks-waves-loop-cli`, `/riaworks-waves-loop-watch`                      | `/waves-operate`, `/waves-watch`                              |
  | `riaworks-waves-loop-sweep`, `riaworks-waves-loop-core` (automation)          | `waves-sweep`, `waves-orchestrator`                           |
  | plugin `riaworks-waves-tea`, `[plugins.riaworks-waves-tea]`                   | `waves-tea`, `[plugins.waves-tea]`                            |
  | `.riaworks-waves/` (`.riaworks-waves/loop/` for the loop's state)             | `.waves/` (`.waves/loop/`)                                    |
  | `RIAWORKS_WAVES_LOOP_*`                                                       | `WAVES_*`                                                     |
  | relays `riaworks_waves_loop_hook.py`, `riaworks_waves_loop_probe_hook.py`     | `waves_hook.py`, `waves_probe_hook.py`                        |
  | tmux `riaworks-waves-loop-<run>` / `-ctl`, refs `riaworks-waves-loop/<run>/…` | `waves-<run>` / `waves-ctl`, `waves/<run>/…`                  |
  | antigravity hook group `riaworks-waves-loop`                                  | `waves`                                                       |
  | `_bmad/custom/riaworks-waves-plan.toml`, `riaworks-waves-plan-run.toml`       | `waves-plan.toml`, `waves-master.toml`                        |
  | TEA artifact namespace dir `riaworks-waves`                                   | `waves`                                                       |

  Every machine token a plan or a tracker carries is unchanged — `epic-<N>-plan-<date>.md`,
  `epic-<N>-run-<date>.yaml`, `execution.mode`, `contracts[]`, the `ready-to-merge` /
  `failure` / `blocked` lines, `SUITE-DONE rc=<n>`, `.front-hb`, the DW ledger format, the
  `--json` schemas, `ExitCode`, journal kinds — so plans written yesterday keep resolving.

  **Upgrading a project.** `uv tool upgrade riaworks-waves`, then in the project
  `waves init --force-skills`, then re-register the module with the BMAD installer —
  `npx bmad-method install --action update --modules <every module you use, waves included>
--custom-source <package>` (the explicit module list is what drops `riaworks-waves`;
  `quick-update` would keep the stale entry) — then commit. `init` does what the `1.0.0`
  rename left to hand: it moves `.riaworks-waves/` to `.waves/` with every run intact (each
  journaled `state-dir-migrated`), refusing when both directories exist, when a run under
  the old one has a live engine, or when a suite lock's owner is alive; removes the old
  relay's hook registrations from every CLI config it manages (the antigravity group
  included) and the old relay file; retires the old-named skill directories, merging a
  project's own `rules.toml` additions into their successors; renames the team-layer
  `_bmad/custom` overrides of the two renamed skills; swaps its own three `.gitignore`
  lines. Your `~/.local/state/riaworks-waves-loop/` (the out-of-tree control plane of 1.x
  runs) is not needed by anything after the upgrade; remove it by hand when you like.

- **The product is spelled in one module.** `namespace.py` is the only code that carries
  the command, the state dir, the env prefix, the skill and plugin names, the relay file
  names and the legacy spellings; every message, lookup and injected variable names a
  constant there (`envvars.py` registers the session- and hook-protocol names the engine
  injects), and `tests/test_portability_guard.py` refuses a product string in any code
  literal outside it. A fourth rename, if it ever comes, is one constant plus directory
  moves.

- **`validate` reports what a 1.x project still carries** (`namespace.legacy`): the old
  state dir, a hook config still registering the old relay, an old-named skill dir, an
  old-named `_bmad/custom` override — one warning each, naming the `init` that clears it
  (a personal `.user.toml` override is named for renaming by hand; this tool never writes
  that layer). Warnings, never problems: every leftover still works, it is the property of
  one spelling the operator is losing.

- **`list` and the dashboard show a 1.x project's runs across the rename** —
  `runs.list_run_dirs` reads `.waves/loop/runs/` first, then `.riaworks-waves/loop/runs/`,
  and a ref that resolves into the old dir is refused with the `init` that moves it, so no
  command ever writes there.

- **The fork tracks upstream bmad-loop 0.11.1.** Merged v0.11.0 and v0.11.1 (229 commits,
  106 files) with the fork's namespace applied to both upstream sides before the 3-way, so
  the rename never read as a conflict: 19 files conflicted where the fork had its own
  changes. Their sections follow below, under `[0.11.1]` and `[0.11.0]`. What reached this
  fork's own loops: git 2.34 is the declared floor (`git.version`, refused by run/sweep/
  resume), `post_dev_verify` fires on the repair leg too with structured `command_results`
  and one `verify-command-result` journal record per command under `verify/`, a provider
  5xx or a mid-response connection drop on the `claude` adapter pauses the run, dev/review
  stall grace arms at launch and re-arms on activity, the policy loader rejects mismatched
  TOML scalar types for every field (the fork's `[llm]`, `epic_gate` and operator-hold
  fields go through the same typed readers), the run inventory (`discover_runs`, liveness,
  statuses) moved from `tui.data` to `runs` so `list` no longer drags the TUI extra in —
  the fork's `source` header field and its pause-vs-stop rule moved with it — `STAGES`
  lives in `policy.py` with the fork's orchestrator and workflow roles, `sweep --migrate`
  refuses a ledger with duplicate `DW-<n>` ids, a stop request is consumed by rename so a
  concurrent escalation to `"hard"` is never read stale, and every atomic writer keeps the
  file entire on a failed replace.
  - **The merge guard grades the index column (#618), and the fork's `tolerate` list
    narrows to what it can prove.** Upstream measured that an unstaged tracked stray is
    inert to the merge under both strategies, and that the real hazard is the paths the
    run's own post-merge carry commits by pathspec (`protected`: the board and the ledger).
    The fork kept its `tolerate` operand — the `unit` verbs write both files in the main
    checkout while a story is in flight — but the board is now tolerated only while every
    line it differs from HEAD by is this story's own (`_tolerated_at_merge` /
    `_board_dirt_is_own`: the story's row, its epic's row, `last_updated`, the writer's
    own STATUS DEFINITIONS lines). A sibling row an operator reopened or a private note
    hands the board back to `protected`, and the merge is refused before the carry could
    commit their bytes under the run's name. The ledger stays tolerated as named.
  - Kept ours, deliberately: the version stamps (`1.0.0`), the fork's README, the rendered
    dashboard images, and the changelog structure; `uv.lock` regenerated for the `rich`
    pin the `tui` extra gained.
  - `diagnose`'s policy scrub reduces `adapter.stages` — the fork's second user-keyed
    table — to its stage names, the way `plugins.settings` is reduced to plugin ids, so
    upstream's free-keyed-table invariant holds here too.

- **BMAD-METHOD 6.12.0 is the supported floor.** 6.12 rewrote the dev primitive's review
  step — the diff and the spec reach the reviewers as files, triage renders a verdict per
  finding, `maybe-false` findings defer as `medium (unverified)`, the deprecated shims are
  opt-in — and that is the protocol this tool reads. Older trees are still _resolved_ (both
  primitive names, both review topologies) but no longer supported: `validate` fails and the
  run preflight refuses below the floor. README, the setup guide and FEATURES say so; the
  setup skill's config-resolver note names 6.12+.

- **`waves-plan` and `waves-master` pass `--project-root {project-root}`
  to `resolve_customization.py`**, as every 6.12 skill does. The 6.12 resolver prefers the
  working directory over the skill's own path; the explicit root removes the ambiguity for a
  skill installed under the user's home.

- **The self-installer's tool table learns `grok`, `polytoken` (`.agents/skills`) and `zcode`
  (`.zcode/skills`)**, mirroring `bmad-method install --list-tools` at 6.12.0.

- **Setup guide: what 6.12 changed for the loop.** `project-context.md` is no longer
  auto-loaded (`persistent_facts` ships empty in `bmad-build-auto`, `bmad-review` and
  `bmad-sprint-planning`); the guide names the two remedies — `/bmad-project-context` into
  `AGENTS.md`, or re-adding the fact in `_bmad/custom/bmad-build-auto.toml` — and the
  `{diff_output}` → `{diff_file}` migration a review-layer override needs.

- **The TEA plugin is on by default, and inert without TEA installed.** `[plugins] enabled`
  defaults to `["waves-tea"]` — the dataclass, the template `init` writes, and an
  absent table all agree — so a red-phase acceptance scaffold before every story and the
  Test Architect's analyses at every epic boundary are the cadence a project gets without
  asking; `enabled = []` opts out, and `atdd_enabled = false` and its siblings turn off one
  step. Safe as a default because of the seam above: in a project without
  `_bmad/tea/config.yaml` the plugin is inert, the sprint tree lists no boundary rows, and
  `validate` names the missing module and both ways out. `require_tea` flips to `false` and
  changes meaning — `false` is now "inert, with the reason" rather than "run the steps
  advisory-only into skills that do not exist"; `true` keeps the startup failure for a
  project that demands TEA. `init` no longer detects TEA to decide whether to enable the
  plugin: the template says enabled either way. Turning the plugin off is the operator's
  decision, not the tool's default.

- **The wave skills stop running the gate ladder five times per story.** A cycle-time
  measurement on a nine-wave epic found the ladder running five or six times per story — on
  the front after every edit, on the master after every merge, and again at the close — at
  15–20 minutes of machine time per pass, plus the queue. Seven changes to
  `waves-plan` and `waves-master`, each measured before it was made:

  - **The whole ladder runs ONCE per `ready-to-merge`.** After a rejection the front reruns
    only the inner loop the plan names — the touched packages plus the story's own specs,
    free of the queue — and the whole ladder again only when the fix touched a package the
    previous ladder did not cover.
  - **After a merge the master runs only the parallelism smoke.** The whole ladder and the
    Test Architect skills run once, at the epic close, on the integration branch.
  - **ATDD moves to wave 0**, run once per live story by one subagent through the new
    `{workflow.atdd_skill}`. It produces one acceptance case per AC as SKIPPED scaffolds, so
    the integration branch stays green; the front un-skips its story's cases BEFORE the code,
    sees them red, and turns them green. This is what `bmad-testarch-atdd` was built for — it
    refuses to emit a test without `test.skip()` — and it makes those cases the "executed
    case" of the AC matrix at the merge gate.
  - **The `tests:` block loses `tdd`.** `bmad-build` does not do TDD by construction: its
    handoff says "implement the spec", and its Matrix Test Audit checks AFTERWARDS that every
    matrix row has a test that ran and passed. The plan promised an order nothing observes.
    What stays guaranteed is what is actually mechanical: a test per matrix row, executed,
    green, not skipped or filtered out.
  - **The front runs `bmad-build` end to end, steps 1 to 4**, with the story as its intent
    and the I/O matrix mandatory — one row per AC clause. A story with no spec file did not
    run the pipeline: `failure <story> pipeline bmad-build not run`. (Measured: an epic's
    largest story shipped with no spec, no matrix and no audit, because the brief said "YOU
    implement the story".)
  - **Every ladder rung must name a gate that exists on today's integration branch.**
    Measured: a brief carried a language gate deleted the same day, plus the `git add` that
    existed only to feed it, and every front paid both.
  - **The AC matrix is checked MECHANICALLY at the merge gate**: each row names a test file
    present in the story's diff or in wave 0's ATDD set, not skipped, and appearing in the
    front's suite log. The master reads artifacts, not the front's prose.

- **A plan targets a SCOPE — an epic, or a story set that crosses epics.** The collision
  matrix was always epic-agnostic: the Phase 0 sheet measures a story's file surface,
  sequential resources, append regions, routes, test resource and consumed contracts, and
  none of those fields is about the epic. What tied a plan to one epic was the reading scope
  and the file names. `epics[]` replaces `epic`, step 1 declares that nothing downstream
  branches on which epic a story belongs to, and the executor dispatches fronts across epics
  in one wave with no other change.

- **Artifact names lead with a timestamp, so a listing is chronological.**
  `{stamp}-{scope}-plan.md` with `YYYY-MM-DD-HHMM` local time — the stamp FIRST, because with
  the scope leading, runs of different scopes interleave and the timeline is lost. A run's
  three artifacts share the stem, so they sort together and in order. This fixes a real
  collision on the way: the wave report used to be `epic-<N>-wave-<n>.md`, with no date at
  all, so a second run of the same epic silently overwrote the first one's report. Plans
  already on disk keep resolving under the old shape and are never renamed, and a live run
  keeps the shape of the plan it is executing.

- **The close splits what is about the TREE from what is about an EPIC.** The whole gate
  ladder runs ONCE, over the integration branch — it answers a question about the branch, so
  running it per epic re-verifies one tree N times for one answer. The Test Architect skills
  run ONCE PER EPIC the run actually closed: `gate_type: epic` over the stories of four epics
  records a scope that is not true, and a quality review whose subject is a mixture belongs
  to none of them. "Closed" is read from the tracker — every story under that epic `done` —
  never inferred from "the scope's merges are finished", so an epic the scope covers only in
  part gets no tea pass and stays `in-progress`, which is the truth.

- **One master per project, and now it is checked.** The integration branch, the tracker and
  the suite lock are single resources: a second master merging into the same branch and
  writing the same tracker is corruption, not parallelism. The rule always held and was never
  written down; the pre-flight now looks for another live sidecar and halts naming the run
  that holds the project. Several epics at once is ONE plan whose scope spans them.

- **The wave pipeline drops its second review pass.** `story_pipeline` is
  `["bmad-build", "verify"]`, and the merge gate no longer runs `bmad-code-review` with the
  story as `spec_file`. The build rung run end to end already carries a review — `bmad-build`
  step-04 with its own `[[workflow.review_layers]]` — so the second pass was a whole extra
  LLM review per story on top of it. **What it cost:** that argument was what switched on the
  Acceptance Auditor, the review of the ACs themselves, and step-04 reviews the code against
  the spec the same skill wrote. The mechanical matrix check above is what replaced it: more
  reliable about "a case exists, ran and is not skipped", and silent about whether the case
  truly exercises the AC. Projects that want the auditor back can name `bmad-code-review` in
  `story_pipeline` through `_bmad/custom/waves-plan.toml`.

### Deprecated

- **`riaworks-waves-loop`, the 1.x command**, ships as an alias for one minor: it prints
  `riaworks-waves-loop is now waves; this alias goes away in 2.1` to stderr and delegates.
  Stderr, so `--json` stdout stays one object.

- **Both env spellings, for one minor.** Every session and every plugin hook is handed
  `WAVES_*` and its `RIAWORKS_WAVES_LOOP_*` twin (`envvars.legacy_exports`), and the relay —
  the copied `waves_hook.py` and `waves relay` alike — reads the new spelling first and the
  old one second, so a project whose relay predates `init`, or a 1.x orchestrator driving a
  session through the new relay, keeps completing sessions. The double export, the alias
  and the read-only legacy listing drop in 2.1 (`namespace.LEGACY_RETIRES_IN`);
  `tests/test_envvars.py` fails the first version that forgets.

### Removed

- **The `tea` plugin.** Merged into `waves-tea` above, which carries its commit
  gate and its verdict parsers unchanged. A `policy.toml` naming `tea` (or the never-bundled
  `tea-epic`) must name `waves-tea` instead; the loader reports an unknown plugin
  rather than silently running nothing.

### Fixed

- **The extras were spelled after the command, not the distribution.** Four messages and
  every install line in the docs said `riaworks-waves-loop[tui]` (or `[opencode]`,
  `[non-linux]`) — a name `uv` and `pip` refuse against a project called `riaworks-waves`.
  They say `riaworks-waves[tui]` now, from `namespace.DISTRIBUTION`.

- **A `deferred[].severity` of `medium (unverified)` no longer loses its grade.** The 6.12
  marker made the whole string miss the alias table, so the harvested ledger entry carried no
  severity at all. The grade is now the first word, mapped as before; the marker becomes a
  `[severity unverified]` prefix on the evidence, where 6.12 puts "what would settle it".

- **The setup skill looked for the module under the wrong directory.** The BMAD installer
  registers a module under its `code` — `_bmad/waves/` — while the skill, the skills
  README and the setup guide said `_bmad/waves/`, so the skill declared an
  installer-registered module unregistered and wrote a stray `module-help.csv` beside it. All
  three name the code's directory now, and the setup-skill contract test pins it.

- **`unit dispatch` refuses a role nobody configured and a story the run never opened.**
  Measured 2026-09-05 on an LLM-held run: the orchestrator dispatched `codex` — the CLI's
  name where the role goes — and the verb accepted it, resolved the unknown role to the base
  `[adapter]` table, and the "dev" ran on claude, the binary dev had been pointed AWAY from;
  in the same run it skipped `unit open`, the tasks table stayed blank for the whole session,
  and the board never moved. The role must now be one of `dev`, `review`, `triage` or a
  plugin workflow role (`invalid-args`, listing them and saying the CLI is chosen in
  `[adapter.<role>]`), and the story must be open (`not-found`, naming the `unit open` that
  was owed). The orchestrator skill states the sequence and the roles outright.

- **An orchestrator on a client no other stage uses runs on that client.** `llm-run` builds
  one adapter per bootstrap role (dev, review, triage) and matched every other role to one of
  them by resolved client; a role matching none fell back to dev's object — "a gap rather than
  a decision", the code said. Reached from one line of policy: base `claude`,
  `[adapter.orchestrator] name = "gemini"`, and the orchestrator started in `claude` carrying
  gemini's model name, failing on the first real turn with nothing in the config to explain
  it. Now every call site that dispatches, steers or waits on a session names its role to
  `build_adapters`, which builds a role on a client none of the three drives from its own
  table (`make_adapters` takes `roles`; a role outside the pinned profiles resolves from
  disk), and `adapter_for_role` refuses — an `env` fault naming the role and the client —
  instead of substituting dev's. A role on a client a bootstrap role already drives keeps
  sharing that object, as before. Surfaced by putting `[adapter.orchestrator]` on the settings
  screen, which made the configuration one form field away.

- **The project a run belongs to is derived from the state dir's depth, never a literal.**
  The tmux adapter walked `run_dir.parents[2]` to find the project it tags a session with;
  nesting the state directory added a level, and the tag silently became `.waves/`
  instead of the project — which is how a cleanup running in another project prunes this
  run's session. It now takes the depth from `RUNS_DIR` itself, the way the LLM watcher
  already did.

- **A stage the plugin system only _declared_ is no longer walked.** `workflow_stages()` —
  the engine's O(1) "is there work at this stage" guard — counted workflows from every
  loaded manifest, while the dispatch that follows counted only ACTIVE ones (an un-enabled
  `[python]` plugin is inert). The disagreement was invisible while no bundled plugin
  declared a stage of its own; the moment one did, every project on earth walked that stage
  with nothing to dispatch — and the epic boundary recorded an empty progress entry for a
  boundary that ran nothing. Both now read the same active set.

- **The planner counts requirements, not bullets.** A `Then` that strings clauses together —
  "Then A, B, C and D" — is N acceptance criteria wearing one number, so a story that reads
  as 8 ACs can really be ~25 and walk past the slicing flag. MEASURED: that story took eight
  hours from its first `ready` to merge. The planner's size check now says how to count, and
  `ac_flag_threshold` documents that a team whose epics are written with composite `Then`s
  wants it lower (4, downstream). The skill only flags; the slicing is still the PM's, in the
  epics document.

- **The stub scan reads the sentence, not the word.** MEASURED on story 14.1 of a
  downstream epic: the merge gate failed the story because the word "placeholder" appeared
  in the added lines — inside a comment that FORBADE placeholders — and the whole gate
  ladder ran again for it. The scan now splits what it looks for. `stub_markers` (`TODO`,
  `FIXME`, `XXX`, `HACK`) are conventions for "come back here" and still count anywhere,
  comment included. The natural-language claims moved to a new `stub_phrases` list
  (`placeholder`, `not implemented`, `mock data`, …) and count only OUTSIDE a comment,
  where they are nearly always breaking the rule rather than stating it. And a line whose
  words before the marker negate it — the new `stub_negations` list, in English and in the
  project's language — is not a hit at all. Nothing measured stopped being caught: the
  contract test asserts every old marker still appears in one of the two lists.

## [1.0.0] — 2026-09-05

### Added

- **The epic-parallelism half, brought in whole.** What follows was the `riaworks-waves`
  package's own changelog, unreleased at the merge; it is the history of the two skills that
  are now `riaworks-waves-plan` and `riaworks-waves-plan-run`.

- **The package.** Two skills for epic-level parallelism on BMad Method projects.
  `riaworks-waves-plan` measures where an epic's stories collide before any code exists — a
  pairwise collision matrix with a skeptical audit, then waves and fronts, a merge grid,
  execution governance and a machine-readable YAML block. `riaworks-waves-plan-run` is the session
  that becomes the master: it dispatches fronts as subagents, merges by the grid, runs the
  broad gate by subagent, keeps the tracker, and writes the run's state to disk at every
  watch tick and every event, so a dead master is resumed by `[C]` from what was written.
  Neither runs under an orchestrator: they are interactive skills invoked in a coding-CLI
  session, and they need only a BMad Method project and a harness with subagents.

  Born in a downstream project on 2026-08-26 as `rws-build-parallelism` / `rws-run-waves`,
  evolved over eighteen commits through 2026-09-03, and briefly bundled in the
  `riaworks-loop-llm` module before becoming this package. Made project-agnostic on the way:
  the front discipline that project kept as team overrides — synchronous fronts, the
  `.front-hb` liveness file, substitution by overlap, whole-repository suite only through a
  queue — is skill text plus three `customize.toml` keys (`front_liveness_file`,
  `suite_queue_script`, `suite_lock_dir`); the queue script it rewrote per run ships as
  `assets/suite-queue.sh` (POSIX sh, suite command as an argument, lock released only by its
  owner, dead-owner lock broken by atomic rename). Authored in English; at run time both
  skills speak the project's `communication_language`.

- **A contract gap has its own path; "decide and continue" stops at execution detail.**
  Measured on an epic that shipped after three days with its frontend green and its central
  functions printed on screen as curl commands: the master's brief authorized "declare the
  absence in one place", a front applied it to the save function its own AC named, the gate
  saw only the symptom, and no ledger line was ever written — the story had also reached the
  front with an object nobody built. Six rules close that, in both skills. Fronts report three
  lines and no other: `ready-to-merge` now carries the AC matrix (one executed case per AC —
  the master reads the matrix, never the prose), `failure`, and the new
  `blocked <story> <AC> <missing>` line; declared absence never covers an AC. The merge gate
  checks the matrix, refuses
  any story with an open gap or an unresolved gap ledger line ("no line, no merge; half a
  story never merges"), and for a UI AC wants a capture of the real screen beside the mock. A
  contract gap is never decided away: ledger line first, then exactly one of build-it (extra
  front), defer-the-whole-story, or park-it `awaiting-owner` — the run never pauses, the story
  does; the sidecar gains `decisions.kind` and a `parked` list, heartbeat and status carry
  `parked <p>`. Upstream of all that, the planner's Phase 0 sheet now lists every route,
  object, migration and event a story consumes with its producer, the YAML block carries
  `contracts[]` and `contract_gap_policy`, a `none` producer must have a `pending_approval`
  entry, and the executor refuses to dispatch a story whose dependency has no owner.

  A second pass, reviewing both skills against the model's actual behavior, added what the
  first left open. The review of the ACs is BMAD's own: the pipeline's review rung is
  `bmad-code-review` with the story as `spec_file` — the argument that switches on its
  Acceptance Auditor; every Epic-12 brief omitted it, so the AC review never ran in nine
  waves — and it is run by the master as a clean-context subagent on the front's commit,
  never by the author on itself, with its findings routed deterministically
  (`decision-needed` → gap, `patch` → failure, `defer` → ledger). The story reaches the front
  verbatim, never paraphrased. The moves the model reaches for when a piece is missing are
  named and forbidden, and a deterministic stub scan (`stub_markers`) over the story's added
  lines makes any of them a failure. The gap-versus-detail test is mechanical (a
  route/object/table/module that does not exist and no producer builds; in doubt, a gap),
  so the master cannot reason around it. The planner's skeptic now refutes producer claims,
  not only matrix cells. The tracker only ever receives statuses its header defines. And a
  browser tool (Playwright MCP or equivalent) is an absolute prerequisite for UI stories:
  pre-flight checks it, absent means those stories are parked with the remedy spelled out,
  and only the owner may waive visual capture (`visual_acceptance: waived-by-owner`, decided
  in the plan) — the master never does.

- **Distribution without a public repository.** `scripts/build-dist.py` builds two artifacts
  into `dist/` from the same tree: `riaworks-waves-<version>.zip`, the package as the BMAD
  installer wants it (unzip anywhere, `--custom-source ./that/folder`, module registered and
  skills laid down for every selected tool), and `riaworks-waves-<version>.sh`, a POSIX sh
  self-installer with the package embedded — copies the skills into each tool's directory
  with no npm, git or network, keeps existing directories unless `--force`, or hands the
  tree to the BMAD installer with `--via-bmad`. Deterministic builds, `SHA256SUMS` alongside,
  version taken from `skills/module.yaml`. Tests build both into a temp dir and install from them.

- **Install path for any coding CLI.** `module.yaml` and `module-help.csv` sit at
  the skills' common parent, so `npx bmad-method install --custom-source <this repo>` resolves
  the module by the installer's first strategy and lays the skills into the directory of every
  tool selected with `--tools`. No dependency on the Claude Code plugin marketplace.

- **`baton`: the orchestrator now says when it takes the turn back.** The window between a session
  settling and the next dispatch is where the LLM reads the gates, the log and the diff — the whole
  reason this control loop left Python — and it was the only part of a turn with no trace at all.
  From outside it is indistinguishable from a stalled turn: measured 2026-08-22 in run
  `20260822-095341-34b9`, every `session-end` was followed by four to nineteen silent minutes, and
  one of those gaps ended with the monitor intervening rather than with a decision. It also cost the
  successor — a turn that dies mid-reading leaves nothing behind, so the next one re-reads from
  scratch. `rws-loop-core-llm` now names a fourth turn obligation: journal `baton` the moment a
  session settles, before reading, with what settled and what is being weighed. Both fields are
  facts at the moment of writing, so the "journal only what happened" rule holds. One entry per
  handover and never a heartbeat — silence during a live session is correct, and a stream of
  "still working" entries would blind the checks that exist to notice a stalled turn. No engine
  change: `unit journal` already takes a free-form kind.

  The monitor learns the token on the other side: `pulse.py` counts `baton` as PROTOCOL, not work,
  so a turn that opens, announces the handover and then stalls cannot buy a credit from
  `turnos-sem-avanco` — the check would otherwise go blind exactly where the new obligation makes
  the entry universal. It does still count in `silencio_do_turno`, and should: there it is honest
  evidence the turn was alive at that instant, and unlike `operator` it cannot be gamed into a
  false green, because the protocol forbids repeating it while reading.

- **The board now defines the statuses this tool writes into it.** `sprint-status.yaml` is a
  BMAD-METHOD artifact, and the method's own updater for it — `sync-sprint-status.md`, executed by
  an LLM, not a binary — decides idempotency in prose that enumerates five statuses
  (`backlog`/`ready-for-dev`/`in-progress`/`review`/`done`). Anything else lands in an undefined
  case. Measured, with a control: an agent executing that workflow literally against a lab board,
  blind to which row was under test, skipped `review` (the text decides that one) and regressed
  BOTH `awaiting-merge` and `awaiting-operator` to `in-progress`, reporting that neither was
  text-determined — so this is a pre-existing exposure that `awaiting-operator` shares, not one
  `awaiting-merge` introduced. That workflow's step 1 loads the whole file, so `sprintstatus.advance`
  now puts the ordering where the executor already looks: writing a status outside the method's five
  adds a definition for it to the board's own `STATUS DEFINITIONS` block, stating the ordering in
  step 3's vocabulary ("LATER than 'review', EARLIER than 'done'. Never regress it."). Comment-only,
  idempotent, and the neighbours are read off `STATUS_ORDER` so the sentence cannot drift from the
  tuple that decides. A board with no such block is left alone — no structure is invented inside
  someone else's artifact — and the run journals `board-status-undocumented` instead. Defense in
  depth, NOT a guarantee: a literal executor can still ignore what it read, and the real fix is
  upstream's step 3 refusing to overwrite a status it cannot order.

- **`awaiting-merge`: a board status for work that passed the gates but has not landed.** Under
  `[scm] isolation = "worktree"` a story's commit lives on its unit branch until a merge-back that
  can be refused, so between those two moments `done` asserts something git cannot confirm —
  measured in run `20260818-003134-49e2`, where `sprint-status.yaml` called stories 4-5 and 4-6
  done while `master` contained neither, because a pre-merge guard had refused both integrations
  for a reason that was not the stories' own. The token joins `STATUS_ORDER` between `review` and
  `awaiting-operator`: parking already implies committed and, under worktree isolation, merged, so
  it cannot come before the merge. It stays out of `ACTIONABLE_STATUSES` — a story mid-merge must
  never be picked up again — and only the `llm` path writes it, through the `unit sprint advance`
  verb the orchestrator already owns, whose discipline is one paragraph of protocol in
  `rws-loop-core-llm` rather than a change to the deterministic engine's mirroring. The dashboard
  paints it "M" in yellow, beside `awaiting-operator`'s pause. The review gate reads the board, so
  it learns the token too: under isolation `unit verify review` expects `awaiting-merge` — the
  status the protocol has written by the time it runs — and still expects `done` with no worktree,
  where there is no separate branch the work could be missing from. The expectation is precise per
  configuration rather than "either": `awaiting-merge` precedes `done` in the order, so accepting
  both would let a board that never advanced sign off an in-place story.

- **`rws-loop-deferred`: the deferred-work decision queue, answered away from the prompt.** A
  sweep's `DecisionPrompter` is a blocking terminal prompt with a one-line question and two-word
  labels, and no LLM in that loop by design — so "explain this" is structurally unavailable and
  deliberating on one decision holds the rest of the run hostage. The new human-invoked skill
  reads the queue with `decisions --json`, anchors each decision in the document and code the
  ledger entry already cites, emits a dossier grouped by subsystem (recommendation, cost of each
  option, contradicting precedent first), and submits the batch through `decisions --answer`. It
  holds no state and writes nothing itself. Modes: `[D]` dossier, `[R]` answer, `[A]` autonomous
  for what the sources settle unambiguously — `close` effectively never automatic, since a wrong
  close is silent loss.

- **`riaworks-bmad-loop decisions --answer DW-<n>=<key>` answers the queue without a terminal
  prompt (repeatable).** A sweep's triage can surface decisions faster than the blocking
  `choice [1/2/3]` prompt can absorb them — one measured run produced 93 — and that prompt has
  nowhere to put a code excerpt or a quoted doctrine paragraph, so the operator answers under
  pressure or not at all. The flag lets the reading and the answering happen at different times.
  The whole batch is validated against the pending set before any of it is written, so one bad
  pair aborts with every defect named rather than leaving the first N recorded; answers route
  through `apply_pre_answer`, the same function the prompter uses, so both channels leave
  byte-identical state (pinned by a parity test over the ledger and the pre-answer store). One
  batch is one commit, not one per answer — at 93 answers the per-call commit was 93 `git add` +
  `git commit` rounds and 93 commits for one sitting; the interactive prompter keeps its
  per-answer commit, and since granularity is history rather than state the two channels stay in
  parity. Refuses alongside `--list` or `--json` at `USAGE`, since `--json` on this command
  already means the listing.

- **`unit finish` — an LLM-held run can end without claiming it needs a human.** The supervisor's
  loop stops on `state.finished`, and no verb could set it: a run whose last story was done and
  whose selector was exhausted could only `pause`, which every consumer reads as "waiting for a
  human" — the dashboard badge, the epic gate, an operator skimming a run list. The cost of the
  workaround was measured on a real run, not theorised: without pausing, the run stays non-terminal
  and every relaunch spends a turn reading state, finding no work and closing, burning the relaunch
  quota to reach a conclusion nothing records. The verb refuses only what is incoherent — a paused
  run, or a story still mid-flight, which finishing would strand in a run nothing will drive again —
  and never consults the board, because deciding the scope is done is the caller's whole purpose.
  `RunState.finish_reason` records the sentence that closed the run, since this loop's ending is a
  judgment somebody made.

- **The dashboard knows an LLM-held run when it sees one.** It was built on the deterministic run
  model and a contract test pinning that run-dir artifacts alone make an `llm-run` legible — true,
  and not the same as useful: the orchestrator session was invisible, none of the turn vocabulary
  showed, and there was no way to speak to a session without `attach`. Four additions, none of which
  changes how any other run renders. `data.open_sessions` reports every session currently open with
  its role, which the existing single-id reader cannot: it tracks one `active`, so with an
  orchestrator and a worker both live the second start displaces the first and the second end clears
  the slot while the first still runs. `n` cycles the Log pane through those sessions and back to
  auto-follow, pinning as it goes. A full-height column beside the detail pane tails the orchestrator
  session for runs whose `source` is `llm` — full height rather than a split inside the Log tab,
  because the point is to watch it decide while reading the journal or the worker. The run header
  gains `turn N`, the last verdict, and consecutive silent turns against the relaunch quota, read by
  the new `llm.turn.progress`.

- **`i` says one line into the session the focused pane is showing.** It hands the line to the
  `intervene` CLI rather than reimplementing it, which is what carries the hold on the
  session-timeout clock, the `operator` journal entry, and every refusal the command already makes.
  The target is refused rather than guessed when no pane has a session, and the modal names it above
  the field — with an orchestrator and a worker both live, "which one am I speaking to" is the
  question a mistyped intervention gets wrong.

- **The fork's own skills share one prefix: `rws-loop-*`.** Three of them had accumulated three
  different prefixes, so a name told you neither who owned it nor what it did — and one pair,
  `riaworks-bmad-loop-llm` and `rws-bmad-loop-llm-vigia`, both carried `llm` while being a machine
  protocol and a human-invoked watcher. They become `rws-loop-cli` (you call it; it operates the
  deterministic loop), `rws-loop-llm` (you call it; it watches an `llm-run` and may not write to it)
  and `rws-loop-core-llm` (the orchestrator protocol `llm-run` loads; never invoked by hand). What
  ships from upstream keeps `bmad-loop-*`, so ownership now reads off the prefix alone. `operador`
  is gone from the CLI-side name: it collided with `bmad-loop-resolve`'s operator flow, with
  `intervene`'s operator, and with the journal's `operator` kind — the name says which LOOP it
  drives, not which role.

- **`rules.toml` survives a reseed, and gains rules it lacks.** The file lives inside a bundled
  skill but belongs to the project — its thresholds, its gate markers, its tuned judgment — so
  `--force-skills` rmtree'ing the skill dir discarded configuration that existed nowhere else. It is
  now preserved across the replace, and `[[regra]]` blocks the shipped skill has and the project
  does not are appended by `id`, with their comments, under a marked banner. A shipped rule whose
  `id` the project already carries is never re-applied: the local copy may be a deliberate edit, and
  there is no way to tell that from a stale one — losing the deliberate case is the expensive
  direction. Thresholds stay out of the merge by design, since a key absent from the project file
  already falls back to the probe's own default, so a newly shipped knob works by being missing. An
  unparseable file is handed back byte for byte with nothing appended: growing a file nobody can load
  buries the syntax error its owner has to find.

- **`riaworks-bmad-loop intervene` — operator authority over a live session, with the journal as its
  price.** Reading a running session and typing into it were always possible with raw multiplexer
  commands; the engine's own repair path does exactly that. What was missing was everything around
  it. This routes reading, speaking, holding and note-taking through one command so acting and being
  recorded are the same step: `--say`, `--hold`, `--release` and `--note` all land in the run's
  journal under kind `operator`, so the record of what drove a story stays true when a human drove
  it. `--read` is deliberately not journalled. `--task` names the session; on an `llm-run` always
  pass it, since the orchestrator and a dispatched worker can be live at once and "freshest
  heartbeat" decides between them by a meaningless margin. Multi-line text is refused — the
  multiplexer submits at each newline, so it would arrive as several turns. `--json` emits an
  `INTERVENE_SCHEMA_VERSION` document under machine.py's contract: a document means the action
  landed, so a refusal or an undelivered `--say` leaves stdout empty with a nonzero exit rather than
  shipping an `ok: false` that invites treating a message the session never received as a soft
  outcome. Every key is always present, null where the action does not produce one, and
  `crediting_disabled` is explicit because a lease written under `operator_hold_max_min = 0` is real
  and buys nothing — the operator would otherwise believe the clock was held while it kept running.

- **A hold that stops the session-timeout clock while a human is talking.**
  `limits.session_timeout_min` is wall-clock and re-read only on `resume`, so a conversation inside
  a live session spent the session's own budget and could get it killed mid-work. `--say` and
  `--hold` grant a short lease (`limits.operator_hold_lease_s`, default 300s) that the wait loop
  credits to both deadlines. A lease and not a switch, for three reasons that are each a failure of
  the naive version: an operator who vanishes costs at most one lease before the ordinary ceiling
  resumes; a forgotten hold is bounded by `limits.operator_hold_max_min` (default 120, `0` disables
  crediting); and a host suspend cannot be laundered into credit, because a nap longer than the
  lease expires it — the one sanctioned exception to #157's "the wall clock may expire a deadline,
  never extend it", and sanctioned only because the other two bounds hold. Grant, lapse and
  exhaustion are recorded in `session-lifecycle.jsonl`. No new completion path: the session still
  ends on a hook Stop or window death.

- **The `operator` journal kind is excluded from the `llm-run` turn contract.** The supervisor
  classifies a turn by whether state or journal moved, counting every entry the orchestrator did not
  write off. Without the exclusion, a human speaking to a session would refill that evidence and a
  turn that wrote nothing — the one failure the relaunch budget exists to catch — would read as
  productive for as long as somebody kept watching. The masking would be worst exactly when someone
  is paying attention.

- **Two operator-side monitor skills, one per control loop.** `rws-loop-cli` watches a
  deterministic `run`/`sweep` and operates it — arm the vigilance, read the signals that separate
  work from a hang, run the runbook that puts the run back in motion. `rws-loop-llm`
  watches an `llm-run` and deliberately writes nothing: there every mutation belongs to the
  orchestrator's `unit` verbs under the run-dir lock, so the monitor only detects that the
  _supervisor_ stopped doing its job (dead supervisor, violation turns eating the relaunch quota,
  a pause nobody saw, a turn past the timeout, churn without progress). They are separate skills
  because their doctrines contradict; one skill stating both rules would leave the reader to pick.
  Each ships a `rules.toml` holding the thresholds, the project's gate markers and the decision
  rules — new judgment goes there, not into the prose — and each ships a probe (`heartbeat.py`,
  `pulse.py`) that reads the same file, so script and reader cannot drift. A rules file that is
  missing or unparseable degrades to defaults with a warning: a monitor that dies of its own
  config leaves the run unwatched, which is worse than a generic threshold.

- **`data/skills/` is exempt from the portability guards, and the exemption is self-defending.**
  Skill scripts are payload: copied out of the wheel into a project's skill tree and run standalone
  there, with `bmad_loop` not importable, so `verify.py`'s git chokepoint, the multiplexer seam and
  `process_host` are all out of reach — a monitor legitimately spawns `git`, `pgrep` and `tmux`
  itself. `test_skill_payloads_are_standalone` holds the line: nothing under that prefix may import
  `bmad_loop`, which is both what makes it payload and the shape a chokepoint bypass hidden under
  the exempt prefix would take.

- **The fork tracks upstream 0.10.0, and its out-of-tree state root is namespaced.** Merged
  upstream through `6945c60` (214 commits past the fork's previous base) and re-applied the
  footprint rename over everything new. One of those additions writes outside the project: the
  hook-event channel #494 moved each run's control plane under the user's state home, and that
  path is derived in `runs.state_root` — where `namespace.STATE_DIR` cannot police it. It now
  derives its segment from `namespace.PRODUCT`, so the two tools do not share
  `~/.local/state/bmad-loop/` keyed only by run id, and `test_namespace.py` pins both platform
  arms.

- **A refused auto-sweep is now visible outside the journal (#501).** A run whose deferred-work
  sweep was refused ended looking exactly like one that swept, and under `[sweep] auto = "run-end"`
  there is one trigger per run that is never re-asked once the run finishes — so the journal was
  the only trace. Runs now record `sweeps_refused` (trigger → reason), surfaced by the end-of-run
  summary, `bmad-loop status`, `status --json` and `bmad-loop diagnose`; the follow-up they name
  is `bmad-loop sweep`, which needs a clean worktree. The reason is a fixed slug — `not-started`,
  `failed` or `dirty` — never an exception message, which `diagnose` would refuse to emit at all.
  The `--json` key is additive and always present, so `STATUS_SCHEMA_VERSION` is unchanged.

### Changed

- **One package, one name: riaworks-waves.** Two repositories become one. The
  parallelism skills and the orchestrator that were deliberately kept apart — siblings that
  never imported each other — are now halves of a single package, under a single name, a
  single version and a single CHANGELOG. Nothing about how they relate at run time changed:
  the loop still never invokes the waves, and the waves still need only a BMad Method
  project and a coding CLI with subagents. What changed is that they ship together, upgrade
  together, and are named as what they are — one method.

  What the rename maps, old to new:

  | Was                                     | Is                             |
  | --------------------------------------- | ------------------------------ |
  | package `riaworks-loop-llm`             | package `riaworks-waves`       |
  | command `riaworks-loop-llm`             | command `riaworks-waves-loop`  |
  | import `riaworks_loop_llm`              | import `riaworks_waves_loop`   |
  | `.riaworks-loop-llm/` (state)           | `.riaworks-waves/loop/`        |
  | `RIAWORKS_LOOP_LLM_*` (env)             | `RIAWORKS_WAVES_LOOP_*`        |
  | `riaworks-loop-cli`                     | `riaworks-waves-loop-cli`      |
  | `riaworks-loop-llm` (the skill)         | `riaworks-waves-loop-watch`    |
  | `riaworks-loop-core-llm`                | `riaworks-waves-loop-core`     |
  | `riaworks-loop-deferred`                | `riaworks-waves-loop-deferred` |
  | `riaworks-loop-resolve`                 | `riaworks-waves-loop-resolve`  |
  | `riaworks-loop-setup`                   | `riaworks-waves-loop-setup`    |
  | `riaworks-loop-sweep`                   | `riaworks-waves-loop-sweep`    |
  | `riaworks-waves-run`                    | `riaworks-waves-plan-run`      |
  | branch prefix `riaworks-loop-llm/<run>` | `riaworks-waves-loop/<run>`    |
  | hook relay `riaworks_loop_llm_hook.py`  | `riaworks_waves_loop_hook.py`  |

  `riaworks-waves-run` became `riaworks-waves-plan-run` because it is not a second way in:
  it executes the plan the planner wrote, and the name now says so. The skill that watches
  an LLM-held run was called `riaworks-loop-llm`, the same string as the product — it is now
  `riaworks-waves-loop-watch`, which is what it does.

  **Upgrading a project.** Re-run `/riaworks-waves-loop-setup`, then delete what the old
  name left behind: move `.riaworks-loop-llm/` to `.riaworks-waves/loop/` (the runs and
  policy inside are read unchanged), remove the old skill directories from
  `.claude/skills/` and `.agents/skills/`, remove the old `riaworks_loop_llm_hook.py` relay
  and its `riaworks-loop-llm` group from the coding CLI's settings, and rename any
  `_bmad/custom/<old-skill-name>.toml` override to the new skill name — an override the
  resolver cannot find by name is silently not loaded, and the facts inside it stop
  applying.

  **The state directory is nested, not renamed sideways.** The epic-parallelism skills
  already wrote their run state to `.riaworks-waves/` — trackers, briefs, front worktrees —
  so a sibling `.riaworks-waves-loop/` would have read as a second, unrelated tool while
  being the same product, one name a prefix of the other and nothing saying which half owned
  what. One roof instead: `.riaworks-waves/` is the product and `loop/` is this half of it.
  The corollary is worth naming, because nothing in code can enforce it: the two halves now
  share a parent, so an `rm -rf .riaworks-waves` aimed at one takes the other with it.

  The module identity moved with the rest: `code: riaworks-waves`, display name
  `Riaworks Waves`, and one `.claude-plugin/marketplace.json` listing all nine skills. The
  BMAD installer now resolves the module by **strategy 2** (identity read from the `-setup`
  skill's `assets/`) rather than by strategy 1, because the merged module carries a `-setup`
  skill. The distribution artifacts (`scripts/build-dist.py`) still install the skills
  without the orchestrator, and now carry all nine.

  History is kept as it was written: entries below this one name the product as it was
  spelled at the time, and this repository's internal working notes are left alone. A
  changelog that is rewritten to match today's names is a changelog that cannot be trusted
  about yesterday.

- **The epic-parallelism pair is not bundled here.** `riaworks-build-parallelism` /
  `riaworks-run-waves` entered this module in an unreleased commit and leave it in the same cycle:
  they are their own package, `riaworks-waves` (a sibling directory in the development repository,
  published separately), under the names `riaworks-waves-plan` / `riaworks-waves-run`.
  `MODULE_SKILLS`, `init`, the wheel, `module-help.csv` and the marketplace carry the seven
  `riaworks-loop-*` skills only. Nothing in this orchestrator ever invoked them, so no behavior moves.

- **The product is `riaworks-loop-llm`, and every name it owns moves with it.** The fork
  carried the upstream trademark in its own product name, which their
  [trademark policy](TRADEMARK.md) does not permit for a distributed — let alone commercial —
  product: "Use 'BMad' or any confusingly similar variation as your product name" is listed
  under what a fork may not do. Naming it after compatibility ("Compatible with BMad Method")
  is expressly permitted and is what the README does now. Renamed together, from the single
  `namespace.PRODUCT` constant outward:

  | was                       | is                    |
  | ------------------------- | --------------------- |
  | `riaworks-bmad-loop`      | `riaworks-loop-llm`   |
  | `.riaworks-bmad-loop/`    | `.riaworks-loop-llm/` |
  | `RIAWORKS_BMAD_LOOP_*`    | `RIAWORKS_LOOP_LLM_*` |
  | `bmad_loop` (the package) | `riaworks_loop_llm`   |
  | `bmad-loop-*` skills      | `riaworks-loop-*`     |
  | `rws-loop-*` skills       | `riaworks-loop-*`     |

  **This breaks every initialized project.** The state directory, the env vars the hook relay
  reads, the tmux session names and the git ref namespace all move at once, so runs in flight
  do not survive the upgrade and the old hook registrations go stale. Finish or abandon open
  runs first, then re-run `riaworks-loop-llm init` to lay down the renamed relay and skills,
  and delete the stale `.riaworks-bmad-loop/` directory and the old hook entries by hand.

  **Out-of-tree extensions must re-declare their entry points.** The three discovery
  groups move with the package — `bmad_loop.adapters` -> `riaworks_loop_llm.adapters`,
  `bmad_loop.mux_backends` -> `riaworks_loop_llm.mux_backends`, `bmad_loop.plugins` ->
  `riaworks_loop_llm.plugins`. A package advertising the old group is not seen at all:
  the scan finds nothing and reports nothing, so the adapter or backend is simply
  absent rather than failing loudly. An external package that wants to serve both
  tools can declare both groups; nothing stops it.

  Names deliberately left alone: `bmad-build-auto`, `bmad-dev-auto`, `bmad-review-*`,
  `bmad-sprint-planning`, `bmm` and `_bmad/` are BMAD-METHOD's, not this tool's; `bmadconfig.py`
  reads BMAD's config and is named for what it reads; the `LICENSE` keeps BMad Code, LLC's
  copyright, as the MIT terms require.

- **Files the orchestrator replaces by name now land at `0600`.** Those writes pass
  `follow_symlinks=False`, and that mode deliberately carries nothing over from the target — not
  its permission bits, not its xattrs — so the new contents arrive at `mkstemp`'s private default.
  Affected: `.bmad-loop/decisions.json`, `.bmad-loop/policy.toml`, the park records under
  `.bmad-loop/operator/`, and any story spec written through `set_frontmatter_status`,
  `set_frontmatter_field` or `devcontract`. Most were already being reset to `0644` on every
  rewrite — the hand-rolled temp they replaced was created at `0666 & ~umask` and `os.replace`
  swapped _that_ inode into place — so for those the delta is `0644` → `0600`. Git records no mode
  but the exec bit, so nothing downstream of a commit notices.

  The no-follow choice is made per **file**, not per call site: once one writer of a file replaces
  it by name, every writer of that file has to, or they disagree about what the path means.
  Applying it that way brought four writers into line that had been direct
  `write_text`/`write_bytes` calls — `verify.safe_rollback`, the engine's park-record restore,
  `set_frontmatter_status` and `set_frontmatter_field`. Those four opened the name, and so wrote
  _through_ any symlink planted at it; they now replace it. That is a real change at those four,
  and what makes it safe is the same per-file rule: each of those files already had a
  name-replacing sibling writer (`policy.write_mux_backend`, `record_park`,
  `devcontract._atomic_write_spec`), so no link at those names survived the orchestrator anyway.
  Files with no name-replacing sibling keep following symlinks — `sprint-status.yaml` and your
  CLI's `settings.json`, both operator-curated, so a board or a config kept outside the tree and
  linked in keeps being a link.

- **`status --json` names the tree each task worked in.** Two additive per-task keys,
  `worktree_path` and `spec_file`, for the readers that have to look at the tree rather than at the
  counters: under `scm.isolation = "worktree"` a story's files and commits exist only in its
  worktree, and nothing in the document said which one. Without them an out-of-process reader — the
  `rws-loop-llm` monitor, which crosses a dispatched session's log mtime against the dirt in the
  tree it was dispatched into — had to read `state.json` behind the contract's back or not ask.
  `spec_file` is re-absolutized from `worktree_path` rather than reported verbatim, because
  `StoryTask` persists it worktree-relative and a document that changed shape depending on whether
  the caller had round-tripped the state would be no contract at all. `""`/`null` for an in-place
  run, which is the honest answer there. Additive per `machine.py`, so `STATUS_SCHEMA_VERSION`
  stays 1.

- **`atomic_write_bytes` accepts `follow_symlinks`, as its text sibling already did.** The default
  stays `True`, which the private-git-exclude writer depends on: it pre-creates the target
  precisely so the helper has a umask mode to carry over, and git silently ignores an exclude file
  it cannot read.

### Fixed

- **The dashboard painted the orchestrator's log twice on an LLM-held run that had not
  dispatched yet.** The orchestrator column and the Log tab pick their target by different
  readers: the column asks for the open session whose `session-start` recorded
  `role="orchestrator"`, while the tab's auto-follow goes through `active_task_id`, which is
  role-blind and answers "whichever session started last". Before the first dispatch that is the
  orchestrator, so both halves of the screen showed one file and the dashboard looked like it was
  watching two sessions while one was up. `03bc9be` knew and deferred it, because correcting the
  single-id reader in place would have moved a default its own tests pin; the tab now selects
  `data.worker_task_id` instead, on LLM-held runs only. It has no fallback at all,
  deliberately: the newest file in `logs/` during a dispatch gap IS the orchestrator's, so a
  fallback would restore the duplication by the back door on precisely the runs this was written
  for. With no worker open the pane says `— no work session — the orchestrator holds the turn,
watch the column →` — where the work actually is. `n` still cycles onto the orchestrator while
  a worker runs beside it; an explicit choice was never the duplication, and it cannot revive an
  ENDED session (it walks the run's open ones) — the Journal pane's jump is what reaches a
  finished worker's log. Every other run keeps the old reader and its fallback,
  orchestrator-named sessions included.

  It was not only cosmetic. `i` submits into the session the focused pane is showing, read off
  `_displayed_log_task` — so on the Log tab it typed into the orchestrator, against a tab the
  guide documents as reaching the worker, and against the docstring that refuses to guess
  precisely because the cost is a message delivered to the wrong agent. A waiting pane now
  answers None and the prompt declines.

- **The watcher spawn spelled its own detach, breaking the typecheck gate and evading the
  portability guard.** `llm/dispatch.py` picked the detach kwarg inline instead of calling
  `platform_util.detach_kwargs`, and both halves of that duplication cost something. Naming
  `subprocess.CREATE_NEW_PROCESS_GROUP` unguarded is a pyright error everywhere the attribute does
  not exist — i.e. on POSIX, where CI runs `uv run pyright` — so the `typecheck` job was red on the
  branch. And writing the POSIX half as `kwargs["start_new_session"] = True` is neither a call kwarg
  nor a dict literal, the only two forms `test_start_new_session_only_in_detach_helpers` scanned,
  so the site sat outside `DETACH_ALLOW` unnoticed. The call now routes through the helper (same
  kwargs on both platforms — this is a consistency and gate fix, not a behavior change), the guard
  learns the subscript form, and `spawn_watcher` gains the direct coverage it never had, including
  that an unstartable watcher is an `env` fault rather than the story's.

- **The monitor measured a dead orchestrator session, so every turn after the first raised a
  permanent false alarm.** `pulse.py` picked the orchestrator session with `next()` over the journal
  in chronological order, which returns the FIRST — but the supervisor opens a new orchestrator
  session on each turn relaunch and all of them stay in the journal, so in any long run it was
  reading a corpse. Measured 2026-08-22 in run `20260822-095341-34b9`: `orchestrator-1` died at
  14:10 on an authentication screen while `orchestrator-3` was writing in the current second. Three
  readings came off the wrong file — the reported `turno_task` (which sends a human to talk to a
  session that is gone), the heartbeat read from `tasks/<id>` (why `turno_restante_s` froze at a
  fixed value), and the log mtime in `silencio_do_turno`. The last is the expensive one: a dead log
  never grows again, so the measured silence climbs without a ceiling and `turno-silencioso` can
  never clear, costing the watchman the only signal that separates a stalled turn from a working
  one — and `turno-silencioso` recommends reading the orchestrator's log before stopping anything.
  It now takes the most recent orchestrator `session-start`. Nothing else in the script had the same
  shape: `silencio_do_turno` already iterated in reverse, the alert row already took `alertas[-1]`,
  and the two chronological walks that remain need that order.

- **The dev and review gates demanded mutually exclusive board values on an isolated story.** With
  `[review] enabled = false` the dev session finalizes straight to `done` and its gate is the last
  one, so it demanded a board reading `done` — while `verify_review` demanded `awaiting-merge` for
  the same story. `sprintstatus.advance` never regresses and `awaiting-merge` precedes `done`, so
  the two were not merely inconsistent but mutually exclusive in one direction: satisfying dev put
  the board past `awaiting-merge` permanently and closed review for good, and satisfying review
  failed dev. Fixing either alone left the other standing (measured 2026-08-22, run
  `20260822-095341-34b9`, where the orchestrator had to choose one and judge the story on evidence
  it gathered itself). `verify_dev` now takes `merge_pending`, exactly as `verify_review` does, and
  applies it only on the `done` branch — the `review` board between dev and review precedes the
  merge either way, and a park is already merged. One board value satisfies both gates, and it is
  the one git backs. Caller-supplied for the same reason `operator_park` is: the deterministic
  engine has no `awaiting-merge` call site and still gets the flat `done` it needs, and
  `verb_verify` derives the flag from the same `task.worktree_path` that decides the review gate's
  `merge_pending` and `verb_close`'s `isolated`, so the three cannot disagree. Per-configuration,
  not a widening — an in-place story is still refused a board parked at `awaiting-merge`.

- **The LLM loop's review gate could not pass an isolated story, whatever the story did.** Under
  `[scm] isolation = "worktree"` the finalized spec exists only in the story's worktree until the
  merge, while the shared checkout keeps the baseline's `planned`. `StoryTask.spec_file` is
  "absolute in memory and worktree-relative on disk" — `to_dict` re-roots it so a kept run's
  `state.json` survives the worktree moving — but the round trip is ASYMMETRIC: `from_dict` hands
  the relative form straight back, and whoever loads it owes the other half. The deterministic
  engine pays that debt when it reopens the unit (`worktree_flow`); the LLM host never did, so every
  reader resolved the path against the ORCHESTRATOR's cwd and the gate reported `spec status is
'planned', expected 'done'` for a story whose spec said `done` the whole time. Nothing a session
  did inside the worktree could move the file the gate was reading: unpassable by construction, not
  a failure on the merits (measured 2026-08-22, run `20260822-095341-34b9`, story 6-10b, where the
  orchestrator had to substitute its own reading at both gates twice). `LLMHost` now restores the
  in-memory form on load, `_stamp_spec_file` resolves a session's claim against the tree that holds
  the work, and `verify_dev` resolves the claimed spec through the same `work_root` seam its
  proof-of-work check already takes. Only the relative-with-a-worktree case moves — an in-place run
  and a spec outside the worktree are both persisted verbatim, and re-rooting either would invent a
  path nobody wrote.

- **A crooked spec stamp fixed itself permanently, and killed the correction written to undo it.**
  `_stamp_spec_file` kept any stamp that still named a READABLE file — a predicate chosen
  deliberately, so a live stamp stays authoritative and a stale re-dispatch cannot overwrite a good
  record. Under isolation readable stopped being enough: the shared checkout's copy of the spec is
  readable AND wrong, so the first bad stamp became permanent and the review path's own re-stamp —
  added for exactly this correction — was guarded out by the function it calls. That is why the
  failure read "can never pass" rather than "failed this time". Live now means readable IN THE TREE
  THAT HOLDS THE WORK; with no worktree the two readings coincide and the original predicate stands
  unchanged.

- **`validate` now says when a project's bundled skills have fallen behind the wheel.** The skills
  are COPIED into the project by `init`, exactly like the hook relay `hooks.relay-stale` has
  reported on since #494, and nothing said the same for them. Measured 2026-08-18: a project was
  running `rws-loop-llm/pulse.py` 110 lines behind its source — missing `turno-silencioso` and
  `teto-nao-disparou`, two findings that had existed upstream for weeks — and the only symptom was
  silence through an incident those findings would have named. `skills.module-stale` compares every
  installed bundled skill against the packaged one and names the files that differ. A warning, not
  a problem: a stale skill still works, and the exit code does not move. `rules.toml` is excluded —
  it belongs to the project, `init` merges rather than overwrites it, and a tuned threshold is not
  staleness — as is `__pycache__` bytecode, which an editable install grows beside any skill script
  that has been imported. The check lives in `validate` because `validate` runs in the TARGET
  project; this repository's canonical-vs-seeded drift test only ever grades its own checkout, and
  is structurally blind to the skew that matters.

- **More messages pointed an LLM-held run at a `resume` that refuses it.** The same defect as the
  `resume` refusal above, on paths that never read `state.source`: the graceful-stop messages (CLI,
  TUI, and `runs.request_graceful_stop`'s dead-engine refusal) and every escalation `WorktreeFlow`
  raises — including the merge refusal at the centre of the 2026-08-18 incident — named
  `riaworks-bmad-loop resume <id>` unconditionally. That command exits 2 on an `llm` run by design,
  so following the suggestion spends the operator's trust before telling them anything, and an
  unattended orchestrator copies the sentence into the alert it writes for its owner — which is
  exactly what happened. `namespace.resume_command(source, run_id)` now answers the question in one
  place, beside the rest of this fork's operator-facing spelling, and `runs.resume_hint(run_dir)`
  reads it for the callers holding only a run dir (never raising: an unreadable `state.json` falls
  back to the deterministic spelling rather than taking down the surface trying to be helpful).

- **`unit close`'s merge-back failure read as a dead end, so the 2026-08-18 incident paused the run
  over a verb that was retryable the whole time.** `verb_close` sets a story's terminal phase before
  it integrates the unit's branch back, on purpose — integration reads the phase — and `_set_terminal`
  already tolerates a task that is already at the phase it is asked for, precisely so a crash or
  refusal mid-integration leaves the story re-closable. None of that reached the operator: a failed
  `integrate_unit` surfaced only `could not integrate 4-5: <git error>`, which named the failure and
  said nothing about the retry, so two finished, reviewed stories sat outside `master` for hours
  while the orchestrator asked a human for help it did not need. The `git`-kind error `verb_close`
  raises now names the story, states that it is already at its terminal phase with its worktree still
  mounted (and where), and says that calling `close` again with the same outcome resumes the
  integration without redoing the work; `rws-loop-core-llm`'s `git`-kind reference carries the same
  instruction, since the fixed message only helps if the orchestrator's protocol already expects it.

- **`stop` on a paused run never made it terminal, so the monitor alarmed on it forever.** A pause
  ends the engine process by design, so when `stop` arrives there is nothing alive to observe it and
  transition the run: it set `stopped` and every surface went on answering `paused`. The
  `rws-loop-llm` monitor reported `run-pausado` at `act` on every tick, indefinitely, over work
  somebody had already closed — the noise that teaches an operator to ignore the alarm, which is the
  same alarm owed the next real finding. `status --json`, `list --json`/the dashboard and the
  human-readable `status` now all read a stopped pause as terminal. Nothing is cleared to say so:
  `paused_reason` survives and is still reported (the text line names it, "was paused at …"), so a
  consumer crossing the raw pair can still tell a closed pause from an orphan one — which is what
  keeps the monitor's `pausa-encerrada` reachable. Written as an extra conjunct rather than a
  reordering, so exactly one combination moves and every other precedence stands.

- **Nothing crossed the board against git, so `done` could mean "the merge was refused".** The
  incident's cheapest and earliest symptom, and the one nobody had a name for: `sprint-status.yaml`
  marked two stories `done` while `master` contained neither, because the merge guard refused both
  and the board recorded gate approval as delivery. Four hours of `severity: ok` over two proven
  stories outside the integration branch. `pulse.py` now runs one
  `git merge-base --is-ancestor` per `done` story of the current run and reports
  `quadro-diverge-do-git` at `act` when the integration branch does not contain it — deterministic,
  one cheap git call per story, and it speaks at the minute of the first refused merge. Like
  `encerrado-sem-concluir` it is a finding about CONCLUSION, so a terminal run does not silence it:
  a board that lies about delivery is what the _next_ run reads to choose scope. A ref git cannot
  resolve (the branch a successful merge teardown already deleted) stays "did not measure", never
  divergence. `status --json` gained the two fields the test needs — per-task `branch` and run-level
  `target_branch`, additive, so `STATUS_SCHEMA_VERSION` does not move — keeping the monitor on the
  public contract instead of reading `state.json` behind it.

- **The same orchestrator alert reached its owner eight times in consecutive ticks.** `pulse.py`
  took the last `llm-attention` entry and returned the raw text, so nothing distinguished a new
  message from one already reported, and the monitor repeated it every tick. A channel that repeats
  itself dies of repetition — and the alarm the operator learns to ignore is the same one owed the
  next real finding. The report now carries `alerta_id` (a hash of the text, also printed in the
  finding itself) and `alerta_n` (how many alerts the journal holds), and the
  `alerta-do-orquestrador` rule tells the reader what to do with them: an unprecedented alert speaks
  in full, a repeat fits in one line citing the id.

- **The shared checkout's HEAD had no vocabulary at all.** Unreviewed code reached `master` through
  it once already, via a cwd bug in a dev session — that bug is fixed, but the signature covers the
  whole class: the main checkout moving without a merge journalled beside it. `pulse.py` now reports
  `head_projeto` (sha + branch) and `merges_n` (`unit-merged` entries), and the new
  `head-compartilhado-mexeu` rule owns the comparison across ticks. Deliberately facts plus a rule
  rather than a finding in the script: the pulse writes nothing anywhere, because every mutation of
  a run belongs to the verbs under the run-dir lock, and state parked beside the run would put a
  second writer exactly there — with two monitors racing for it.

- **A paused LLM-held run was unrecoverable: `resume` pointed at a flag that did not exist.**
  `riaworks-bmad-loop resume <id>` refuses a run whose `source` is `llm` and tells the operator to
  use `llm-run --resume <id>`; `llm-run` had no such flag, so the answer was
  `error: unrecognized arguments`. Measured on a run that had paused with two finished, proven
  stories still outside the integration branch: the only way out was to integrate by hand and
  launch a fresh run — which cuts new worktrees from the branch as it stands _now_, the exact
  damage the run paused to avoid. `llm-run --resume <run-id>` now exists with the spelling the
  refusal already promised. It adopts the run dir, its journal and its mounted worktrees rather
  than minting a run (`llm.supervisor.resume_run`, the sibling of `open_run`), and mirrors
  `cmd_resume`'s bookkeeping: config.yaml and policy.toml are re-read from disk, the policy
  snapshot and the host-exec integrity pin are re-stamped (both copies, the out-of-tree one and
  the one travelling in `state.json`), a stale graceful-stop request is discarded, and the pid
  lands before the cleared pause so no observer sees "not paused + dead pid". Refuses, with the
  same exit codes the deterministic path uses: an unknown or unreadable run, a finished run, a
  live run (two supervisors on one `state.json` is corruption), launch-time scope flags
  (`--epic`/`--story`/`--max-stories`, pinned in run state and silently ignored otherwise), and —
  symmetrically with `resume` refusing an `llm` run — a non-`llm` run, pointing back at plain
  `resume`. A stopped or crashed llm-run re-arms rather than being refused, the same choice
  `RunState.clear_pause` already made for the engine. The turn counter is seeded from the run's
  own journal, so a resumed run relaunches as `orchestrator-<n+1>` instead of overwriting the task
  dir, session result and pane log of the turn the operator resumed to act on; the relaunch budget
  deliberately starts fresh, since the run paused _because_ that budget ran out and carrying it
  forward would re-pause on the same reason.

- **The `rws-loop-llm` monitor answered `ok` at a run that had died mid-story.** Measured
  2026-08-18: `status = stopped`, `finished = false`, story 4-8 parked in `dev-running` — and
  `pulse.py` reported `severity: ok` with zero findings, because `stopped` enters its `terminal`
  calculation and `terminal` suppressed every finding it had. A run that died without concluding
  read exactly like a healthy one, which is the worst failure mode an alarm has. Findings are now
  two families: terminal may silence a PROCESS finding (dead supervisor, silent turn, mute session
  — things that mean nothing without a process), and may never silence a CONCLUSION finding. New
  `encerrado-sem-concluir` at `act` names every story left outside a terminal phase when the run
  ended.

- **A story could sit `escalated` for hours while the monitor reported `ok`.** `status --json`
  already carried `tasks[].phase` and `pulse.py` loaded the dict and threw it away, so no field of
  its report could see `escalated` or `deferred` — measured 2026-08-18, four hours until the
  orchestrator itself complained. The phases now reach `facts.fases`, and a terminal-without-
  delivery phase on a still-running run is a `story-parada` finding at `act`.

- **A paused run that had already been stopped reported `run-pausado` forever.** `stopped` only
  turns true after an explicit `stop`, so paused-and-stopped is a third recognizable state:
  somebody already came, saw the pause and closed the run. It now reports `pausa-encerrada` at
  `watch` ("archive it") instead of repeating an `act` over finished work — the kind of noise that
  teaches an operator to ignore the alarm that matters. The pause itself is still decided before
  `terminal` and still wins, so an orphan pause keeps its own finding.

- **A frozen session read as a live one, because the monitor trusted the heartbeat.**
  `heartbeat.json` is written by the adapter's WAIT LOOP, not by the session doing the work
  (`llm/watch.py`), so it proves the waiter is waiting and nothing else: a session dead on an
  `API Error: 500` keeps it perfectly fresh forever. Measured — twelve minutes after death, log at
  the same mtime, worktree untouched, heartbeat showing six seconds of freshness, and a human
  reader called the session "alive and producing". The corollary is structural and now stated in
  the code: the adapter's own `stale-heartbeat` condition _cannot_ catch a frozen session, since
  what freezes is not what writes, and tightening its threshold never will. `pulse.py` now crosses
  the two signals that do prove work — the session's log growing, and the tree it was dispatched
  into getting dirty — over every dispatched session with no `session-end`, and reports
  `sessao-muda` at `act`. An unmeasurable tree stays "not measured", never "clean".

- **An isolated session was dispatched into the shared checkout, so the story's commit came out
  empty.** `verb_dispatch` launched every session with `cwd = paths.repo_root`. Under
  `scm.isolation = "worktree"` that is the wrong tree: the session edits the shared checkout while
  the story's worktree stays untouched, the unit commits nothing, and every gate downstream is
  measuring a story that — as far as its own branch is concerned — never happened (measured
  2026-08-18, run 49e2, story 4-5). The session now runs in `task.worktree_path` when the task
  records one, and in the repo root otherwise, which is still right for in-place runs and for any
  story dispatched before `unit open` mounts anything.

- **A `spec_file` stamp that no longer named a file was kept forever, and the gates reported an
  empty status for it.** `_stamp_spec_file` guarded on `if task.spec_file: return` — first write
  wins, permanently — and stored the claim unresolved. Both halves misfire under worktree isolation:
  a stamp can name a path inside a worktree the merge has since torn down, and an un-normalized
  path (one carrying a `..` segment the session composed from its own cwd) fails to match git's own
  normalized output, so the dev gate's exclude silently evaporates. Neither failure is loud: an
  unreadable spec makes `_gate_frontmatter` read nothing and the gate answers `spec status is ''`,
  which reads as a session that forgot to finalize. The stamp is now stored resolved, and is
  replaced when it stops naming a readable file — while a stamp that still resolves stays
  authoritative over any later claim.

- **The LLM path's dev and review gates measured the main checkout, so the review gate went green
  testing the baseline.** Under `scm.isolation = "worktree"` a story's commits and files exist only
  in its worktree until the merge. The deterministic engine never notices — it runs each unit with
  `paths` rebased onto that worktree — but the LLM-held loop cannot do the same, because it must
  read the sprint board from the MAIN checkout (`unit sprint-advance` is its sole writer and writes
  it there). Both gates therefore asked the wrong tree. `verify dev`'s proof-of-work check answered
  "no changes in worktree since baseline commit" for every isolated story, with the commit sitting
  readable in the worktree — a gate that is inert exactly when isolation is on, failing stories that
  did the work. `verify review` ran the deterministic verify commands in the main checkout, which is
  worse: it PASSED, on the baseline, for a story it never opened, and nothing downstream re-checks a
  green review. `verify_dev`/`_verify_shared_gates` take a `work_root` and `verify_review` a
  `commands_root`, both defaulting to `paths.project` so the engine is unchanged, and the verb
  supplies the story's worktree when one is mounted and readable. The dev gate's exclude derivation
  now relativises a candidate against either root, since the session's spec is absolute inside the
  worktree while the board stays absolute in the main checkout and neither root alone reaches both.
  `verify review` also re-stamps `task.spec_file` from the REVIEW session's own claim (falling back
  to dev's), since the review session is the one that finalized the document.

- **The merge guard refused over the orchestrator's own bookkeeping, and two proven stories sat
  outside the target branch for hours.** `clean_incoming_collisions` treats uncommitted changes to
  TRACKED files outside a branch's incoming set as operator work and escalates, because
  `merge_strategy = "squash"` would fold them into the story's commit (#460). On the LLM path the
  sprint board and the deferred-work ledger are exactly that shape and are not operator work:
  `unit sprint-advance` is the board's sole writer and targets the MAIN checkout, and `unit ledger`
  writes the ledger there while a story is in flight, so every story after the first arrived at its
  own merge with the target already dirty. Measured on a real run: two finished, reviewed stories
  with green gates, neither integrated, the run paused asking for a `resume` that does not exist for
  its source. `merge_local` now hands the guard a `tolerate` allowlist naming those two files and
  nothing else — they stay ordinary tracked files, walked past rather than cleaned or reverted, so
  whatever the orchestrator wrote is still in the checkout after the merge. Every other tracked file
  keeps escalating, exactly as before.

- **The LLM monitor's stale-turn finding measured duration, which is not a symptom.** A healthy turn
  spans story after story — in an LLM-held run turn 1 may not close for a whole epic — so any
  "open for X minutes" threshold only defers the false positive to the next number. The criterion is
  silence: a turn that writes nothing, to neither the journal nor its pane log, is stuck whether it
  is ten minutes or ten hours old. The ceiling observation survives as a separate `watch` finding,
  because a session outliving `limits.session_timeout_min` proves the adapter's timeout did not fire
  — a defect in the mechanism, not in the turn, and never on its own a reason to stop live work.
  Turn findings are also gated on a live run now: a paused or finished run leaves its last
  `turn-start` unpaired, and reporting that residue as silence flagged the ordinary end of the day
  as an illness.

- **An LLM-held run reported zero tokens however much it spent.** Same root as the broken dev gate:
  the deterministic engine records a finished session onto its task — `record_session` plus
  `attach_session_usage`, which is what makes `task.tokens` add up — and this loop had no equivalent
  moment, so `sessions` stayed empty and the dashboard's token column sat at 0 for the life of a run.
  The watcher already read the usage and journalled it; it now also persists it beside the settled
  result, in a file of its own written after it (the result is what a caller waits on and must be
  durable; usage is metadata the engine itself treats as best-effort). `await` and `session-result`
  absorb the settled session onto the task — whichever first observes it — under the run-dir lock,
  and idempotently by task id, because a caller polling until settled must not add the same usage
  once per poll. Recorded where the orchestrator observes the outcome rather than in the watcher: the
  watcher is a detached process and must not contend for the lock with the turn that is driving.

- **`unit verify dev` failed every story on the LLM path, and took `unit verify review` with it.**
  Two independent defects in one verb, found by an orchestrator that had to hand-check its own gates
  against verify.py's docstrings rather than use them. It read the session's claim from
  `task.sessions`, which only the deterministic engine ever writes (`engine.py` holds the lone
  `record_session` call), so on this path the list is always empty and the gate answered "dev
  result.json missing spec_file" while the claim sat readable in the settled session-result file.
  And it passed `policy.review.enabled` straight through where the engine asks a narrower question:
  the generic `bmad-build-auto` skill self-finalizes to `done` with no in-review handoff, so the verb
  demanded `in-review` from correctly finished specs. The rule moves to
  `devcontract.dev_review_enabled`, which both loops now call — they were answering the same question
  differently, which is what a shared rule exists to prevent. `verify dev` also stamps
  `task.spec_file` from the claim it just read, the way the engine does when it accepts a dev result:
  `verify review` reads that field and nothing on this path was writing it.

- **`[llm] turn_timeout_min` was removed, not implemented.** It sat in the policy, was parsed, was
  exposed in the settings schema, and no executing code ever read it — the kill-and-relaunch it
  advertised was never built. It is also unnecessary: `supervisor._run_turn` builds the orchestrator
  session through the same `build_spec` every dispatched session uses and waits on the same
  `wait_for_completion`, so a wedged orchestrator window is already killed by
  `limits.session_timeout_min` and comes back as an ordinary `timeout` turn outcome. A second ceiling
  over one session would only have fought the first, and at the 30-minute default it advertised it
  would have won — killing turns that are long by design, since a turn is meant to span a story and
  often an epic. A policy.toml still carrying the key stays inert rather than erroring.

- **`limits.operator_hold_lease_s` and `limits.operator_hold_max_min` were defined but never read.**
  Both existed on `LimitsPolicy` with matching `core.toml` entries, and neither was mapped in
  `policy.load` — so a project that set them, including the `= 0` kill switch for hold crediting,
  was silently ignored. The core.toml sync test compares defaults and options, not whether the
  loader ever looks at the key, so a dead knob passes every other check; `test_policy.py` now pins
  the round trip.
- **Overlong lowercase/kebab sweep bundle labels now proceed deterministically (#503).** An
  otherwise valid name over 40 characters is truncated to 40, journaled and persisted before
  validation, so the sweep proceeds without spending a feedback retry or pausing the run.
  Post-truncation collisions and other invalid shapes still fail validation.

- **Silent OpenCode parent sessions now enter bounded recovery from launch (#411).** Parent/child
  SSE activity and a provably busy or retrying parent re-arm the grace; true silence spends the
  bounded nudge budget and is classified `stalled`. This neither prevents upstream subagent
  interruption nor guarantees that best-effort `prompt_async` nudges wake it.

- **Generic and OpenCode dev/review stall grace now arms at launch and re-arms on activity (#470).**
  Pane/SSE activity and later turn-end evidence restart the grace, so a truly silent live session
  spends its configured bounded nudges and becomes `stalled` near the grace sequence instead of
  necessarily consuming all of `session_timeout_min`. Completion still requires Stop/idle evidence
  or window/server death plus deterministic artifact verification; prose never completes a session.

- **Dead targets no longer abort the generic completion loop from its two nudge sends (#504).** The
  stall and result-less-Stop sends alone contain `MultiplexerError`, after which deterministic
  liveness and artifact logic decides `crashed` or `stalled`; this is not blanket multiplexer failure
  tolerance.

- **Path-resolution refusals no longer tear down worktree runs mid-provisioning (#556).**
  Observation probes report coarse unknown entries, each refused seed is skipped independently,
  provisioning-root uncertainty raises a typed escalation and pauses before any write or session,
  and mount uncertainty defers only the affected unit. Required upstream-skill absence still
  escalates; this boundary does not include `ProjectPaths` or confined cleanup resolution.

- **Rollback path uncertainty now triggers a pre-destructive rollback pause (#557).** Trusted
  spec containment fails closed, observational exclude and story derivation use explicit
  fail-open or empty fallbacks, collision uncertainty keeps and escalates the branch, and exact
  commits omit only an uncertain candidate after a trusted root is established. This is limited
  to the audited verify and recovery boundaries, not every path-resolution call.

- **The dashboard now survives project-root resolution refusal with unavailable panes (#558).**
  Startup and polling retain empty or unavailable views through one stable lexical/canonical
  cache spelling. This preserves the dashboard around a dead provider; it does not recover the
  provider or make it operational.

- **Advancing a sprint board now preserves every authored line ending (#576).** A valid UTF-8
  board keeps each CRLF, LF, bare-CR or mixed per-line terminator while the requested story,
  conditional parent-epic and optional `last_updated` values still change. Previously the
  read/write relay could translate the whole board to the platform line ending, producing
  newline-only diff noise outside those intended value edits; parsed YAML content was not
  corrupted.

- **A `sweep --migrate` rewrite that drops a `gate:` token a pre-existing entry declared is now
  refused, instead of un-gating that story silently (#519).** Validation held the rewrite to each
  entry's id and status only, so losing the token passed, got committed, and the next dispatch ran
  the story the entry existed to hold back. The original ledger is now restored and the session
  re-prompted with the error, escalating after `max_migration_attempts` — a rewrite that previously
  passed can now fail. An _added_ token is still accepted, since over-blocking fails loudly and in
  the safe direction. Migration-scoped: every other ledger edit is still held by the format doc's
  instruction alone.

- **`sweep --migrate` now refuses a ledger that already carries duplicate `DW-<n>` ids, rather than
  migrating it into silent data loss (#519).** One id naming two entries cannot survive a migration
  either way: the rewrite that keeps both is rejected as duplicate, and the one that passes collapses
  them and drops a twin's `gate:`. The sweep now pauses before any rewrite is dispatched, naming the
  ids to renumber, and resumes with its migration budget intact. **A deliberate behavior change
  beyond #519's original scope:** such a migration completes today by losing that data, and will now
  stop instead. Bounded to ledgers that already carry duplicate ids.

- **An unrelated untracked file in your main checkout no longer blocks every isolated unit merge
  (#460).** Under `[scm] isolation = "worktree"` the pre-merge reconcile refused over any dirty path
  outside the unit branch's incoming set, untracked included, so a single `notes.txt` escalated the
  story and paused an unattended run. A merge writes only the paths that differ between target and
  branch and never stages an untracked file into the commit, so untracked dirt outside that set is
  now left where it is, the merge proceeds, and the run journals `merge-target-tolerated` naming it.
  Uncommitted changes to **tracked** files still escalate — `merge_strategy = "squash"` would fold
  them into the story's commit. Reaches dirt that appears after the run starts, and every `resume`.

- **The escalation that remains no longer blames a game engine (#460).** It asserted that "likely a
  Unity Editor wrote into the main project" on every isolated merge — the guard's origin story
  rather than a diagnosis, fired on repos with no Unity anywhere and no plugins loaded — and told
  you to "clean them", which is the exact verb the reconcile performs with `unlink` on its own
  paths. It now names the tracked files, asks you to commit, stash or revert them, and demotes a
  `per_worktree` engine Editor to one possible cause beside ordinary local work.

- **A git that warns while still exiting 0 no longer corrupts the answers the orchestrator reads
  back from it (#442).** An unknown `core.fsyncMethod` value or a `core.fsmonitor` hook that cannot
  exec is a property of the host's git config rather than a failure, but the shared git helper handed
  callers `stdout` and `stderr` merged — so every probe that read git's text as the ANSWER took the
  advisory for data. Silently: a rollback candidate list grew a phantom path, a commit list grew a
  phantom sha, and the sha and branch probes answered with the warning appended — the last of which
  reached the baselines persisted in run state, so a resume graded a warning-carrying string against
  a clean one and read "moved". Loudly: preserve-ref retention raised `PrunePreserveError`,
  `commit_paths` raised where its contract reports nothing to commit, and the worktree snapshot
  failed outright — which since #340 is a gate and not a safety net, so a noisy host had no working
  rollback at all. Thirteen value-reading probes now take stdout alone; the ~45 call sites that only
  check a return code are unchanged, and a failing git call still carries its stderr.

- **An indented, tab-separated or empty heading in the deferred-work ledger no longer lets a `gate:`
  below it hold a story the entry never named (#516).** A canonical entry ended only at a `#` run at
  column zero with exactly one space after it, so three shapes CommonMark spells as ATX headings —
  up to three spaces of indent, a tab as the separator, and an empty heading — ran on past the
  section header and absorbed the next section's field lines. A later `gate:` then landed in an open
  entry that had declared nothing: `validate` failed (`deferred.hard-gate`) and `run` paused
  (`story-gate`) on a story that entry never gated. Two reads move with the boundary: a `status:`
  below such a heading is now that section's rather than the entry's, so the entry parses with no
  status and leaves the open set; and a tail below one is no longer masked by an over-long span and
  reaches the legacy parser again. Four spaces of indent or a leading tab is an indented code block
  rather than a heading and still ends nothing, and a heading nested in a list item or a blockquote
  (`- ## Notes`) is still not a boundary either — the same line-scope limitation as #327.

- **Launching with a `--run-id` that already names a run is refused (#602).** The flag pointed at an
  existing run adopted that run's directory and published its own `state.json` over it. The id is
  now claimed exclusively as the directory is created, so a collision aborts the launch before
  anything is written and the earlier run is left untouched.

- **A launch that aborts while standing up its adapters no longer strands an empty run (#602).** An
  adapter failure left a run directory with no `run-start` that nothing reconciled, so it lingered
  in `bmad-loop list` looking resumable. Composition is now atomic from the first published
  artifact: on any escape the run directory and its out-of-tree state are removed and the original
  error is re-raised unchanged. The removal keeps the live-session guard, and a removal that itself
  fails is now reported instead of passing silently.

- **A failing auto-sweep can no longer kill its parent run, and a stop during one is no longer
  swallowed (#600, #601).** A `SystemExit` from the child — what an unusable multiplexer or an
  unresolvable profile raises — escaped every handler and ended the process at exit 1, leaving the
  parent neither `finished` nor `crashed` with an orphaned agent session. In the other direction a
  stop was recorded as a child failure, letting the parent run on to `finished` and leaving it
  unstoppable. `KeyboardInterrupt` deliberately still escapes.

- **A run's `sweeps_triggered` records only auto-sweeps that actually started (#501).** The trigger
  was spent before anything had been attempted, so every way a child could decline to launch
  consumed it — including a plain `git status` timeout, which fails closed and could silently burn
  a run's one and only sweep. The tree check now runs ahead of the record and journals a `reason`
  distinguishing a git fault from real local changes. Not a retry: what this buys is that
  `bmad-loop diagnose` stops reporting sweeps that never ran. A child that fails after its run
  directory exists still spends the trigger; the never-launched case journals
  `sweep-auto-not-started` and keeps its own notification.

- **A failed write can no longer truncate the sprint board, a story spec, your CLI settings or your
  policy file (#379).** Seven writers read a file, merged into it, and wrote the whole thing back
  through a truncating `Path.write_*` — so a fault partway through (ENOSPC, EIO, a quota) published
  a _prefix_ of the file and destroyed the rest. All seven now go through
  `platform_util.atomic_write_text` / `atomic_write_bytes`: contents to a temp, fsync, replace.

  Most of these fail _quietly_ — the file still parses afterwards, so nothing downstream raises:

  - **The sprint board.** `sprintstatus.advance` is the orchestrator's sole write path to
    `sprint-status.yaml`. YAML cut at a line boundary is still a valid mapping, just a smaller one,
    so the epics past the tear ceased to exist and the run walked off the end of the sprint instead
    of erroring.
  - **A story spec.** A spec is laid out `before + edited + after`, so a write that faulted after
    the frontmatter had landed left intact frontmatter saying `status: done` over a decapitated
    body — a spec that lies, which the loop then commits. `set_frontmatter_status`,
    `set_frontmatter_field` and `devcontract`'s four in-place rewriters now share one call.
    `devcontract` was already atomic and recorded the measured cost: fault injection on the old
    truncating write cut a 46-byte spec to 12.
  - **`.bmad-loop/policy.toml`.** `safe_rollback` captures it before the `git reset --hard` and
    writes it back after, so your orchestration config survives a rollback whether or not it was
    committed. A truncated TOML is not a smaller config — it is a parse error the next `run`
    refuses on, which is the failure the whole restore exists to prevent.
  - **The park records.** The engine restores a story's record when the commit it was written for
    fails. A record left truncated reads as a park owing nothing, while the board still says a
    human owes something.

  Your CLI's `settings.json` is the loud one. Both writers that register the completion hook —
  `init` and each isolated worktree's provisioning — parse the whole config, merge the relay into
  it, and write all of it back, so your permission allowlist, `env`, MCP entries and your own hooks
  survived only by round-tripping through that one call. JSON has no partial read — a prefix of an
  object is a parse error, not a smaller object — so this was never silent, just unrecoverable:
  `init` refused on the next run with `is not valid JSON; fix it and re-run init`, pointing you at
  a file it had shredded itself, and refusing _before_ the merge meant re-running could not rebuild
  it. In a worktree it was quieter and worse — nothing re-reads that copy, so the session started
  against unparseable settings, the CLI fell back to its defaults, the Stop hook was never
  registered, and the run idled to timeout with nothing naming the cause.

  Three of the seven are **put-backs**: they restore a file _after_ something has already failed,
  which is the worst possible moment for a second loss. One of them, the engine's restore of a park
  record after a failed commit, now journals its own failure as `park-record-rollback-failed`
  rather than dropping it. Nothing else would ever surface that — `validate` reports a board parked
  with no record, but never a record left over for a park that is in no commit.

- **Four writers under `.bmad-loop/` no longer strand an untracked temp when their replace fails
  (#363).** Each built a fixed-name temp and then `os.replace`d it, and `atomic_replace` does no
  cleanup of its own. No ignore rule covers those names — `init` writes `.bmad-loop/runs/`,
  `.bmad-loop/cache/`, `.bmad-loop/policy.toml` and `_bmad/render/` — so a failed replace left an
  untracked file holding `verify.worktree_clean` False until a human deleted it by hand.

  - Three route through the helpers, which name the temp uniquely per write and remove it on any
    raise: the pre-answer store (`.bmad-loop/decisions.json`), `policy.toml`'s `[mux] backend`
    writer, and the TUI settings editor's save. The last two built the _same_
    `.bmad-loop/policy.toml.tmp` path, so they could also collide with each other.
  - `archive_run` keeps writing its own tarball — the path goes to `tarfile.open`, so there is no
    payload for a helper to take — and gains the unlink-on-raise guard instead. Its temp was also
    misnamed: `with_suffix` replaces only the last suffix, so `<id>.tar.gz` yielded
    `<id>.tar.tar.gz.tmp`. It is now `<id>.tar.gz.tmp`.

  Under a monorepo `repo_root:` override this surfaces as a failing `validate` and TUI rather than
  a blocked `run`: `run` and `sweep` probe the repo root, `validate` and the TUI probe the project.

  Five more temp-and-replace writers took the same helper without having been exposed: the sweep's
  two `decisions.json` writes, whose file is the per-run one under the gitignored
  `.bmad-loop/runs/<id>/` and not the project-level store named above; the two park-record writers
  behind `bmad-loop confirm` and `drop`, which already carried a hand-rolled guard; and
  `devcontract`'s spec writer. All five gain the fsync before the replace and a unique temp name in
  place of a fixed `.tmp` sibling that two concurrent writers would collide on.

  **Scope, for both entries above.** This closes the _raise_ path, and only that. The helpers stage
  at `mkstemp(dir=target.parent, suffix=".tmp")`, so a `SIGKILL` mid-write still strands a temp
  that `worktree_clean` reads as dirty; and on Windows `os.replace` is
  `MoveFileEx(MOVEFILE_REPLACE_EXISTING)`, which is not guaranteed atomic and may fall back to a
  non-atomic copy. What holds everywhere is that a failed write cannot truncate the original.

- **An atomic write no longer fails on a file whose name fills the filesystem's limit.** The helpers
  stage a temp named after their target, and `mkstemp` inserts eight random characters, so the temp
  ran `len(name) + 13` — long enough that a target with a perfectly legal name produced an illegal
  _temp_ name and the write died with `ENAMETOOLONG` — or, on Windows, with `ENOENT` carrying
  `winerror` 206, which is the same condition under a different name. On ext4 the cutoff was a
  243-byte basename.
  Latent in the helpers since they were written, and reachable from this release because the story
  spec writers moved onto them: a spec is named by your planning skills, and nothing bounds that
  name. When the readable temp name cannot fit, the helpers now fall back to a short digest of it
  rather than failing — the OS decides, so there is no guess at a per-filesystem byte limit.

- **A best-effort diagnostic write no longer takes the run down, and POSIX tmux captures no longer
  raise on an undecodable byte (#380).** Both halves are one defect: an exception net that names one
  direction of the Unicode hierarchy while the other escapes it. `_append_diag_jsonl` serializes
  with `ensure_ascii=False` and writes through a UTF-8 handle, so a story spec whose filename holds
  a byte the filesystem codec could not decode arrived surrogate-escaped and failed at the encode
  with `UnicodeEncodeError` — a `UnicodeError`, so a `ValueError`, not an `OSError` — straight past
  a guard whose stated contract is that an unwritable run dir must never break the completion loop.
  The guard is now `(OSError, UnicodeError)` and the breadcrumb is dropped instead of crashing the
  run. Separately and visibly: `tmux_base`'s `_ERRORS` was the strict handler on POSIX while the
  Windows backend already set `"backslashreplace"`, so a capture holding such a byte raised out of
  the one place tmux is spawned; it now comes back with that byte rendered as a `\xNN` escape, and a
  session name or window title carrying one reads back escaped. Fixing the decode at its source
  rather than at the fourteen catch sites is deliberate — most of them return a sentinel, so
  catching there would have converted a crash into a wrong answer (`[]` reads as "window dead").
  `_ENCODING` stays `None`, so POSIX keeps the locale codec and only stops being strict. This closes
  the diagnostic writer and the capture decode; it does not sweep the wider `except`-tuple family.

- **A plugin hook or version probe whose child emits a non-UTF-8 byte no longer crashes the run
  (#383).** `subprocess.run(..., text=True)` decodes with the locale codec at `errors="strict"`, and
  the `UnicodeDecodeError` that raises is neither an `OSError` nor a `SubprocessError`, so it
  escaped both captures' guards. The declarative-hook transport is the run-crashing half: `_HookError`
  is the bus's designed channel for "the hook could not run to completion", and the decode happens
  after the child has exited — so a hook that actually **passed** took its exit code down with the
  run instead of being classified. `probe.run_version_help` documents "Never raises", and a
  `--version`/`--help` banner carrying such a byte made that false. Both now decode with
  `errors="replace"`, so the hook's verdict survives and a fault is classified through the normal
  channel. Visible change: those bytes now show as `�` (U+FFFD) in journal entries, hook advisory
  text and probe documents. The `except` tuples are deliberately not widened — the fix is to stop
  raising, and a widened tuple would guard a fault nothing could ablate into existence.

- **A session whose log merely writes _about_ a provider error no longer pauses the run (#507).**
  `claude` shipped one pattern joining a framing token to a cause across an unbounded `.*`, and this
  adapter scans a tmux pane capture — the model's own output — so any line mentioning both halves
  classified. 44 of this repo's own tracked lines did, most of them ordinary pytest/grep/diff output.
  The harm ran the other way: a **genuine** timeout was read as an environment fault, re-arming the
  budget and halting the run for an operator instead of charging the attempt. The three replacements
  reproduce only complete error sentences Claude Code was captured printing, 5xx statuses enumerated
  rather than ranged. A standing guard walks `git ls-files` and asserts no tracked line classifies —
  write the framing token and a cause separated (`API Error` … `<cause>`) in future entries.

- **A mid-response connection drop or a provider 5xx refusal on the `claude` adapter now pauses the
  run with the matched evidence (#323).** The withdrawn connection-only pattern caught 2 of the 5
  captured Claude Code failure lines, so a session killed by either of those three misses was charged
  a dev attempt, and `max_dev_attempts` of them deferred a story whose spec and code were fine. All
  five classify now, and the pause re-arms the budget instead of spending it. A subscription
  usage-limit / quota refusal is still **not** classified on this adapter: no captured Claude Code
  quota line exists to seed a pattern from, and on a pane capture that vocabulary is what a story
  _implementing_ rate limiting prints all day — follow-up: #610. The four unseeded profiles
  (`codex`, `gemini`, `copilot`, `antigravity`) are unchanged and still ship none.

- **An out-of-tree module that claims a bundled transport's name is no longer driven in the bundled
  backend's place (#565).** Backend selection breaks ties on registration order, and the bundled
  `tmux` / `psmux` entries were seeded only on the first multiplexer resolution — so any
  registration that landed before it owned that name, and the whole process silently ran on a
  third-party transport. The trigger is reachable rather than theoretical: a plugin's `[python]`
  module is executed in-process by the plugin registry, which has no ordering relationship to when
  the mux is first resolved. Registering a backend now seeds the bundled ones first, making
  builtins-first an invariant of the registration itself rather than a property of which import ran
  first — the same fix the adapter registry already carries. A shadowing external is still
  registered, just behind the bundled entry.

- **Two broken distributions that publish the same entry-point name no longer collapse to a single
  recorded error (#566).** `importlib.metadata` does not deduplicate entry points across
  distributions, and all three external-load scans — adapters, profiles and mux backends — recorded
  failures by assignment into a name-keyed map, so the second failing package overwrote the first.
  You fixed the one failure you were shown, then met the other on the next run with nothing saying
  it had ever been there. Both reasons now surface, and every recorded external-load failure names
  its **distribution** when one is resolvable — in `bmad-loop adapters`, `bmad-loop mux`,
  `validate`'s human output and `validate --json` — because the entry-point name is not the
  distribution you uninstall.

  The limit, plainly: two failing same-named distributions still produce **one** finding and one
  warning line, whose text now carries both reasons `"; "`-joined. The row count does not double.
  That is what keeps the change contract-preserving — `detail`'s key set and value types are
  unchanged, so `VALIDATE_SCHEMA_VERSION` stays 1.

  **A deliberate scope addition:** the multiplexer's entry-point scan is now ordered by (name,
  distribution), as the adapter and profile scans already were, so which of two same-named
  distributions is recorded first is a fact about the packages rather than about `sys.path`.

- **A run launch whose adapter class rejects a bootstrap keyword now aborts on a clean `error:`
  line instead of a bare traceback (#569).** The construct call converted only the failures an
  adapter family declares, and a signature mismatch is refused by the interpreter rather than by
  the family — so an out-of-tree class whose `__init__` does not accept a keyword the bootstrap
  passes escaped uncaught. The abort now names the profile, the adapter kind and the rejected
  keyword; the exit code is unchanged at 1. Deliberately unchanged: a `TypeError` raised from
  inside a working `__init__` still surfaces as itself, because that is a bug in that package
  rather than a declared failure, and relabelling it as a signature mismatch would bury it. This is
  message quality only — an error escaping here already unwound the composition it had started.

- **A modal dialog on a terminal narrower than its declared width now shrinks to fit instead of
  being clipped, so its action buttons stay reachable (#281).** The docked button row is
  right-aligned, so the buttons were exactly what fell off the right edge — the horizontal twin of
  the vertical defect #275/#280 fixed. `EscalationModal` needed 87 columns, so a standard
  80-column terminal already clipped it outright; `DecisionModal` needed 83 and the bounded
  confirms 61. Below 60 columns those buttons additionally render smaller and tighter, because
  clamping the dialog alone still leaves a three-button row demanding 54 columns inside a content
  region narrower than that.

  On the other axis, below 20 rows a dialog now renders in a compact layout — collapsed padding,
  no title margin, a one-row button row — rather than clipping its docked buttons and safety
  warnings. `docs/tui-guide.md` accordingly records the terminal sizes these dialogs were measured
  at — **39 columns × 9 rows** for a dialog's own chrome — stated as sizes measured to be
  sufficient rather than as a supported minimum, and scoped to the dialogs, not the dashboard
  behind them. `EscalationModal` sets that figure and it is width-dependent, its docked warning
  wrapping to 9 rows at 39 columns but 6 at 80. Titles, headers and paths dock outside the
  scrolling body, so a long enough one wraps and costs rows the body cannot give back: a
  ~300-character deferred-work heading clips the close button, the validate viewer grows with its
  document's spec folder (#629), and the spec viewer's `copy path` button plus its action verbs
  simply do not fit 39 columns (#628). Nothing bounds that caller-supplied text, so no fixed size
  is a minimum these dialogs will always meet; a standard 80 × 24 terminal absorbed every measured
  example and the guide quotes it on those terms. At 60 columns and 20 rows and above the full
  chrome renders exactly as it does today.

- **A deferred-work bundle whose name or key ends in a newline is now rejected instead of becoming a
  directory (#330).** Both sweep regexes anchored with `$`, which in Python also matches just before
  a single trailing newline, and every call site uses `.match()`. So a bundle named `fix-it\n`
  validated clean and was used unsanitized as both the `run_dir/bundles/<name>/` path segment —
  invalid on native Windows — and the `dw-<name>` story key, while a key of `dw-foo\n` silently
  rebuilt a degraded bundle's intent under the different directory `foo`. Both patterns now anchor
  with `\Z`. Only a name or key ending in exactly one bare LF flips to rejected; `\r\n`, `\n\n`, a
  bare `\r`, a trailing space and any interior newline already were. A cached triage carrying such a
  name now re-runs instead of crashing, and a pre-fix run-state task keyed that way becomes inert
  rather than re-driven under a silently different name. Sweep-scoped: a bundle name is still not
  guaranteed safe as a path segment.

## [0.13.1] — 2026-10-01

### Added

- Tag hook events with relay-side process lineage; once the launched session's first
  `SessionStart` reads `match`, a nested CLI's `mismatch` events (id-less included) are
  dropped. Untrusted lineage writes one `hook-lineage-untrusted` crumb (DW-507).
- Write one `pinned-session-id-mismatch` crumb when a pinned session's first non-rebind
  `SessionStart` reports an id other than the pin, so the drop of its own events as
  foreign is no longer silent; a nested CLI's `mismatch`-tagged start is skipped (DW-509).
- Record opt-in per-worker test metrics with `pytest --test-metrics-dir=PATH`, keeping
  wall-clock apart from summed worker-seconds; bound a run with a tree-stopping deadline
  via `scripts/run_test_benchmark.py`. Upload metrics and JUnit from every CI test job,
  failed or timed out included.
- Shard tests by digest with `pytest --ci-shard=I/N` (whole functions and xdist groups, no
  hand-kept list); prove a sharded run complete and disjoint with
  `tests/perf_report.py verify-shards`.

### Changed

- A tmux coding-CLI pane's start command now shows the
  `/bin/sh -c 'WAVES_LAUNCH_PID=$$; …'` prelude; the command itself runs under
  `default-shell` exactly as before (DW-507).
- Run each Windows CI leg as two shards plus a serial psmux-gate job; fail the
  `test (windows, py3.x)` aggregator on a missing or red shard or gate, a test run in no
  shard or two, a skipped live-gate test, or a shard or gate job whose latest attempt
  failed (so a re-run cannot pass on an earlier attempt's records).
- Cut test-suite runtime without dropping assertions: allocate state roots in constant time,
  give render-only tests a Git-free `project_tree`, observe TUI lifecycle events instead of
  polling, and copy submodule origins from per-worker templates.

### Fixed

- Ignore hook events from nested coding-CLI sessions that inherit the relay environment,
  so a child's `Stop`/`SessionEnd` no longer completes or crashes the launched session:
  an id that announces its own `SessionStart` after the launched session's first is
  foreign, and its events are dropped, crumbed once per id as
  `foreign-hook-event-ignored`, counted as `foreign_hook_events` in `heartbeat.json` and
  `timeout-fired`, and excluded from the sweep diagnostic (`hook_foreign_ids`). Forward
  SessionStart `source` so a `clear`/`compact` start rebinds; re-run `waves init` to
  re-vendor the relay (#767). Contributed by [@Pinstack](https://github.com/Pinstack).
- Pin the launched session's id at launch for hook-event attribution: a new profile key
  `session_id_flag` (claude: `--session-id`) makes the generic adapter pass a minted UUID4
  and treat an identified `SessionStart`/`SessionEnd` from any id the session never had
  as foreign (a `clear`/`compact` rebind still counts as its own), so a nested child's
  `SessionEnd` without a prior `SessionStart` no longer crashes the parent (DW-505/508).
  A same-name `.waves/loop/profiles/claude.toml` overlay replaces the packaged profile and
  stays unpinned until it adds `session_id_flag = "--session-id"`. A claude run paused
  before upgrading reports the host-exec config changed on resume: its launched argv
  gained `--session-id`. Dry-run previews show the flag as `--session-id <auto>`.
- Advance a sprint-status row whose status is folded onto an indented continuation line,
  as a width-80 YAML dump writes a long story key, instead of leaving the old status and
  rolling the finished story back; the row collapses to one `key: status` line. Edit only
  the row the YAML parser reads, never look-alike text in a block scalar or another
  mapping, and leave a multi-line value the writer cannot read whole untouched (#842).
  Contributed by [@mswanson](https://github.com/mswanson).
- Raise `SprintStatusWriteRefused` when an existing sprint-status row below its target is
  in a shape the writer cannot rewrite, instead of returning the unchanged status: a
  finished dev or review-demotion pass escalates with board, row, statuses and reason and
  keeps its work (no rollback, no retry); the board carry journals
  `board-advance-carry-failed` with `refuse_cause`; `waves confirm` exits 1 naming
  the repair and keeps the park entry (follow-up to #842).
- Replace only a sprint-status value's own text when advancing a row, keeping the
  gap, inline comment, trailing whitespace and line ending as authored. A null row with a
  comment (`key:  # note`) keeps its comment, and a bare `key:` row can now be advanced.
  Refuse rows in a flow-style `{...}` mapping (`mapping-is-flow`) instead of publishing
  invalid YAML, and any anchored value (`value-is-anchored`), aliased or not. A quoted value
  with a glued comment (`'backlog'#c`) is now refused (`unreadable-value`) rather than
  rewritten (DW-514, DW-516).
- Advance the sprint-status row the reader reads, matched by its parsed key rather than
  its text (`advance`'s epic lift now lifts a lone `epic-01` row as epic 1). Refuse two
  distinct keys that read as one (`"2001-01-04"` and the date `2001-01-04`; `epic-1` and
  `epic-01`) as `key-ambiguous`, publishing nothing, instead of rewriting a row the reader
  ignores or regressing a `done` epic (DW-515).
- Retry the transient Windows errors `delete`/`archive` (CLI and TUI) hit while removing a
  run dir — a sharing violation from a concurrent reader's handle, and the WinError 145 a
  parent `rmdir` hits while a child is still delete-pending — instead of failing on the
  first one (DW-519, DW-520).
- Return `waves validate`'s coding-CLI probe at its timeout on a Windows `.cmd` launcher
  and kill the launcher's descendants, instead of waiting for the launched program to exit
  (120 s observed in CI).
- Keep a Windows release cut byte-stable: the release scripts read and write CHANGELOG and
  version files as UTF-8 with LF line endings, and exchange `git`/`gh` text — release
  notes included — as UTF-8 rather than the ANSI code page. A portability guard now
  refuses file `open` / `read_text` / `write_text` without an explicit encoding in
  `src/riaworks_waves_loop` (DW-513, DW-517, DW-518).

## [0.13.0] — 2026-09-28

### Added

- Implement `[gates] retrospective = "auto"`: at each epic boundary, and at run end for
  the last epic once every story is `done`, run one headless
  `/bmad-retrospective -H <epic>` session on the new `retro` adapter role
  (`[adapter.retro]`, inheriting from `[adapter]`), before the auto-sweep. Success needs a
  completed session, `result.json` `done`, the board at `epic-N-retrospective: done` and
  an `epic-N-retro-*.md` doc; only the doc and board are committed, and leftover dirt
  pauses. The verdict rides `retro-auto-finished` and the done notice (a `rejected` epic
  adds an `ATTENTION` line). `validate` and `status --json` name the retro role, and
  `config_digest` covers it (DW-389, DW-487, DW-488).
- Ingest sprint-status retro `action_items` into the deferred-work ledger: a fresh
  `waves sweep` files each not-`done` item as a `DW-<n>` entry
  (`origin: retro action item <id>`) before triage, never re-filing a twin (DW-388).
- Document the `_bmad/custom/bmad-retrospective.toml` override that points the retro at
  run-dir journals and session logs (setup guide) (DW-387).
- Add `waves resolve <run> --adopt-branch`: finish an escalated worktree story from
  its kept branch (spec set `done`, board mirrored, branch squashed and merged) with no
  new session. Review, `[verify]` and `pre_commit_gate` are not re-run. A resume that
  drains the queue past an ESCALATED story now pauses instead of recording the run
  `finished` (DW-386).
- Add `waves resume <run> --accept-baseline`: restarted in-place stories adopt the
  current HEAD as their baseline, so commits above the old one are kept rather than
  parked and reset (`baseline-accepted`). Restart resets that do park work now notify
  (`ATTENTION`) naming the `attempt-preserve/*` / `attempt-preserve-dirty/*` refs with
  recovery hints, and a failed preserve leg journals `attempt-preserve-fallthrough`
  (DW-371, DW-480, DW-481, DW-482).
- Add `[operator] on_review_demotion = "escalate" | "park"` (default `escalate`): under
  `park`, a review that finalizes a `done` story at `awaiting-operator` moves the board
  back, commits and parks (DW-383).
- Seed antigravity workspace trust per unit worktree via a profile's `[workspace_trust]`
  table, so `isolation = "worktree"` works with antigravity (journals
  `worktree-trust-seeded` / `-unseeded`); add `probe-adapter --workspace PATH` for a
  read-only trust verdict (DW-390).
- Add parked-session detection: a canonical `Notification` event with
  `PermissionPrompt`/`IdlePrompt`/`QuotaPrompt` kinds, a
  `[hooks.notification_types]` profile table, and `parked_prompt_patterns` matched
  against the pane at every stall-grace expiry. A parked session ends `stalled` +
  `parked` and pauses instead of being nudged. The claude profile maps its permission,
  idle, quota and MCP elicitation dialogs; re-run `waves init` to register the
  relay (DW-348, DW-350, DW-433, DW-434).
- Add a `post_review_verify` plugin hook stage publishing every review verify gate's
  `[verify] commands` results (DW-357).
- Expose `ctx.delivery_id` on `post_migrate` and `ctx.rollback_outcome` on
  `post_rollback` (declarative: `WAVES_DELIVERY_ID`, `WAVES_ROLLBACK_OUTCOME`);
  `post_rollback` now fires once for every `pre_rollback`, also on a paused or failed
  rollback (DW-317, DW-322).
- Add a free-form `effort` key to `[adapter]` and `[adapter.<stage>]`; `opencode-http`
  sends it as the per-prompt `variant` (shown on the `run --dry-run` launch line), and
  `validate` warns (`policy.effort-unsupported`) for tmux stages (#643).
- Journal a session's idle stretches as `session-idle` / `session-active` (threshold
  `limits.dev_stall_grace_s`), with `transcript_idle_s` on `heartbeat.json` and the TUI
  agent line (#680).
- Add opt-in `waves validate --render-probe`: runs each renderer stub's render
  command in a throwaway copy and fails on a render `HALT:` (DW-381).
- Add `validate` warnings: `policy.bypass-dropped` when `adapter.extra_args` drops the
  profile's `bypass_args` (also warned and journaled at real launches);
  `policy.isolation-shared-artifact-dir` for artifact dirs shared with the main checkout
  under worktree isolation; `deferred.ledger-untracked` and
  `deferred.ledger-ignored-isolated` for a ledger that waves's commits would sweep in
  or lose; `hooks.relay-path-unsafe` for a relay path with shell metacharacters on
  Windows; `policy.extra-args-unservable` for `opencode-http` `extra_args` repeating an
  adapter-owned serve flag (DW-349, DW-410, DW-485, DW-361, DW-375, DW-346, DW-483).
- Show auto-sweep outcomes (refused with reason, or ran) in the TUI run header (DW-366).

### Changed

- **Hooks now register through the installed `waves relay <Event>` command.
  Re-run `waves init` after upgrading.** Codex treats the new commands as untrusted
  and silently skips them until you accept them at the next launch. `validate` warns
  when a hook still points to another installation, and (`hooks.relay-stale`) while a
  Windows backslash registration remains (#773; Windows paths are now forward-slash);
  `init` replaces a relay installed for the other OS.
- Support `isolation = "worktree"` when the project sits inside a `repo_root:` override
  (a monorepo's `<repo>/app`): unit worktrees provision at the project's offset. The
  `policy.isolation-repo-root` refusal now fires only when the project is outside
  `repo_root`, and `validate`/the TUI launch guard now require a clean `repo_root`, as
  `run` and `sweep` do (DW-379).
- For the claude profile, an idle dev/review/workflow session now pauses as parked at
  stall-grace expiry instead of receiving the stall wake nudge; opt out by dropping
  `idle_prompt` from `[hooks.notification_types]` in a project overlay (DW-348).
- Commit hooks in the ledger-publication candidate worktree now see only the target
  file: a hook that reads other tracked files may fail the publication (DW-401).
- Name an earlier attempt's parked work in the retry dev prompt once Git confirms the
  ref still resolves on this task's baseline (#777).
- Name every mux session's window 0 `shell` on tmux and psmux (DW-351).
- Document the live-session removal guard's ceiling: `delete`, `archive` and `clean` can
  still remove a run whose live session a listing omits (#732).

### Fixed

- Pause a dev session with no confirmed work (a permission dialog, a login, a
  dead-on-arrival window) instead of retrying into the same wall; `dev-decision` and
  `session-end` carry `produced_work` (#727).
- Stop charging an attempt for a session that times out having consumed zero tokens (a
  provider quota stall): it is now an environment fault that pauses, and usage with no
  signal is journaled as untracked (`null`), not 0 (DW-364).
- Count Copilot shutdown metrics, increased Codex output-token totals and new or changed
  Gemini model messages as work when a dev session exits before the next transcript
  heartbeat (#822).
- Honor a hard `waves stop` inside verify commands and declarative plugin hooks, and
  kill the whole process tree (including descendants that outlive their shell) on stop or
  timeout; on Windows the post-kill drain no longer blocks on a held pipe (DW-353,
  DW-477, DW-478).
- Escalate an isolated unit before a Codex session starts in a worktree Codex does not
  trust, instead of starting a session whose Stop hook is silently skipped; trust the
  worktree, then `resolve --no-interactive` and `resume` (DW-340, DW-341).
- Report stale or unverifiable Codex hook trust in `validate` and `probe-adapter` before
  a live probe launches (#461).
- Tighten hook-registration checks: `validate`/`probe-adapter` report hooks registered
  only when every Stop-mapped event runs an executed relay naming `Stop`, and refuse a
  managed relay reporting `Stop` (or a wrongly mapped event) under another native event
  or any antigravity hook group; `init` strips or warns about them (DW-342, DW-343,
  DW-344, DW-345, DW-391, DW-392, DW-409, DW-490).
- Preflight the complete bundled `waves-core-sweep` skill before `sweep`, a sweep resume
  or an auto-sweep, naming `waves init --force-skills`, instead of every triage
  session stalling at `Unknown command`; `validate` reports `skills.sweep*` (DW-367).
- Re-merge on resume a worktree story saved DONE before its merge started, instead of
  letting GC discard the unit branch (DW-385).
- Stop worktree teardown and the run-end GC from silently discarding a story's edit to a
  `skip-worktree`-pinned hook config: success paths pause with the worktree kept
  (`pinned-config-edit-refused`), and DEFERRED or merge-escalated units carry the edit in
  `changes.patch`. A GC pause now leaves the run resumable (DW-368, DW-479, DW-501,
  DW-502).
- Protect the tracked ledger and board at the merge pre-flight only when the task writes
  them, and park an operator's uncommitted edit to a path the branch changes under
  `refs/merge-preflight-preserve/<sha>` before restoring it (DW-354, DW-356).
- Prove ledger ownership on every harvested-deferral carry retry, pausing
  (`harvest-carry-foreign-dirt`) rather than committing an operator's ledger edit
  (DW-355, DW-413).
- Seed a leaf-symlinked ledger or board at its configured path, ending the #426 defer
  loop, and name a link to outside the project in `worktree-seed-dropped` (DW-377,
  DW-432).
- Keep deferred-work ledger ids and dedupe keys stable: mint ids from `### DW-<n>`
  headings only, refuse a migration that edits an entry's `origin:`/`source_spec:`,
  ignore fenced examples when checking for a field, and restore severity when reopening
  an old archive stub (DW-334, DW-363, DW-384, DW-394, DW-408).
- Harden sweep-migration recovery: resume a migration interrupted mid-retry, mid-triage
  or after escalating from `committing` by restoring its durable snapshot (or replaying
  its idempotent commit tail) instead of escalating or triaging over unaccepted text;
  replay `sweep-migrated` / `post_migrate` after a host death past `DONE`; re-raise a
  ledger publish whose `git status` fails (DW-313, DW-314, DW-315, DW-317, DW-336,
  DW-405, DW-407, DW-426, DW-436, DW-439).
- Never rewind a sweep migration over a HEAD that moved past the task baseline or over
  unrelated dirt: recovery resets pause instead, dirt is parked under
  `refs/attempt-preserve-dirty/*`, and an escalated restart that finds a newer ledger
  re-pauses (`sweep-migration-restore-diverged`) (DW-427, DW-428, DW-429, DW-430,
  DW-435).
- Pause a sweep migration before dispatch when its tracked ledger differs from the
  committed one (`migrate-ledger-dirty`: commit it, then resume), and finish one with
  nothing to convert as DONE with no session (DW-437, DW-440).
- Make the exact-path ledger publication robust: hold `index.lock` across the target
  compare and reset, read past `git replace` refs, refuse a live exec-bit mismatch
  (chmod the ledger to match), bind attempt-owned spec normalization to one inode, and
  prune or name leftover candidate worktrees on failure (DW-319, DW-323, DW-324,
  DW-325, DW-326, DW-327, DW-328, DW-329, DW-330, DW-331, DW-398, DW-399, DW-400,
  DW-402, DW-403, DW-404).
- Skip the candidate cleanup's `git worktree remove --force` / `prune` when
  `<git-common-dir>/worktrees/` holds a symlinked or junction entry, which git would
  empty the target of; remove the link, then prune (DW-494).
- Report undelivered nudges as failed (`nudge-send-failed`) instead of sent, in the
  generic and `opencode-http` adapters; heartbeat `stall_nudges_sent` counts delivered
  nudges only (DW-449, DW-503).
- Stop recording a failed session probe as a vanished session: only a window listing
  that proves the session gone writes `session-vanished`; otherwise
  `session-probe-failed` (DW-459).
- Distinguish confirmed missing tmux-family sessions from failed window listings (#525).
- Journal observation faults instead of folding them into a healthy-looking empty
  answer. Generic adapter: `liveness-probe-failed`, `parked-probe-failed`,
  `log-evidence-failed`, `result-json-refused`, `usage-sample-failed`,
  `transcript-scan-failed`, `spec-readback-failed`, `env-fault-scan-failed`,
  `spec-reconcile-skipped-status`, and a `liveness_unknown` flag on over-budget and kill
  verdicts. `opencode-http`: `usage-sample-failed`, `usage-capture-failed`,
  `sse-stream-failed`, `sse-frame-dropped`. Verdicts are unchanged (DW-382, DW-447,
  DW-448, DW-450, DW-451, DW-452, DW-453, DW-454, DW-455, DW-456, DW-457, DW-460,
  DW-461, DW-462).
- Warn instead of reading as "nothing there" when a mux session listing, pane or option
  read, or backend probe fails (`mux` and `validate` report `mux.backend-probe`), and
  when the removal guard cannot list sessions (DW-458, DW-463, DW-464, DW-466).
- Report an unreadable runs dir, run dir, legacy registry or orphan sweep instead of "no
  runs" / "nothing orphaned": `list`, `status`, `clean`, `cleanup` and the TUI say so,
  with additive `--json` keys `listing_fault`, `sessions.legacy_unverified`,
  `worktree_faults` and `state_dir_fault`. An unreadable `engine.pid` reads as liveness
  `unknown`, and `resume` warns about an unreadable config baseline (DW-465, DW-467,
  DW-468, DW-469, DW-470, DW-471).
- Surface TUI read faults: a stale run header (`⚠ state stale`),
  `decisions unreadable`, `agent unreadable`, and notes for unreadable `ATTENTION` or
  journal files (DW-472, DW-473, DW-474, DW-475).
- Shape every notice through `gates.notify`/`gates.notice_line`: control characters
  become visible escapes, multi-line faults and pause reasons fold onto one line, a
  4000-character cap applies, and lone surrogates never raise. `state.json`, `--json`
  and the journal keep the raw text (DW-13, DW-332, DW-417, DW-419, DW-491, DW-492).
- Resolve artifact paths from BMAD's central `_bmad/config.toml`, falling back to
  `_bmad/bmm/config.yaml` only for missing keys, and refuse malformed values; sweep
  triage reads the orchestrator's resolved ledger (#154, #769).
- Read untracked paths verbatim so rollback snapshots, cleanup and failed-unit diffs
  handle non-ASCII and space-edged filenames (#783).
- Run a declarative `post_story` hook from the repo root after worktree teardown, and
  count `plugin-hook-error` in `diagnose` (#779).
- Refuse `init` when `.waves/loop`, its `policy.toml` or `.gitignore` resolves outside
  the project (#771).
- Parse plugin manifests in `validate` (`plugins.manifests`) without importing plugin
  code (#765).
- Scope the sweep skill's `open_ids` to the session's triage universe, so `--only` /
  `--min-severity` no longer burns a retry (#824).
- Show a sweep run's effective `max_bundles`, `repeat`, `max_cycles` and selector in
  text `status` (#815).
- Diagnose non-completed sweep triage and migration sessions: which of `result.json`
  and the hook events arrived (#752).
- Prove ownership of an untagged control window before the TUI attaches to or kills it,
  so two projects using the same `--run-id` no longer target each other's
  orchestrator (#531).
- Preserve inherited `model`, `effort` and `extra_args` when a stage names an alias of
  the base client; key the `run --dry-run` preview on adapter kind.
- Honour `launch_args` before `serve` for `opencode-http` wrapper profiles
  (`npx -y opencode-ai`), with `adapter.launch-args-unservable` in `validate`; report a
  deeply nested pattern entry as a `ProfileError` (DW-373, DW-374).
- Fit TUI dialogs to narrow and short terminals (down to 39×9): long titles and paths
  truncate with `…`, and button rows wrap or scroll instead of going off-screen (DW-358,
  DW-359, DW-414, DW-415).
- Decode unity plugin child output as UTF-8 with replacement, so a cp932 Windows
  codepage no longer raises `UnicodeDecodeError` (DW-365).
- On Windows, stop a DW bundle pausing at baseline capture when the artifacts root
  reports no inode (`artifact-observation-unpinned`) (DW-444).
- Alias commit and snapshot refs in `diagnose` dumps (DW-318, DW-337, DW-435).
- Correct docs: why `resume` tolerates a dirty tree while `run`/`sweep` refuse one, and
  `gates.on_escalation` is reserved (only `pause`, no effect) (DW-360, DW-376).

### Security

- Pin the run dir, each worktree mount, and every writer below them to the identity
  recorded when the orchestrator minted them (`run_dir_identity`,
  `worktree_identity` in `state.json`): verify-stream and integration-snapshot writes,
  spec repair/reset/reconcile/adoption, park records and their rollback, re-arm/replan
  writes and ledger restores now refuse a root, mount or `.waves/loop/` subdirectory
  swapped for a link instead of writing outside the repository. Older state records its
  roots at the first `resume` (`root-identity-recorded`). Parent directories above the
  worktree, and operator-chosen roots, may still be links (DW-338, DW-423, DW-445,
  DW-446, DW-486, DW-497, DW-498, DW-500).
- Harden the exact-path candidate worktree: check it out without running smudge filters
  or fsmonitor, and pin its root, `.git` gitfile, admin dir and `commondir` so a swap
  before a later git call is refused instead of steering it into another repository;
  on Windows, refuse junctions when creating its parents (DW-401, DW-420, DW-425,
  DW-442, DW-493, DW-495).
- Create missing artifact directories through no-follow opens pinned to the accepted
  root, and on Windows refuse a junction at or below the artifacts directory (DW-421,
  DW-422).
- Pass `--` before notify-send positionals and shape the Unity dialog probe's line, so
  an untrusted window title cannot forge `ATTENTION` lines (DW-418).

## [0.12.0] — 2026-09-20

### Added

- Restore and normalize attempt-owned specs on Windows through NT handle-relative
  opens instead of pausing for manual adoption. `win32_at` binds `NtCreateFile` with a
  `RootDirectory` handle plus `FileRenameInformationEx`/`FileDispositionInformationEx`
  (POSIX semantics, classic classes as the fallback) and refuses a symlink or junction
  as `O_NOFOLLOW` refuses a link; `platform_util.HANDLE_ANCHORED_WRITES` joins that arm
  to the POSIX `dir_fd` one behind `open_at`/`stat_at`/`replace_at`/`unlink_at`, so the
  confined spec writers and `open_dir_confined` anchor at a handle on both hosts. The
  DW-309/DW-310 refusal now fires only on a host with neither arm; its journaled
  `problem` reads `lacks handle-anchored writes`.

- Accept a session-asserted artifact-only sweep bundle at the dev proof-of-work gate
  (DW-273). A bundle whose only deliverable lives under a gitignored
  `implementation_artifacts` (a spec-only erratum) burned every attempt on
  `no changes in worktree since baseline commit`. The bundle dev session may assert
  `Artifact only: true` in its `## Auto Run Result` marker (`Artifact only`,
  `artifact_only` or `Artifact-only` — at least one separator between the words, so
  the fused `Artifactonly` asserts nothing), and `verify_dev_bundle` —
  the bundle path alone — then accepts ignored entries under the artifacts dir once
  the ordinary probe found nothing, journaling `bundle-artifact-only-accepted`. Only
  artifacts this attempt created or changed count; residue that predates the attempt
  or cannot be measured refuses the receipt, and a fault taking the attempt's
  snapshot degrades to `bundle-artifact-baseline-unavailable` with the attempt still
  driven. Under `scm.isolation = "worktree"` the accepted ignored spec and its
  declared `artifact_deliverables` are published to the main checkout before the
  success teardown (DW-283); undeclared ignored residue is not copied. The review
  gate's every-id-`done` check is unchanged.

- Announce a ledger publish that publishes nothing (`sweep-ledger-commit-clean`), for every
  outcome that publishes nothing. An ignored path reads clean, so a project
  that gitignores its `implementation_artifacts` skipped every ledger commit with no
  journal row at all (DW-191).

- Name the published file on every `_commit_ledger` journal row with a `file` field —
  the lexical basename, never the resolved symlink target's name — so a scrubbed
  `waves diagnose` dump still says which of the two published files went
  uncommitted, where `repo`, `message` and `error` all collapse to presence booleans
  (DW-192).

- Write each repeat-loop stop's token as a closed-slug `stop_cause` beside
  `sweep-repeat-done`'s existing `reason`, so a diagnostics dump tells the five stops
  apart instead of rendering one `reason_present` boolean (DW-201).

- Declare a journal schema for the five sweep kinds `waves diagnose` prints as a JSON
  block in the default Markdown dump (`sweep-ledger-commit`, `-clean`, `-refused`,
  `-unavailable`, `sweep-repeat-done`), so a field a future producer adds without
  routing collapses to `<name>_present` instead of riding the generic scrub into the
  pasted block.

- Give each declared journal `**splat` hole a COUNT of the unresolved `**` keyword
  arguments it holds — not write calls, so `append(kind, **a, **b)` counts 2 — and a
  second unresolvable splat inside an already-declared position now reddens instead of
  being waived on arrival, whether it arrives as a new call or as a second `**` on an
  existing one; the field inventory moves to a sibling `JOURNAL_SPLAT_FIELDS` table
  (DW-150).

- Enforce the bare-function-name key the five journal position tables rest on: the
  scan emits each journal write's enclosing def identity and a guard reddens if one
  module ever holds two same-named journal-writing functions. The property is exactly a
  pair of WRITERS, which is what the four position tables need — not full name safety
  for the fifth, `JOURNAL_FORWARDERS`, whose row makes any call to that name in that
  file read as a journal write, so a same-named twin that never journals still routes
  its callers' keywords into the field inventory and, emitting nothing, stays invisible
  to the guard. Qualifying those keys to `class.method` stays deliberately deferred;
  the guard is what makes the writer-pair half of that deferral safe (DW-152).

- Grade the real harvest exclusion producer through the stories plan-halt observation (DW-153).

- Name the three harvest exclusion grading rows in the producer docstring (DW-154).

- Grade the real harvest exclusion producer through the sweep bundle proof-of-work gate (DW-168).

- Correct the harvest exclusion docstring to name both `repo_root` override shapes (DW-169).

- Prove real-tmux teardown reaps the exact detached child after identity publication fails (DW-149).

- Pin dynamically generated journal kind spellings in `recovery_flow` and detect
  renames independently of write counts (DW-151).

- **The accepted-park arm's `_harvest_gate_exclude` join is now graded engine-side**
  (DW-139). `tests/test_verify.py::test_verify_dev_park_zero_diff_excludes_the_orchestrators_own_writes`
  hand-spells its `engine_written`, so the producer is never invoked and re-rooting it
  left that row green. `tests/test_engine.py` gains
  `test_accepted_park_observation_excludes_the_nested_ledger_under_the_monorepo_shape`,
  driving an asserted park through `Engine._verify_dev_artifacts` under the nested
  monorepo shape — where the orchestrator's own append to the NESTED ledger is the only
  unexcluded residue and a `project`-rooted spelling silently names the outer project's
  real ledger. Its control trips the producer's stand-down disjunct through the same
  join, so `park_zero_diff is True` is attributable to the pathspec.

- **The `_usage` stash is now pinned to survive teardown** (DW-129) — the invariant
  DW-117's cap placement rests on, since `read_usage(result)` runs after `run()`/`kill()`
  return. `tests/test_opencode_http.py` gains a row that stashes a session's usage,
  drives a real `kill()` -> `_teardown()` (nothing stubbed) over a live child process and
  a real log handle, and asserts `read_usage` still resolves that session id. Until now
  the invariant was only observed incidentally, by three fake-binary E2E rows that happen
  to read usage after teardown; this one pins it directly at the kill seam.

- **Verify-command seam coverage for the legs the earlier passes left unpinned**
  (DW-55). `tests/test_verify.py` gains a row driving all three exits of
  `run_verify_commands`' loop body — completed, timed out, never spawned — in a single
  call with a further command after each fault, so the timeout arm's `continue` is
  load-bearing and the two "no exit status" sentinels (`-1` vs `SPAWN_FAULT_RC`) are
  shown to stay distinguishable when the legs occur together. `tests/test_cli.py` gains
  three rows calling `cli._reverify` directly with a two-command policy: the first pins
  that `env_fault_reason` is read ahead of the return code and that a later offender is
  never what the operator is shown, the second pins the same for an ordinary failure,
  and an all-green control keeps their absence assertions honest.

- **A fresh mount that supersedes an accepted-but-uncommitted spec now journals
  `accepted-spec-write-unreachable`** (DW-101). The `pause_after_spec` gate hands the
  operator a spec that is uncommitted by construction; a re-drive's worktree is a
  checkout of a commit, so for a tracked artifacts dir it delivers the pre-approval
  bytes and the existing delivery probe passes on existence alone. The mount's copy is
  now byte-compared against the main checkout's, and a difference — or a read that
  fails, recorded as `compared: false` — is journalled with the main-checkout spec path
  and the target branch to commit it on. Advisory only: the record refuses nothing,
  pauses nothing and overwrites nothing.

- **A mount that cannot be shown to carry the accepted spec at all now journals
  `accepted-spec-delivery-unreachable`** (DW-104, DW-115). Fires only for a spec the
  task already spells project-relative — the spelling a resume persists, and the one
  leg with no escalating guard above it — when the mounted parent escapes the
  worktree, or the spec could not be resolved at all (a swallowed filesystem fault,
  or a spelling that no longer resolves). Carries the main-checkout spec path, the
  target branch, and `located`, a bare boolean saying which of the two silences it
  ended: `true` the spec was resolved and the mount could not be shown to carry it,
  `false` the spec itself could not be resolved. Advisory only: nothing reads it as a
  gate, and the relocated leg still escalates instead of recording.
- **Target deferred-work sweeps.** `waves sweep --only DW-1,DW-3` selects an
  exact open-id set, while `--min-severity low|medium|high|critical` selects the
  named severity and higher. Selection happens before triage, bundle formation,
  and `--max-bundles`; dry-run and resume preserve the same contract, excluded
  and missing-severity ids are journaled, and selectors are incompatible with
  each other and with archive mode. Named dry-runs over mixed legacy ledgers
  project and label provisional post-migration ids, while real runs revalidate
  after semantic duplicate merging assigns the actual universe.

- **Journal-kind and refusal-site coverage gates.** `tests/test_portability_guard.py` gains
  three enumerate-vs-declare inventories: the literal journal kinds (`JOURNAL_KINDS`,
  fed by a literal-kind emit that also sees kind-only writes, constructor-inline
  `Journal(run_dir).append(...)` writes — a receiver spelling the journal scan was blind
  to — and every literal reaching a declared dynamic-kind position, by keyword, by
  POSITION, through a `**` splat, or as the parameter default; a `kind` argument such a
  position cannot read — a variable, a `*args` splat over the slot, or a `**` splat the
  scan cannot read into — fails loud rather than passing as "no literal here", which is
  the one way an undeclared kind could still reach the journal with the inventory
  green), the `_refuse_*`/`_reject_*` helper definitions counted with
  multiplicity (`REFUSAL_HELPER_DEFS`), and the eleven #414-family isolation-refusal call
  sites counted with multiplicity (`ISOLATION_CONFLICT_CALLERS`). A new kind, refusal
  helper, or refusal call site reddens CI until its row lands; the row is the PR-time
  decision, and the failure message demands the covering test land beside it. Each new
  detector arm carries must-flag and must-stay-silent probe rows.

- **Interactive resolve context names both the BMAD project root and the run's code
  root.** `waves resolve` warns before a divergent-root session launches, keeps the
  session project-rooted, and directs code fixes and commits to the code root. The
  re-arm, from both `resolve` and the TUI, writes the tree the context published, so a
  moved project no longer has the agent edit one copy of the spec while the re-arm flips
  another. A recorded spelling that traverses out through `..` stays external and
  unchanged.

- **A failed re-arm commits probe now journals `rearm-commits-probe-failed`** (DW-81).
  The warn-only probe that lists the commits an abandoned attempt left below the re-drive's
  new baseline used to swallow its `GitError` and write nothing — byte-identical to finding
  no commits at all. It now records the baseline and the typed error, and both operator
  surfaces render it through `runs.rearm_event_notice`. Advisory: it does not hold the
  resume.

- **Review-gate verify commands are journalled** (#656, partial). The three review gates
  (`verify_review`, `verify_review_stories`, `verify_review_bundle`) now emit one
  `verify-command-result` per command, `verification_stage: "review"`, sharing the story's
  `verification_sequence` with its dev and fix passes and writing the same `verify/` stream
  files. `post_dev_verify` stays dev/fix only — #656 narrows to the hook stage. A gate that
  refuses before reaching its commands records nothing.

- **Portability guard: `verify_commands_outcome` is callable only from
  `verify._verify_review_commands`.** A fourth review gate composing run+classify itself would
  reintroduce #695's project-vs-repo root split; the guard now fails and names the file and
  line. Deliberately not widened to `run_verify_commands`, which has three legitimate callers
  on two roots.

- **Source-scan parity guards for three invariants previously held only by docstring prose**
  (DW-65, DW-66, DW-82). The task-directory artifact names move to one shared
  `journal.TASK_CYCLE_ARTIFACTS` that both adapters and `resolve._gather_escalations` iterate,
  and `tests/test_portability_guard.py` gains three detectors: a bare artifact literal outside
  that constant, a session task id composed outside `engine._session_task_id`, and a journal
  field name that neither `diagnostics`' redaction tables route nor the benign inventory
  declares. Each carries positive and negative probes so a detector that stops detecting cannot
  read as green, and an unresolvable `journal.append(**splat)`, a journal write whose kind is
  not a string literal, and a benign entry whose producer has been deleted all fail loud rather
  than being skipped. Journal field routing is graded per kind where `diagnostics` routes per
  kind, and a declared forwarder's call sites (`plugins/bus.py::_log`) enter the inventory.

- **`repo_root` in run `state.json`** (#716). A run records the git root its code work happens in,
  so an out-of-process reader — `waves resolve`'s re-arm — uses the tree the run measured
  instead of re-deriving one. `resume` re-stamps that mirror against the `repo_root` it re-reads
  from `_bmad/bmm/config.yaml`, so an edit made while the run was paused cannot leave the engine
  working in one tree while the out-of-process re-arm advances the attempt baseline in the other,
  with no error on either side; a move is announced rather than silent, since the baselines,
  preserve refs and branches already recorded name objects in the previous tree. A `state.json`
  written before the field existed degrades to the project directory — the pre-upgrade behavior —
  and migrates without being reported as a move.

- **Atomic writers gain an opt-in `require_writable_target` refusal** (#597). Callers over
  operator-curated files can ask for the `PermissionError` a plain `Path.write_text` used to
  raise on a read-only target. Off by default — what the other callers do today is a
  compatibility contract. The probe opens non-blocking, so a planted reader-less FIFO cannot
  park the orchestrator.

- **`waves sweep --archive`** moves closed (`status: done <ISO date>`) deferred-work entries to
  a sibling `deferred-work-archive.md`, replacing each with a stub that preserves the DW- id for
  grep and `closes_deferred` cross-references plus the load-bearing field lines (`gate:`,
  `origin:`/`source_spec:`, live `severity:`/`priority:`, reopenable-close undo markers). The live ledger then carries open
  entries in full and archived ones as compact stubs, rather than every closed body forever.
  Supports `--before DATE` to archive only entries closed before a cutoff, and `--dry-run` to
  preview. Reopening an archived stub leaves an `archived-body:` line pointing at the archive
  block that holds its body. Refuses while any engine run is live. Pure deterministic Python —
  no LLM involvement.

- **Batched deferred-work ledger primitives** (#286, #469). `append_entries`,
  `mark_open_many`, `record_decision` and `mark_done_many`'s per-id `notes=` each collapse a
  sequence that used to be one write per row — or one write per half of an append-then-close
  pair — into a single read-modify-write. Each is byte-identical to the serial sequence it
  replaces, validating the whole batch before it takes the lock, minting sequential ids and
  deduplicating in-call twins exactly as the loop it stands in for did, so a caller adopting one
  changes how many windows it leaves open and nothing else. `append_entries_published`
  additionally hands back the text it wrote, so a caller that has to record what it published —
  rather than what the file happens to hold afterwards — takes its anchor from inside the hold
  instead of reading the ledger back once the lock is gone. An empty batch takes no lock at
  all, matching the per-id loop it replaces, so a caller that batches nothing cannot begin
  failing on a lock it never needed.

### Changed

- Organize decision-answer and publication documentation into navigable operator sections
  for stale answers, store validation, publication refusals and recovery (DW-240).

- Display scrubbed sweep publication and repeat-stop details in the default Markdown diagnostic report.

- Pin the real-tmux xdist grouping guard at EXACT per-module gated-def counts instead of
  floors: `_EXPECTED_E2E_FLOORS` becomes `_EXPECTED_E2E_DEF_COUNTS` and the assertion is
  equality, so adding a tmux-gated def now fails the guard just as deleting one does
  rather than letting the pin silently start trailing again (DW-173).

- Grade `tests/test_stories_e2e.py`'s own module-level AST for the detach-ceiling splice:
  a third `tests/test_conftest.py` scanner requires the `detach_ack_ceiling_s=` fragment
  to be followed by `int(<conftest REAL_MUX_HANG_CEILING_S>)` under either import form,
  with a named expected-site inventory that fails a scan finding nothing. A hardcoded
  `90` renders byte-identically to the splice and passed the existing rendered-text
  assert unnoticed; `_run_detach_gate`'s deliberately varying in-def budget stays out of
  scope because the scan is module-level only (DW-174).

- **The deferred-work ledger-read contract is settled repo-wide** (DW-146).
  `deferredwork` now owns both arms as named readers — `read_for_write` (repair/write:
  absence is `None`, OS metadata/text-read faults raise `LedgerReadFault`
  with the original `OSError` chained (DW-279), undecodable bytes raise
  `LedgerReadError` with the codec error chained) and `read_for_observation`
  (observation: never raises, degrading to an empty text plus an attributed fault) —
  documented once in the module docstring alongside the advisory pre-lock probes that
  are neither arm. Every deferred-work ledger read in `src/riaworks_waves_loop` now names its
  arm or carries a comment classifying it. Three sites change behavior:
  `decisions.pending_missed_decisions` no longer aborts `waves decisions` and
  `waves status` on a ledger that is not valid UTF-8, `sweep --dry-run` refuses
  such a ledger with an attributed `error:` naming the file instead of an anonymous
  traceback (never a fabricated empty listing), and `verify.verify_review_bundle`
  plus the TUI's deferred pane reach their existing degrade arms for it. Pre-lock
  presence probes, lock acquisition and writes retain raw `OSError`; authoritative
  reads now distinguish OS faults through `LedgerReadFault` (DW-279).
  Observation sites degrade on OS faults as well as on undecodable bytes, so an
  `OSError` that used to escape `decisions.pending_missed_decisions` or abort
  `sweep --dry-run` with a bare traceback now yields an empty result or an
  attributed `error:` instead. The observation arm probes with `stat` + `S_ISREG`
  inside its own guard (DW-254), so a metadata refusal — `EACCES` on every
  supported interpreter, Python 3.14 included — becomes an attributed fault;
  only `ENOENT`/`ENOTDIR` and a present non-regular file still mean absence, and a
  symlink loop at the ledger is an attributed fault rather than a clean empty
  read. A ledger that goes undecodable while a
  decision prompt is open still names the decision that did not land — in
  `waves decisions` and in the TUI's decision modal, which keeps degrading to a
  per-decision toast instead of taking the dashboard down. And a sweep whose ledger
  cannot be read at a graceful stop journals `sweep-remaining-estimate-unreadable`
  next to the `run-stop` row, so a withheld estimate says why it was withheld.

- **`waves diagnose --json` reports `schema_version: 4`.** Journal `path` values
  become `path_present`; stale-restore and merge filename lists become counts.

- **Sanitize remaining diagnostic journal identifiers.** Commit residue and sentinel
  names are aliased explicitly, excluded and merge filenames are counted, overloaded
  paths are presence-only, and derived fields win same-named raw-field collisions.

- **Remove the unused whole-artifact-folder exclusion helper** (DW-15). Proof-of-work
  exclusions remain file-granular and rollback protection keeps its workspace-rooted
  path derivation.

- **Resolve context builds only the mode-specific details its consumer uses.**
  Non-stories runs skip stories-root lookup, and stories sentinels report null frozen-spec
  reachability without probing a spec they do not edit.

- **`waves diagnose --json` reports `schema_version: 3`.** Replacing a journal-entry value
  with a presence key is a payload break under the additive-only rule, and the redaction fixes
  above make two: a consumer reading `entry["question"]` on `decision-pending`, or an
  off-schema key on `preference-escalation`, finds a `<name>_present` boolean instead. Exactly
  what minted v2 for `patch` / `stashed_to`. Structure is otherwise unchanged.

- **A story's `verification_sequence` now numbers its review passes too**, so the ordinals a
  `post_dev_verify` handler receives shift: for an unchanged run whose review gate sits between
  the dev and repair legs, the `fix` pass moves from 2 to 3. The ordinal was always documented
  as a per-story counter across a run's verify passes rather than a per-leg one, and the review
  passes are now among them — but a plugin that hardcoded the numbers, rather than joining on
  the `verification_sequence` its context hands it, will read the wrong records.

- **The `verify-command-result` census inverts its meaning.** It was "the dev-phase passes only,
  never a complete count"; it is now every in-run pass — dev, fix and review — with only
  `waves confirm --reverify` outside it (and a pass with no `[verify] commands` configured,
  which records nothing because nothing ran). A run therefore retains one record set plus a
  `verify/` stream file pair per command per review pass where the review leg previously
  retained none, so `verify/` grows with the review budget on a story that loops.

- **psmux sessions now live in a per-project registry** (#537). waves points
  `PSMUX_DATA_DIR` at `<state root>/<project>/_mux`, so a prune in one project cannot address
  another's servers at all. A bare `psmux ls` no longer shows them — `waves mux` prints the
  root and the export that does. The `waves-ctl` control session becomes one per project —
  named `waves-ctl-<registry digest>` on psmux, whose duplicate-server mutex is keyed on the
  session name across every registry in a login session (a fixed name would fail every project's
  launch but the first);
  unchanged on tmux —
  and `cleanup` also sweeps the old default registry for tagged pre-upgrade sessions, naming
  whatever it still holds afterwards. The root is always derived: an ambient `PSMUX_DATA_DIR` is
  overridden — reported once on stderr, and left alone for your own psmux sessions — because
  honouring it would make the registry a function of the shell a command started in. Coding-CLI
  windows are told the state root through their env; other windows inherit it as before, and
  psmux's `PSMUX_BARE_ENV=1` — which breaks that inheritance — is declared unsupported and warned
  about once per process. Cleanup demands the project tag
  whenever the registry it addresses is not one waves derived, a shared default registry
  included. The multiplexer seam signatures are unchanged; a backend built against them keeps
  working.

- **`waves diagnose` routes the re-arm records by field name** (#640, #716). `spec_file` and
  `overwritten` are aliased, and `repo` is dropped — an absolute host path that correlates nothing.
  All three arrive only on the re-arm kinds, so no run predating them renders differently on their
  account. By-name routing is the default rather than the whole rule: a narrow kind-scoped table is
  consulted FIRST, for the fields whose meaning depends on the kind carrying them, and that table
  DOES change pre-existing dumps — `target` is aliased on `unit-merge-started`, `unit-merged` and
  `resume-unit-merge` (see `### Security`) while the `board-advance-*` family keeps rendering it
  verbatim, and `sentinel` is aliased on `sentinel-cleared`. `SCHEMA_VERSION` is unaffected.

- **`waves diagnose`'s default report shows the split code root and the task generation**
  (#705, #716). Both fields reached `--json` but not the markdown renderer, which samples its fields
  by hand — so the two conditions they exist to name were legible only to whoever thought to ask for
  JSON. They render as a `code root differs from project` yes/no line and a `gen` column beside
  `att`; the code root's path itself still never renders.

- **`resolve` and the TUI's re-arm aim the code root before they re-arm, not after** (#716). Both
  surfaces re-armed and THEN resumed, so resume's `repo_root` re-stamp landed after the re-arm had
  already read the stale mirror out of process: a `repo_root:` edit made while a run was paused
  advanced the attempt baseline in the tree the run had left, while the engine that resumed measured
  in the new one, with no error anywhere. Both now re-stamp through one shared writer, after the
  confirm — so a cancelled resolve still leaves the divergence for `resume` to report — and each
  warns that the run has changed repositories, and journals `rearm-code-root-restamped` so the
  move leaves a durable record: this re-stamp is what makes resume's own `code_root_changed`
  read `false` later in the same gesture, and a stderr line or a TUI toast is not a record. A
  config this process cannot read degrades to the root the run recorded, and says so. The #414 isolation refusal is hoisted alongside it, ahead of
  both writes: under `isolation = "worktree"` beside a `repo_root` override, both surfaces used to
  re-stamp, advance the attempt baseline and report "re-armed" before resume refused the
  configuration — spending an escalation `resolve` could no longer re-run, since the story was no
  longer escalated. `resolve` refuses it a second time BEFORE the interactive session, ahead of
  the adapter build: the pair is knowable from config, so the late refusal alone let an operator
  converse with a full agent and answer the re-arm prompt only to be handed rc 1 for it. The
  post-confirm refusal stays the authority — it re-reads the config after a conversation of
  unbounded length, and is the only one `--no-interactive` reaches.

- **Re-arm refuses a story spec it cannot re-open, instead of re-driving onto a status the session
  cannot route** (#640). A spec carrying no top-level `status:` failed the flip silently: the
  operator was told "re-armed <story>", the run resumed in the same gesture, and the re-driven
  session halted on `unrecognized status in existing story file`, spending the escalation. The skip
  record now aborts the re-arm, leaving the escalation armed for a corrected spec, the run state
  untouched and the spec byte-identical. Narrowed to the spec the re-drive will actually READ — an
  unreachable path only warns, since the re-drive mounts a fresh worktree and reads the committed
  spec regardless.

- **Re-arm writes the spec the run actually used, and reports every write it could not make**
  (#640). `StoryTask` persists `spec_file` relative to the worktree and re-arm resolved it against
  the process cwd, where the main checkout carries the same implementation-artifacts-relative
  path — so the status flip and the baseline re-stamp landed on the WRONG file while the
  worktree's real spec kept the escalated attempt's sha. The recorded path is now re-anchored on
  the worktree before either write.
  Separately, both frontmatter writers answer a spec they cannot move with `False` rather than an
  exception and those returns were discarded; they now journal `rearm-baseline-restamp-skipped` and
  `rearm-spec-flip-skipped`, on genuine failure only — re-arm reads the status back, so an ordinary
  second re-arm is no longer told its spec "could not be re-opened". The skip record no longer nests
  behind a successful git advance.

- **Re-arm warns when its spec writes cannot reach the re-drive** (#640). Under worktree isolation
  the status flip and baseline re-stamp land in a worktree the re-drive discards before reading it,
  and the re-driven session reads the COMMITTED spec — so a correction left only in the working tree
  is silently lost. Re-arm journals `rearm-spec-write-unreachable` and both surfaces tell the
  operator to commit the corrected spec. It is raised only when the committed spec does not already
  carry the status the re-drive needs; gating on isolation alone fired on every isolated re-arm,
  where the advice is a no-op. That proof is read at the run's pinned target branch — the ref the
  replacement worktree is cut from — not at the code root's current `HEAD`, which parts company with
  it the moment an operator checks out another branch while the run is paused; the record carries
  the branch so the remedy names the tree the re-drive will actually read. This record alone also
  HOLDS the resume both surfaces fold in behind
  the re-arm, since its advice is unactionable once the run has resumed, and `--resume` does not
  override the hold — the re-arm stands, and `waves resume <run-id>` picks the story up once the
  fix is committed. A spec in an artifact directory configured outside the project is exempt
  entirely: `ProjectPaths.rebased` leaves such a directory where it is, shared across checkouts
  rather than rebased onto each worktree, so the flip lands on the one file every re-drive reads and
  there is nothing to commit — a remedy naming a file outside the repository. Containment is decided
  on the canonical paths, so a spec spelled out of but resolving back into the worktree still warns,
  as does one the host cannot canonicalize.

- **The re-arm baseline records reach the TUI operator too** (#640). Each surface carried its own
  copy of the journal-kind → message routing and they had drifted: the TUI printed only
  `re-armed <key>` and handled three kinds to `resolve`'s six, silently dropping the whole
  `stale-restore-*` family — including the commits warning that is the only notice telling a human
  to inspect the tree. Both now route through one table (`runs.rearm_event_notice`), raise the same
  warnings before resuming, and agree on the ABORT path. Both read the journal through one shared
  guard, so a corrupt journal costs the echo and never the gesture. The TUI omits the trailing
  "before resuming" imperative, since it resumes in the same gesture.

- **`waves resolve` re-stamps the spec's `baseline_revision` on both re-drive legs** (#640),
  not only on a patch-restore. A from-scratch re-drive carried the escalated attempt's sha until
  step-03 re-stamped it, so every gate reading a claimed baseline before then read a stale one. The
  trade is recorded rather than hidden: a claim that genuinely diverged is journalled
  (`rearm-baseline-restamped`) instead of being silently normalized, and a re-stamp is refused
  outright when the baseline advance failed, so spec and task can never agree on a stale sha. The
  record compares against the baseline the run RECORDED, so it fires only on a claim the run never
  made. That refusal now also puts the spec back, as does the abort a failing `## Auto Run Result`
  strip raises: those are the two that fire after the status flip has landed — the rest are
  sequenced ahead of every write — so a spec carrying a movable `status:` beside an unmovable
  `baseline_revision:`, or one whose strip could not be written, used to come back flipped while
  the run still called the story escalated. A restore that itself fails raises rather than
  degrading.

- **A published run archive now lands at mode `0600`** instead of a umask-derived mode (#591).
  It is staged through a file the orchestrator creates itself rather than one `tarfile` opens
  by name, so it inherits the private mode the rest of the `.waves/loop` write path uses.
- **A read-only operator file is refused again instead of being rewritten** (#597).
  `os.replace` needs write permission on the parent _directory_, never on the entry it
  replaces, so marking `sprint-status.yaml`, `policy.toml`, a hook `settings.json`, a story
  spec, a park record or the decisions store read-only stopped meaning anything once those
  writes became atomic. Their writers now refuse with the `PermissionError` a plain
  `write_text` used to raise. Machine-minted state (run archives, stop requests, the
  config-digest stamp) is unaffected.
- **Document the qualified-id obligation once for adapter authors (#311).** The authoring guide
  states the rule a native-id backend must follow rather than leaving it to be inferred from
  psmux's per-seam specifics, and `TerminalMultiplexer.new_parked_window` now says its id is
  opaque and MAY be qualified, matching `new_window`. Documentation only; no behavior change.
- **A config path component that names a Windows device, or ends in a period or space, is
  refused at load** (#480). Values that were accepted before — `skill_tree = "NUL"`, a
  `seed_files` entry of `aux.json`, a `worktree_seed` of `.claude/skills.` — now raise at all
  seven validation sites: `scm.worktree_seed`, an adapter's `hooks.config_path` / `skill_tree` /
  `seed_files`, a plugin's `seed_files` / `seed_globs` and `[python] module`, and the Unity
  seeder's guard dir. Such a component names a _different_ path on Windows than the one it
  spells — a device rather than a file, or a sibling once Win32 strips the trailing run — so the
  file that gets seeded and the exclude pattern rendered from the authored spelling disagree
  about which path they mean. The refusal is cross-platform on purpose, matching how the family
  already rejects `C:\secrets` on POSIX: a config value must not mean one thing per host. A
  component of only periods and spaces embedded beside a real one (`sub/...`) is refused by the
  same rule — Win32 empties it and the value addresses `sub` — and the Unity seeder and a
  plugin's `[python] module` validate the authored value rather than a `.strip()`-normalized
  copy, so an authored trailing space is refused like at every other site instead of silently
  trimmed. No shipped profile,
  bundled `plugin.toml` or default trips it, but this is a compatibility break on
  previously-loading config.

### Fixed

- Bound the GitHub release body `scripts/release.py publish` sends at GitHub's
  125,000-character limit, cutting at an entry boundary and linking the full
  `CHANGELOG.md` section. An oversize section was rejected with HTTP 422 only after
  `gh release create` had pushed the tag, stranding a tag with no release that the
  next publish then treated as already published. `prepare` warns when a section
  will be truncated.

- Bind legacy migration dispatch and publication to the ledger bytes actually accepted
  (DW-311, DW-316). Retire stale recovery authority when the ledger changes before
  the true post-hook adapter-launch boundary, then publish a validated one-path,
  clean-filter-normalized candidate through a prepared expected-old transaction on
  the captured terminal direct branch. Resolve lost commit acknowledgements by
  deterministic replay, and reconcile the target index against bounded stable checkout
  observations while preserving unrelated stages. An absent committed target is accepted
  only when the baseline commit proves the ledger was never tracked: a ledger a rival
  commit deleted after the baseline was taken refuses publication instead of being
  silently re-added on top of that commit, the committed twin of the staged deletion
  the publisher already refuses; a ledger the transition itself published that a later
  commit removed refuses its replay the same way. The candidate carries the live ledger's
  own bytes, read once they are proven to decode to the accepted text, so the committed
  blob is what `git add` of the validated file stages under any line-ending configuration
  and a CRLF checkout is not left dirty beside an LF commit; every later validation
  re-reads those bytes and holds the target's size, mtime and ctime with its inode, so a
  rewrite in place — rival bytes, or the same text under other line endings — is refused
  before the transaction commits rather than noticed after it. The baseline's identity
  is the blob its commit holds, bound to the baseline text under the ledger readers'
  universal-newline decoding, rather than the LF blob re-encoding that text names: a
  tracked legacy ledger Git preserves with CRLF bytes (`core.autocrlf=false`, the
  shape every Windows-written ledger takes) was refused as rival content and left the
  migration in COMMITTING for good.

- Refuse no-descriptor attempt-owned spec restoration before staging or lifecycle
  normalization, preserving the existing target bytes for manual recovery (DW-310).

- Fail closed after no-descriptor attempt-owned spec publication and pause for
  manual adoption instead of trusting a path-based readback (DW-309).

- Refuse attempt-owned spec recovery when final prepublication validation observes an
  existing target was edited in place, preserving the competing bytes (DW-308).

- Restore the accepted commit chain and index when the post-squash HEAD identity
  probe fails, retaining the probe fault if rollback also fails (DW-305).

- Preserve accepted tracked artifact identities through target merge, squash,
  fast-forward, hooks, and crash replay; snapshot the complete target transaction
  into aggregate-limited streamed sidecars, preserve exact index/worktree and
  cleanup-phase state, and refuse drift with verified, retained-source recovery
  when ref, index, worktree, ignored-path, topology, or submodule evidence is unsafe
  (DW-302/DW-303). The incoming paths are held to the integrated commit too — a
  target hook's rewrite of an ordinary incoming source file, staged, left in the
  checkout, or sealed into the squash leg's own commit, is refused and restored
  rather than recorded as `unit-merged`; so is an incoming path the unit deletes
  that a target hook recreates unstaged, which no index reading can see; and so
  is any change a target hook leaves outside every receipt-owned set — a clean
  tracked file edited, staged, deleted or renamed, a new file written beside it
  — which a whole-tree reading names (after the hooks the target may hold only
  the strays the guard tolerated before the merge), the orchestrator's own
  `.waves/loop/` included — the hook relay script, a committed `policy.toml`,
  a profile overlay — with only the run's own records left out, and the
  pre-merge guard tolerating or blocking a stray there on the same terms as
  any other (and cleaning one the unit's commit also changes: the cleanup
  re-read the tree without `.waves/loop/`, so a planned path there was
  "missing" and every attempt refused before its merge, and again on each
  resume) — and a hook's `update-index --assume-unchanged` on a clean
  tracked file outside the incoming set, which status never lists, is
  refused by the receipt's digest of every other index entry's flag word
  and named from its map of the marked ones — and a hook's overwrite of a
  file the index already trusted unread when the receipt was armed
  (assume-unchanged or skip-worktree), which moves no word, no blob and no
  status or diff reading, is refused by the receipt's `lstat` identity of
  that file, the way an ignored file's overwrite is (a rename's source is incoming
  too — `diff --name-only` had named the destination alone — so a renaming
  bundle is not refused over the entry its merge deletes), and a hook's
  gitignored write anywhere — beside an incoming path in a directory the
  target already held populated, which no reading listed, over an
  ignored file that was already there, which leaves the path set unchanged
  and `status` and `diff` silent, or its deletion of one, which they are as
  silent about — is refused by the receipt's sealed
  listing of the whole tree's ignored entries, each with its `lstat`
  identity (a sidecar under the operation's capture root; bytes never
  read; a tolerated stray an incoming `.gitignore` change turned ignored
  left out, and an entry beneath an incoming path git's own write clobbered;
  the refused receipt's residue reading skips the recorded side, so
  deleting a named rewrite clears it and a named removal is the operator's
  to weigh before resuming) and named — a listing that also walks
  the tree for every nested `.git` entry, which git lists in no reading at
  all, so a hook's `git init` beneath a populated tracked directory, or a
  repository it puts in an ignored one, is refused the same way (each
  repository boundary one entry; the `.git` of a checkout the submodule
  reading accepts at a gitlink the unit introduced tolerated) — and a
  hook's write a captured populated submodule's own `.gitignore` covers,
  which that listing never descends to, the checkout reading never asked
  for, and the superproject's `status` never reports, is refused by the
  listing the receipt seals of each such checkout's ignored entries beside
  its HEAD — into a submodule the unit leaves alone, one whose gitlink it
  rewrites, or the leftover git could not remove, the unit's own paths
  written into a replaced leftover left out, and a `.waves/loop/` the
  checkout's own rules ignore read like any other path there (the run's
  records are the target's alone, left out of the target's listing only);
  a hook's plain write into a captured checkout the unit leaves alone —
  which the superproject's `status` reports only as `submodule.<name>.ignore`
  allows, and a tracked `.gitmodules` setting `dirty` or `all` to quiet
  that noise hid from every whole-tree reading — is refused by the
  checkout's own `status`, the reading the capture required empty, and the
  restore's own;
  an untracked nested repository in the target — the one entry `status`
  still collapses, `vendor/` — is tolerated as `vendor` and passed over by
  the capture, its `.git` and every entry of its tree sealed at their
  identities (the listing walks a nested repository git tracks nothing
  under — that one, or an ignored one — like the ignored directory it
  stands in, since no git listing descends into it and no reading captured
  it, so a hook's write over `vendor/tool.py`, which changes no listing,
  is named after the hooks; a boundary git tracks something beneath stays
  that reading's, and the leftover of a deleted gitlink the captured
  checkout's), where its spelling had
  paused every receipt-bearing integration before the merge as malformed
  and again at each resume; the restore reverts what
  the hook staged and leaves unstaged, untracked and ignored entries in place, named
  for the operator — and a resume over that residue is refused until it is
  cleared (a resume after the hook was disabled read the restore complete,
  which it is for the receipt's own paths, and re-armed over the target as it
  stood: the untracked write a tolerated stray, the ignored one an entry of
  the new listing, the flipped word a marked entry, and the retry recorded
  `unit-merged` with the refused output still there); the refused receipt's
  readings are taken again before either re-arm, at the restored epoch or
  after a commit the operator made since, with the receipt's own paths left
  to the restore's reading, and name what stands — the residue, or work of
  the operator's since, which they cannot tell apart and say so; and the
  `ls-files --debug` flag reading walks its records — path to the NUL, then
  the five fixed lines — instead of scanning the output for `flags:`, which
  read a tracked path holding a newline followed by that text as one flag
  word more than the index has entries and paused every integration into
  that target as malformed; and a directory the unit creates, where the receipt
  proved nothing was — or proved an empty untracked directory, which git
  never tracks and no reading lists — or where the receipt captured a
  tracked file, a symlink, or an unpopulated gitlink the unit replaced — is
  walked on disk
  against the integrated commit, so a hook's gitignored write or nested
  `.git` there — which no `status` reading lists — is refused too (that
  restore is the proved-absent directory's existing doctrine: it removes
  nothing it cannot attribute, and pauses as not safely restorable with the
  path named; the replaced file's restore goes through its own path, git
  taking the directory with it, and the replaced gitlink's puts the empty
  directory back once git has taken the commit's files, refusing over
  anything else left there). A unit
  that deletes a populated target submodule integrates: git leaves the checkout
  behind (`?? path/`), which is accepted only as the exact captured checkout
  and otherwise refused, with the refusal's restore undoing a hook's writes
  into a captured submodule checkout rather than pausing unrestored; a unit
  that replaces a populated submodule with a tracked directory integrates the
  same way — git writes the commit's files into the checkout it could not
  remove, and that leftover is accepted only owned, at the captured HEAD, and
  holding nothing beyond what the integrated tree holds under it. A gitlink
  the unit adds is read the same way as a captured one — index at the gitlink
  (skip-worktree accepted on a sparse target's out-of-cone gitlink — on a
  sparse target only, git stripping a hook's bit from an in-pattern entry
  and a hook alone setting it elsewhere — and a hook's `update-index
  --assume-unchanged` or `--skip-worktree` on an incoming file, which no
  diff reading sees, refused by its index flag word, and an incoming entry
  that word leaves git trusting unread — the captured bit a hook puts back
  over its own bytes, which every git reading of the checkout then trusts —
  read from disk against the integrated commit (type, blob, exec bit, or
  absence under skip-worktree alone); an
  operator's assume-unchanged bit on a captured gitlink is recorded and
  preserved — every modern integration into a target holding one paused,
  even of a bundle that never touched the submodule — a hook's flip of the
  captured word is drift, and the restore puts the word back where
  `git restore` cleared it; a crash replay of a `cleanup-pending` receipt
  takes a cleaned tracked collision for the planned result only with the
  captured index entry still there, flag word included — the two content
  probes read clean over an assume-unchanged or skip-worktree entry
  whatever the worktree holds, so a flag an operator set after the host
  died, and any edit under it, read as the planned result and the resume
  put the captured entry back over them; every flag-word reading masks to
  the bits the index file holds — on a `core.fsmonitor` target git's
  in-process fsmonitor-valid bit read as identity, refusing the rollback
  that recreated an entry without it and reading every fresh entry as a
  hook's),
  a populated checkout this repository's, clean (ignored entries included, the
  path having been proved absent), at the gitlink — since an
  incoming `.gitmodules` with `ignore = all` hides a hook's `submodule update
--init` and everything it writes from every `git diff` reading; the restore
  removes such a hook-made checkout at a receipt-proved-absent path — and the
  accepted artifact paths are
  resolved before the receipt is armed, so a resolver refusal pauses ahead of any
  target mutation instead of snapshotting short of them. A collision-cleanup fault
  restores only the paths the cleanup touched, never a planned path it had not
  reached. Restoration completeness reads the receipt-attributable inventory, so an
  operator's unstaged edit elsewhere during the merge window no longer fails a
  completed restore or blocks its replay; a refused no-ref-update attempt records
  its unchanged revision so the receipt stays replayable instead of reading as
  malformed on resume. A unit that turns a tracked file into a directory
  (`a` deleted, `a/b` added) integrates — the capture read the leaf beneath
  the file as a fault rather than as absent, pausing before the merge and
  again on every resume — and its refusal restores the old shape through the
  parent path alone, git refusing the pair (a symlink it turns into a
  directory — a dangling one too, whose leaf beneath is absent by topology
  rather than "an unavailable parent", and one that resolves, into the
  repository or out of it, to a directory holding the leaf's own name,
  which the capture dereferenced and refused as a redirected parent or an
  escaped path: git tracks no path through a symlink, so a leaf beneath a
  link the incoming set replaces is absent by topology wherever the link
  points, the link captured and put back as bytes under its own path and
  every receipt reading confining the leaf by the link's parent rather than
  reading through it — the checked-path restore refusing a parent swapped
  for a link before its first write — and the reverse transition, a tracked
  directory the commit turns into such a link, no longer read as a deleted
  leaf recreated — and a leaf it puts deeper beneath the file, restore the same
  way: the restore refused the put-back symlink as a redirection and crashed
  opening the restored file as the deeper leaf's parent); a target cloned without
  `--recurse-submodules`, every gitlink an empty directory, integrates too —
  the capture probed each one for its superproject and called it foreign —
  and the receipt records such a gitlink unpopulated, so a checkout a target
  hook's `submodule update --init` makes there is the refusal's to remove
  (a repository of any other kind there refuses the restore) rather than
  the next capture's baseline. Receipt paths are held to the Win32 name
  rules — reserved characters, device aliases, a drive prefix, a backslash —
  on a Windows host alone: on POSIX git permits `:`, `?`, `*`, `\` and
  control characters in a name, every reading round-trips them
  NUL-delimited, and holding them everywhere paused each modern bundle that
  touched such a file as malformed (containment — absolute, `..`, `.git`, NUL —
  holds on every host); an ignored file that was already there and that an
  incoming `.gitignore` change uncovers — `??` after the merge, never in
  the tolerated set since the pre-merge guard never listed it — is no
  longer named as a hook's stray when the receipt's ignored listing holds
  it at the identity it still has (it used to pause every retry until the
  operator deleted it), while one the listing holds under another identity
  is still named; and the receipt's absent-parent topology is read by
  git's slash hierarchy, the one the capture wrote: the Windows reading took
  `a:` for a drive and a backslash for a separator, so a POSIX receipt naming
  such a parent was refused as malformed at the replay that needed it. No
  record retires a live receipt or stands for a modern bundle's
  completion: a coding session holds the writable run directory and can
  append a `unit-merged` row under its own key — the receipt's operation
  identity included — and it holds the shared repository, so the target
  reflog transition under that identity is its to write too (`git
  update-ref -m waves-integrate:<id>`, on a branch checked out in
  another worktree as well); reading the pair as the validated completion
  skipped the deterministic target validation after a host loss (receipt
  gone, merge skipped, publication over whatever the session had put on
  the target). A live receipt always replays the merge, which finds the
  moved ref under the receipt and validates it, or pauses with evidence;
  with no live receipt — a host lost before one was armed, or after a
  successful integration retired it — the merge replays while the unit's
  source is still mounted (it stages nothing again over a landed result,
  re-validates the target's bytes and re-records — an integration that
  made no ref update, an artifact-only bundle's squash, the same way), and
  once the completed integration has consumed the source (worktree torn
  down, branch gone) the completion stands only on the target as it is
  now — the unit's commit in its history, or, since a squash seals a
  commit of its own and never that one, every change the unit made over
  its baseline folded into the target's tree (mode and object id per added
  or rewritten path, or — where the target had moved the same file before
  the squash resolved it, so the sealed blob holds both sides' edits — the
  three-way merge of the unit's change over its baseline that stages
  nothing over the held blob; each deleted path absent) — and
  every accepted artifact blob in its tree and index — or pauses naming
  the reason (the released legacy payload integrates without a receipt
  and keeps its bare row).

- Recover sweep migration publication faults without persisting unearned `DONE`
  state (DW-296/DW-297). Persist accepted baseline/rewrite records, clear a
  pre-dispatch baseline after publication refusal, restore result-faulted ledgers
  by compare-and-set, and resume a durable `COMMITTING` task through the commit-only
  tail.

- Bind tracked and pending-tracked isolated bundle deliverables to their accepted
  Git-normalized bytes and validate their exact staged entries before commit (DW-300).
  Drift now pauses with path-only recovery evidence and retains the source mount;
  the validated index is committed without a second working-tree staging pass. The
  no-op arm is validated too: an index reset to baseline after the staged validation
  (a concurrent writer) no longer reads as "nothing to commit" with the accepted chain
  orphaned and baseline recorded as the bundle's commit — the committed-tree validator
  runs against baseline, the original chain and index are restored, and the run pauses.
  The integrated target commit and post-hook index are validated ahead of `unit-merged`
  as well, so a target-side hook rewriting a tracked deliverable in the integration's own
  commit never lands it under the bundle's name (the receipt-backed refusal and restore
  are DW-302/DW-303's, below).

- Sample destination pathname identity after streamed artifact probes, refusing observed
  detachment while retaining checked-fallback races (DW-301).

- Stream artifact destination hashing and equality checks in fixed-size chunks, bounding
  baseline-capture and publication memory even when operator-owned files are large or grow
  during validation (DW-298/DW-299).

- Restore attempt-owned specs through descriptor-capable parent-anchored publication and
  verification on POSIX, preventing late parent substitution from redirecting bytes; retain
  checked path-based restoration on no-descriptor platforms (DW-295).

- Bind explicitly published ignored bundle deliverables to the exact bytes accepted by final
  dev, repair, or review verification (DW-290). Preparation now refuses post-verification byte
  or declaration drift before freezing a payload, retains the source mount and evidence for
  recovery, and cannot refresh authority by replaying the same accepted result after a crash.
  It re-derives the tracked declaration set too, so a spec outside `implementation_artifacts`
  cannot swap one tracked deliverable for another after acceptance (Codex P1 on #795).

- Bound isolated artifact publication payload preparation (DW-289) to measured raw-byte
  defaults of 5 MiB per ignored file and 10 MiB aggregate. Preflight now rejects an
  oversize selection before any base64 encoding, bounded reads catch file-growth races,
  and the existing refusal pause retains the source for a no-redispatch resume. Tracked
  declarations do not count, exact limits remain legal, and frozen legacy payloads still
  replay idempotently.

- Refuse concatenated `Artifactonly: true` assertions while preserving accepted
  separated spellings (DW-291). The artifact-only line's gaps now take the same
  horizontal-whitespace class as `Status:` (DW-285), so a vertical separator such as
  `\x0b` between the label and `true` no longer mints the receipt.

- Preserve attempt binding and seed-delivery observer fallbacks when named path
  resolution guards receive embedded-NUL or lone-surrogate faults (DW-292/DW-294).

- Distinguish ownership-path resolution faults from proven-external paths at the
  residual deferred-work and sprint-board probes, preserving conservative recovery
  and carry behavior (DW-293).

- Handle embedded-NUL and lone-surrogate faults at the named observation,
  configuration, stories, worktree, restore, and recovery resolution guards (DW-287).

- Route terminal isolated sweep harvest-carry read faults through the sweep
  story-gate repair pause while preserving the engine route for direct defer and
  ordinary story carries (DW-286).

- Parse independently bold Auto Run `Status` values without allowing bare labels
  to consume next-line tokens (DW-285).

- Preserve explicit ignored bundle artifacts before isolated worktree teardown; capture
  destination baselines, refuse conflicting edits, and replay interrupted publication
  without losing recoverable sources (DW-283). This lifts the interim refusal of the
  artifact-only receipt for an artifacts dir rebased into a unit worktree: the
  accepted spec is carried by publication, so the receipt stands under isolation.

- Advertise conditional artifact-only receipts in all bundle prompts and sweep
  triage guidance, including verification gates and isolated-publication limits (DW-284).

- Show unreadable sweep-ledger refusals and repair guidance on dashboard resume
  before launching a detached window (DW-270).

- Pause existing engine and sweep locked-read repair routes on OS metadata and
  text-read faults, preserving task phase, pending work and ledger bytes (DW-279).
  Wrap these faults as `LedgerReadFault(LedgerReadError)` with the original
  `OSError` chained; retain absence/decode handling, OS refusal attribution, and
  raw `OSError` from pre-lock probes, lock acquisition and writes.

- Resume a pending review-timeout salvage refile over the preserved product after
  ledger repair, rerunning verification without rebuilding or new dev/review sessions
  under either rollback policy; retain ordinary commit gates (DW-278). The latch is
  set at every salvage's handoff save — the first, fault-free salvage included, not
  only the repair-pause arm — so a host lost between that save and the commit
  (notification, a `pre_commit_gate` workflow) replays the salvage with zero sessions
  instead of restart recovery, which erased the published refile under rollback and
  paused without it. A sweep bundle has no replay arm and restarts instead; its
  restart now clears the latch, which otherwise rode onto the replacement attempt and
  forced a review the fresh attempt never asked for.

- Notify operators when a ledger snapshot outage leaves story-declared deferred
  closes unapplied, naming the story, every declared ID, and the fault (DW-277).

- Fold a `ValueError` from the publisher target resolve into `target-unreadable` at
  the three publisher arms — `engine._publication_refusal`, `SweepEngine._commit_ledger`,
  `decisions.apply_pre_answer` — instead of letting it escape best-effort bookkeeping
  (DW-275). `Path.resolve()` raises `ValueError` for an embedded NUL, and its
  `UnicodeEncodeError` subclass for a lone surrogate, on CPython 3.11-3.14 POSIX; the
  arms caught `(OSError, RuntimeError)` only. The refusal row, journal row and cause
  are unchanged; the fault text rides in `error`.

- Pause at the story gate under `sweep-bundle-close-refused` with a `-locked` site,
  instead of `run-crash`, when a deferred-work ledger turns undecodable inside the
  locked window of one of the sweep's three bundle-close mutator calls — the
  accepted-dev close, the review-leg reclose, the isolated close carry (DW-280,
  the DW-259 residual). The task's phase and recorded close intent are left
  untouched, so `waves resume` re-drives the close — with no session spent at
  the accepted-dev close and the carry; through the sweep's restart arm (the
  bundle re-driven from dev) at the reclose. DW-279 extends the same locked-read
  route to OS metadata/text-read faults, and the row keeps that classification:
  `reason="ledger-inaccessible"` with a permissions-or-storage steer for an OS
  refusal, `reason="ledger-unreadable"` with a UTF-8 steer for undecodable bytes,
  never the decode token for both; lock/write failures remain raw `OSError`.

- Pause for repair under `ledger-read-refused` with a `-locked` site, instead of
  `run-crash`, when a deferred-work ledger turns undecodable inside a mutator's own
  locked window — the harvest's seen-again mark and append, the commit-boundary
  `closes_deferred:` close, the review-timeout salvage refile, the isolated harvest
  and close carries (DW-259). `waves resume` retries the write; the notice now
  names a declared close. DW-279 extends the same locked-read route to OS
  metadata/text-read faults; lock/write failures remain raw `OSError`.

- Route a deferred-work ledger read the OS refuses (EACCES, EIO, ELOOP) at the
  engine's four direct `read_for_write` sites the way DW-231 routes a decode fault
  (DW-258), instead of ending the run as `run-crash` with the completed session's
  work on disk. The observation reads (proof-of-work digest, pre-harvest and defer
  snapshots, both restores) degrade to a typed `_UnreadableLedger` that carries no
  digest and journal `ledger-read-degraded`; the two publish reads (spec-deferral
  harvest, isolated carry) journal `ledger-read-refused`, notify `ACTION REQUIRED`
  (now naming both repairs: valid UTF-8; permissions or storage) and pause without
  changing the task's phase, so `waves resume` after the repair replays the
  recorded session result. The attribution digest of a refused read is the
  `<unreadable>` sentinel, and `_ledger_changed_since_baseline` treats a sentinel
  on either side as unknown — never credited — so the engine's own harvest append
  after the repair cannot pass a session that wrote nothing.
- Arm the sweep's persisted ledger doubt when the ledger's path cannot be resolved,
  so the cycle's bundles are withheld instead of crashing at the bundle intent's
  own ledger read (DW-260). A git-fault degrade after a successful resolve stays
  un-armed; the `sweep-ledger-commit-unavailable` row is unchanged on both arms.
- Make a resumed sweep honour and announce its own persisted ledger doubt (DW-246,
  DW-244, DW-251). The three ledger publishers that run on a resume ahead of the
  dispatch gate — the already-resolved close's own publish, its stranded-close
  republish, and the publisher above the loop body (the post-recovery publish, and
  the persisted commit-debt settle it shares — the only trigger that still reaches
  it under doubt, since the recovery pass itself is withheld whole) — now read
  `_ledger_unfit_to_publish()` and journal `sweep-ledger-commit-withheld`
  (`message`, `file`, `reason="ledger-in-doubt"`) instead of committing a ledger
  the run already holds unfit, or silently skipping the settle; a ledger-family `sweep-ledger-commit-refused` arms the persisted doubt after
  its row, so a refusal after a landed decision effect withholds the cycle's bundles
  instead of crashing at the bundle intent's own ledger read (store refusals arm
  nothing; a refusal at the cycle-boundary publisher, which sits below the unfit
  stop, is honoured one cycle later — cycle N+1 withholds and ends on the unfit stop
  unless one of its own effects lands and releases the arm); and the nothing-open
  exit writes the ledger-repair ATTENTION notice when the doubt is armed — the
  arming class never wrote one, so the run that withheld said nothing — with its
  rows and return unchanged.
- Gate the nothing-open exit's stranded-close publisher whole on the run's persisted
  ledger doubt, and probe its decision ids individually (DW-250, DW-249).
  `_publish_stranded_close` now reads `_ledger_unfit_to_publish()` once, above BOTH of
  its probes, after the triage cache validates and the plan names at least one id:
  a doubted resume journals `sweep-ledger-commit-withheld` with the close message,
  `file`, `reason="ledger-in-doubt"` and a `dw_ids` list naming every cached id it
  declined to prove, instead of publishing the whole ledger — unaudited flip included
  — on an already-resolved id that read `done`, or returning silently on a
  decisions-only plan; an empty plan and a fresh sweep still reach no read and no
  row. The decision term is now an `any` over the plan's decision ids (the
  already-resolved term and the close phase's own arm keep their `all`), so one
  decision id absent from the ledger or carrying an unparseable status no longer
  vetoes a stranded close under its sibling; the decision set is still read once,
  an empty list still authorizes nothing, and read faults still degrade to
  `sweep-resolved-close-unavailable` with the union of ids.
- Route a deferred-work ledger read fault at the engine's own sites and at the resume
  gate (DW-231, DW-234). The base engine now catches `LedgerReadError` at its four
  direct `read_for_write` sites: observation reads (proof-of-work digest, pre-harvest
  and defer snapshots, both restores) degrade to a typed answer nothing can write back
  and journal `ledger-read-degraded`; the two publish reads (spec-deferral harvest,
  isolated carry) journal `ledger-read-refused`, notify `ACTION REQUIRED` and pause
  the run without changing the task's phase, so `waves resume` retries the write
  instead of crashing as `run-crash` — replaying the recorded session result where
  one exists (dev and review legs), re-driving the leg otherwise. The residual —
  `deferredwork` mutators' own locked re-reads and the review-timeout salvage refile
  still raised — was recorded as a deferral and is closed by DW-259 (entry above).
  `runs.unreadable_sweep_ledger` gains the `except OSError` arm — its own
  permissions-or-storage attribution on the `waves sweep`
  route the sweep's own stop already gives — a recorded reversal: the arm was
  written, struck by the DW-204 resolution on scope grounds, and is restored under
  DW-234's accepted decision; the TUI's stopgap `except OSError` around the probe is
  removed as dead.
- Propagate ledger metadata refusals consistently across supported Python versions
  (DW-221). Treat ELOOP and EBADF as errors; a cyclic ledger symlink is a refusal
  rather than an absence at every `read_for_write` site — routed where the harvest
  reads (DW-258 above: degraded observation, paused publish); where no publish read
  is reached, the story completes and a declared close journals the outage.
- Report refused sweep ledger metadata as `ledger-inaccessible` with error details
  and arm ledger doubt through the existing reader handlers (DW-253).
- Report directories, FIFOs and sockets at the ledger path as `target-not-a-file`.
  Preserve `target-unreadable` when metadata becomes inaccessible between probes
  (DW-238).
- Guard the five remaining `verify.commit_paths` callers with the publishable-target
  check their sibling publishers already take, so a directory left at a ledger, board,
  spec or park-record name is no longer handed to `git add` as a literal pathspec and
  staged recursively under a `chore(...)` message. A refusal is journaled
  (`harvest-carry-refused`, `story-deferred-close-carry-refused`,
  `sweep-bundle-close-carry-refused`, `board-advance-carry-refused`) or, in `confirm`,
  drops that operand alone; it never raises, and `confirm` still commits an ABSENT park
  record's deletion. The guard's ledger leg now tells a DURABLE decode fault
  (`target-undecodable`, a fourth `refuse_cause`) from a TRANSIENT OS fault
  (`target-unreadable`), so the harvested-deferral carry refuses the former outright
  and hands only the latter back to git, where its commit latch survives — an
  undecodable ledger no longer reaches HEAD through that fall-through (DW-237).
- Probe operand presence in `commit_paths` with `lstat`, which suppresses nothing on
  any interpreter, so a tracked candidate under an unsearchable parent is reported as
  uncertain instead of being ruled missing and staged as a deletion on Python 3.14
  (DW-239).
- Take the readable-ledger refusal at `waves resolve`'s entry and at the TUI's
  re-arm gesture, ahead of the interactive session and of `rearm_escalation`, so an
  escalated sweep over an undecodable ledger keeps its escalation instead of spending
  it; one shared probe now serves all three surfaces, and `docs/FEATURES.md` documents
  the refusal, its declines and its precedence (DW-229, DW-230, DW-235).
- Screen an adopted `build` answer against the ledger's live open set before it mints a
  bundle, dropping an id the ledger no longer holds open under a fifth `drop_cause`,
  `entry-not-open`; a ledger read that refuses screens nothing and journals
  `sweep-decision-open-set-refused` (DW-214).
- Recover stranded decision closes at the sweep's no-open exit, withholding the
  whole recovery publish — its already-resolved term too, since the commit is of
  the file — while the run retains ledger doubt; the close phase's own two commit
  arms read the same verdict, so a resume that inherited a doubt no longer walks a
  half-landed decision flip into HEAD ahead of the dispatch gate (DW-222).
- Retry ledger publication before repeating sweeps stop on `no-progress` or
  `max-cycles`; rename the commit message to
  `chore(sweep): commit ledger at the sweep cycle boundary` (DW-223).
- Degrade triage-cache metadata read failures to `sweep-triage-reload-failed` and
  fresh triage, with absent caches remaining silent (DW-224).
- Degrade a refused triage-cache write-back to a new `sweep-triage-cache-write-failed`
  journal kind and still return the validated plan, instead of crashing the sweep
  after a healthy triage; a directory planted at the cache path lands on the same
  row (DW-247).
- Pause a resume at the story gate when an in-flight bundle's intent document must
  be regenerated and the ledger read refuses, journaling `sweep-intent-ledger-refused`
  (`ledger-unreadable` / `ledger-inaccessible`) and leaving the run resumable and the
  bundle task PENDING, instead of crashing at that read ahead of every cycle gate;
  `waves resume` after the repair re-drives the same bundle (DW-243).
- Screen every bundle reaching the final keep loop — a cached plan's own bundles
  included — against the ledger's live open set, skipping one whose ids are not all
  open under `sweep-bundle-skipped` `reason="entry-not-open"`; `_write_intent` now
  refuses (`MissingLedgerEntriesError`) to render a document for a bundle id with no
  ledger entry, and the regeneration path journals that refusal as
  `sweep-intent-regen-refused` and pauses the run the same way rather than dispatching
  a session briefed on an empty entries section or letting fresh triage run beside
  the refused bundle (DW-252).
- Unlink a triage cache whose read faults before re-triaging
  (`sweep-triage-cache-invalidated`, or `sweep-triage-cache-unlink-failed` on a refused
  unlink) and write the cache back atomically, so a refused or short overwrite can no
  longer leave an older or torn plan for the next resume to replay (DW-263).
- Probe `<run>/decisions.json`'s metadata with `stat()` rather than `is_file()` so a
  refusal of that probe degrades to `sweep-decisions-reload-failed` and the pending path on
  Python 3.11–3.13 instead of aborting the sweep over a bookkeeping read (DW-248).
- Degrade a refused SEEDED write-back of `<run>/decisions.json` (a directory planted at
  the store; a refused or redirected parent — `UnconfinedWriteError`, the #593 confinement
  refusal) to a new `sweep-decisions-store-write-failed` journal kind naming the adopted
  ids, and carry on with the answers in memory, instead of aborting an otherwise healthy
  sweep; the interactive write-back stays bare so a human's answer whose write FAILS still
  stops the sweep loudly (DW-262).
- Withhold the seeded `<run>/decisions.json` write-back for the cycle when the store's
  metadata probe or content read was refused with an `OSError`, journaling
  `sweep-decisions-store-write-withheld` with the adopted ids whose answers stay in memory,
  so a transient read refusal no longer replaces a store of valid answers with an empty
  map; decode faults and a non-object top level still replace the file wholesale (DW-264).
  In the same cycle the interactive prompt is not put at all
  (`sweep-decisions-prompt-withheld`, ATTENTION notice): an answer that cannot be
  persisted is not taken, so a crash can no longer lose a `build` authorization held only
  in memory; the decisions stay pending for the next interactive sweep.
- Raise a refused ledger out of the five write-bearing mutators (`mark_done_many`,
  `mark_seen_again_many`, `mark_open_many`, `record_decision`, `archive_closed`) on
  every interpreter: their pre-lock presence guard is `stat()` + `S_ISREG` and the
  under-lock guard is the reader's own absence answer, so on Python 3.14 an `EACCES`
  ledger no longer takes the no-op return — `sweep --archive` reporting success having
  archived nothing, `record_decision` answering "no such entry" — and ELOOP and EBADF
  move to the fault side on Python 3.11–3.13 too, so a symlink loop at the ledger's name
  now raises out of all five instead of taking the no-op return. An absent ledger still
  returns the no-op value without a lock (DW-255).
- Answer the publishable-target guard's store leg from one `lstat()`, so a refused
  store is `target-unreadable` on Python 3.14 too, where the
  `is_file()`/`is_symlink()`/`exists()` probes suppressed the refusal and degraded it to
  `target-absent`; a regular file and the 3.13+ symlink-loop link entry still publish,
  a directory or FIFO is still `target-not-a-file` (DW-257).
- Probe the project-level pre-answer store's metadata inside `load_pre_answers`' own
  guard, so a refusal degrades to `{}` as the docstring promises instead of re-raising
  out of `_decisions_phase` on Python 3.11–3.13 (DW-261).
- Probe the ledger's metadata with `stat()` + `S_ISREG` in `read_for_observation`, so a
  refused ledger degrades to an attributed `PermissionError:` fault on Python 3.14
  instead of silent absence; `ENOENT`/`ENOTDIR` and a non-regular file stay absence,
  and a symlink loop is now an attributed fault at the observation arm as it already
  was at the write arm (DW-254).
- Probe the ledger's metadata with `stat()` + `S_ISREG` inside `Engine._refuse_gated_story`'s
  own `try`, so a refused ledger pauses the run at `PAUSE_STORY_GATE` on Python 3.14 too,
  where `is_file()` suppressed the refusal and the `gate:` hard gate failed OPEN — the story
  dispatched and `story-gate-unreadable` was unreachable; `ENOENT`/`ENOTDIR` and a
  non-regular file stay the empty ledger, and a symlink loop at the ledger's name now
  pauses at the gate instead of passing it (DW-266; also closes DW-276). A configured
  ledger path the OS cannot encode takes the same pause instead of crashing the run.
- Same probe inside `validate`'s deferred-ledger read and `verify_review_bundle`'s, so on
  Python 3.14 a refused ledger is the `deferred.ledger-unreadable` problem rather than a
  clean deferred check, and the non-fixable "deferred-work ledger unreadable" retry rather
  than the fixable "entries not marked done" one (DW-267). A configured ledger path the
  OS cannot encode is that problem and that retry rather than a crash.
- Take ledger absence from the observation reader's own answer in `sweep --dry-run` and
  `SweepEngine._non_write_state`, and probe the archive's post-report presence inside its
  `try`, so a refused ledger is the attributed `error: ... cannot be read` failure, the
  "holds no entry" fallthrough and the `cannot archive` failure respectively — not "no
  deferred-work ledger" / "the ledger file is gone" on Python 3.14, and at the two CLI
  sites not a `PermissionError` traceback on 3.11–3.13 (`_non_write_state` already
  degraded there). A 0-byte ledger now reads as "no deferred-work ledger" in the dry-run
  listing (DW-265).
- Retire the two decision non-write `is_file()` probes that DW-265 left behind: the
  sweep's interactive decision arm now takes its `sweep-decision-effect-unavailable`
  sentence from `_non_write_state`, and `waves decisions`' outcome line asks the
  observation reader, so a refused ledger reads "holds no entry for this id" and
  "no decision line was written; ledger state unavailable" respectively on Python 3.14
  — not "the ledger file is gone" — and the sweep arm no longer ends `run()` with a
  `PermissionError` on 3.11–3.13. The sweep-arm exposure is the window between the
  recorder's False answer and the diagnostic probe (a ledger refused at the recorder
  itself already took the `except` arm). Absence still reads "gone" at both sites, and
  a present 0-byte ledger reads "holds no entry" at both — the recorder reached it and
  found nothing — through a presence-aware sibling of the observation reader
  (`deferredwork.observe_ledger`, `None` text for absence) rather than the text-only
  reader's empty text, which had made an empty ledger read as gone (DW-281, DW-282).
- Absorb pathlib's ignored winerrors (21 `ERROR_NOT_READY`, 123 `ERROR_INVALID_NAME`,
  1921 `ERROR_CANT_RESOLVE_FILENAME`) and the `ValueError` a non-encodable path raises as
  ABSENCE at the ledger's repair/write reader, the five mutators' pre-lock guard and both
  legs of the publishable-target guard, through one shared `deferredwork.probe_absence`
  — the set `is_file()` absorbed before the `stat()` probes replaced it — so a ledger on
  a disconnected mapped drive or at a lexically invalid Windows path now READS AS ABSENCE
  (an empty ledger) at every `read_for_write` consumer, as it did before DW-221: the
  sweep's cycle gates end on `no-open` instead of `ledger-inaccessible`, the resume entry
  gate admits the resume instead of refusing with the DW-234 storage-fault route, and the
  mutators take their no-op return. A NUL in the store path no longer escapes the guard
  as a `ValueError` (the publishers' own `resolve()` arms still raise it on POSIX,
  unchanged).
  `EACCES`/`EIO`/`ESTALE`/`EBADF`/`ELOOP` and every other winerror still raise or fold
  to `target-unreadable`; `commit_paths` keeps reporting the winerrors into uncertainty
  (DW-256, DW-268).

- Mirror a sweep cycle's ledger-in-doubt verdict onto run state at every site that
  ARMS it — not at the dispatch gate, and not at the decision phase's tail publish,
  whose span contains a human at a prompt — so a stop or crash between the arm and
  the gate's report resumes into the same withholding rather than into a dispatch
  that publishes a half-written ledger. Released again by the two sites that clear
  the walk's own verdict — but only for an arm THIS process made: the mirror is
  held while the close phase's latch is armed this cycle, and whenever it was
  inherited across a resume, so in those two states it is deliberately stickier and
  waits for a human repair plus a fresh sweep. The mirror also outranks the
  persisted commit debt (`sweep_ledger_commit_owed`): a resume that inherits both
  skips the top-of-`_loop` settle, since the doubted bytes are the debt. And it
  withholds the resume's in-flight recovery pass whole: a bundle re-armed out of
  band by `waves resolve` is not re-driven while the mirror is on disk — its
  own commit is a whole-tree `git add -A` — and is journaled as withheld and then
  stranded rather than dispatched around the gate. Legacy prose met on such a
  resume is not migrated either: the rewrite session and its commit are refused
  on the doubt's own `ledger-unreadable` stop and repair notice (DW-218/219).

- Withhold sweep bundles and ledger commits after close, re-apply, or idle decision
  faults; preserve pre-answers while the ledger is in doubt (DW-216/217/220).

- Publish the out-of-band decisions answer ONE OPERAND AT A TIME, each rooted at that
  operand's own resolved parent, and report a publish git could not make. One
  `commit_paths(project, ...)` call over both operands failed two ways: a ledger
  configured outside the project (or inside a disjoint `repo_root`) was relativized
  away by `commit_paths`' `except ValueError: continue`, so the `decision:` line
  reached no history and neither surface said so; and a gitignored operand made
  `git add` exit 1 and took its publishable sibling down with it, swallowed by a bare
  `except GitError: pass`. A `GitError` is now caught per operand into a
  `PublishFailure` that the CLI line and the TUI toast both print through the shared
  `publish_note()`, under a `commit-unavailable` token beside the existing refusals.
  A `build`/`keep-open` answer whose operands share a repository now makes two commits
  carrying the same message (DW-225, DW-226).

- Refuse to publish a decisions store that is present but not a REGULAR FILE, under a
  third `refuse_cause` token, `target-not-a-file`, preserving the existing symlink-loop
  exception. The publishable-target guard checked
  existence only, so a store replaced by a directory (or by a symlink to one) passed it
  and `commit_paths` handed that literal pathspec to `git add`, which stages the
  directory's descendants recursively. `is_file()` follows symlinks, so a store
  symlinked to a regular file still publishes, and the store's bytes are still never
  examined (DW-211, DW-228).

- Fold a metadata-probe fault into a refusal instead of letting it escape a best-effort
  publisher. On Python 3.11-3.13, `Path.exists()`/`is_file()`/`is_symlink()` raise on
  anything outside the `ENOENT`/`ENOTDIR`/`ELOOP` class, so an `EACCES` arriving after a
  successful write aborted `waves decisions`' walk or undercounted a TUI answer; the
  store guard now answers `target-unreadable` and `commit_paths` omits only the faulted
  candidate, raising just when no usable operand survives. Python 3.14 suppresses all OS
  errors inside those three convenience probes, so both sites have since moved to `lstat`
  instead (`commit_paths` under DW-239, the store guard under DW-257), which reports the
  fault on every interpreter and makes this fold uniform across them
  (DW-227).

- Refuse `waves resume` for a sweep run whose deferred-work ledger does not decode,
  naming the file, the decode fault and the repair. Such a resume used to arm the run (pid
  publication, policy re-stamp, `run-resume` row) and only then meet the ledger, stopping
  with no repair route offered from this surface. An absent ledger is not a refusal and
  story runs are unaffected (DW-204). DW-234 also routes OS refusal at this entry
  gate with a permissions/storage repair notice; DW-279 preserves that attribution
  when `read_for_write` wraps the original `OSError` as `LedgerReadFault`. The
  metadata probe reports refusal on every supported interpreter since DW-221.

- Diagnose a `null` or bare-string member of a migration result's `mapping` list as the
  shape fault it is — `mapping[0] not an object: NoneType` — instead of reporting
  `mapping invents unknown key ''` into the migrate-decision journal record, the retry
  feedback the next migration session is handed, and the attempt-cap escalation
  reason (DW-190).

- Prevent out-of-band decision answers from committing a vanished ledger's deletion
  or files the answer did not write. Report refused publication in the CLI and TUI,
  preserving the recorded count and decision walk (DW-209, DW-213).

- Commit an already-resolved close whose ledger write landed but whose commit never
  ran. A crash between the two left the resume replaying a triage plan that flipped
  nothing, so the durable write stayed off HEAD for the rest of a single-cycle run.
  The close now also publishes when every id the plan named already reads `done` on
  disk — proved per id, never from ledger dirtiness — and a read fault there degrades
  through the existing `sweep-resolved-close-unavailable` row. Where the stranded
  close retired the LAST open entry the phase never ran at all, so the same publish
  now also happens at the sweep loop's nothing-open exit, gated on this cycle's
  triage cache already being on disk: a fresh sweep has none and still spawns no git,
  and a cache or probe fault there journals `sweep-triage-reload-failed` /
  `sweep-resolved-close-unavailable` and publishes nothing (DW-193).

- Degrade a sweep's ledger read when the OS refuses it, at the three sites that GATE a
  cycle: the pre-answer prune and `_loop`'s two top-of-cycle reads. The other
  `read_for_write` calls in `sweep.py` are unchanged and an OS refusal there still ends
  a run as crashed. An EACCES/EIO reported a completed cycle — or a whole run whose
  earlier cycles had completed — as crashed. The refusal is journaled
  (`sweep-preanswer-prune-refused` / `sweep-cycle-ledger-refused`) and ends a run on a
  new `ledger-inaccessible` stop token, kept distinct from `ledger-unreadable` because
  the operator repair differs. `deferredwork.read_for_write` is unwidened (DW-197).

- Withhold sweep bundles when a decision effect leaves the ledger unfit to publish,
  and stop repeating sweeps with repair instructions (DW-194/202/210).

- Stop a decision effect that never landed from speaking for the human at its two
  stored-answer consumers. A stored `close` for an entry the ledger still lists as
  open is re-applied on resume instead of being counted consumed, so a crash between
  the answer write and the effect no longer leaves the decision permanently
  unapplied and never re-asked (`sweep-decision-effect-reapplied`; the write order is
  unchanged, and an unreadable or absent ledger re-applies nothing and journals one
  `sweep-decision-effect-unavailable` per candidate id) — DW-167. That replay is the
  one caller of `record_decision`'s new keyword-only `require_open`, which re-checks
  the still-open premise inside the same locked read/edit/write as the mutation, so a
  rival writer closing the entry between the walk's gate and its write is refused
  rather than given a second `decision:` line; every other caller is unchanged and
  still records on an already-closed entry. Keep metadata faults in the refusal's
  diagnostic probe from aborting the sweep. A `build` answer whose `record_decision`
  reported writing no line now takes a fourth drop lane
  (`drop_cause: effect-unlanded`) rather than materializing a bundle and spending a
  dev session on an id the ledger holds no entry for — DW-200. That verdict is
  persisted where it is observed (`sweep_unlanded_decisions` on run state, cleared by
  the drop that announces it), so an interruption between the non-write and the drop
  resumes into the same refusal instead of reviving the bundle.

- Report a ledger that took no `decision:` line at the two surfaces that answer
  decisions outside a sweep (DW-198). `decisions.apply_pre_answer` returns
  `record_decision`'s boolean instead of discarding it, so `waves decisions` no
  longer prints `closed now` and the TUI modal no longer counts the answer into
  `recorded N decision(s)` when the ledger file is gone or a rival writer retired the
  entry while the prompt blocked. Keep walking with exit 0 even if the CLI's later
  diagnostic probe fails. Report saved store answers only for build/keep-open;
  preserve the existing best-effort commit.

- Commit a ledger write an interrupted sweep phase left unpublished. The
  already-resolved close and the decision phase gate their commit on the write THIS
  invocation made (DW-183/DW-185), and a process that died between the publish and
  the commit replayed as a phase that wrote nothing — the ids already `done`, the
  answer already saved — leaving the closure dirty ahead of the cycle's bundles, to
  be absorbed by a story commit, discarded by a rollback, or left at run end. Both
  sites now persist the debt on `state.json` (`sweep_ledger_commit_owed`) before the
  write; the ledger-family `_commit_ledger` clears it once git says the file is at
  HEAD, and a resume settles an outstanding one at the top of `_loop`, before triage
  or a bundle baseline reads the ledger. An outcome that definitively published
  nothing — a fault ahead of the write, a failed atomic write, a mutator that flipped
  no ids — retracts the debt in the same invocation, so a false one never survives to
  be settled against an operator's edit; a debt inherited from an earlier invocation
  is never retracted by a replay that closes nothing.

- Handle non-dictionary session result documents through existing empty-document
  paths (DW-206/DW-207). Share read-time normalization across engine, stories,
  sweep, and verification consumers so malformed results reach the existing
  refusal paths instead of crashing; preserve dictionary identity and snapshots.

- Validate the target before publishing it in every sweep ledger/pre-answer-store
  commit (DW-199/203/205). `commit_paths` keeps a missing-but-tracked path as a
  deletion to stage, so a ledger removed after the phase wrote it was committed AWAY
  under a `chore(sweep):` message — at the decision phase's commit gate and at the
  repeat boundary — and a resume whose ledger held undecodable bytes published them
  before raising on them. Each call site now declares its file family: the five
  ledger publishers re-take the ledger's repair/write read, the two store prunes
  check existence. A refusal spawns no git and journals
  `sweep-ledger-commit-refused` with `refuse_cause` (`target-absent` |
  `target-unreadable`). The sweep loop's own read still raises on undecodable bytes;
  only the publish that preceded it is gone.

- Make `escalation._escalation_list` and `sweep._normalize_bundle_names` total on a
  non-dict JSON result document (DW-181). Return their existing empty results (`[]`
  and `()`) for wrong-shaped documents, preserving dictionary and `None` behavior.
  The normalizer previously guarded only `None`, so falsy non-dicts now return
  `()` too. This hardened direct helper calls only; the earlier engine dereference
  still crashed before a malformed session document could reach the sweep
  validators, which DW-206 above closes.

- Close the two ledger write-fault arms the DW-166 pass left bare (DW-182/186). A
  deferred-work ledger holding undecodable bytes raised out of the pre-answer prune —
  the LAST call of a sweep cycle — and reported a fully completed cycle as crashed;
  it now takes the existing `sweep-preanswer-prune-refused` row under a second fixed
  reason token (`ledger-unreadable`) and keeps every recorded answer, exactly as the
  absent-ledger arm does. And `record_decision`'s boolean was discarded, so a
  decision whose id the ledger no longer holds (or a ledger that is gone) counted as
  closed and emitted `post_decision` for a `decision:` line that was never written;
  the sweep now journals `sweep-decision-effect-unavailable` — naming which of the
  two states it was, since a missing ledger loses every line the walk already wrote
  where a missing entry loses one — and claims nothing. The commit withhold is left
  untouched by a False return rather than tripped by it: the latch still reports the
  last attempt that actually READ the ledger, which a False return may never have
  done. The prune's undecodable refusal is also carried to the repeat boundary: a
  `--repeat` run ends there on `sweep-repeat-done` `reason="ledger-unreadable"`
  (counting the cycle that completed) with a best-effort repair notification, and
  WITHOUT taking the cycle-boundary ledger commit — whose pathspec is the ledger, so
  a purely local refusal published the very bytes it had just refused to read and
  the next cycle crashed on them regardless. The completed cycle's work is kept and
  the undecodable bytes stay dirty for a human to repair. The absent-ledger arm is
  unchanged: it stays cycle-local and the next cycle ends on `no-open`.

- Narrow every sweep bookkeeping commit to the file the phase actually published
  (DW-183/185/187/188). `_commit_ledger` now takes that FILE rather than a root: it
  resolves it — following symlinks, as the atomic writer already does, so a ledger
  symlinked out of the project commits in the repository holding its target — roots
  both git calls at the resolved parent, and pathspecs the dirty check and the commit
  to that one literal name, including symlink targets with Git pathspec magic,
  and include new files even when Git hides untracked files. Unrelated edits no longer ride into a
  `chore(sweep):` commit and a prune later in the same cycle no longer publishes the
  ledger the decision phase withheld. The already-resolved close and the decision
  phase additionally commit only on a non-empty pass, so a phase that wrote nothing
  spawns no git.

- Sanitize bundle, untriaged-ID, and migration diagnostics so object values print
  their position or type instead of their contents (DW-178–180). Preserve string
  wording and acceptance behavior; render non-string scalar mapping keys without
  stringification quotes.

- Keep a sweep running when the deferred-work ledger will not read (DW-166). An
  undecodable ledger during the already-resolved close, or during an attended
  decision's effect, ended the whole sweep as crashed — on the decision path after the
  human's answer had already been saved and journaled. Both now journal the fault
  (`sweep-resolved-close-unavailable`, `sweep-decision-effect-unavailable`) and carry
  on: the answers stay in the run's `decisions.json` and the entries stay open for the
  next cycle. The PUBLISH is the exception: a ledger mutator whose atomic write fails
  (`ENOSPC`, `EROFS`, a failed rename) now raises `deferredwork.LedgerWriteError` — an
  `OSError` subclass, so the CLI and TUI degrade arms are unchanged — and both sweep
  sites re-raise it ahead of the degrade, since a repair write that failed is not a
  phase that closed nothing. Its sibling `LedgerLockReleaseError` covers the far side:
  the publish landed and the ledger lock's release then faulted (Windows `LK_UNLCK`,
  `os.close`), which the same arm had read as "nothing was written" while the closure
  was already on disk.

- Commit the deferred-work ledger in the tree that owns it (DW-175). `implementation_artifacts`
  is configurable to any absolute path, so the ledger may sit under the project, inside
  a disjoint `repo_root`, or in no git repository at all — and a single fixed root is
  wrong in two of the three. Ledger commits now name the ledger's own directory and let
  git resolve the enclosing repository; pre-answer-store commits keep naming the
  project, which is the tree that store is a bare join off. Where no repository encloses
  the file, the commit is skipped and journaled (`sweep-ledger-commit-unavailable`,
  naming the directory and git's error) rather than ending the sweep. That degrade is
  for a tree git cannot interrogate only: a ledger commit git was asked to make and
  refused (a hook, the index, a full disk) still raises, as the publishers did before
  re-rooting — the cycle's bundles would otherwise run against the dirty baseline the
  commit was meant to clean. The store's commits keep degrading on both.

- Stop a sweep wiping every recorded pre-answer when the ledger vanishes mid-cycle
  (DW-176). An absent ledger read as "nothing is open" and dropped the whole store,
  committing the wipe; it now journals `sweep-preanswer-prune-refused` and writes
  nothing. An empty-but-present ledger still prunes.

- Withhold the decision phase's ledger commit when the LAST decision effect faulted
  (DW-166), so the ledger bytes that would not parse are never published; a later
  effect that reads and writes the ledger settles the doubt and the commit happens,
  carrying the earlier decisions' lines with it. The attended hand-back no longer
  prints `✓ decisions recorded` when any effect missed the ledger — it reports that
  the answers are saved, that not every decision reached the ledger, and which
  journal kind names the misses.

- Stop a re-dispatched sweep bundle from carrying the SUPERSEDED bundle's state
  (DW-162, DW-163, DW-165). `Sweep._run_bundle` already adopted a different bundle's
  `dw_ids` onto a task `_recover_inflight_bundle` had reset to PENDING, but every other
  per-bundle field stayed: `bundle_closes_intended` (which the DONE-leg ledger carry and
  the engine's replay predicate both read, so it closed ids this task never ran),
  `spec_file` + `restore_patch` (which made the dispatch prompt select the superseded
  amended contract, and `_record_dev_spec` — a no-op once set — refuse the replacement's
  own spec). Reset `attempt`, `review_cycle` and `followup_reviews_spent`, clear
  `defer_reason`, and advance `generation` to give replacement work fresh session ids
  and review budgets, as a human-resolved re-arm does. Apply these changes through
  `_reset_superseded_bundle_state` on the DIVERGENCE branch alone;
  an agreeing or merely reordered re-dispatch is the same bundle and keeps everything,
  and `resolved_redrive` stays latched because it records a HUMAN resolution, not spec
  ownership. Defensive: no reachable sequence was demonstrated for the `spec_file` /
  `restore_patch` half.

- Grade a persisted sweep bundle intent document against the task that owns it (DW-164).
  `_run_bundle` writes `task.bundle_file` and only then `_save()`s the adopted ids, so a
  crash between them left `_ensure_bundle_intent` reusing a still-existing document whose
  `dw_ids:` line named ids the task no longer carried. Re-ordering the two writes only
  inverts that pairing, so the check is total instead: a new `_bundle_intent_reason`
  compares the document's ids against `task.dw_ids` as a SET and regenerates on
  disagreement, on an unreadable file, on a document with no `dw_ids:` line at all, or
  when the file is gone — `sweep-intent-regenerated` now carries a `regen_cause` field
  saying which. That is a closed slug rather than a free-text `reason`, which
  `diagnostics._JOURNAL_DROP_FIELDS` would have rendered as a presence boolean, defeating
  the field's whole purpose. An EMPTY `task.dw_ids` (the pre-`dw_ids` `state.json` shape)
  is not an authority and keeps its real document.

- Serialize the project pre-answer store's three writers (DW-161). `record_pre_answer`,
  `prune_pre_answers` and `drop_pre_answer` each did an unlocked `load_pre_answers` ->
  `_write_store`, so a `waves decisions` answer, a TUI decision modal or a second sweep
  landing in that window was overwritten wholesale — the store read-modify-writes the WHOLE
  file, so a lost update is a human's answer gone, not a stale field. Each now runs its read
  and its write inside ONE `deferredwork.ledger_lock` hold keyed on the store path. The
  ledger's helper is reused rather than twinned, and the two files share only its
  path-agnostic NESTING guard — never an OS lock, since each sidecar is keyed on its own
  resolved path — whose consequence is that no caller may hold both at once, in either
  order. The two conditional writers keep a #736 advisory pre-lock probe, so a call a read
  proves will write nothing still acquires nothing and still leaves the store's bytes and
  mtime untouched. Readers stay lock-free; a real write can now surface a lock-acquisition
  failure where none was possible before.

- Commit the sweep's pre-answer prunes in the store's own tree (DW-160). Both prune sites
  resolve the store under `_project_of_run_dir(self.run_dir)` but committed through
  `_commit_ledger`, which checked and committed `self.workspace.root`: where `repo_root`
  names a tree DISJOINT from the project those diverge, the clean check passed against the
  untouched code repo, nothing was committed, and the project worktree was left dirty ahead
  of this cycle's bundles. (The nested/monorepo shape was unaffected — `repo_root` is an
  ancestor there, so the store edit was already visible.) `_commit_ledger` takes a
  keyword-only `root` and both prune sites pass the store's own; a `verify.GitError` from an
  explicitly-rooted call now degrades to a `sweep-ledger-commit-unavailable` journal row
  naming the tree and the error, so a project that is not a git repository keeps its store
  write instead of aborting the sweep.

- Gate the stories E2E's detached-writer fakes on a completed `setsid` transition. `$!`
  names the straggler the instant `fork` returns, but `setsid(2)` runs in that child
  afterwards, so publishing the identity straight off `$!` only assumed the escape the
  rows exist to prove — under a scheduler delay the reaper could be graded against a
  child still inside the pane's session, covering the weaker same-pgid case. Both
  detached fakes now bounded-poll the child's observed `/proc` session id, off the
  shared real-tmux hang ceiling, and fail loudly rather than publish an ungraded
  identity (DW-159). Three local-process rows drive that fragment directly — the
  detached, the late-detaching and the never-detaching child — and the stories module's
  xdist-group floor is re-pinned from 30 to its actual gated-def count, so it no longer
  carries fourteen deletions' worth of silent slack. Synchronize retry coverage, grade
  session identity independently of process groups, and kill unpublished children when
  readiness times out.

- Type-check the decision `question` and option `key` a triage plan carries instead of
  `str(...)`-ing them: both are printed by `waves decisions`, announced by the
  attention notifier and written to the `decision-pending`/`decision-answered` journal
  records, so a list `question` used to validate cleanly and reach an operator as the
  repr `['a', 'b']`. A non-string one is now refused through the existing `errors`
  channel, one error per fault, with no repair path. This refuses triage plans the
  previous release accepted: such a plan is re-driven, and a cached `triage*.json`
  written before this release that carries such a value stops contributing its
  decisions to `decisions --list`, `status` and the TUI until the next sweep re-triages
  the still-open ids (DW-156).

- Name a triage decision by its position when its `id` is not a string, in every
  diagnostic the decisions loop emits, so an object-valued `id` can no longer print its
  own contents into messages that promise type names only. Acceptance is unchanged: the
  same plans validate and are refused, and a string id — the empty string included —
  keeps today's wording byte for byte (DW-157).

- **Refuse a migration result whose top level is the wrong shape** (DW-170), the DW-155
  guard `validate_triage` got and its twin one function over did not. `rj = rj or {}`
  substituted only on a falsy document, so a truthy non-object result — a list, a
  string, a number — reached `.get` and raised `AttributeError` out of
  `validate_migration`. It is now refused through the existing `errors` channel, which
  for a list top level emits `migration result not a JSON object: list`, and an empty
  list is refused by shape rather than reported as a `workflow` error. This makes the
  function total over parseable JSON for its own callers rather than fixing a live
  crash: `_ensure_migration`, its only production caller, screens the same result
  through `critical_escalations` first, which raises on a truthy non-dict before this
  guard is reached.

- Extend DW-157's positional naming to the triage diagnostics it missed (DW-171): the
  `already_resolved`, `blocked` and `skip` loops, the open-set mismatch's `not open in
the ledger` list and the `workflow must be ...` refusal in BOTH validators used to
  interpolate LLM-authored objects verbatim into strings that reach the journal. A
  non-string identifier is now named by its position and type name (`already_resolved[0]
(id not a string: dict)`, `open_ids[0] (not a string: dict)`) and a non-scalar
  `workflow` prints as `a dict`. Acceptance is unchanged — the identifier fields are
  still deliberately not type-checked, so the same plans validate and the same plans are
  refused — and a string identifier, the empty string included, plus a scalar `workflow`
  (`got None`, `got 'wrong'`) keep today's wording byte for byte.

- Re-offer a decision hand-seeded as `effect: "close"` in `.waves/loop/decisions.json`
  (DW-147), instead of counting it answered while no sweep ever built, closed or re-asked
  it. Re-answer it with `waves decisions`; the file is journaled, never edited.

- Adopt the current bundle's deferred-work ids before writing a reset sweep task's
  intent (DW-144). Keep dispatch and ledger-close ids aligned, and journal both
  old and new ids as `sweep-bundle-dwids-adopted` when they differ.

- **Retire stale keep-open pre-answers when dropped** (DW-143), so decisions are
  offered again and fresh sweeps stop repeating stale-answer notifications. Journal
  the removal and preserve run-local answers and ledger history. A read-only project
  store raises `PermissionError` after the drop is announced and quarantined; a fresh
  run retries once the store is writable. The retirement removes the entry only while
  it still holds the value that was dropped: a paused run's stale run-local copy wins
  over the store on resume, so a replacement a human recorded out of band meanwhile
  is left in place for the next run instead of being deleted and committed away. The
  compare and the delete are one step under the store's lock (DW-161 below), so that
  compare-and-delete and a concurrent `waves decisions` re-answer cannot interleave.

- **Skip an unreadable cached triage instead of failing the read** (DW-145). Widen
  `decisions.pending_missed_decisions`' except tuple to include `UnicodeDecodeError` —
  a `ValueError`, not an `OSError`, so non-UTF-8 bytes in one run's `triage*.json`
  escaped past `cmd_decisions` and `cmd_status` (which catch `BmadConfigError` alone,
  leaving `main`'s backstop to exit 1 with no `--json` document) and out of the TUI
  uncaught. Degrades per file: the bad cache is skipped, the other runs still count.

- **Refuse a triage plan whose free-text scalars are not strings** (DW-148). Type-check
  bundle `name`/`intent`, option `effect`/`intent`/`label`/`resolution`/`bundle_name`
  and decision `context`/`recommendation` in `validate_triage` instead of `str(...)`-ing
  them — a list `intent` used to become a truthy Python repr that passed the
  `effect == "build"` intent gate and rode into `Bundle.intent`, `intent.md` and a dev
  session (the DW-141 harm, on the plan-input surface). Errors name the decision id or
  the bundle's position, the field and the type name only, one per fault. Identifiers
  and ledger-bound notes (`key`, `question`, `id`, `evidence`, `blocker`, `reason`,
  `dw_ids` members) deliberately keep `str(...)`. Note: a pre-existing cached triage
  that the stricter check now refuses is skipped by `pending_missed_decisions`, so its
  decision drops out of `decisions --list`, `status` and the TUI until the next sweep
  re-triages the still-open entry.

- **Refuse a triage plan whose CONTAINERS are the wrong shape** (DW-155, DW-158), instead
  of raising out of `validate_triage` and every caller of it. `rj = rj or {}` substituted
  only on a falsy document, so a non-object top level raised `AttributeError`; a `null`
  `open_ids`/`bundles`/`already_resolved`/`blocked`/`skip`/`decisions`/`options`/`dw_ids`
  raised `TypeError`; and a `null` member of any list section raised `AttributeError` —
  crashing the sweep run loop on a live triage session and taking `decisions --json`,
  `status` and the TUI down on one bad cached `triage*.json`. The validator is now total
  over parseable JSON: wrong shapes in these containers and object members are refused
  as `(None, errors)`, with a shape diagnostic naming the location and type. Independent
  partition errors can still be reported. Positions stay the document's, so a
  dropped member does not renumber its siblings, and a shape-failed section no longer
  double-reports its own `has no dw_ids` / `needs at least 2 options` value error.
  `pending_missed_decisions` degrades per file, as it does for an unreadable cache.

- **Close the last reuse-exposed test child identities** (DW-136, DW-137). Share the
  pidfd-authentication helpers, publish identities atomically, and sweep authenticated
  children abandoned during pre-bind failures. The OpenCode row is now Linux-only,
  and no executable `os.kill(` call remains in `tests/`.

- **A stored decision answer is now screened by SHAPE, not just by container type**
  (DW-140/141/142). Three gaps behind DW-134's container-level check: a project
  `.waves/loop/decisions.json` holding non-UTF-8 bytes raised `UnicodeDecodeError` out of
  `load_pre_answers` and aborted the whole sweep that read it; the build lane stringified
  `key`/`label`/`intent`/`bundle_name`, so a list `intent` shipped its truthy Python repr
  into `intent.md` and a dev session as prose no human wrote; and an answer with a missing
  or unrecognized `effect` matched no materialize lane while `decisions.pending_missed_decisions`
  counted it answered, so no reader ever surfaced the id again. `load_pre_answers` now
  catches the decode fault, and one shared predicate (`sweep.unusable_answer_reason`)
  screens both readers, so a value the sweep will not act on is one `waves decisions`
  re-offers rather than counting answered. It screens only what a reader of THAT effect
  consumes — `key`/`label` always, `intent`/`bundle_name` for `build` alone, `resolution`
  and `answered_at` never — because a refused `keep-open` answer stops suppressing its
  bundle, and `effect: "close"` stays usable (the in-run writer stores it). The lanes'
  own typed reads (`""` rather than a repr) are now defense-in-depth rather than the
  production path: the read site rejects such answers first, so the lanes matter only for
  callers that bypass it — the test suite hands `_materialize_bundles` a map directly.
  No new journal kinds and no new drop causes; the degrade stays per-value and in-memory,
  so the two write-backs still re-publish an unusable value verbatim rather than repairing
  the human's file.

- **The re-stamp row that settles an owed code-root record now records THAT a move
  happened** (DW-128) — not which trees: the row's `repo` is the new root and a dump
  reduces it to `repo_present`. `runs.restamp_code_root`'s trailing `rearm-code-root-restamped`
  append writes `code_root_changed` about THIS call, so the one path where the row is a
  real move's sole durable trace — call one re-points the root, persists, and its append
  raises; the retry discharges the record having moved nothing — recorded `false` and read
  as "nothing moved". That append now also carries `discharged_owed_move`, true exactly
  when the row settles a record owed by an earlier call's move. `code_root_changed` keeps
  its exact current value at every append site, and the two sibling discharge appends
  (which already assert `code_root_changed=true`) are untouched, so an absent key on those
  rows means "not stated", not `false`.

- **A regenerated sweep bundle no longer vanishes into a finished bundle's key** (DW-125).
  `_run_bundle`'s terminal-task early return compared only the derived `dw-<name>` key, and
  the key is a pure function of `(name, cycle)` — so a resume that lost `<run>/triage.json`
  re-triaged, re-authored the remaining ids under freely chosen names, and any bundle that
  happened to reuse a completed bundle's name was skipped with its deferred work never run.
  The skip now also requires the persisted task's `dw_ids` to agree with the bundle's, as set
  equality (a reordered plan is still the same bundle) and with an empty persisted list
  counting as agreement (the pre-`dw_ids` `state.json` shape, so no paused run needs
  migrating). On divergence the bundle takes the same bounded `-2` … `-9` name suffix the
  decision-bundle site already uses, journaled `sweep-bundle-key-deduped`; exhausting the
  bound journals `sweep-bundle-key-collision`, notifies, and leaves the ids open rather than
  swallowing them. In-flight tasks are untouched — they still go through the existing
  recovery — and the cycle's progress count now grades the key each bundle was resolved to
  (the one it ran under, or the terminal one it was skipped at) rather than one re-derived
  from the plan's name.

- **A sweep's decision dispositions now survive a pause/resume of the same run** (DW-124).
  The two quarantines — ids journaled `decision-skipped-unattended`, and ids whose recorded
  answer was journaled `sweep-decision-answer-dropped` — moved from `SweepEngine.__init__`
  set state onto `RunState` (`sweep_skipped_decisions` / `sweep_dropped_decisions`),
  persisted immediately after each disposition is announced. Once that state publication
  succeeds, a resumed run no longer re-journals a drop and re-fires its `gates.notify` for an
  id it already reported, nor revives a bundle when the resumed cycle's re-triage happens to
  mint an agreeing option. Deliberately
  run-scoped: a NEW run still re-evaluates every decision, the human's answer in
  `<run>/decisions.json` is untouched, and a pre-upgrade `state.json` loads both empty.

- **Degrade a malformed `<run>/decisions.json` instead of aborting the sweep** (DW-134).
  An unreadable file, a non-object top level or a non-object value journals
  `sweep-decisions-reload-failed` (one record per fault class; per-value records name their
  store and affected ids) and drops only the unusable answers; the well-shaped rest answer
  as before, and both `_materialize_bundles` lanes shape-guard the map they are handed. A
  per-value drop is re-published unchanged by the phase's own write-backs; a whole-file fault
  has nothing per-value to carry. `waves decisions` re-offers an id whose stored
  pre-answer value is unusable, instead of counting the bare key as answered. Also count
  every decision-answer drop as repeat progress (DW-135): `_cycle` previously counted only
  the keep-open lane, so a `--repeat` cycle whose sole event was a `no-intent` or
  `name-collision` drop stopped at `no-progress` even though the drop frees the id for a
  later cycle's fresh triage. All three lanes now signal, still bounded to one drop per id
  per run.

- **Make stories E2E reap identity reuse-proof and clean up a live child when either
  protected reap assertion fires** (DW-126, DW-127).

- **`runs.restamp_code_root` now warns only when THAT call moved the code root**
  (DW-114). A set `code_root_restamp_pending` with the mirror already equal to the
  incoming root made the function fall past the "already agrees" exit, discharge the
  owed record with a hardcoded `code_root_changed=True`, and return the "the code root
  in `_bmad/bmm/config.yaml` has changed" warning that `waves resolve` and the TUI's
  re-arm print — on a call that re-pointed nothing, and on the same seam where
  `cli._prepare_resume_locked` stays quiet. The marker is a record DEBT, not a move: the
  trailing record now reports whether THIS invocation re-pointed the root, and the call
  returns `None` when it did not, so the re-arm surfaces and plain `resume` now agree
  about whether an operator is warned in that state. They still differ on the journal:
  this record reads `code_root_changed=false` where resume's own discharge row keeps
  `true`, because resume's names the pre-overwrite root and this one names the call that
  moved nothing. The at-least-once discharge is unchanged — the record
  still lands exactly once under the root now recorded, the marker still clears only
  after the append returns, and the pre-overwrite discharge still names the previous
  root with `code_root_changed=True`. A genuine move still warns.

- **Stop stale `keep-open` answers from suppressing later deferred-work bundles**
  when triage options are renumbered or removed (DW-123).

- **A stored deferred-work decision answer is now validated against the triage
  option its key resolves to before the two are blended** (DW-118). `Decision.option`
  matches on key alone and a key is a position in a list every triage re-authors, so a
  renumbering re-triage attributed one question's answer to another question's option:
  on DW-55 a stored `build` answer keyed "1" met a fresh option "1" spelled "Close as
  decayed", and the bundle shipped the stale review intent under the close label while
  quoting a question the human never answered. The answer's own `label` and `effect` —
  the two fields both provenances carry — are now compared first, and a disagreeing
  option is discarded outright: it contributes no intent, label or bundle name, the
  mismatch is journaled (`sweep-decision-option-mismatch`), and the decision note cites
  the earlier triage rather than the current question. Precedence is flipped with it, so
  even an agreeing option fills only the fields the stored answer omits and re-authored
  triage prose can no longer reach a bundle the human chose against different prose.
  Covers the in-run lane too — `--repeat` re-triages each cycle while answers persist for
  the whole run — where a discarded option can leave nothing to build from: that answer
  is journaled (`sweep-decision-answer-dropped`) and notified instead of vanishing, and
  its ledger entry stays open for the next sweep to re-ask. A dropped decision is
  quarantined for the rest of the sweep process, so a later cycle whose re-triage agrees
  with it again neither revives it nor re-notifies it; the quarantine is instance state
  and is never persisted, so a resumed run re-evaluates the decision. The
  `decision-<id>` fallback name is also made unique now: it is a fallback, not a
  reserved namespace, so a plan bundle may legally carry it and the two would have
  hashed to one task key and one intent directory, silently losing the human's bundle. A
  taken name gains a bounded numeric suffix (`-2` … `-9`, first free wins, journaled
  `sweep-bundle-name-deduped`); exhausting the bound is the one point in name assignment
  at which a buildable answer yields no bundle, journaled with
  `drop_cause: name-collision` and notified.

- Inventory keyword and splat journal kinds only over an empty positional slot,
  preserving literalness and field findings (DW-109); give unresolved-kind failures
  call-site advice and prohibit sentinel declarations (DW-113); remove stale guard
  counts (DW-110, DW-112) and pin every kind covered by the by-name `patch` drop
  (DW-78).

- Name the property instead of counting siblings in the portability guard's last three
  journal-kind comments (DW-120): a kind-only write is one passing no keyword arguments
  at all, not even a `**` splat, and the other class is a literal reaching a declared
  dynamic-kind position from outside its body — a caller's `kind=` keyword or the
  position's own parameter default. A fifth of either no longer falsifies the prose.

- Retire two unpinned prose claims in the portability guard (DW-130, DW-131): the
  dynamic-kind literalness docstring no longer counts the writes it governs, keeping only
  the ablation-pinned position count, and the kind-literal probe's ablation now maps each
  feeding emit to the rows it reddens instead of crediting one emit with all of them.

- Pin each declared dynamic-kind position's journal-write count in the portability
  guard (DW-138). `JOURNAL_DYNAMIC_KIND_ALLOW` is now a mapping from position to its
  expected number of `journalkind` findings, held against the tree by a new row, so a
  write added or removed inside an already-declared position reddens instead of only
  falsifying a comment — the waiver is granted per position, so the declaredness gate
  passes on such a write by construction. Waiver semantics are unchanged.

- Probe both existence arms of the accepted-spec worktree seed through the total
  `_is_file` (DW-103), matching its structural siblings and the DW-101 supersession
  warning. On Python <=3.13 a raw `Path.is_file` raises on an unreadable path, and
  this call site sits outside every `except` in `run_isolated`, so the fault ended
  the run instead of allowing dispatch to continue. No change on non-faulting paths.

- Name the two silent refusals on the accepted-spec delivery path (DW-104, DW-115).
  The worktree seed's containment refusal now nominates its rel anyway, so
  `worktree-seed-dropped` reports it — the copier re-checks destination containment
  itself, so still nothing is written outside the mount — and both that refusal and a
  source the locator could not resolve at all (a swallowed filesystem fault, or a
  spelling that no longer resolves) are journalled as
  `accepted-spec-delivery-unreachable` on the non-relocated leg. Previously the rel reached no journal and, for a
  project-relative spec, no gate either: the unit dispatched against a mount lacking
  the operator's spec and fell back to the bare story key. Nothing new escalates.

- Probe the accepted spec for file-ness inside `relativize_project_local_accepted_spec`'s
  own `except` (DW-116). `run_isolated` calls the method before its first `try`, so a
  TOCTOU or non-EACCES `OSError` at that probe ended the run; it now leaves the
  spelling unchanged, as a false probe already did.

- Discharge an owed code-root re-stamp record under its original root before
  resuming (DW-100), preserving the record and integrity pin for retry on failure.
  Warn only when the configured root differs from the recorded root; a pending
  record alone no longer triggers the code-root warning.

- **Stopped the real-tmux E2Es contending with each other under `-n logical`**
  (DW-95). They shared the box with every other worker and could starve past their
  fixed waits — a load flake, not a defect. All 23 collected cases now carry one
  `xdist_group`, so loadgroup scheduling serializes them while the rest of the suite
  still fans out; `--dist loadgroup` is declared in `pyproject.toml` `addopts`, without
  which the marks are silently inert. Separately, the four completion- and crash-path
  waits in `tests/test_generic_tmux.py` now share one named 90s hang ceiling — a hang
  detector, not a performance budget — replacing per-site 30s and 20s walls; the
  `tests/test_stories_e2e.py` subprocess `timeout=` budgets stay their own and rely on
  the grouping alone. Guards in `tests/test_conftest.py` check repository scheduling
  declarations and the synthetic scheduling mechanism, and prevent short completion
  walls from returning while preserving the deliberate 6s triggers. Tests only; no
  production change.

- **Put the last two load-sensitive real-tmux walls on the shared hang ceiling**
  (DW-108). The descendant-reap polls in `tests/test_stories_e2e.py` deadlined on a
  fixed `time.monotonic() + 10`, which a starved scheduler can blow through — the class
  DW-95 removed from the generic-tmux waits but left in the one module its guard
  excludes. Both now spell the imported `REAL_MUX_HANG_CEILING_S`; the trade-off is
  deliberate, a merely slow reaper is caught at 90s rather than at 10s while a broken
  one still fails. A second scanner in `tests/test_conftest.py` keeps them there,
  rejecting any `time.monotonic() + <budget>` in a tmux-gated test in that file that is
  not the imported constant, with a named expected-site inventory so it cannot pass by
  scanning nothing and must-flag / must-stay-silent probe rows through the same function.
  The subprocess `timeout=` budgets in that file stay out of scope. Tests only; no
  production change.

- **Bound launch-marker snapshot retention in the dev adapters** (DW-96). Each dev
  session start stored a park-marker snapshot under its task id and nothing removed it;
  an unpinned launch (no `expected_spec`) snapshots every `*.md` in the artifacts dir,
  so an adapter driving N such sessions over M files retained O(N x M) entries for its
  lifetime. The mixin's `run()` now evicts the task's entry in a `finally`, holding only
  launches still in flight. Eviction is scoped to the returning task id, so a concurrent
  launch is untouched, and lands after `_post_kill_reconcile`, the last in-lifecycle
  reader. No verdict changes.

- **Bound four more per-task dev-adapter stores to the session** (DW-106, DW-107).
  `_fm_fallback_obs`, `_fm_transition_obs`, `_contract_nudge_sent` and the OpenCode
  transport's `_server_procs` (a live `Popen` per task) grew one entry per session for
  the adapter's lifetime. All four are now evicted through one `_evict_task_state` seam
  called from `run()`'s `finally` — past every in-lifecycle reader, including
  `_post_kill_reconcile`, and still reached when `wait_for_completion` raises. Scoped to
  the returning task id, so a concurrent session keeps its entries; within-session
  semantics (the exactly-once contract nudge included) are unchanged.
  `OpencodeHttpAdapter._usage` is a separate case: it is keyed by session id and read
  after `run()` returns, so it cannot use this seam — it is capacity-bounded instead
  (DW-117).

- **Bound the OpenCode HTTP adapter's session usage stash** (DW-117).
  `OpencodeHttpAdapter._usage` was written once per session in `_capture_usage` and
  never popped, so it grew O(sessions) for the adapter's lifetime. It cannot join the
  `_evict_task_state` seam — it is keyed by session id, not task id, and the engine
  calls `read_usage(result)` after `run()` returns, so evicting there would zero token
  accounting. The write site now enforces a fixed `USAGE_STASH_CAP` (256), dropping the
  oldest entries first and only when the key is new, so a re-stash of a live session
  never evicts a peer. The cap sits orders of magnitude above any plausible in-flight
  session count, and `read_usage`'s contract — signature, idempotence, `None` for a
  missing or absent session id — is unchanged.

- Prevent harvest races from filing cross-spec duplicates for one fingerprint (DW-98).

- **A partial journal flush no longer swallows the writer's next record** (DW-97). A
  partially flushed `Journal.append` left an unterminated fragment, the next append
  concatenated its own record onto it, and both readers dropped the combined line — so
  one fault lost a record that was written whole (a swallowed `unit-merged` re-drives
  already-merged work). `append` now terminates a fragment on its own line first. That
  bounds the loss to the torn record for the writer's own next append only; another
  process tearing a write concurrently can still produce the old pairing, and append
  durability is unchanged (no fsync, no lock). Both readers (`Journal.entries`,
  `tui.data.JournalTail.read_new`) now substitute a reader-minted
  `journal-line-unreadable` marker — kind plus byte count, no timestamp, no line
  content — for a complete line that will not parse, so the loss is counted in
  `diagnose --json`'s `kind_histogram` and rendered red in the TUI. That count is a
  floor on lost records, not an exact one: a single unparseable line can be two
  concatenated records. An unterminated final line is still withheld by the TUI tail
  until the heal terminates it; `Journal.entries`, which reads the file whole, marks a
  trailing fragment straight away.
- Preserve complete CRITICAL escalation detail in run records while visibly bounding human displays and naming the spec or journal that holds the recovery trail.

- **The TUI's re-arm declines a contended run instead of waiting for it.** The
  gesture runs on Textual's message loop, so taking the run's state lock blocking
  froze the whole dashboard for as long as a rival held it — unbounded on POSIX,
  where `fcntl.flock` never times out, and a rival `resume` holds it across a git
  preflight bounded only by `[limits] git_timeout_s`. It now acquires without
  waiting and toasts the contention; the post-lock liveness re-check refused that
  re-arm anyway.

- **An orphaned mount's reclaim no longer destroys the orchestrator's own artifacts.** The
  pre-reclaim snapshot drew its untracked candidates from `untracked_files`, which excludes
  ignored paths by contract, and the deferred-work ledger, sprint board and bound spec are
  ignored inside every mount by construction. Over a clean tracked tree it therefore parked
  nothing, so the force-remove took them with no ref, no callback and no journal line. Those
  three are now force-included when the mount holds them as regular files, judged one by
  one; no other ignored path is parked.
- **A harvest's ledger anchor no longer adopts a rival entry that beat it to the lock.**
  Both `deferredwork` mutators publish the whole post-edit file, so an entry appended
  between the pre-harvest snapshot and their locked read was claimed by
  `post_engine_ledger_digest`, and a later rejected attempt restored over it —
  unrecoverably, on a gitignored ledger. The mark and append legs now re-anchor only when
  the preimage they wrote over is still the bytes the run last claimed; the restore skips
  and journals `ledger-restore-skipped-diverged`.
- **Re-arm hold remedies name the status the re-drive routes on.** All four holding
  remedies — correct the spec in the main checkout, commit it on the pinned branch,
  restore it at the recorded path, commit the upstream `SPEC.md` / `stories.yaml` — now
  name the `status:` the corrected file must carry, so a correction that lands
  byte-correct but still terminal no longer burns the escalation the hold just bought.
  The restore remedy also stops claiming the re-drive "will see the escalated attempt's
  status": that arm fires only when the path holds no readable file, so the re-drive
  finds no spec there at all.

- **The TUI's re-arm hold now names the remedy of the record that actually held.** Its
  hold branch printed one hardcoded "commit the corrected spec" for all four holding
  records, and two of them cannot be obeyed that way: `rearm-spec-write-unreachable`'s
  in-place arm needs the edit made in the MAIN checkout, and `rearm-spec-flip-skipped`'s
  holding arm fires only where the recorded spec path is not a readable file — nothing to
  commit, and possibly a shared artifact directory outside any repository.
  `runs.RearmOutcome` gains `hold_next_step`, captured first-wins from the earliest
  holding record so the operator is told the cause they must clear first, and the toast
  composes it as "not resuming in this gesture. `<step>` — the run stays paused and
  resumable from this screen." The advisory toasts still drop `next_step`; only the hold
  line carries it.

- **A failed `rearm-code-root-restamped` append no longer loses the move record for
  good.** `restamp_code_root` committed the new root and journalled afterwards, so an
  append that failed once left a retry exiting at "already agrees" with the record never
  written and the later `run-resume` line reporting `code_root_changed=False`. The move
  now lands with an intent marker (`RunState.code_root_restamp_pending`) in one atomic
  state write, the record follows it, and the marker is cleared only once the record is
  down — so a retry writes the record the move still owes, and a record can never claim
  a move the state write did not make. A plain `resume` consumes the outstanding record
  too: it counts the marker as a move, so its `run-resume` line and the code-root warning
  fire even though the re-stamped mirror already agrees with config, and clears the
  marker on the same write that persists the resume.

- **An owed code-root re-stamp record survives a second move of the root.** The pending
  marker is a bare flag, so the root a failed record was owed for is described only by
  the run's own `repo_root`. An operator who re-pointed the root again — restoring the
  original or moving to a third tree — before retrying had that value overwritten, and
  the earlier move's record could never be written. The retry now discharges the owed
  record under the root the marker still names before taking the new one, so every move
  keeps its own journal row.

- **The journal-kind inventory no longer misses a kind passed POSITIONALLY to a declared
  dynamic-kind position.** The scan read `node.keywords` only, so
  `_close_bundle_ledger_when_spec_status(task, spec, status, "new-kind")` — legal Python,
  since `kind` is positional-or-keyword — reached the journal with no `JOURNAL_KINDS` row
  anyone had to decide on, while the guard reported itself complete. All three ways a literal
  reaches such a position (keyword, positional, parameter default) now feed the same emit,
  with the slot resolved from the declared function's own signature and the bound receiver
  dropped. A `*args` splat covering the slot yields a kind no row can declare, so an
  unreadable position reddens the inventory naming its site instead of passing in silence; a
  declared forwarder is exempt, its kind already read by the journal-write emit.

- Take the re-arm's mount claim and its resume hold from the `rearm-spec-flip-skipped`
  record instead of inferring both from `reaches_redrive`. The record now carries the live
  `redrive` mode, so the notice no longer tells an ISOLATED run that it "mounts no worktree" —
  that arm reaches the re-drive through a spec shared across checkouts, with a worktree very
  much mounted. A record written before the field drops the mode clause rather than guessing.
  The same leg now HOLDS the resume (`reaches_redrive` and not `refused`), so its "check the
  recorded spec path before resuming" imperative stops rendering on the two surfaces that
  re-arm and resume in one gesture.
- **`waves clean` no longer aborts the whole sweep when one run's state lock is
  held.** A busy run used to end the invocation, so later candidates went unprocessed and
  runs already reclaimed vanished from a report only emitted after the loop. `clean` now
  takes each run's lock without waiting and records the contended run like the lifecycle
  races beside it — `trimmed` if anything reached it, else `protected` — then continues.

- **`waves stop` no longer retries forever on an engine whose identity cannot be
  read.** The rival-engine compare under the state lock used the local pid after every
  declining path had cleared it, so an unchanged pid file with `"unknown"` liveness read
  as a freshly published rival on every attempt. The compare now uses the pid file as
  recorded; a rival is a changed file, nothing else.

- **The OpenCode adapter validates every task artifact it will write.** It refused a
  redirected `messages.json` but not a symlinked, hardlinked or special `heartbeat.json`,
  `resultless-stops.jsonl` or `session-lifecycle.jsonl`, which the inherited result-file
  mixin writes; the three names now live in one `RESULT_FILE_ARTIFACTS` tuple both adapters
  validate.
- Serialize run deletion/archive against resume (DW-94), refusing a newly live
  engine under the per-run lock and preventing a waiting resume from recreating a
  run cleanup already removed.

- Serialize every run-state writer and control read-modify-write transaction with one canonical per-run advisory lock (DW-93).

- Let interactive resolve present `paused_reason` when watermark filtering leaves no newer
  recorded escalation detail, without recovering or inventing an escalation (DW-91).

- Reject malformed session escalation/result artifacts and non-finite resolve JSON
  (DW-86, DW-89).

- **Confine built-in adapter task directories** (DW-74), refusing unsafe task ids and
  symlink- or junction-redirected task directories before prompt, artifact, log, or
  transport side effects.

- **Treat embedded-NUL verify commands and working directories as typed environment
  faults** (DW-53, DW-54), while documenting that stream retention degrades but
  journal record writes remain fail-loud.

- Make successful escalation re-arms return authoritative ordered notices and a resume-hold
  verdict, so a corrupt journal cannot hide a persisted hold from the CLI or TUI gesture.
- **An accepted spec reached through a link out of the unit worktree no longer counts as
  delivered.** The pre-dispatch check asked only whether a file existed at the mounted path,
  and that probe follows symlinks, so a spec directory the checkout carries as a link
  pointing outside the mount let an unrelated external file stand in for the accepted spec
  and the session ran against the wrong bytes. The check now also requires the resolved path
  to stay inside the worktree; a link whose target is inside it still passes, and a probe
  that cannot be resolved escalates rather than binding.
- **`branch_checkout_path` keeps a registered worktree path's trailing whitespace.** The
  reader went through `_git_out`, which returns `stdout.strip()`, so a foreign checkout
  registered at a unit's own mount path plus a trailing space came back as the bare mount
  path, compared equal to it, and was exempted by the remount's occupancy guard — the ref
  then moved under a live foreign checkout, its tree went spuriously dirty, and `worktree
add` failed on the held branch anyway, which is the harm the guard exists to prevent. A
  new `_git_raw_out` hands back stdout verbatim alongside the merged diagnostic, and only
  the single framing newline is removed; `_git_out` and its other callers are unchanged.
  POSIX-only, and a spurious refusal is unreachable because `safe_segment` rstrips `". "`
  from every segment we compose. A path ending in `\r` stays indistinguishable under
  `text=True` universal newlines — an accepted bound, documented at the reader.
- **An aborted re-arm's spec rollback confines against the live project root, not the
  recorded one.** `_restore_rearmed_spec` picked between the confined and plain writers on
  a lexical `is_relative_to` against `task_spec_root` — the launch-time spelling nothing
  re-stamps — while the flip, the strip and the baseline re-stamp it undoes all confine
  against `live_spec_root`. After a project rename the live spec path was not under the
  recorded root, so the undo silently dropped to the unconfined arm and lost #593's
  O_NOFOLLOW walk of the parent components (`follow_symlinks=False` guards only the final
  one) on exactly the specs its siblings had just written through the confined one. The
  live project root is now threaded through `_rollback_rearm` as a required parameter.
- **The review-budget rescue and the timeout salvage route on the tree in hand, not on
  live policy.** Both selected on `scm.isolation` alone, so an accepted continuation that
  reopened a recorded mount after a `"worktree" -> "none"` flip took the in-place arm: the
  commit landed in the mount and `_integrate_unit` merged it out, turning a story that never
  converged (or a timed-out review) into DONE-and-merged where the same work under unchanged
  policy defers with the unit's worktree and patch preserved. Salvage additionally performed
  `in-review` repair writes the mounted path never performs. Both now use the
  `self._isolated or task.worktree_path` pair `_defer` and `_run_story` already share.
- **The escalation modal's story manifest follows a moved project onto the mount.**
  `runs.live_stories_root` probed the mount at its RECORDED spelling before rebasing, so
  after a project rename the probe failed, the mount was discarded, and the modal read
  title, description and sentinel from the main checkout's stale twin while `blocking` and
  the re-arm targeted the moved worktree. It now probes the rebased mount first, and
  `resolve._context_stories_root` delegates to it so `context.json` and the TUI cannot
  disagree about which tree the run owns.

- **A remount parks an orphaned worktree's uncommitted work before reclaiming its path.**
  `open_unit_workspace` force-removed whatever stood at the deterministic mount path, so the
  directory an isolation flip had "retained for recovery" lost its tracked edits and
  run-created files irreversibly (even under `keep_failed = true`) — only commits unique to a
  story-branch tip were preserved. A registered orphan's dirty state is now snapshotted under
  `refs/attempt-preserve-dirty/<run>-<head>-orphan` (the family `scm.preserve_keep` already
  bounds) and journaled as `isolation-flip-orphan-preserved`; a clean orphan parks nothing, a
  plain directory is never read as a worktree (git run there would address the project
  checkout), and a failed capture refuses the remount and leaves the orphan standing.

- **A `branch_per = "run"` remount catches the run branch up to the pinned base.** An
  existing run branch reattached at its own tip and ignored `pinned_base`, so when the target
  advanced while the run branch was unmounted (a story landed in place, then isolation flipped
  back) the next unit developed without that story — `merge_strategy = "ff"` then refused the
  integration and the other strategies merged stale work. The run branch is now
  compare-and-swap fast-forwarded before the mount when its tip is an ancestor of the base,
  and a diverged base (the normal serial shape under `squash`) is merged into the fresh mount;
  a conflicting catch-up aborts, drops the mount, leaves the run tip unchanged, and raises for
  an operator to reconcile. The attempt baseline is read after the catch-up. Both ref moves —
  this fast-forward and the story-branch reset — are refused up front (`GitError` naming the
  branch and the path) when the branch is checked out anywhere other than the unit's own mount
  path, e.g. a `git worktree move`d recovery mount: the compare-and-swap would move the ref
  under that live checkout, leaving its files and index at the old tip.

- **The TUI escalation modal reads the spec, story context and sentinel the re-arm will
  write.** `_paused_spec` / `_paused_spec_root` anchored on the recorded `state.project`
  while `_do_rearm` flips the copy under the live project, so a run opened from a moved
  project showed the old tree's spec — unreadable once that tree was gone, refusing the
  re-arm — or let the operator review one copy and re-arm another; `_story_context` and
  `_sentinel_kind` located the stories folder the same way, so the modal omitted the title,
  description and sentinel indicator (or showed stale ones) beside the live spec. All four
  now use the same live mapping as the re-arm (`runs.live_spec_path` / `live_spec_root`,
  promoted from private, and the new `runs.live_stories_root`).

- **`worktree list -z` is gated on git 2.36; the 2.34 support floor keeps the newline
  parse.** The NUL-delimited listing was issued unconditionally, and Ubuntu 22.04's stock
  2.34.1 rejects the switch (exit 129), so every isolated-task resume escalated instead of
  reopening its recorded mount and orphan reconciliation skipped its cleanup. Below 2.36 —
  or when git will not say what it is — the pre-existing newline parse is used.

- **A looped `*.md` symlink under an artifact dir no longer aborts every unpinned dev
  session on Python 3.11.** `_marker_path_key`'s `resolve()` guard caught only `OSError`,
  but a symlink loop raises `RuntimeError` on the support floor (3.13 resolves it
  silently), so the launch-time marker capture died before the transport started. The
  guard now catches `(OSError, RuntimeError)` like every other `resolve()` in the package,
  and the loop entry reads as one unreadable marker.

- **The defer notice under a recorded mount names the kept branch instead of an
  in-place merge.** `_defer_recovery_note` selected on live `scm.isolation` alone, so a
  run flipped `"worktree" -> "none"` while paused advertised
  `git -C <mount> merge --ff-only <ref>` against the worktree `_integrate_unit` was about
  to delete, and hid the kept branch when `keep_failed` was on. It now selects on the same
  live-isolation-or-recorded-mount pair as the defer arm itself.

- **`docs/FEATURES.md` no longer promises a ledger entry the review-budget damping does not
  file.** The bounded-review-loop bullet said a lingering follow-up recommendation is re-filed
  to the deferred-work ledger; `_journal_review_budget_spent` journals the spent budget and
  deliberately files nothing, on the damping path and on plain budget exhaustion alike (the
  DW-55/64/90 class showed such rows re-litigate a converged story's review). FEATURES.md is a
  behavior contract, so the bullet now matches the shipped behavior and names the review
  _timeout_ salvage as the one path that does still file.

- **A `seen-again:` match that goes stale inside the ledger lock no longer swallows the
  recurrence.** `_harvest_spec_deferrals` decides the cross-spec dedupe against a ledger
  snapshot and excludes the matched finding from its append, then stamps the sighting later
  under `deferredwork.mark_seen_again_many`'s lock. A rival that closed or archived the entry
  in that window got the line stamped onto a done entry while no open entry was filed — the
  finding was then recorded neither as a sighting nor as an entry. The primitive now rechecks
  `entry.open` inside the hold and returns the ids whose match went stale; the harvest files
  those findings after all, persists their records ahead of the append so the isolation carry
  can re-file them, keeps `seen_again` naming only entries that actually took a sighting, and
  journals `spec-deferral-sighting-stale`.

- **Document spec baseline frontmatter as an optional `verify_dev` attestation**
  (DW-51), with no-claim acceptance and no-work refusal regressions anchored to
  the orchestrator-recorded baseline.

- **Restore the original spec when a TUI replan cannot strip its stale result**
  (DW-33), keeping the status reset and result removal atomic before resume.

- **Document the three story-spec path resolvers and their distinct ownership
  contracts** (DW-17, DW-18, DW-36). Persisted-task anchoring, session-reported
  candidate probing, and exact attempt recovery binding now cross-reference one
  another and spell out their different bare-basename results; production prose
  also names the real implementation-artifacts-relative layout.
- **An artifact the escalation walk cannot stat is recorded as unreadable rather than absent**
  (DW-11). `resolve._gather_escalations` classified each task-cycle artifact with
  `Path.is_file()` outside its guard, and that probe's answer to EACCES splits by interpreter.
  Through 3.13 it re-raises anything outside `pathlib._IGNORED_ERRNOS`, so an artifact under an
  unreadable directory escaped `build_context` and `cmd_resolve` to the top-level backstop as
  `error: [Errno 13] ...` — a read fault ending the interactive command this reader's contract
  says it must survive. On 3.14, where the body became `os.path.isfile`, the same fault was
  swallowed as absence instead: the skip sink stayed empty, so the caller recorded coverage and
  `escalations_resolved_upto` withheld every CRITICAL entry under that directory permanently.
  Classification is now `stat`, which answers with an errno — ENOENT and ENOTDIR are genuine
  absence and still cost nothing, while EACCES, EIO, ESTALE and EBADF join the shown-side skip
  sink. ELOOP moves with them — the one reading that changes on every interpreter rather than
  one, since a symlink cycle answered False through 3.13 (ELOOP is in the ignored tuple) and on
  3.14 (`os.path.isfile` swallows it): a degrade withholds coverage rather than being laundered
  into a durable claim. The regular-file check stays, because `stat` succeeds where `is_file()`
  answered False — without it a directory at an artifact path would raise `IsADirectoryError`,
  and a FIFO would block the read forever, wedging the interactive command.
- **An aborted re-arm no longer leaves the spec re-armed against an escalated task**
  (DW-79, DW-83, DW-85). `runs.rearm_escalation` published the status flip and stripped the
  stale `## Auto Run Result` about 250 lines before `save_state`, and only two of the aborts
  in that window undid those writes — a failing `journal.append` from the stale-restore
  residue pass, a non-git fault from the commits probe, or a failing `save_state` each escaped
  with the spec flipped on disk while persisted state still said ESCALATED. The window is now
  one transaction with `save_state` as its single commit point: any fault — an interrupt
  included, which is why the guard catches `BaseException` — restores the spec's BYTES to what
  the re-arm found and re-raises the original fault unchanged. Clearing a stories sentinel is
  deliberately outside that scope: it unlinks a file rather than writing spec bytes, and
  `_clear_sentinel` already preserves a copy and is idempotent on retry. The rollback journals
  `rearm-aborted` carrying `restored`, `unchanged` (proved byte-identical), `failed` or
  `unknown`, which `resolve` and the TUI render through the one shared routing table — so the
  residue notices they echo from a `finally` can no longer describe files as excluded from a
  baseline that was never saved, and an outcome the undo could not confirm (the cleared
  sentinel among them) reports the abort without claiming the file is intact. A rollback that
  cannot write still raises, naming the possibly part-written spec to restore from git _or_
  your own copy — an untracked or out-of-checkout spec has no committed version to recover —
  with the original fault kept in the exception chain. The undo picks its writer the same
  lexical way the three spec writers it undoes do, so a spec in an artifacts folder configured
  outside the checkout is restored rather than refused; it declines to write at all when the
  spec's bytes could not be CAPTURED from a file that is there and that the re-drive will
  actually read, since a transient read fault followed by successful writes would leave a
  published flip with nothing to put back; and it leaves a re-arm whose `save_state`
  demonstrably committed alone, because that rename can be interrupted on the way out and
  undoing the spec beneath it mirrors the same defect. An ORDINARY failure of the abort
  record's OWN journal write is suppressed whatever its type, so an observation that cannot
  be made never replaces the fault the operator is being told about — an interrupt still
  leaves, since by then the rollback has already run and the operator asked to stop. That
  `finally` is also what makes the residue echo unconditional: the residue is journalled before
  the re-stamp that can raise, so an abort would otherwise drop the notices for records already
  on disk — the commits warning among them.

- Stop an LLM-authored preference escalation from aborting the review leg. `_review_and_commit`
  splats a review session's own `result.json` escalation entries into `journal.append`, so a
  result.json carrying a `kind` or `story_key` key raised `TypeError: got multiple values for
argument` and failed the story; a `ts` key did not raise and instead silently replaced the
  entry's real timestamp, skewing every relative offset a diagnostic dump derives from it. Those
  three journal-owned names are now dropped before the splat.

- Close three journal-field leaks into `diagnose`, all found by the new field-routing guard and
  each reproduced through `diagnostics._scrub_entry`. On `preference-escalation`, whose keys are
  LLM-authored (`engine._review_and_commit` splats a session's own `result.json` entries into
  the journal), every key outside the record's declared `{type, severity, detail}` schema now
  renders as `<name>_present`; the key NAME still ships, a bound stated on the routing entry and
  accepted rather than collapsed. `decision-pending`'s `question` joins the free-text drop set —
  a multi-word question collapsed only by accident of the fallback forbidding spaces, while a
  one-token one shipped verbatim; no operator surface loses it, since the TUI reads the raw
  journal. And `story_keys` is aliased element-wise on `sweep-inflight-stranded`, which carried
  raw bundle story keys because the value fell through to `scrub_json` — the identity on a list
  of identifier-shaped strings — while the singular `story_key` beside it was already aliased;
  a non-list value on any key-list field now fails closed instead of taking that same path.
- Carry an isolated unit's harvested ledger findings when a defer runs under a
  recorded mount after `[scm] isolation` was edited to `none` mid-pause. Resume reopens
  the mount regardless of live policy, but the defer routed on live policy alone: it
  reset the main repo, skipped the carry, and the findings died with the deleted
  worktree. `_defer` now routes on the tree in hand, matching `_run_story`.
- Stop a second resolve cycle re-presenting escalations the human already answered
  (DW-11). Only a re-arm that accepted a `resolution.json` watermarks the session
  trail; later cycles show what came after it and print how many were withheld. A
  cycle whose walk could not read a session artifact records no coverage at all, so
  a transient read fault no longer buries the escalations it hid.
- Emit `diagnose --json` v2, replacing journal `patch` / `stashed_to` paths with
  `patch_present` / `stashed_to_present`, and silently degrade Git stale-commit probe
  failures while propagating non-Git faults.
- De-duplicate interactive-resolution escalations across repeated task IDs and mirrored
  artifacts, and skip malformed artifacts without aborting resolution.
- Prevent escalated sweep restarts from reusing abandoned session ids, and clear stale
  `escalation.json` artifacts when either adapter reuses a task directory.
- Route interactive resolve task ids through the shared whole-composition sanitizer while
  preserving generation-zero ids for clean story keys.
- A verify command whose child cannot be started pauses the run instead of crashing it. Any
  spawn-time `OSError` — most often a working directory that is missing, is a regular file, or
  cannot be searched, but a missing shell or EMFILE too — raised out of `subprocess.run` past
  every guard and ended the run with `crash.txt` + `state.crashed`. It is now translated into
  one `CommandResult` per command carrying a `spawn_error` (and a synthetic return code outside
  the range a signal-killed child reports, distinct from the timeout leg's `-1`), classified as
  an environment fault, and escalated — budget untouched, re-armable.
  `waves confirm --reverify` reports it as a refusal too. A command that merely times out
  is unchanged: still an ordinary fixable retry.
- Require the current session's genuine `awaiting-operator` Auto Run Result marker before a
  park skips proof-of-work, so previous-run, out-of-band, and re-armed specs cannot inherit
  waiver authority through retained frontmatter or operator actions; unasserted parks with
  real changes still pass (#335, #676). Journal each waived artifact-gate pass as
  `park-proof-of-work-skipped`, with `zero_diff` reporting no non-excluded residue (`true`),
  residue (`false`), or an unanswerable probe (`null`). The record does not mean the park
  committed; use the later `story-awaiting-operator` event for that. Missing, repaired, legacy,
  and malformed assertions fail closed to the ordinary proof gate.
- Anchor the TUI's paused-spec read and its `Request replan` write on the tree the run
  owns. Under isolation both resolved against the main checkout, so the review modals
  showed that copy of the spec and the replan reset it — reporting success while the run's
  real spec kept its terminal status, so the next dispatch did not re-plan.
- Anchor a spec's confinement root on a tree that can actually contain it, so the status
  flip, the result strip and the baseline re-stamp no longer fall back to an unguarded
  write, and the re-arm's undo no longer fails outright.
- Re-anchor spec ownership and the attempt baseline before a discarded worktree is dropped,
  in both the engine and sweep. A later resume could otherwise probe the main checkout —
  deleting untracked files the operator already had, or restoring a dead attempt's spec
  over their own copy.
- Release spec ownership when a half-built worktree is discarded for a restart, so the
  replacement mount can bind the spec. The attempt's binding is cleared and the accepted
  spec returns to its mount-relative spelling; left absolute into the deleted tree it
  resolved to nothing, and the restarted attempt ran unbound with the repair prompt naming
  a path that no longer existed.
- Release a mount's state when a resumed run stops treating it as isolated. Flipping
  `[scm] isolation` to `none` left the re-anchored spec absolute inside a mount the resume
  neither reopens nor discards, so the in-place attempt ran unbound; worse, it carried the
  unit's `baseline_commit`/`baseline_untracked` into an in-place rollback of the main
  checkout, where a unit's empty untracked snapshot marks every untracked file in the
  operator's own tree as attempt debris — deleted outright under an auto-recovering cause.
  The task also stops CLAIMING the mount: `worktree_path` doubles as the record of which
  tree owns a task's persisted state, so keeping it set made the spec and stories-root
  helpers answer for the unit while execution used the project checkout. Every
  non-isolated leg releases, not only the restart: the spec-approval, recorded-result and
  commit-finalizer continuations each finish their work and return without ever reaching
  it, so they went on consuming a spec absolutized into the orphan. The directory itself is
  left standing and the orphan is journaled, and a later flip back to `worktree` now
  reclaims it — the mount path is deterministic, so the leftover checkout made that second
  flip fail outright. The shared run branch is spared by the reclaim, keeping the commits
  earlier units landed on it.
- Fall back to the project when a task's recorded worktree is gone. Successful integration
  retires a task without clearing `worktree_path`, so the TUI's story-checkpoint card
  looked for `stories.yaml` under a deleted mount and lost the committed story's title and
  description.
- Tell the resolve session where an unreachable correction has to land. `context.json` now
  carries `redrive_base_ref` beside the reachability verdict, and the skill spells out that
  committing from the main checkout cannot include a file in a linked worktree and that the
  unit's own branch is not what the replacement mount is cut from.
- Locate the stories folder from the workspace root rather than from the spec's confinement
  root, so one modal can no longer read its spec from the run's tree and its sentinel from
  the project.
- Anchor pause notifications and the `checkpoint-pause` journal on the run's tree, sprint
  mode included. The dev-session prompt keeps the raw path — that session runs in the mount.
- Keep the dashboard up on a spec that is absent or undecodable: an absent spec reads as an
  explicit read failure rather than an empty body, and a bad byte degrades in place instead
  of losing the document.
- Refuse `Re-arm & resume` on a spec that could not be read, and report its blocking
  condition as unknown rather than absent. `Resolve` stays offered — it writes nothing and
  is what repairs a bad anchor.
- Report in `context.json` whether an edit to the spec survives to the re-drive, and teach
  the resolve skill to act on it: under isolation the mount is discarded first, so an edit
  to a worktree-local spec is lost unless it is committed.
- Decide whether the re-drive will run isolated from live policy instead of from the mount
  the escalated attempt recorded. `resolve` builds `context.json` in a separate process
  before the resume, so editing `[scm] isolation` while a story sat escalated made its
  advice wrong in opposite directions: switched to `none`, the session was told to commit
  the correction on the run's pinned branch, which an in-place re-drive never reads;
  switched to `worktree`, it was told a working-tree edit was safe when the replacement
  mount reads only committed content. The re-arm's unreachable-write record now says which
  of the two remedies applies, and the resolve skill spells out that a `HEAD` base means
  re-applying the correction in the main checkout rather than committing it anywhere. The
  TUI's re-arm refuses when `policy.toml` cannot be read rather than guessing a mode — a
  re-arm consumes the escalation, so a wrong guess is unrecoverable.
- Hold a re-armed SENTINEL until its upstream correction reaches the re-drive. A
  pre-planning sentinel is cleared by deletion, so that arm dropped the spec and returned
  before the reachability gate the status-flip arm runs — no gate was ever computed for it.
  The correction that stops the sentinel recurring is upstream (`SPEC.md` / `stories.yaml`,
  where the resolve skill sends the agent instead of the sentinel), and an isolated re-drive
  re-plans from the committed tree of a fresh mount, so an uncommitted upstream edit was
  invisible and the re-plan minted the same sentinel again, spending the escalation. The
  re-arm now records `rearm-upstream-write-unreachable`, names the folder and the branch to
  commit on, and stops the re-arm-and-resume gesture. Narrowed by proof rather than by
  configuration: the record fires only while the ref the re-drive mounts from does not
  already hold this checkout's copy of those two files, so a correction already committed
  there resumes in one gesture as before. An in-place re-drive never records — it reads the
  main checkout, which is where the resolve session runs.
- Re-read `[scm] isolation` after the interactive resolve session, before the re-arm.
  `resolve` loaded policy, then blocked on a human conversation of unbounded length, then
  keyed the re-arm on that stale answer while the engine it arms re-read policy for itself.
  Editing isolation while the agent was open therefore split the two readers: `none` to
  `worktree` re-armed treating the main-checkout correction as reachable, emitted no hold,
  then mounted a fresh worktree cut from git that could not see it. A change across the
  session is now reported on stderr.

- **A YAML boolean in a spec's baseline key no longer refuses the attempt** (#716). `no`, `off`,
  `yes` and `on` parse as booleans, and the shared reader stringified them into `"False"`/`"True"` —
  non-empty, so they were judged as a claimed sha and outranked a `baseline_commit` naming the
  correct commit. Booleans are now treated as absent, exactly as a YAML null already was.

- **A dev RETRY now notifies the operator, with the reason** (#640). RETRY was the only dev outcome
  that REJECTS an attempt without raising a notice, and it is the one that discards a completed
  implementation. The reason lived only in the `dev-decision` journal line, so a run could spend its
  whole attempt budget throwing finished work away with nothing but the eventual exhaustion notice
  reaching a human. The notice carries the reason's first line, capped and marked with `[…]` when
  trimmed; the untruncated text stays in the journal. It can repeat for one attempt if the host dies
  between the notice and the rollback.

- **A stale `baseline_commit` no longer outranks the fresh `baseline_revision` a spec claims**
  (#716). Both consumers of a claimed dev baseline ranked the legacy key first — and `waves
resolve` manufactures exactly that dual-key spec, inserting `baseline_revision` while never
  removing a pre-existing `baseline_commit`, so the gate judged the leftover and failed an attempt
  that had done everything right. One shared reader (`frontmatter.auto_dev_baseline_of`) now backs
  both: `baseline_revision` wins whenever it is non-empty, `baseline_commit` remains the
  backward-compatible fallback, and an empty or YAML-null value on either key reads as absent.

- **The dev proof-of-work gate measures the tree the baseline was written in** (#716). Under an
  explicit `repo_root:` with `isolation = "none"` the baseline is stamped in the git root, but every
  gate probe — the commit-identity lookup, both ancestry checks and `has_changes_since` — asked the
  BMAD project directory about it, so a marker only the project tree held satisfied proof of work
  and a correct attempt was refused forever. The four probes now share the git root, and so do the
  three file-granular exclude sources that feed them. Rollback protection independently builds its
  own list against the workspace root. No effect where the two roots coincide, which is every other
  configuration.

- **`waves resolve` advances the re-arm baseline in the code tree, and says so when it cannot**
  (#640). The advance read HEAD of the BMAD project directory rather than the git root, and
  swallowed every failure with a bare `except Exception`, so a re-drive that silently rebuilt
  against the pre-resolution tree looked exactly like one that adopted the human's fix. It is still
  non-fatal outside a repository, but now narrowed to the typed git errors and journalled
  (`rearm-baseline-advance-failed`); anything that is not a git answer propagates.

- **A re-armed story can no longer replay the abandoned attempt's verdict** (#705). Re-arm resets
  `attempt` to 0 and deliberately keeps `task.sessions`, so the next dispatch re-minted a session id
  byte-equal to a record the abandoned attempt had already written — and a host death before the new
  record landed resumed straight into that stale result. A per-task generation counter now
  discriminates the id, emitted only above zero, so every id already on disk stays byte-identical
  and a run resumed across the upgrade still finds its `tasks/` directories.

- **The three review gates run `[verify] commands` in the git root, not the BMAD project
  root** (#695). Under an explicit `repo_root:` with `isolation = "none"` they shelled out in
  the wrong tree — an operator's build/test verbs ran in the BMAD project dir rather than in
  the git root their code lives in.
  Artifact reads — the spec, the sprint board, the deferred-work ledger — stay project-rooted;
  only the command `cwd` moves. Every other caller already used the repo root.
- **A park that produced no code passes the dev gate** (#676). A session parking at
  `awaiting-operator` may legitimately leave nothing but the spec's own park declaration and
  the board sync, both of which proof-of-work excludes — so the gate read a correct park as
  "no changes since baseline commit" and refused it, costing the attempt and the park
  declaration with it. What was still pending at that point was the ORCHESTRATOR's commit —
  the squash and the park record land only once this gate passes; the session's own work is
  usually already committed above baseline, and a reset discards that too (onto an
  `attempt-preserve/*` ref). What the loss looked like depended on configuration — a reverted tree
  under `isolation = "worktree"` or `scm.rollback_on_failure = true`, a paused run with manual
  recovery steps on the default in-place config. Proof-of-work is now skipped on the parked
  leg only; the gate that refuses a park enumerating no `operator_actions` still runs. That skip
  covers every park, including one that produced nothing and listed plausible actions — the
  action gate tests that the list is non-empty, never what is in it.
- **The git-add shield refuses to enable `extensions.worktreeConfig` over an operator's
  explicit disable** (#396), instead of enabling it and deleting the line on rollback. The
  probe read the flag `--type=bool`, so a `false`/`off`/`no`/`0` in the shared config read
  as "needs enabling": the success path rewrote that declaration to `true` permanently, and
  a failed activation's `--unset-all` removed the operator's line and reported a clean
  rollback. Such a repo now gets no shield there, with a reason naming the spelling found.
- **The git-add shield seeds `%APPDATA%/Git/ignore` on Git for Windows >= 2.46** (#403), the
  file that fork prefers over `$HOME/.config/git/ignore` whenever it exists. Seeding the
  `$HOME` one there was wrong in both directions — an empty seed that let global ignores leak
  into `git add -A`, or patterns git is not applying that made session files go missing. Gated
  on the reported version's own `.windows.` fork string, not on the platform.
- **`--run-id` refuses the reserved control-session shape — `ctl` and every `ctl-<anything>`, in
  any letter case**.
  Such an id mints the control session's own name as the run's agent session (`waves-ctl`,
  or a per-registry `waves-ctl-<digest>` on psmux), so the adapter adopts the live control
  session and the run's teardown kills it — every parked window with it; on Windows the
  multiplexer resolves session names case-insensitively, so the case variants alias it too. The
  two session namespaces are now disjoint at the mint — and guarded at the read paths for runs
  an older release already persisted under such an id: `resume` and `resolve` refuse (at entry,
  before any side effect) with the recovery steps, while `stop`, `delete`, `archive` and `clean`
  work on the run without ever addressing a session that can be a control session's name (`ctl`,
  `ctl-<16 hex>` — the narrower shape a control session's name can actually take). A historical
  run under any other `ctl-*` id keeps its genuine agent session
  reachable in the registry the process addresses: `stop` kills it there by its exact name, and
  `cleanup` sweeps it like any other run's — including, for a tagged pre-upgrade session left in
  a legacy registry, through the legacy pass (`stop` reaches no registry but the one this
  process exported; the stop itself is registry-independent, only its backstop session kill is
  scoped).
- **TUI: a graceful-stop request that cannot be written is reported, not fatal.** The `S`
  worker caught only the helper's own refusals; an `OSError` from the write itself escaped,
  and Textual's default `exit_on_error` took the dashboard down with it. It now surfaces
  the same "may still be pending" guidance as `stop --graceful`.
- **A denied publish no longer leaks its staging temp on Windows** (#597). The temp had
  already taken a read-only target's READONLY bit when the replace was denied, and Windows
  refuses to delete a READONLY file, so the cleanup was denied too and the temp survived.
  It now clears the bit and retries.
- Refuse a psmux attached-client count whose answer names a different session, so a duplicated
  registry entry can no longer vouch for a `switch-client` that moved nobody — which
  `return_attached_client` reported as `RETURNED`, clearing the return option for a human still
  sitting there. Also refuse an empty or `:`-bearing session name before the probe spawns. A
  same-named session on a foreign server, and one differing only by whitespace the seam
  normalizes away, stay #531's subject (#671)
- The git-add shield's rollback report no longer raises through its own stderr decode on
  Windows (#394). `_shield_undo_extension` is contracted never to raise, but the `fsdecode` of a
  failing `--unset-all`'s stderr was guarded for `GitError` alone.
- **A run ref that names the runs directory itself is refused, and the two destructive run-dir
  writes are contained** (#480). `runs._is_path_escape` was the only member of the seven-site
  guard family omitting `names_tree_root`, so `""` and `"."` joined to the runs root exactly,
  and `delete_run` removed whatever it was handed with a bare `rmtree`. That reach needed a
  `state.json` lying at the runs root — without one those refs fall through to partial matching
  and can only name a child — and the ref is the operator's own argv, so this was a footgun
  rather than an escalation. `delete_run` and `archive_run` now also refuse a `run_dir` that is
  not a direct child of the runs directory, raising `UnconfinedWriteError` ahead of the
  live-session guard and not waived by `--force`. That refusal also covers a `run_dir` spelled
  `runs/..` — the one shape the direct-child rebuild reproduces verbatim while `rmtree` would
  resolve it to `.waves/loop` itself — and a run-dir level redirected through a symlink or, on
  Windows, an unelevated directory junction, which kept the lexical spelling while sending the
  removal outside the project. An empty run ref is refused outright as well: it is a prefix and
  a suffix of every id, so partial matching read it as a wildcard and resolved the sole run of
  a one-run project.
- **A sweep bundle name that is not a legal path segment is refused at triage** (#637), at both
  of `validate_triage`'s bundle-name sites — the `bundles` list and a decision option's
  `bundle_name`, which becomes `Bundle.name` by way of `_materialize_bundles`. A cycle-1
  bundle's name becomes its directory verbatim, and the reserved device basenames are all
  `[a-z0-9-]`-legal, so `BUNDLE_NAME_RE` accepted `con`, `nul` and `com1` while no Windows
  filesystem would create the directory — matched case-insensitively, so lowercase was no
  reprieve. The test is `safe_segment` identity rather than a second hand-written device list,
  which keeps the accepted set in lockstep with the sanitizer that defines it: the same idiom,
  for the same reason, as `runs.is_valid_run_id`. The persisted pre-answer lane takes the same
  two rules at `_materialize_bundles` — a `bundle_name` answered out of band against an earlier
  triage never passes `validate_triage`, and a fresh triage can renumber the option it named —
  applied by journaled discard rather than by error: the build decision is honored under the
  always-legal `decision-<id>` fallback name.
- **Deferred-work ledger mutators serialize on a cross-process lock** (#286, #469). Every
  mutator was an unlocked read-modify-write of the whole file, so two orchestrator processes —
  a second `waves run`, a run plus a sweep, a run plus the TUI decision modal, a run plus
  `sweep --archive` — both read, both edited, and the last atomic write won: entries lost,
  closures silently reverted, and two appenders minting the same `DW-<n>` because each read
  `next_seq` from the text it had just read. Every mutator now holds an advisory lock across its
  whole read-modify-write, and the orchestrator's remaining multi-write sequences adopt the
  batched primitives above, so each is one locked pass rather than one open window per row. The
  lock lives at `<state root>/locks/<digest>-<basename>.lock`, out of the repository rather than
  beside the ledger, because the ledger is tracked by design and the engine stages with
  `git add -A`; it is keyed on the resolved path, so every spelling of one file contends on one
  lock. Readers stay lock-free — every writer already replaced the file atomically, so a reader
  sees one whole version or another. Nested acquisition raises instead of self-deadlocking, and a
  lock that cannot be taken fails the write rather than proceeding unlocked. The dev/review
  session's own ledger writes are unchanged and still take no lock. `waves sweep --archive`
  names the ledger lock in its failure message rather than printing a bare `errno` — as a
  possibility rather than a verdict, since the same arm also catches the archive's own read
  and write failures and a full disk must not send an operator hunting a rival process. And
  `waves
decisions` and the TUI decision modal now also catch the state-root failure that deriving a
  lock path can raise — in the TUI an uncaught one escaped into the Textual event loop and took
  the dashboard down mid-walk. A project with no ledger at all is still answered without taking a
  lock, so `--archive` keeps reporting it as the success it always was rather than failing
  wherever no state root can be derived. `--archive`'s refusal while a run is live is
  unchanged and deliberately kept: it is coarser than the lock, refusing the archive rewrite outright rather
  than merely serializing it.
- **`sprint-status.yaml` advances serialize on a cross-process lock** (#286, #469). Being the
  board's sole writer was never mutual exclusion — a second orchestrator process runs that same
  sole writer — and an advance is a read-modify-write of the whole board, so two of them both
  read, both edited, and the last atomic write won: a story flipped by one run silently reverted
  to its earlier status, and the run simply walked past it. `advance` now holds the board's own
  sidecar lock across all three of its reads and its write, which also closes the gap inside a
  single call between the never-regress decision and the bytes that decision was applied to. A
  board that does not exist is still reported missing without creating a lock file at all, and a
  lock that cannot be taken fails the advance on the channel that already carries its errors
  rather than rewriting the board unserialized. Recomputing an advance for the isolated-run
  ownership check runs the locked body directly against its private throwaway copy: it needs no
  exclusion, nobody else being able to name that copy, and taking a lock anyway would strand one
  more sidecar keyed on a path that exists only for that call, since lock files are never
  reaped. The atomic, symlink-following,
  read-only-refusing write itself is unchanged.
- **A failed commit now rolls back only the ledger entries the story itself closed** (#286).
  The window between a story's declared `closes_deferred:` closure and its commit spans git
  spawns and, on the escalation leg, a pause for a human, so it is long enough for another
  writer to reach the same ledger — and the rollback used to rewrite the whole document from
  the pre-close text, taking whatever had arrived with it: an entry another process filed
  vanished (and its `DW-<n>` was handed out again), and a closure someone else had verified
  silently reverted to `open`. A story close is therefore written the way a sweep bundle's
  has been since #284, with a durable undo marker owned by that close, and the rollback
  reopens exactly those entries in one locked read-modify-write. Concurrent appends, closes
  and recorded decisions are left standing. An armed entry whose marker has since been
  displaced — a foreign line inserted between the status and its marker breaks the pairing —
  is left `done` with the foreign content intact and journaled as
  `deferred-close-reopen-unmatched`, rather than overwritten around; `deferred-close-rolled-back`
  now names the ids it reopened. The rollback stays advisory: it still never raises out of
  the failure arm it runs inside, so the commit's own escalation remains the disposition.
  **Ledger format:** a story close now leaves a permanent
  `resolution-undo: <digest> <date> <hex>` line beside its `resolution:` line, in the same
  committed ledger — the format `sweep` bundle closes already publish, now used by one more
  writer. Readers that ignore unknown fields are unaffected; `waves sweep --archive`
  already preserves the line.
- **A rolled-back defer no longer restores its ledger over a writer that arrived during
  the rollback** (#286). The three ledger-restore windows that remain all span `git reset --hard`
  and its preflight spawns, so a lock must not cover them; each is instead compare-and-set
  against the ledger as observed the instant the rollback returned. The defer restore is also
  gated on git owning the file, which inverts the old guard's worst case: on an untracked or
  external ledger — the one kind `reset --hard` cannot have touched — every difference from the
  snapshot was by definition somebody else's write, and rewriting the file on exactly that
  difference is what destroyed it. Such a ledger is now left alone. When the text does move
  between the observation and the lock, the snapshot is republished by APPENDING the entries disk
  has since lost, keyed by DW- id and carrying their bodies verbatim, so a concurrent append
  survives the restore instead of being rolled back with it; `defer-ledger-restore-diverged`
  names the ids moved. Flat appender blocks, which belong to no canonical entry, are reported
  rather than guessed at (`flat_remainder`) — the merge never invents a boundary the parser does
  not model. Entries are matched by id AND body, so an id the reset removed and a rival then
  re-minted for an entry of its own is reported as an `id_collisions` conflict rather than
  silently accepted as already-there: matching on the id alone dropped the very entry the
  merge exists to carry, and re-appending it would publish a duplicate `DW-<n>` instead. A
  write or lock fault still propagates, as the unguarded write always did.
- **A failed legacy-ledger migration refuses to restore over a ledger that changed
  underneath it** (#286). The sweep's post-reset rewrite of the pre-migration text had the
  same unguarded window; on a difference it now journals `sweep-migration-restore-diverged` and
  escalates for a human to re-run the sweep rather than writing. Deliberately no merge and
  no silent skip: leaving the rejected rewrite standing is the "never re-prompt over a
  half-broken rewrite" failure the restore exists to prevent, and a migration input that
  moved after the attempt was graded against it is a human problem — the same call the
  duplicate-id refusal already makes.
- **A rejected attempt's ledger retraction no longer overwrites, or deletes, a concurrent
  writer's work** (#286). This restore compares against two anchors — a persisted digest of the
  bytes the engine itself last published, and the ledger as observed the instant the rollback
  returned when git owns the file and its `reset --hard` republished it. Matching neither means
  the text is somebody else's, and the restore degrades to a journaled
  `ledger-restore-skipped-diverged` skip rather than a write. Deliberately no merge: a
  retraction cannot be expressed as an append. The skip is the safe direction — the
  harvest entries left standing are real findings, `append_entry`'s idempotence stops the
  next attempt filing them twice, and a non-restored ledger already reads as "changed" to
  the attribution rebase, which stands the harvest exclusion down and exposes more of the
  tree to the proof-of-work gate. The `snapshot is None` arm, which retracts a ledger the
  harvest itself created, is gated on the same digest, closing a latent data loss: it
  previously deleted whatever it found at that path, so a ledger a concurrent writer had
  created inside the window went with it. A tracked ledger absent at snapshot time is
  still never deleted, and is now answered before any lock is taken. A write or lock fault
  is journaled as `ledger-restore-failed` and preserves an in-flight pause, as before.
- **A read-dependent no-op is answered before its lock is taken** (#736). Taking a lock for
  work that turns out to write nothing could fail a call that used to succeed — a replayed
  `waves confirm` against a story the board already records as `done`, a replayed
  rollback, `sweep --archive` over a ledger holding nothing closed — either on contention or
  on deriving a sidecar path where no state root exists. `sprintstatus.advance` and the five
  read-dependent `deferred-work.md` mutators now take one advisory read first, running the
  same pure decision helper the locked pass runs; only a writes-nothing answer skips the lock,
  and every other answer, plus any probe fault, falls through to the hold and decides there.
  `sweep --archive` with nothing eligible now exits 0 rather than 1; an eligible archive under
  a dead lock still fails as before. `append_entries_published` deliberately still locks on a
  missing ledger, where absence means create.
- **A ledger restore that spans `git reset --hard` anchors on the committed baseline blob**
  (#735). The three restores no lock may cover — the rejected attempt's retraction, a rolled
  back defer's, and the sweep's failed-migration rewrite — compared the ledger against an
  observation read after the reset returned. A rival writing a tracked ledger inside that
  window became the observation, so the compare held and the restore overwrote its entries.
  Each write arm now takes its expected text from the ledger's blob at the baseline commit,
  probed before the lock, since a lock may never span a subprocess. Where the reset
  republishes no text at all — an untracked ledger, one configured outside the repo tree, or
  one symlinked into it, whose blob is a target pathname rather than ledger text — the anchor
  is the rewrite the attempt actually graded. Where no anchor can be derived, the retraction
  skips, the defer restore merges what disk has lost, and the sweep escalates; those
  doubly-uncertain cases previously still wrote. A rival whose text is byte-equal to the
  anchor stays indistinguishable from the reset's own work.

### Security

- **Confine the sweep's triage-cache write-back and bundle intent write to the project
  root** (DW-269). `_ensure_triage`'s `<run>/triage{suffix}.json` write-back and
  `_write_intent`'s `<run>/bundles/<dirname>/intent.md` still went through the plain
  `atomic_write_text`, which resolves every directory above the file by name, so a link
  planted at any directory component below the project root (`.waves/loop/`, `runs/`, the
  run dir, `bundles/` or `bundles/<dirname>/`) aimed both the staged temp and the
  published file out of the project — the escape #593 already closed for the sibling
  `<run>/decisions.json` writes. Both now write through `atomic_write_text_confined`
  against the project that owns the run dir. The cache write-back's refusal degrades on
  its existing `sweep-triage-cache-write-failed` row (`UnconfinedWriteError` is an
  `OSError`), costing the cycle its cache and nothing else; the intent write's refusal
  propagates exactly as any other write fault there does (DW-243). No new journal kind,
  pause stage or policy field.
  A link (or symlink loop) planted at the file's OWN name is no longer followed either:
  the plain writer resolved it and rewrote its target, the confined writer replaces the
  name (DW-247's `RuntimeError` loop arm goes with the `resolve()` it guarded), and the
  file lands `0600` with no mode inherited.
  On POSIX the `sweep-triage-cache-write-failed` `errors[0]` text now names the bare
  filename rather than the full path — the replace is dir_fd-relative.
  Accepted residual, unchanged: the run dir's other writers — the journal, `state.json`,
  and `ATTENTION` — still go through plain writers. The intent's preceding `mkdir` can
  still create directories through a redirected parent; a failed cache read can still
  unlink `triage{suffix}.json` through one. This change confines only the two file writes.
- **Confine migration run-directory record writes to the project root** (DW-288).
  `_ensure_migration`'s `<run>/migrate-manifest.json` and
  `<run>/migrate-result.json` used bare `Path.write_text`, so a link planted at any
  parent beneath the project could aim either record outside it. Both now publish
  atomically through `atomic_write_text_confined`, rooted at the project that owns the
  run directory. A manifest refusal still propagates before migration dispatch; a
  successful-result refusal still propagates before the ledger commit. Their JSON
  payloads and publication ordering are unchanged; unlike the old umask-derived files
  (commonly `0644`), both records now land with private `0600` mode.
- **`waves diagnose` no longer ships a merge record's target branch verbatim** (#640).
  The leak PRE-DATES the re-arm work this section is otherwise about: all three producers
  and the by-name routing shipped in earlier releases, so any dump of a run that merged a
  unit is affected, and the `#640` citation names the work that happened to find it rather
  than an issue that reported it.
  The journal's `target` field carries a branch on `unit-merge-started`, `unit-merged` and
  `resume-unit-merge` but a sprint status on the `board-advance-*` family, and per-field
  routing is by field NAME — so the field was left unrouted and an identifier-shaped branch
  name (`main`, `release`) passed through `scrub_json` into a bundle meant to be posted
  publicly. The egress backstop only masked it: it repairs a value already in the legend, so
  a run that journalled the same branch earlier was rescued while disclosing a
  `backstop_repairs` gap, and a journal truncated past that event was not rescued at all.
  Routing gains a narrow kind-scoped table for this one overloaded field; the sprint status
  keeps rendering verbatim, since aliasing it would destroy what those records are read for.
  The producers are deliberately NOT renamed —
  `engine._replay_unlatched_ledger_carries` correlates the merge kinds on a tuple including
  that field and reads journals written by earlier processes, so a rename would break the
  carry replay across a version boundary.

- **The run-archive staging temp is minted by `mkstemp` beside the destination — exclusive,
  `0600`, freshly named per attempt** (#591). The fixed temp name was created and unlinked by
  name, so a symlink planted there was followed and the cleanup could remove a concurrent
  archiver's in-flight temp; the exclusive create closes both, and the unpredictable
  per-attempt name keeps a temp stranded by a kill — or a file planted at a guessable name —
  from denying every later archive. The staged tarball is also `fsync`ed before publish,
  since the run dir it came from is removed immediately after.
- **Confined atomic writers anchor a file's parent with a directory descriptor instead of
  resolving it by name** (#593). `follow_symlinks=False` refuses a link planted at the file
  itself, but every directory above it was still looked up by name, so a link planted at
  `.waves/loop/` redirected the staging and the publish both. `atomic_write_text_confined` and
  `atomic_write_bytes_confined` walk the components `O_NOFOLLOW` and write through the
  resulting descriptor; a refusal raises `UnconfinedWriteError`, an `OSError`. Windows has no
  `*at()` family and degrades to the documented check-then-write.
- **The orchestrator's own writers under session-writable roots adopted those confined
  helpers** (#593): the decisions store, park records, the stop-request channel (the graceful
  lodge keeps its exclusive-create arbitration, now anchored at the walked parent), sweep
  decisions, `policy.toml`, the story-spec writers, and the run's config-digest stamp. A
  story spec in an artifacts folder configured _outside_ the checkout keeps the plain
  no-follow write — supported configuration a confined write cannot vouch for.

## [0.11.1] — 2026-08-23

### Added

- **git 2.34 or newer is now a declared prerequisite**, and the first one the orchestrator
  enforces. Set to keep Ubuntu 22.04 LTS (stock git 2.34) supported; Ubuntu 20.04 (2.25) and
  Debian 11 (2.30) fall below it. This is a support floor, not a capability one — nothing
  riaworks-waves-loop runs needs 2.34 — so the project can stop carrying workarounds for untested git.
  - `riaworks-waves-loop validate` checks it, as `git.version`.
  - `riaworks-waves-loop diagnose` records the host's git version in its Environment block.

### Changed

- **`run`, `sweep` and `resume` refuse to start below git 2.34, and `validate` now exits 1
  there** — a change of exit code on an under-floor host. A git that cannot be run, times out,
  or answers unparseably is refused the same way. `--dry-run` names the refusal in its
  "NOT runnable" banner instead of previewing a run that cannot start, and the TUI's
  pre-launch guard toasts it instead of opening a pane that dies.
- **The git-add shield's version gate moves from 2.20 to the project floor.** It now refuses as
  an unsupported-version policy rather than claiming a missing capability, which would be false
  at 2.34 — git 2.25 has everything the shield uses.
- **The git-add shield's activation check has git name the winning scope (#692).** The shield
  already refused to trust a `core.excludesFile` write it could not confirm git reads; the
  degrade reason now says _which_ configuration scope won, from the same single probe
  (`git config --show-scope`, git 2.26 — inside the 2.34 floor, which is what unblocked it):
  an ambient command-scope override (`git -c`, `GIT_CONFIG_PARAMETERS`, `GIT_CONFIG_COUNT`)
  now reads differently from a worktree write git does not see at all, which is a different
  repair. An rc-0 answer that names no scope is a new fail-closed degrade rather than a
  mismatch mislabelled. The decision is unchanged — a byte-identical answer still activates
  whatever scope supplied it, every unconfirmed answer still degrades, and the repo-format
  flag is still rolled back.
- **A hard stop rides `stop-request.json` with `mode: "hard"` (#319).** It is lodged before the
  engine is signalled — the atomic write also supersedes a pending graceful request — and honored
  at item boundaries and mid-session, where both real adapter wait loops poll it twice per iteration,
  which normally lands well inside the 10s grace window. An iteration blocked on a transport call
  or waiting for an artifact can exceed it, and the stop then degrades to the force-kill backstop —
  the pre-#319 outcome, never a worse one. SIGTERM is now the POSIX fast path rather than the mechanism, so a hard stop
  lands on every platform and multiplexer backend, and reaches a nested auto-sweep through the
  owning run's channel — hard-only; `stop <child-id>` is unchanged. A run directory that rejects
  the write degrades to the signal path with the stop still delivered.
- **`status --json`'s `graceful_stop_pending` is now mode-exact (#319)** — it reports only
  genuinely graceful requests. A modeless pre-#319 request body still reads graceful.
- **`stop --graceful` and the TUI report an already-pending request without calling it graceful
  (#319).** The request standing on disk may be a hard one — `stop` leaves one lodged when it
  could not prove the engine dead — and the idempotency answer is deliberately mode-blind.

### Removed

- **`verify.same_commit` is gone — nothing called it.** #645's `_canonical_commit_oid` displaced
  its last call site and compares canonical full object ids exactly. The helper's leftover
  prefix-tolerant equality — either argument a prefix of the other once both reach 7 characters —
  would have handed that looseness to whichever caller reached for it next.

### Fixed

- Escape gitignore pattern syntax (wildmatch specials, trailing spaces) when rendering
  worktree shield patterns, so a seed path carrying such syntax is shielded and its broken
  pattern can no longer hide an unrelated file (#476)
- Tokenize settled exclude lines the way git does (`\n`-split, one trailing `\r` trimmed), so
  an operator line carrying a lone `\r` can no longer make the shield writer skip a needed
  pattern (#472)
- Stop shielding a tracked tool directory whole: its pattern is replaced by per-file patterns
  for the untracked files provisioning wrote, so its tracked children no longer read as ignored
  to repo-hygiene gates. A file the session itself creates under such a directory can now be
  staged; an untracked tool directory keeps its ambient pattern unchanged (#484)
- **A queued release publish can no longer be evicted by a newer push (#468)** — the
  repo-wide `release-publish` concurrency group now sets `queue: max`; the default
  single-slot queue cancels an older _pending_ run when a newer one queues, so a
  maintenance-branch publish could be silently discarded by an unrelated `main` push.
  Also pins `cmd_publish`'s `check=False` with a regression test (the lost-race swallow
  was one revert away from dead code with the suite still green) and corrects a comment
  that still described the group as keying on `github.ref`.
- TUI: story-gate and epic-boundary pauses open a pause-reason viewer naming the blocking
  entries and the remedy, instead of an empty spec pane (#515)
- **Provisioning refuses an unparseable seeded hook config instead of silently replacing it
  (#592).** An isolated worktree's seeded `.claude/settings.json` that failed to parse was read
  as an empty document, so the relay merge always ran against a blank baseline and published a
  hooks-only file — the operator's permission allowlist, `env` and MCP entries gone, with no
  message and no backup. #590 made that write atomic; the parse still substituted `{}`, and
  that swallow is what this closes. Provisioning now raises, escalating the story as CRITICAL
  and pausing the run with the bytes untouched — the policy `init` has always applied to an
  unparseable config. The refusal names whichever source actually supplied the bytes — read from
  the seed bookkeeping, which now records each path copied rather than each entry attempted, so a
  config carried in as a child of a seeded directory is told apart from one merely sitting beside
  a seeded sibling. Invalid UTF-8 joins the same lane, having previously crashed the engine
  rather than escalating.
- **Native Windows: `riaworks-waves-loop stop` no longer burns the full 10s grace window into a blind
  `taskkill /F` (#319).** An inter-process SIGTERM is never delivered to a native-Windows engine,
  so every stop completed through the external fallback with no engine teardown at all. The engine
  honors the stop request itself now, so it is the single writer of `stopped` again and
  `run-stop fallback=True` is no longer stamped on a stop the engine recorded itself — it marks
  one this tool had to complete from outside.
- **`riaworks-waves-loop stop` no longer reports success when it delivered neither channel (#319).** A run
  directory that rejects the request write, followed by a signal the OS refuses, left the CLI
  saying the run had stopped — and stamping `run-stop fallback=True` — over an engine that may
  still be running with nothing on disk to stop it. It now kills the agent session as a backstop,
  records the undelivered attempt, and exits non-zero naming the retry.
- **Two concurrent `stop` invocations against one run no longer collide on a staging temp (#319).**
  The write staged through a fixed `stop-request.json.tmp`, so the loser's rename raised
  `FileNotFoundError`. It now stages under a per-writer name: the last write wins and neither
  caller errors.
- **`resume` no longer re-arms a run whose stale stop request it could not remove (#319).** It read
  "could not remove it" as "nothing was pending", wrote the pid, and stopped again at the first
  item boundary with nothing printed to say why. Resume now refuses before the pid lands and names
  the file, without re-stamping the host-exec integrity pin for a run it never started.
  `stop --cancel-graceful` likewise stops reporting "no stop request pending" for a request still
  on disk and still honorable — same exit code, accurate message.
- **A `stop` that never proved the engine dead keeps its request lodged (#319).** A `terminate` or
  `force_kill` refused with `PermissionError`, or a `taskkill /F /T` that failed silently,
  discarded the hard request while reporting the run stopped — throwing away the only channel left
  to stop a live engine. Death is now distinguished from refusal, so the stop stays genuinely in
  flight.
- **A hard stop arriving as the last item finishes stops the run instead of reporting it completed
  (#319).** Covers `max-stories-reached` too; a graceful request at an exhausted queue still
  finishes truthfully.
- **`stop --graceful` no longer downgrades a hard request that landed while it ran (#319).** The
  graceful lodge is now an atomic `O_CREAT | O_EXCL` create that answers "already pending" for
  anything already there, and a symlink planted at the path is refused rather than followed. Two
  concurrent graceful asks resolve the same way, which is the documented idempotency. A write that
  fails part-way leaves the request standing instead of rolling back — an unlink there resolves the
  path, not the file the call created, so it could remove a hard request escalated onto it — and
  `stop --graceful` reports it as possibly pending rather than as a clean failure.
- **A policy field of the wrong TOML type now raises `PolicyError` naming `section.key`
  (#440).** `loads()` coerced with bare `int()`/`float()`/`bool()`/`str()` outside the
  `PolicyError` funnel, so a wrong-typed value escaped every handler written to degrade on
  one: `_configure_mux` runs before dispatch on _every_ command, so one bad character in
  `.riaworks-waves/loop/policy.toml` traced back at you; the TUI died at construction instead of
  falling back to defaults; and `validate --json` exited before printing the document its
  one-object contract promises, which now carries the fault as an ordinary `policy` finding.
  Two of these never announced themselves at all: `notify.desktop = "false"` is a truthy
  string, so it turned the feature **on** (the hazard #278 recorded), and
  `verify.commands = "pytest"` exploded into six one-character commands that read back as
  applied configuration. Extends #587's `[limits]` sweep to every remaining section, with
  `[limits]`' own messages unchanged; allowlisted fields blame the type first. Valid policies
  parse identically — an unset `extra_args` still means "inherit the profile's flags" where
  `[]` means "none".
- **An undecodable or unreadable profile overlay or plugin manifest is a typed error naming
  the file, not a traceback (#473, #689).** `load_profiles` and the plugin loader read each
  `*.toml` outside the funnel that converts parse faults, so a non-UTF-8 file escaped as a
  raw `UnicodeDecodeError` past consumers that all key on the domain error: `validate --json`
  printed a bare `error:` line and empty stdout instead of an `adapter.profile` finding,
  `get_profile` carried it into run/sweep preflight, and a bad project `plugin.toml` took the
  settings screen down at construction. Both loaders now raise `ProfileError`/`PluginError`
  naming the path, on both arms — a file present but unreadable (permissions, a dead mount)
  was leaking a bare `OSError` on the same route. The packaged built-ins read through the
  same guard: a corrupt install is a packaging bug and should say so.
- **Merge-back failures are classified from the measured tree state, and the catch-all stopped
  inventing a conflict (#619).** A merge that died part-way through its checkout — all three
  strategies, `--ff-only` included — now raises `MergeHalfAppliedError` instead of "refused
  before starting": untracked residue is named for you to clear, and a tracked rewrite is
  restored automatically by `git checkout HEAD --` over exactly the affected paths.
  Attribution is per path — before/after deltas intersected with the branch's incoming set —
  so neither your pre-existing dirt nor an edit you make outside that incoming set while the
  merge is failing is ever called git's: the repo-wide dirtiness reading this replaces
  classified that concurrent-edit scene "failed part-way through checkout" and its repo-wide
  `reset --hard HEAD` destroyed the edit. (An edit racing the very paths the merge is
  rewriting is indistinguishable from git's write and is restored with them — the stated
  ceiling.) A post-merge probe that itself fails — the
  residue probes, the unmerged-stages reading, or the MERGE_HEAD reading — no longer bypasses the
  merge cleanup or impersonates a verdict: cleanup not gated on the dead reading still runs, the
  failure raises `MergeResidueUnreadError` (checkout state unverified, run `git status`), and an
  unread MERGE_HEAD skips the abort it gates and says so. The squash **replay** reading gets the
  same honesty on the far side of success: unreadable, it used to answer "dirty", and the doomed
  `git commit` that followed dressed the probe failure as a commit refusal with a
  `reset --hard HEAD` riding on it — now nothing is committed, nothing is reset, and the
  escalation names the dead reading. A refused
  **squash commit** now raises `MergeCommitRefusedError` like the `--no-ff` leg — the squash leg
  seals its result with its own `git commit`, where commit hooks and signing do run — rolled back
  by `git reset --hard HEAD` gated on the pre-merge reading having found the tree clean (a dirty
  checkout is never reset; the
  escalation then names the staged result and clearing it as your first step). A content conflict
  is typed too (`MergeConflictError`), so anything unclassified escalates saying just that — run
  `git status`, git's text names the cause — instead of "resolve the conflict by hand".
- **psmux: a hand-back that succeeded no longer reports as failed — or undoes itself (#659).**
  `switch_client` read its verdict off the session's attached-client count, which a same-session
  move cannot change — and same-session is the common shape for the return path, so a correct
  hand-back answered "failed". With the last-client fallback enabled (how
  `return_attached_client` always calls it) that verdict then fired `switch-client -l`, relocating
  the operator to an unrelated session; the relocation supplied the count change the correct move
  could not, so the call reported success and cleared its return option. The `-t` verb now takes
  its exit code as the verdict, gated on a client having been attached, and the fallback fires
  only when that verb failed.
- **A sweep whose client has dropped no longer keeps prompting the empty window (#659).** On tmux,
  `switch-client` spends one nonzero exit on both "that target is unreachable" and "there is no
  client here at all", so a failed hand-back read as "the human is still in front of me" either
  way; the session's attached-client count now separates them. `TerminalMultiplexer.switch_client`
  answers a third value, `None`, for any move it cannot vouch for — that state, a timed-out verb,
  and on psmux an unreadable gate count — which `return_attached_client` routes to `UNREACHABLE`:
  the return option survives, but the sweep goes unattended instead of blocking a later `--repeat`
  cycle on `input()`. `False` now carries the joint claim its caller always read it as. Out-of-tree
  backends answering a plain bool still work; `detach_client` is unchanged.
- **A psmux probe now answers for the calling pane, not the focused window (#669).** A target-less
  `display-message -p` resolves the server's _active_ window, so `current_window_id`,
  `current_pane_id`, `current_session` and `current_return_target` answered for a foreign window
  whenever the caller's own window was not the focused one — the ctl prune could kill the window it
  was running in, and the attach return could record a pane the human never came from. The probes
  now pin to the calling pane via `TMUX_PANE`, and answer `None` without spawning when that value
  is absent or not pane-shaped.
- **An unresolvable restore-patch or spec-folder path is now a named refusal, not a bare
  `[Errno ...]` (#560).** `_resolve_restore_patch` (`cli --restore-patch`) and
  `relativize_spec_folder` (`--spec`, `[stories] source`) each called `.resolve()` outside the
  exception type their handler caught, so a host that cannot canonicalize the path — a dead UNC
  provider (`WinError 64`), a symlink loop on the 3.11/3.12 floor — escaped by a route neither
  describes. Both now refuse by name and point at `riaworks-waves-loop validate`: the restore patch returns
  its sibling rejected-latch shape, the spec folder raises `stories.StoriesError`, and `--dry-run`
  reports it before exiting 1. A spec folder that merely lies outside the project tree still comes
  back verbatim — that is a supported layout, and only the canonicalization leg refuses.
- **An unstaged edit in your main checkout no longer escalates the story and pauses an unattended
  run (#618).** Under `[scm] isolation = "worktree"` the merge pre-flight refused over any dirty
  _tracked_ path outside the unit branch's incoming set, so a worktree-only porcelain `M` — modified in the
  working tree, nothing staged — stopped the run over a hazard git itself does not have. The axis
  is the index column, not trackedness: such a stray is now tolerated and journaled
  `merge-target-tolerated` alongside untracked dirt. A **staged** stray still escalates.
- **Dirt on a path the run commits for itself now blocks the merge whatever its index column
  (#618).** The post-merge carries stage the sprint board and the deferred-work ledger by
  pathspec, which takes whatever the working tree holds no matter who wrote it, so narrowing the
  pre-flight to staged strays alone would have let an operator's private edit land in history
  under a `chore(sprint-status): carry ...` message with the tree left clean. Both paths are now
  passed to the pre-flight as protected, and a stray among them escalates with its own remedy —
  such dirt has to leave the path, not merely be unstaged. Tracked artifacts only.
- **A resumed run no longer commits — or overwrites — board edits you made while it was down
  (#618).** When the merge was already journaled `unit-merged`, the replay falls through to the
  carry commits with no pre-flight in front of them. The carry cannot simply refuse on dirt: a
  crashed pass's own half-written advance is dirt on exactly that path and finishing it is what
  the leg exists for. It now asks whether the board holds HEAD's content plus this pass's
  advance — git's own question, so a board spelled CRLF by one host and LF by another still
  answers yes — and proves the index too, since the carry's `git add` overwrites it as well as
  the working tree; an ABSENT index entry counts as a staged untracking (`git rm --cached`) rather
  than as nothing to lose. That guards the commit, which is one write too late for the OWN row:
  `advance` would already have replaced the edit with the target, leaving precisely the bytes the
  proof accepts. So that row is now checked BEFORE the advance, and a status that is neither
  HEAD's nor this pass's own refuses it. Either refusal journals `board-advance-carry-foreign-dirt`.
- **A merge git refused before it started no longer sends you to resolve a conflict that does not
  exist (#619).** Every `GitError` out of the merge was labelled "content conflict against the
  target", but most are git declining at pre-flight — an untracked file the merge would overwrite,
  a staged change on an incoming path, a file/directory shape clash, an `ff` target that cannot
  fast-forward — where nothing merged, the target checkout is untouched, and there are no markers
  to find. Those now raise `verify.MergePreflightError` (a `GitError` subclass, so every existing
  handler is unchanged) and escalate describing that state, with git's own text naming the cause.
  A third state needed its own type. A `--no-ff` that merges cleanly and is then refused at the
  COMMIT — a `pre-merge-commit` or `commit-msg` hook, or a `commit.gpgsign` that cannot sign —
  leaves no unmerged stages but does leave `MERGE_HEAD`, so reading the index alone called a
  started merge a pre-flight refusal and sent you to clear a clash that does not exist.
  `verify.MergeCommitRefusedError` now names it: the merge is aborted and the escalation points at
  the policy that declined rather than at a tree with nothing wrong. Where the abort ITSELF fails,
  it says so and sends you to recover the mid-merge checkout first — a resume attempted before
  that dies on the merge state however well the hook is fixed.
- **A refused `squash` merge no longer destroys the uncommitted work in your main checkout
  (#619).** `--squash` has no `--abort`, so the recovery is `git reset --hard HEAD` — gated on a
  tree-state probe read _after_ the merge and used to answer "did the squash act". A checkout
  already carrying an unstaged edit reads dirty whether or not git touched a byte, so a merge git
  refused at pre-flight fired the reset and discarded work the merge never went near. The probe is
  now read once _before_ the squash and a tree found dirty is never reset. The same root cause
  corrupted the replay gate that recognises "the squash staged nothing", which now asks the index.
- **The journal no longer records a path as tolerated when that path is what stopped the merge
  (#623).** `merge-target-tolerated` is written from inside the pre-flight guard, strictly before
  the merge runs, so it can only record what the guard decided. A stray outside the incoming set
  by _path_ can still clash with it by _shape_ — a file where the merge needs a directory, or the
  reverse — and git then refuses over the very path the event called harmless. The refusal path
  now appends a corrective `merge-preflight-refused` naming the same paths and carrying git's text.
- `riaworks-waves-loop ls` on a core-only install lists runs again instead of crashing on a missing `pyte`
  — the run-inventory reader moved into core (#650)
- A missing `[tui]` extra now prints the install hint whichever dependency fails first, instead of
  a traceback (#678)
- The settings schema no longer reaches the `[tui]` extra at module scope, and CI now proves the
  core CLI works extra-less (#679)

## [0.11.0] — 2026-08-19

### Added

- **Plugins can now observe structured dev verification results (#641).** The existing
  `post_dev_verify` hook receives immutable per-command results after normal and repair
  verification, with separate `stdout`/`stderr` alongside the compatible bounded
  `output_tail`. The context also carries `verification_stage` (`"dev"` or `"fix"`) and
  `verification_sequence` — the only way to tell a dev verification from a repair one
  (both emit the same stage from the same phase) and the key that joins the context to
  its own journal records. Core writes `verify-command-result` journal records with
  stream pointers under the run's `verify/` directory — its own store, kept out of the
  adapter-owned, TUI-consumed `logs/`; plugins remain unable to alter verification or
  commit decisions. Storage, upload, signing, and any policy response stay plugin-owned.
  Scope is the dev phase: the review gate runs the same `[verify] commands` and retains
  nothing, so the journal records are not a census of a run's verifier invocations —
  `docs/plugin-authoring-guide.md` states the boundary, and #656 tracks closing it.
  Retention is bounded by the new `[verify] stream_capture_kb` (default 256 KiB per
  stream, `0` = capture nothing): the tail is kept, and the record carries the full
  byte count plus a `*_truncated` flag so a cut file is never mistaken for a whole
  one. A concluded run gives the store back: `riaworks-waves-loop clean` trims `verify/` with the
  rest of a run's heavy scaffolding and counts it in the reclaimed total, leaving the
  run listed and resumable. Separately from that on-disk cap, a hard 32 MiB per-stream
  ceiling bounds what is held in memory while the remaining commands run, so a
  pathologically chatty suite cannot grow peak memory with the number of configured
  verify commands; the record still reports what the command emitted, so a stream the
  ceiling cut is never mistaken for a whole one. Retaining a stream is observation, so a
  failed write (ENOSPC, a read-only run dir) degrades — the record still lands, with a
  null pointer and `capture_error` — instead of taking down a dev pass whose verify
  commands passed.

- **A refused auto-sweep is now visible outside the journal (#501).** A run whose deferred-work
  sweep was refused ended looking exactly like one that swept, and under `[sweep] auto = "run-end"`
  there is one trigger per run that is never re-asked once the run finishes — so the journal was
  the only trace. Runs now record `sweeps_refused` (trigger → reason), surfaced by the end-of-run
  summary, `riaworks-waves-loop status`, `status --json` and `riaworks-waves-loop diagnose`; the follow-up they name
  is `riaworks-waves-loop sweep`, which needs a clean worktree. The reason is a fixed slug — `not-started`,
  `failed` or `dirty` — never an exception message, which `diagnose` would refuse to emit at all.
  The `--json` key is additive and always present, so `STATUS_SCHEMA_VERSION` is unchanged.

- **`validate` now reports a binary that is on PATH but will not run (#294).** The
  `adapter.binary` gate asked `shutil.which`, which a dead WSL/npm shim satisfies — it is a real
  file with the execute bit — so validate went green on an install that could not start a session,
  and the opencode adapter's own "binary not found" error sent the user to `riaworks-waves-loop validate` to
  be told everything was fine. Each binary named by a **packaged** profile is now run once as
  `<binary> --version`; a nonzero exit or a launch fault reports the new check id
  `adapter.binary-unrunnable`, carrying the resolved path and the return code. A project overlay's
  profile is resolved and reported found but never launched: its fields are project-supplied, and
  validate is the command used to decide whether a checkout is safe to run at all, so a clone's own
  config cannot choose which binary it launches. The gate bounds which NAME is probed, not what
  that name resolves to — resolution runs through the user's `PATH`, and a probed name resolves to
  whatever the session launch would itself run. That boundary is the profile's provenance and not
  the spelling of `binary`, because a bare name still resolves into the checkout whenever a
  checkout-local directory is on `PATH`. The severity is `warning`, so validate's exit code is
  unchanged for a live CLI that merely answers `--version` oddly, and `adapter.binary` keeps its
  existing found/absent meaning. The check id is additive, so `VALIDATE_SCHEMA_VERSION` is
  unchanged.

### Changed

- **The psmux live gate now runs in CI instead of before releases (#662).** The `test-windows`
  job installs psmux from its GitHub release, so `tests/test_psmux_live.py` — prune isolation, the
  workaround premise probes, the 3.3.8-floor adoption probes — runs on every pull request
  and on pushes to `main`/`release/*`, rather than on a maintainer's Windows box at release
  time. It runs as its own serial step: real psmux servers are a single-machine resource,
  and the gate flaked when interleaved with the parallel run. The step asserts
  `PsmuxMultiplexer.available()`, not just that the binary resolves: the gate skips itself on
  an unadmitted version, which would otherwise read green. `test_opencode_live.py` remains the
  one manual gate.

- **The psmux backend now requires psmux 3.3.8 or newer (#658, closes #222).** `available()`
  refuses 3.3.7 and below, so **on such a host the backend reports unavailable and selection
  falls through**. Every verb now assumes 3.3.8's fixes instead of routing around the defects
  they close, and a 3.3.7 install would fail silently rather than loudly.

- **The retired psmux workarounds change three visible behaviors (#658).** The run-log sink rides
  the same `-EncodedCommand` transport as every other window command instead of a sidecar
  `.ps1`, so a log path containing a space, `$` or a backtick no longer breaks or blocks log
  capture, and nothing is written beside the log. `select-window` takes the session-qualified window id
  directly, dropping a listing round-trip per focus change. `kill_session` inherits the base's
  `=name` exact-match target.

- **The psmux option-value gate now refuses only what it cannot read back (#658).** Ordinary
  Windows paths all pass — spaced, UNC, apostrophed, trailing-separator. What stays refused is
  what the backend's own listing parse would mangle: a double quote, a line break, edge
  whitespace, and a `-`-leading value psmux still treats as a flag.

- **`post_dev_verify` now fires on the repair leg too, not only after dev verification (#641).**
  A plugin written against "once per story, after the dev session" will see the stage again after
  every repair session's verification, and on the way to a pause: an attempt whose session reported
  a CRITICAL escalation now emits before the run stops, on either leg, where the repair leg used to
  escalate without emitting at all. Discriminate the legs with `ctx.verification_stage`
  (`"dev"` / `"fix"`) and de-duplicate on `ctx.verification_sequence`; handlers that assumed one
  call per story must be idempotent.

- **`probe-adapter` now bounds how long a single scrubbed line can be (#481).** `scrub_text` capped
  how many lines it emitted but never how long one of them could be, so a single very long line —
  from a foreign CLI's `--version`/`--help`, or from a log tail — reached the `probe-adapter`
  report and its `--json` document verbatim: `max_lines=5` over a 5000-character line still emitted
  all 5000. Each line is now bounded, and a line that is cut ends with `… (N more chars redacted)`,
  the same convention as the existing line-count marker. **This is a visible output change** for any
  line that long. A cut that would land inside anything the egress guard flags — a credential-shaped
  token, or a URL credential whose match ends at the `@` — retracts out of it and drops it whole:
  cutting mid-construct could otherwise leave a fragment that keeps the sensitive part while no
  longer tripping the rule, turning a fail-closed refusal into an emission carrying part of the
  credential. `probe.SCHEMA_VERSION` is unchanged: no field is removed or renamed and no type
  changes, and the meaning of the value was already "the CLI's scrubbed output, capped" — adding a
  second axis to an already-documented lossy cap is the same class of value, not a new one.

- **Files the orchestrator replaces by name now land at `0600`.** Those writes pass
  `follow_symlinks=False`, and that mode deliberately carries nothing over from the target — not
  its permission bits, not its xattrs — so the new contents arrive at `mkstemp`'s private default.
  Affected: `.riaworks-waves/loop/decisions.json`, `.riaworks-waves/loop/policy.toml`, the park records under
  `.riaworks-waves/loop/operator/`, and any story spec written through `set_frontmatter_status`,
  `set_frontmatter_field` or `devcontract`. Most were already being reset to `0644` on every
  rewrite — the hand-rolled temp they replaced was created at `0666 & ~umask` and `os.replace`
  swapped _that_ inode into place — so for those the delta is `0644` → `0600`. Git records no mode
  but the exec bit, so nothing downstream of a commit notices.

  The no-follow choice is made per **file**, not per call site: once one writer of a file replaces
  it by name, every writer of that file has to, or they disagree about what the path means.
  Applying it that way brought four writers into line that had been direct
  `write_text`/`write_bytes` calls — `verify.safe_rollback`, the engine's park-record restore,
  `set_frontmatter_status` and `set_frontmatter_field`. Those four opened the name, and so wrote
  _through_ any symlink planted at it; they now replace it. That is a real change at those four,
  and what makes it safe is the same per-file rule: each of those files already had a
  name-replacing sibling writer (`policy.write_mux_backend`, `record_park`,
  `devcontract._atomic_write_spec`), so no link at those names survived the orchestrator anyway.
  Files with no name-replacing sibling keep following symlinks — `sprint-status.yaml` and your
  CLI's `settings.json`, both operator-curated, so a board or a config kept outside the tree and
  linked in keeps being a link.

- **`atomic_write_bytes` accepts `follow_symlinks`, as its text sibling already did.** The default
  stays `True`, which the private-git-exclude writer depends on: it pre-creates the target
  precisely so the helper has a umask mode to carry over, and git silently ignores an exclude file
  it cannot read.

### Fixed

- **A failed `kill-window` that left the window alive is no longer swallowed (#658).**
  `BaseTmuxBackend.kill_window` ran `check=False` and discarded the result, so a kill that failed
  with the window still standing left it behind with no trace. A non-zero exit now reads the
  session's own window list once and warns on stderr only when the target's window is still in
  it; an already-gone window — what ordinary teardown produces — and a target that names no
  window at all both stay silent, because neither leaves anything behind. The verdict is
  unchanged: still returns `None`, still never raises.

- **A plugin can no longer erase a CRITICAL escalation out from under the engine's audit.**
  `HookContext` copies the session `result_json` precisely so a plugin observes history rather
  than rewriting it, but `dict()` is shallow: the nested `escalations` list stayed the engine's
  own object, and both verify legs emit `post_dev_verify` before reading
  `critical_escalations(result.result_json)`. An in-process plugin that cleared that list
  therefore erased the escalation before the audit ran, and a verify-green repair proceeded
  where the run owed a pause. The copy is now deep, so the observe-only guarantee holds at the
  depth escalations actually live.

- **The egress self-check now sees Windows→WSL UNC home paths (#512).** `diagnose` and
  `probe-adapter` re-scan their own rendered bytes before emitting and refuse to emit at all on a
  hit, but the absolute-home-path rule knew only forward-slash spellings — so a path reached through
  the Windows→WSL UNC bridge (`\\wsl.localhost\<distro>\home\<user>`, the legacy `\\wsl$\...`, the
  extended-length `\\?\UNC\...` folding) was invisible to it, including through the `--json` render,
  where every backslash is doubled. **No released version leaked such a path**: since #485
  `collect_env` reduces the project path to a boolean and no `EnvInfo` field carries it. What was
  wrong was the claim — the `diagnostics` module docstring described the backstop as fail-closed
  without qualification — and that docstring is corrected in the same change to say what the guard
  is, a shape re-scan of the rendered bytes, and what stays outside it: a home spelling it does not
  know, or a username that is not this process's.

- **The `diagnose` policy snapshot's verbatim-key invariant is now enforced (#202).** The snapshot
  emits dict keys unredacted, which is correct only while no policy section is a free-keyed table
  — the one user-keyed table, `plugins.settings`, is intercepted before it reaches the
  passthrough. Nothing enforced that property, and a value-level check could not: a newly declared
  free-keyed section defaults to an empty dict, so such a check stays green while the hazard is
  live. A test now fails at declaration time, the moment such a section appears, and the reason is
  written down at the passthrough. No behavior change.

- **The zero-token OpenCode live smoke skips stale or broken shims (#294).** Its availability
  gate now requires `opencode --version` to succeed before starting a server; runnable installs
  still fail loudly when the pinned API contract drifts.

- **Policy loading now enforces the declared timeout and result-less Stop nudge minima (#648).**
  The valid `session_timeout_min = 1` and `stop_without_result_nudges = 0` boundaries remain
  accepted, while smaller values now raise `PolicyError`.

- **Reject mismatched TOML scalar types for every `limits.*` policy field (#278).**
  Quoted booleans and other coercible values now raise `PolicyError` instead of silently changing
  the configured limit or enabling a disabled behavior.

- **Attempt-owned spec-only retries no longer demand a false manual rollback (#123).** A
  bound plain attempt whose only residue is its lifecycle flip is restored to its pre-attempt
  lifecycle status and proven Git-clean before retry. A resolved re-drive may instead retain an
  authorized dirty, human-corrected spec and reports `rollback-owned-spec-normalized` without
  claiming cleanliness or auto-committing the correction. Each bound retry chain now snapshots its
  first spec input byte-for-byte and retains it across dev- and review-verification repairs, so a
  later failed child cannot replace that input with its own body edits. Non-fixable retries park the
  failed child, restore the snapshot, and then re-establish the promised lifecycle route after
  resetting sibling residue. Repair prompts validate retained authority before they can reset a
  spec, and a plain child that puts a tracked spec back at Git baseline cannot erase pre-launch
  operator edits. Pre-existing untracked and ignored bound specs use that snapshot as their
  independent dirtiness oracle and are force-included only in the private recovery ref before
  restoration; index-only force-adds and cached removals also trigger cleanup, which restores the
  baseline index ownership. `rollback-owned-spec-restored` records the repair. Missing, unreadable,
  retargeted, changed external, or unsafe legacy authority pauses with convergent spec-adoption
  instructions, and recovery refuses a reset whose baseline would replace the canonical path or a
  parent directory with a symlink, tree, file, or other unsafe shape. An initial Sprint observation
  fault may leave a bare-key attempt unbound; an existing Stories folder+id target instead aborts
  unless it can be snapshotted. Post-bind faults abort before launch while retaining the authority
  for recovery. Protected rollback inventories and deletion replay remain byte-safe for POSIX
  filenames outside UTF-8. Snapshots are retired after commit. Other substantive changes and
  sibling source, artifact, or untracked residue still follow the configured rollback policy.

- **Recorded sprint re-drives now route directly through their known spec (#630).** Only a
  generic sprint task with a recorded `spec_file` names that `ready-for-dev` spec explicitly and
  pins deterministic read-back to the same file. Fresh sprint tasks with no recorded path remain
  bare-key dispatches; Stories stays folder+id, Sweep stays intent-bundle, and patch-restore plus
  verification-feedback routes retain their existing wording and precedence. A filesystem fault
  while observing the dispatch binding leaves that attempt unbound instead of aborting the run.

- **Accept canonical reachable-descendant spec baselines without trusting untracked residue.** An
  exact recorded baseline remains valid; any different real claim must uniquely resolve from 7–64
  hex characters to a direct immutable commit that descends from the recorded baseline and is
  reachable from `HEAD`. Symbolic or movable refs, ambiguous prefixes, non-commit objects, older,
  diverged, unknown, and off-HEAD claims remain refused, apart from the existing deferred-work
  bundle ancestor exception. Proof is re-anchored after an accepted descendant and counts only
  tracked, staged, or committed changes because the launch snapshot cannot date untracked files
  relative to that later claim. Shared-checkout mode proves later tracked work exists but cannot
  attribute it to one session; worktree isolation preserves that provenance. This accepts a skill
  stamp made after an intervening commit without letting stale untracked residue satisfy the gate.
  The same mismatch in the opposite direction is #640.

- **Overlong lowercase/kebab sweep bundle labels now proceed deterministically (#503).** An
  otherwise valid name over 40 characters is truncated to 40, journaled and persisted before
  validation, so the sweep proceeds without spending a feedback retry or pausing the run.
  Post-truncation collisions and other invalid shapes still fail validation.

- **Silent OpenCode parent sessions now enter bounded recovery from launch (#411).** Parent/child
  SSE activity and a provably busy or retrying parent re-arm the grace; true silence spends the
  bounded nudge budget and is classified `stalled`. This neither prevents upstream subagent
  interruption nor guarantees that best-effort `prompt_async` nudges wake it.

- **Generic and OpenCode dev/review stall grace now arms at launch and re-arms on activity (#470).**
  Pane/SSE activity and later turn-end evidence restart the grace, so a truly silent live session
  spends its configured bounded nudges and becomes `stalled` near the grace sequence instead of
  necessarily consuming all of `session_timeout_min`. Completion still requires Stop/idle evidence
  or window/server death plus deterministic artifact verification; prose never completes a session.

- **Dead targets no longer abort the generic completion loop from its two nudge sends (#504).** The
  stall and result-less-Stop sends alone contain `MultiplexerError`, after which deterministic
  liveness and artifact logic decides `crashed` or `stalled`; this is not blanket multiplexer failure
  tolerance.

- **Path-resolution refusals no longer tear down worktree runs mid-provisioning (#556).**
  Observation probes report coarse unknown entries, each refused seed is skipped independently,
  provisioning-root uncertainty raises a typed escalation and pauses before any write or session,
  and mount uncertainty defers only the affected unit. Required upstream-skill absence still
  escalates; this boundary does not include `ProjectPaths` or confined cleanup resolution.

- **Rollback path uncertainty now triggers a pre-destructive rollback pause (#557).** Trusted
  spec containment fails closed, observational exclude and story derivation use explicit
  fail-open or empty fallbacks, collision uncertainty keeps and escalates the branch, and exact
  commits omit only an uncertain candidate after a trusted root is established. This is limited
  to the audited verify and recovery boundaries, not every path-resolution call.

- **The dashboard now survives project-root resolution refusal with unavailable panes (#558).**
  Startup and polling retain empty or unavailable views through one stable lexical/canonical
  cache spelling. This preserves the dashboard around a dead provider; it does not recover the
  provider or make it operational.

- **Advancing a sprint board now preserves every authored line ending (#576).** A valid UTF-8
  board keeps each CRLF, LF, bare-CR or mixed per-line terminator while the requested story,
  conditional parent-epic and optional `last_updated` values still change. Previously the
  read/write relay could translate the whole board to the platform line ending, producing
  newline-only diff noise outside those intended value edits; parsed YAML content was not
  corrupted.

- **A `sweep --migrate` rewrite that drops a `gate:` token a pre-existing entry declared is now
  refused, instead of un-gating that story silently (#519).** Validation held the rewrite to each
  entry's id and status only, so losing the token passed, got committed, and the next dispatch ran
  the story the entry existed to hold back. The original ledger is now restored and the session
  re-prompted with the error, escalating after `max_migration_attempts` — a rewrite that previously
  passed can now fail. An _added_ token is still accepted, since over-blocking fails loudly and in
  the safe direction. Migration-scoped: every other ledger edit is still held by the format doc's
  instruction alone.

- **`sweep --migrate` now refuses a ledger that already carries duplicate `DW-<n>` ids, rather than
  migrating it into silent data loss (#519).** One id naming two entries cannot survive a migration
  either way: the rewrite that keeps both is rejected as duplicate, and the one that passes collapses
  them and drops a twin's `gate:`. The sweep now pauses before any rewrite is dispatched, naming the
  ids to renumber, and resumes with its migration budget intact. **A deliberate behavior change
  beyond #519's original scope:** such a migration completes today by losing that data, and will now
  stop instead. Bounded to ledgers that already carry duplicate ids.

- **An unrelated untracked file in your main checkout no longer blocks every isolated unit merge
  (#460).** Under `[scm] isolation = "worktree"` the pre-merge reconcile refused over any dirty path
  outside the unit branch's incoming set, untracked included, so a single `notes.txt` escalated the
  story and paused an unattended run. A merge writes only the paths that differ between target and
  branch and never stages an untracked file into the commit, so untracked dirt outside that set is
  now left where it is, the merge proceeds, and the run journals `merge-target-tolerated` naming it.
  Uncommitted changes to **tracked** files still escalate — `merge_strategy = "squash"` would fold
  them into the story's commit. Reaches dirt that appears after the run starts, and every `resume`.

- **The escalation that remains no longer blames a game engine (#460).** It asserted that "likely a
  Unity Editor wrote into the main project" on every isolated merge — the guard's origin story
  rather than a diagnosis, fired on repos with no Unity anywhere and no plugins loaded — and told
  you to "clean them", which is the exact verb the reconcile performs with `unlink` on its own
  paths. It now names the tracked files, asks you to commit, stash or revert them, and demotes a
  `per_worktree` engine Editor to one possible cause beside ordinary local work.

- **A git that warns while still exiting 0 no longer corrupts the answers the orchestrator reads
  back from it (#442).** An unknown `core.fsyncMethod` value or a `core.fsmonitor` hook that cannot
  exec is a property of the host's git config rather than a failure, but the shared git helper handed
  callers `stdout` and `stderr` merged — so every probe that read git's text as the ANSWER took the
  advisory for data. Silently: a rollback candidate list grew a phantom path, a commit list grew a
  phantom sha, and the sha and branch probes answered with the warning appended — the last of which
  reached the baselines persisted in run state, so a resume graded a warning-carrying string against
  a clean one and read "moved". Loudly: preserve-ref retention raised `PrunePreserveError`,
  `commit_paths` raised where its contract reports nothing to commit, and the worktree snapshot
  failed outright — which since #340 is a gate and not a safety net, so a noisy host had no working
  rollback at all. Thirteen value-reading probes now take stdout alone; the ~45 call sites that only
  check a return code are unchanged, and a failing git call still carries its stderr.

- **An indented, tab-separated or empty heading in the deferred-work ledger no longer lets a `gate:`
  below it hold a story the entry never named (#516).** A canonical entry ended only at a `#` run at
  column zero with exactly one space after it, so three shapes CommonMark spells as ATX headings —
  up to three spaces of indent, a tab as the separator, and an empty heading — ran on past the
  section header and absorbed the next section's field lines. A later `gate:` then landed in an open
  entry that had declared nothing: `validate` failed (`deferred.hard-gate`) and `run` paused
  (`story-gate`) on a story that entry never gated. Two reads move with the boundary: a `status:`
  below such a heading is now that section's rather than the entry's, so the entry parses with no
  status and leaves the open set; and a tail below one is no longer masked by an over-long span and
  reaches the legacy parser again. Four spaces of indent or a leading tab is an indented code block
  rather than a heading and still ends nothing, and a heading nested in a list item or a blockquote
  (`- ## Notes`) is still not a boundary either — the same line-scope limitation as #327.

- **Launching with a `--run-id` that already names a run is refused (#602).** The flag pointed at an
  existing run adopted that run's directory and published its own `state.json` over it. The id is
  now claimed exclusively as the directory is created, so a collision aborts the launch before
  anything is written and the earlier run is left untouched.

- **A launch that aborts while standing up its adapters no longer strands an empty run (#602).** An
  adapter failure left a run directory with no `run-start` that nothing reconciled, so it lingered
  in `riaworks-waves-loop list` looking resumable. Composition is now atomic from the first published
  artifact: on any escape the run directory and its out-of-tree state are removed and the original
  error is re-raised unchanged. The removal keeps the live-session guard, and a removal that itself
  fails is now reported instead of passing silently.

- **A failing auto-sweep can no longer kill its parent run, and a stop during one is no longer
  swallowed (#600, #601).** A `SystemExit` from the child — what an unusable multiplexer or an
  unresolvable profile raises — escaped every handler and ended the process at exit 1, leaving the
  parent neither `finished` nor `crashed` with an orphaned agent session. In the other direction a
  stop was recorded as a child failure, letting the parent run on to `finished` and leaving it
  unstoppable. `KeyboardInterrupt` deliberately still escapes.

- **A run's `sweeps_triggered` records only auto-sweeps that actually started (#501).** The trigger
  was spent before anything had been attempted, so every way a child could decline to launch
  consumed it — including a plain `git status` timeout, which fails closed and could silently burn
  a run's one and only sweep. The tree check now runs ahead of the record and journals a `reason`
  distinguishing a git fault from real local changes. Not a retry: what this buys is that
  `riaworks-waves-loop diagnose` stops reporting sweeps that never ran. A child that fails after its run
  directory exists still spends the trigger; the never-launched case journals
  `sweep-auto-not-started` and keeps its own notification.

- **A failed write can no longer truncate the sprint board, a story spec, your CLI settings or your
  policy file (#379).** Seven writers read a file, merged into it, and wrote the whole thing back
  through a truncating `Path.write_*` — so a fault partway through (ENOSPC, EIO, a quota) published
  a _prefix_ of the file and destroyed the rest. All seven now go through
  `platform_util.atomic_write_text` / `atomic_write_bytes`: contents to a temp, fsync, replace.

  Most of these fail _quietly_ — the file still parses afterwards, so nothing downstream raises:

  - **The sprint board.** `sprintstatus.advance` is the orchestrator's sole write path to
    `sprint-status.yaml`. YAML cut at a line boundary is still a valid mapping, just a smaller one,
    so the epics past the tear ceased to exist and the run walked off the end of the sprint instead
    of erroring.
  - **A story spec.** A spec is laid out `before + edited + after`, so a write that faulted after
    the frontmatter had landed left intact frontmatter saying `status: done` over a decapitated
    body — a spec that lies, which the loop then commits. `set_frontmatter_status`,
    `set_frontmatter_field` and `devcontract`'s four in-place rewriters now share one call.
    `devcontract` was already atomic and recorded the measured cost: fault injection on the old
    truncating write cut a 46-byte spec to 12.
  - **`.riaworks-waves/loop/policy.toml`.** `safe_rollback` captures it before the `git reset --hard` and
    writes it back after, so your orchestration config survives a rollback whether or not it was
    committed. A truncated TOML is not a smaller config — it is a parse error the next `run`
    refuses on, which is the failure the whole restore exists to prevent.
  - **The park records.** The engine restores a story's record when the commit it was written for
    fails. A record left truncated reads as a park owing nothing, while the board still says a
    human owes something.

  Your CLI's `settings.json` is the loud one. Both writers that register the completion hook —
  `init` and each isolated worktree's provisioning — parse the whole config, merge the relay into
  it, and write all of it back, so your permission allowlist, `env`, MCP entries and your own hooks
  survived only by round-tripping through that one call. JSON has no partial read — a prefix of an
  object is a parse error, not a smaller object — so this was never silent, just unrecoverable:
  `init` refused on the next run with `is not valid JSON; fix it and re-run init`, pointing you at
  a file it had shredded itself, and refusing _before_ the merge meant re-running could not rebuild
  it. In a worktree it was quieter and worse — nothing re-reads that copy, so the session started
  against unparseable settings, the CLI fell back to its defaults, the Stop hook was never
  registered, and the run idled to timeout with nothing naming the cause.

  Three of the seven are **put-backs**: they restore a file _after_ something has already failed,
  which is the worst possible moment for a second loss. One of them, the engine's restore of a park
  record after a failed commit, now journals its own failure as `park-record-rollback-failed`
  rather than dropping it. Nothing else would ever surface that — `validate` reports a board parked
  with no record, but never a record left over for a park that is in no commit.

- **Four writers under `.riaworks-waves/loop/` no longer strand an untracked temp when their replace fails
  (#363).** Each built a fixed-name temp and then `os.replace`d it, and `atomic_replace` does no
  cleanup of its own. No ignore rule covers those names — `init` writes `.riaworks-waves/loop/runs/`,
  `.riaworks-waves/loop/cache/`, `.riaworks-waves/loop/policy.toml` and `_bmad/render/` — so a failed replace left an
  untracked file holding `verify.worktree_clean` False until a human deleted it by hand.

  - Three route through the helpers, which name the temp uniquely per write and remove it on any
    raise: the pre-answer store (`.riaworks-waves/loop/decisions.json`), `policy.toml`'s `[mux] backend`
    writer, and the TUI settings editor's save. The last two built the _same_
    `.riaworks-waves/loop/policy.toml.tmp` path, so they could also collide with each other.
  - `archive_run` keeps writing its own tarball — the path goes to `tarfile.open`, so there is no
    payload for a helper to take — and gains the unlink-on-raise guard instead. Its temp was also
    misnamed: `with_suffix` replaces only the last suffix, so `<id>.tar.gz` yielded
    `<id>.tar.tar.gz.tmp`. It is now `<id>.tar.gz.tmp`.

  Under a monorepo `repo_root:` override this surfaces as a failing `validate` and TUI rather than
  a blocked `run`: `run` and `sweep` probe the repo root, `validate` and the TUI probe the project.

  Five more temp-and-replace writers took the same helper without having been exposed: the sweep's
  two `decisions.json` writes, whose file is the per-run one under the gitignored
  `.riaworks-waves/loop/runs/<id>/` and not the project-level store named above; the two park-record writers
  behind `riaworks-waves-loop confirm` and `drop`, which already carried a hand-rolled guard; and
  `devcontract`'s spec writer. All five gain the fsync before the replace and a unique temp name in
  place of a fixed `.tmp` sibling that two concurrent writers would collide on.

  **Scope, for both entries above.** This closes the _raise_ path, and only that. The helpers stage
  at `mkstemp(dir=target.parent, suffix=".tmp")`, so a `SIGKILL` mid-write still strands a temp
  that `worktree_clean` reads as dirty; and on Windows `os.replace` is
  `MoveFileEx(MOVEFILE_REPLACE_EXISTING)`, which is not guaranteed atomic and may fall back to a
  non-atomic copy. What holds everywhere is that a failed write cannot truncate the original.

- **An atomic write no longer fails on a file whose name fills the filesystem's limit (#595).** The
  helpers stage a temp named after their target, and `mkstemp` inserts eight random characters, so
  the temp ran `len(name) + 13` — long enough that a target with a perfectly legal name produced an
  illegal _temp_ name and the write died with `ENAMETOOLONG` — or, on Windows, with `ENOENT`
  carrying `winerror` 206, which is the same condition under a different name. On ext4 the cutoff
  was a 243-byte basename.
  Latent in the helpers since they were written, and reachable from this release because the story
  spec writers moved onto them: a spec is named by your planning skills, and nothing bounds that
  name. When the readable temp name cannot fit, the helpers now fall back to a short digest of it
  rather than failing — the OS decides, so there is no guess at a per-filesystem byte limit.

- **A best-effort diagnostic write no longer takes the run down, and POSIX tmux captures no longer
  raise on an undecodable byte (#380).** Both halves are one defect: an exception net that names one
  direction of the Unicode hierarchy while the other escapes it. `_append_diag_jsonl` serializes
  with `ensure_ascii=False` and writes through a UTF-8 handle, so a story spec whose filename holds
  a byte the filesystem codec could not decode arrived surrogate-escaped and failed at the encode
  with `UnicodeEncodeError` — a `UnicodeError`, so a `ValueError`, not an `OSError` — straight past
  a guard whose stated contract is that an unwritable run dir must never break the completion loop.
  The guard is now `(OSError, UnicodeError)` and the breadcrumb is dropped instead of crashing the
  run. Separately and visibly: `tmux_base`'s `_ERRORS` was the strict handler on POSIX while the
  Windows backend already set `"backslashreplace"`, so a capture holding such a byte raised out of
  the one place tmux is spawned; it now comes back with that byte rendered as a `\xNN` escape, and a
  session name or window title carrying one reads back escaped. Fixing the decode at its source
  rather than at the fourteen catch sites is deliberate — most of them return a sentinel, so
  catching there would have converted a crash into a wrong answer (`[]` reads as "window dead").
  `_ENCODING` stays `None`, so POSIX keeps the locale codec and only stops being strict. This closes
  the diagnostic writer and the capture decode; it does not sweep the wider `except`-tuple family.

- **A plugin hook or version probe whose child emits a non-UTF-8 byte no longer crashes the run
  (#383).** `subprocess.run(..., text=True)` decodes with the locale codec at `errors="strict"`, and
  the `UnicodeDecodeError` that raises is neither an `OSError` nor a `SubprocessError`, so it
  escaped both captures' guards. The declarative-hook transport is the run-crashing half: `_HookError`
  is the bus's designed channel for "the hook could not run to completion", and the decode happens
  after the child has exited — so a hook that actually **passed** took its exit code down with the
  run instead of being classified. `probe.run_version_help` documents "Never raises", and a
  `--version`/`--help` banner carrying such a byte made that false. Both now decode with
  `errors="replace"`, so the hook's verdict survives and a fault is classified through the normal
  channel. Visible change: those bytes now show as `�` (U+FFFD) in journal entries, hook advisory
  text and probe documents. The `except` tuples are deliberately not widened — the fix is to stop
  raising, and a widened tuple would guard a fault nothing could ablate into existence.

- **A session whose log merely writes _about_ a provider error no longer pauses the run (#507).**
  `claude` shipped one pattern joining a framing token to a cause across an unbounded `.*`, and this
  adapter scans a tmux pane capture — the model's own output — so any line mentioning both halves
  classified. 44 of this repo's own tracked lines did, most of them ordinary pytest/grep/diff output.
  The harm ran the other way: a **genuine** timeout was read as an environment fault, re-arming the
  budget and halting the run for an operator instead of charging the attempt. The three replacements
  reproduce only complete error sentences Claude Code was captured printing, 5xx statuses enumerated
  rather than ranged. A standing guard walks `git ls-files` and asserts no tracked line classifies —
  write the framing token and a cause separated (`API Error` … `<cause>`) in future entries.

- **A mid-response connection drop or a provider 5xx refusal on the `claude` adapter now pauses the
  run with the matched evidence (#323).** The withdrawn connection-only pattern caught 2 of the 5
  captured Claude Code failure lines, so a session killed by either of those three misses was charged
  a dev attempt, and `max_dev_attempts` of them deferred a story whose spec and code were fine. All
  five classify now, and the pause re-arms the budget instead of spending it. A subscription
  usage-limit / quota refusal is still **not** classified on this adapter: no captured Claude Code
  quota line exists to seed a pattern from, and on a pane capture that vocabulary is what a story
  _implementing_ rate limiting prints all day — follow-up: #610. The four unseeded profiles
  (`codex`, `gemini`, `copilot`, `antigravity`) are unchanged and still ship none.

- **An out-of-tree module that claims a bundled transport's name is no longer driven in the bundled
  backend's place (#565).** Backend selection breaks ties on registration order, and the bundled
  `tmux` / `psmux` entries were seeded only on the first multiplexer resolution — so any
  registration that landed before it owned that name, and the whole process silently ran on a
  third-party transport. The trigger is reachable rather than theoretical: a plugin's `[python]`
  module is executed in-process by the plugin registry, which has no ordering relationship to when
  the mux is first resolved. Registering a backend now seeds the bundled ones first, making
  builtins-first an invariant of the registration itself rather than a property of which import ran
  first — the same fix the adapter registry already carries. A shadowing external is still
  registered, just behind the bundled entry.

- **Two broken distributions that publish the same entry-point name no longer collapse to a single
  recorded error (#566).** `importlib.metadata` does not deduplicate entry points across
  distributions, and all three external-load scans — adapters, profiles and mux backends — recorded
  failures by assignment into a name-keyed map, so the second failing package overwrote the first.
  You fixed the one failure you were shown, then met the other on the next run with nothing saying
  it had ever been there. Both reasons now surface, and every recorded external-load failure names
  its **distribution** when one is resolvable — in `riaworks-waves-loop adapters`, `riaworks-waves-loop mux`,
  `validate`'s human output and `validate --json` — because the entry-point name is not the
  distribution you uninstall.

  The limit, plainly: two failing same-named distributions still produce **one** finding and one
  warning line, whose text now carries both reasons `"; "`-joined. The row count does not double.
  That is what keeps the change contract-preserving — `detail`'s key set and value types are
  unchanged, so `VALIDATE_SCHEMA_VERSION` stays 1.

  **A deliberate scope addition:** the multiplexer's entry-point scan is now ordered by (name,
  distribution), as the adapter and profile scans already were, so which of two same-named
  distributions is recorded first is a fact about the packages rather than about `sys.path`.

- **A run launch whose adapter class rejects a bootstrap keyword now aborts on a clean `error:`
  line instead of a bare traceback (#569).** The construct call converted only the failures an
  adapter family declares, and a signature mismatch is refused by the interpreter rather than by
  the family — so an out-of-tree class whose `__init__` does not accept a keyword the bootstrap
  passes escaped uncaught. The abort now names the profile, the adapter kind and the rejected
  keyword; the exit code is unchanged at 1. Deliberately unchanged: a `TypeError` raised from
  inside a working `__init__` still surfaces as itself, because that is a bug in that package
  rather than a declared failure, and relabelling it as a signature mismatch would bury it. This is
  message quality only — an error escaping here already unwound the composition it had started.

- **A modal dialog on a terminal narrower than its declared width now shrinks to fit instead of
  being clipped, so its action buttons stay reachable (#281).** The docked button row is
  right-aligned, so the buttons were exactly what fell off the right edge — the horizontal twin of
  the vertical defect #275/#280 fixed. `EscalationModal` needed 87 columns, so a standard
  80-column terminal already clipped it outright; `DecisionModal` needed 83 and the bounded
  confirms 61. Below 60 columns those buttons additionally render smaller and tighter, because
  clamping the dialog alone still leaves a three-button row demanding 54 columns inside a content
  region narrower than that.

  On the other axis, below 20 rows a dialog now renders in a compact layout — collapsed padding,
  no title margin, a one-row button row — rather than clipping its docked buttons and safety
  warnings. `docs/tui-guide.md` accordingly records the terminal sizes these dialogs were measured
  at — **39 columns × 9 rows** for a dialog's own chrome — stated as sizes measured to be
  sufficient rather than as a supported minimum, and scoped to the dialogs, not the dashboard
  behind them. `EscalationModal` sets that figure and it is width-dependent, its docked warning
  wrapping to 9 rows at 39 columns but 6 at 80. Titles, headers and paths dock outside the
  scrolling body, so a long enough one wraps and costs rows the body cannot give back: a
  ~300-character deferred-work heading clips the close button, the validate viewer grows with its
  document's spec folder (#629), and the spec viewer's `copy path` button plus its action verbs
  simply do not fit 39 columns (#628). Nothing bounds that caller-supplied text, so no fixed size
  is a minimum these dialogs will always meet; a standard 80 × 24 terminal absorbed every measured
  example and the guide quotes it on those terms. At 60 columns and 20 rows and above the full
  chrome renders exactly as it does today.

- **A deferred-work bundle whose name or key ends in a newline is now rejected instead of becoming a
  directory (#330).** Both sweep regexes anchored with `$`, which in Python also matches just before
  a single trailing newline, and every call site uses `.match()`. So a bundle named `fix-it\n`
  validated clean and was used unsanitized as both the `run_dir/bundles/<name>/` path segment —
  invalid on native Windows — and the `dw-<name>` story key, while a key of `dw-foo\n` silently
  rebuilt a degraded bundle's intent under the different directory `foo`. Both patterns now anchor
  with `\Z`. Only a name or key ending in exactly one bare LF flips to rejected; `\r\n`, `\n\n`, a
  bare `\r`, a trailing space and any interior newline already were. A cached triage carrying such a
  name now re-runs instead of crashing, and a pre-fix run-state task keyed that way becomes inert
  rather than re-driven under a silently different name. Sweep-scoped: a bundle name is still not
  guaranteed safe as a path segment.

## [0.10.0] — 2026-08-14

Much of this section is the `release/0.9.x` hotfix line brought forward onto `main` (#433).
**Upgrading from 0.9.1, you already have those fixes** — the entries below re-state them for `main`,
whose seams had diverged enough that several ports needed a different fix, and they close holes
0.9.1 left open. `main` has not been released since 0.9.0 and does not descend from v0.9.1.

### Added

- **Hook events move out of the project tree (#494).** A run's session-completion signals now land
  under a user-scoped state root — `$XDG_STATE_HOME/bmad-loop`, `%LOCALAPPDATA%\bmad-loop\state`, or
  an absolute `BMAD_LOOP_STATE_DIR` — so a branch switch, a worktree mount or a rollback can no
  longer take a live run's control plane away. Relays predating the move keep working through an
  in-tree fallback until you re-run `bmad-loop init`; `validate` flags a stale one as
  `hooks.relay-stale`, and `delete`/`archive`/`clean` collect the new directory with the run
  (`clean --json` gains `state_dirs_swept`).

- **`bmad-loop relay <Event>` records a session event without the copied-in script (#494).** It
  keeps the script's contract: nothing on stdout, rc 0 always, a silent no-op outside a driven
  session. `init` does not point hooks at it yet, so no run behaves differently today.

- **A coding-CLI adapter class can ship out-of-tree (#226).** A profile's new `adapter` field names
  a kind resolved against the adapter registry, so a co-installed package can register its own
  driving class — and the profile that selects it — with no core edit, as the transport axis has
  long allowed. `bmad-loop adapters` lists the registered kinds and the profiles selecting them,
  `validate` gains `adapter.kind` and `adapter.external` reports, and a broken third-party package
  degrades to a surfaced reason instead of breaking selection.

- **A deferred-work entry can block stories from running: `gate:`.** A `gate: 3-2, 3-3` line names
  the story keys that must wait for the entry, and both `validate` (`deferred.hard-gate`) and `run`
  (a `story-gate` pause) enforce it — the prose `HARD GATE:` convention stopped nothing. Closing the
  entry or dropping the token clears it, sweeps are exempt because a sweep is what closes the entry,
  and a gate that can enforce nothing warns as `deferred.hard-gate-unstructured`.

- **Deferred review findings are harvested from spec frontmatter (#433).** A successful dev, review,
  repair or review-timeout-salvage pass files each item from the spec's `deferred:` list into the
  ledger as `### DW-<n>`, so findings triaged as `defer` reach the sweep instead of stopping at the
  spec. Retries and replays never re-file, malformed items collapse into one `severity: low` entry,
  and a spec outside the orchestrator's roots is refused.

- **A park record travels with its story's commit (#356).** Each parked story writes
  `.bmad-loop/operator/<key>.json` inside the story's own commit window, so `bmad-loop confirm`
  works from any clone; the machine-local `operator-actions.json` index is retired — still read and
  pruned, never written. `validate` reports a park with no record as `operator.park-record-missing`;
  pull the park commit's branch if that is what you are missing.

- **Stories can park at `awaiting-operator`, and `bmad-loop confirm` completes them (#335).** A dev
  session whose story needs an action only a human can take outside the repo — publish a DNS record,
  grant an API key — now commits everything an agent can do, records what is owed in the spec's
  `operator_actions:` frontmatter, and parks so the run moves on, in place of a dishonest `done` or
  a run-halting `blocked`. Once you have carried the external work out, `bmad-loop confirm
<story-key>` walks the actions (`--yes` skips the prompts, `--reverify` re-runs `[verify]` first
  and blocks on failure, `--list`/`--json` show what is parked), advances the spec and board to
  `done` and commits the pair; `[operator] enabled = false` reverts. Run state carrying the new
  phase is forward-only — an older bmad-loop rejects it.

- **Defer notifications name the branch where the work survives (#333).** A deferred story's
  rollback parks the attempt on `attempt-preserve/*`, but the ref only ever reached `journal.jsonl`,
  leaving you to hunt with `git log --all`; the notice now names the ref and the
  `git merge --ff-only` that restores it. New `preserve_ref` on each task is projected into `status`
  and `--json` (additive; schema stays 1).

- **Stories can close deferred-work entries (#234).** `closes_deferred: [DW-5, DW-6]` on a
  `stories.yaml` entry or in a spec's frontmatter flips each named entry to `status: done` with a
  `resolution:` naming the story, at the story's commit. Advisory: a failed or escalated story
  closes nothing, bad ids only warn and `validate` reports them up front
  (`deferred.closes-unknown`), and no upstream skill emits the field yet (BMAD-METHOD#2619).

- **Readable run logs for `opencode-http` (#306).** Contributed by
  [@jackmcintyre](https://github.com/jackmcintyre). The HTTP adapter has no tmux pane to replay, so
  a finished run left `logs/<task-id>.log` holding nothing but the server's own INFO stdout; the SSE
  stream now also yields a curated role-prefixed transcript, a `<task-id>.server.out` and a raw
  `<task-id>.sse.jsonl` trace.

- **`review.on_timeout` policy knob (#271).** A timeout-like review verdict (`timeout`, `stalled`,
  `over_budget`) burned every review cycle before deferring, even when the dev product was already
  finalized and verify-green. Beside the default `"retry"`, `"salvage-if-done"` commits the verified
  product and refiles the outstanding recommendation to deferred work, and `"defer"` gives up on the
  first such verdict.

- **Transport failures pause the run instead of burning attempts (#194).** A session whose CLI lost
  its API connection stayed alive but idle until the session clock ran out, so two outages could
  exhaust `max_dev_attempts` and defer a story untouched. Adapters classify it from per-profile
  `env_fault_patterns` and pause like an `rc 126/127` verify fault; re-arming restores the budget.

- **Raw psmux premise probes (#488).** The zero-token Windows live gate now flags the workarounds a
  current psmux no longer needs, so they can be dropped on evidence rather than kept on suspicion.
- **Documented the `RIAWORKS_BMAD_LOOP_*` environment variables (#246).** The three runtime override vars —
  `RIAWORKS_BMAD_LOOP_MUX_BACKEND`, `RIAWORKS_BMAD_LOOP_PROCESS_HOST`, `RIAWORKS_BMAD_LOOP_SESSION_TIMEOUT_S` — now have a
  reference table in the README, and are read through one `bmad_loop.envvars` registry so the
  supported knobs are discoverable in one place. Behavior is unchanged.

- **`python -m bmad_loop` (#240).** The package is runnable as a module, mirroring the installed
  `bmad-loop` console script.

- **`{story_title}` in `scm.commit_message_template` (#475).** The placeholder renders the spec's
  `title:` frontmatter minus any leading `Story <id>:` label, so a commit subject can carry a
  readable title. It never renders empty and never fails a commit — a spec that is missing,
  unreadable or lacks the field falls back to a first `#` heading and then to the story key, and
  characters `git commit -m` cannot take in an argv are dropped.

### Changed

- **Docs state the deferred-work contract of the 6.11 era (#567).** The sweep's format doc,
  FEATURES.md, the setup guide and the module skills now name `bmad-build-auto` and describe the
  spec-frontmatter harvest it uses, keeping the legacy spelling only where a pre-rename install
  still needs it. Prose only, no behavior change.

- **docs/testing.md states the testing strategy.** Layer taxonomy and placement rules, fixture and
  ablation doctrine, the quality-guard inventory, and the zero-token and flake policy; AGENTS.md,
  docs/README.md and CONTRIBUTING.md link to it.

- **The `BMAD_LOOP_*` environment variables are documented and centrally registered (#246).** The
  three runtime override vars — `BMAD_LOOP_MUX_BACKEND`, `BMAD_LOOP_PROCESS_HOST`,
  `BMAD_LOOP_SESSION_TIMEOUT_S` — now have a reference table in the README and are read through one
  registry, so the supported knobs are discoverable in one place. Behavior is unchanged.

- **The supported tmux floor is 3.2.** It was never written down, so the only floor a reader could
  infer was whatever the argv grammar happens to accept — older than anything the project tests. No
  version gate gets added: an older tmux is not refused up front, it is simply unsupported.

- **The mid-run config pin covers the adapter kind (#461).** `adapter` selects which argv builder
  runs at all, so it joins the `config_digest` launch payload — a driven session that rewrites it
  now moves the pin the auto-triggered child sweep gates on, instead of swapping the whole launch
  shape underneath it.

- **`validate`'s httpx and model-format checks key on the adapter kind, not hooklessness (#226).**
  Both are facts about the `opencode-http` class rather than about whether a profile registers
  hooks, so a hookless profile driven by another kind no longer FAILs with a remedy that installs
  the wrong package, nor warns about a naming convention it does not use. An `opencode-http` profile
  carrying a hook dialect now gets the model warning it always needed.

- **A hookless profile can no longer wait out the clock on the `generic` adapter (#226).** `generic`
  completes on a Stop hook that `hooks.dialect = "none"` never registers, so both routes into the
  profile map refuse the pair outright rather than passing `validate` and then idling until
  `session_timeout_min`. A pre-`adapter` overlay copied from the packaged opencode profile resolves
  to `opencode-http` instead of that dead pairing; an explicit `adapter` is always honored, and
  hookless on any other kind stays legal.

- **Profiles from a `bmad_loop.profiles` entry point are validated like TOML ones (#226).** Both
  routes share one invariant set — hook dialect, path containment, `env_fault_patterns` compilation,
  canonical `name`/`binary`/`adapter` — so a package can no longer install a profile state the TOML
  parser would refuse, such as an invalid env-fault regex that trades a load-time error for a silent
  never-match at classification time.

- **An unreadable deferred-work ledger fails `validate` rather than warning.** The `gate:` hard gate
  rides on the same bytes, so `deferred.ledger-unreadable` as a warning exited 0 with the gate never
  evaluated — a fail-open on the one deferred check that refuses. `run` pauses on the same fault, so
  preflight and dispatch now agree.

- **Every spec-frontmatter status read goes through `status_of` (#358 follow-up).** Five inline
  reads remained in the engine and the generic adapter, each taking a blank `status:` as the token
  `none`. One behavior change falls out: a session that erases a previously-set status no longer
  records a transition, because a blank is not an observed live status.

- **The story token budget is checked while the story runs (#336).** `max_tokens_per_story` was read
  once, after the story was marked done, so an overrun surfaced only after every token was spent and
  a story that deferred or escalated went unchecked. Cumulative weighted spend is now re-checked at
  every session boundary, raising one ATTENTION plus a desktop notice, latched per story; still
  advisory — `limits.max_tokens_per_session` remains the session-ending cap.

- **A failed snapshot blocks the rollback reset (#340).** An auto-rollback refused to reset past
  commits it could not park, yet journaled a failed _uncommitted_-work snapshot and reset anyway,
  destroying the tracked edits and run-created files that snapshot existed to capture. Both preserve
  steps now refuse alike, pausing with rescue instructions naming the tree; inert under shipped
  defaults, this bites `scm.rollback_on_failure = true` and in-worktree retries.

- **A review that revokes the sprint sign-off escalates (#334).** `sprint-status` is advanced to
  `done` at dev time, so a review session writing it back left the remaining cycles re-reading the
  same failure until the story deferred and its work rolled back. The review-verify gate now pauses
  with the two ways out — finish and re-arm, or accept and advance the board — under a new
  `[review] on_status_contradiction` (default `escalate`; `retry` restores the old behavior).

- **`bmad-loop-setup` stops registering BMAD config; the installer owns it (#258).** The skill wrote
  the pre-v6.10 `_bmad/config.yaml` layout that BMAD's own resolver never reads, and since v6.10.0
  the installer stages the module and regenerates `config.toml` wholesale, discarding outside
  writes. Its PEP 723 scripts go with it, closing the bare-`python3` bug (#259); setup now writes
  one help CSV, installs the tool and preflights.

- **Ctrl+C outside a run exits `130` cleanly (#241).** A `KeyboardInterrupt` escaping `main()`
  during config load or engine construction now prints a one-line `interrupted` to stderr and
  returns the new `ExitCode.INTERRUPTED`, in place of a bare traceback dumped after any partial
  `--json` stdout. The shell exit code is unchanged, but a Python caller's `subprocess.returncode`
  now reads `130` rather than `-2`; Ctrl+C _during_ a run is unaffected.

### Removed

- **The `bmad-auto` → `bmad-loop` rename shims are gone.** The rename shipped in 0.8.0 and no
  pre-rename installs remain in the wild, so `init` no longer strips `bmad_auto`-marked hooks,
  deletes `bmad-auto-*` skill dirs, carries `.automator/policy.toml` over to `.bmad-loop/`, or
  prints the leftover-`.automator/` note, and `bmad-loop-setup` drops its migration section. A
  project still on `bmad-auto` should migrate on 0.9.1 — the last release carrying the shims —
  before upgrading past it.

### Fixed

- **The settings editor's `review.trigger` help no longer names a dev primitive that may be absent.**
  Its `recommended` blurb said "only when bmad-dev-auto flags it", a name upstream retired in BMAD
  6.10.1 but still correct on the 6.10.0 support floor — either spelling is wrong for the other era.
  It now says "the dev pass", matching the adjacent `review.enabled` description and the
  `docs/tui-guide.md` table it mirrors; the `policy.toml` template `init` writes got the same fix.

- **The `version-sync` gate no longer passes on a marketplace.json it could not read.**
  `sync_version.check()` iterated `market.get("plugins", [])`, so a renamed, deleted or emptied
  `plugins` key made the loop run zero times and the gate print "ok: every version field agrees"
  — green on exactly the corruption it exists to catch, including when a real stale version sat
  behind the renamed key. It now refuses a `plugins` value that is not a non-empty list, and
  reports a non-object entry instead of raising. Covered by a new `tests/test_sync_version.py`.

- **`trunk check` is documented as the changed-files check it is.** `AGENTS.md` and
  `CONTRIBUTING.md` both called it "full lint, no path filter", but bare `trunk check` lints only
  files changed against the upstream — 7 of 254 on the branch that fixed this — and CI's
  `trunk-action` defaults the same way. `--all` is the whole-repo run, and both files now say so.
  `CONTRIBUTING.md` also no longer claims `release.py check` rejects a hand-authored version
  section (it returns 0 on one), tells maintainers that `prepare` refuses until they promote the
  CHANGELOG by hand, and stops presenting three commands as the complete set of CI gates.

- **Contributor docs now name every obligation CI enforces.** `CONTRIBUTING.md` never mentioned
  `pyright` or the CHANGELOG, so its verify step — "`trunk check` and `uv run pytest -q` both
  pass" — sent contributors into a CI failure on the dedicated typecheck job. It now carries
  `uv run pyright`, the `## [Unreleased]` CHANGELOG contract, the Windows `PYTHONUTF8=1`
  requirement and the Python 3.11 floor, the real extras (`tui`, `non-linux`, `opencode` — it
  claimed only `tui`), and `scripts/release.py`'s two-phase `prepare`/`publish` flow. The pull
  request template gains a matching Changelog section, as does CONTRIBUTING's copy of it.

- **The docs no longer describe a state the code has left behind.** The README's command table
  gained `bmad-loop adapters`, and its docs list gained five missing guides plus `docs/README.md`,
  the full index. `docs/FEATURES.md` now covers all 15 policy sections rather than 12 — `[dev]` was
  documented nowhere. The roadmap's native-Windows entry read `planned` while its own body said
  psmux had shipped, and `AGENTS.md` counted `~25` leaf modules where there are 28.

- **A failed ledger write can no longer empty the deferred-work ledger (#328).** Every write built
  its replacement in place, so an unencodable value, `ENOSPC` or `EIO` partway through left a
  zero-byte ledger with every entry gone. Writes are now atomic — a failure raises with the original
  untouched — and a ledger created from nothing lands `0600` rather than at the umask default.

- **A lone surrogate in triage text no longer crashes the sweep (#329).** A code point with no UTF-8
  encoding at all could reach the ledger through a cached triage result and take down a close path
  that had no guard. Every free-text ledger field and the whole of a bundle's `intent.md` now
  neutralize such characters to `�`, so the text stays visible instead of ending the sweep.

- **A `#` inside a quoted sprint-status value is no longer rewritten into a comment (#366).**
  Advancing `3-2-x: "a # b"` produced `3-2-x: done # b"`, promoting scalar text into a comment the
  board never had. A quote-led value is now taken whole with no comment recognized inside it;
  unquoted values keep the wide class this board needs and still cede the first whitespace-preceded
  `#` as authored.

- **A gitignored sprint board no longer crashes a worktree-isolated run (#350).** A worktree checks
  out tracked files only, so the board the orchestrator advances was simply absent: the advance
  no-opped in silence and the run then died on the same missing file. The board is now seeded into
  the worktree and the story's advance re-applied to the main checkout after the merge — journaled
  `board-advance-carried`, or `board-advance-carry-uncommitted` where git refuses the ignored path
  (the ordinary outcome for such a board), or `board-advance-carry-failed` where the main row never
  reached the target. Without that carry the next run reads the main board and hands you the
  finished story again. Tracked boards are unaffected.

- **`confirm` no longer loses its commit to a gitignored board (#577).** Confirming a park on such a
  board printed `✓ confirmed` while the spec's flip to `done` and the park record's deletion stayed
  uncommitted, dirtying the tree the next run's preflight refuses. The board is now left out of that
  commit when git will not take it — a force-tracked board still commits — and is advanced on disk
  either way.

- **`resume`'s config-change baseline moves out of the agent-writable tree (#498).** The baseline
  `resume` compares against — verify commands, launch binary/args/env, plugin allowlist —
  round-tripped through `state.json`, inside the very tree the digest exists to police, so a session
  that rewrote `policy.toml` could blank the field in the same breath and the warning never fired.
  It now lives in the run's out-of-tree state dir (#494) and is collected by the same
  `delete`/`archive`/`clean` lifecycle; `state.json` keeps a copy consulted **only** when no
  out-of-tree file exists, which covers a run paused under an older version and a project that has
  been moved or renamed (#572). This closes the _incidental_ path only — sessions launch with
  permission bypass by default and are handed the state dir's location, so a deliberate one can
  still silence the warning; closing that needs privilege separation, tracked in #571.

- **Worktree runs no longer stall when a seeded hook config carries the main repo's relay (#352).**
  The seeded `.claude/settings.json` arrived naming a relay path that resolves inside the worktree,
  where none exists, so the session emitted no hook events and idled out the session clock. Relay
  entries are now stripped from the seeded config before merging, and a project that _tracks_ its
  hook config gets the same rewrite pinned `skip-worktree` so the machine-specific command never
  folds into a story commit — while pinned, the config is orchestrator-owned and a story's own edit
  to it stays session-local.

- **`cleanup` no longer reports a surviving ctl window as removed (#435).** Killing a window reports
  nothing, so the prune counted every _attempted_ kill as a removal. It now verifies with one
  liveness listing and partitions into `removed` / `survived` / `unverifiable`, so
  `CLEANUP_SCHEMA_VERSION` is **2** and text mode names the two non-removed arms on stderr. A
  candidate scan that fails outright reports `ctl_windows.scan_error` with empty arms, so a
  preflight failure is never the same document as "nothing to prune"; `sessions.removed` is
  untouched and still an attempted kill.

- **A crashed version probe is distinguishable from "reports no version" (#428).** A binary on
  `PATH` that dies answering `-V` — corrupt install, AV-blocked exe, hung server — collapsed to the
  same answer a quiet binary gives, and its stderr was gone. `bmad-loop mux` now prints the dropped
  diagnostic as a `warning:` line on stderr below the table, since the `-` in the VERSION column
  cannot say which of the two happened.

- **A project path the OS refuses to canonicalize no longer kills every command (#552).** On a
  Windows host whose WSL UNC provider is registered but not serving, resolving `\\wsl$\<distro>\...`
  fails outright — and that resolve runs before dispatch, so every subcommand died at the backstop,
  `diagnose` and `validate` included: the `host.win32-on-wsl-path` warning naming the fault was
  unreachable on the only hosts it is for. Those commands now degrade to an absolute path with one
  note on stderr and run. Config loading refuses instead, with a typed error every caller already
  handles: a degraded root beside a canonically spelled artifact path mis-files an in-tree directory
  as external and sends a worktree-isolated run's writes into the original checkout. The paths that
  need a canonical answer downstream — run tagging, worktree provisioning, verify — still raise, so
  nothing tags one project two ways.

- **`BMAD_LOOP_SESSION_TIMEOUT_S=inf` no longer disables the session timeout.** The guard rejected a
  non-positive value but let `inf`, `1e999` and `Infinity` through, producing a deadline that could
  never expire — and that budget is the outer bound every stall-grace and wake-nudge window defers
  to, so an unattended run could wedge with no backstop left. The value must now be finite and
  positive, otherwise falling back to `limits.session_timeout_min` as it already did for `0` and
  unparseable input. A large _finite_ value is still honoured.

- **A tab in the project path no longer truncates the project tag a window listing carries.** The
  multiplexer listing is tab-delimited and the tag holds a resolved filesystem path, where a tab is
  a legal byte — so the tag came back truncated and read as another project's, and the prune scan
  then skipped the project's own parked control windows. The last requested field now keeps its
  delimiters.

- **Removing a run directory no longer strands a session that outlived its engine (#526).**
  `delete`, `archive` and `clean` gated on engine-pid liveness, which an orphan — engine dead, agent
  session still alive — passes; for an untagged session the run dir is the last ownership proof a
  prune can read, so removing it leaked the session for the life of the machine. Removal now refuses
  while a `bmad-loop-<run-id>` session the project cannot prove foreign is live, and `clean` leaves
  the run untouched; `--force` overrides the refusal and kills nothing, since a session name carries
  no project.

- **A project path the multiplexer cannot carry no longer strands the scans over it (#419).** The
  ownership tag held the resolved path, which psmux's control line refuses when it names a spaced
  UNC share and which a listing row can split on an exotic separator or fail to decode — either way
  the session or window went untagged, leaking once `clean` removed its run dir and prunable by
  another project on a reused `--run-id`. The tag is now a 16-hex digest of the path, safe on both
  transports by construction; pruning still accepts the legacy path tag, so state surviving the
  upgrade keeps its ownership; reading a legacy raw tag is the decode half (#380).

- **A run id that is a suffix of another no longer resolves to the neighbour's control window.**
  `--run-id` is caller-supplied and may contain `-`, so `run-other-RID` satisfied the lookup for
  `RID` and sorted ahead of it — `bmad-loop x` could kill the neighbouring run's live orchestrator.
  Window names are now parsed and the run id compared whole, as the prune scan already did.

- **Attach, return-stamp and kill follow the run's live control window, not an older one (#482).**
  Window names are not unique, so the lookup answered the first match: `a`, the return stamp and `x`
  all landed on a parked run's dead window while the live one ran on. Each launch now records the
  window id it minted and the lookup prefers it, and a resume whose id was not captured warns rather
  than reporting plain success. **Adapter authors:** the re-prove pairs `new_parked_window`'s id
  with the `window_id` column of `list_windows`, which the seam previously left free to diverge — a
  backend where they differ degrades to the by-name resolve.

- **Diagnose a lost multiplexer session on the crash path (#489).** A dead window and a session
  destroyed under the run — a reaper, this tool's own prune, an operator `kill-session`, a server
  crash — both scored `crashed` and read as an agent fault. A crash verdict now probes for the
  session and carries `session_vanished` in the failure reason, on every role's `session-end` entry
  and as a `session-vanished` breadcrumb, composed with an environment-fault pause. It also reaches
  the repair path's exhaustion defer, which otherwise blamed the tree for repairs that never ran.
  Diagnosis only: routing is unchanged and a retry re-creates the session.

- **A native-Windows install driven from a WSL shell now says so (#332).** WSL appends the Windows
  `PATH` to its own, so a bash prompt can reach a Windows-installed `bmad-loop`: that interpreter
  reports `win32`, takes the psmux platform default, and never sees the distro's tmux — while
  `validate` printed a green `multiplexer PsmuxMultiplexer available` and nothing named the platform.
  `validate` now reports the multiplexer selection reason for **every** host (it was emitted only for
  a forced `RIAWORKS_BMAD_LOOP_MUX_BACKEND`/`[mux] backend` choice), so `platform default for win32` is on
  screen wherever the mismatch happens; the same un-gating makes a `fallback` selection — no
  available backend matches this platform — a warning rather than a green line. A `win32` interpreter
  working on a `\\wsl.localhost\...` project additionally raises a `host.win32-on-wsl-path` **warning**
  naming the fix (install with the WSL/Linux Python) and the backend it actually chose. That warning
  covers the project-on-the-distro shape only; a project under `/mnt/c` gets a genuine Windows path
  and no warning, and is covered by the selection line instead. Nothing changes which backend is
  selected — psmux is correct for a `win32` interpreter — nor validate's exit code. `diagnose` gains
  `sys.platform` and `win32 on WSL distro path` (`yes`/`no`) in its Environment block.

- **A multiplexer-detection failure is reported instead of swallowed (#332).** `validate` caught and
  discarded any exception from backend detection, so the selection and the backend inventory
  vanished with nothing said — while the healthy-looking `mux.backend` line above them, which comes
  from an independent call, still printed. It now reports under `mux.backends-detected` at
  **warning**, carrying the error.

- **Provider quota refusals are environment faults on `opencode-http` too (#323).** #194's
  classifier lived on the generic adapter only, so its hookless HTTP sibling silently omitted it: a
  five-hour provider usage limit read as three stalled stories and burned their retry budgets. Both
  adapters now share the classifier, and the `opencode` profile seeds quota, rate-limit and
  connection patterns. Those patterns are scanned against the server's own stdout, never the curated
  transcript carrying the model's words — a pattern is only sound against a log the model cannot
  write to.

- **A re-armed escalation no longer overwrites the previous attempt's dirty snapshot (#349).** The
  preserve-ref names were keyed on the attempt counter, which re-arming resets to 0, so a
  post-resolve re-drive rolling back against the same baseline recomputed the earlier rollback's
  refname and destroyed the only copy of that attempt's work. A free name is now probed for instead,
  suffixing `-r2`, `-r3`, …; the scan is bounded and exhausting it refuses
  (`attempt-worktree-preserve-failed`, then the usual pause) rather than reusing an occupied name.
  Prune the namespace or lower `scm.preserve_keep` if it ever fires.

- **The auto-sweep child refuses config a session rewrote under the run (#461).** `policy.toml` and
  `profiles/*.toml` sit in the agent-writable workspace and reach host code execution — verify
  commands run with a shell, the resolved profile decides the launch argv and env, and
  `[plugins] enabled` gates in-process Python import. A run freezes its policy at launch, but the
  auto-triggered child sweep re-read both from disk; it is now pinned to a launch-time digest of
  those fields and refuses on a mismatch (`sweep-auto-failed` plus a notification, the parent run
  continues), while `resume` re-baselines and warns with the changed categories instead. The digest
  is field-scoped, so live-editing `[limits]` mid-run still works, and plugins are pinned by
  allowlist name only — swapping the module behind an already-enabled plugin is still uncaught
  (#496, #497).

- **The hook relay refuses a redirected `events/` dir, and `validate` stats the relay (#461).** The
  relay's event write followed a symlink — or, on Windows, a directory junction, which needs no
  elevation to create — so a driven session could redirect the orchestrator's control-plane event
  stream and stall the run to `session_timeout_min`. The write now refuses a redirected events dir,
  creates the file privately, and writes the payload in full, degrading to a no-op rather than
  failing the session. Separately, `hooks.registered` never touched the script it points at, so a
  deleted `.bmad-loop/` (a branch switch) read green while every hook event no-opped; a new
  `hooks.relay-present` finding stats the relay and says `run bmad-loop init`.

- **Dispatched sessions are told the sprint board is orchestrator-owned (#437).** The board advances
  at dev-verify time but the story commits only after the review loop, so a session dispatched in
  between opened on an uncommitted, unattributed `sprint-status.yaml` change — one review reverted
  it as a spec violation and #334 escalated a finished story. Story dev prompts, the review prompts
  of sprint and sweep runs, and every injected plugin-workflow session now carry the prohibition:
  never write the board, never revert it, and a row at `done` or `awaiting-operator` is bookkeeping
  rather than a defect to fix. Review prompts alone add the way out (`status: blocked`, for a story
  that cannot be finished without a human decision); stories mode carries none of it.

- **A seed path naming the project root is refused at load, in every source that feeds it (#456).**
  A root-naming entry made worktree provisioning resolve source to the repo root and destination to
  the worktree — both pass its containment checks — so it copied the whole project in, untracked
  files included, then recursed into its own destination. `""` was one spelling of several: `.`,
  `./`, `.\`, and on Windows `". "`, `"..."` and `"   "`, which Win32 trims to the root while
  pathlib reads them as ordinary child names. `scm.worktree_seed`, a profile's `seed_files` and
  `skill_tree`, `hooks.config_path`, a plugin manifest's seeds and its Python module, and the Unity
  seeder's scene guard now refuse every spelling. **Behavior change:** a non-string seed entry is
  rejected rather than silently coerced.

- **`init` no longer follows a config path that leaves the project (#456).** The profile and
  manifest guards are lexical, so a `skill_tree`, `hooks.config_path` or plugin module naming an
  ordinary project-relative directory passed them even when that directory linked out of the tree —
  and unlike worktree provisioning, `init` reached mkdir, rmtree and write with no re-check after
  resolution. Each now requires the target to resolve _strictly below_ the project — equality would
  admit a link back to the root — and a refused skill tree fails the install instead of being
  skipped past `init complete`.

- **A wrongly-typed field in a profile or plugin TOML is reported, not crashed on.** A TOML-legal
  value of the wrong type, an `inf`, or an oversized integer raised past every consumer's error
  handling, so the command died with one `error:` line naming neither the file nor the key. Both
  parsers now funnel at their load boundary, over a fault set closed on the nine value types TOML
  can yield. `policy.toml`'s own conversions are still raw (#474).

- **The worktree git-add shield no longer marks a project's tracked files as ignored (#392).** It
  wrote a pattern for every path it shields, including hook configs and skill trees a project tracks
  — where the pattern shields nothing, since git applies ignore rules only to untracked paths, and
  its one effect was the tracked-and-ignored state repo-hygiene gates reject, blocking the very
  story commit it was meant to protect. Such patterns are now dropped; a tracked **directory** keeps
  its pattern, since that one does hide new children.

- **An isolated codex stage no longer runs without the project's hook config (#471).** The seed list
  and the shield list came from two unreconciled sources, so a profile's hook config was seeded only
  if that profile happened to name the path twice — which claude's `seed_files` does and codex's
  does not. Every non-hookless profile's resolved `config_path` is now seeded.

- **An isolated sweep bundle can land when the deferred-work ledger is gitignored (#426).** A
  worktree checks out tracked files only, so a project that gitignores its ledger — the default —
  gave the unit none, and the bundle deferred on a fixable retry for ever. Provisioning now seeds it
  when the checkout cannot deliver one. A ledger symlinked to an untracked target is seeded to the
  wrong path and still hits this (#462).

- **Every ledger write an isolated unit makes now reaches the main checkout (#425, #458).** A damped
  review round's refiled follow-up and a story's `closes_deferred:` flips died with the unit
  worktree, because the story commit skips the gitignored ledger in silence. Both now re-file after
  the merge, journaled `review-followup-carried` / `review-followup-carry-uncommitted` and
  `story-deferred-close-carried` / `story-deferred-close-carry-uncommitted`.

- **A host lost in the merge-to-carry window replays a carry that filed no findings (#433).** The
  resume pre-pass only replayed units carrying harvested findings, so a unit whose sole ledger
  payload was a bundle's closures, a damped review follow-up or a story's `closes_deferred:` flips
  was skipped and that write stranded. Replay eligibility now names every payload the carry
  delivers, and runs before the sweep reads the open set so a replayed closure leaves it before
  triage re-bundles. An accepted state sync and an accepted repair session replay too.

- **A deferred bundle's closure is no longer carried by the resume replay (#433).** The deferral
  path deliberately re-files the harvest and withholds the closure — a defer discarded the code that
  closure claims to have resolved — but the replay carried it anyway, and since only `open` entries
  are re-bundled a wrongly `done` entry is invisible to every later sweep. The replay now mirrors
  the deferral exactly: harvest only.

- **The ledger snapshot a rollback restores from degrades loudly (#420).** A probe that cannot
  answer whether the ledger is in scope or tracked now keeps the file (`ledger-scope-probe-failed`,
  `ledger-tracked-probe-failed`), and reaching the restore unarmed records `ledger-snapshot-missing`
  instead of passing in silence. The revert is lossless either way: a spec's `deferred:` frontmatter
  is never mutated, so the next attempt re-harvests from it.

- **A worktree missing its required upstream skills now pauses instead of stalling (#433).**
  Provisioning skips a skill tree resolving outside the repo — exactly what a symlink to a shared
  machine-wide BMad install is — while the run-start preflight stats through that symlink and
  passes, so an isolated run was dispatched into a worktree holding none of its skills and every
  session stalled on `Unknown command`. Undelivered paths are journaled `worktree-seed-skipped`, and
  the engine re-probes disk before dispatch. Only the deterministic skill contract can pause a run —
  the resolved dev primitive plus the review skills this project's `customize.toml` requires;
  everything else in the catalogue is copied best-effort and can never pause a run.

- **A wheel-bundled skill that lands partially in a worktree is reported (#464).** A `bmad-loop-*`
  skill the copy could not deliver — a checkout file squatting the skill's directory refuses the
  whole subtree under per-file no-clobber — seeded nothing and said nothing. Shortfalls are now
  re-probed on disk and journaled `worktree-module-skills-dropped`: informational, never a pause,
  because these skills dispatch at the main checkout and their absence in a worktree stalls no
  session.

- **Worktree provisioning survives a filesystem it cannot fully read (#422).** A single unreadable
  file, dangling link, symlink cycle or FIFO in the repo's skill trees or seed sources ended the
  whole run with a traceback where a named, resumable escalation belonged. Every probe and copy the
  isolated seed makes is now total, on one shared walk that descends symlinked source directories
  without looping. Only provisioning degrades.

- **A worktree's hook config is never registered through a symlink (#421).** A checkout carrying its
  per-CLI settings file as a symlink out of the tree had the registration read the _outside_ file
  and write there — mutating the operator's real dotfile while the worktree, left with no Stop hook,
  never reported completion. The whole profile is now refused unless the path is inside the worktree
  with no symlinked component on the way to it.

- **A renderer stub that cannot compose its prompt now fails the preflight (#410).** A stub
  `SKILL.md` (BMAD-METHOD#2601) shells out to a renderer script; when that cannot run it writes
  `HALT: …` and the session stops with no spec — a fact about the install, so every story does the
  same. Three `problem` findings now refuse it up front: `skills.dev-renderer` for a short script
  unit, `skills.dev-renderer-config` for an absent `_bmad/config.toml`, and
  `skills.dev-renderer-sources` for a missing `workflow.md` or snapshot target.

- **Refuse `isolation = "worktree"` combined with a `repo_root` override (#414).** The pair produced
  a green preflight and then an isolated session with no dev primitive, no result, and nothing
  journaled naming the cause. `validate` now reports it; `run`, `sweep`, `resume` and the child
  sweep refuse to start; the dry-run banner names it first; the TUI toasts it ahead of its
  clean-tree gate. Making the two work together is #443.

- **A configured path carrying `[`, `*` or `?` no longer makes git act on the wrong files (#423).**
  `implementation_artifacts` reaches git verbatim out of `_bmad/bmm/config.yaml`, and git reads a
  positional operand as a _pathspec_ — so such a name always matched wider than it named: an
  unrelated sibling was staged under a story's name, a changed attempt reported CLEAN, and a
  rollback's preserve restore handed back a change the reset had just discarded. Every operand is
  now literal.

- **`diagnose` pseudonymizes the spec name, and gives one spec one alias (#433).** A journal
  record's `spec` field carries the customer's feature name, and a bare basename is
  identifier-shaped, so the scrub fallback shipped it verbatim. `spec` now has an alias namespace of
  its own and the value is reduced to its basename first — the producers disagree on shape, so
  without that one spec drew two aliases and an absolute home path landed in the local `--legend`
  file.

- **The upstream `bmad-dev-auto` → `bmad-build-auto` rename no longer breaks a project (#393).** The
  dev primitive is resolved on disk — `bmad-build-auto` preferred, a marker-complete `bmad-dev-auto`
  accepted — so `validate`, `run`, `sweep` and `resume` pass on either era with no `policy.toml`
  edit. `skills.base-shim` refuses the forwarding shim as marker-incomplete: it is a valid slash
  command, and it HALTs an unattended session on its interactive migration gate. A run mixing
  `.claude/skills` and `.agents/skills` at different eras gets the right name per role, resolved
  against the **workspace** so a run resumed into an existing worktree spells the era that worktree
  carries. Mid-upgrade, the orphaned-override warning says to **copy** the legacy
  `_bmad/custom/bmad-dev-auto.toml`, never rename it, and `--dry-run` says on stderr when its
  preview is not runnable.

- **The git-add shield no longer hides new files in your own checkout (#384).** It appended the tool
  files it writes — skill trees, hook config, seeded configs — to `.git/info/exclude`, which is
  shared with the main checkout and every sibling worktree, permanent and unversioned; projects
  legitimately track those paths, so every **new** file under them silently stopped being staged by
  `git add -A`. The shield now writes a private exclude in the worktree's own gitdir, activated by a
  worktree-scoped `core.excludesFile` that dies with `git worktree remove`.
  **Upgrading from 0.9.1 or earlier:** the lines those versions wrote are still there and upgrading
  does not remove them — open the file `git rev-parse --git-path info/exclude` names, delete the
  shield's own lines (typically the skill trees, the hook config, the `/_bmad` family and any
  `[scm] worktree_seed` path), and use `git check-ignore -v <path>` to name whatever is still
  hidden. #384 has the full account of what got written and why.

- **The shield now proves it applies, or skips with a reason (#384).** Storing the worktree-scoped
  config key proved only that the value was stored, and an inherited `!` negation below a copied
  pattern cancelled it — either way the tool files stayed stageable with nothing reported. It now
  asks git which excludes file actually resolves, re-appends past any negation, and honors an
  **explicitly empty** `core.excludesFile` as "no excludes file at all". An unreadable file, an
  unresolvable git home, a peer-accessible `core.sharedRepository` or an unanswerable probe skips
  the shield — journaled, notified.

- **Caveats for the worktree shield (#384).** It enables `extensions.worktreeConfig`, a
  **permanent** repo-format flag; it is rolled back wherever it could be left set without a working
  shield, surviving only where a sibling worktree depends on it or the rollback itself failed — the
  reason says which. It needs **git 2.20**: below that the shield is skipped and no repo-format
  change is made, since git that old refuses a repo carrying the flag. Concurrent runs serialize on
  a `.git` lock.

- **The git-add shield's git calls run on the shared chokepoint (#389).** They were the last bare
  `git` spawns outside it, so they missed its `LC_ALL=C` pin and used a hardcoded 120s timeout
  instead of the configured `[limits] git_timeout_s`. Both now apply.

- **An odd byte in a commit subject no longer crashes the TUI's story checkpoint (#390).** The modal
  read the subject with a strict locale decode, so a commit whose subject is undecodable in the
  run's codec raised mid-render and took the dialog down. It now goes through the git chokepoint and
  decodes with replacement, degrading one label instead; a stalled `git log` surfaces as a missing
  subject in seconds rather than freezing the UI.

- **A non-UTF-8 filename no longer crashes the run past every git guard (#377).** The git chokepoint
  decoded git's output strictly, and the resulting error matched neither its timeout arm nor its
  spawn arm — so it escaped untyped past every `except GitError`: the merge pre-flight, the
  stale-run reconcile at every run and sweep start, and `git diff`, whose failure bypassed the valve
  that preserves a failed unit's work. It is now a `GitError` like any other git failure.

- **One undecodable byte of verify output no longer crashes the run (#378).** Verify commands are
  arbitrary operator tools and their captured output was decoded strictly, so a child emitting bytes
  invalid in the run's encoding lost every command's result instead of classifying the failure.
  Output now decodes with replacement; the tail is display-only, while exit codes still drive
  classification.

- **A short write no longer truncates the worktree exclude (#375).** The update rewrote the file in
  place, so an `ENOSPC` or `EIO` partway through cut the operator's own excludes mid-content while
  the degrade reason still reported nothing written — and the surviving tail parses as valid
  patterns, so nothing reported the damage: cut shield lines simply stop shielding, and a cut
  landing on a path boundary widens a surviving pattern over a whole subtree. The update is now
  atomic — fully applied or untouched.

- **The exclude's git query no longer crashes on a non-UTF-8 repo path (#374).** POSIX filenames are
  bytes, so a repo path carrying bytes invalid in the locale encoding raised out of a
  documented-best-effort helper that caught neither arm of it. Git's output is now captured as bytes
  and decoded with the filesystem codec inside the guarded tail.

- **The worktree's local git exclude is best-effort now (#359).** Only its `git rev-parse` was
  guarded; the filesystem tail crashed the run on a symlink loop, a read-only `.git`, or a non-UTF-8
  exclude file or seed path. It now degrades to a journaled `worktree-exclude-degraded` reason —
  without the exclude, the unit's commit would fold the provisioned skill trees and tool configs
  into the merge. Git unqueryable at all stays a silent, expected skip.

- **A spec left with a blank `status:` is rescued again (#369).** A blank-but-present `status:` read
  as the truthy token `none`, so the prose `## Auto Run Result` fallback never fired and synthesis
  read inconsistent — and since that consistency gates the post-kill rescue (#61), a session that
  lost only its final Stop was discarded as stalled. Blank frontmatter with a prose `blocked` or
  `awaiting-operator` now gets a truthful label too; routing is unchanged.

- **A blank frontmatter `status:` reads as blank, not as the token `none` (#358).** YAML parses a
  bare `status:` line as null, which was then stringified, so every gate saw a token nothing in the
  project writes — and a half-finalized generic spec was read as carrying a deliberate custom status
  and left untouched. A YAML-null status now reads as empty, the same as a missing key, while a
  literal `status: none` stays the string; `confirm` renders `status: (blank)` and the stories-mode
  board reads `present`.

- **Spec writers no longer relay a spec's line endings (#357).** The writers read specs through a
  universal-newline translation that handed each one an all-LF copy of a CRLF spec, so a write meant
  to move one value rewrote every line ending in the file. All four now read bytes and a replaced
  line carries its own terminator, so each line keeps the ending it had; a CR-only spec is a clean
  no-op through the two strippers.

- **A trailing inline comment on a spec's `status:` line survives the write (#357).** The writers
  kept everything through the colon and dropped the rest, so `status: draft  # set by hand` came
  back as `status: done`. The comment and its separating whitespace now carry through whenever a
  conservative token pattern can certify where the scalar ends; anything it cannot read as a bare
  token falls back to the full drop, and the value's own quotes are still dropped deliberately.

- **A spec status the writer cannot rewrite is no longer a silent no-op (#335).** The writer found
  its line by prefix while every reader parses the block as YAML, so a quoted key, a space before
  the colon or a flow mapping wrote nothing and told no one — while a block scalar, a continued
  value or a nested `status:` was rewritten into corruption. The edit is now re-parsed with
  `yaml.safe_load` as an oracle and kept only if the block still parses as a mapping, its `status`
  is the target, and every other key is unchanged.

- **A status no line edit can safely move now raises instead of reporting success (#335).** `False`
  now means "nothing to change", so setting an already-`done` status returns without rewriting,
  while a genuine failure raises: a re-arm aborts before persisting rather than routing the re-drive
  to the wrong step.

- **A symlink-loop fault at park no longer loses the run's park (#335).** Below Python 3.13 a
  symlink loop is reported as a type neither guard on the park path held, and the park-index write
  ran outside every `try` in the commit phase — so an escape skipped the park notification, the
  `post_commit` hook and the state save. Both guards now hold the type, and the writer degrades to
  its `operator-index-failed` journal line.

- **An unwritable `ATTENTION` file can no longer crash a run.** The notice promised "never raises",
  but only its desktop half was guarded — so an unwritable run dir turned an advisory notice into a
  run crash at every site that journals a decision and then announces it: defer, escalate, plugin
  veto, manual-recovery pause, budget warnings. The file sink now degrades like the desktop one; the
  journal entry each caller writes first remains the durable record.

- **`limits.max_tokens_per_story` is validated like its per-session sibling.** It was parsed with a
  bare `int()`, so `true` silently became a 1-token story cap and `0` was accepted, both against the
  documented `int >= 1`. Non-integers and values below 1 now raise `PolicyError` at load. Note this
  rejects a `policy.toml` that previously loaded; there is no `0 = off` semantic — set the cap high
  instead, it only warns.

- **A pause inside a defer's rollback no longer loses the defer record (#342).** The task reached
  terminal DEFERRED before the tree was recovered, so a rollback that paused instead — rollback off,
  the default, or a preserve failure — unwound past the tail for ever: no `story-deferred` journal
  entry, no defer notification, an under-counted `defer_count` in `diagnose`. The record is now
  emitted before the pause re-raises, and its notice points at the ACTION REQUIRED manual-recovery
  notice instead of describing a rollback that never ran.

- **Spawn-level `OSError` is translated at the git chokepoint (#343).** Only a timeout was
  translated, so an `EMFILE`, `ENOMEM` or `ENOENT` out of the spawn itself bypassed every
  OSError-blind `except GitError` guard and crashed the run — under exactly the resource pressure
  those guards exist for. Spawn faults now raise a typed `GitSpawnError` with the errno on
  `__cause__`: a fault opening a unit worktree pauses instead of marching the queue into DEFERRED,
  and one during merge-target reconciliation keeps the unit branch and escalates.

- **`safe_rollback` no longer swallows a failed `git stash create` (#340).** The empty snapshot
  silently disabled the whole `preserve` restore, so the hard reset reverted exactly the paths the
  caller asked to keep — a resolved re-drive's corrected spec — with no error anywhere. It now
  raises before the reset, and only where a restore was actually requested, so the callers that ask
  for none degrade as before.

- **A spawn-level `OSError` during the attempt snapshot no longer crashes the run (#343).** An
  `EMFILE` or `ENOMEM` escaped untyped out of the middle of a rollback. Preservation is observation
  rather than a repair write, so it now degrades into the same journal-and-decide path a `GitError`
  takes, keeping the errno as the breadcrumb; `safe_reset` still raises.

- **A git fault while counting the attempt's commits no longer crashes the rollback (#343).** The
  range above baseline was enumerated with no guard at all, so an ordinary git timeout or a spawn
  fault took the run down mid-rollback. An un-determinable range now reads as "there may be work
  above baseline" and refuses the reset instead of taking the clean-tree early return, journaled
  `attempt-preserve-enumerate-failed` apart from `attempt-preserve-failed`.

- **The orchestrator's ledger writers no longer inject lines from a multiline value (#305).** Found
  by [@Haven2026](https://github.com/Haven2026) in #274. The deferred-work ledger is line-oriented
  but its mutators interpolated their arguments verbatim, so a note could mint a phantom entry,
  truncate an entry's span and re-surface its tail as a phantom legacy item, or leave one entry
  carrying two `status:` lines. Line breaks in free text now collapse to a space — sanitized rather
  than rejected, because a formatting defect must not cost a triage attempt.

- **Ledger writers validate the orchestrator-owned fields (#305).** A non-ISO `date`, a `status`
  outside `open`/`done <date>`, or a `severity` outside `critical|high|medium|low` now raises rather
  than landing in the file. The inner dev session and the sweep's migration session still write
  ledger markdown directly, so the sweep skill now states the single-line expectation — picked up on
  `bmad-loop init --force-skills`.

- **A deferred finding appended after the last ledger entry is no longer lost (#304).** Found and
  first fixed by [@Haven2026](https://github.com/Haven2026) in #274. The inner dev session appends
  each defer as a flat block, which the last canonical `### DW-<n>` entry's span absorbed — so it
  was invisible to the sweep, to `--dry-run` and to the TUI's legacy view. Spans now end at a flat
  block, and `append_entry` writes the documented `location:` field it had been omitting.

- **A sweep's return to your terminal no longer claims a hand-off that never happened (#227).** The
  return answered success unconditionally, discarding the switch's own result, so a failed switch
  plus a failed fallback still journaled the return and sent the sweep unattended. The return option
  is now cleared only on a real return, a failed one left for the parked window's trailer, and the
  two failures report apart: `ATTENDED` (a human is still there) versus `UNREACHABLE` (no client at
  all), which journals `sweep-return-no-client`.

- **`bmad-loop mux` renders a readable table whatever a backend reports as its version (#321).** A
  probe answering with an embedded newline split every row and stranded SELECTED on a line of its
  own; a very long single line broke the table just as thoroughly, since the column widths are sized
  off the widest cell. A backend's reported version is now one bounded line — folded rather than
  truncated, so the tail naming psmux as the answering binary survives, and capped at 80 characters
  — and every consumer applies the same fold defensively, so an out-of-tree backend cannot split a
  row or a message. On a psmux host the folded value **replaces** the previously truncated version
  in `diagnose --json` and in `validate --json`'s `mux.backend` and `mux.backends-detected`
  findings; the field shapes are unchanged.

- **`bmad-loop mux` explains a row that is available but unselectable (#321).** A backend reads
  AVAILABLE because its binary answers here, which is not the same question as whether automatic
  selection can pick it — on Windows `tmux` is psmux's compatibility shim, so the tmux row looks
  like a real tmux install. Gating the column would be wrong, since a forced choice does reach those
  backends, so the listing now carries a `note:` naming them instead. A forced backend is exempt:
  calling it unselectable would contradict the `*` marker one line above.

- **Both mux client verbs now owe effect, not dispatch (#317).** `TerminalMultiplexer.detach_client`
  widens from `None` to `bool`. tmux reads the effect off the exit code; psmux cannot — every arm of
  its verbs exits 0 whether or not a client moved — so it measures the session's attached-client
  count across the call and answers on the drop, degrading to `False` rather than a vacuous `True`
  where that is unobservable. Out-of-tree backends still returning `None` read as "nothing detached"
  — degraded, not broken.

- **Harden the psmux option channel's safety core (#313).** The cleanup sweeps matched any
  `<name>_@<digits>` key, so a hand-written `@theme_@3` died with window `@3`; keys now carry a
  seam-owned marker (`@bmad_project__blw@3`) only a deliberate imitation collides with.
  `kill_window` frees the keys only once a liveness listing proves the kill landed, so a failed kill
  no longer strips a live window's project tag and return key, and a free that fails warns instead
  of leaking silently. **Dev builds only:** a window parked by a pre-marker build reads as untagged
  and its return move stops firing — restart the ctl psmux server after upgrading.

- **Gate the psmux session project tag on transportability (#320).** The session tag rode a control
  line that stores some project paths corrupted at rc 0 — and a corrupted tag never equals the
  caller's again, so the prune skipped that session for ever. The tag now takes the same transport
  gate as the window channel: a refusal warns, frees the key and leaves the option unset, where the
  prune's run-dir fallback takes over (bounded by #419); accepted writes keep the raise-on-failure
  contract.

- **Give psmux a working per-window option channel (#310).** psmux keeps one user-option scope per
  server and answered empty to any per-window read of an `@`-prefixed name, so the control window's
  project tag bled across rows — letting a prune in one project kill another's window — and the
  parked-return option always read empty. Both now use a session-scoped key carrying the window id
  (`@bmad_project__blw@3`); the `switch-client` leg stays inert on builds predating psmux/psmux#483,
  still inert at 3.3.7.

- **Session-qualify the psmux TUI-side window ids (#291).** #254 covered the engine seam but left
  the launcher's surfaces bare, and that process usually runs outside any pane — where a bare `@N`
  resolves through psmux's most-recent-session fallback rather than the session that minted it, so
  the control-window prune could kill another server's identically-numbered window at rc 0. The
  launcher's window ids now carry their session, and `select_window` resolves the id to an index
  first.

- **Verify environment faults are classified per shell, so Windows stops burning attempts (#302).**
  The `{126, 127}` convention is `sh`'s; `cmd` has no equivalent — a missing tool exits `1`, like
  the "tests failed" that should route to repair — so the arm never fired on win32, leaving #130's
  charged-attempt regression live there. It now classifies on rc 9009, `cmd`'s `is not recognized` /
  `access is denied`, and a probe that also catches a file outside `PATHEXT` exiting `0` unrun — a
  pass verify never earned.

- **psmux window ids are now session-qualified (#254).** psmux mints window ids per server, so a
  bare `@N` replayed as a target routed by the caller's own `$TMUX` — from a `bmad-loop-ctl` pane,
  the ctl server rather than the agent's. The log sink then bound to the engine's own window (empty
  run logs), nudges went to the engine's pane, and teardown killed it instead of the agent's. Both
  verbs now emit the session with the id, degrading to the bare id when the session name contains
  `:` (#221); tmux ids are server-global and untouched.

- **A session's read-back could adopt another story's spec (#261).** The generic dev and review
  read-back picked its artifact by mtime from the shared implementation-artifacts directory — which
  under worktree isolation also covers the main checkout's copy — so a foreign spec landing there
  after launch won: a review that produced nothing scored `completed:done`, and a dev leg skipped
  review. Unlike the rest of this family (#127/#160/#224) it failed toward _landing_ unverified
  work.

- **The read-back is pinned to the spec the orchestrator named (#261).** Wherever the dispatched
  prompt names the path — every review leg, dev repair and patch-restore — the read-back takes that
  path and the directory scan is never reached; a sweep bundle's differently-named spec (#161) needs
  no exemption. A bare-story-key re-drive and a dev attempt 1 keep the scan, and the skill's no-spec
  fallback marker is no longer recorded as a story's spec.

- **A dead session with no evidence it ran can no longer be upgraded to `completed` (#261).** A
  read-back artifact is refused unless a turn ended — a `Stop` event specifically — or the pane log
  grew past a small floor; the two are ORed because each has a blind spot. Scoped to the
  shared-directory read-back; a task-scoped result stays authoritative. Applies to the crash path
  too, journaling `readback-refused-no-proof-of-work`.

- **`validate` requires the review skills your dev primitive really invokes (#260).** The preflight
  held every project to a fixed catalog naming a skill no tagged BMAD-METHOD release ships,
  misdiagnosing it as a missing bmm module even where bmm was installed — so `validate`, `run`,
  `resume` and `sweep` all failed on a stock install. The reviewers now come from the installed
  skill itself: its `customize.toml` review layers, else what its review step names inline, with
  overrides merged as BMAD's own resolver does.

- **New `skills.*` findings for a review-layer config (#260).** A configured layer naming a skill
  the tree lacks is a `skills.review-layer-missing` problem instead of passing and then failing on
  every dev run; disabling every layer is `skills.review-layers-empty`, an unreadable override is a
  `skills.customize-unreadable` warning, and a layer gated by a run-time condition is
  `skills.review-layer-unresolved`. `validate` and the run preflight branch on severity, so an
  advisory can no longer abort a run.

- **Isolated worktrees get the review skills that were validated (#260).** Provisioning copies the
  skills the project's own layers name, not just the fixed base catalog, and seeds `_bmad/custom/` —
  whose user override layer the upstream installer gitignores — so the preflight and the worktree
  run no longer resolve different layer sets.

- **`notify.desktop` works on macOS/Windows, and warns when it can't (#231).** The channel was
  `notify-send`-only, so on macOS and Windows it was inert while defaulting to `true` — every "a
  human is needed" path reached no one. It now dispatches natively (`osascript`, a best-effort WinRT
  PowerShell toast, `notify-send`), passing untrusted text through the environment or argv rather
  than a command string. With none available, `validate` warns `notify.desktop-unavailable` and the
  run start prints one.

- **Scrollable modal dialogs (#275).** The decision, escalation, confirm, sweep-options and
  story-checkpoint TUI dialogs now scroll their bodies and dock their action buttons, so the buttons
  stay reachable with long content down to the dialog's minimum frame height. Safety warnings that
  gate an enabled Resume or Re-arm dock with them, and the Resume confirm re-checks engine liveness
  at click time.

- **A finished story whose session omitted its result marker no longer DEFER-drops (#224).** The
  review HALT intermittently finalizes the spec to `status: done` without the terminal
  `## Auto Run Result` block the harvest scan keys on, so every Stop read `no-artifact`, stall
  nudges re-invoked an already-exited workflow (#149), and after `max_review_cycles` the finished,
  verify-passing work was rolled back.

- **The harvest scan synthesizes a result from terminal frontmatter (#224).** It fires once the
  spec's (path, mtime, status) fingerprint holds stable across two resultless Stops, and the
  post-kill reconcile applies it on a single sighting once the window is provably dead. Synthesized
  results carry `synthesized_from_frontmatter` and journal `session-synthesized-from-frontmatter`.

- **Deterministic missing-marker catch and repair (#276).** The #224 fallback was heuristic: a
  review killed after an mtime bump but before its `in-review` flip could score `done` without
  running. The engine now snapshots the spec at review launch and refuses a candidate still hashing
  equal to it (`unmodified-since-launch`), while an observed mid-session status transition proves
  the session ran and outranks that gate, collapsing the two-Stop fingerprint to one sighting.

- **A synthesized result repairs the spec (#276).** The marker the skill owed is written back
  atomically, refused outside the orchestrator-owned roots or where the fresh frontmatter disagrees
  (`spec-marker-repaired`, `spec-marker-repair-failed`, `spec-marker-repair-skipped`). The launch
  `status:` is **never** mutated: it is load-bearing routing input to the upstream skill.

- **`limits.dev_contract_nudge` (default `true`) asks the skill to repair its own omission (#276).**
  On the first pending Stop the dev adapter sends one nudge, once per session
  (`contract-nudge-sent`); set it `false` to rely on harness-side synthesis alone.

## [0.9.1] — 2026-08-02

Compatibility hotfix for the BMad Method's `bmad-dev-auto` → `bmad-build-auto` rename
(BMAD-METHOD#2651, first shipped in bmad-method 6.10.1-next.33) and the two upstream changes
that rode the same window. Both skill eras are supported; the rename itself needs no
`policy.toml` edit.

### Fixed

- **The dev primitive is resolved on disk, so the upstream rename no longer breaks a project
  (#405).** `bmad-build-auto` is preferred and a marker-complete `bmad-dev-auto` accepted, so
  `validate`/`run`/`sweep`/`resume` pass on either era and report which one resolved. A new
  `skills.base-shim` check refuses the forwarding shim, which HALTs an unattended session when a
  legacy `_bmad/custom/bmad-dev-auto*.toml` sits beside it. `[dev] skill` stays `bmad-dev-auto`.

- **Every session prompt spells the resolved primitive (#405).** Dev, review, repair, restore,
  stories dispatch and all three sweep bundle legs hardcoded `/bmad-dev-auto`, which post-rename
  dispatches the shim. The name is now resolved per skill tree, so a run mixing `.claude/skills`
  and `.agents/skills` gets the right one per role, and the fallback marker matches both prefixes.

- **`--dry-run` says when its preview is not runnable (#405).** Dry runs returned before their own
  skill preflight, so a broken install still got a plausible-looking schedule. Preflight failures
  now print to stderr under a "NOT runnable as-is" banner; exit code stays 0 and stdout is
  untouched, since rc 0 means "the preview rendered", not "ready to run".

- **The skills preflight no longer gates a triage-only CLI's skill tree (#405).** Every `skills.*`
  check asks a dev-primitive question, yet the tree list came from all three adapter roles — so a
  `[adapter.triage]` of `gemini` demanded the whole BMad Method module in `.agents/skills`. It is
  now scoped to dev and review; single-CLI and dev/review-split projects are unaffected.

- **A worktree that could not be given its upstream skills now pauses instead of stalling (#405).**
  The containment guard skips a skill tree symlinked to a shared machine-wide install while the
  run-start preflight stats through that symlink and passes, so every isolated session stalled on
  `Unknown command`. Undelivered skills are journaled `worktree-seed-skipped` and the engine
  escalates before dispatch.
  The seed also merges per _file_, and checks each file for containment — a behaviour change.

- **A renderer stub that cannot compose a prompt fails preflight (#405).** Three new checks block
  `validate`/`run`/`sweep`/`resume` when the resolved `SKILL.md` is the renderer stub
  (BMAD-METHOD#2601): `skills.dev-renderer` for an incomplete script unit,
  `skills.dev-renderer-config` for an absent `_bmad/config.toml` (the renderer's only required
  config layer), and `skills.dev-renderer-sources` for a missing `workflow.md` or an unloadable
  `[[bmad-snapshot:…]]` token.

- **A stale customization override is reported, not obeyed (#405).** `skills.customize-legacy` warns
  when an override still sits at `_bmad/custom/bmad-dev-auto[.user].toml`, where it no longer
  applies — the session runs, unstyled.

- **Worktree isolation carries the `_bmad/` config surface (#405).** The renderer-era primitive
  takes the worktree as its project root and hard-fails when that root has no `_bmad/` — there is
  no walk-up — so on a project that gitignores it (most do) every isolated session HALTed with
  nothing written. Provisioning now merge-copies `_bmad/` per file, and a short seed pauses the run
  when the resolved primitive is a renderer stub, naming what is missing.

- **The renderer's `_bmad/render/` output stays out of story commits (#405, #409).** Outside a git
  repo the check stays quiet rather than fabricating an ok (#409). It is never
  seeded into a worktree and is git-excluded inside one, and `init` now gitignores it — the only
  protection under the default `isolation = "none"`. Neither shield helps a path already tracked,
  so a new `git.render-tracked` warning names the one-time `git rm -r --cached _bmad/render`.

- **Worktree provisioning survives a filesystem it cannot fully read (#405).** The `_bmad/` seed
  and its detector both used `rglob`, which does not descend a symlinked _sub_-directory, so a
  symlinked `_bmad/scripts/lib` was under-seeded and reported complete; both now share the skill
  seed's walk. Per-file faults in the walk are skips the gate names, not an exception out of
  provisioning; the eager `worktree_seed`, plugin and hook-config copies still raise.

- **A seed entry the worktree never got is now reported (#405).** The seed loops dropped an entry
  with a bare `continue` when the containment guard refused it, so a config the repo carries as a
  symlink _out_ of itself delivered nothing and said nothing. Drops are journaled as
  `worktree-seed-dropped`, and `worktree-opened` now fires at mount rather than after the gates.

- **Seeding never writes _through_ a symlink (#405).** Both seed loops probed and copied against
  the _resolved_ destination, and `Path.resolve()` is non-strict — so a dangling link reported its
  slot free and the copy landed at the link's target, a path `git add -A` would stage into the
  story branch. `git worktree add` produces exactly that state for a tracked symlink whose target
  is untracked, so it arrives on a project's _first_ story.

- **A hook config is no longer its own alibi (#405).** The drop report probed the destination for
  existence, but the per-CLI hook step writes `profile.hooks.config_path` after both seed loops, so
  a dropped config was answered for by the hook's own bytes — and for gemini, copilot and
  antigravity that path is the profile's only default seed. Those rels are now asked whether the
  source escapes the repo, or the destination is a symlink or escapes the worktree.

- **`isolation = "worktree"` is refused when `repo_root` is overridden (#405).** A project whose
  `_bmad/bmm/config.yaml` sets `repo_root` — the documented monorepo knob — decouples the git root
  from the project dir. Provisioning seeds every surface off `repo_root` while `init`, `validate`
  and the run preflight write and probe them under `project`, so the preflight approved a surface
  the isolated run never received and every story ended as a result-less Stop.

- **The `repo_root` refusal covers every entry point (#405).** `validate` reports
  `policy.isolation-repo-root`, and `run`, `sweep`, `resume`, `resolve` and the child sweep all
  refuse — drop the override, or set `isolation = "none"`. The child raises rather than declining
  quietly, so a mid-run flip is journaled `sweep-auto-failed`. Plumbing `project` through
  provisioning stays open as #414 and #443.

- **`worktree_clean` and `path_tracked` no longer read their answer out of git's stderr (#405).**
  `ls-files` and `status` exit 0 while still writing to stderr, and that chatter was
  indistinguishable from an index entry or a porcelain line — so `git.render-tracked` named an
  uncommitted path and a clean checkout read dirty. Other callers still merge, which is #442.

- **An undecodable `policy.toml` or `config.yaml` is reported, not a traceback (#405).**
  `UnicodeDecodeError` is a `ValueError`, not an `OSError`, so it escaped every
  `except (PolicyError, OSError)` handler — the TUI could not open and the CLI died at startup on a
  raw codec message naming no file. Both loaders now raise typed errors; `validate` names the file.

- **Deferred review findings are harvested out of the spec's frontmatter (#405).** BMAD-METHOD#2640
  moved `defer`-triaged findings from `deferred-work.md` into the spec's own `deferred:` list,
  silently starving the sweep pipeline. A successful dev, repair or review session now files each
  into the ledger with its `location` and `severity` (`spec-deferrals-harvested`), deduped on a
  fingerprint of its summary and location; the frontmatter is never rewritten, so a revert is
  lossless. The review prompt no longer files the finding itself, which double-filed it.

- **A transient harvest read cannot silently drop recorded findings (#405).** An unreadable,
  missing, undecodable or temporarily malformed spec at the harvest step now follows the existing
  bounded retry paths instead of letting a later verifier accept and commit without the ledger
  repair. A persistent fault defers with the artifacts preserved, or re-escalates a CRITICAL.

- **Post-session ledger work keeps its proof attribution across crash replay (#405).** The
  completed-session checkpoint is refreshed after hooks return, so a retained retry cannot hide a
  hook-authored ledger repair behind an earlier harvest's engine-written exclusion. A pre-feature
  checkpoint with no ledger digest reconstructs attribution from its Git baseline, so a
  ledger-only session still resumes while the new harvest stays excluded from proof.

- **A harvested deferral is reverted when its attempt rolls back (#405).** The harvest runs above
  the artifact gate, so a session that finalized its spec and then failed a non-fixable check left
  an entry describing discarded code the reset cannot remove — the ledger sits under a
  `keep`-shielded artifacts folder. The dev phase now snapshots it and restores around the rollback,
  persisting the snapshot with the attempt and never unlinking a ledger git tracks.

- **That restore spans the whole retry chain (#405).** On the `rollback_on_failure = off` default it
  reverts every attempt's ledger writes, not just the last — matching the
  `git reset --hard <baseline_commit>` the pause notice tells the operator to run. Reaching the
  restore unarmed still records `ledger-snapshot-missing`.

- **The pre-harvest snapshot is spent by a stop-and-wait pause, and scoped to the retry chain
  (#405).** Under the default `rollback_on_failure = off` the operator may append to the ledger
  before typing `resume`, but the armed snapshot survived that wait and the resume wrote stale
  bytes over their edit; the pause leg now disarms as it restores. A fixable retry neither re-arms
  nor spends it, so the revert reaches as far as the reset does. Not closed: `_finish_inflight`'s
  restart arm resets to the same baseline with no ledger restore at all.

- **A harvest is reverted even when the ledger lives outside the repo (#405).**
  `implementation_artifacts` may be configured out of tree, and the restore classified any such
  ledger as git's — backwards, since `reset --hard` cannot reach outside the workspace, so every
  revert was a no-op and the entry outlived the code it described. It now reads as "not git's".

- **The harvest's own ledger write is no longer the session's proof of work, and the session's own
  edit still is (#405).** The dev artifact gate deliberately does not exclude the ledger — a story
  whose whole scope is ledger reconciliation has to count as real work — so it could not tell the
  orchestrator's write from the session's, and a session that changed no code but recorded one
  finding proceeded to done on the engine's line. The gate now excludes the harvest's own attempts,
  and stands down again when the ledger had already moved off the dev phase's baseline.

- **Both of those answers span a fixable retry (#405).** A fixable retry keeps the harvest's ledger
  line with its tree by design, so the repair session met a stale baseline: an attempt that merely
  reverted the offending change passed on the orchestrator's own write, and a stalled attempt
  deferred with an empty record of the harvest's intent. Both records now survive the continuation,
  and the ledger baseline re-bases: forward onto the kept tree, back onto the restored snapshot on a
  rollback. (A gitignored ledger is invisible to the gate either way.)

- **A sweep bundle's ledger closes are withheld until its attempt is accepted (#405).** The
  orchestrator marked a bundle's ids `done` above the artifact gate, so a discarded attempt left the
  ledger claiming its work resolved, and `open_ids` re-bundles only open entries. The close now runs
  below the gate, for a PROCEED decision only. One deliberate consequence: a bundle session that
  changed no code now fails the gate rather than passing on the orchestrator's own bookkeeping.

- **A review-leg defer takes those closes back (#405).** A defer after acceptance — every route, the
  stock `trigger = "recommended"` included — re-opens the ids it closed itself, since `_defer`
  writes its post-close snapshot over the reset that reverted them.

- **An isolated unit's ledger writes reach the main checkout — findings and bundle closes alike
  (#405).** A defer drops the unit worktree unmerged, and a landing unit's ledger edit rides the
  branch only when the ledger is tracked: `finalize_commit` stages with `git add -A`, which skips a
  gitignored path in silence. Both legs now re-file what the harvest intended and re-apply what the
  close **intended**, the DONE leg **after** the merge so entries dedup; `mark_done` is idempotent
  and a DEFER carries findings only. An _unseeded_ gitignored ledger still defers rather than lands.

- **A carry lost to a crash mid-landing replays on resume (#405).** `Phase.DONE` is persisted
  before the merge, the merge removes the worktree, and only then does the carry fire — so a host
  death there skipped it and resume never looked again. Resume now re-runs an unlatched carry once,
  behind a persisted latch and a durable `unit-merged` record; the merge writes its intent before
  invoking git, so an interrupted merge is re-run rather than assumed to have landed.

- **Tracked ledger carry failures stop and remain replayable (#405).** A rejected `git add`,
  `status` or `commit` used to be journaled and swallowed, letting an isolated unit finish with a
  dirty or staged main ledger. A committable carry now persists its commit intent and raises, and
  resume retries it. Gitignored and external ledgers keep their advisory degrade behavior.

- **An artifacts dir whose name holds `[` or `]` no longer misdirects those two paths (#405,
  #423).** Git reads a positional operand as a pathspec, so such a path was a glob that also
  matched its neighbours: the harvest revert's tracked-probe answered off a neighbour and skipped
  its unlink, and the carry's commit swept a neighbour's edit in. Both now name the path literally.

- **Three small contracts brought back into line (#405).** A ledger entry filed with no file:line
  carries `location: n/a`, the value `deferred-work-format.md` has always specified — entries
  already on disk without the line stay valid, so read an absent `location:` as `n/a`. A plugin
  workflow's completion marker resolves on its own role's skill tree, not always the dev one. And
  `diagnose` pseudonymizes the `spec` journal field, which was shipping the feature name verbatim.

## [0.9.0] — 2026-07-21

### Added

- **Active agent indicator (#153).** The TUI run header and tasks table now name who is driving —
  the resolved adapter·model for the live stage, or the run's configured adapters when no session is
  open. Session-start journal entries and session records stamp the resolved adapter identity, and
  `bmad-loop status --json` gains an additive run-level `adapters` (the snapshot-resolved
  dev/review/triage identity, `null` on a run predating stamping) and per-story `adapters_used` (the
  identity actually recorded per role) — both are a projection of the run's persisted policy snapshot
  (re-stamped from current config on resume) and its recorded sessions, not live policy read at status
  time; a run whose snapshot predates adapter stamping reports `adapters: null` rather than a
  fabricated default. Schema version unchanged.

- **Graceful stop (`stop --graceful`, TUI `S`).** Ask a live run to finish its in-flight item —
  a story or sweep bundle through commit, or an in-progress sweep triage — then finalize cleanly
  and stop as a resumable `stopped` run, instead of the hard SIGTERM stop that kills mid-item.
  Delivered through a `stop-request.json` control file consumed at the next item boundary, so it
  needs no signal and works on every platform and multiplexer backend. Pending auto-sweeps are
  suppressed; `--cancel-graceful` withdraws a request, and a hard stop still wins over a pending one.
  `status --json` gains an additive `graceful_stop_pending` field (schema version unchanged).

- **`bmad-loop validate --json` (#205).** A stable, schema-versioned JSON document of the
  preflight: the `ok` verdict, the queue `mode`/`spec_folder`, per-severity `counts`, and every
  check as a flat emission-ordered finding. Each finding carries a **stable `check` id** —
  `hooks.registered`, `adapter.binary`, `skills.base-incomplete`, … — so CI can branch on a
  particular failing gate instead of matching remediation prose, which is the part most likely
  to be reworded. `detail` keeps what each check knew before it flattened itself into a
  sentence: `mux.backends-detected` keeps every detected backend row rather than the text's
  `tmux*, psmux (unavailable)` soup, whose trailing `*` a consumer had to parse to learn which
  backend was selected, and `skills.base-incomplete` keeps `missing_markers` as a list rather
  than a `", "`-joined string. **A failing check emits the whole document and still exits 1** —
  the nonzero code is the verdict being reported, not a failure to produce one, so the existing
  `bmad-loop validate || exit 1` in CI is untouched. `machine.py` gains the clause that makes
  this well-defined: parse non-empty stdout whatever the exit code, and read the verdict from
  the document's own `ok`, which unlike `rc` separates "the checks failed" from "the command
  broke". The text output is byte-for-byte unchanged.

- **`bmad-loop clean --json` / `bmad-loop cleanup --json` (#204).** Stable, schema-versioned
  JSON documents (one per command — they are separate contracts) reporting what a reclaim
  removed, or under `--dry-run` would remove: for `clean` the worktree paths, trimmed,
  archived, deleted and protected run ids, the effective retention policy, and `freed_bytes`
  as a raw integer — the text's `~1.2MB` is a rendering of that number, and formatting is the
  renderer's job; for `cleanup` the run ids whose sessions went, the live ids left alone, and
  the ctl windows closed. Plan and outcome share one schema — same fields, same meanings, with
  `dry_run` saying which one you are holding — so a script can pre-flight and then compare
  against what actually happened. The values are each invocation's own sample rather than a
  promise the two agree: `freed_bytes` is re-measured, and the world can move between the
  preview and the commit. **The real paths are now scriptable at all** — they previously discarded
  the per-item data and printed only a summary line, and `protected` was a bare count. Both
  commands printed progress as they mutated, and both warned mid-loop about an unverifiable
  engine pid; under `--json` that warning becomes a document field, so stderr stays empty and
  stdout stays one pure document.

- **`bmad-loop decisions --json` (#203).** A stable, schema-versioned JSON document of the
  pending deferred-work decisions, so a script can select an option by policy and pre-answer
  it rather than scraping the numbered text. It is strictly richer than that text, which drops
  each decision's `context` and shows only key/label/effect per option — hiding the `intent`,
  `resolution` and `bundle_name` that decide what the next sweep actually builds or writes.
  The recommendation, a `(recommended)` suffix on a free-text line in the text form, becomes a
  derived boolean on the option it names. `--json` implies the listing and never prompts (the
  interactive prompter reads stdin and cannot coexist with a pure document), and nothing
  pending is a valid empty document with exit 0.

- **`bmad-loop list --json` (#192).** A stable, schema-versioned JSON document — one entry
  per run, oldest first (short ref, run id, type, started-at, liveness-aware status, paused
  stage) — replaces the text table when passed. Unparseable runs are included as status
  `unknown`, and an empty runs dir yields a valid empty document with exit 0.

- **`bmad-loop status --json` (#190).** A stable, schema-versioned JSON document (run
  id/type/source, derived status + pause fields, snapshot `cache_read_weight`, raw +
  weighted token totals, and per-story phase/attempt/review-cycle/tokens/commit/defer
  reason) replaces the text output when passed. This is the supported machine-readable
  surface — the human text, whose layout #129 already changed once with no warning
  path, is now explicitly best-effort.

- **`session-end` journal entries carry `tokens_weighted` beside `tokens` (#129).** Only the
  raw scalar was persisted, and the weight cannot be backed out of it, so a session's
  cost-weighted spend was unreconstructible after the fact — the weighted figure existed
  only for sessions that tripped the budget guard. Every entry whose usage was read now
  records both. `null` (never `0`) when the usage read failed, since untracked is not free;
  both fields stay absent on an `aborted` end, where no read happened. Distinct from a
  tripped session's `budget_weighted`, which is the guard's mid-session sample at trip time
  rather than the end-of-session total. The `cache_read_weight` knob also gained a
  description in the TUI settings screen, where it had none.

- **Mid-session token-budget guard (#158).** Both adapter wait loops now sample cumulative
  weighted usage every ~30s and act on crossing the new per-session cap
  (`limits.max_tokens_per_session`, default 4M weighted) per `limits.session_budget_mode`:
  `warn` = one ATTENTION + lifecycle breadcrumb; `enforce` = wrap-up nudge +
  `limits.session_budget_grace_s` (default 240s) to finish, then termination with the new
  `over_budget` session status, which rides the ordinary retry→defer routing. Defaults to
  `warn`: on upgrade, existing installs gain visibility (one ATTENTION line per over-cap
  session) but no terminations — set `session_budget_mode = "enforce"` to opt into the
  hard bound, or `"off"` to silence the guard entirely. Session-end
  journal entries carry `budget_weighted`/`budget`/`budget_mode` for tripped sessions.
  Live-verified on `claude`; other transcript-reading profiles sample best-effort, and
  adapters with no mid-session usage signal (`usage_parser = "none"`, Copilot) stay inert.

- **OpenCode adapter (`opencode-http` profile, alias `opencode`).** Drives
  [OpenCode](https://opencode.ai) ≥ 1.18 entirely over HTTP/SSE — one headless
  `opencode serve` per session (no tmux window), SSE `session.idle` as the completion
  signal with an HTTP poll fallback, per-session server password, hermetic skills, and
  token usage read back over the API. Full dev/review synthesis parity via the new
  `_ResultFileMixin`/`_DevSynthesisMixin` seams in `generic.py`; profiles gained a
  hookless `[hooks] dialect = "none"` mode (no hook registration anywhere). Install the
  HTTP client with `pip install 'bmad-loop[opencode]'`; set `model` as `provider/model`.
  The pinned 1.18.2 API contract is recorded in the adapter's module docstring, guarded
  by a zero-token real-binary smoke test (`tests/test_opencode_live.py`, skipped when
  the binary is absent).

- **Native-Windows `psmux` multiplexer backend (experimental).** A bundled builtin that
  drives runs on native Windows through psmux — a ConPTY tmux re-implementation that speaks
  the tmux CLI via its own `psmux` binary — so tmux's session/window model and the
  `bmad-loop-<run-id>`/`bmad-loop-ctl` session names carry over unchanged. It registers for
  `win32` and is the platform default there, selected automatically when the `psmux` and
  `pwsh` binaries are on `PATH` and psmux reports newer than 3.3.6 (older releases can
  force-kill a recycled PID during teardown, so they read as unavailable and selection falls
  through). Native Windows stays experimental — window hosting, attach/detach mapping, and
  Unity cache-path correctness are tracked in the roadmap — but the dev→review→verify→commit
  loop and TUI observation run. WSL is unaffected (it _is_ Linux and uses tmux). (#58)

- **Out-of-tree multiplexer backends (`bmad_loop.mux_backends` entry points).** A backend
  package installed next to bmad-loop (e.g. `uv tool install bmad-loop --with <adapter>`) now
  registers itself with no config step: before every selection, core imports each module
  advertised under the `bmad_loop.mux_backends` entry-point group, whose import-time
  `register_multiplexer(...)` call makes the backend selectable exactly like a bundled one
  (builtins load first, so default selection is unchanged by installing an adapter). A package
  that fails to import can never break selection — the failure is recorded and surfaced as a
  `warning:` line by `bmad-loop mux` and a note in the `validate` preflight
  (`external_backend_errors()`).

- **Unity modal-dialog guards (`[plugins.unity]`).** A chronically-dirty Unity scene raises modal
  Editor dialogs ("scene changed on disk", "save changes before closing") that freeze the MCP
  dispatch loop and stall the whole run. The bundled Unity plugin now defends in depth: it seeds an
  editor-only `SceneAutoSaveGuard` into the project (`install_scene_guard`, default on), quiesces
  the Editor around a failed-attempt rollback so `git reset --hard` can't leave a stale scene open
  (`quiesce_on_rollback`, default on), and appends the scene-save discipline (from a shipped
  `unity_facts.md`) to every dev/review prompt so the agent saves at the boundaries that would
  otherwise trip a modal. As a last-resort observability net, an opt-in **detect-only** probe
  (`dialog_probe`, default off) watches — via xdotool, X11/Linux only — for those dialogs and
  _reports_ any it sees (a JSONL record, an `ATTENTION` line, and a best-effort `notify-send`); it
  never clicks or keys anything, no-ops where there is no X display, and self-reaps when the engine
  exits (`dialog_probe_interval_sec`, `dialog_probe_notify`).

- **Follow-up-review damping (`limits.max_followup_reviews`, default 1).** Bounds how many extra
  review rounds a story is granted _solely_ because a completed round finalized `status: done` yet
  still set `followup_review_recommended: true`. Once spent, the next such round force-converges —
  verify, then re-file the lingering recommendation to the deferred-work ledger, then commit —
  instead of burning cycles up to `max_review_cycles`. This damps the structurally non-convergent
  case where every review pass patches findings and therefore recommends another pass. The damped
  converge is the expected steady state and stays quiet (no ATTENTION); only the re-review cap (a
  story that itself originated from a `review-budget-followup` entry and still won't converge) still
  notifies. Verify-repair rounds, non-terminal rounds, and `PAUSE`/`DEFER`/`RETRY` never spend the
  grant; `0` never honors a pass's own recommendation. `runs.rearm_escalation` resets the counter so
  a human-resolved re-drive gets a fresh budget.

- **Resizable dashboard panes.** Every pane boundary is now adjustable by mouse-drag (divider
  bars, which also carry the Sprint / Deferred Work headings) or a keyboard resize mode (`ctrl+w`,
  then `←`/`→` for the sidebar, `↑`/`↓` for the active horizontal split, `Tab` to pick it, `Esc` to
  exit). Sizes persist per-project to a new `[tui]` section in `policy.toml` and re-apply on the
  next launch; untouched projects keep the previous fixed proportions.

- **Dev-choosable multiplexer backend selection (#87).** `get_multiplexer()` now resolves by
  precedence — `RIAWORKS_BMAD_LOOP_MUX_BACKEND` env var → the new machine-scoped `[mux] backend` key in
  policy.toml → the platform default (win32: `psmux`, elsewhere: `tmux`) when installed → the first
  registered backend that matches the platform _and_ is `available()` — so two same-platform
  backends (psmux / tmux-windows) no longer collide by registration order. Forced names are trusted
  (no availability gate) and fail loudly when unregistered, naming the policy file. New
  `bmad-loop mux` lists registered backends (platform / available / version / selected + why);
  `bmad-loop mux set <name>` persists the choice (`--clear` reverts to auto, `--force` allows a
  name that only registers on the target machine); no interactive prompts anywhere. `validate`'s
  preflight lists all detected backends when more than one is registered and notes an env/policy
  forced selection. A tmux-less POSIX host still selects `TmuxMultiplexer` and reports it
  unavailable, exactly as before.

- **Seam-canonical window targets.** The `=session[:window]` target grammar is now owned by the
  `TerminalMultiplexer` seam instead of living as hand-assembled tmux syntax in core: a new
  concrete `target(session, window=None)` encoder (overridable per backend, tmux inherits the
  default and passes it straight through) and a module-level `parse_target()` decoder that
  native-id backends reuse instead of re-deriving the grammar (the out-of-tree herdr
  adapter's `_parse_target` delegates to it). `runs.py`/`tui/launch.py`/`tui/app.py` format every
  target via `target()` (new `runs.session_target` / `launch.ctl_target` helpers) — output is
  byte-identical, so no backend or operator behavior changes; the contract is documented in the
  adapter authoring guide's new "Window targets" section.
- **Herdr multiplexer backend — shipped out-of-tree.** A complete non-tmux-family
  `TerminalMultiplexer` backend for [herdr](https://herdr.dev)'s cross-platform
  workspace/tab/pane model was developed in-tree (engine run path #136, TUI-launch surface
  #137) and extracted before ever shipping in a release to
  [`bmad-loop-adapter-herdr`](https://github.com/pbean/bmad-loop-adapter-herdr), where it
  co-installs with bmad-loop and registers through the `bmad_loop.mux_backends` entry-point
  discovery above. Core bundles only tmux; herdr's capabilities, remaining degradations, and
  operator notes live in the adapter repo's docs.
- **Stories mode — a second planning pipeline that drives the loop off a typed `stories.yaml` (folder+id dispatch) instead of `sprint-status.yaml`.** Opt in with `[stories] source = "stories"` + `spec_folder`, or per run with `bmad-loop run --spec <folder>` (overrides policy); `--story` then filters by story id. Each entry dispatches by folder + id — the dev skill creates-or-resumes the story spec at `<folder>/stories/<id>-<slug>.md` and the orchestrator reads that id-keyed path back deterministically (no shared board to line-edit, no result-artifact mtime-scan). Strictly linear schedule (list order, no `depends_on`); `bmad-loop run --dry-run --spec <folder>` and `bmad-loop status` print the board (id · live disk state · checkpoint markers · title). Sprint mode is unchanged and remains the default. Requires a `bmad-dev-auto` new enough for folder+id dispatch — the run preflight checks and remediates.
- **Per-story human checkpoints (stories mode).** Independent `spec_checkpoint` (pause before code to review the plan — dev halts at `ready-for-dev`; approve to implement, or request a replan that resets the spec to `draft`) and `done_checkpoint` (pause after the story commits, skipped when it is the last story); both additive to `gates.mode`. A blocked story escalates + resolves as in sprint mode, with a pre-planning-halt sentinel auto-deleted (a copy preserved under the run dir) on re-arm.
- **TUI human-in-the-loop surface for stories mode.** The sprint tree is replaced by a stories board (id · live disk state · spec/done checkpoint markers · title) when a stories-mode run is selected; paused runs carry a per-run pause-kind badge and the run list shows a global _⚑ N need attention_ count; `p` opens the stage-appropriate viewer — plan-checkpoint spec review (Approve & resume / Request replan), story-checkpoint summary card (Continue / Stop), escalation with story context (Resolve / Re-arm & resume), and a gate spec viewer that the existing spec-approval/epic pauses reuse. The start-run modal gains a source select + spec-folder field with a live schedule preview. Every TUI action calls the same code paths as the CLI.
- **Intent-gap patch-restore recovery.** When review halts on an `intent gap`, `bmad-dev-auto`
  now saves the attempted change as a patch before reverting (BMAD-METHOD#2564). If the attempted
  reading was correct, `bmad-loop resolve` re-arms the spec to `in-review` and re-applies the patch
  onto baseline after every reset, so the re-driven session resumes review on the restored diff
  instead of re-implementing. New `--restore-patch <path>` flag for the `--no-interactive` path; a
  patch that fails to apply escalates instead of running on a half-restored tree (a resolve session
  that committed over the patched lines triggers exactly this — re-resolve without a restore).
  Restore is rejected up front for worktree-isolation runs and for stories-mode pre-planning
  sentinels, and the latched patch file itself never counts as proof-of-work. Deferred-work
  `sweep` bundles get the same recovery — an escalated bundle re-arms to `in-review` and the
  re-driven bundle session resumes review on the re-applied patch (#75).
- **Preflight covers the inline review layers.** `bmad-loop validate` (and run-start) now require the
  three upstream review-hunter skills `bmad-dev-auto`'s step-04 invokes — `bmad-review-adversarial-general`,
  `bmad-review-edge-case-hunter`, and `bmad-review-verification-gap` (new in BMAD-METHOD#2550) — plus a
  `customize.toml` in `bmad-dev-auto` (its review-layer config, BMAD-METHOD#2535/#2550). A pre-July bmm
  install missing any is reported with remediation before a run stalls.

### Changed

- **The TUI's validate modal (`v`) renders `validate --json` instead of the text output (#210).**
  One row per check — glyph, stable `check` id, message — with the verdict taken from the
  document's `ok` rather than the exit code, which cannot tell "the checks failed" from "the
  command broke". A check's `detail` is now reachable at all: inline for warnings and problems,
  and `d` toggles it on for everything, so `mux.backends-detected` expands to a row per backend
  instead of the text's `tmux*, psmux (unavailable)`. A failure adds a footer noting the gates
  are chained — the later gates emit nothing after one fails, so a short list is not a short
  list of problems. An unrenderable document (a newer schema, unparseable stdout) re-runs
  validate in text mode and shows the old modal unchanged.

- **`validate` reports a failed external mux backend as a warning, not a note (#210).** The
  `mux.external-backend` finding has always read as a failure — "external mux backend 'x'
  failed to load: …" — while carrying severity `ok`, so it counted as a passing check; it is
  now `warning`, matching what `bmad-loop mux` has always printed for the same condition. It
  stays below `problem` deliberately: selection degrades past a broken external, so the verdict
  and exit code are unchanged. On an affected host `validate --json`'s `counts` shift by one
  (`warning` +1, `ok` −1) while `ok` and rc do not; the schema version is deliberately
  unchanged, since the document contracts each `check` id, not a given check's outcome. The
  text line gains the doubled `ok:   warning:` prefix that `render()` preserves by design.

- **BREAKING: `probe-adapter` now runs `diagnose`'s egress leak self-check, and captured hook
  payloads ship as a schema instead of scrubbed values (#199).** The rendered report re-scans
  itself before emitting (the guard moved to `sanitize.guard`, one audited implementation for
  both commands): an email / secret / home path / username in the final bytes makes the command
  refuse to emit — message on stderr, empty stdout, exit ≠ 0, no `--out` file — and a stray
  occurrence of the pseudonymized project directory name is repaired to its alias and disclosed.
  Each captured event now reports dotted key paths with leaf types (`tool_input.command:str`),
  never payload values, so the `--json` document's `schema_version` bumps to 2
  (`captured_events[].payload` removed, `payload_schema` added; `payload_keys` stays, now
  identifier-gated). Collection hardening rides along: transcript-location components that embed
  the username are redacted, the project dir name is aliased in locations, a home-rooted
  `--binary` hint renders `~`-relative, and a credential-shaped dict key can no longer surface
  in the token key paths.
- **BREAKING: `diagnose --json` and `probe-adapter --json` now emit a pure JSON document
  (#195).** Both used to print their human-readable report with a fenced ` ```json ` block
  appended, so a consumer had to scrape the fence out of prose. `--json` now emits the
  document _instead of_ the report — stdout parses whole, and every human-facing line (`ok:`
  trailers, the leak-backstop warning, the `unknown profile` notice) moves to stderr. With
  `--out FILE` the document goes to the file, stdout stays empty and the confirmation goes to
  stderr; **no file written in JSON mode carries markdown fences any more**. That file is held to
  the same standard as the stream — it is validated and newline-terminated identically, so
  `--json --out FILE` and `--json > FILE` produce byte-identical files. The text mode (no
  `--json`) is unchanged. `diagnostics.SCHEMA_VERSION` deliberately stays at 1 — it versions the
  document, and only the packaging changed — while the probe document gains a `schema_version`
  of 1 alongside its existing `version` key, which still holds the _probed CLI's_ `--version`
  output. Scripts that split on ` ```json ` must switch to parsing stdout directly; the break is
  in the flag's output shape, not in either payload. Two
  incidental fixes ride along: `diagnose --json` no longer renders the markdown report it was
  about to discard, which was double-counting every leak-backstop repair in the warning, and
  the probe document is now `sort_keys`-stable so two probes of the same CLI diff cleanly.
- **Machine-output (`--json`) contract codified in `machine.py`.** The pure-document conventions
  from #190 — one JSON object on stdout, inline `schema_version`, additive-only evolution,
  errors → stderr with empty stdout — now live in one module with shared `emit`/`add_json_flag`
  helpers; `status --json` uses them (output byte-identical) and the duplicated token-total math
  folded into `run_token_totals`. All four `--json` commands share the contract (#195); `--json`
  adoption on more commands is tracked in #196.
- **Backend-neutral naming for the seam-backed helpers and operator messages.** The multiplexer
  seam has non-tmux backends now, so the helpers that wrap it drop their legacy tmux names —
  `launch.tmux_available` → `mux_available`, `app._tmux_missing` → `_mux_missing`,
  `runs.tmux_sessions` → `mux_sessions` (internal, no deprecation aliases) — and the operator-facing
  strings stop naming tmux when they mean the selected backend: launch errors say
  `multiplexer new-session/new-window failed` and `multiplexer backend unavailable (binary not on
PATH)`, the TUI notifies `multiplexer backend unavailable — launch/attach disabled` and
  `launched (control session bmad-loop-ctl)`, and the "attach to … bmad-loop-ctl" hints say
  _control session_. The TUI-guide troubleshooting table matches. Behavior is unchanged.
- **Docs: multiplexer backend guide (`docs/multiplexer-backends.md`).** The user-facing docs no
  longer claim tmux is the only multiplexer backend. The new page covers backend selection
  (`bmad-loop mux` / `mux set`) and how external backends are installed and discovered;
  backend-specific operator guidance (what changes from your seat on herdr, its degradations)
  moved out with the extraction and lives in each adapter repo's docs. README, setup guide,
  TUI guide, and FEATURES name the mechanism and link the page.
- **Docs: `followup_review_recommended` is now scored upstream.** BMAD-METHOD#2580 replaced the
  skill's convergence-prone significance judgment with a severity-weighted score over patched
  findings and added a fourth default review layer (Intent Alignment Auditor, #2560). README,
  FEATURES, TUI guide, the `[review].enabled` setting description, and the engine's damping
  comments now describe the scored flag; `limits.max_followup_reviews` is unchanged and remains
  the orchestrator-side bound.
- **`bmad-loop init` now gitignores `.bmad-loop/policy.toml`.** Policy is per-machine-per-repo —
  it carries the machine-specific `[mux] backend` choice (and the TUI settings editor rewrites
  it), so it must not travel to teammates on other machines or OSes. A `.gitignore` entry does not
  untrack an already-committed file: existing repos run `git rm --cached .bmad-loop/policy.toml`
  once (the local copy is kept; `init` prints this hint when it detects a tracked policy).
  bmad-loop's own worktree-clean preflight already exempted policy.toml — this additionally stops
  inner dev sessions and plain `git status` from reading a policy edit as a dirty tree.
- **The patch-restore seam is now one validator, one path normalizer, and one exclusion site.**
  `runs.validate_restore_latch` holds every latch precondition (sentinel wedge, spec-less escalation,
  worktree isolation) — the worktree check lived only in the CLI, so `rearm_escalation` called
  programmatically could latch a patch the re-drive can never honor; it now rejects it too.
  `verify.resolve_restore_path` replaces four copies of the maybe-relative→absolute join, and the
  shared verify gate derives the restore-patch proof-of-work exclusion from the task instead of
  threading it in from three call sites. The resolve context's `restore_supported` signal is now the
  validator's verdict too, so the agent never negotiates a restore for a sentinel-wedged or spec-less
  escalation either. Otherwise behavior-neutral. (closes #91)
- **Test helper fidelity.** `make_engine` seeds the launching scope (`max_stories`, `story_filter`,
  `epic_filter`) on `RunState` like `cmd_run` does, so resume tests no longer silently ran uncapped;
  the three `_escalated_run` fixtures collapse into one parameterized conftest builder. (closes #84)

### Fixed

- **Locale-stable rollback (#236).** Git subprocesses now run with `LC_ALL=C`, so `safe_rollback`'s
  benign "pathspec did not match" no-op is no longer misread as a hard failure under a localized git
  (e.g. `LANG=it_IT.UTF-8`) — which had turned a resolvable re-drive into a rollback pause. Forced at
  the single `_run_git` spawn point, so every git message the orchestrator inspects stays English.

- **The parked-window return target is now backend-composed (#221).** An interactive attach
  recorded the client's origin as a bare pane id (`%N`) and replayed it as `switch-client -t %N`
  from inside the control session — sound under tmux's one-server model, but on psmux (one
  server per session, upstream-final per psmux/psmux#483) a bare id is session-local: at best
  unresolvable, at worst colliding with a real control-session pane and landing the client on
  the wrong one with exit 0, past the `switch-client -l` fallback. No single form resolves on
  every backend (tmux's window resolver rejects a pane id in the `session:%N` slot, and a
  native-id backend needs its own id passed through untouched), so the recording seam now asks
  the backend: `TerminalMultiplexer.current_return_target()` defaults to the bare native pane
  id — tmux and native-id backends behave exactly as before — and psmux overrides it to emit
  `=session:%N`, which releases carrying the psmux/psmux#483 fix resolve cross-server,
  degrading to the bare id only if the session probe fails. The replay sides treat the value
  as an opaque target and are unchanged.

- **A `worktree_seed` entry that silently copies nothing is now journaled (#230).** Under
  worktree isolation `provision_worktree` copies a seed only when the destination is absent —
  right for a file the checkout legitimately carries, but a _directory_ entry is skipped whole
  the moment any child is tracked, so `worktree_seed = ["_bmad"]` with a tracked `_bmad/custom`
  copies nothing at all, including the absent children that would clobber nothing. Provisioning
  is quiet by contract (it runs under the TUI), so the skip was invisible: user-authored config
  that reads as applied was a no-op. It now returns the skipped entries and the engine records a
  `worktree-seed-skipped` journal event; glob-expanded matches are excluded, since a plugin glob
  is expected to hit paths the checkout already carries. Behavior is otherwise unchanged —
  nothing new is copied.

- **A dry run the TUI cannot spawn opens a modal instead of taking the app down (#210).** The
  `run --dry-run` / `sweep --dry-run` workers called `run_captured` unguarded, and
  `@work(thread=True)` defaults to `exit_on_error=True` — so an `OSError` from the spawn itself
  (a venv deleted out from under `sys.executable`, `EAGAIN` off a loaded process table) escaped
  the worker and killed the whole app rather than the one modal. Both workers and the validate
  degrade now share a guard that reports the reason in the modal body.

- **`--json` output survives a console that cannot encode it (#200).** A JSON document is not
  necessarily ASCII: `diagnostics.render_json` serializes with `ensure_ascii=False` so its leak
  guard can scan values unescaped (#195, below), which lets a _non_-sensitive non-ASCII field —
  a localized `platform.release()`, say — reach stdout verbatim. Printing it to a console whose
  encoding could not carry it raised `UnicodeEncodeError`, in practice a legacy non-UTF-8
  Windows one. It failed safe rather than silently — the encode runs before any write, so
  stdout stayed empty instead of half-written — but `diagnose --json` still died on a machine
  where `--out FILE` would have worked. `machine.emit_document` now switches stdout to UTF-8
  before writing. Re-serializing the document as escaped ASCII would have been the smaller
  change and the wrong one: the leak check verified the unescaped bytes, and emitting anything
  re-derived from them is what that helper exists to prevent. `--out FILE` was never affected;
  it has always written `encoding="utf-8"`.

- **Leak self-check now matches JSON-escaped values (#195).** Two evasions became reachable
  the moment `diagnose --json` stopped also rendering the markdown report, since that raw-text
  pass was what had been catching them: `json.dumps` doubles backslashes, so a Windows home
  path (`C:\Users\…`) serialized to a form `_ABS_HOME_RE` did not match, and its default
  `ensure_ascii=True` escaped non-ASCII sensitive values to `\uXXXX`, hiding them from the
  pseudonymizer's stray-original check while `json.loads` handed the consumer back the
  original. The home-path rule now matches either separator form, and `diagnostics.render_json`
  serializes with `ensure_ascii=False` so the guard sees values as themselves. Both apply to
  the markdown path too; neither changes what a clean dump contains.

- **Resumed runs display the policy they actually enforce (#189).** `policy_snapshot` was
  stamped only at run creation. `resume` reloads `policy.toml` and enforces it — the
  per-story budget, every `SessionSpec` — but left the launch-time snapshot in place, and
  every display reads the snapshot: the run summary, `bmad-loop status`, the TUI, and the
  `policy` block of the `diagnose` bundle, which claimed to describe the run that was
  executed. Edit `limits.cache_read_weight` between launch and resume and the run enforced
  at the new weight while every surface reported the old one, silently up to 10x apart at
  the legal extremes (0.0–1.0). Resume now re-stamps the whole snapshot and persists it
  before the engine starts, restoring the documented contract that policy edits apply to
  resumes. A single `session-end` entry could likewise carry `tokens_weighted` at the
  snapshot weight beside `budget_weighted` at the live one; the two now agree by
  construction. Run scope and mode (`source`, `spec_folder`, `epic_filter`, …) stay pinned
  at launch as before — a policy edit still cannot redirect a live run.
  **Visible output change:** a run resumed across a weight edit re-weights its _whole_
  history, not just post-resume sessions, since totals are recomputed from raw counts (this
  is what the budget always did). A pre-0.8.2 run with no snapshot at all gets one on its
  first resume, so it stops displaying at the hardcoded 0.1 default. `run-resume` journal
  entries now carry `cache_read_weight`, `policy_changed`, and `cache_read_weight_was` when
  it moved, keeping per-session totals written under the old weight reconstructible.

- **Run summaries and `bmad-loop status` report weighted tokens, with both units labeled
  (#129).** The run-finished summary — stdout, the `ATTENTION` file, and the desktop
  notification all render from one place — reported the **raw** total, counting cache reads
  at full price, while every budget judges the **cost-weighted** total. On a cache-heavy run
  that overstates spend by ~6.5x, and neither figure said which unit it was. Both surfaces
  now lead with weighted and name both: `<weighted> weighted tokens (<raw> raw incl. cache
reads)`, matching the TUI, which has shown weighted since 0.7.12. `bmad-loop status` also
  gained a run-level `tokens:` line (it previously printed no run total at all).
  **Visible output change:** per-story `status` cells go from `<raw>t` to
  `<weighted>t (<raw> raw)`, so the number is both differently scaled and differently
  shaped — scripts scraping that column need updating. A story with only cache reads under
  `cache_read_weight = 0` correctly renders `0`, not `-` (which means no tokens at all).
  Displayed weights come from the run's persisted policy snapshot, so every observer
  reproduces the same number from `state.json` alone.

- **The TUI guide's task-table reference described the pre-0.7.12 columns.** It documented
  `tokens` as the raw total and omitted the `raw` column entirely; the run-header and
  journal sections were likewise silent on the weighted/raw split. Docs only.

- **`diagnose` leak self-check is now recoverable (#186).** A stray pseudonymized
  identifier (a per-field routing gap) is repaired by substituting its alias and disclosed
  in the report and on stderr, instead of refusing to emit any dump; residual failures name
  `sensitive[<ns>:<alias>]` instead of an opaque index, and the local `--legend` file is
  written even on refusal so the operator can decode it. PII/secret/path/username hits
  still fail closed.

- **Deferred-work bundles that adopt an existing story spec pass the baseline gate (#161).** A
  "follow-up review of story X" bundle is routed by `bmad-dev-auto` into that story's done
  spec, whose `baseline_revision` is the story's original dev baseline — necessarily older
  than the bundle's worktree cut, so the exact-match gate failed every such bundle after the
  session had already done its work. The bundle gate now accepts a claimed baseline that is
  an _ancestor_ of the orchestrator-recorded one (the session diffed a superset of the
  unit's changes); diverged or unknown baselines still fail, any git fault in the probe
  reads as not-an-ancestor, and sprint/stories modes keep the exact-match requirement.

- **A failed attempt inside a unit worktree auto-recovers instead of pausing with in-place
  instructions (#161).** The mid-drive dev retry was the only recovery path without an
  isolation guard: with `rollback_on_failure = false` it paused the run with manual-recovery
  instructions aimed at the operator's checkout — whose HEAD _is_ the baseline under
  worktree isolation, while the commits sat on the unit branch, so following them literally
  did nothing and invited a destructive reset of a tree the attempt never touched. A mounted
  unit worktree is disposable: the attempt's commits are parked on `attempt-preserve/` refs
  and the worktree resets regardless of the flag, which gates in-place (`isolation = "none"`)
  recovery only. The remaining reachable pauses name their tree (`git -C "<root>" …`).

- **A failed worktree teardown no longer crashes the run after the merge landed (#139).** When a
  process the just-ended session left running (e.g. pytest recreating `.pytest_cache`) makes
  `git worktree remove` fail with ENOTEMPTY, git still drops its admin entry, so the `force=True`
  retry failed with "is not a working tree" and that second `GitError` crashed the run. The
  teardown tail of `close_unit_workspace` never raises now: a failed worktree removal falls back to
  `rmtree` + `worktree prune` (the rmtree confined to the run's own worktrees dir — the path can
  arrive from persisted state), a failed branch delete is reported and swallowed, and both journal a
  `worktree-teardown-degraded` event — teardown is post-merge housekeeping. A failed forensic diff
  capture instead preserves the worktree + branch (they hold the only copy of a dropped unit's
  changes). `discard_worktree` gains the same removal fallback so a stuck dir can't block the
  resume re-mount.

- **A git call exceeding its timeout no longer crashes the whole run (#156).** Every git
  subprocess the orchestrator spawns now translates `subprocess.TimeoutExpired` into
  `GitError`, so the existing degrade guards handle a slow git like any other git failure.
  The rollback gate specifically (`_rollback_or_pause`'s dirty check — the reported crash
  path) degrades to assume-dirty: rollback OFF pauses with the manual-recovery notice and
  the worktree kept; ON / resolved re-drives still auto-recover behind their preserve
  steps. A `rollback-dirty-check-failed` journal entry records the fault. The bound is now
  configurable as `limits.git_timeout_s` (default 120).

- **Session timeouts now fire on time and leave a forensic trail (#157).** A
  `session_timeout_min` that fired but journaled its session-end 2h19 late — with zero record
  of _when_ the deadline was declared or why — is now timely and observable on three fronts.
  (1) `wait_for_completion` gains a **wall-clock co-bound**: a host suspend (macOS sleep)
  freezes `time.monotonic()`, silently extending the monotonic deadline by the nap's length;
  the wall clock keeps counting through a suspend, so it may now EXPIRE the deadline — never
  extend it (a stepped-back wall clock changes nothing, and all sub-waits stay monotonic).
  (2) The fire moment stamps the result (`timeout_fired_at`, `timeout_expired_clock` —
  `"wall"` alone is the suspend fingerprint) and appends a `timeout-fired` line to
  `tasks/<id>/session-lifecycle.jsonl`; each wait tick tops up a throttled
  `tasks/<id>/heartbeat.json` whose staleness under a still-live session diagnoses a frozen
  orchestrator (the previously uninstrumented gap). The engine journals **session-end
  unconditionally** — even a teardown that throws still records the ended session (status
  `aborted` when the outcome is unknowable), carrying `fired_at`/`teardown_s`/`expired_clock`.
  (3) Teardown is now a **verified kill escalation**: `terminate → wait → force_kill`, where
  `limits.teardown_grace_s` bounds the liveness-wait before escalating (default 20; `0` = a
  single unverified best-effort kill) and every escalation step carries its own bound, so a
  timeout can no longer hang on an unkillable session. Covers the tmux (`generic`) and
  `opencode-http` adapters alike. A frozen
  process still cannot run this code while frozen, but recurrence is now diagnosable rather
  than silent.

- **`validate` and `probe-adapter` no longer report antigravity's hooks as unregistered
  (#159).** The `antigravity-hooks-json` dialect keys `.agents/hooks.json` by hook-group name
  at the top level, with no `"hooks"` wrapper — but both readers looked up `"hooks"`, got `{}`,
  and reported a correctly-installed relay as missing (`FAIL: bmad-loop hooks not registered
for antigravity`, immediately after a successful `init --cli antigravity`). Both now share
  one `install.relay_registered()` helper that resolves each dialect's container shape, so the
  two call sites can no longer drift apart. `init`'s merge dedup keys on the narrow bmad-loop
  script markers rather than the bare `bmad_loop` substring, so an unrelated hook command whose
  path merely contains `bmad_loop` can't make init skip a registration that validate would then
  report missing.
- **The antigravity hook relay now reads agy's payload keys.** agy encodes hook payloads as
  protojson — `conversationId`, `transcriptPath`, `workspacePaths` — while the relay only tried
  snake_case plus copilot's `sessionId`. Every agy event therefore recorded a null
  `session_id`, and `cwd` was never populated (agy sends no `cwd`, only a `workspacePaths`
  list). Both the relay and the probe capture hook now try agy's casing, verified against a
  live 1.1.3 turn.
- **`probe-adapter antigravity` finds the transcript.** The shipped convention glob had the
  wrong filename — agy writes `transcript_full.jsonl`, not `transcript.jsonl`, under
  `~/.gemini/antigravity-cli/brain/<conversationId>/.system_generated/logs/`. Corrected against
  a live capture. A live `--probe` now also prefers the `transcriptPath` the CLI hands the hook
  on stdin over the convention glob: the payload names _this_ turn's file, while a glob can
  only take the newest match and may land on an unrelated session.
- **antigravity: `usage_parser = "none"` is now documented as permanent, not pending.** A live
  capture confirmed agy's transcript carries only
  `step_index`/`source`/`type`/`status`/`created_at`/`content`/`thinking` — no usage block
  anywhere. agy does count tokens, but only inside `conversations/<id>.db`, an undocumented
  SQLite/protobuf store outside the `(transcript_path) -> TokenUsage` parser contract. Runs
  work; token columns stay empty.
- **antigravity: trust is exact-path (verified against `agy` 1.1.3).** `agy` blocks on an
  interactive "trust this folder" dialog for any workspace not listed verbatim in
  `settings.json` `trustedWorkspaces`; a trusted parent does not cover subdirectories, and
  `--dangerously-skip-permissions` does not bypass it (it covers tool permissions only).
  `isolation = "none"` (the default) works; `isolation = "worktree"` hangs on every run, since
  each worktree is a fresh untrusted path — now called out in the profile and setup guide, and
  tracked in #169. Replaces the profile's previous "verify during probe" placeholder.
- **Follow-up review sessions are no longer killed on their first Stop by the dev pass's stale
  `## Auto Run Result` (#160).** The review leg re-invokes bmad-dev-auto on the finalized (`done`)
  spec whose dev pass left that terminal marker; the review's own entry write lifted it past the
  adapter's launch-mtime floor, so the first result-less Stop read the stale marker as this
  session's result and ended the review mid-flight (the #109 stall grace never armed). The engine
  now strips the marker before every review launch — the frontmatter `done` stays, so step-01
  still routes to a review pass. The review-budget exhaustion defer reason now reports the last
  pass's actual status instead of always claiming a lingering follow-up recommendation.
- **`branch_per=run` + `keep_failed` no longer poisons a multi-story run after the first kept
  failure (#138).** The first story to end deferred under `keep_failed=true` left its worktree
  checked out on the single shared run branch, so every subsequent story's `git worktree add`
  collided ("branch already checked out") and insta-deferred with zero dev activity — one kept
  failure turned an N-story run into a 1-story run. A kept worktree under `branch_per=run` now
  detaches its HEAD (`git checkout --detach`), freeing the shared branch name for the next story
  while preserving the working tree, uncommitted changes, and the branch ref (still at the kept
  commit) for inspection; subsequent stories mount the run branch normally and get genuine
  attempts. Best effort — if the detach ever fails, the existing `worktree-open-failed` defer
  still surfaces the collision (no regression). The escalate-and-pause path was already safe: it
  halts the run rather than continuing, and resume frees the kept worktree before any sibling mounts.

- **Dev/review sessions can no longer livelock on their own wake nudges (#149).** The idle
  wake nudge is delivered as a submitted turn, so a session that merely _answers_ it ends in
  another result-less Stop — which refilled the nudge budget, re-armed the grace window, and
  repeated until `session_timeout_min`, burning a turn per cycle. Dev/review sessions now get the
  same monotonic cap injected workflow sessions already had: after `limits.dev_stall_nudges_cap`
  (default 6) total nudges the session is declared stalled instead (post-kill reconcile still
  rescues a finished one whose terminal artifact is on disk). The nudge text now also states that
  a prose reply cannot end the session. And each result-less Stop leaves a diagnostic breadcrumb
  (`tasks/<task_id>/resultless-stops.jsonl`: pending / not-terminal / stale-mtime / ambiguous /
  no-artifact / no-result-json) so _why_ a completed-looking session read as result-less is
  answerable from the run dir.

- **Split-story keys (`2-6a-…`) are no longer silently skipped (#144).** The sprint-status
  parser rejected story numbers carrying BMAD's split-story letter suffix, dropping exactly the
  stories that were split to be loop-tractable — invisible to `run`/`--story`/the TUI tree, and
  skipped by the epic-lift. The suffix is now a first-class `Story`/selector field: `--story 2-6a`
  (or `2.6a`, or `--epic 2 --story 6a`) selects exactly that half, while a plain `2-6` selects the
  whole `2-6a`/`2-6b` family in file order. `run` and `--dry-run` also print a stderr warning when
  sprint-status keys remain unparseable, instead of only journaling them.

- **Review leg repairs a finalize-tail death.** A review session that died between writing its
  terminal `## Auto Run Result` (`Status: done`) and flipping the spec frontmatter off the transient
  `in-review` marker left the orchestrator re-reviewing already-finished work — a burned review
  cycle. The review leg now runs the same terminal-status reconcile the dev leg does: when the prose
  says done and the frontmatter sits at a reconcilable non-terminal status, it advances the spec to
  `done` and re-folds the frontmatter's `followup_review_recommended` flag (only when present) before
  the convergence/damping gate reads it. Bookkeeping-only — every deterministic verify gate still
  runs against real on-disk/git state, so it cannot pass uncompleted work.

- **Claude sessions launch with `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` (#109).** Claude Code
  could bias a dev session toward backgrounding its implementation sub-agent despite the
  bmad-dev-auto prompt ban; the session then ended its turn to await a completion notification,
  and a harness exit at that turn boundary stranded the sub-agent with the story stuck
  `in-progress` → manual-rollback pause. The shipped claude profile now forces subagents and bash
  to run synchronously — the behavior the skill contract already requires. Opt out with a custom
  profile in `.bmad-loop/profiles/`.

- **Resume no longer discards a story that already passed its pre-commit gates.** A host death in
  the COMMITTING window (phase persisted before `finalize_commit` ran and the DONE save stamped
  `commit_sha`) matched no resume arm — there is no COMMITTING-keyed session record to replay — and
  fell through to resume-restart, rolling back or pausing over fully-verified work. Resume now
  finishes the commit in place: the `pre_commit_gate` workflows are not re-charged (the persisted
  phase is durable proof they passed), the `pre_commit` hook re-fires (message regeneration and
  pause veto honored), and `finalize_commit`'s content-idempotence covers both the pre- and
  post-squash crash states. Sweep bundles get the same recovery in `_recover_inflight_bundle` (#115).

- **Resume no longer asks for a rollback of a completed session's committed work.** A host death
  in the post-verify decision window left the task persisted at `DEV_VERIFY`/`REVIEW_VERIFY`,
  where the resume replay matcher (which only knew the `*_RUNNING` phases) missed the
  durably-recorded completed session and fell through to resume-restart — pausing with a
  `git reset --hard <baseline>` instruction that would discard the attempt's finished, possibly
  already-pushed commits. Those phases now replay the recorded result through the normal
  verify/decide pipeline, and the rollback-OFF manual-recovery notice detects commits above
  baseline and leads with saving/checking them instead of a bare reset (#100).

- **The TUI no longer crashes on a private-mode CSI sequence in an adapter log.** The gemini
  CLI's startup burst includes XTMODKEYS `CSI > 4 ; ? m`; the marker byte sat _inside_ the
  params, so the private-marker strip filter missed it and pyte 0.8.2 raised a `TypeError`
  that killed the poll worker — and the whole dashboard. The filter now matches a marker
  anywhere in the params, and any escape sequence pyte still can't parse is dropped instead
  of propagating (upstream fix exists but was never released — selectel/pyte#202) (#111).

- **An unreadable spec no longer crashes the whole run.** Every spec read-back — the four verify
  gates, the reconcile/sprint/ledger bookkeeping passes, and the generic adapter's Stop poll — raced
  the dev skill's own writes, so a transient `OSError` (a TOCTOU truncation, a lock, an EACCES)
  escaped to `engine.run()` and abandoned every remaining story. Observation now degrades where
  repair still raises: verify gates return a retryable outcome naming the read fault (never a phantom
  status mismatch), bookkeeping passes skip and journal `spec-read-failed`, and the read-back poll
  treats it as not-yet-terminal, falling through to the existing stall/timeout → post-kill-reconcile
  ladder. Review routing re-derives `followup_review_recommended` from the finalized spec when a
  replayed result lacks it, so a fault that skips the reconcile re-fold can no longer silently skip
  a recommended follow-up review on resume (#97).

- **A resumed sweep re-drives its in-flight bundles by identity, not by bundle name.** `SweepEngine`
  recovered a bundle only from inside `_run_bundle`, which a cycle reaches after re-deriving the key
  from the _current_ triage plan — so a bundle re-armed by `bmad-loop resolve` survived a resume only
  because the cached `triage.json` reloaded and re-emitted the same name. Lose that cache and a fresh
  triage partitioned the ids under new names, silently orphaning the human's resolution. The sweep
  loop now opens with `_finish_inflight_bundles`, mirroring the base engine: every non-terminal `dw*`
  task is re-driven under its own persisted `story_key`, before the ledger is read, so its ids leave
  the open set and no fresh plan can re-bundle them. A still-escalated bundle stays terminal and
  untouched. A missing bundle intent file is regenerated from the task (the verbatim ledger entries
  become the contract; the triage prose is the only unrecoverable piece), and a bundle that survives
  to a cycle anyway is journaled + notified rather than dropped. Relatedly, a truncated or
  wrong-shaped `triage.json` now degrades to a fresh triage instead of crashing the whole run — the
  corrupt leg of this bug was previously unreachable. New journal events: `sweep-inflight-redrive` /
  `-stranded`, `sweep-intent-regenerated`. (#94)
- **Run ids are validated, so a run ref can no longer escape the runs directory.** A positional ref
  (`delete`, `stop`, `archive`, `resume`, `status`) was recomposed into a path raw, so
  `bmad-loop delete ../../x` deleted any outside directory holding a `state.json`; the hidden
  `--run-id` flag on `run`/`sweep` reached a directory name, a multiplexer session name and a git ref
  unchecked. A supplied id must now match `[A-Za-z0-9][A-Za-z0-9_-]*` (≤ 120 chars, no reserved
  Windows device name) — rejected, never sanitized, so ids stay bijective with paths and sessions —
  and a ref that is absolute, climbs with `..`, or carries a separator skips the exact-match branch,
  falling through to partial matching over enumerated run dirs only. Ids recovered from the outside
  world — a `bmad-loop-<id>` session name, a `<kind>-<id>` control-session window name — pass the
  same validator before they steer a path. Partial refs unaffected (#104).

- **An abandoned patch-restore no longer smuggles its files into the corrected story's commit.**
  Re-arming a story whose previous re-drive had already applied a restore patch snapshotted that
  patch's new (untracked) files as _pre-existing_, so every later rollback preserved them and
  `finalize_commit`'s `add -A` swept the abandoned attempt into the corrected commit. The re-arm now
  parses the old latch (`verify.patch_new_files`) and subtracts its creations from the refreshed
  baseline snapshot — the re-drive's own reset then removes them. Best-effort: a missing or
  unreadable patch degrades to the old behavior instead of failing the resolve. Commits the
  escalated attempt left below the advanced baseline can't be reverted mechanically (the resolve
  session's own commits share that range), so they are journaled and echoed to stderr for the human
  to classify. New journal events: `stale-restore-excluded` / `-unparseable` / `-commits`.
  (closes #90)
- **Baseline-era untracked residue no longer vacuously satisfies the proof-of-work gate.**
  `has_changes_since` counted every untracked file. After an intent-gap halt the saved patch is
  untracked residue under the artifact dirs every reset deliberately protects, so a from-scratch
  re-arm — which never learns the patch's path — let a re-driven session that produced nothing but a
  spec status flip pass the gate on that file's mere presence, and `finalize_commit`'s `add -A` swept
  it into the story commit. The gate now subtracts the task's `baseline_untracked` snapshot. A `None`
  snapshot (a pre-upgrade run) still counts every untracked file — deliberately the opposite of
  `attempt_dirty`'s ignore-all, because a proof-of-work gate has to fail open toward "work happened".
  (closes #88)
- **The baseline-match verify gate was dead code for generic dev sessions.** The gate read the spec's
  `baseline_commit` and skipped itself when that key was absent — but `bmad-dev-auto` stamps
  `baseline_revision`; `baseline_commit` exists only in the orchestrator's synthesized `result.json`.
  In production the check never fired, so a spec claiming a stale or foreign baseline sailed through.
  The gate now reads either key, the idiom `devcontract` already used. The test fixture stamps
  `baseline_revision` like the real skill does, so it can no longer fabricate the key that hid this.
  (closes #89)
- **Unit keys with git-ref-illegal characters no longer break worktree runs.** `unit_branch_name`
  built `bmad-loop/<run_id>/<unit_key>` from the raw ids, so a key or `--run-id` carrying `:`, `..`,
  `@{`, a space or a trailing `.lock` cleared the (already-sanitized) worktree dir only to die at
  `git worktree add` with _"is not a valid branch name"_. Both segments now go through a new
  `platform_util.safe_ref_segment` — identity for clean ids, `-<hex8>` digest suffix otherwise, on
  git's alphabet rather than Windows' (`CON` is a legal ref; `a..b` is a legal filename). A
  `git check-ref-format` oracle test pins the agreement; the `attempt-preserve` recovery-ref slugs
  now reuse the same sanitizer instead of their own inline one. (closes #102)
- **The deferred-artifact stash overwrites its target atomically.** A story deferring a second time
  re-stashes the same spec filename over the previous one. `shutil.move` fell back to a non-atomic
  `copy2` there — which tears the stash on a mid-copy crash and fails outright on Windows when an
  AV/indexer handle turns the rename into a sharing violation. The stash now stages a copy inside the
  destination dir and routes through `platform_util.atomic_replace`, inheriting its win32 retry; the
  source removal gets the same retry via a new `platform_util.retrying_unlink`, since Windows denies a
  delete against an open handle exactly as it denies a rename-over. (closes #101)
- **A finished session whose final `Stop` hook was lost no longer loses its work.** A dev/review
  session that wrote its terminal spec but never delivered the `Stop` ended `stalled` — or `timeout`,
  when hooks were misconfigured and no event ever arrived — and the on-disk result was discarded.
  The adapter now re-reads the spec after the window is provably dead, rescuing a self-consistent
  successful terminal; every rescue still faces the full deterministic verify, and the journal records
  `session-rescued-post-kill` so it stays distinguishable from a live completion. (#95, closes #61)
- **A corrupt terminal artifact no longer crashes the whole run.** A spec truncated mid-write (a
  multi-byte UTF-8 sequence cut in half) raised out of the read-back and past the per-task boundary,
  marking the run `CRASHED` and abandoning every remaining story. The read-back now degrades an
  undecodable spec to "no result yet" — the session retries or keeps its verdict — and the post-kill
  rescue additionally keeps its verdict on _any_ read fault, so a best-effort rescue can never make
  things worse. The repair path still raises on purpose. (#95, closes #96)
- **Windows installs now pull `psutil` automatically** — moved from the opt-in `non-linux` extra to a
  platform-scoped core dependency (`sys_platform == 'win32'`), so the TUI liveness column no longer
  shows every run as `?` on a stock install. macOS keeps the `non-linux` extra; Linux stays dep-free.
  (#72, closes #71)
- **`bmad-loop-setup` no longer deletes live core BMAD config or the installer manifest.** In a
  multi-module BMAD v6 project the setup scripts hardcoded `core` (and `--also-remove _config`) into
  their delete lists, destroying `_bmad/core/config.yaml`, per-module config, and the whole
  `_bmad/_config/` manifest — breaking future `npx bmad-method install` upgrades. Cleanup now removes
  a directory only when it is a verified-redundant skill payload (has a `SKILL.md`, carries no
  config/manifest, and its skills are installed); live config dirs are protected and reported under
  `directories_protected`. The merge scripts read legacy config as fallback but never delete it. Same
  root cause as upstream `bmad-code-org/bmad-builder#96`. (closes #64)

## [0.8.1] — 2026-07-05

### Added

- **Attempt-preserve recovery refs are now bounded.** With `scm.rollback_on_failure` on, auto-rollback
  parks a failed attempt's committed work under `attempt-preserve/*` and its dirty worktree snapshot
  under `attempt-preserve-dirty/*`; nothing pruned them, so they grew unbounded. Run start now keeps
  only the newest `scm.preserve_keep` (default 20, `0` = never prune) per family by committer date and
  best-effort-deletes the tail — a stuck ref never wedges the ones behind it, and prune failures are
  journaled but never block the run. (#50 #54, closes #32 #49)

### Changed

- **The adapter shell-dialect seam is now an explicit, documented contract.** `new_window` /
  `new_parked_window` factor their shell-dialect fragments into overridable hooks (POSIX output stays
  byte-identical), and the `command` parameter's semantics are pinned in the ABC docstring
  (shlex-joined argv; operator handling is backend-defined). Relevant only to authors porting the
  adapter to a non-POSIX backend. (#47 #60)

### Fixed

- **A session that finished its work but crashed before the run recorded it no longer loses that work
  to a restart-and-rollback.** The engine now records a completed dev/review session behind a
  durability barrier _before_ running post-session hooks (usage is folded in afterward as best-effort
  metadata); on resume it consumes that durably-recorded result straight into verify/decide instead of
  restarting the attempt from baseline. A raw `KeyboardInterrupt` now records a controlled stop, and
  replay preserves the attempt/cycle/baseline. (#62, closes #57)
- **Several narrower resume-replay edges opened by that durability work are closed.** A host death in
  the post-session window of the _last_ allowed review cycle no longer drops a recorded clean review to
  a defer; a reconcile early-return no longer persists a pre-reconcile dict that could silently skip a
  recommended follow-up review; and triage/sweep and labeled plugin-workflow sessions no longer persist
  large, never-consumed result payloads into `state.json`. (#63)
- **A dev session is now completed only on a real Stop or window death, never on a terminal artifact
  glimpsed while the agent window is still alive.** The idle-tick and grace-expiry shortcuts could
  return "completed" mid-turn and let the run's cleanup kill a working agent, handing the engine
  half-written state. Both shortcuts are removed, liveness is re-probed immediately before the
  grace-expiry stall verdict, and a re-driven spec has its stale `## Auto Run Result` section stripped
  on both re-arm paths so a resolved re-drive can't be misread as its own terminal result. Result scans
  are now fence-aware, so an `## Auto Run Result` heading quoted inside a fenced code block is never
  mistaken for a real section (nor destructively stripped). (#53, closes #48 #52)
- **Long journal fields in the TUI now wrap with a hanging indent instead of spilling back under the
  timestamp and kind columns.** Each row renders as a fixed-width grid whose fields cell folds within
  its own column.

## [0.8.0] — 2026-07-03

### Added

- **New `pre_commit_gate` plugin workflow-injection stage.** Gate workflows can bind to
  `pre_commit_gate`, which fires unconditionally just before every commit — on the review-converged,
  review-skipped, and review-budget-rescue paths alike — while the phase can still legally defer.
  TEA's trace/nfr/review gates rebind to it, fixing blocking gates that were previously inert
  whenever a dev session recommended no review follow-up (so `on_pre_commit` fail-opened on the
  missing artifacts).

### Changed

- **BREAKING: the project is renamed `bmad-auto` → `bmad-loop`.** The distribution, console script,
  and CLI are now `bmad-loop`; the Python package is `bmad_loop` (was `automator`); the BMAD module
  code and marketplace plugin are `bmad-loop` (was `bauto`); per-project state moves from
  `.automator/` to `.bmad-loop/`. The GitHub repo is now
  [bmad-code-org/bmad-loop](https://github.com/bmad-code-org/bmad-loop) — old web and git URLs
  redirect. Clean break: no compatibility shims.
- **BREAKING: renamed public identifiers.** Env vars `BMAD_AUTO_*` → `RIAWORKS_BMAD_LOOP_*`; plugin
  entry-point group `bmad_auto.plugins` → `bmad_loop.plugins`; hook relays `bmad_auto_hook.py` /
  `bmad_auto_probe_hook.py` → `bmad_loop_hook.py` / `bmad_loop_probe_hook.py`; skills
  `/bmad-auto-{setup,sweep,resolve}` → `/bmad-loop-{setup,sweep,resolve}`; tmux session/window
  prefixes `bmad-auto-*` → `bmad-loop-*`; worktree branches `automator/<run-id>` →
  `bmad-loop/<run-id>`; TUI class `BmadAutoApp` → `BmadLoopApp`. Custom plugins, CLI profiles, and
  policy files that reference any of these must be updated.

### Fixed

- **A workflow session that finishes its work but never writes a completion marker no longer
  livelocks the run.** Each result-less Stop used to refill the stall-nudge budget, re-nudging a
  responsive-but-signal-less session until `session_timeout_min`. The engine now appends an explicit
  completion contract (absolute marker path + frontmatter shape) to every workflow-session prompt,
  and a new `limits.workflow_stall_nudges_cap` (default 3) caps the total nudges a workflow session
  may receive — degrading a still-missing marker to "stalled" in ~30 min instead of hours. Dev/review
  session nudging is unchanged.
- **On Windows, a live engine whose process identity can't be read now shows `UNKNOWN` instead of a
  false `INTERRUPTED`.** psutil raises `ERROR_ACCESS_DENIED` for a process in another session or
  elevation, which the identity-aware liveness read had surfaced as dead — mislabeling running runs
  and weakening the resume/delete guards. Liveness is now tri-state (`alive`/`dead`/`unknown`) and
  biased away from false-dead; `resume`, `resolve`, `delete`, `archive`, and cleanup all surface and
  warn on `unknown` without ever letting an unverifiable pid block cleanup forever, and `resolve`
  gains `--force` to override a squatted-pid block.
- **A review session that appends to the deferred-work ledger no longer leaves a sweep bundle
  unclosed.** The bundle ledger is reclosed after review (journaled distinctly as
  `sweep-bundle-reclosed`), and the review prompt now states the ledger is append-only for sessions.
- **Worktree git-exclude patterns now anchor correctly on native Windows.** `install.py` normalizes
  backslashes in the per-worktree exclude paths so the ignore rules match (a no-op on POSIX).

### Migration

- **Reinstall the tool under its new name** — uv can't rename a package in place:
  `uv tool uninstall bmad-auto`, then
  `uv tool install "bmad-loop[tui] @ git+https://github.com/bmad-code-org/bmad-loop.git"`.
- **Re-run `/bmad-loop-setup`** (or `bmad-loop init` directly). `init` migrates a project in place:
  it strips the old `.automator/` Stop hook from each CLI's settings, removes the `bmad-auto-*`
  skill dirs, and carries `.automator/policy.toml` over to `.bmad-loop/policy.toml`. Setup folds the
  old `bauto` config into `bmad-loop` and clears the leftover `bauto` config section, stale
  `BMAD Automator Skills` help rows, and the `_bmad/bauto/` installer dir.
- **Legacy `.automator/` is left in place** (runs, archives, profiles, plugins) and can be deleted
  or hand-moved once the migration is confirmed; stale `.automator/*` gitignore lines are left
  untouched.

## [0.7.12] — 2026-07-01

### Added

- **The TUI dashboard now shows the cost-proportional weighted token total, with the raw total in a new
  column.** The `tokens` column and the run-header summary discount cache-read tokens by the run's
  `cache_read_weight` — the same weighting the per-story budget enforces — so the headline number
  tracks spend rather than context re-reads; the previous unweighted total moves to a new `raw` column.

### Fixed

- **The dashboard no longer crashes when a background poll lands as the screen is torn down or
  switched away.** A poll worker delivers its refresh on the UI thread; if that arrived just as the
  app quit or another screen opened, the query for the run table raised `NoMatches`. The apply now
  drops stale refreshes for a screen that is no longer running (while still updating one merely
  backgrounded under a modal).
- **A failed attempt's work is preserved before an auto-rollback hard reset instead of being silently
  discarded.** With `scm.rollback_on_failure` on (or on a resolved re-drive), a deferred or stopped
  attempt's commits above baseline are now parked under an `attempt-preserve/<run_id>-<head8>` branch,
  and its uncommitted working-tree diff — tracked edits and run-created untracked files alike — under
  `refs/attempt-preserve-dirty/`; both are recoverable by name and survive gc. A plain rollback that
  cannot create the ref refuses to reset and pauses for manual recovery rather than destroying work.
  The uncommitted snapshot is scoped to this run's own changes (never a pre-existing untracked file),
  commits under a synthetic identity so it works with no git user configured, and is keyed per retry
  so repeated rollbacks against the same baseline no longer overwrite each other's recovery ref.
- **Process liveness is now identity-aware, so a reused PID no longer reads as a live run.** A recycled
  pid (common on Windows) used to register as a false "alive" — blocking resume of a dead run,
  stranding worktree reclaim, leaking sessions, and showing dead runs as RUNNING. The pid file now
  carries a process-identity token that resume, stop, and the TUI verify against; on win32 the engine
  also ignores console SIGINT/SIGBREAK during a run so a ConPTY Ctrl+C broadcast can't kill it.
- **A story from a resolved escalation that still can't finish now re-escalates instead of being
  silently deferred.** When a human-resolved CRITICAL `blocked` escalation was re-driven and the
  re-drive couldn't reach `status: done` (e.g. the environment was still broken), the story used to
  exhaust its dev/review budget and plateau-defer — filing an unresolved blocker as deferred work and
  rolling back the implemented code. While `resolved_redrive` is latched, budget exhaustion now
  re-escalates (pauses for the human) instead of deferring, and the attempt's tree is preserved.
- **A resumed `--epic N` run stays scoped to its epic and no longer declares the epic "done" while
  stories remain.** `resume` rebuilt the engine without the run's `--epic`/`--story`/`--max-stories`,
  so a scoped run silently widened to every epic; with strict file-order story selection, deferring or
  finishing a story in an epic placed out of numeric order in the sprint board (e.g. one appended last)
  bounced selection to an earlier-in-file epic and fired a spurious "epic N complete" boundary,
  stranding the epic's remaining stories. The selector and cap are now persisted and restored on
  resume, and story selection exhausts the current epic before advancing — so an epic boundary fires
  only when that epic has no actionable stories left. Document-order epic execution is unchanged.

## [0.7.11] — 2026-06-30

### Fixed

- **A finalized story the review just won't stop recommending a follow-up for is now committed, not
  rolled back, when the review budget runs out.** Exhausting `limits.max_review_cycles` previously
  always deferred + reverted — discarding completed, review-passing work (frontmatter `status: done`,
  verify green) whose only "failure" was a never-clearing `followup_review_recommended`. The
  orchestrator now commits that work and re-files the lingering recommendation as a fresh open
  deferred-work entry; a story that itself came from such an entry is committed without re-filing, so
  a second non-convergence reaches a human instead of looping across sweeps. Worktree-isolation runs
  were unaffected — a deferred unit already keeps its worktree.

## [0.7.10] — 2026-06-29

### Fixed

- **Completed work left at the transient `in-review` frontmatter is no longer falsely deferred and
  rolled back.** A `bmad-dev-auto` session that dies in its step-04 Finalize tail can leave the spec
  frontmatter at the transient `in-review` marker while the `## Auto Run Result` prose already says
  `Status: done` — the same stale-frontmatter gate bug as 0.7.8 with a different value. The 0.7.8
  reconcile skipped `in-review` to protect the legacy `bmad-auto-dev` review-handoff, but that fork
  is retired and `in-review` is now only ever a transient marker, so it is reconciled to `done`
  before the gates run. Every deterministic gate still runs afterward, and a `followup_review_recommended: true`
  spec still triggers the follow-up review pass. Closes a re-sweep loop that re-ran and discarded the
  same completed bundles (~47M tokens/cycle).

## [0.7.9] — 2026-06-29

### Fixed

- **The multiplexer seam no longer leaks raw subprocess timeouts.** Every contract method now raises
  `MultiplexerError`/`TmuxError` or returns its documented sentinel instead of letting a 30 s tmux
  hang escape as a raw `subprocess.TimeoutExpired`.
- **A transient tmux hang no longer crashes a run or mis-reads a working session as dead.** The
  wait-loop tolerates an unknowable liveness probe — a persistent hang degrades to an honest
  `timeout`, never a false `crashed`.
- **An unexpected engine exception is now recorded instead of being lost to the parked control
  window.** The orchestrator writes a `run-crash` journal line + a `crash.txt` traceback, sets a
  `CRASHED` run status, and tears down the orphaned agent session — rather than dying with a
  traceback printed only to the pruned control pane.

## [0.7.8] — 2026-06-29

### Fixed

- **Completed `bmad-dev-auto` work is no longer falsely deferred when the skill leaves the spec
  frontmatter `status` stale.** The skill can finalize a run in its `## Auto Run Result` prose
  (`Status: done`) yet leave the YAML frontmatter at the template default `draft`; since every gate
  reads frontmatter, the sprint/ledger sync no-op'd and the story or sweep bundle deferred — losing
  tested work on rollback. The orchestrator now reconciles the frontmatter to the success status
  from the terminal prose before the gates run (journaled `spec-status-reconciled`). It reconciles
  only a `done` outcome from a non-terminal status, and every deterministic gate (worktree diff,
  dw-ids, verify commands, ledger) still runs — so the bookkeeping is repaired without trusting prose
  to pass a gate.

## [0.7.7] — 2026-06-28

### Fixed

- **Spec-status gates are now case- and whitespace-insensitive.** A hand-edited spec whose
  frontmatter carried a stray-cased `Done`/`In-Review` silently failed the dev/review gate and the
  story never advanced; every spec-frontmatter status read now normalizes through a single
  `verify.status_of` helper. The well-formed lowercase path is unchanged. Also fixes the
  manual-rollback notice, which rendered an invalid `git reset --hard the run's baseline commit`
  when no baseline was recorded — it now shows a `<baseline_commit>` placeholder.
- **Project-relative path guards reject `..` traversal and OS-foreign absolute paths.** A CLI
  profile or plugin manifest could declare a `config_path`/`skill_tree`/`seed_files`/module path
  that climbed out of the project with `../` — or, on Windows, a POSIX-absolute `/etc/...` that
  `Path.is_absolute()` failed to flag — and slip past the "must be project-relative" check. The
  guards now reject both, on every platform.
- **Persisted relative paths serialize with forward slashes.** A worktree run's `spec_file` and the
  resolve context's `resolution_path` were written with the host separator, so a `state.json` or
  context file produced on Windows read back with backslashes. Both now persist via `as_posix()` for
  a single cross-OS contract (a no-op on POSIX).
- **The TUI no longer shows a stale run after a same-size state rewrite.** The dashboard's
  stat-gated cache keyed on `(mtime_ns, size)`, so an atomic `state.json` rewrite of identical size
  within one coarse mtime tick (e.g. WSL2 drvfs) could be served stale. The engine rewrites
  atomically onto a fresh inode, so the cache signature now includes `st_ino`.
- **A dev session is no longer mis-stalled while it is actively working or legitimately waiting.**
  Building on `dev_stall_grace_s` (0.7.5), the idle-grace window now measures genuine _inactivity_
  rather than time-since-last-Stop: any growth of the session's pane log (a long productive turn, a
  streaming subagent) re-arms it, so a session that has finished implementation and is mid-review is
  no longer killed and rolled back. And because bmad-auto cannot re-invoke a turn that ended to await
  a background process, the grace window no longer dead-ends in a stall — on real silence the
  orchestrator wakes the session with up to `limits.dev_stall_nudges` (new, default 2) nudges before
  giving up; a genuine Stop restores the budget, so a slow-but-cooperative session waits up to
  `session_timeout_min` while a truly unresponsive one still stalls. `0` restores stall-on-grace-expiry.

## [0.7.6] — 2026-06-28

### Changed

- **The OS is now abstracted behind a registry of seams, so a non-tmux/native-Windows port is new
  files plus one registration line each — no core edits.** The terminal multiplexer is selected
  through a registry (`register_multiplexer`, by `sys.platform` with a `BMAD_AUTO_MUX_BACKEND`
  override) rather than hardcoded in `get_multiplexer()`, and the tmux backend split into a reusable
  `BaseTmuxBackend` extension point — every tmux invocation funnels through one overridable `_run()`
  primitive — with `TmuxMultiplexer` as a thin POSIX leaf, so a tmux-family backend (an eventual
  "psmux") overrides only the spawn primitive and the few divergent methods.
- **Process-lifecycle primitives moved behind a `ProcessHost` seam.** Politely-stop / force-kill /
  liveness / PID-reuse-identity now route through `get_process_host()` (registered like the
  multiplexer, with a `BMAD_AUTO_PROCESS_HOST` override); a `WindowsProcessHost` ships ready to
  register. Hook registration no longer hardcodes `python3` — it takes the interpreter prefix from
  `ProcessHost.hook_interpreter()` (POSIX `python3`; Windows `uv run --no-project python`), and
  `bmad-auto validate` runs a platform preflight that reports the selected backend's readiness and
  names the process host. Behavior on Linux/macOS/WSL is unchanged.
- **The bundled Unity plugin's teardown delegates pid lifecycle to `ProcessHost` and its helper
  scripts run under the orchestrator's own interpreter.** Plugin helper scripts are spawned via
  `sys.executable` (not a PATH-resolved `python3`), so a bundled script may import `automator` seams;
  `unity_teardown.py` now reaps leaked Editor/MCP processes through `get_process_host()` instead of
  re-implementing kill/liveness, gaining Windows behavior for free.

### Added

- **A consolidated [porting guide](docs/porting-to-a-new-os.md)** maps the four OS seams (terminal
  multiplexer, process lifecycle, hook interpreter, validate preflight), their registries and
  test-override env vars, and exactly what a native-Windows port costs end to end. The
  adapter-/plugin-authoring guides, ROADMAP, README, and FEATURES are updated to the post-registry
  world.

## [0.7.5] — 2026-06-28

### Added

- **Select and copy text from the TUI Log and Attention panes.** Click-drag highlights and `ctrl+c`
  copies (those panes are now selectable `RichLog`s with a working `get_selection`); `y` copies the
  whole active pane in one keystroke. The other panes are interactive widgets — hold your terminal's
  bypass modifier (Shift on most Linux terminals, Option on iTerm) to use its native selection. Copy
  rides OSC 52, so under tmux it needs `set -g set-clipboard on` to reach the system clipboard.
- **`bmad-auto diagnose` emits a sanitized diagnostic dump of a run/sweep** so a user can hand
  maintainers what's needed to debug a run without shipping any code, spec/story content, prompts,
  transcripts, file paths, or PII. It derives the diagnostic _shape_ — phase/token/session
  histograms, escalation counts, adapter/model, env, run-dir file sizes — and routes every
  content-bearing value through the audited `sanitize` chokepoint: identifiers (story keys,
  branches, SHAs) are pseudonymized to stable per-dump aliases so events still correlate, free text
  collapses to presence booleans, and the rendered output is re-scanned by a fail-closed leak
  self-check before writing. Defaults to the latest run; `--all`, `--out`, `--json`, and a
  local-only `--legend` are supported.

### Changed

- **The `sanitize` chokepoint now redacts credential-shaped strings.** Identifier-shaped secrets
  (`ghp_`/`sk-`/`AKIA`/`xoxb-`/JWTs and long high-entropy blobs) previously passed the slug gate
  verbatim; they are now `<redacted:secret>`, closing the same hole for `probe-adapter`.

### Fixed

- **A dev session that ends its turn to await a long-running background process is no longer
  mis-stalled.** A `bmad-dev-auto` session that yields to wait on a slow job (a Unity PlayMode run, a
  long test) and expects to be re-invoked on completion fired a result-less Stop — and since the
  generic dev adapter runs zero nudges, that was ruled stalled after only the 15s result grace,
  driving a retry that (with `scm.rollback_on_failure` off) paused the whole sweep for a manual
  reset. A new `limits.dev_stall_grace_s` (default 600s) opens an idle-grace window on a result-less
  dev Stop and re-arms it on each re-invocation, so only a genuinely idle gap with no terminal spec —
  or the session timeout — counts as a stall. Non-dev adapters keep zero grace and are unchanged.

## [0.7.4] — 2026-06-26

### Fixed

- **Deferred-work sweep no longer defers every bundle it just finished.** After the migration to
  the generic upstream `bmad-dev-auto` primitive, bundle dev sessions completed the work but were
  rejected by `verify_dev_bundle` with `result.json dw_ids [] do not match the bundle's […]`,
  retried to budget, deferred, and rolled the work back — so a sweep could never close a bundled
  entry. The retired dev fork used to echo the dw ids; the generic skill doesn't. The orchestrator
  already owns the bundle→dw-id binding, so the cross-check now passes when the session claims no
  ids, and the run exports `BMAD_AUTO_DW_IDS` so the synthesized result still carries them and the
  check stays live.

## [0.7.3] — 2026-06-26

### Fixed

- **The Log tab no longer shows only a single page for Claude runs.** Claude Code's new
  fullscreen TUI (an opt-in research preview) draws on the terminal's alternate screen and repaints
  in place, so the pane capture the Log tab emulates collapsed to the final frame — while
  line-oriented CLIs like codex still showed in full. The `claude` profile now forces the classic
  inline/scrollback renderer (`CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1`), which overrides any `tui`
  setting and keeps output in native scrollback so the whole session is reconstructable. As a
  safety net, the log view also detects an alternate-screen switch and flags such a capture as
  showing only the final frame, pointing at the agent's full JSONL transcript.

## [0.7.2] — 2026-06-26

### Fixed

- **Worktree isolation no longer false-stalls a story that actually finished.** Under
  `scm.isolation = worktree` the `bmad-dev-auto` session runs with its cwd set to the worktree and
  leaves its terminal spec in the worktree's `_bmad-output/implementation-artifacts`, but the dev
  adapter searched the main checkout's dir (resolved once at startup). The completed `status: done`
  spec was never found, so the orchestrator misread the session as stalled, rolled the unit branch
  back to baseline, and re-ran the same story. The adapter now resolves the spec directory from the
  live session cwd; in-place runs and artifact dirs configured outside the project tree are
  unaffected.

- **An uncommitted `policy.toml` edit no longer vanishes on rollback.** `policy.toml` is tracked but
  lives inside the kept `.automator` dir, so a rollback's `git reset --hard` to baseline silently
  reverted operator edits — a freshly enabled `scm.rollback_on_failure` could disappear before it ever
  took effect — and a lone policy edit could register as attempt dirtiness, trapping the
  manual-recovery loop. Rollback now restores `policy.toml` from its on-disk content unconditionally —
  so a config change committed after the baseline on an otherwise-clean tree survives too, not only
  one that rode a non-empty `git stash` snapshot — and the dirty check always excludes it, regardless
  of the preserve set.

- **Fixed a decision-toast notification race in the TUI test suite on Python 3.14.** Test-only; no
  runtime change.

## [0.7.1] — 2026-06-25

### Fixed

- **The Log tab no longer renders whole CLI sessions underlined.** Modern CLIs emit an XTMODKEYS
  sequence (`CSI > 4 ; 2 m`, "modifyOtherKeys") at startup that the pane emulator (pyte) misread as
  SGR 4 / underline-on — with no matching off present in a live capture — so every line came out
  underlined and hard to read. The log view now strips private-marker CSI sequences before emulation;
  genuine color, bold, and properly-closed underline styling is preserved.

- **Resolving a CRITICAL escalation no longer loops on a manual-rollback prompt when the resolve
  edited the spec.** 0.7.0 fixed the loop only for an already-clean tree, but the resolve workflow's
  whole job is to correct the frozen spec under the BMAD artifact folder (`_bmad-output/...`, which is
  tracked). So on resume the orchestrator saw a dirty tree and — with the default
  `scm.rollback_on_failure = false` — paused for a manual reset; because the dirty check diffs against
  the frozen `baseline_commit`, even committing the spec re-paused on the next resume, an endless loop.
  A resolved re-drive is human-initiated, so it now always auto-recovers regardless of the flag: the
  BMAD artifact folders are treated as orchestrator-owned — excluded from the dirty check and preserved
  through every reset of the re-drive (not just the resume-time cleanup) — so the spec correction
  survives while the failed attempt's source changes revert to baseline. This closes a latent sibling
  bug: with `rollback_on_failure = true` a _later_ mid-re-drive retry/defer reset previously ran with no
  preserve set and reverted the just-corrected spec silently, looping the re-drive.
  `scm.rollback_on_failure` still defaults OFF and now governs only unattended/stopped attempts; the
  manual-recovery notice (reached by stopped attempts only now) drops its resolved-cause wording.

- **A failed artifact restore during rollback now surfaces instead of silently dropping the
  correction.** When `safe_rollback` restores the preserved BMAD folders from its pre-reset snapshot, a
  genuine `git checkout` failure (corrupt snapshot, lock, IO) was swallowed alongside the benign
  empty-dir "pathspec did not match" case — so a corrected spec could vanish with no error and loop the
  re-drive. Real failures now raise; the empty-dir case stays tolerated.

## [0.7.0] — 2026-06-24

### Changed

- **Retired the `bmad-auto-dev` fork; the orchestrator now drives the upstream `bmad-dev-auto`
  skill unmodified** (bmad-code-org/BMAD-METHOD#2500, merged upstream) as its sole dev primitive.
  The skill is the inner autonomous coding session; everything automator-specific — escalation,
  sprint/ledger bookkeeping, repair-resume — stays in the orchestrator, which synthesizes
  `result.json` from the spec the skill leaves on disk. There is no fork to keep in sync with upstream.

- **Review is now a re-invocation of `bmad-dev-auto` on the done spec, not a separate skill.**
  `bmad-dev-auto` routes a `status: done` spec to a fresh step-04 review pass (BMAD-METHOD#2508), so
  the orchestrator's follow-up review just re-runs `/bmad-dev-auto <done spec>` in a fresh context.
  `review.enabled` still gates whether that follow-up pass runs at all; the new `review.trigger` knob
  (see Added) decides when it fires. The loop converges when a pass finishes `done` without the skill
  setting `followup_review_recommended`, still bounded by `limits.max_review_cycles` (default 3).

- **The skill commits each iteration; the orchestrator squashes to one commit per story.**
  `bmad-dev-auto` now commits its own work at the end of a successful run (BMAD-METHOD#2506). At
  finalize the orchestrator collapses that chain plus its own sprint/ledger writes back onto the
  pre-dev baseline into a single commit carrying the configured message — `pre_commit`/`post_commit`
  hooks and `scm.commit_message_template` stay authoritative.

### Added

- **Skill-recommended review (`review.trigger`).** `bmad-dev-auto` self-reviews inline and sets
  `followup_review_recommended` on a `done` spec when its changes warrant an independent pass
  (BMAD-METHOD#2505). The orchestrator consumes it: `review.trigger = "recommended"` (new default)
  runs the follow-up `bmad-dev-auto` review pass only when flagged; `"always"` keeps the old
  run-every-story behavior. Adjustable in the TUI and `policy.toml`. The follow-up loop stays bounded
  by `limits.max_review_cycles` (default 3) — the oscillation guard — so a skill-recommended review
  can never loop indefinitely.

- **Non-bundled-skill preflight.** `bmad-auto validate` and run/sweep/resume start verify that
  `bmad-dev-auto` and the two adversarial review hunters (`bmad-review-adversarial-general`,
  `bmad-review-edge-case-hunter`) — which `bmad-dev-auto`'s step-04 invokes inline on every run — are
  installed in each active CLI skill tree, failing loudly with remediation instead of stalling mid-run
  on an `Unknown command`. Worktree provisioning copies these upstream skills from the main repo,
  since they are not bundled in the wheel.

- **`result.json` `workflow` is now an enforced contract on the dev path.** `verify_dev` /
  `verify_dev_bundle` reject a mismatch against `verify.DEV_WORKFLOW` (`"auto-dev"`); the synthesized
  result carries `"auto-dev"`. Review re-runs the same skill, so it carries the same tag, and
  `verify_review` stays purely disk-derived — it is never handed the result.json.

- **Pluggable terminal-multiplexer seam (groundwork for native Windows).** All tmux usage now goes
  through a `TerminalMultiplexer` ABC (`get_multiplexer()`); `TmuxMultiplexer` is the only code that
  shells out to `tmux` and the only place the POSIX `sh -c` parked-window trailer lives. The generic
  adapter (renamed `generic_tmux.py` → `generic.py`), `runs.py`, `tui/launch.py`, `probe.py`, and
  `tui/data.py` all route through it, so a future non-tmux backend slots in with no engine changes.
  Behavior on Linux/macOS/WSL is byte-identical; **no native-Windows backend ships yet** (see [ROADMAP](docs/ROADMAP.md)).

- **POSIX portability hardening + CI guard.** Scattered POSIX-only primitives are guarded behind a
  platform seam — `SIGKILL` fallback, detach kwargs, `terminate_pid`, `os.devnull` — and the Unity
  plugin degrades off Linux (`/proc` → `psutil` via a new optional `windows` extra, `/tmp`, `cp -a`
  CoW, symlinks, `start_new_session`), keeping every Linux fast path unchanged. A new
  `tests/test_portability_guard.py` AST/byte scan blocks new POSIX-only patterns from creeping back,
  with sanctioned exceptions carrying `# portability:` acks.

- **Adapter & profile authoring guide.** `docs/adapter-authoring-guide.md` now carries the complete
  `CLIProfile` / `HookSpec` field reference (the single canonical schema home) and a "writing a new
  adapter class" section for non-tmux transports — linked from the README documentation index.

### Removed

- **Retired the bundled `bmad-auto-dev` and `bmad-auto-review` skills.** `bmad-auto init` now installs
  three bundled skills — `bmad-auto-resolve`, `bmad-auto-sweep`, `bmad-auto-setup` — and the upstream
  `bmad-dev-auto` skill (from a recent bmm module) is a hard prerequisite. `bmad-auto-review`'s
  adversarial review is fully covered by `bmad-dev-auto`'s inline step-04 (Blind + Edge-Case hunters);
  the independent Acceptance Auditor layer is dropped, and the two hunters are now always-required base
  skills rather than gated on `review.enabled`. The canonical `deferred-work-format.md` moved into
  `bmad-auto-sweep`, its remaining owner.

### Fixed

- **Resolving a CRITICAL escalation no longer loops on a manual-rollback prompt.** Re-arming an
  escalation requests a clean rebuild, which in non-worktree (in-place) runs means resetting to the
  story baseline. With the default `scm.rollback_on_failure = false` the orchestrator paused for a
  manual reset — but never cleared `baseline_commit`, so following the instructions (`git reset --hard`,
  then `resume`) re-paused on the next resume, an endless loop. `_rollback_or_pause` now no-ops when the
  tree is already at baseline (nothing this attempt touched), so a clean tree — including one the
  operator just reset — proceeds straight to the re-drive. The same guard suppresses the spurious prompt
  when an escalation left no changes at all.
- **Manual-recovery notice wording.** The prompt no longer claims the story "failed" — it now reflects
  the real cause ("escalation was resolved; re-driving needs a clean baseline" vs. "attempt was stopped").
- **Resolved escalations now actually re-drive instead of HALTing on a stale `blocked` spec.** `verify_dev`
  only recorded `task.spec_file` on a fully successful session, so a dev session that escalated with a
  `blocked` spec (the common escalation case) left it unset. `rearm_escalation` then had no spec path to
  flip to `ready-for-dev`, so on resume `bmad-dev-auto`'s step-01 routing re-HALTed on the still-`blocked`
  frontmatter — a second loop. The orchestrator now captures the spec the session produced when it
  escalates or defers (the synthesized result names it even on a HALT), so re-arm flips the status and
  the re-drive proceeds, and a deferred story's spec is stashed as intended.
- **Copilot dev stage no longer stalls on a subagent `agentStop`.** Copilot fires `agentStop` for
  every subagent turn too — with an empty `transcriptPath` and a tool-use session id, not the main
  session's turn-end. With dev decoupled to `bmad-dev-auto` (which implements via subagents), that
  premature Stop reached the dev stage, where 0 nudges made the orchestrator declare an outright stall
  before the skill wrote its terminal spec (same root cause as the 0.6.4 review stall). A new
  per-profile `subagent_stop_without_transcript` (true for `copilot`) ignores a `Stop` carrying no
  transcript, so the main session's real turn-end drives completion — and restores usage tallying,
  since that Stop carries the transcript.
- **Process liveness/termination no longer risks signaling the wrong process.** A corrupt
  `engine.pid` read as `0` or negative would make `os.kill` target a process group — for `0`, the
  orchestrator's own — so `pid_alive`/`terminate_pid` now reject non-positive PIDs before signaling.
  The remaining liveness checks (`runs.py`, `tui/data.py`) that called `os.kill(pid, 0)` directly now
  route through `pid_alive`, since on Windows `os.kill(pid, 0)` maps to `TerminateProcess` and is
  destructive; a CI guard blocks bare `os.kill(_, 0)` from regressing.

## [0.6.4] — 2026-06-21

### Fixed

- **Copilot token usage now records (was always 0).** Copilot writes its token totals only in
  the trailing `session.shutdown` events line, ~1s after `agentStop` — usage was sampled before
  it landed. `read_usage` now polls the transcript for a short grace, driven by a new per-profile
  `usage_grace_s` (8s for `copilot`, 0 elsewhere = read once).
- **Copilot multi-turn reviews no longer stall.** `agentStop` fires per response turn, so a
  parallel-subagent review ends several turns and tripped the global `stop_without_result_nudges`
  default of 1. New per-adapter floor (5 for `copilot`), overridable per stage via `[adapter.review]`.

### Added

- **`[adapter] usage_grace_s` / `stop_without_result_nudges`** (base + per-stage
  `[adapter.dev|review|triage]`), editable in the settings TUI. Unset = inherit the CLI profile's
  shipped default.

### Changed

- **Copilot docs.** Pin a capable model — the free GPT-5 mini default silently skips steps in
  multi-step dev/review — and it's the Copilot **CLI** binary that's supported, not the VS Code
  extension.

## [0.6.3] — 2026-06-21

### Fixed

- **GitHub Copilot adapter (CLI 1.0.63).** Turn-end is `agentStop`, not PascalCase `Stop`
  (which never fires) — every session previously read as a timeout. Remapped events, dropped
  the non-existent `PreCompact`, and the shared hook relay now reads camelCase payload keys
  (`sessionId`/`transcriptPath`). Probe mode sends its prompt verbatim so a skill-templating
  `prompt_template` no longer renders a missing-skill path that stalls the turn.

### Added

- **Copilot token accounting.** New `copilot-events` `usage_parser` reads
  `~/.copilot/session-state/*/events.jsonl` (`data.modelMetrics.<model>.usage.*`); the `copilot`
  profile is wired to it (was `usage_parser = "none"`).

## [0.6.2] — 2026-06-21

### Added

- **`bmad-auto probe-adapter` (alias `collect-adapter-data`).** A self-service command that
  collects and sanitizes everything needed to finalize a CLI adapter profile — the hook payload
  shape, transcript location/format, and token-usage schema for a `usage_parser` — so a user of
  any coding CLI can paste back a clean, content-free report. A default zero-launch **scan** reads
  on-disk conventions; opt-in `--probe` does a live capture in an ephemeral workspace. All output
  passes through one audited PII sanitizer (token counts and field names survive; paths, prose, and
  emails are redacted).
- **GitHub Copilot CLI profile.** Bundled `copilot` profile (Copilot CLI ≥ 2026-02): `-i`
  interactive launch, VS Code-compatible `Stop` hook, `--allow-all-tools` for unattended runs.
  Still pending live E2E and a `usage_parser` — `probe-adapter` captures the token schema to write
  one.

- **Adapter authoring guide.** New [adapter authoring guide](docs/adapter-authoring-guide.md)
  walks through finalizing a CLI profile with `probe-adapter` (scan vs probe, the PII model, and
  the parser-writing loop); `probe-adapter` is added to both command references.

## [0.6.1] — 2026-06-20

### Added

- **Short run refs (Docker-style).** Every command that takes a run id (`status`, `attach`,
  `resume`, `resolve`, `stop`, `delete`, `archive`) now accepts a partial — the tail after the
  last `-` (e.g. `a1b2`, or as few chars as stay unique). Full ids still work; an ambiguous ref
  fails listing the candidates. New `bmad-auto list` (alias `ls`) prints each run/sweep with its
  short ref, type, and status.
- **Flexible `--story` selection.** `bmad-auto run --story` now takes more than the exact full
  key: an epic+number (`--epic 3 --story 1`, `--story 3-1`, or `--story 3.1`) or a slug fragment
  (`--story user-auth`). Full keys still work. Mismatches are caught before the run launches with a
  targeted error — no match, ambiguous slug, or matched-but-not-actionable.

## [0.6.0] — 2026-06-20

### Fixed

- **Rollback no longer wipes non-automator files.** A failed in-place attempt previously ran
  `git reset --hard` + a blanket `git clean -fd` over the whole checkout, which could delete a
  project's `_bmad-output/` and any other untracked files (only `.automator/` and two artifact
  subdirs were spared). The orchestrator now never runs a blanket `git clean`: it reverts the
  attempt's tracked changes and removes only the untracked files **that run created**, preserving
  pre-existing untracked files and the entire `_bmad-output/` tree.

### Changed

- **Auto-rollback is now opt-in (`[scm] rollback_on_failure`, default off).** With it off the
  orchestrator never touches your working tree on a failed attempt — it pauses the run with bold
  manual-recovery instructions (back up untracked files → `git reset --hard <baseline>` → restore).
  Turn it on for the safe automatic rollback above (it discards the attempt's uncommitted work, so
  it warns when it fires). Worktree isolation (`scm.isolation = "worktree"`) sidesteps this entirely.

## [0.5.1] — 2026-06-20

### Added

- **`bmad-auto clean` + `[cleanup]` retention.** Reclaims disk from concluded runs: tears down
  git worktrees a mid-flight stop orphaned (freeing each worktree's Unity `Library/` + MCP-server
  build — the main accumulation source), trims the heavy `worktrees/` tree from runs kept for
  history (they still list in the TUI), and archives/deletes runs past `[cleanup] run_retention`
  (default 10). Only finished/stopped runs are touched; `--keep`/`--dry-run`/`--retain`/`--hard`.
  Every `run`/`sweep` start auto-reconciles worktrees a prior **finished** run leaked
  (`auto_clean_on_finish`); the Unity plugin's new `post_run` hook clears the IvanMurzak MCP
  server's `/tmp/<company>/<product>/*.zip` downloads + truncates its editor log (`clean_tmp`).
- **Test Architect (TEA) plugin.** New bundled, opt-in `tea` plugin that wires the BMAD
  Test Architect Enterprise module into every run and sweep as advisory-by-default quality steps.
  Enable with `[plugins] enabled = ["tea"]`; it injects six TEA workflows — test-design, ATDD,
  automate (after dev) and trace, NFR, test-review (after review) — and fails fast at startup if
  TEA isn't installed (`npx bmad-method install` → Test Architect). Each step is individually
  toggleable; the three gate steps (`trace`/`nfr`/`review`) can be flipped to **blocking**, so a
  failing FAIL/CONCERNS gate escalates the unit for human review at commit instead of landing
  (fail-open: a missing or unparseable artifact never blocks). See the
  [TEA plugin guide](docs/tea-plugin-guide.md).
- **Settings-driven workflow `enabled` / `blocking`.** A plugin can let an operator disable a
  `[workflows.<name>]` step or flip its gate from policy via the `<name>_enabled` / `<name>_blocking`
  setting convention — no code, and byte-identical for plugins that don't declare them. Documented
  in the [plugin authoring guide](docs/plugin-authoring-guide.md#making-a-workflow-configurable).
- **Manage plugins from the TUI.** The settings screen (`g`) gains a **Plugins** section: a roster
  of every discovered plugin with an enable toggle (writing `[plugins] enabled`). A plugin's
  settings appear only once it is enabled — revealed live, hidden otherwise — so the form stays
  scannable; data-only plugins are always on. Saving now also runs each enabled plugin's coupling
  check (e.g. unity `editor_mode` ↔ `scm.isolation`), blocking an invalid combo at save time
  instead of mid-run.

- **MIT license + open-source community files.** The project is now MIT-licensed (© BMad Code, LLC)
  with a trademark notice, and ships `CONTRIBUTING`, `SECURITY`, `CODE_OF_CONDUCT`, and GitHub
  issue/PR templates as it becomes a first-class citizen in the BMAD org.
- **Uninstall procedure.** The [setup guide](docs/setup-guide.md#uninstalling) now documents a
  full teardown — reclaim disk, remove `.automator/`, skills, hooks, and gitignore lines, then
  `uv tool uninstall`.

### Changed

- **Renamed the project and package to `bmad-auto`.** The distributable is now `bmad-auto`
  (install with `uv tool install 'bmad-auto[tui]'`) and the repo has moved to the BMAD org at
  [bmad-code-org/bmad-auto](https://github.com/bmad-code-org/bmad-auto). The CLI command, skills
  (`bmad-auto-*`), tmux sessions, and `BMAD_AUTO_*` env vars are unchanged. The separate legacy
  [bmad-automator](https://github.com/bmad-code-org/bmad-automator) project is unrelated and stays
  as-is. Re-run `uv tool upgrade bmad-auto --reinstall` to move an existing install onto the new name.

## [0.5.0] — 2026-06-20

### Added

- **Plugin system.** New `automator.plugins` package — a general extension layer: a `plugin.toml`
  manifest (metadata, declarative `[hooks.<stage>]`, a `[[settings]]` schema, optional in-process
  `[python]`), a folder-drop loader with builtin/project overlay (and a locked seam for
  entry-point packaging later), a trust allowlist (`[plugins] enabled` in `policy.toml`), and a
  registry that isolates plugin failures. A dropped `[python]` plugin is never imported unless
  explicitly enabled. Plugins can **observe, veto (defer/pause/skip), and mutate** a shared
  context at every run/sweep lifecycle stage via the hook bus, with an O(1) no-op fast path so
  zero-plugin runs stay byte-identical.
- **Dynamic, TOML-driven settings.** The settings schema moves to `data/settings/core.toml`
  (presentation only; defaults/options referenced from the `policy.py` dataclasses, never
  duplicated), the TUI settings screen renders from a registry, and an enabled plugin's
  `[[settings]]` appear under `[plugins.<name>]`.
- **Workflow plugins.** A plugin can declare a `[workflows.<name>]` table that injects an extra
  agent session at a lifecycle stage (`post_dev_phase` / `post_review_result`, run by the `dev` or
  `review` adapter); the prompt substitutes `{story_key}`/`{run_id}`/`{scripts}`. Non-blocking by
  default (advisory); a blocking workflow that fails routes through the normal defer path. Ships
  with a worked-example plugin (`examples/plugins/guardrails/`) exercising every extension point and
  a full [plugin-authoring guide](docs/plugin-authoring-guide.md).

### Changed

- **The game-engine layer is now a plugin.** Unity runs entirely through the plugin system, with
  no engine-specific code in the core loop. Enable it with `[plugins] enabled = ["unity"]` and
  configure it under `[plugins.unity]` (`editor_mode`, `mcp`, `unity_path`, `ready_timeout_sec`,
  `ready_grace_sec`). Behavior — the readiness gate, `per_worktree` Editor setup/teardown, MCP
  agent routing, and Library priming — is unchanged.

### Deprecated

- The `[engine]` policy block is deprecated in favor of `[plugins] enabled = ["unity"]` +
  `[plugins.unity]`. Existing `[engine]` configs still load but emit a deprecation warning and are
  folded onto the `unity` plugin; explicit `[plugins.unity]` values win. `[engine]` will be
  removed in a future release.

## [0.4.4] — 2026-06-19

### Fixed

- Unity `per_worktree`: auto-recover merge-back when a competing Editor leaks asset writes
  (`.cs.meta` GUIDs, asmdef edits) into the **main** checkout. Previously git refused the merge
  pre-flight because the target already held the unit's incoming files as dirt, escalating the unit
  spuriously. Merge-back now cleans only the leaked copies of this branch's incoming files (journaled
  as `merge-target-cleaned`); dirt outside the branch's path set still escalates as possible operator
  work, with a distinct message.
- Unity `per_worktree`: route **every** worktree CLI's MCP config at the worktree's Editor, not
  just the dev agent. When dev and review use different CLIs (e.g. `dev=claude`, `review=codex`),
  the review agent could read a main-repo-seeded config and route its asset writes into the main
  checkout. Each agent's config is now written to the deterministic per-path port and verified; a
  mismatch fails the setup hook (the unit defers) instead of leaking writes.

### Changed

- Unity engine plugin: pin the `unity-mcp-cli` verification stamp to **v0.81.1** (subcommand
  signatures re-checked; no call-site changes). Documents the new upstream **dev-control HTTP
  bridge** (dev-only, off by default, not wired) in the [Game Engine MCP guide](docs/game-engine-mcp-guide.md).

## [0.4.3] — 2026-06-18

### Added

- **Game-engine plugin layer (opt-in; Unity).** New `[engine]` policy section adapts the
  dev/sweep cycle to projects that drive a live engine Editor through an MCP (Unity via
  [IvanMurzak/Unity-MCP](https://github.com/IvanMurzak/Unity-MCP) or
  [CoplayDev/unity-mcp](https://github.com/CoplayDev/unity-mcp)); off by default. Plugins ship
  like CLI profiles — bundled under `automator/data/engines/<name>/`, overridable in
  `.automator/engines/<name>/`. `editor_mode` couples to `[scm] isolation`: `shared` runs the
  agent in place on the operator's open Editor; `per_worktree` gives each unit its own managed
  Editor. A readiness gate blocks until the Editor + MCP report ready before each unit, deferring
  on timeout instead of starting against a half-open Editor.
- **Unity `per_worktree` mode.** Each unit runs in its own git worktree with a dedicated Editor:
  - Launches in local (Custom) mode — `bootstrap-local` plus `open --start-server true` so the
    Editor hosts its own per-path MCP server; this makes `wait-for-ready` a real readiness signal
    before any client connects. Connection knobs overridable via `BMAD_AUTO_UNITY_MCP_*`
    (`…_LOCAL=0` keeps the prior cloud launch).
  - Primes the worktree `Library` with a reflink/CoW copy of the warm main `Library`, so Unity
    reimports incrementally rather than cold — a cold import on a large project crashes the import
    workers (Burst `SIGFPE` writing `VirtualArtifacts`). Tunable via `BMAD_AUTO_UNITY_LIBRARY_SEED`
    and `…_SEED_MODE` (`reflink`|`copy`|`symlink`|`off`).
  - Teardown quits the Editor and reaps its child `gamedev-mcp-server` on completion or pause, so
    neither leaks across runs (a leaked server holds its port and breaks the next run).
  - Cold-launch grace via `[engine] ready_grace_sec`; MCP skill tree seeded into each worktree via
    `seed_globs`; `init` now gitignores `.automator/cache/`.
- **Worktree config seeding.** A fresh worktree checks out tracked files only, so a project's
  gitignored MCP/CLI configs (`.mcp.json`, `.claude/settings.json`, …) were missing — isolated
  sessions then timed out reaching their MCP and escalated as spurious spec errors. Each loaded
  adapter's configs are now copied in before launch, via new `[scm]` knobs `seed_adapter_defaults`
  (default on) and `worktree_seed` (extra paths). Both are in the TUI settings editor.
- **Game Engine settings in the TUI.** All six `[engine]` keys (`name`, `editor_mode`, `mcp`,
  `unity_path`, `ready_timeout_sec`, `ready_grace_sec`) are now editable in the settings editor
  (`g`) under a collapsible titled **Game Engine**; the `editor_mode` ↔ `[scm] isolation` coupling
  is validated on save. New authoring docs: [Writing a Game Engine plugin](docs/game-engine-plugin-guide.md)
  and [Writing a plugin for a specific Editor MCP](docs/game-engine-mcp-guide.md) (full
  `BMAD_AUTO_UNITY_*` env-var reference).

### Changed

- Default `limits.session_timeout_min` raised from 45 to 90 minutes — the old default cut off
  substantial units, especially MCP-driven Unity sessions where each Editor step is a slow
  round-trip. Override per project under `[limits]`.

### Fixed

- `bmad-auto cleanup` (and the TUI `c` action) no longer stops other projects' live runs. tmux
  sessions are global but were named only `bmad-auto-<run_id>`, so a run id absent from the current
  project looked like a prunable orphan and matched another project's active run. Sessions and
  windows are now stamped with their project (`@bmad_project`); cleanup prunes only the current
  project's, while still clearing true same-project orphans. Pre-existing untagged sessions are
  left untouched.

## [0.4.2] — 2026-06-17

### Fixed

- Answering sweep decisions over an attach now returns you to your terminal. After the
  last decision in a cycle was answered, the session previously stayed in the orchestrator
  window instead of handing control back. The sweep now returns the terminal as soon as the
  current cycle's decisions are answered and continues running bundles in the background.
  `bmad-auto attach` lands on the orchestrator window when a decision is pending and restores
  your previous session on exit.

## [0.4.1] — 2026-06-16

### Fixed

- Worktree isolation (`[scm] isolation = "worktree"`) now works. Isolated runs previously
  failed on the first session with `Unknown command: /bmad-auto-dev`. Worktrees are now
  created under the run directory (`.automator/runs/<run_id>/worktrees/<unit>`) instead of
  inside `.git/`, and each worktree is provisioned with the bundled skills and signal hook so
  project commands resolve correctly.

## [0.4.0] — 2026-06-16

First release with **opt-in git-worktree isolation** for runs and sweeps. The default is
unchanged: with no `[scm]` configuration, work happens in place on the checked-out branch
exactly as before (`isolation = "none"` is byte-for-byte identical to prior behavior).

### Added

- **Configurable `repo_root` + Workspace seam.** `_bmad/bmm/config.yaml` gains an optional
  `repo_root` key (defaults to the project dir) that decouples "where git work + code sessions
  happen" from "where run state lives." All code/git/artifact access now routes through a single
  `Workspace` indirection, so redirecting work into a worktree is a localized change rather than a
  sweep across the engine.
- **Worktree isolation** — `[scm] isolation = "worktree"` runs each story (and each sweep bundle)
  in its own `git worktree` on a dedicated `automator/<run_id>[/<story>]` branch cut from the
  target branch, then merges it back into the target **locally** (merge strategy `ff`, `merge`, or
  `squash`). The main checkout stays free while a run is in flight, and run state stays in the main
  repo's `.automator/` — never inside a worktree. Knobs: `branch_per` (`story` | `run`; `run`
  shares one branch across the run and forces `delete_branch = false`), `target_branch` (default =
  the branch checked out at run start; a configured branch is created/checked out in the main repo
  and never inside a worktree), `delete_branch`, and `keep_failed`.
- **Failed-unit forensics.** A deferred/escalated unit's full diff (tracked + untracked) is
  preserved to `run_dir/failed/<unit>/changes.patch`; with `keep_failed` (default) its worktree +
  branch stay mounted for inspection. `failed_diff_max_mb` (default `5`) caps the per-file size of
  untracked files in that patch — oversized files are skipped with a labelled marker — and
  `failed_diff_unlimited` lifts the cap entirely (logs a warning when active).
- **`commit_message_template`** — optional `[scm]` template (`{story_key}` / `{run_id}`
  substituted) used for story and sweep-bundle commits when set.
- The full `[scm]` section (isolation, `branch_per`, `target_branch`, `merge_strategy`,
  `delete_branch`, `keep_failed`, the failed-diff caps, and the commit template) is editable from
  the TUI settings screen. (`max_parallel` is omitted while it stays inert.)
- **Low-frame-rate TUI mode.** `bmad-auto tui --low-frame-rate` (or `[tui] low_frame_rate = true`,
  editable from the settings screen) caps Textual to 15fps and disables animations by setting
  `TEXTUAL_FPS` / `TEXTUAL_ANIMATIONS` before the app starts. Fixes the repaint tearing/garbage
  seen when driving the dashboard over a slow or high-latency link (SSH, Tailscale), where a 60fps
  update stream can't drain in time and partial frames paint over old ones. The setting takes
  effect the next time the TUI launches; an explicit `TEXTUAL_FPS` in the environment still wins.
- **git worktree / branch / merge / diff primitives** in `verify.py` (worktree add/remove/list/
  prune, `create_branch`, `merge_branch`, `capture_diff`, …), unit-tested in isolation.

### Changed

- Worktree-mode integration is always **serialized** — unit branches merge into the target one at
  a time. `max_parallel` exists as a validated knob but is clamped to `1` (inert) until internal
  parallel fan-out is built.
- Story spec paths are persisted **relative to the worktree** in `state.json`, so a kept-failed
  run's state stays portable if the worktree is later moved.
- The run reclaims its worktree scaffolding on clean completion (deliberately-kept failed/escalated
  worktrees are left in place and journalled so they can be found).
- **TUI settings editor now collapses every section by default.** Each policy section
  (`gates`, `limits`, `scm`, …) starts collapsed with a one-line description in its header, so the
  grown-large form scans at a glance — expand only the section you want to edit. `ctrl+e` toggles
  all sections open/closed at once.

### Fixed

- A detached HEAD or unborn repo no longer lands worktree merges on an unreferenced commit — the
  run pauses with a clear reason instead. A merge conflict against the target keeps the unit branch
  for manual merge and escalates; `capture_diff` now raises on a genuine `git` error (rather than
  silently truncating the patch) and `merge_branch` reports a failed abort/reset.
- **Editing settings no longer dirties the worktree for validation.** `worktree_clean()` (the
  pre-flight gate for `run`/`sweep`/`validate`) now ignores `.automator/policy.toml`, so saving a
  change in the settings editor no longer forces a commit of the config before the next command.
  Only that one file is exempt — the deferred-work ledger under `.automator/` still commits as
  before.

## [0.3.2] — 2026-06-15

### Added

- **Arrow-key navigation and Enter-to-edit on the settings screen.** Up/Down now move focus
  between fields (additive — Tab/Shift+Tab still work), and Enter activates the focused field
  by type: it opens a dropdown (`Select`), toggles a switch, or enters cursor-edit mode on the
  multi-line box (`TextArea`), where the box's own Up/Down then move the cursor; Escape leaves
  edit mode without leaving the screen. Plain text/number inputs stay editable on focus, so
  Enter is a no-op there. Implemented with priority bindings gated by `check_action` so an open
  dropdown or an editing TextArea keeps Up/Down, and Escape still pops the screen in nav mode.

### Fixed

- **Attaching to answer a deferred-work decision now returns you where you came from.**
  When a prompting sweep blocks on a decision (or you open a resolve session), pressing
  `a`/`R` switches a tmux client into the orchestrator's control window so you can answer
  there — but on exit it left you stranded in the control session on the parked
  exit-status prompt instead of back at the TUI. The control window now records where the
  attach came from and, once you press enter, returns you: it switches the client back to
  the TUI's own pane when the TUI runs inside tmux (i.e. your original session), or
  detaches the throwaway attach client so the suspended TUI resumes when it runs outside
  tmux. Windows nobody attached to interactively still park unchanged.

- **Empty optional numeric fields no longer flash a red "invalid" outline.** The start-run
  and start-sweep modals draw their numeric inputs (`epic`, `max stories`, `max bundles`)
  with `type="integer"`, which under Textual validates on blur and — with the default
  `valid_empty=False` — treats an empty string as invalid. Tabbing past a blank field that
  is explicitly optional ("blank for all", "blank for no limit") therefore tripped the red
  `$error` border. The inputs now pass `valid_empty=True`, matching the settings screen, so
  leaving them blank is accepted silently while a typed integer still validates.

### Changed

- **Clearer review toggle on the settings screen.** The `[review]` switch showed only the
  raw key `enabled`, with no hint about what it controls. It is now relabelled "separate
  review session" and carries a muted caption spelling out both states (ON: triple review
  runs in a dedicated 2nd session · OFF: quick-dev runs its own tri-review inline). The
  change is display-only — the config key and save logic are unchanged.

- **`bmad-auto-setup` now upgrades, not just installs.** Re-running the skill (or invoking
  it with `upgrade`) on an already-installed project is detected as an upgrade — it runs
  `uv tool upgrade bmad-automator --reinstall` (the `--reinstall` is required for a git
  source) and re-lays the per-project skills with `bmad-auto init --force-skills`, then
  reports the before → after version. Previously a re-run was treated as a config-only
  update: it left `--force-skills` off, so `init` silently skipped every existing skill
  dir and the project kept stale skills against the upgraded tool. Upgrade is detected from
  an existing `bauto` config section and/or a uv-managed `bmad-automator`, and the tool
  follows `main` by default with an offer to pin a release tag. Docs (README "Upgrading",
  `docs/setup-guide.md`) now describe the skill-driven upgrade alongside the manual ritual,
  and the stale `uv tool upgrade bmad-automator` hint (missing `--reinstall`) is corrected.

## [0.3.1] — 2026-06-14

Maintenance release. Also backfills the previously-undocumented `[0.3.0]` notes below.

### Changed

- `scripts/sync_version.py` now runs `uv lock` as part of the version stamp, so a
  version bump regenerates the pinned lock in one command. CI runs `uv sync --locked`,
  which fails the install step on a stale lock (hit while cutting 0.3.0); folding the
  relock into the stamp keeps a bump a single command. Idempotent, with a loud non-zero
  exit if `uv` is missing or the lock fails.

## [0.3.0] — 2026-06-14

First release carrying the optional review toggle.

### Added

- **Optional review pass** — new policy `[review] enabled` toggle (default `true`). When
  disabled, a run skips the separate fresh-context `bmad-auto-review` session: the dev pass
  runs quick-dev's own internal triple-review unattended and finalizes the story straight to
  `done` — one session per story instead of two, with verify commands still gating the
  commit. The flag flows to the dev session via `BMAD_AUTO_SKIP_REVIEW=1`; the dev skill (not
  the engine) writes the `done` status, preserving the engine-never-writes-status invariant.
  Global scope: also governs deferred-work sweep bundles. Exposed as a switch in the TUI
  settings screen.

### Changed

- **Install / upgrade docs** — the README install block now offers main-tracking vs.
  pinned-tag installs, and a new "Upgrading" section documents the two-step ritual
  (`uv tool upgrade --reinstall` — required for a git source — then re-lay per-project skills
  with `init --force-skills`). The `bmad-auto-setup` skill is corrected to use `--reinstall`
  (plain `uv tool upgrade` reuses the cached git commit and won't pull new code) and notes the
  skill re-lay step plus tag pinning.
- Regenerated `uv.lock` for the 0.3.0 version pin.

## [0.2.0] — 2026-06-14

First versioned release since the initial `0.1.0`. Consolidates everything built since then and
realigns the version across the Python package and the BMAD-module metadata (which had drifted to a
placeholder `1.0.0`). All version-bearing fields are now kept in sync by `scripts/sync_version.py`,
enforced in CI.

### Added

- **TUI dashboard** (`bmad-auto tui`) — live, read-only view of runs, the sprint tree, the
  deferred-work ledger, a per-story phase/token table, and tailing of the journal / pane log /
  ATTENTION file, plus an integrated launcher for new runs and an in-app policy editor.
- **Deferred-work sweeps** — `bmad-auto sweep` triages the ledger against the real codebase and
  runs full dev → review → verify → commit on actionable bundles; `--repeat` re-triages each cycle;
  `bmad-auto decisions` surfaces and pre-answers human decisions earlier sweeps left open.
- **Interactive escalation resolution** — `bmad-auto resolve <run-id>` opens a resolve agent to
  disambiguate a frozen spec on a CRITICAL escalation, then re-arms the story and resumes.
- **Multi-CLI / multi-agent support** — a generic tmux adapter driven by declarative TOML profiles,
  with built-in `claude` (default), `codex`, and `gemini` profiles and per-stage overrides
  (`[adapter.dev|review|triage]`) for client/model/extra args.
- **Run operations** — `stop`, `delete`, `archive`, and `cleanup` for tmux artifacts of finished or
  stopped runs.
- **Cost-weighted token budgeting** — per-story `max_tokens_per_story` using cache-read weighting.
- **Bundled skill module** — the `bmad-auto-*` skills ship inside the wheel and are laid down by
  `bmad-auto init` into `.claude/skills/` and/or `.agents/skills/`.

### Changed

- **BREAKING:** policy `[adapter]` no longer accepts the flat `model_dev` / `model_review` keys; use
  the `[adapter.dev]` / `[adapter.review]` / `[adapter.triage]` sections instead (a clear error
  points at the replacement).
- **BREAKING:** build system migrated from setuptools + pip to **hatchling + uv**. Install with
  `uv tool install "bmad-automator[tui] @ git+…"`; develop with `uv sync --all-extras`. All docs,
  CLI hints, the `bmad-auto-setup` skill, and the eval-runner Dockerfile now use uv.
- **BREAKING:** module layout renamed `module/` → `skills/`; the canonical skills live under
  `src/automator/data/skills/`.

### Fixed

- BMAD-method installer could not locate `module.yaml` for the `bauto` module
  (`collectAgentsFromModuleYaml` / `writeCentralConfig` warnings): restored a repo-root
  `module.yaml` descriptor so the installer's shallow lookup resolves the module again.
- Replaced stale `pip install` instructions across docs, CLI hints, the setup skill, the
  eval-runner Dockerfile, and the module greeting with their uv equivalents.

## [0.1.0] — 2026-06-10

- Initial release: deterministic dev → review → verify → commit orchestrator for the BMAD
  implementation phase, driven by a Python control loop with hook-based session transport and
  resumable on-disk run state.

[Unreleased]: https://github.com/riaworks/waves/compare/v3.6.12.4...HEAD
[3.6.12.4]: https://github.com/riaworks/waves/releases/tag/v3.6.12.4
[3.1.0]: https://github.com/riaworks/waves/releases/tag/v3.1.0
[3.0.0]: https://github.com/riaworks/waves/releases/tag/v3.0.0
[2.0.0]: https://github.com/riaworks/waves/releases/tag/v2.0.0
[1.0.0]: https://github.com/riaworks/waves/releases/tag/v1.0.0
[0.13.1]: https://github.com/bmad-code-org/bmad-loop/releases/tag/v0.13.1
[0.13.0]: https://github.com/bmad-code-org/bmad-loop/releases/tag/v0.13.0
[0.12.0]: https://github.com/bmad-code-org/bmad-loop/releases/tag/v0.12.0
[0.11.1]: https://github.com/bmad-code-org/bmad-loop/releases/tag/v0.11.1
[0.11.0]: https://github.com/bmad-code-org/bmad-loop/releases/tag/v0.11.0
[0.10.0]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.10.0
[0.9.1]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.9.1
[0.9.0]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.9.0
[0.8.1]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.8.1
[0.8.0]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.8.0
[0.7.12]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.7.12
[0.7.11]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.7.11
[0.7.10]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.7.10
[0.7.9]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.7.9
[0.7.8]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.7.8
[0.7.7]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.7.7
[0.7.6]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.7.6
[0.7.5]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.7.5
[0.7.4]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.7.4
[0.7.3]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.7.3
[0.7.2]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.7.2
[0.7.1]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.7.1
[0.7.0]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.7.0
[0.6.4]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.6.4
[0.6.3]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.6.3
[0.6.2]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.6.2
[0.6.1]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.6.1
[0.6.0]: https://github.com/riaworks/riaworks-loop-llm/releases/tag/v0.6.0
[0.5.1]: https://github.com/bmad-code-org/bmad-loop/commit/06d089d734c6
[0.5.0]: https://github.com/bmad-code-org/bmad-loop/commit/c6a4e4f09e7c
[0.4.4]: https://github.com/bmad-code-org/bmad-loop/commit/37a2886eee7c
[0.4.3]: https://github.com/bmad-code-org/bmad-loop/commit/e1c3f17e989a
[0.4.2]: https://github.com/bmad-code-org/bmad-loop/commit/e4cce98fc6b6
[0.4.1]: https://github.com/bmad-code-org/bmad-loop/commit/d34e8bd609f3
[0.4.0]: https://github.com/bmad-code-org/bmad-loop/commit/ad6a292c0f41
[0.3.2]: https://github.com/bmad-code-org/bmad-loop/commit/243ea6f80b77
[0.3.1]: https://github.com/bmad-code-org/bmad-loop/commit/37dd884efaff
[0.3.0]: https://github.com/bmad-code-org/bmad-loop/commit/11a9d5a067a6
[0.2.0]: https://github.com/bmad-code-org/bmad-loop/commit/823adae1c047
[0.1.0]: https://github.com/bmad-code-org/bmad-loop/commit/274f0f5b6fd2
