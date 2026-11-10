# waves documentation

Start with the [project README](../README.md) for the overview and quick start. The
guides below go deeper, roughly in the order you'll need them.

## Using waves

- **[Setup guide](setup-guide.md)** — install the tools, pick a CLI, initialize a project, pass preflight, and uninstall.
- **[TUI guide](tui-guide.md)** — the dashboard: layout, key bindings, the settings editor, and troubleshooting.
- **[Features & functionality](FEATURES.md)** — the full capability matrix and policy reference.
- **[Terminal multiplexer backends](multiplexer-backends.md)** — which backend drives your agent sessions (tmux bundled; externals like the [herdr adapter](https://github.com/pbean/bmad-loop-adapter-herdr) install as packages), how selection works, and how external backends arrive.

## Extending waves

- **[Authoring CLI adapters & profiles](adapter-authoring-guide.md)** — using `waves probe-adapter` to collect + sanitize the hook payload shape, transcript location, and token schema a new CLI profile needs, plus the `CodingCLIAdapter` ABC and how an adapter class (and the profile selecting it) ships out-of-tree.
- **[Writing a waves plugin](plugin-authoring-guide.md)** — the plugin system: `plugin.toml` manifest, hooks, lifecycle stages, settings, the trust model, and workflow injection, with a worked walkthrough.
- **[Writing a Game Engine plugin](game-engine-plugin-guide.md)** — the game-engine layer (built on the plugin system): driving a live engine Editor, the `editor_mode` ↔ `[scm] isolation` coupling, a minimal Godot example.
- **[Writing a plugin for a specific Editor MCP](game-engine-mcp-guide.md)** — Editor-MCP specifics for the bundled Unity plugin: IvanMurzak vs CoplayDev, readiness probes, `per_worktree` isolation, and the full `WAVES_*` env-var reference.
- **[Porting waves to a new OS](porting-to-a-new-os.md)** — the four OS seams (terminal multiplexer, process lifecycle, hook interpreter, validate preflight), their registries and override env vars, and what a native-Windows port costs end to end.
- **[Testing map](testing.md)** — the test layers and their inventory: where each kind of test lives, the simulation scenarios (`simulate.py --list`), what only a live run can prove, and the conventions (ablation rule, sandbox fixtures, zero-token gates).
- **[The Test Architect (TEA) plugin](tea-plugin-guide.md)** — the bundled `waves-tea`: a red-phase acceptance scaffold before every story, the four TEA analyses once per epic, optional commit-time gates, and how artifacts are attributed to a scope so the two cadences never read each other's verdict.

## Project direction

- **[Roadmap](ROADMAP.md)** — planned and intentionally-deferred work.

For released changes, see the [CHANGELOG](../CHANGELOG.md).

## Contributing & community

- **[Contributing guide](../CONTRIBUTING.md)** — dev setup (uv + trunk), PR guidelines, and conventional commits.
- **[Testing strategy](testing.md)** — the layer model, fixture and ablation doctrines, quality guards, the zero-token invariant, and the CI/flake policy behind the suite.
- **[Code of Conduct](../.github/CODE_OF_CONDUCT.md)** — the Contributor Covenant we follow.
- **[Security policy](../SECURITY.md)** — how to report a vulnerability and what's in scope.
- **[Trademark guidelines](../TRADEMARK.md)** — proper use of the BMad name and brand.
