# Workflow: Java 21 LTS Master Coding Agent

## Fase 1: Análise do Código
1. Escanear o código fornecido em busca de padrões legados.
2. Identificar oportunidades de modernização com recursos Java 21.
3. Classificar achados por severidade e impacto.

## Fase 2: Refatoração por SKILL
Aplicar as SKILLs na ordem de maior impacto:

### SKILL 01 — Virtual Threads & Loom
- Substituir Thread Pools por `Executors.newVirtualThreadPerTaskExecutor()`
- Refatorar `synchronized` + I/O para `ReentrantLock`
- Adicionar `ScopedValue` onde `ThreadLocal` é usado

### SKILL 02 — Pattern Matching & Records
- Converter classes de dados para `record`
- Refatorar `switch` / `instanceof` para Pattern Matching
- Aplicar `sealed interface/class` para exaustividade

### SKILL 03 — Sequenced Collections
- Substituir `list.get(0)` / `list.get(size-1)` por `getFirst()` / `getLast()`
- Usar `collection.reversed()` em vez de loops manuais
- Aceitar `SequencedCollection` como tipo de parâmetro

### SKILL 04 — Architecture & Microservices
- Aplicar `StructuredTaskScope` para concorrência resiliente
- Usar `record` para tipos de retorno de API
- Validar invariantes nos construtores de records

### SKILL 05 — Code Quality Gate
- Executar checklist de validação
- Verificar ausência de pools de Virtual Threads
- Garantir uso completo de Pattern Matching

## Fase 3: Validação
1. Executar o Quality Gate (seção 5 do SKILL.md).
2. Reportar mudanças realizadas e pendências.
3. Sugerir testes unitários para código refatorado.
