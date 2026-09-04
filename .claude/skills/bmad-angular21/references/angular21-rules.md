# Angular 21 — Regras de Validação (A001–A015)

## Zoneless & Change Detection

| ID | Regra | Descrição |
|----|-------|-----------|
| A001 | ZONELESS_BOOTSTRAP | Use `provideExperimentalZonelessChangeDetection()` no bootstrap |
| A002 | NO_ZONE_JS | NUNCA importe ou use `zone.js` em novas aplicações |
| A003 | NO_NG_ZONE | NUNCA injete `NgZone` — use signals para estado reativo |
| A004 | NO_MARK_FOR_CHECK | NUNCA use `markForCheck()` — signals propagam mudanças automaticamente |
| A005 | ON_PUSH | Use `ChangeDetectionStrategy.OnPush` em todos os componentes |

## Signals & State Management

| ID | Regra | Descrição |
|----|-------|-----------|
| A006 | USE_SIGNAL | Use `signal()` para estado local reativo |
| A007 | USE_COMPUTED | Use `computed()` para estado derivado |
| A008 | USE_LINKED_SIGNAL | Use `linkedSignal()` para estado dependente que reseta |
| A009 | USE_RESOURCE | Use `resource()` para dados assíncronos |
| A010 | NO_BEHAVIOR_SUBJECT | NUNCA use `BehaviorSubject` para estado local — use `signal()` |

## Components & Templates

| ID | Regra | Descrição |
|----|-------|-----------|
| A011 | STANDALONE | Todos os componentes devem ter `standalone: true` |
| A012 | SIGNAL_INPUT_OUTPUT | Use `input()`, `input.required()`, `output()` em vez de decorators |
| A013 | CONTROL_FLOW | Use `@if`, `@for`, `@switch` em vez de `*ngIf`, `*ngFor`, `*ngSwitch` |
| A014 | FOR_TRACK | `@for` SEMPRE deve incluir `track` |
| A015 | NO_NG_MODULES | NUNCA crie `NgModules` — use standalone components |

## Forms

| ID | Regra | Descrição |
|----|-------|-----------|
| A016 | SIGNAL_FORMS | Use `form()` de `@angular/forms/signals` para novos formulários |
| A017 | FIELD_DIRECTIVE | Use `[field]` directive em vez de `formControlName` |
| A018 | SCHEMA_VALIDATION | Use validação schema-based com `required()`, `email()`, etc. |

## Testing

| ID | Regra | Descrição |
|----|-------|-----------|
| A019 | VITEST | Use Vitest como test runner — configure `@angular/build:unit-test` |
| A020 | NO_KARMA | NUNCA use Karma/Jasmine para novos testes |
| A021 | VI_SPY_ON | Use `vi.spyOn` em vez de `spyOn` |
| A022 | VI_FAKE_TIMERS | Use `vi.useFakeTimers()` em vez de `fakeAsync`/`tick` |

## Accessibility

| ID | Regra | Descrição |
|----|-------|-----------|
| A023 | ANGULAR_ARIA | Use `@angular/aria` para componentes acessíveis |
| A024 | KEYBOARD_NAV | Garanta navegação por teclado em todos os componentes interativos |
| A025 | ARIA_ATTRS | Use atributos ARIA corretos (roles, labels, states) |
