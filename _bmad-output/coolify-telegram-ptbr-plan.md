# Notificações do Coolify no Telegram em PT-BR — Plano de Implementação

> **Para agentes executores:** sub-skill obrigatória: `superpowers:executing-plans` (execução inline) ou `superpowers:subagent-driven-development`. Passos com checkbox (`- [ ]`) para rastreio.

**Objetivo:** entregar todas as notificações de operação do Coolify no Telegram com textos em Português do Brasil, mais um bot de consulta e ações, sem fork do Coolify e sem sudo.

**Arquitetura:** o Coolify envia webhooks JSON (15 eventos nativos) para um serviço Python/FastAPI (`coolify-tg-relay`) rodando em container na rede Docker `coolify`. O relay renderiza templates PT-BR, enfileira em SQLite, envia pela Bot API do Telegram com HTML e botões, e enriquece eventos de deploy com commit e duração via API REST do Coolify. O mesmo processo roda um bot em long polling (sem porta pública) para consultas e ações com confirmação.

**Stack:** Python 3.12, FastAPI, uvicorn, httpx, PyYAML, SQLite (stdlib), pytest. Docker para empacotamento.

**Spec:** este documento (decisões aprovadas em 2026-11-09) complementado por:
- `https://coolify.io/docs/core/notifications/events`
- `https://coolify.io/docs/core/notifications/channels/webhook/payload-reference`
- Código do Coolify `v4.6.0`: `app/Notifications/**`, `app/Jobs/SendWebhookJob.php`, `app/Rules/SafeWebhookUrl.php`

---

## 1. Diagnóstico que fundamenta o plano

| Fato (verificado em 2026-11-09) | Consequência |
|---|---|
| Coolify `4.6.0` em Docker; Telegram nativo ativo com 15 eventos | Já existe entrega; falta PT-BR e operações extras |
| Textos de notificação são strings fixas em inglês em 29 classes `toTelegram()` | Não há i18n; configuração de UI não resolve |
| `lang/pt-br.json` tem 46 chaves, nenhuma de notificação | Traduzir só a UI não altera mensagens |
| Canal nativo envia texto puro (sem `parse_mode`) | Sem negrito/link embutido; relay entrega mais |
| Canal Webhook existe na 4.6.0 com 15 eventos e JSON documentado | Base estável para o relay |
| Webhook não assina requisição; `SafeWebhookUrl` bloqueia IP privado sem allowlist | Exige segredo longo + rede interna + allowlist |
| 3 falhas 401/403/404/410 desligam o canal; timeout/5xx não | Relay deve responder 2xx para eventos válidos/desconhecidos |
| `activity_log` não audita ações de usuário | Bot cobre ações que ele mesmo executa; API cobre deploys |
| Container `coolify` alcança host `10.0.1.1:8000` e a si em `coolify:8080` | Relay usa `http://coolify:8080` para API |
| Container `coolify` não alcança o n8n (`10.0.3.2` e URL pública: 000) | n8n descartado como relay |
| `/data/coolify` é `0700 root`; sem sudo sem senha | Fork/imagem própria exigiria senha; relay não exige |

## 2. Decisões aprovadas

1. **Estratégia:** relay webhook → Telegram (sem fork).
2. **Escopo:** notificações PT-BR + bot de comandos.
3. **Exposição:** rede interna Docker (`coolify`), sem FQDN público, bot em long polling.
4. **Glossário:** "Deploy" (não "Implantação"); datas em `America/Sao_Paulo`; números e percentuais pt-BR.
5. **Corte:** desligar o canal Telegram nativo após a matriz E2E ficar verde.

## 3. Restrições globais

- Segredos **nunca** entram no git. `.env` fica no `.gitignore`; apenas `.env.example` é versionado.
- Nenhuma alteração dentro do container `coolify` ou em `/data/coolify`.
- Nenhum comando com `sudo`.
- O relay **não** pode derrubar o canal webhook: responde `200` para evento desconhecido, JSON inválido e segredo válido; `401` apenas para segredo inválido.
- Toda mensagem ao usuário é em PT-BR; datas BRT; limite Telegram de 4096 caracteres.
- Mensagens não podem vazar tokens, segredos ou conteúdo sensível de `output`/`logs`.
- Ações destrutivas exigem confirmação inline com validade de 60 s e usuário autorizado.
- Nomes de comandos e campos de API devem seguir exatamente os contratos deste plano.

