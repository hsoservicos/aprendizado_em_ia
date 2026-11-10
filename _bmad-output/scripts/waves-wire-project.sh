#!/bin/sh
# waves-wire-project.sh <project-dir>
# Integra o Riaworks Waves num projeto BMAD (>= 6.12.4) para os DOIS agentes:
#   waves init (skills em .claude/skills, hooks, policy, agent, gitignore)
#   -> espelha waves-* em .agents/skills  -> wrappers .opencode/commands/waves-*.md
#   -> registra o módulo em _bmad/_config/bmad-help.csv  -> para de rastrear _bmad/render
set -eu
P=$(CDPATH= cd -- "${1:?uso: $0 <project-dir>}" && pwd)
cd "$P"
[ -d _bmad ] || { echo "sem _bmad/ em $P"; exit 2; }
waves init --project "$P" --cli claude --cli opencode --force-skills
# espelho para a árvore do OpenCode (paridade .agents/skills == .claude/skills)
if [ -d .agents/skills ]; then
  for s in .claude/skills/waves-*; do n=$(basename "$s"); rm -rf ".agents/skills/$n"; cp -r "$s" ".agents/skills/$n"; done
fi
# wrappers do OpenCode (mesmo formato dos bmad-*.md: frontmatter description + @skills/<name>)
if [ -d .opencode/commands ]; then
  for s in .claude/skills/waves-*; do n=$(basename "$s")
    desc=$(sed -n '2,/^---$/p' "$s/SKILL.md" | grep '^description:' | head -1)
    printf -- '---\n%s\n---\n\n@skills/%s\n' "$desc" "$n" > ".opencode/commands/$n.md"
  done
fi
# catálogo do /bmad-help (o instalador BMAD regenera este arquivo: re-rodar após cada update)
if [ ! -f _bmad/waves/module-help.csv ] && [ -f .claude/skills/waves-setup/assets/module-help.csv ]; then
  mkdir -p _bmad/waves && cp .claude/skills/waves-setup/assets/module-help.csv _bmad/waves/module-help.csv
fi
if [ -f _bmad/_config/bmad-help.csv ] && [ -f _bmad/waves/module-help.csv ]; then
  grep -q "Riaworks Waves" _bmad/_config/bmad-help.csv || tail -n +2 _bmad/waves/module-help.csv >> _bmad/_config/bmad-help.csv
fi
# _bmad/render é saída renderizada; nunca deve ser versionado
if git ls-files --error-unmatch _bmad/render >/dev/null 2>&1; then
  git rm -r -q --cached _bmad/render
  grep -qx '_bmad/render/' .gitignore 2>/dev/null || printf '\n# BMAD rendered skill output\n_bmad/render/\n' >> .gitignore
fi
echo "--- waves wired: $P"
