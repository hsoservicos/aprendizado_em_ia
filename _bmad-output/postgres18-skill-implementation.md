# PostgreSQL 18 Agent & Skill Implementation

**Data**: 2026-09-03  
**Versão**: 1.0.0  
**Status**: Concluído

## Visão Geral

Implementação completa do PostgreSQL 18 Agent & Skill para o BMAD Method, seguindo o padrão estabelecido pelo Docker Agent & Skill.

## Arquivos Criados

### Skill: `bmad-postgres18`

| Arquivo | Descrição |
|---------|-----------|
| `.agents/skills/bmad-postgres18/SKILL.md` | Documentação principal da skill |
| `.agents/skills/bmad-postgres18/customize.toml` | Configuração e metadados |
| `.agents/skills/bmad-postgres18/workflow.md` | Fluxo de trabalho (4 fases) |
| `.agents/skills/bmad-postgres18/references/postgres18-rules.md` | 15 regras (PG001-PG015) |
| `.agents/skills/bmad-postgres18/references/postgres18-templates.md` | 8 templates de código |
| `.claude/skills/bmad-postgres18/` | Espelho completo em .claude/ |

### Agent: `bmad-agent-postgres18`

| Arquivo | Descrição |
|---------|-----------|
| `.agents/skills/bmad-agent-postgres18/SKILL.md` | Persona "PostgreSQL 18 Architect 🐘" com 5 SKILLs |
| `.agents/skills/bmad-agent-postgres18/customize.toml` | Menu com 8 opções |
| `.claude/skills/bmad-agent-postgres18/` | Espelho completo em .claude/ |

### Comandos OpenCode

| Arquivo | Descrição |
|---------|-----------|
| `.opencode/commands/bmad-postgres18.md` | Comando da skill |
| `.opencode/commands/bmad-agent-postgres18.md` | Comando do agent |

## 5 SKILLs do Agent

| SKILL | Nome | Descrição |
|-------|------|-----------|
| SKILL-01 | DDL | Modern DDL & Schema Architecture Design |
| SKILL-02 | OPT | Query Optimization & PG18 Execution Analysis |
| SKILL-03 | VEC | Vector Search & Hybrid Persistence (`pgvector`) |
| SKILL-04 | CONC | Concurrency, Microsservices & Async Patterns |
| SKILL-05 | SEC | Security, Auditing & Maintenance Hardening |

## Features PostgreSQL 18 Cobertas

1. **Asynchronous I/O (AIO)** — `io_method = io_uring` para 3x performance
2. **B-Tree Skip Scan** — Otimização de índices multicolunas
3. **UUIDv7** — `uuidv7()` para chaves primárias ordenadas
4. **Virtual Generated Columns** — Padrão PG18
5. **RETURNING OLD/NEW** — Extração direta de deltas
6. **NOT NULL NOT VALID** — Constraints não-bloqueantes
7. **WITHOUT OVERLAPS** — Chaves temporais
8. **pgvector** — HNSW, busca híbrida, RRF

## Regras Implementadas

| ID | Regra | Descrição |
|----|-------|-----------|
| PG001 | UUIDv7 | PKs com `uuidv7()` para alto volume |
| PG002 | Virtual Generated | Colunas derivadas VIRTUAL (padrão PG18) |
| PG003 | NOT VALID | Constraints não-bloqueantes |
| PG004 | WITHOUT OVERLAPS | Chaves temporais |
| PG005 | Skip Scan | Índices multicolunas sem prefixo |
| PG006 | RETURNING OLD/NEW | Deltas diretos em mutations |
| PG007 | AIO | `io_method = io_uring` |
| PG008 | pgvector | HNSW, busca híbrida |
| PG009 | Outbox | Transactional Outbox com RETURNING |
| PG010 | Optimistic Locking | Controle de concorrência otimista |
| PG011 | SKIP LOCKED | Filas de alta concorrência |
| PG012 | SCRAM-SHA-256 | Autenticação segura |
| PG013 | TLS 1.3 | Criptografia em trânsito |
| PG014 | Autovacuum | Políticas por tabela |
| PG015 | pg_upgrade | Migração com preservação de estatísticas |

## Templates Incluídos

1. UUIDv7 Primary Key with Generated Columns
2. Transactional Outbox with RETURNING OLD/NEW
3. Queue Processor with SKIP LOCKED
4. Temporal Table with WITHOUT OVERLAPS
5. Hybrid Vector Search (pgvector + Relational)
6. Audit Table with OLD/NEW Deltas
7. Non-Blocking Migration Pattern
8. pg_upgrade with Statistics Preservation

## Manifest

Entradas adicionadas ao `_bmad/_config/skill-manifest.csv`:
- `bmad-postgres18` — Skill de PostgreSQL 18
- `bmad-agent-postgres18` — Agent com 5 SKILLs

## Contagem Total

- **Skills**: 57 (55 anteriores + 2 novas)
- **Agents**: 7 (6 anteriores + 1 novo)