## 4. Estrutura de arquivos

```
coolify-tg-relay/
├── pyproject.toml                 # deps + pytest + ruff
├── Dockerfile                     # python:3.12-slim, usuário non-root
├── compose.yml                    # network coolify, restart unless-stopped
├── .env.example                   # todas as variáveis, sem valores reais
├── .gitignore                     # .env, data/, __pycache__
├── README.md                      # instalação, operação, runbook
├── app/
│   ├── __init__.py
│   ├── config.py                  # Settings + load_settings()
│   ├── store.py                   # SQLite: outbox, dedupe, audit, meta
│   ├── format.py                  # escape, BRT, truncamento, render
│   ├── templates.py               # carrega templates.yml; EVENT_IDS
│   ├── templates.yml              # 19 mensagens PT-BR
│   ├── telegram.py                # cliente Bot API
│   ├── coolify.py                 # cliente API REST
│   ├── worker.py                  # dispatcher da outbox + digest
│   ├── bot.py                     # long polling, comandos, confirmação
│   └── main.py                    # FastAPI: /hook/{secret}, /healthz
└── tests/
    ├── fixtures/payloads/<event>.json   # 19 payloads de exemplo
    ├── golden/<event>.txt               # saída esperada por evento
    ├── test_health.py
    ├── test_store.py
    ├── test_format.py
    ├── test_templates.py
    ├── test_telegram.py
    ├── test_coolify.py
    ├── test_hook.py
    ├── test_worker.py
    ├── test_bot_auth.py
    └── test_bot_confirm.py
```

## 5. Contratos

### 5.1 Configuração (`app/config.py`)

```python
class Settings(BaseModel):
    telegram_bot_token: str
    telegram_chat_id: str
    telegram_threads: dict[str, int]      # event -> message_thread_id
    allowed_user_ids: set[int]
    allowed_chat_ids: set[int]
    hook_secret: str                       # >= 32 chars
    coolify_base_url: str                  # http://coolify:8080
    coolify_api_token: str
    database_path: str = "/data/relay.db"
    timezone: str = "America/Sao_Paulo"
    quiet_hours: tuple[int, int] | None = None   # (inicio, fim) em horas
    log_level: str = "INFO"

def load_settings() -> Settings: ...       # lê ambiente; falha rápida se faltar campo
```

Variáveis: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `TELEGRAM_THREADS` (JSON),
`TELEGRAM_ALLOWED_USER_IDS` (CSV), `TELEGRAM_ALLOWED_CHAT_IDS` (CSV), `HOOK_SECRET`,
`COOLIFY_BASE_URL`, `COOLIFY_API_TOKEN`, `DATABASE_PATH`, `TZ`, `QUIET_HOURS`, `LOG_LEVEL`.

### 5.2 Store (`app/store.py`)

Tabelas:
- `outbox(id INTEGER PK, dedupe_key TEXT UNIQUE, payload TEXT, status TEXT, attempts INT, next_at TEXT, last_error TEXT, created_at TEXT)`
- `audit(id INTEGER PK, ts TEXT, user_id INT, chat_id INT, action TEXT, target TEXT, result TEXT)`
- `meta(key TEXT PK, value TEXT)`

API:
```python
class Store:
    def __init__(self, path: str) -> None: ...
    def enqueue(self, dedupe_key: str, payload: dict) -> int | None: ...   # None = duplicado
    def claim_due(self, now: datetime) -> list[OutboxItem]: ...
    def mark_sent(self, item_id: int) -> None: ...
    def mark_failed(self, item_id: int, error: str, retry_at: datetime) -> None: ...
    def audit(self, user_id: int, chat_id: int, action: str, target: str, result: str) -> None: ...
    def meta_set(self, key: str, value: str) -> None: ...
    def meta_get(self, key: str) -> str | None: ...
    def stats_since(self, since: datetime) -> dict[str, int]: ...
```

