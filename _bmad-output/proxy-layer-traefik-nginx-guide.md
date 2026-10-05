# Guia: Camada de Proxy no Coolify — Traefik × nginx

**Versão**: 1.0.0
**Data**: 2026-10-05
**Autor**: Hsantos
**Validado em**: Coolify v4.3.23 · Traefik v3.7.13 · túnel Cloudflare
**Base**: análise de arquitetura com medições de desempenho reais

---

## 0. Para que serve este guia

Definir o **melhor uso das aplicações de proxy** em publicações no Coolify,
eliminando redundâncias e concentrando cada função na camada correta. Resultado
direto: builds mais leves, menos hops por requisição e configuração consistente
entre aplicações.

> **Pergunta que motiva o guia:** o nginx, colocado à frente das aplicações,
> não seria redundante com o Traefik (coolify-proxy)?

---

## 1. Resposta objetiva

**Depende do tipo de entrega:**

| Cenário | Há redundância? | Caminho correto |
| --- | --- | --- |
| Conteúdo **estático** (HTML/CSS/JS, docs, landing) | **Não** | Traefik → **nginx** |
| **API / backend dinâmico** (Node, Python, PHP…) | **Sim**, se houver nginx no meio | Traefik → **aplicação direto** |
| **SPA + API** (mesmo domínio) | Parcial | Traefik → nginx (SPA) + `/api` → aplicação |
| Proxy sobre proxy | **Sim** | Nunca empilhar proxies redundantes |

### 1.1 Papéis reais (não são intercambiáveis)

| Componente | Papel | Serve arquivos estáticos? |
| --- | --- | --- |
| **Traefik** (`coolify-proxy`) | **Ingress / reverse proxy** — roteamento por `Host`, middlewares (compress, redirect, headers), descoberta por labels Docker | **NÃO** |
| **nginx** (container da aplicação) | **Web server de estáticos** — lê o disco e responde o conteúdo | **SIM** |
| **Aplicação** (backend/API) | **Servidor HTTP da regra de negócio** | Serve o que for da sua alçada |

---

## 2. Evidência 1 — Traefik não serve arquivos estáticos

Testado no Traefik **v3.7.13** (instância self-hosted):

```yaml
http:
  middlewares:
    test-files:
      fileServer:
        root: /html
```

**Resultado:**

```text
ERR  Error while building configuration
     error="collecting file configs: /dynamic/test.yaml: field not found, node: fileServer"
```

> O middleware `fileServer` **não existe** no Traefik v3.7. Ele é um
> *reverse proxy*, não um *web server*: encaminha requisições, não lê arquivos
> do disco. **Não é possível publicar site estático "somente com Traefik".**

---

## 3. Evidência 2 — o Coolify usa nginx para estáticos

Inspecionando a instância (`bootstrap/helpers/shared.php`):

```php
function defaultNginxConfiguration(string $type = 'static'): string
{
    return <<<'NGINX'
        root /usr/share/nginx/html;
        ...
    NGINX;
}
```

> O **build pack `static` do Coolify gera configuração nginx** por padrão.
> Usar nginx para estáticos é o **padrão da plataforma**, não uma adição
> arbitrária de infraestrutura.

---

## 4. Cadeia real de acesso

```text
Navegador
  → Cloudflare (TLS, cache, WAF, edge)
    → túnel cloudflared
      → Traefik (coolify-proxy) :80        ← ingress: Host, compress, headers
        → destino
             ├─ nginx        (estáticos)
             └─ aplicação    (API / backend)
```

---

## 5. Medições de desempenho (referência)

Página estática de 7,5 KB · 150 requisições sequenciais + carga de 6 s com 16
conexões concorrentes.

### 5.1 Latência sequencial

| Cenário | p50 | p95 | p99 | média | req/s |
| --- | ---: | ---: | ---: | ---: | ---: |
| nginx **direto** (sem proxy) | **0,78 ms** | 1,91 ms | 2,42 ms | 0,93 ms | **1077** |
| Traefik → nginx (hop local) | 1,50 ms | 4,21 ms | 6,79 ms | 2,04 ms | 490 |
| Cloudflare → Traefik → nginx (**público**) | 193,60 ms | 228,24 ms | 259,76 ms | 199,39 ms | 5 |

### 5.2 Carga concorrente (16 conexões, 6 s)

| Cenário | total | req/s | p50 | p95 |
| --- | ---: | ---: | ---: | ---: |
| nginx **direto** | 6433 | **1072** | 10,93 ms | 29,76 ms |
| Traefik → nginx | 5069 | **845** | 15,67 ms | 34,74 ms |
| Cloudflare → Traefik → nginx | 156 | 26 | 216,32 ms | 265,11 ms |

### 5.3 Leitura dos números

| Fato | Valor | Interpretação |
| --- | --- | --- |
| Custo do hop Traefik | **~0,7 ms** · **~21%** de throughput (1072 → 845 req/s) | Baixo; aceitável pelo que entrega |
| Custo do nginx | **~3 MiB** RAM · **0%** CPU ocioso · imagem **~75 MB** | Irrisório |
| **Custo Cloudflare/rede** | **~200 ms** (p50) | **Dominante** — 15 a 25× a pilha local |

> **Conclusão numérica:** o gargalo real é a **rede/edge do Cloudflare**, não a
> pilha de proxy. Remover nginx dos **estáticos** não seria possível (Traefik não
> serve arquivos); remover nginx das **APIs** elimina ~1 hop e ~3 MiB por réplica
> sem impacto perceptível ao usuário.

---

