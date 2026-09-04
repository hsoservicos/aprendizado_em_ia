# Java 21 LTS — Regras de Validação (J001–J015)

## Concorrência & Virtual Threads

| ID | Regra | Descrição |
|----|-------|-----------|
| J001 | NO_THREAD_POOL | NUNCA crie ThreadPoolExecutor para Virtual Threads. Use `Executors.newVirtualThreadPerTaskExecutor()` |
| J002 | NO_SYNCHRONIZED_IO | NUNCA execute I/O dentro de `synchronized`. Use `ReentrantLock` |
| J003 | VIRTUAL_THREAD_FACTORY | Use `Thread.ofVirtual().start()` ou `Executors.newVirtualThreadPerTaskExecutor()` |
| J004 | STRUCTURED_CONCURRENCY | Use `StructuredTaskScope` para sub-tarefas interdependentes |
| J005 | SCOPED_VALUE | Prefira `ScopedValue` a `ThreadLocal` para Virtual Threads |

## Pattern Matching & Records

| ID | Regra | Descrição |
|----|-------|-----------|
| J006 | USE_RECORDS | DTOs e Value Objects devem ser `record`, não classes |
| J007 | PATTERN_SWITCH | Use `switch` com Pattern Matching em vez de `instanceof` + casting |
| J008 | SEALED_EXHAUSTIVE | Use `sealed interface/class` para garantir exaustividade |
| J009 | RECORD_PATTERNS | Extraia campos aninhados diretamente em `instanceof` ou `switch` |
| J010 | GUARDED_CASES | Use `when` em vez de ifs internos no `switch` |

## Sequenced Collections

| ID | Regra | Descrição |
|----|-------|-----------|
| J011 | GET_FIRST_LAST | Use `getFirst()` / `getLast()` em vez de `get(0)` / `get(size-1)` |
| J012 | REVERSED_ITERATION | Use `collection.reversed()` em vez de loops manuais reversos |
| J013 | SEQUENCED_PARAM | Aceite `SequencedCollection` quando ordem importa |

## Architecture & Microservices

| ID | Regra | Descrição |
|----|-------|-----------|
| J014 | RECORD_RETURN | Use `record` para tipos de retorno de endpoints REST |
| J015 | NULL_VALIDATION | Valide nulos no construtor compacto do `record` |