Chave de dedupe: `"{event}:{id}:{bucket}"`, onde `id` é o primeiro de
`deployment_uuid`, `task_uuid`, `database_uuid`, `server_uuid`, `container_name`;
`bucket` = minuto UTC para eventos recorrentes (`high_disk_usage`, `server_unreachable`,
`server_reachable`, `docker_cleanup_*`, `traefik_version_outdated`) e vazio para
`deployment_*`, `backup_*`, `task_*`, `status_changed`, `container_*`.

### 5.3 Templates (`app/templates.yml` + `app/templates.py`)

```python
@dataclass(frozen=True)
class Button: text: str; url: str
@dataclass(frozen=True)
class EventTemplate: title: str; body: list[str]; buttons: list[Button]
@dataclass(frozen=True)
class TemplatesConfig: events: dict[str, EventTemplate]

def load_templates(path: str) -> TemplatesConfig: ...
EVENT_IDS: tuple[str, ...]   # os 19 abaixo, nesta ordem
```

Formato YAML:
```yaml
version: 1
events:
  deployment_success:
    title: "✅ <b>Deploy concluído</b>"
    body:
      - "<b>Aplicação:</b> {application_name}"
      - "<b>Projeto:</b> {project} · <b>Ambiente:</b> {environment}"
      - "<b>Commit:</b> <code>{commit_short}</code> {commit_message}"
      - "<b>Duração:</b> {duration}"
      - "<b>Quando:</b> {finished_at_brt}"
    buttons:
      - {text: "Abrir aplicação", url: "{fqdn}"}
      - {text: "Ver logs do deploy", url: "{deployment_url}"}
```

Regra de renderização: uma linha do `body` é **omitida** se qualquer `{placeholder}`
nela resolver para vazio/None. Botão é omitido se a URL não começar com `http`.

### 5.4 Render (`app/format.py`)

```python
def escape_html(text: str) -> str
def format_brt(value: str | datetime | None) -> str          # "08/11/2026 00:53"
def short_commit(commit: str | None) -> str                  # 8 chars
def human_duration(start: str | None, end: str | None) -> str # "2 min 44 s"
def render(payload: dict, cfg: TemplatesConfig, extra: dict | None = None) -> Rendered
# Rendered: text: str; buttons: list[Button]; thread_id: int | None
```

Truncamento: se `len(text) > 4096`, corta no último `\n` antes de 4000 e acrescenta
`\n…(mensagem truncada)`.

### 5.5 Telegram (`app/telegram.py`)

```python
class TelegramClient:
    def __init__(self, token: str, http: httpx.AsyncClient) -> None: ...
    async def send_message(self, text: str, buttons: list[Button],
                           thread_id: int | None = None) -> None: ...
    async def get_updates(self, offset: int, timeout: int = 30) -> list[dict]: ...
    async def answer_callback(self, callback_id: str, text: str) -> None: ...
```

Regras: `parse_mode=HTML`, `disable_web_page_preview=true`; 429 → aguarda
`retry_after` (máx. 60 s) e repete; 400 com erro de botão → reenvia texto com links
anexados; 5xx → exceção para retry do dispatcher.

### 5.6 Coolify (`app/coolify.py`)

```python
class CoolifyClient:
    async def list_applications(self) -> list[dict]
    async def get_application(self, uuid: str) -> dict
    async def list_servers(self) -> list[dict]
    async def get_deployment(self, uuid: str) -> dict
    async def deploy(self, uuid: str) -> dict
    async def start(self, uuid: str) -> dict
    async def restart(self, uuid: str) -> dict
    async def stop(self, uuid: str) -> dict
```

Base: `COOLIFY_BASE_URL`. Header: `Authorization: Bearer <token>`.

### 5.7 Hook (`app/main.py`)