## 6. Regra de ouro — cada função de proxy uma única vez

| Função | Camada correta | Evitar |
| --- | --- | --- |
| TLS / certificados | **Cloudflare** (terminação) | Duplicar no Traefik e no nginx |
| Redirect HTTP→HTTPS | **Traefik** (middleware) | Repetir no nginx ou na aplicação |
| Compressão (gzip/brotli) | **Traefik** (`compress: true`) | `gzip on` no nginx quando o Traefik já comprime |
| Headers de segurança | **Traefik** (`headers`) **ou** nginx | Configurar nos **dois** |
| Cache de assets imutáveis | **nginx** (ou Cloudflare) | — |
| Roteamento por domínio/caminho | **Traefik** | Usar nginx como roteador |
| Servir arquivos estáticos | **nginx** | Tentar no Traefik |
| Rate limit / WAF | **Cloudflare** | — |
| Lógica de negócio | **Aplicação** | Empurrar para o proxy |

### 6.1 Anti-padrão comum: compressão duplicada

Muitos `nginx.conf` de exemplo trazem `gzip on; …`. Se o Traefik já tem o
middleware `compress: true` (o Coolify gera `gzip` em `traefik/dynamic/coolify.yaml`),
o conteúdo é **comprimido duas vezes** — CPU desperdiçada e possível ganho zero.

**Correção:** remover o bloco `gzip` do `nginx.conf` do app e deixar a
compressão **somente** no Traefik.

### 6.2 `nginx.conf` recomendado para estáticos (sem redundância)

```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;
    charset utf-8;

    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    location = /healthz {
        access_log off;
        default_type text/plain;
        return 200 "ok\n";
    }

    location / { try_files $uri $uri/ =404; }

    location ~* \.(css|js|svg|png|jpg|jpeg|gif|ico|webp|woff2)$ {
        expires 7d;
        add_header Cache-Control "public";
    }
}
```

> Sem `gzip` — compressão fica no Traefik. Headers podem migrar para o Traefik
> se quiser consistência entre apps; mantidos no nginx apenas se o app for
> exposto também sem o Traefik.

---

## 7. Matriz de decisão — melhor opção de proxy no Coolify

| Tipo de entrega | Caminho | Build Pack | Por quê |
| --- | --- | --- | --- |
| **Estático** (landing, docs, apresentação) | Traefik → nginx | **`static`** (Coolify) ou `Dockerfile` | Traefik não serve arquivos; nginx é o padrão do Coolify |
| **API REST / backend** | Traefik → aplicação | `nixpacks` ou `Dockerfile` | Remover nginx do meio; backend já é servidor HTTP |
| **SPA + API** (mesmo domínio) | Traefik → nginx (SPA) + `/api` → app | `Dockerfile` com `proxy_pass` **ou** routers separados | Separação clara de responsabilidades |
| **Múltiplos serviços** | Traefik roteia por `Host`/caminho | — | Um único ingress para todos os apps |
| TLS / redirect / headers / compressão | **Traefik** (middlewares) | — | Uma vez no ingress, não por app |

### 7.1 Caminhos padrão

```text
ESTÁTICO:   Cloudflare → Traefik → nginx (arquivos)
API:        Cloudflare → Traefik → aplicação (porta exposta)   ← sem nginx
SPA + API:  Cloudflare → Traefik → nginx (SPA) / app (/api)
```

---

## 8. Checklist de auditoria de camada de proxy

Use ao revisar um projeto publicado no Coolify:

- [ ] Conteúdo estático é servido por **nginx** (ou build pack `static`)?
- [ ] **Não** há nginx entre Traefik e aplicação dinâmica?
- [ ] `gzip`/`compress` está em **um** lugar só (preferencialmente Traefik)?
- [ ] Redirect HTTP→HTTPS está **só** no Traefik?
- [ ] Headers de segurança configurados em **um** lugar?
- [ ] `/healthz` (ou equivalente) responde `200` sem autenticação?
- [ ] Domínio no Coolify usa **`http://`** quando o TLS é do Cloudflare?
- [ ] Auto-deploy desativado se a publicação for manual?

---

## 9. Solução de problemas

| Sintoma | Causa provável | Correção |
| --- | --- | --- |
| Conteúdo não publica, `404` no Traefik | Esperando que o Traefik sirva arquivos | Adicionar nginx (ou build pack `static`) |
| `gzip` aparenta não funcionar | Compressão só no nginx, mas o Traefik devolve sem comprimir (ou o contrário) | Deixar `compress` **só** no Traefik |
| Latência alta na resposta | Gargalo de **rede/Cloudflare**, não do proxy | Ver §5.3 — normal ~200 ms via túnel |
| Loop de redirect `307` | Domínio registrado como `https://` com TLS no Cloudflare | Registrar como `http://` (ver `coolify-cloudflare-tunnel-deploy-playbook.md`) |
| Dois `Server` headers / headers duplicados | Headers em nginx **e** em middleware do Traefik | Centralizar em um |

---

## 10. Referências

| Documento | Uso |
| --- | --- |
| `coolify-deploy-guide.md` | Visão geral do Coolify + CLI |
| `coolify-github-deploy-guide.md` | Fontes GitHub (público, Deploy Key, GitHub App) |
| `coolify-local-deploy-guide.md` | Fontes sem Git |
| `coolify-cloudflare-tunnel-deploy-playbook.md` | Publicação com túnel Cloudflare (regra do `http://`) |
| Traefik Docs (middlewares) | https://doc.traefik.io/traefik/middlewares/http/overview/ |
