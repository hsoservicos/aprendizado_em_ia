# PHP 8.4 Agent & Skill Implementation

**Data**: 2026-09-03  
**Versão**: 1.0.0  
**Status**: Concluído

## Visão Geral

Implementação completa do PHP 8.4 Agent & Skill para o BMAD Method, seguindo o padrão estabelecido pelo Docker Agent & Skill.

## Arquivos Criados

### Skill: `bmad-php84`

| Arquivo | Descrição |
|---------|-----------|
| `.agents/skills/bmad-php84/SKILL.md` | Documentação principal da skill |
| `.agents/skills/bmad-php84/customize.toml` | Configuração e metadados |
| `.agents/skills/bmad-php84/workflow.md` | Fluxo de trabalho (4 fases) |
| `.agents/skills/bmad-php84/references/php84-rules.md` | 15 regras (PHP001-PHP015) |
| `.agents/skills/bmad-php84/references/php84-templates.md` | 8 templates de código |
| `.claude/skills/bmad-php84/` | Espelho completo em .claude/ |

### Agent: `bmad-agent-php84`

| Arquivo | Descrição |
|---------|-----------|
| `.agents/skills/bmad-agent-php84/SKILL.md` | Persona "PHP Architect 🔵" com 3 sub-roles |
| `.agents/skills/bmad-agent-php84/customize.toml` | Menu com 8 opções |
| `.claude/skills/bmad-agent-php84/` | Espelho completo em .claude/ |

### Comandos OpenCode

| Arquivo | Descrição |
|---------|-----------|
| `.opencode/commands/bmad-php84.md` | Comando da skill |
| `.opencode/commands/bmad-agent-php84.md` | Comando do agent |

## Sub-Roles do Agent

O PHP Architect Agent opera com 3 sub-roles:

1. **🏗️ Arch-PHP (Arquiteto)** — Arquitetura, design patterns, DDD, hexagonal, CQRS
2. **🔧 CodeRefactor-PHP (Refatorador)** — Modernização PHP 8.4, hooks, visibility
3. **🔒 WebSec-PHP (Segurista)** — Segurança, OWASP, validação, sanitização

## Features PHP 8.4 Cobertas

1. **Property Hooks** (get/set) — Substitui getter/setter boilerplate
2. **Asymmetric Visibility** — `public private(set)` para controle de mutação
3. **New Expression Syntax** — `new MyClass()->method()` sem parênteses
4. **DOM API (HTML5)** — `Dom\HTMLDocument` com suporte nativo
5. **Array Functions** — `array_find`, `array_find_key`, `array_any`, `array_all`
6. **#[\Deprecated] Attribute** — Marcadores explícitos de deprecação
7. **BCMath Object API** — `BCMath\Number` para aritmética de precisão
8. **Lazy Objects** — `newLazyGhost()` para instanciação adiada
9. **mb_trim/mb_ltrim/mb_rtrim** — Trimming multibyte

## Regras Implementadas

| ID | Regra | Descrição |
|----|-------|-----------|
| PHP001 | Strict Types | Declaração obrigatória `declare(strict_types=1)` |
| PHP002 | Property Hooks | Uso de hooks get/set |
| PHP003 | Asymmetric Visibility | Padrão `public private(set)` |
| PHP004 | New Expression Syntax | `new Foo()->bar()` sem parênteses |
| PHP005 | DOM API HTML5 | `Dom\HTMLDocument` para parsing |
| PHP006 | Array Functions | `array_find`, `array_any`, `array_all` |
| PHP007 | #[\Deprecated] | Atributo de deprecação |
| PHP008 | BCMath Object | `BCMath\Number` para precisão |
| PHP009 | Lazy Objects | `newLazyGhost()` para deferred init |
| PHP010 | mb_trim | Trimming multibyte UTF-8 |
| PHP011 | Typing Standards | Union types, intersection, readonly |
| PHP012 | PSR Standards | PSR-12, PSR-4, PSR-3 |
| PHP013 | Error Handling | Exceptions sobre error codes |
| PHP014 | Security | Validação, sanitização, prepared statements |
| PHP015 | Performance | OPcache, readonly, match |

## Templates Incluídos

1. **DTO com Property Hooks & Asymmetric Visibility**
2. **DOM HTML5 Parser**
3. **Array Functions Usage**
4. **BCMath Object API (Money)**
5. **Lazy Object para Database Entity**
6. **#[\Deprecated] Pattern**
7. **Match Expression com Enums**
8. **New Expression Syntax**

## Manifest

Entradas adicionadas ao `_bmad/_config/skill-manifest.csv`:
- `bmad-php84` — Skill de PHP 8.4
- `bmad-agent-php84` — Agent multi-role

## Contagem Total

- **Skills**: 55 (53 originais + 2 novas)
- **Agents**: 6 (5 originais + 1 novo)