- `POST /hook/{secret}`: compara com `hmac.compare_digest`; `401` se inválido;
  enfileira e responde `200 {"ok": true}`; JSON inválido → `200 {"ok": true, "ignored": true}`.
- `GET /healthz`: `200 {"ok": true, "queue": n, "last_event": "..."}`.

### 5.8 Bot (`app/bot.py`)

Comandos e ações (todos em PT-BR):

| Comando | Efeito |
|---|---|
| `/ajuda` | cartão de ajuda |
| `/status` | apps, servidores e deploys em andamento |
| `/apps` | lista de aplicações com status |
| `/app <nome\|uuid>` | ficha da aplicação |
| `/deploys [app]` | últimos deploys |
| `/logs <uuid>` | status + link do deploy |
| `/deploy <app>` | confirma → `POST /deploy` |
| `/iniciar <app>` | confirma → `POST /applications/{uuid}/start` |
| `/reiniciar <app>` | confirma → `POST /applications/{uuid}/restart` |
| `/parar <app>` | confirma → `POST /applications/{uuid}/stop` |
| `/silenciar <30m\|2h\|off>` | pausa/retoma notificações não críticas |

Autorização: `user_id` **e** `chat_id` na allowlist; allowlist vazia = nega tudo.
Confirmação: callback `c:<acao>:<uuid>`, validade 60 s, uso único.
Rate limit: 1 ação por (usuário, app) a cada 30 s. Auditoria em `audit`.

## 6. Matriz de eventos e mensagens PT-BR

| `event` | Título | Campos obrigatórios |
|---|---|---|
| `deployment_success` | ✅ Deploy concluído | app, projeto, ambiente, commit, duração, quando |
| `deployment_failed` | ❌ Falha no deploy | app, projeto, ambiente, commit, erro |
| `status_changed` / `container_stopped` | ⛔ Recurso parou inesperadamente | recurso, projeto, ambiente |
| `container_restarted` | 🔄 Recurso reiniciado automaticamente | container, servidor |
| `restart_limit_reached` | 🚫 Limite de reinícios atingido | app, contagem, projeto, ambiente |
| `backup_success` | 💾 Backup concluído | banco, frequência |
| `backup_failed` | 🚨 Falha no backup | banco, frequência, erro |
| `backup_success_with_s3_warning` | ⚠️ Backup local OK — envio S3 falhou | banco, erro S3 |
| `task_success` | ✅ Tarefa agendada concluída | tarefa, saída curta |
| `task_failed` | ❌ Tarefa agendada falhou | tarefa, saída curta |
| `docker_cleanup_success` | 🧹 Limpeza Docker concluída | servidor, resumo |
| `docker_cleanup_failed` | 🧹❌ Falha na limpeza Docker | servidor, erro |
| `server_reachable` | 🟢 Servidor voltou a responder | servidor |
| `server_unreachable` | 🔴 Servidor inacessível | servidor |
| `high_disk_usage` | 💽 Disco quase cheio | uso, limite, servidor |
| `server_patch_check` | 🧩 Atualizações de SO disponíveis | total, críticos |
| `server_patch_check_error` | ⚠️ Falha ao verificar atualizações | servidor, erro |
| `traefik_version_outdated` | 🌐 Traefik desatualizado | versão atual, alvo |
| `test` | 🧪 Teste de notificação | origem, horário |

## 7. Review focus (erros prováveis que os testes devem pinar)

1. **Mensagem com campo ausente** (ex.: app sem `fqdn`): não pode imprimir `None` nem quebrar o envio — a linha desaparece.
2. **Payload gigante** (`task_failed` com `output` longo): não pode estourar 4096 e falhar no Telegram — truncar.
3. **Evento desconhecido ou JSON inválido**: não pode gerar 4xx que desligue o canal — responder 200 e registrar.
4. **Relay reiniciado com outbox pendente**: não pode duplicar mensagem já enviada nem perder a pendente — dedupe + status.
5. **Botão com URL inválida/localhost**: Telegram rejeita a mensagem inteira — remover botão e anexar link no corpo.

---

## 8. Tarefas de implementação

