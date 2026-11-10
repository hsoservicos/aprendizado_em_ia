# LLM-held orchestration

`waves` ships two control loops. The LLM-held one is this fork's addition and,
since 3.0.0, what `waves run` launches: an LLM session holds the loop and drives
the same primitives through a machine-readable verb surface, while every
irreversible operation stays in Python. The deterministic engine is upstream's,
untouched, and runs under `waves run --deterministic`. `llm-run` is the old
spelling of the default and still works.

Nothing here is on by default. With `[llm] enabled = false` the fork behaves
exactly as upstream does.

## Why

The deterministic engine routes every outcome through a fixed pipeline and
numeric bounds. When a junction falls outside them — a session that dies without
a result, a review that revokes the dev sign-off, an attempt budget that runs out
with the work 90% done — the only move left is to pause and wait for a human.

That loop cannot read the failing log, form a theory, run a diagnostic, or decide
that a defect is worth fixing now and a residue worth deferring. It can only pick
a branch someone wrote in advance. This one can.

## Getting started

```bash
waves init --project /path/to/project --cli claude
```

Then in `.waves/loop/policy.toml`:

```toml
[llm]
enabled = true

[adapter.orchestrator]
name  = "claude"
model = "opus"
```

`[adapter.orchestrator]` is a separate binding on purpose: the model that holds
the control loop is a different decision from the one that writes the code. It
may name a CLI no other stage uses; the orchestrator then gets an adapter of its
own, built from that table, and never borrows another stage's binary.
Both tables are on the TUI's policy editor (`g`): `[llm]` is a section of its
own, and `[adapter.orchestrator]` sits with the other stage sections under a
header that says what it is — so the LLM that holds the loop is chosen where the
rest of the policy is, not only by hand in the file.

```bash
waves run --project /path/to/project --epic 2
waves tui  --project /path/to/project      # watch it
```

`waves run` refuses up front if the orchestrator skill or the CLI's hook config is
missing (and, with `[llm] enabled = false` in the policy, refuses and names
`--deterministic`). That check exists because the failure it replaces is silent: a coding
CLI that has never run in a project opens a first-run trust dialog, a spawned
session cannot answer one, and the initial prompt is typed into the dialog and
lost. The run would report a timeout many minutes later with a live-looking
window and nothing in the journal to say why.

## Resuming a paused run

An LLM-held run pauses rather than pressing on when it meets something it should
not decide alone. Pick it back up with **its own** resume:

```bash
waves run --resume <run-id>
```

Not `waves resume <run-id>` — that one rebuilds the deterministic
engine, and standing that up over an LLM-held run would put two orchestrators
with different decision models on one `state.json`. Each command refuses the
other's runs and names the right one.

The resume adopts the run rather than starting one: same run dir, same journal,
same mounted worktrees, and the turn numbering continues where it left off. That
is the point of the command. A fresh run would cut new worktrees from the
integration branch as it stands _now_, throwing away exactly the work a paused
run was holding onto.

It re-reads `config.yaml` and `policy.toml`, so a policy edit made while the run
was parked takes effect — and if the config it pinned at launch has since moved
(verify commands, launch binary, plugin allowlist) it says so on stderr before
driving. The launch-time scope flags are refused here: `--epic`, `--story` and
`--max-stories` are pinned in run state, so accepting them would silently ignore
them. A finished run, a live one, and a run id that matches nothing are all
refused.

## How it is put together

Four processes, with disjoint ownership.

```
waves run
│
├─ SUPERVISOR ─────────── owns engine.pid, signals, stop-request, crash.txt
│  │                      one turn per iteration; checks the turn contract
│  │
│  ├─ ORCHESTRATOR SESSION ─── tmux window · [adapter.orchestrator] · the LLM
│  │                            calls verbs from its own shell
│  │
│  └─ WATCHER (one per dispatch) ─ runs adapter.wait_for_completion
│       │                          writes tasks/<id>/session-result.json
│       └─ EXECUTOR SESSION ────── tmux window · [adapter.dev|review|…]
│
└─ VERBS ─────────────── short-lived processes: rebuild the host from the run
                          dir, perform ONE primitive, exit
```

**Why the supervisor exists.** A verb is short-lived, so no verb can own
`engine.pid`; between two verbs there would be no live pid and the dashboard
would read the run as interrupted.

