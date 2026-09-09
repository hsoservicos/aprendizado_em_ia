#!/usr/bin/env python3
"""
BMAD Method — Questionário de Inicialização do Template
========================================================

Executa após o clone do template para configurar o projeto.
Gera: AGENTS.md, CLAUDE.md, _bmad/custom/config.toml, _bmad/config.user.toml

Uso:
    python3 project-init-questionnaire.py [--project-root /caminho/para/projeto]

Saída:
    - _bmad/custom/config.toml (configuração do projeto)
    - _bmad/config.user.toml (configuração do usuário)
    - AGENTS.md (instruções do agente)
    - CLAUDE.md (instruções do Claude Code)
"""

import argparse
import os
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════════
# Constantes
# ═══════════════════════════════════════════════════════════════════════════════

VERSION = "1.0.0"
DATE = datetime.now().strftime("%Y-%m-%d")

COMMUNICATION_LANGUAGES = {
    "1": "Português do Brasil",
    "2": "English",
    "3": "Español",
}

PROJECT_TYPES = {
    "1": "greenfield",
    "2": "brownfield",
}

SKILL_LEVELS = {
    "1": "beginner",
    "2": "intermediate",
    "3": "advanced",
}

STACK_SUGGESTIONS = [
    "Python 3.14",
    "Node.js 22+",
    "PHP 8.4",
    "PostgreSQL 18",
    "Docker",
    "React",
    "Vue.js",
    "FastAPI",
    "Django",
    "Laravel",
    "Next.js",
    "Tailwind CSS",
]


# ═══════════════════════════════════════════════════════════════════════════════
# Funções auxiliares
# ═══════════════════════════════════════════════════════════════════════════════

def clear_screen():
    """Limpa a tela do terminal."""
    os.system('clear' if os.name != 'nt' else 'cls')


def print_header():
    """Exibe o cabeçalho do questionário."""
    print("=" * 70)
    print("  BMAD Method — Questionário de Inicialização do Template")
    print(f"  Versão {VERSION} | {DATE}")
    print("=" * 70)
    print()
    print("  Este questionário configura o template para o seu projeto.")
    print("  Responda as perguntas abaixo para gerar os arquivos de configuração.")
    print()


def print_separator():
    """Exibe um separador visual."""
    print("-" * 70)


def get_input(prompt: str, required: bool = True, default: str = "") -> str:
    """Obtém entrada do usuário com validação."""
    while True:
        if default:
            user_input = input(f"  {prompt} [{default}]: ").strip()
            if not user_input:
                user_input = default
        else:
            user_input = input(f"  {prompt}: ").strip()

        if user_input or not required:
            return user_input

        print(f"  ⚠️  Este campo é obrigatório. Tente novamente.")


def get_choice(prompt: str, choices: dict, default: str = "1") -> str:
    """Obtém escolha do usuário de uma lista de opções."""
    print(f"\n  {prompt}")
    for key, value in choices.items():
        marker = "→" if key == default else " "
        print(f"  {marker} {key}. {value}")

    while True:
        choice = input(f"\n  Sua escolha [{default}]: ").strip() or default
        if choice in choices:
            return choice
        print(f"  ⚠️  Opção inválida. Escolha uma das opções listadas.")


def get_multiple_choice(prompt: str, options: list, min_selections: int = 1) -> list:
    """Obtém múltiplas escolhas do usuário."""
    print(f"\n  {prompt}")
    print("  (Digite os números separados por vírgula, ex: 1,3,5)")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")

    while True:
        choices = input(f"\n  Sua escolha: ").strip()
        if not choices:
            continue

        try:
            selected = [options[int(c.strip()) - 1] for c in choices.split(",")]
            if len(selected) >= min_selections:
                return selected
            print(f"  ⚠️  Selecione pelo menos {min_selections} opção(ões).")
        except (ValueError, IndexError):
            print(f"  ⚠️  Formato inválido. Use números separados por vírgula.")