### Tarefa 1: Esqueleto do serviço e healthcheck

**Arquivos:** criar `coolify-tg-relay/pyproject.toml`, `app/__init__.py`, `app/config.py`, `app/main.py`, `tests/test_health.py`, `.env.example`, `.gitignore`.

**Interfaces:**
- Consome: nada.
- Produz: `load_settings() -> Settings`; `create_app(settings: Settings) -> FastAPI` com `GET /healthz`.

- [x] **Passo 1:** escrever `tests/test_health.py` com `test_healthz_returns_ok`: `TestClient(create_app(settings)).get("/healthz")` → `200`, corpo `{"ok": True, "queue": 0, "last_event": None}`.
- [x] **Passo 2:** rodar `uv run pytest tests/test_health.py -v` — esperar FAIL por `create_app` inexistente.
- [x] **Passo 3:** implementar `Settings`, `load_settings()` (falha com mensagem clara se variável faltar) e `create_app()`.
- [x] **Passo 4:** rodar pytest — PASS.
- [ ] **Passo 5:** commit `feat(relay): esqueleto do serviço com healthcheck`. *(consolidado na Tarefa 14)*

### Tarefa 2: Store SQLite (outbox, dedupe, auditoria)

**Arquivos:** criar `app/store.py`, `tests/test_store.py`.

**Interfaces:**
- Produz: `Store` (contrato 5.2), `OutboxItem` (`id`, `dedupe_key`, `payload`, `attempts`).

- [x] **Passo 1:** testes: `test_enqueue_dedupes_same_key`, `test_claim_due_only_returns_due_items`, `test_mark_failed_schedules_retry`, `test_audit_persists_rows`.
- [x] **Passo 2:** rodar pytest — FAIL.
- [x] **Passo 3:** implementar com `sqlite3`, WAL e transações; sem ORM.
- [x] **Passo 4:** pytest — PASS.
- [ ] **Passo 5:** commit `feat(relay): store sqlite com dedupe e auditoria`. *(consolidado na Tarefa 14)*

### Tarefa 3: Formatação PT-BR e templates

**Arquivos:** criar `app/format.py`, `app/templates.py`, `app/templates.yml`, `tests/test_format.py`, `tests/test_templates.py`, `tests/fixtures/payloads/*.json` (19), `tests/golden/*.txt` (19).

**Interfaces:**
- Consome: nada.
- Produz: `render(payload, cfg, extra) -> Rendered`; `EVENT_IDS`; `load_templates`.

- [x] **Passo 1:** testes de unidade: `test_escape_html`, `test_format_brt`, `test_human_duration`, `test_truncates_at_4096`, `test_drops_line_with_missing_field`, `test_drops_button_without_http_url`.
- [x] **Passo 2:** teste parametrizado `test_golden_message[<event>]` para os 19 eventos contra `tests/golden/<event>.txt`.
- [x] **Passo 3:** rodar pytest — FAIL.
- [x] **Passo 4:** implementar `format.py`, `templates.py` e o YAML com os 19 textos da seção 6.
- [x] **Passo 5:** rodar pytest — PASS; revisar os 19 golden files manualmente (texto PT-BR, acentuação, BRT).
- [ ] **Passo 6:** commit `feat(relay): templates pt-br e renderizador`. *(consolidado na Tarefa 14)*

### Tarefa 4: Cliente Telegram

**Arquivos:** criar `app/telegram.py`, `tests/test_telegram.py`.

**Interfaces:**
- Consome: `Button`.
- Produz: `TelegramClient` (contrato 5.5).

- [x] **Passo 1:** testes com `httpx.MockTransport`: `test_send_message_uses_html_and_thread`, `test_retry_after_429`, `test_fallback_when_button_url_rejected`, `test_truncates_before_send`, `test_server_error_raises`, `test_get_updates_and_answer_callback`.
- [x] **Passo 2:** pytest — FAIL.
- [x] **Passo 3:** implementar.
- [x] **Passo 4:** pytest — PASS.
- [ ] **Passo 5:** commit `feat(relay): cliente telegram com html, retry e fallback`. *(consolidado na Tarefa 14)*