**Why the watcher exists.** `wait_for_completion` is not a sleep — it holds the
stall-nudge budget, the mid-session token guard, spec-status sampling and
env-fault classification in process memory. A dispatch that blocked would make
the caller blind for the session's whole length; one that returned without a
watcher would drop that machinery and leave `await` to reimplement it, worse,
from artifacts.

**Why verbs are processes, not a daemon.** The orchestrator is a coding CLI with
a shell. `waves unit state` is the most natural thing it can call —
no client, no protocol, no server to die.

## The verbs

Twenty-three subcommands under `unit`. Success is one JSON document on stdout
with exit 0; failure is one JSON document on **stderr** with stdout empty and a
non-zero exit, carrying a `kind` from a closed vocabulary.

| Group           | Verbs                                                                            |
| --------------- | -------------------------------------------------------------------------------- |
| Read            | `state`, `pick`, `session-result`                                                |
| Story lifecycle | `open`, `close`, `commit`                                                        |
| Execution       | `dispatch`, `workflows` (`list` \| `dispatch`), `await`, `tail`, `nudge`, `kill` |
| Judgment        | `verify` (`dev` \| `review` \| `commands`)                                       |
| State           | `phase`, `journal`, `attention`, `notify`, `pause`, `finish`, `boundary`         |
| Close           | `sprint advance`, `ledger` (`add` \| `close` \| `list`), `rollback`              |

Error kinds: `invalid-args`, `not-found`, `illegal-transition`, `lock-timeout`,
`git`, `state-conflict`, `env`.

**Verbs measure and act; they never route.** `verify` reports `fixable`,
`env_fault` and `contradiction` by name rather than a verdict, because
collapsing them to pass/fail would put the deciding back inside the tool — which
is the thing this design moved out.

**`dispatch` refuses what would otherwise fail silently.** A role outside the
known set (`dev`, `review`, `triage`, and the plugin workflow roles `atdd`, `td`,
`trace`, `nfr`, `test-review`, `automate`, `retro-prep`) is `invalid-args` — the
CLI is chosen in `[adapter.<role>]`, never named as the role — and a story the
run has not `open`ed is `not-found`. Both were measured on 2026-09-05: an
orchestrator dispatched `codex` as a role and skipped `unit open`; the session
ran on the wrong CLI and the dashboard showed no story at all.

**Plugin workflows run here too.** The deterministic engine injects every
plugin-provided workflow itself — the TEA acceptance scaffold (`atdd`) before a
story's first dev session, the Test Architect's analyses at each epic boundary.
An LLM-held run drives them through `unit workflows`: `list <stage> --story
<key>` (or `--epic <n>` at `post_epic_boundary`) names what is due and what
already ran, from the same registry the dashboard paints its boundary steps
from; `dispatch <stage> --name <step>` launches one exactly as the engine would
— the manifest's prompt, the step's own role and adapter, the
`<plugin>.<step>` label, the `workflow-start` entry — and the watcher writes
`workflow-end` and stamps a boundary step `done`/`failed` for the sprint tree.
The plugin's in-process hooks (artifact attribution, the commit-time gates, the
boundary's own commit) stay the engine's for now; the orchestrator judges a
step's outcome from its result and journals the judgment.

**Git, the sprint board, worktrees and the ledger are never reachable by free
shell.** Only through verbs. This continues an invariant the package already
held: no bundled skill runs git, and the unconstrainable actor is a coding-CLI
session with shell access.

## Watching a live session

A dispatch returns as soon as the session is up; waiting is its own verb, and the
condition is the caller's:

```
unit dispatch dev 2-1-a --prompt-file /tmp/p.md
unit await 2-1-a-dev-1 --until end --until match --match 'CRITICAL|FAILED' --quiet 180
unit tail  2-1-a-dev-1 --from-offset 40213
unit nudge 2-1-a-dev-1 "you are rewriting the test, not fixing the code"
```

Conditions: `end`, `match:<regex>`, `quiet:<s>`, `stale-heartbeat`, `vanished`,
plus the timeout that always bounds the wait.

Two orderings are load-bearing. A landed result reads as `end` even when the
window is gone, because the adapter tears every window down on completion and
`vanished` would otherwise fire on every healthy session. A missing heartbeat is
not staleness: a session that has not written its first beat is starting, not
dead.

**The honest limit:** the caller only thinks between tool calls, so it reacts
when the wait returns, not when something happens. The granularity of its
attention is exactly the condition it wrote. `--until end` is choosing to be
blind, which is a legitimate choice.

