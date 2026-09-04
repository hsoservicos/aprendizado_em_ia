# Workflow: Angular 21 LTS Master Coding Agent

## Fase 1: Análise do Código
1. Escanear o código fornecido em busca de padrões legados.
2. Identificar oportunidades de modernização com recursos Angular 21.
3. Classificar achados por severidade e impacto.

## Fase 2: Refatoração por SKILL
Aplicar as SKILLs na ordem de maior impacto:

### SKILL 01 — Zoneless State & Signals
- Substituir `BehaviorSubject` por `signal()` e `computed()`
- Configurar `provideExperimentalZonelessChangeDetection()`
- Remover dependências de `zone.js`

### SKILL 02 — Signal Forms
- Substituir `FormGroup`/`FormControl` por `form()` de `@angular/forms/signals`
- Usar `[field]` directive em vez de `formControlName`
- Aplicar validação schema-based

### SKILL 03 — Modern Router
- Refatorar para function-based guards e resolvers
- Usar `input()` para parâmetros de rota
- Remover `NgModule` do routing

### SKILL 04 — Control Flow & @let
- Substituir `*ngIf` por `@if`
- Substituir `*ngFor` por `@for` com `track`
- Substituir `*ngSwitch` por `@switch`
- Adicionar `@let` para variáveis no template

### SKILL 05 — Angular ARIA
- Integrar `@angular/aria` para componentes acessíveis
- Aplicar patterns: Accordion, Menu, Tabs, Tree
- Garantir keyboard navigation

### SKILL 06 — Vitest Testing
- Configurar `@angular/build:unit-test` em `angular.json`
- Migrar specs para Vitest
- Substituir `spyOn` por `vi.spyOn`
- Substituir `fakeAsync`/`tick` por `vi.useFakeTimers()`

## Fase 3: Validação
1. Executar o Quality Gate (seção 5 do SKILL.md).
2. Reportar mudanças realizadas e pendências.
3. Sugerir testes unitários para código refatorado.