### Tarefa 5: Cliente Coolify e enriquecimento

**Arquivos:** criar `app/coolify.py`, `tests/test_coolify.py`.

**Interfaces:**
- Produz: `CoolifyClient` (contrato 5.6). O enriquecimento de payload (`enrich`) é responsabilidade do worker, na Tarefa 6.

- [x] **Passo 1:** testes com MockTransport: `test_get_deployment_maps_commit_and_duration`, `test_deploy_posts_uuid`, `test_api_error_raises`.
- [x] **Passo 2:** pytest — FAIL.
- [x] **Passo 3:** implementar; erros de enriquecimento nunca impedem o envio (loga e segue).
- [x] **Passo 4:** pytest — PASS.
- [ ] **Passo 5:** commit `feat(relay): cliente da api do coolify`. *(consolidado na Tarefa 14)*

### Tarefa 6: Hook, dispatcher e worker

**Arquivos:** criar `app/worker.py`, `tests/test_hook.py`, `tests/test_worker.py`; modificar `app/main.py`.

**Interfaces:**
- Consome: `Store`, `render`, `TelegramClient`, `CoolifyClient`.
- Produz: `Dispatcher.dispatch_once()`; rotas `/hook/{secret}` e `/healthz` completas.

- [x] **Passo 1:** testes: `test_valid_secret_enqueues_and_returns_200`, `test_invalid_secret_returns_401`, `test_unknown_event_returns_200`, `test_malformed_json_returns_200`, `test_dispatcher_sends_and_marks_sent`, `test_dispatcher_retries_on_5xx`.
- [x] **Passo 2:** pytest — FAIL.
- [x] **Passo 3:** implementar; subir `Dispatcher` no `lifespan` do FastAPI.
- [x] **Passo 4:** pytest — PASS.
- [ ] **Passo 5:** commit `feat(relay): endpoint de webhook e dispatcher`. *(consolidado na Tarefa 14)*

### Tarefa 7: Docker, compose e README

**Arquivos:** criar `Dockerfile`, `compose.yml`, `README.md`; modificar `.env.example`, `.gitignore`.

**Interfaces:**
- Produz: imagem `coolify-tg-relay:local`, serviço `relay` na rede externa `coolify`.

- [x] **Passo 1:** `Dockerfile` multi-stage, `USER 10001`, `HEALTHCHECK` via `/healthz`.
- [x] **Passo 2:** `compose.yml`: `networks: coolify: external: true`, volume `relay-data`, `restart: unless-stopped`, env de `.env`.
- [x] **Passo 3:** build local: `docker build -t coolify-tg-relay:local coolify-tg-relay` — esperar exit 0.
- [x] **Passo 4:** rodar com `.env` de teste e validar `curl localhost:8787/healthz` no host (publicação temporária em 127.0.0.1).
- [ ] **Passo 5:** commit `feat(relay): empacotamento docker e documentação`. *(consolidado na Tarefa 14)*

### Tarefa 8: Deploy operacional do relay (GATE: credenciais)

**Arquivos:** criar `.env` local (não versionado).

**Pré-requisitos do usuário:** token do bot, chat ID, chat/tópicos, token de API do Coolify, app de teste.

- [x] **Passo 1:** gerar `HOOK_SECRET` com 48 caracteres (`openssl rand -hex 24`).
- [x] **Passo 2:** subir container: `docker compose up -d` (rede `coolify`).
- [x] **Passo 3:** validar do container `coolify`: `docker exec coolify python -c "import urllib.request; ..." http://coolify-tg-relay:8000/healthz` → `{"ok":true,...}` (porta interna 8000).
- [x] **Passo 4:** liberar *Settings → Advanced → Allowed internal targets* = `10.0.1.0/24` **e** `fddd:fe89:f0ec::/64` (o Coolify valida IPv4 e IPv6 resolvidos; ação aplicada via `instance_settings.webhook_allowed_internal_hosts`).
- [x] **Passo 5:** configurar webhook via API:
  `PATCH /api/v1/notifications/webhook` com `webhook_enabled=true`, `webhook_url=http://coolify-tg-relay:8000/hook/<segredo>` e os 15 `*_webhook_notifications=true`.
