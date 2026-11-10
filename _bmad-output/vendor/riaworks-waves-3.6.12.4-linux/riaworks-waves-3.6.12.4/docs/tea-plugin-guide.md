# The Test Architect (TEA) plugin

The bundled **`waves-tea`** plugin drives the BMAD Method's **Test
Architect (TEA)** module — the "Murat" agent and its `bmad-testarch-*` workflows —
at the cadence each of its steps actually pays for: a red-phase acceptance scaffold
before every story, the four analyses once per epic, and optional commit-time
gates for a project that wants them.

Like the [game-engine layer](game-engine-plugin-guide.md), it is **just a plugin**
on the general [plugin system](plugin-authoring-guide.md) — same `plugin.toml`
manifest, same [lifecycle hooks](plugin-authoring-guide.md#stage-reference), same
trust model. It ships bundled
(`src/riaworks_waves_loop/data/plugins/waves-tea/`) and **on by
default**: `[plugins] enabled` defaults to `["waves-tea"]`, so a fresh
`init` and an absent `[plugins]` table both run it; `enabled = []` is the
opt-out. In a project without the Test Architect module installed it is
**inert** — enabled, listed, contributing nothing, with the reason in
`waves validate` — rather than a startup failure. **Read the
[plugin authoring guide](plugin-authoring-guide.md) first**
for the manifest, settings, hook and trust fundamentals — this guide covers only
the TEA-specific slice.

> **History.** Until 2026-09-05 two plugins shipped side by side: `tea`, inherited
> from [bmad-loop](https://github.com/bmad-code-org/bmad-loop), which ran all six
> TEA steps per story, and an epic-boundary plugin of the same family. Enabled
> together they did five of the six twice; enabled apart each was wrong for half
> the work. They are one plugin now. If your `policy.toml` still names `tea` or
> `tea-epic`, replace both with `waves-tea`.

## Prerequisite: install TEA in your project

The plugin **invokes** the BMAD Method's TEA skills; it does not contain them.

```bash
npx bmad-method install     # choose "Test Architect"
```

That writes `_bmad/tea/config.yaml` and compiles the `bmad-testarch-*` skills into
your CLI's skill tree. The plugin probes for that config file at startup: absent,
the plugin declares itself **inert** — no step runs, the sprint tree lists no
boundary rows, `validate` names the missing file and both ways out. Set
`require_tea = true` to make the absence a startup failure instead, for a
project that demands TEA.

## Enabled by default

The plugin is the **policy default**: `PluginsPolicy.enabled` is
`("waves-tea",)`, the template `init` writes says the same, and an
absent `[plugins]` table means the default. ATDD before every story and the Test
Architect's analyses at every epic boundary are the cadence a project gets
without asking; turning them off is the operator's decision:

```toml
[plugins]
enabled = []                       # opt out of the TEA plugin entirely

[plugins.waves-tea]
atdd_enabled = false               # or turn off one step and keep the rest
```

**The shipped defaults are the measured configuration.** You do not need a
`[plugins.waves-tea]` table at all unless you want to change one.

### On the dashboard

With TEA installed, the TUI shows the plugin's work without any setting: the
tasks table's `atdd` column (`…` running, `✓` done, `✗` failed, `-` never ran)
and a ` ·atdd✓` suffix on the story in the sprint tree, plus one `boundary:
<step>` row per epic for `epic_td`, `epic_trace`, `epic_nfr`, `epic_test_review`
and `epic_retro_prep`, painted from the run's `boundary_progress`. Both loops
paint alike — see below.

### Under `llm-run`

The deterministic engine injects the workflows itself. An LLM-held run drives
them through `unit workflows`: `list pre_dev_phase --story <key>` before the
first dev dispatch (it answers `atdd`, pending), `dispatch pre_dev_phase --name
atdd --story <key>` to run it, and at a boundary `list post_epic_boundary --epic
<n>` then one `dispatch` per step, in the listed order. Each dispatch journals
`workflow-start` and the watcher `workflow-end`, stamping the boundary step for
the sprint tree — the same records the engine writes. What does **not** run under
`llm-run` yet: the plugin's in-process hooks — artifact attribution, the
commit-time gates and the boundary's own commit. The orchestrator reads each
step's result and journals its judgment instead; the boundary's writes stay in
the tree for it to commit or ledger. See
[docs/llm-orchestration.md](llm-orchestration.md).

## The twelve steps and where they run

| Step                | TEA workflow                | Stage                | Default |
| ------------------- | --------------------------- | -------------------- | ------- |
| `atdd`              | `bmad-testarch-atdd`        | `pre_dev_phase`      | **on**  |
| `story_td`          | `bmad-testarch-test-design` | `post_dev_phase`     | off     |
| `story_automate`    | `bmad-testarch-automate`    | `post_dev_phase`     | off     |
| `story_trace`       | `bmad-testarch-trace`       | `pre_commit_gate`    | off     |
| `story_nfr`         | `bmad-testarch-nfr`         | `pre_commit_gate`    | off     |
| `story_test_review` | `bmad-testarch-test-review` | `pre_commit_gate`    | off     |
| `epic_td`           | `bmad-testarch-test-design` | `post_epic_boundary` | **on**  |
| `epic_trace`        | `bmad-testarch-trace`       | `post_epic_boundary` | **on**  |
| `epic_nfr`          | `bmad-testarch-nfr`         | `post_epic_boundary` | **on**  |
| `epic_test_review`  | `bmad-testarch-test-review` | `post_epic_boundary` | **on**  |
| `epic_automate`     | `bmad-testarch-automate`    | `post_epic_boundary` | off     |
| `epic_retro_prep`   | —                           | `post_epic_boundary` | **on**  |

Each runs as an extra agent session through its own role's adapter, with
`workflow-start` / `workflow-end` journal entries. Because sweep bundles run the
same inherited dev/review pipeline, the per-story steps fire for **sweep bundles
too**, with no sweep-specific code.

### Why ATDD runs before the code

`bmad-testarch-atdd` **refuses** to emit a test without `test.skip()` — its own
`step-04c-aggregate.md` raises if one is missing — because it is a **red-phase**
scaffold: written first, unskipped by the implementation. Bound to
`post_dev_phase`, the only in-unit stage that existed before, it produced a skipped
scaffold for code already written, which gates nothing. The `pre_dev_phase` stage
exists for it.

Two properties of that stage are positional and load-bearing:

- it is dispatched **before** `baseline_untracked` is captured, so the scaffold
  survives the rollback of a failed attempt (that snapshot is what a rollback
  subtracts — anything outside it counts as the attempt's own work);
- it fires only on a story's **first attempt**, so a retry does not regenerate a
  net the previous attempt is midway through turning green.

### Why the four analyses default to the epic

`test-design`, `trace`, `nfr` and `test-review` analyse a **body of work**. Run per
story they re-analyse the same ground once per story — 48 to 77 minutes of it,
measured downstream — and `automate` writes a fixture per story instead of one the
epic shares. Their per-story twins ship **off**: turn one on when you want a
commit-time gate and are willing to pay three extra agent sessions per commit.

At the boundary the six steps run **in declaration order**, and the order is a
contract: `epic_automate` reads the `trace` and `test-review` that just ran, and
`epic_retro_prep` reads all four reports plus, if `automate` committed, that commit
too.

## Artifact attribution: why the gates can be trusted

Every TEA skill writes to a **fixed name** directly under the configured
`test_artifacts` directory — `nfr-assessment.md`, `gate-decision.json`,
`test-review.md` — with nothing in the name saying which story or epic the verdict
is about. Run in two cadences, the epic's report overwrites the story's, and a gate
that discovered its artifact by glob or by "the most recent file" would veto a
commit on the other cadence's verdict.

Their output path is not configurable either: five of the six TEA skills expose
only `activation_steps_*`, `persistent_facts` and `on_complete`, and the sixth's
`output_file_override` is a scalar with no story token.

So attribution is **measured, not requested**. The plugin snapshots the artifacts
directory before each of its sessions and diffs it afterwards; whatever appeared or
changed is that session's output, whatever the session chose to name it. The delta
is **copied** — never moved, so your CI keeps finding TEA's file where TEA put it —
into a directory computed from the scope:

```text
<test_artifacts>/riaworks-waves/story/<story-key>/…
<test_artifacts>/riaworks-waves/epic/<n>/…
```

A gate then reads a path it **calculated**, not one it searched for. Resolve the
whole surface with:

```bash
waves tea-config --json
```

## The two gates

A step marked `<step>_enforce` has its verdict read and acted on. Both gates are
**fail-open**: a gate not enforced, with no artifact, or with an artifact that does
not parse into a known verdict never stops anything. `PASS` and `WAIVED` never
block; only a confidently-parsed `FAIL` or `CONCERNS` acts.

**Per story, at commit** (`story_trace_enforce`, `story_nfr_enforce`,
`story_test_review_enforce`). The plugin reads the verdict in `on_pre_commit` — the
first vetoable stage after the `pre_commit_gate` sessions have written — and
`pause`-vetoes, so the story **escalates for a human** instead of landing. Both
stages fire unconditionally before every commit, so enforcement holds even when
`review.trigger = "recommended"` skips the orchestrator's review loop entirely.

**Per epic, at a boundary** (`epic_trace_enforce`, `epic_nfr_enforce`,
`epic_test_review_enforce`). Nothing at a boundary can veto: there is no unit to
defer and the epic's stories are already committed. Instead the plugin **reports a
failed boundary step**, which makes the boundary red — and `[gates] epic_gate =
"on-failure"` turns a red boundary into a pause. An all-green boundary rolls into
the next epic unattended.

Verdicts the plugin read are recorded on the shared context (`tea_gates`) as a
breadcrumb for the journal, whether or not they enforced.

## Who commits what the boundary wrote

The reports, and any test file `epic_automate` wrote, land in the working tree with
no unit to carry them. Left there, the next story's dev session finds them and
sweeps them into **its** commit — wrong author, wrong message, and a baseline check
that no longer means anything. So the plugin commits its own output, once, at the
end of the boundary (`commit_boundary_writes`, on by default), after running the
project's own `[verify]` commands (`verify_before_commit`, on by default). A red
verify commits nothing, leaves the tree for inspection, writes the reason to the
run's ATTENTION file, **and reports the boundary step as failed**.

`epic_automate` carries one more guard: it is skipped when the working tree was
**already dirty when the boundary started**. The measurement that matters is the
one taken on _entry_ (`ctx.dirty_baseline`) — by the time it runs, the four reports
have written their own artifacts, so asking "is the tree dirty now" would veto the
step at every boundary, deterministically.

## Settings reference

| Setting                              | Default   | Effect                                                                                                  |
| ------------------------------------ | --------- | ------------------------------------------------------------------------------------------------------- |
| `require_tea`                        | `false`   | `false` = inert, with the reason, when the Test Architect module is not installed; `true` = fail fast.  |
| `require_test_location_fact`         | `false`   | Fail fast unless the managed `_bmad/custom` files are present.                                          |
| `test_location_hint`                 | `""`      | Empty = say nothing about where to write. Set it and the sentence joins the two writing steps' prompts. |
| `<step>_enabled`                     | see table | Turn one step on or off.                                                                                |
| `story_*_enforce` / `epic_*_enforce` | `false`   | Act on that step's verdict (escalate at commit / red boundary).                                         |
| `commit_boundary_writes`             | `true`    | Commit what the boundary wrote, as one commit.                                                          |
| `verify_before_commit`               | `true`    | Run the project's `[verify]` commands before that commit.                                               |

All of them are editable in the TUI: **Settings → Plugins**, where the switch
enables the plugin and the sub-panel below carries its configuration.

`<step>_enforce` is deliberately **not** named `<step>_blocking`. `<name>_blocking`
is the generic [workflow overlay](plugin-authoring-guide.md#making-a-workflow-configurable)
and means "the SESSION must complete"; `_enforce` means "the VERDICT must not be
FAIL/CONCERNS". Two questions, read from two places, so two names.

## What `init` writes into `_bmad/`

When TEA is installed, `waves init` also writes two per-skill
override files in the BMAD Method's own customization channel:

```text
_bmad/custom/bmad-testarch-atdd.toml
_bmad/custom/bmad-testarch-automate.toml
```

Each carries one `persistent_facts` entry — resolved by
`_bmad/scripts/resolve_customization.py` on **every** activation of that skill,
whether the loop invoked it, a wave front did, or you did by hand — stating that an
executable test belongs in the project's own suite and that only reports and
checklists belong under `test_artifacts`. The fact names **no path, framework or
suite command**: it restates the separation each skill's own `workflow.yaml`
already encodes.

Both files open with a managed header. A file **without** that header belongs to
the project and is never overwritten — it is reported instead. Refresh them at any
time with:

```bash
waves tea-config --write
```

## Worktree seeding

TEA's runtime (`_bmad/`) and its compiled per-CLI skills are commonly gitignored or
not guaranteed in a fresh checkout, so the plugin declares `seed_globs` to prime
them into an isolated per-worktree checkout. These no-op under in-place
(`scm.isolation = "none"`) mode and matter once worktrees are used.

## What is deliberately NOT here

A project's own integration suite — docker compose, a disposable database, a
package-filtered test command — is project-specific. It belongs in a
`[hooks.post_epic_boundary]` of a project plugin, and needs no copied workflow.
