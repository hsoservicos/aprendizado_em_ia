# Validação — relay Coolify → Telegram (PT-BR)

Data: 2026-11-09 · Coolify 4.6.0 · relay `coolify-tg-relay:local`

## Ambiente

- Relay na rede Docker `coolify`, sem portas públicas, usuário `10001`.
- Coolify alcança `http://coolify-tg-relay:8000`; relay alcança `http://coolify:8080`.
- Webhook habilitado com os 15 eventos do canal, `failure_count=0`.
- Allowlist de alvos internos: `10.0.1.0/24` e `fddd:fe89:f0ec::/64`
  (o Coolify valida IPv4 e IPv6 resolvidos pelo nome do container).

## Credenciais

- Token do bot e chat ID recuperados do Telegram nativo do Coolify
  (descriptografados no próprio Coolify; valores não exibidos).
- `getMe` e `getChat` da API do Telegram: OK.
- Token de API `coolify-tg-relay` criado com `read` + `deploy`, validado em
  `GET /api/v1/applications` (200, 4 aplicações).
- Nenhum segredo foi gravado no repositório; `.env` está fora do git e com modo `600`.

## Deploy real

```
POST /api/v1/deploy → 200
deployment_uuid: mfzjmi9cfyeycvlz0byvt93n
status: in_progress → finished
commit: bb24bb91
duração: 36 s (14:24:00 → 14:24:36 UTC)
```

Relay após o evento:

```
healthz: {"ok":true,"queue":0,"last_event":"deployment_success"}
outbox:  {"sent":2,"pending":0}
webhook failure_count: 0
```

Mensagem “✅ Deploy concluído” confirmada pelo usuário no Telegram.

## Matriz de eventos

| Evento | Evidência |
|---|---|
| `deployment_success` | real (deploy acima) + sintético |
| `deployment_failed` | sintético |
| `status_changed` | sintético¹ |
| `container_restarted` | sintético |
| `restart_limit_reached` | sintético |
| `backup_success` | sintético |
| `backup_failed` | sintético |
| `backup_success_with_s3_warning` | sintético |
| `task_success` | sintético |
| `task_failed` | sintético |
| `docker_cleanup_success` | sintético |
| `docker_cleanup_failed` | sintético |
| `server_reachable` | sintético |
| `server_unreachable` | sintético |
| `high_disk_usage` | sintético |
| `server_patch_check` | sintético |
| `server_patch_check_error` | sintético |
| `traefik_version_outdated` | sintético |
| `test` | sintético, recebido no Telegram |

Todos os 19 payloads responderam `200`; outbox terminou com `pending=0`.
¹ `docker stop` real não gerou evento: o Coolify 4.6.0 não possui dispatcher para
`Application\StatusChanged`. O template foi validado por payload sintético.

## Corte do canal nativo

`PATCH /api/v1/notifications/telegram` com `telegram_enabled=false` → 200.
`GET` confirma `telegram_enabled: false`. Monitorar 48 h; o relay é o único emissor.

## Pendências

- Monitoramento de 48 h do relay com o Telegram nativo desligado.
- Rotacionar a chave SSH privada exposta acidentalmente durante a configuração.