- [x] **Passo 6:** validar `GET /api/v1/notifications/webhook` → `webhook_enabled: true`.
- [x] **Passo 7:** teste real pelo relay → `200 {"ok":true}`, fila zerada e `last_event=test`.
- [ ] **Passo 8:** commit do que for versionável (sem `.env`). *(consolidado na Tarefa 14)*

### Tarefa 9: Validação ponta a ponta e corte do canal nativo

- [x] **Passo 1:** deploy real em `sound-music-app` → mensagem com commit `bb24bb91` e duração de 36 s.
- [x] **Passo 2:** falha de deploy validada com payload sintético `deployment_failed` (template + entrega); não foi feito deploy com commit inválido para não alterar a configuração da aplicação.
- [x] **Passo 3:** `docker stop` real tentado em `sound-music-app`, sem evento: o Coolify 4.6.0 não dispara `Application\StatusChanged` (classe sem dispatcher). Cobertura por payload sintético.
- [x] **Passo 4:** `task_success`/`task_failed` validados com payloads sintéticos; tarefa agendada real não foi criada para evitar resíduos no Coolify.
- [x] **Passo 5:** enviar payloads de exemplo para os eventos sem gatilho natural (backup, disco, patch, traefik) e conferir — 19/19 entregues.
- [x] **Passo 6:** matriz de eventos preenchida 19/19 (real em `deployment_success`; sintéticos nos demais).
- [x] **Passo 7:** desligar Telegram nativo (`telegram_enabled=false`) — confirmado por `GET /notifications/telegram`; monitorar 48 h.
- [ ] **Passo 8:** commit do relatório de validação em `_bmad-output/`. *(consolidado na Tarefa 14)*

### Tarefa 10: Bot — base, autorização e consultas

**Arquivos:** criar `app/bot.py`, `tests/test_bot_auth.py`; modificar `app/main.py`.

**Interfaces:**
- Consome: `TelegramClient`, `CoolifyClient`, `Store`.
- Produz: `Bot.run()`; comandos `/ajuda`, `/status`, `/apps`, `/app`, `/deploys`, `/logs`.

- [x] **Passo 1:** testes: `test_denies_unknown_user`, `test_allows_listed_user_and_chat`, `test_status_renders_pt_br`.
- [x] **Passo 2:** pytest — FAIL.
- [x] **Passo 3:** implementar long polling com offset persistido em `meta`.
- [x] **Passo 4:** pytest — PASS.
- [ ] **Passo 5:** commit `feat(bot): autorização e comandos de consulta`. *(consolidado na Tarefa 14)*

### Tarefa 11: Bot — ações com confirmação

**Arquivos:** modificar `app/bot.py`; criar `tests/test_bot_confirm.py`.

**Interfaces:**
- Produz: callbacks `c:<acao>:<uuid>`; comandos `/deploy`, `/iniciar`, `/reiniciar`, `/parar`.

- [x] **Passo 1:** testes: `test_action_requires_confirmation`, `test_confirmation_expires_after_60s`, `test_callback_is_single_use`, `test_rate_limits_actions_per_app`, `test_audit_written_for_action`.
- [x] **Passo 2:** pytest — FAIL.
- [x] **Passo 3:** implementar confirmação com `pending` em memória + TTL; auditar.
- [x] **Passo 4:** pytest — PASS.
- [ ] **Passo 5:** commit `feat(bot): ações com confirmação e auditoria`. *(consolidado na Tarefa 14)*

### Tarefa 12: Bot — silêncio e digest

**Arquivos:** modificar `app/bot.py`, `app/worker.py`; criar `tests/test_quiet_and_digest.py`.