def slugify(text: str) -> str:
    """Converte texto em slug (kebab-case)."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text


# ═══════════════════════════════════════════════════════════════════════════════
# Coleta de dados
# ═══════════════════════════════════════════════════════════════════════════════

def collect_project_info() -> dict:
    """Coleta todas as informações do projeto."""
    info = {}

    print_header()

    # 1. Nome do projeto
    print_separator()
    print("  📋 PERGUNTA 1 de 8: Nome do Projeto")
    print_separator()
    info["project_name"] = get_input(
        "Nome do projeto (ex: meu-projeto)",
        required=True
    )
    info["project_slug"] = slugify(info["project_name"])

    # 2. Descrição breve
    print()
    print_separator()
    print("  📋 PERGUNTA 2 de 8: Descrição do Projeto")
    print_separator()
    info["project_description"] = get_input(
        "Descrição breve do projeto (1-2 frases)",
        required=True
    )

    # 3. Tipo de projeto
    print()
    print_separator()
    print("  📋 PERGUNTA 3 de 8: Tipo de Projeto")
    print_separator()
    choice = get_choice(
        "Este projeto é:",
        PROJECT_TYPES,
        default="1"
    )
    info["project_type"] = PROJECT_TYPES[choice]

    # 4. Stack principal
    print()
    print_separator()
    print("  📋 PERGUNTA 4 de 8: Stack Tecnológico")
    print_separator()
    info["stack"] = get_multiple_choice(
        "Selecione as tecnologias principais do projeto:",
        STACK_SUGGESTIONS,
        min_selections=1
    )

    # 5. Idioma do projeto
    print()
    print_separator()
    print("  📋 PERGUNTA 5 de 8: Idioma do Projeto")
    print_separator()
    choice = get_choice(
        "Idioma para documentação e comunicação:",
        COMMUNICATION_LANGUAGES,
        default="1"
    )
    info["language"] = COMMUNICATION_LANGUAGES[choice]

    # 6. Nome do usuário
    print()
    print_separator()
    print("  📋 PERGUNTA 6 de 8: Seu Nome")
    print_separator()
    info["user_name"] = get_input(
        "Seu nome (para configuração do agente)",
        required=True
    )

    # 7. Nível de experiência
    print()
    print_separator()
    print("  📋 PERGUNTA 7 de 8: Nível de Experiência")
    print_separator()
    choice = get_choice(
        "Seu nível de experiência com desenvolvimento de software:",
        SKILL_LEVELS,
        default="2"
    )
    info["skill_level"] = SKILL_LEVELS[choice]

    # 8. Objetivo principal (opcional)
    print()
    print_separator()
    print("  📋 PERGUNTA 8 de 8: Objetivo Principal (opcional)")
    print_separator()
    info["objective"] = get_input(
        "Qual o objetivo principal deste projeto? (pressione Enter para pular)",
        required=False,
        default=""
    )

    return info


# ═══════════════════════════════════════════════════════════════════════════════
# Geração de arquivos
# ═══════════════════════════════════════════════════════════════════════════════

def generate_config_toml(info: dict, output_path: Path):
    """Gera _bmad/custom/config.toml."""
    content = f'''# BMAD Method — Configuração do Projeto
# Gerado automaticamente pelo questionário de inicialização
# Data: {DATE}

[core]
project_name = "{info['project_name']}"
project_description = "{info['project_description']}"
document_output_language = "{info['language']}"
output_folder = "_bmad-output"

[project]
type = "{info['project_type']}"
stack = {info['stack']}
slug = "{info['project_slug']}"

[project.context]
objective = "{info['objective']}"
'''

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")


def generate_config_user_toml(info: dict, output_path: Path):
    """Gera _bmad/config.user.toml."""
    content = f'''# BMAD Method — Configuração do Usuário
# Gerado automaticamente pelo questionário de inicialização
# Data: {DATE}
# ATENÇÃO: Este arquivo é pessoal e NÃO deve ser commitado

[core]
user_name = "{info['user_name']}"
communication_language = "{info['language']}"

[modules.bmm]
user_skill_level = "{info['skill_level']}"
'''

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")


def generate_agents_md(info: dict, output_path: Path):
    """Gera AGENTS.md."""
    stack_list = "\n".join([f"  - {s}" for s in info['stack']])

    content = f'''# AGENTS.md

BMAD Method project — {info['project_description']}

This file is read by **OpenCode**; **Claude Code** reads `CLAUDE.md`,
which imports this file. Both coding agents are first-class and share
one configuration, skill set, and toolchain.

## Project Setup

- **Project**: {info['project_name']}
- **Type**: {info['project_type']}
- **User**: {info['user_name']}
- **Communication language**: {info['language']}
- **Artifacts output**: `_bmad-output/`
- **Project knowledge**: `docs/`
- **Config files**: `_bmad/config.toml`, `_bmad/config.user.toml`
- **Agent instructions**: `AGENTS.md` (OpenCode) + `CLAUDE.md` (Claude Code)
- **Claude Code settings**: `.claude/settings.json`
- **Tools Registry**: `_bmad-output/tools-registry.md`

## Stack

{stack_list}

## Coding Agents

| Concern | OpenCode | Claude Code |
|---------|----------|-------------|
| Instructions | `AGENTS.md` | `CLAUDE.md` → `@AGENTS.md` |
| Skill source | `.agents/skills/` (57) | `.claude/skills/` (57) |
| Skill invocation | `.opencode/commands/*.md` wrappers | native discovery |
| Tool allow-list | inherits shell | `.claude/settings.json` |
| RTK token compression | `~/.config/opencode/plugins/rtk.ts` | `.claude/settings.json` → `PreToolUse` hook |

## Onboarding — first steps

Anyone using this repo must run the pre-flight in
**`_bmad-output/getting-started.md`** first, then follow one of two tracks:

- **Track A — greenfield**: `/bmad-help` → the 5-phase lifecycle
- **Track B — brownfield / legacy**: `/bmad-project-context` → `/bmad-code-review` → `/bmad-build`

## BMAD Skills

57 skills, installed once and exposed to **both** agents.
Entry points are identical from either agent.

### Entry Points

| Command | Purpose |
|---------|---------|
| `bmad-help` | Start here — orient to workflow |
| `bmad-build` | Main code implementation |
| `bmad-build-auto` | Autonomous unattended build loop |
| `bmad-brainstorming` | Ideation and creative exploration |
| `bmad-forge-idea` | Pressure-test an idea |
| `bmad-create-prd` | Product requirements document |
| `bmad-architecture` | System architecture design |
| `bmad-ux` | UX patterns and design specs |
| `bmad-create-epics-and-stories` | Break work into trackable stories |
| `bmad-sprint-planning` | Sprint readiness and status |
| `bmad-code-review` | Adversarial code review |
| `bmad-retrospective` | Epic retrospective |
| `bmad-docker` | Docker containerization |
| `bmad-python314` | Python 3.14+ features |
| `bmad-php84` | PHP 8.4 features |
| `bmad-postgres18` | PostgreSQL 18 features |

### Skill Invocation Rule

Skills must be rendered via the shared script:

```bash
# Claude Code
uv run _bmad/scripts/render_skill.py --project-root {os.path.dirname(output_path)} --skill .claude/skills/<skill-name>
# OpenCode
uv run _bmad/scripts/render_skill.py --project-root {os.path.dirname(output_path)} --skill .agents/skills/<skill-name>
```

### BMAD Workflow Phases

1. **Clarify** — `bmad-help`, `bmad-brainstorming`, `bmad-forge-idea`
2. **Plan** — `bmad-create-prd`, `bmad-architecture`, `bmad-ux`, `bmad-create-epics-and-stories`
3. **Build** — `bmad-build`, `bmad-build-auto`
4. **Review** — `bmad-code-review`, `bmad-checkpoint-preview`
5. **Learn** — `bmad-retrospective`

## Prerequisites

- **Node.js** >= 22 (LTS)
- **Python** >= 3.12
- **uv** — required for rendering skills
- **Git** — required for updates
- **GitHub CLI** (`gh`) — repo / PR / release operations
- **ripgrep** — fast search, RTK dependency
- **RTK** — token compression proxy
- **Coding agent**: OpenCode and/or Claude Code

## Updating BMAD

```bash
npx bmad-method install
```

## Project State

This is a **{info['project_type']}** project.
New here? Run the pre-flight in `_bmad-output/getting-started.md`,
then `/bmad-help` to begin.
'''

    output_path.write_text(content, encoding="utf-8")


def generate_claude_md(info: dict, output_path: Path):
    """Gera CLAUDE.md."""
    content = f'''# CLAUDE.md

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

## Claude Code specifics

- **Skills**: invoke with `/bmad-help`, `/bmad-build`, `/bmad-code-review`, etc.
  — or let the model pick.
- **Skill rendering** (never run workflow files directly):
  ```bash
  uv run _bmad/scripts/render_skill.py --project-root {os.path.dirname(output_path)} --skill .claude/skills/<skill-name>
  ```
- **Tooling**: `uv`, `rtk`, `rg`, `gh`, `crewai`, `npx bmad-method` are
  pre-approved in `.claude/settings.json`.
- **RTK**: Bash output is auto-compressed by the `PreToolUse` hook.
  See `@.claude/RTK.md`. For a raw command: `RTK_DISABLED=1 <cmd>`.

## Attribution

End commit messages with:

```
Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
```
'''

    output_path.write_text(content, encoding="utf-8")


# ═════════════════════════════════════════════════════════════════════════════ Validação e execução

def validate_project_root(path: Path) -> bool:
    """Valida se o diretório raiz do projeto é válido."""
    if not path.exists():
        print(f"  ❌ Diretório não existe: {path}")
        return False

    if not path.is_dir():
        print(f"  ❌ Não é um diretório: {path}")
        return False

    # Verificar se é um repositório git
    if not (path / ".git").exists():
        print(f"  ⚠️  Aviso: Não é um repositório Git")
        print(f"     Recomenda-se inicializar com: git init")

    return True


def print_summary(info: dict, output_files: dict):
    """Exibe resumo das configurações geradas."""
    print()
    print("=" * 70)
    print("  ✅ CONFIGURAÇÃO CONCLUÍDA!")
    print("=" * 70)
    print()
    print("  📁 Arquivos gerados:")
    for name, path in output_files.items():
        print(f"     ✓ {path}")
    print()
    print("  📋 Resumo do projeto:")
    print(f"     Nome: {info['project_name']}")
    print(f"     Tipo: {info['project_type']}")
    print(f"     Stack: {', '.join(info['stack'])}")
    print(f"     Idioma: {info['language']}")
    print(f"     Usuário: {info['user_name']}")
    print()
    print("  🚀 Próximos passos:")
    print()
    if info['project_type'] == 'greenfield':
        print("     1. Abra o agente: opencode OU claude")
        print("     2. Execute: /bmad-help")
        print("     3. Siga a Trilha A (Projeto Novo)")
    else:
        print("     1. Abra o agente: opencode OU claude")
        print("     2. Execute: /bmad-help")
        print("     3. Siga a Trilha B (Projeto Legado)")
    print()
    print("  📖 Documentação:")
    print("     - getting-started.md: Primeiros passos")
    print("     - implementation-playbook.md: Manual detalhado")
    print("     - bmad-project-lifecycle-guide.md: Ciclo de vida")
    print()
    print("=" * 70)


# ═════════════════════════════════════════════════════════════════════════════
# Main
# ═════════════════════════════════════════════════════════════════════════════

def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="BMAD Method — Questionário de Inicialização do Template"
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Caminho para o diretório raiz do projeto (padrão: diretório atual)"
    )
    args = parser.parse_args()

    project_root = args.project_root.resolve()

    # Validar diretório
    if not validate_project_root(project_root):
        sys.exit(1)

    # Coletar informações
    info = collect_project_info()

    # Preparar caminhos de saída
    output_files = {
        "config_toml": project_root / "_bmad" / "custom" / "config.toml",
        "config_user_toml": project_root / "_bmad" / "config.user.toml",
        "agents_md": project_root / "AGENTS.md",
        "claude_md": project_root / "CLAUDE.md",
    }

    # Confirmar antes de gerar
    print()
    print_separator()
    print("  ⚠️  ATENÇÃO: Os seguintes arquivos serão criados/sobrescritos:")
    print_separator()
    for name, path in output_files.items():
        exists = "⚠️  EXISTE" if path.exists() else "✓ novo"
        print(f"     {exists}: {path}")

    print()
    confirm = input("  Confirma a geração? (s/N): ").strip().lower()
    if confirm not in ("s", "sim", "y", "yes"):
        print("  ❌ Operação cancelada.")
        sys.exit(0)

    # Gerar arquivos
    print()
    print("  🔄 Gerando arquivos de configuração...")

    generate_config_toml(info, output_files["config_toml"])
    print(f"     ✓ {output_files['config_toml']}")

    generate_config_user_toml(info, output_files["config_user_toml"])
    print(f"     ✓ {output_files['config_user_toml']}")

    generate_agents_md(info, output_files["agents_md"])
    print(f"     ✓ {output_files['agents_md']}")

    generate_claude_md(info, output_files["claude_md"])
    print(f"     ✓ {output_files['claude_md']}")

    # Exibir resumo
    print_summary(info, output_files)


if __name__ == "__main__":
    main()
