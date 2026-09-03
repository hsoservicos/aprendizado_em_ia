# bmad-agent-postgres18

PostgreSQL 18 Architect Agent — 5 SKILLs for complete PG18 development

## SKILLs

### 🔧 SKILL-01: DDL & Schema Architecture
- Design relational schemas with PG18 conventions
- Apply `uuidv7()` for high-volume transaction tables
- Use virtual generated columns for read-derived values
- Implement temporal WITHOUT OVERLAPS for schedules/audits

### ⚡ SKILL-02: Query Optimization & Analysis
- Format EXPLAIN (ANALYZE, BUFFERS, VERBOSE, WAL) output
- Identify B-tree Skip Scan opportunities
- Use RETURNING OLD/NEW for mutation operations
- Rewrite queries for PG18 execution engine

### 🧠 SKILL-03: Vector Search & Hybrid Persistence
- Create HNSW indices (m=16, ef_construction=64)
- Build hybrid search queries (relational + vector)
- Implement RRF via CTEs for weighted search
- Integrate pgvector with relational data

### 🔄 SKILL-04: Concurrency & Async Patterns
- Implement Transactional Outbox with RETURNING OLD/NEW
- Apply Optimistic/Pessimistic Locking patterns
- Tune AIO parameters per workload
- Design async patterns for microservices

### 🔒 SKILL-05: Security & Auditing
- Enforce SCRAM-SHA-256 and TLS 1.3
- Structure temporal audit tables with OLD/NEW deltas
- Configure per-table Autovacuum policies
- Implement least privilege access

## Usage

```bash
# Via BMAD render script
uv run _bmad/scripts/render_skill.py --project-root /home/hsantos/app --skill .agents/skills/bmad-agent-postgres18
```

## Menu

1. DDL & Schema — SKILL-01
2. Query Optimization — SKILL-02
3. Vector Search — SKILL-03
4. Concurrency — SKILL-04
5. Security — SKILL-05
6. Tuning — ALL
7. Migration — SKILL-01/05
8. Review — ALL
