# bmad-postgres18

PostgreSQL 18 Architect — AIO, Skip Scan, UUIDv7, pgvector, RETURNING OLD/NEW

## SKILLs

| SKILL | Name | Description |
|-------|------|-------------|
| SKILL-01 | DDL | Modern DDL & Schema Architecture Design |
| SKILL-02 | OPT | Query Optimization & PG18 Execution Analysis |
| SKILL-03 | VEC | Vector Search & Hybrid Persistence (`pgvector`) |
| SKILL-04 | CONC | Concurrency, Microsservices & Async Patterns |
| SKILL-05 | SEC | Security, Auditing & Maintenance Hardening |

## Usage

```bash
# Via BMAD render script
uv run _bmad/scripts/render_skill.py --project-root /home/hsantos/app --skill .agents/skills/bmad-postgres18
```

## Features PG18

- `uuidv7()` — UUIDs ordenados por timestamp
- B-Tree Skip Scan — Índices multicolunas sem prefixo
- Virtual Generated Columns — Padrão PG18
- RETURNING OLD/NEW — Deltas diretos em mutations
- WITHOUT OVERLAPS — Chaves temporais
- pgvector — HNSW, IVFFlat, busca híbrida
- AIO — `io_method = io_uring` para 3x performance

## Examples

```sql
-- UUIDv7 com coluna gerada
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    total DECIMAL(12,2) GENERATED ALWAYS AS (subtotal * (1 + tax_rate)) VIRTUAL
);

-- Busca híbrida com RRF
WITH vector_results AS (...),
     text_results AS (...)
SELECT * FROM vector_results v
FULL OUTER JOIN text_results t ON v.id = t.id
ORDER BY (1.0/(1+v.vector_rank)) + (1.0/(1+t.text_rank)) DESC;
```