## The turn contract

A turn is the life of one orchestrator session: prompt, N tool calls, turn-end.
The normal turn is long — ideally a whole epic in one session, which is the live
context this design exists to buy. Relaunch is recovery (a crash, a compaction,
a timeout), not a cadence.

That is what makes the contract structural rather than bureaucratic: **the
journal is the orchestrator's memory across relaunches.** A session that dies
mid-story is only resumable if the previous one recorded why it decided what it
decided. So a turn opens with `unit state`, closes with `unit journal turn`, and
records each junction decision with its reason as it makes it.

At turn end the supervisor compares state and journal against the turn's start:

| Situation                                     | Action                                                     |
| --------------------------------------------- | ---------------------------------------------------------- |
| Terminal (finished, paused, stopped, crashed) | end the run                                                |
| The turn wrote state or journal               | relaunch with a fresh digest; the budget goes back to full |
| The turn wrote nothing, `protocol = "strict"` | violation: relaunch naming it, and spend budget            |
| `max_turn_relaunches` consecutive violations  | pause, naming the count                                    |

The budget counts _consecutive_ silent turns, and any productive turn clears it,
because the question it answers is whether the orchestrator is broken now — not
how long the run has been going. Counting every relaunch instead reads a long
healthy run as a failing one: a real run finished an epic across four turns and
paused on the fifth, having done nothing wrong.

Only entries the _orchestrator_ wrote count. The supervisor writes `turn-start`,
`session-start` and `session-end` itself, and counting those would have it
measuring its own bookkeeping — the contract would never fire once, and the
feature would look fine.

Terminal beats the write check: a turn that paused the run on purpose and then
ended did exactly the right thing.

## What pauses a run — the closed list

1. The LLM calls `unit pause`, legitimate in exactly three cases: a genuinely
   ambiguous product decision, a risk of destroying work, or systemic failure —
   consecutive stories failing for the same cause that is not the story's.
2. `max_turn_relaunches` exhausted: the orchestrator itself is broken.
3. An environment fault no session can fix.
4. A human asked for `stop`.

**Not pausing:** a failed verify, a failed review, an exhausted review budget, a
red epic boundary, a session that died without a result, a dev/review
contradiction. Those are judgment junctions — the orchestrator decides and
proceeds, recording why.

A story owing external human action parks _the story_ in `awaiting-operator`,
never the run.

## Isolation from upstream

This fork shares nothing with upstream except what describes the project.

| Isolated (tool-level)                                     | Shared (project-level)                |
| --------------------------------------------------------- | ------------------------------------- |
| `.waves/loop/` — runs, policy, archive, plugins, profiles | `sprint-status.yaml`                  |
| multiplexer sessions `waves-<id>`                         | `deferred-work.md`                    |
| git refs for unit branches                                | story specs, planning artifacts       |
| `WAVES_*` environment                                     | `_bmad/bmm/config.yaml`, the git repo |

The board and the ledger describe the project, not the tool driving it. Two
copies would mean two readings of what is done, and neither would be wrong —
worse than one being stale.

Everything namespaced derives from a single constant in `namespace.py`. Spelling
it out per site is how a rename half-lands: the state dir moves, the session
prefix does not, and the dashboard stops finding runs that are right there.

**Do not point upstream's `waves` at a project with LLM-held runs.** It picks
its engine from `RunState.source` and has no branch for `llm`, so it would
rebuild the deterministic engine over one. This fork refuses the mirror image of
that; upstream cannot.

## Simulations

```bash
python scripts/simulate.py --list
python scripts/simulate.py --all --repeat 5
```

Eleven scenarios, each building its own sandbox and asserting what it produced.
The orchestrator is scripted so the failure paths are reachable on purpose:
reaching them with a real model means waiting for one to misbehave on cue.
Everything below the judgement stays real — run directory, state machine, verbs,
board, git.

## Configuration

```toml
[llm]
enabled                 = false   # opt-in
protocol                = "strict"   # or "advisory"
max_turn_relaunches     = 20
turn_timeout_min        = 30
await_default_timeout_s = 900
await_default_quiet_s   = 180
```

Nothing project-specific belongs in the tool or the skill. Paths come from
`ProjectPaths`, verification commands from `[verify]`, thresholds from `[llm]`,
and `--until match:` patterns from the caller at call time — a default regex
would be baked-in project knowledge.
