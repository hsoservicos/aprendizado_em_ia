# coolify-tg-relay

Relay que traduz as notificações do Coolify para **Português do Brasil** e as
entrega no Telegram (chat e tópicos), sem fork do Coolify. Inclui bot de
consulta e ações com confirmação.

## Como funciona

```
Coolify ──webhook──▶ relay (FastAPI) ──fila SQLite──▶ dispatcher ──▶ Telegram
                                                        │
                                                        └──▶ API do Coolify (consultas e ações)
```

- `POST /hook/{secret}` recebe os eventos do canal Webhook do Coolify.
- O evento é gravado em uma fila SQLite (dedupe por UUID) e respondido com `200`
  imediatamente; o envio ocorre em segundo plano.
- O dispatcher renderiza o template PT-BR, envia ao Telegram e faz retry com
  backoff em caso de falha.
- `GET /healthz` informa fila pendente e último evento processado.

## Requisitos

- Docker e Docker Compose
- Coolify com rede Docker `coolify`
- Bot do Telegram (BotFather) e chat/grupo de destino

## Configuração

Copie `.env.example` para `.env` e preencha:

| Variável | Obrigatória | Descrição |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | sim | token do bot (BotFather) |
| `TELEGRAM_CHAT_ID` | sim | chat/grupo que recebe as notificações |
| `HOOK_SECRET` | sim | segredo do webhook, mínimo 32 caracteres |
| `COOLIFY_API_TOKEN` | sim | token de API do Coolify com `read` e `deploy` |
| `COOLIFY_BASE_URL` | não | padrão `http://coolify:8080` |
| `TELEGRAM_THREADS` | não | JSON `{"deployment_success": 12}` para tópicos |
| `TELEGRAM_ALLOWED_USER_IDS` | não | CSV de usuários autorizados no bot |
| `TELEGRAM_ALLOWED_CHAT_IDS` | não | CSV de chats autorizados no bot |
| `QUIET_HOURS` | não | silêncio noturno no formato `23-6` |
| `DATABASE_PATH` | não | padrão `/data/relay.db` |
| `TZ` | não | padrão `America/Sao_Paulo` |

Nunca versione o `.env` — ele já está no `.gitignore`.

## Subir o relay

```bash
docker compose up -d --build
docker compose logs -f relay
```

O relay **não publica portas no host**. Ele entra na rede Docker `coolify` e é
alcançado pelo container do Coolify em `http://coolify-tg-relay:8000`.

## Configurar o webhook no Coolify

1. **Settings → Advanced → Outbound endpoints → Allowed internal targets**:
   libere `10.0.1.0/24` (rede interna do Docker).
2. **Notifications → Webhook**:
   - URL: `http://coolify-tg-relay:8000/hook/<HOOK_SECRET>`
   - Eventos: selecione todos os 19 suportados.
3. Clique em **Send test notification** e confira a mensagem no Telegram.

> O Coolify desativa um canal após 3 respostas 4xx consecutivas. Por isso o
> relay responde `200` para evento desconhecido ou JSON inválido; apenas
> segredo errado retorna `401`.

## Bot

Com o long polling ativo, use no Telegram:

| Comando | Efeito |
|---|---|
| `/ajuda` | cartão de ajuda |
| `/status` | apps, servidores e deploys em andamento |
| `/apps` | lista de aplicações |
| `/app <nome\|uuid>` | ficha da aplicação |
| `/deploys [app]` | últimos deploys |
| `/logs <uuid>` | status e link do deploy |
| `/deploy <app>` | confirma e dispara deploy |
| `/iniciar <app>` | confirma e inicia |
| `/reiniciar <app>` | confirma e reinicia |
| `/parar <app>` | confirma e para |
| `/silenciar <30m\|2h\|off>` | pausa/retoma notificações não críticas |

Toda ação exige confirmação por botão (validade de 60 s) e é registrada na
tabela `audit`. A allowlist vazia nega todas as ações.

## Desenvolvimento

```bash
uv sync --group dev
uv run pytest -q
uv run ruff check .
uv run uvicorn app.main:build_app --factory --reload
```

O client usa `httpx`; os testes simulam Telegram e Coolify com
`MockTransport` e não fazem chamadas reais.

## Segurança

- Segredos apenas via `.env` (não versionado) e variáveis de ambiente.
- Container roda como usuário `10001` (não-root), com `no-new-privileges`.
- Sem porta pública; acesso restrito à rede Docker `coolify`.
- O webhook do Coolify não assina requisições: a proteção é o segredo longo,
  a rede interna e a allowlist de alvos internos.

## Runbook

| Operação | Comando |
|---|---|
| Saúde do relay | `docker compose exec relay python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=5).read().decode())"` |
| Ver logs | `docker compose logs -f relay` |
| Reiniciar | `docker compose restart relay` |
| Rebuild + subir | `docker compose up -d --build` |
| Fila pendente | `docker compose exec relay python -c "import sqlite3; print(sqlite3.connect('/data/relay.db').execute(\"select status,count(*) from outbox group by status\").fetchall())"` |
| Auditoria das ações | `docker compose exec relay python -c "import sqlite3; print(sqlite3.connect('/data/relay.db').execute('select * from audit order by id').fetchall())"` |

- O offset do bot fica em `meta.bot_offset`; o silêncio em `meta.silent_until`;
  o último digest em `meta.last_digest_date`.
- O digest diário sai às 08:00 (America/Sao_Paulo) com a contagem de eventos
  desde o último digest.

## Rollback

Para voltar ao Telegram nativo do Coolify em caso de problema:

1. Parar o relay: `docker compose down` (mantém o volume `relay-data`).
2. Desligar o webhook: `PATCH /api/v1/notifications/webhook` com
   `webhook_enabled=false`.
3. Religar o Telegram nativo: `PATCH /api/v1/notifications/telegram` com
   `telegram_enabled=true`.
4. Conferir `GET /api/v1/notifications/telegram` e `GET /api/v1/notifications/webhook`.

## Rotação de segredos

1. **Bot** — no BotFather, gere um novo token (`/revoke`). Atualize
   `TELEGRAM_BOT_TOKEN` no `.env` e o campo `telegram_token` no Coolify
   (ou deixe apenas o relay, já que o nativo está desligado). Rebuild: `up -d --build`.
2. **API do Coolify** — revogue `coolify-tg-relay` em *Keys & Tokens* e crie
   outro com `read` + `deploy`; atualize `COOLIFY_API_TOKEN`.
3. **Webhook** — troque `HOOK_SECRET` (`openssl rand -hex 24`), atualize o `.env`
   e a URL do webhook no Coolify via `PATCH /api/v1/notifications/webhook`.

Após qualquer rotação, confirme `docker compose up -d --build` e o `GET /healthz`.
