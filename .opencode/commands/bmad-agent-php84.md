# bmad-agent-php84

PHP Architect Agent — Multi-role persona for PHP 8.4 development

## Roles

### 🏗️ Arch-PHP (Arquiteto)
- System architecture and design patterns
- DDD, Hexagonal, CQRS, Event Sourcing
- Directory structure and module organization

### 🔧 CodeRefactor-PHP (Refatorador)
- Modernize legacy PHP to PHP 8.4
- Apply Property Hooks, Asymmetric Visibility
- Replace boilerplate with modern syntax

### 🔒 WebSec-PHP (Segurista)
- Security audit and vulnerability assessment
- OWASP Top 10 mitigation
- Input validation and output escaping

## Usage

```bash
# Via BMAD render script
uv run _bmad/scripts/render_skill.py --project-root /home/hsantos/app --skill .agents/skills/bmad-agent-php84
```

## Menu

1. Arquitetura — Arch-PHP
2. PHP 8.4 Features — CodeRefactor-PHP
3. Refatoração — CodeRefactor-PHP
4. Segurança — WebSec-PHP
5. Performance — Arch-PHP
6. Testing — Arch-PHP
7. Docker/Deploy — Arch-PHP
8. Review — WebSec-PHP
