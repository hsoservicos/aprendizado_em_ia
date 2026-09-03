# Python 3.14 Agent & Skill — Documentação da Implementação

**Data:** 2026-09-03
**Status:** Implementado e Validado
**Versão:** 1.0.0

---

## Auditoria da Especificação vs Realidade

### PEPs Confirmados para Python 3.14 (Lançado 07/10/2025)

| PEP | Feature | Status Real | Correção na Especificação |
|-----|---------|-------------|---------------------------|
| PEP 779 | Free-Threading (Fase II) | **Final** | PEP 779 define critérios; PEP 703 é a base |
| PEP 734 | Subinterpreters na Stdlib | **Final** | ✅ Confirmado — `concurrent.interpreters` |
| PEP 750 | Template Strings (t-strings) | **Final** | ✅ Confirmado — `t"..."` syntax |
| PEP 649/749 | Deferred Annotations | **Final** | ✅ Confirmado — `annotationlib` module |
| PEP 784 | compression.zstd | **Final** | ✅ Confirmado — módulo nativo |
| PEP 758 | except sem parênteses | **Final** | ⚠️ Só sem `as` clause |
| PEP 768 | Safe Debugger Interface | **Final** | Não mencionado na spec original |

### Correções na Especificação Original

| Item na Especificação | Status Real | Observação |
|----------------------|-------------|------------|
| `pathlib.Path.copy()` / `.move()` | ❌ Não confirmado para 3.14 | Não é feature do 3.14 |
| `uuid.uuid7()` | ✅ Confirmado | RFC 9562, suportado nativamente |
| `date.strptime()` | ⚠️ Não confirmado como novo | Funcionalidade existente |
| `except ValueError, TypeError:` | ✅ Confirmado | PEP 758 — só sem `as` |
| `from __future__ import annotations` removido | ✅ Confirmado | PEP 649 torna obsoleto |

---

## Arquivos Criados

### Python 3.14 Skill

| Caminho | Descrição |
|---------|-----------|
| `.agents/skills/bmad-python314/SKILL.md` | Ponto de entrada da skill |
| `.agents/skills/bmad-python314/customize.toml` | Configuração de customização |
| `.agents/skills/bmad-python314/workflow.md` | Workflow principal (6 fases) |
| `.agents/skills/bmad-python314/references/python314-rules.md` | 10 regras de validação |
| `.agents/skills/bmad-python314/references/python314-templates.md` | 9 templates de código |

### Python 3.14 Agent

| Caminho | Descrição |
|---------|-----------|
| `.agents/skills/bmad-agent-python314/SKILL.md` | Ativação do agente com persona |
| `.agents/skills/bmad-agent-python314/customize.toml` | Persona, menu (7 itens), principles |

### Comandos OpenCode

| Caminho | Descrição |
|---------|-----------|
| `.opencode/commands/bmad-python314.md` | Comando para Python 3.14 Skill |
| `.opencode/commands/bmad-agent-python314.md` | Comando para Python 3.14 Agent |

---

## Regras de Validação (10 regras)

| ID | Severidade | Regra |
|----|------------|-------|
| PY001 | INFO | Remover `from __future__ import annotations` |
| PY002 | WARNING | Usar t-strings para prevenção de injection |
| PY003 | WARNING | Usar InterpreterPoolExecutor para CPU-bound |
| PY004 | INFO | Usar compression.zstd ao invés de zlib |
| PY005 | INFO | Usar uuid.uuid7() para IDs de banco |
| PY006 | INFO | Usar sintaxe moderna de except (sem parênteses) |
| PY007 | INFO | Forward references sem quotes em 3.14+ |
| PY008 | INFO | Usar annotationlib para introspecção |
| PY009 | INFO | Usar sys.remote_exec() para debug |
| PY010 | WARNING | Build free-threaded: python3.14t |

---

## Templates Disponíveis (9)

| Template | Uso | PEPs |
|----------|-----|------|
| A | Free-Threading CPU-Bound | PEP 779 |
| B | Subinterpreter Isolated Processing | PEP 734 |
| C | T-String SQL Handler | PEP 750 |
| D | T-String HTML Escaper | PEP 750 |
| E | Zstandard Compression | PEP 784 |
| F | Modern Exception Handling | PEP 758 |
| G | Annotation Introspection | PEP 649/749 |
| H | UUID v7 for Database IDs | RFC 9562 |
| I | Asyncio + Subinterpreters | PEP 734 |

---

## Menu do Python Architect Agent

| Code | Descrição | Ação |
|------|-----------|------|
| `FT` | Free-threading: otimizar para CPU-bound | bmad-python314 |
| `SI` | Subinterpreters: InterpreterPoolExecutor | bmad-python314 |
| `TS` | T-strings: DSLs seguras (SQL, HTML) | bmad-python314 |
| `MG` | Migrar código para padrões Python 3.14 | bmad-python314 |
| `CP` | Compression: compression.zstd | bmad-python314 |
| `VL` | Validar código para práticas 3.14 | bmad-python314 |
| `OP` | Otimizar performance Python | bmad-python314 |

---

## Matriz de Migração

| Prática Antiga (até 3.13) | Nova Abordagem (3.14+) | Vantagem |
|---------------------------|------------------------|----------|
| `from __future__ import annotations` | Remover (PEP 649) | Menos boilerplate |
| f-strings para SQL/HTML | t-strings (PEP 750) | Prevenção de injection |
| `multiprocessing.Pool` | `InterpreterPoolExecutor` (PEP 734) | Menor overhead |
| `zlib.compress()` | `compression.zstd.compress()` (PEP 784) | Melhor ratio |
| `uuid.uuid4()` | `uuid.uuid7()` (RFC 9562) | IDs ordenados |
| `except (A, B):` | `except A, B:` (PEP 758) | Sintaxe mais limpa |
| `"ForwardRef"` | Forward refs diretas (PEP 649) | Sem quotes |
| `func.__annotations__` | `annotationlib.get_annotations()` (PEP 749) | API correta |

---

## Uso

### Via OpenCode

```bash
# Skill técnica
bmad-python314

# Agent com persona
bmad-agent-python314
```

### Via Renderização

```bash
uv run _bmad/scripts/render_skill.py --project-root /home/hsantos/app --skill .claude/skills/bmad-python314
```

---

## Estatísticas

| Métrica | Valor |
|---------|-------|
| Total de arquivos criados | 12 |
| Skills novas | 2 (bmad-python314, bmad-agent-python314) |
| Regras de validação | 10 |
| Templates de código | 9 |
| PEPs cobertos | 8 (779, 734, 750, 649/749, 784, 758, 768, RFC 9562) |