- [x] **Passo 1:** testes: `test_silence_skips_non_critical_events`, `test_digest_aggregates_counts`.
- [x] **Passo 2:** pytest — FAIL.
- [x] **Passo 3:** implementar `/silenciar` e digest diário às 08:00 BRT.
- [x] **Passo 4:** pytest — PASS.
- [ ] **Passo 5:** commit `feat(bot): silêncio temporário e digest diário`. *(consolidado na Tarefa 14)*

### Tarefa 13: Documentação final e verificação

**Arquivos:** modificar `README.md`, `_bmad-output/coolify-telegram-ptbr-plan.md` (checkboxes).

- [ ] **Passo 1:** README com instalação, variáveis, comandos, runbook, rollback e rotação de segredos.
- [ ] **Passo 2:** rodar suíte completa `uv run pytest -q` e `uv run ruff check .` — exit 0.
- [ ] **Passo 3:** `docker compose config` — válido.
- [ ] **Passo 4:** verificação de vazamento: `git grep -nE "bot[0-9]{8,}:[A-Za-z0-9_-]{30,}"` → vazio.
- [ ] **Passo 5:** commit `docs(relay): runbook e verificação final`.

### Tarefa 14: Atualização do repositório

- [ ] **Passo 1:** `git status` e `git diff --stat` para revisão.
- [ ] **Passo 2:** `git add coolify-tg-relay _bmad-output/coolify-telegram-ptbr-plan.md`.
- [ ] **Passo 3:** commit `feat(coolify): relay telegram pt-br com bot de operações`.
- [ ] **Passo 4:** `git push origin main` (autorizado pelo usuário).
- [ ] **Passo 5:** confirmar `git status -sb` → `## main...origin/main` sem pendências.

---

## 9. Protocolo de execução passo a passo (obrigatório)

1. Antes de cada tarefa, apresentar: **ação**, **comando/arquivo**, **validação** e **risco**.
2. Aguardar confirmação explícita do usuário (`confirmar` / `ok`).
3. Executar **somente** a etapa confirmada.
4. Rodar a validação e mostrar a saída real (não resumida).
5. Se falhar: parar, diagnosticar com `systematic-debugging`, propor correção e pedir nova confirmação.
6. Se passar: marcar o checkbox no plano e apresentar a próxima etapa.
7. Ações que dependem de credenciais ou de UI do Coolify pausam até o usuário fornecer/executar.
8. Ao final de todas as tarefas: atualizar o repositório (Tarefa 14) e apresentar o resumo com evidências.
9. Os commits por tarefa descritos abaixo ficam **consolidados no commit final** (Tarefa 14), conforme instrução do usuário.

## 10. Definição de pronto

- [ ] 19 mensagens em PT-BR validadas por golden tests e por envio real.
- [ ] Relay saudável, com outbox sem pendências e logs sem segredos.
- [ ] Webhook habilitado com os 15 eventos; Telegram nativo desligado sem duplicidade.
- [ ] Bot autorizado, consultas e ações funcionando, auditoria registrada.
- [ ] Suíte de testes e lint verdes.
- [ ] README/runbook publicados.
- [ ] Commit e push em `origin/main` com árvore limpa.

## 11. Riscos e rollback

| Risco | Mitigação | Rollback |
|---|---|---|
| Relay indisponível | `restart: unless-stopped`, outbox, heartbeat | reativar Telegram nativo |
| Segredo vazado | rotação do `HOOK_SECRET` e do token do bot | atualizar `.env` + restart |
| Canal webhook auto-desligado | relay responde 2xx; monitorar `failure_count` | reabilitar na UI |
| Mudança de contrato em upgrade do Coolify | validar a cada release; payloads documentados | desligar webhook |
| Ação errada pelo bot | confirmação 60 s, allowlist, rate limit, auditoria | reverter via UI/API |

## 12. Estimativas

| Entrega | Prazo |
|---|---|
| Tarefas 1–7 (código e empacotamento) | 3–4 dias |
| Tarefas 8–9 (operação e validação) | 1–1,5 dia |
| Tarefas 10–12 (bot completo) | 3–4 dias |
| Tarefas 13–14 (docs e repositório) | 0,5 dia |
| **Total** | **8–10 dias úteis** |
