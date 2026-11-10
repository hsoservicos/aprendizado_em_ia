# Atualizações pendentes — Coolify e Traefik

Verificado em 2026-11-09. **Decisão do usuário: adiar** (não aplicado).

## Pendências

| Componente | Atual | Última | Tipo | Observação |
|---|---|---|---|---|
| Coolify | `4.6.0` | `4.7.1` | minor | `4.7.1` publicada em 2026-11-09 (mesmo dia). Roda migrações de banco. |
| Traefik (`coolify-proxy`) | `3.7.15` | `3.7.17` | patch | Corrige CVE GHSA-xv5x-242w-7hf7. Mesma minor (3.7, com suporte ativo). |

## Por que não fazer por docker direto

- **Coolify:** não há endpoint REST de auto-update (`/api/v1` só tem `GET /version`).
  O update roda migrações e retroca a própria imagem; `docker pull`/`recreate`
  manual do container `coolify` é inadequado e arriscado.
- **Traefik:** o `coolify-proxy` é gerido pelo Coolify (labels/config). Atualização
  correta via UI **Server → Proxy**, que regenera o compose e recria o proxy.
  `docker restart` não pega nova imagem (tag resolvida no create).
- Único endpoint de proxy via API: `POST /servers/{uuid}/proxy/restart`
  (ability `deploy`) — apenas reinicia, não é o bump canônico de versão.

## Pré-condições verificadas

- Disco `/var`: 79 G livres (12%) — folga OK.
- ⚠️ Nenhum backup S3/offsite do banco do Coolify (`s3_storages = 0`).
- O relay já recebeu o evento `traefik_version_outdated` (o Coolify detectou).

## Procedimento recomendado (quando for retomar)

1. Dump do banco `coolify-db` (Postgres) antes de qualquer update.
2. Traefik via UI → Server → Proxy (patch de segurança; não convém adiar).
3. Coolify via UI → banner "Update to 4.7.1" (rodar migrações).
4. Verificar após: `GET /api/v1/version`, versão do proxy, `GET /healthz` do relay.

## Notas

- `4.7.1` é estável mas recém-lançada; opcional aguardar 24–48 h para o Coolify
  (o do Traefik, por ser CVE, é mais urgente).
