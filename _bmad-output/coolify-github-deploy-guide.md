# Guia Completo: Deploy de Repositórios GitHub no Coolify

**Versão**: 1.0.0  
**Data**: 2026-09-03  
**Coolify**: v4.3.14 (self-hosted)  
**Autor**: Hsantos

---

## 1. Visão Geral — Métodos de Deploy GitHub

O Coolify suporta três métodos principais para deploy de repositórios GitHub:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    GitHub Repository Deployment                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐   │
│  │  🌐 PÚBLICO      │  │  🔐 PRIVADO      │  │  🔐 PRIVADO      │   │
│  │                  │  │  (Deploy Key)    │  │  (GitHub App)    │   │
│  │  Sem autenticação│  │  1 repositório   │  │  N repositórios  │   │
│  │  URL HTTPS       │  │  SSH key         │  │  Webhook + PR    │   │
│  │  Apenas clone    │  │  Read-only       │  │  Full access     │   │
│  │                  │  │                  │  │                  │   │
│  │  Melhor para:    │  │  Melhor para:    │  │  Melhor para:    │   │
│  │  • OSS           │  │  • Apps simples  │  │  • Equipes       │   │
│  │  • Protótipos    │  │  • 1 repo priv.  │  │  • Múltiplos     │   │
│  │  • Demos         │  │  • Sem perms     │  │  • CI/CD completo│   │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘   │
│                                                                      │
│  ⚡ Setup: 2 min         ⏱️ Setup: 5 min        ⏱️ Setup: 15 min     │
│  🔧 Automação: Webhook   🔧 Automação: Webhook  🔧 Automação: Nativa│
└─────────────────────────────────────────────────────────────────────┘
```

### Comparativo Rápido

| Critério | Público | Deploy Key | GitHub App |
|----------|---------|------------|------------|
| **Autenticação** | Nenhuma | SSH Key | OAuth + Webhook |
| **Repositórios** | 1 (público) | 1 (privado) | Múltiplos |
| **Auto Deploy (push)** | Via webhook manual | Via webhook manual | Nativo |
| **Preview Deployments** | ❌ | ❌ | ✅ |
| **Seleção de repositório** | ❌ | ❌ | ✅ |
| **GitHub Enterprise** | ✅ | ✅ | ✅ |
| **Organização** | ✅ | ✅ | ✅ |
| **Complexidade** | Baixa | Média | Alta |
| **Segurança** | Média | Alta | Alta |

---

## 2. Repositório Público

### 2.1 Quando Usar

- Código-fonte aberto (open source)
- Protótipos e demos
- Projetos sem dados sensíveis
- Setup rápido para testes

### 2.2 Pré-requisitos

- Repositório público no GitHub
- Coolify instalado e rodando
- URL HTTPS do repositório

### 2.3 Passo a Passo Detalhado

#### Passo 1: Obter URL do Repositório

```
1. Acesse o repositório no GitHub
2. Clique no botão verde "Code"
3. Selecione "HTTPS"
4. Copie a URL: https://github.com/usuario/repositorio.git
```

#### Passo 2: Criar Recurso no Coolify

```
1. Acesse o Dashboard do Coolify
2. Selecione o Projeto
3. Clique em "+ New" (Novo Recurso)
4. Selecione "Public Repository"
5. Cole a URL HTTPS do repositório
```

#### Passo 3: Configurar Build Pack

```
Coolify detecta automaticamente o framework. Se não detectar:

1. Selecione o Build Pack manualmente:
   - Nixpacks (recomendado para a maioria)
   - Dockerfile (se existe Dockerfile no repo)
   - Static (para sites estáticos)
   - Docker Compose (para multi-container)

2. Configure:
   - Branch: main (ou master)
   - Base Directory: / (raiz do repo)
   - Port: porta que a app escuta
```

#### Passo 4: Configurar Variáveis de Ambiente

```
1. Vá em Configuration > Environment Variables
2. Adicione as variáveis necessárias:
   - NODE_ENV=production
   - DATABASE_URL=postgres://...
   - API_KEY=xxx

3. Para build-time variables, marque "Build Variable"
```

#### Passo 5: Configurar Domínio

```
1. Vá em Configuration > Networking > Domains
2. Adicione o domínio: app.seudominio.com
3. O Coolify gera SSL automaticamente via Let's Encrypt
```

#### Passo 6: Deploy

```
1. Clique em "Deploy"
2. Monitore o build log
3. Verifique se o container está healthy
4. Acesse pelo domínio configurado
```

### 2.4 Deploy via CLI (Público)

```bash
# Configurar contexto
coolify context add -d production https://coolify.seudominio.com <TOKEN>

# Criar aplicação
coolify app create public \
  --server-uuid <SERVER_UUID> \
  --project-uuid <PROJECT_UUID> \
  --environment-name production \
  --git-repository https://github.com/usuario/repositorio \
  --git-branch main \
  --build-pack nixpacks \
  --ports-exposes 3000

# Deploy
coolify deploy name <app-name>
```

### 2.5 Webhook para Auto Deploy

Para deploy automático a cada push:

```
1. No Coolify, vá em Configuration > Advanced > Auto Deploy
2. Copie a URL do webhook
3. No GitHub, vá em Settings > Webhooks > Add webhook
4. Cole a URL do Coolify
5. Selecione "Just the push event"
6. Clique em "Add webhook"
```

---

## 3. Repositório Privado — Deploy Key

### 3.1 Quando Usar

- Repositório privado com **apenas 1 repositório** necessário
- Organização onde **não é possível instalar GitHub App**
- Preferência por acesso **read-only** específico do repositório
- Controle granular de segurança por repositório

### 3.2 Como Funciona

```
┌─────────────────────┐     ┌─────────────────────┐
│     Coolify         │     │      GitHub          │
│                     │     │                      │
│  ┌───────────────┐  │     │  ┌───────────────┐   │
│  │  Private Key  │──┼─────┼─▶│  Deploy Key   │   │
│  │  (armazenada) │  │ SSH │  │  (pública)    │   │
│  └───────────────┘  │     │  └───────────────┘   │
│                     │     │                      │
│  coolify clone ─────┼─────┼─▶ git clone (read)   │
│                     │     │                      │
└─────────────────────┘     └─────────────────────┘
```

### 3.3 Passo a Passo Detalhado

#### Passo 1: Gerar Chave SSH no Coolify

```
1. Acesse Dashboard > Keys & Tokens
2. Clique na aba "Private Keys"
3. Clique em "+ Add"
4. Selecione:
   - "Generate new RSA SSH Key" (compatível com todos)
   - OU "Generate new ED25519 SSH Key" (mais moderno e seguro)
5. Copie a chave PÚBLICA
6. Clique em "Continue" para salvar
```

**Alternativa — Gerar externamente:**
```bash
# Gerar chave RSA
ssh-keygen -t rsa -b 4096 -C "coolify-deploy-key"

# OU gerar chave ED25519 (recomendado)
ssh-keygen -t ed25519 -C "coolify-deploy-key"

# Copiar chave pública
cat ~/.ssh/id_ed25519.pub
```

#### Passo 2: Adicionar Deploy Key no GitHub

```
1. Acesse o repositório no GitHub
2. Vá em Settings > Deploy keys
3. Clique em "Add deploy key"
4. Configure:
   - Title: "Coolify Deploy Key" (ou nome descritivo)
   - Key: Cole a chave pública copiada
   - Allow write access: DESMARCADO (manter read-only)
5. Clique em "Add key"
```

**⚠️ IMPORTANTE:** 
- NÃO marque "Allow write access" — Coolify só precisa ler
- Cada deploy key é vinculada a **um único repositório**
- Se precisar de write access (push), use GitHub App

#### Passo 3: Copiar URL SSH do Repositório

```
1. No repositório GitHub, vá em Code > Local > SSH
2. Copie a URL: git@github.com:usuario/repositorio.git
3. ⚠️ NÃO use a URL HTTPS — use APENAS a SSH
```

#### Passo 4: Criar Recurso no Coolify

```
1. Acesse Dashboard > Projeto > "+ New"
2. Selecione "Private Repository (with Deploy Key)"
3. Selecione o servidor de destino
4. Selecione a Private Key criada no Passo 1
5. Cole a URL SSH do repositório
6. Configure:
   - Branch: main
   - Build Pack: nixpacks/dockerfile/etc
   - Port: porta da aplicação
7. Clique em "Deploy"
```

### 3.4 Deploy via CLI (Deploy Key)

```bash
# 1. Gerar chave SSH
ssh-keygen -t ed25519 -C "coolify-deploy" -f ~/.ssh/coolify_deploy

# 2. Adicionar chave pública no GitHub
# Copiar e colar em Settings > Deploy keys

# 3. Configurar SSH para usar a chave
cat >> ~/.ssh/config << EOF
Host github.com-deploy
  HostName github.com
  User git
  IdentityFile ~/.ssh/coolify_deploy
  IdentitiesOnly yes
EOF

# 4. Criar app no Coolify (via Dashboard)
# Usar "Private Repository (with Deploy Key)"

# 5. Deploy via CLI
coolify deploy name <app-name>
```

### 3.5 Auto Deploy com Deploy Key

Para deploy automático com Deploy Key:

```
1. No Coolify: Configuration > Advanced > Auto Deploy → Ativar
2. No GitHub: Settings > Webhooks > Add webhook
   - URL: <webhook-url-do-coolify>
   - Content type: application/json
   - Events: Just the push event
3. Salvar
```

### 3.6 Limitações do Deploy Key

| Limitação | Descrição | Solução |
|-----------|-----------|---------|
| 1 repositório por chave | Cada key só acessa 1 repo | Criar múltiplas keys |
| Sem acesso a outros repos | Não lista outros repos | Usar GitHub App |
| Sem preview deployments | Não cria ambientes de PR | Usar GitHub App |
| Sem webhook automático | Configurar manualmente | Configurar webhook |

---

## 4. Repositório Privado — GitHub App (Recomendado)

### 4.1 Quando Usar

- **Múltiplos repositórios** privados
- **Preview Deployments** para Pull Requests
- **Auto Deploy** nativo (sem webhook manual)
- **Equipes** com múltiplos membros
- **Organizações** GitHub
- **GitHub Enterprise**

### 4.2 Como Funciona

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────┐
│     Coolify         │     │      GitHub          │     │  Desenvol.  │
│                     │     │                      │     │             │
│  ┌───────────────┐  │     │  ┌───────────────┐   │     │  Push code  │
│  │  GitHub App   │◀─┼─────┼──│  Installation  │   │◀────│  Create PR  │
│  │  (config)     │  │ API │  │  (permissões)  │   │     │  Merge PR   │
│  └───────────────┘  │     │  └───────────────┘   │     │             │
│                     │     │                      │     │             │
│  ┌───────────────┐  │     │  ┌───────────────┐   │     │             │
│  │  Webhook      │◀─┼─────┼──│  Events       │   │◀────│             │
│  │  (auto deploy)│  │     │  │  push, PR     │   │     │             │
│  └───────────────┘  │     │  └───────────────┘   │     │             │
│                     │     │                      │     │             │
│  ┌───────────────┐  │     │  ┌───────────────┐   │     │             │
│  │  Private Key  │──┼─────┼─▶│  Auth         │   │     │             │
│  │  (.pem)       │  │     │  │  (OAuth/JWT)  │   │     │             │
│  └───────────────┘  │     │  └───────────────┘   │     │             │
└─────────────────────┘     └─────────────────────┘     └─────────────┘
```

### 4.3 Permissões Necessárias

| Permissão | Nível | Necessária para |
|-----------|-------|-----------------|
| Contents | Read | Clonar repositório |
| Metadata | Read | Informações do repo |
| Pull requests | Read & Write | Preview deployments |
| Email addresses | Read | Notificações |

### 4.4 Passo a Passo — Instalação Automatizada (Recomendado)

#### Passo 1: Criar GitHub App no Coolify

```
1. Acesse Dashboard > Sources
2. Clique em "+ Add" (GitHub App)
3. Preencha:
   - Name: "Coolify Deploy" (ou nome descritivo)
   - Organization: (deixe vazio se conta pessoal)
4. Clique em "Continue"
5. ⚠️ Anote o Source ID (UUID na URL)
```

#### Passo 2: Registrar no GitHub

```
1. Clique em "Register Now"
2. Você será redirecionado ao GitHub
3. Dê um nome único ao App: "coolify-deploy-seunome"
4. Selecione "Only on this account"
5. Clique em "Create GitHub App"
6. ⚠️ Anote:
   - App ID
   - Client ID
```

#### Passo 3: Gerar Client Secret

```
1. No GitHub App, vá em "Generate a new client secret"
2. ⚠️ Anote o Client Secret (aparece apenas uma vez!)
```

#### Passo 4: Gerar Private Key

```
1. Role para baixo até "Private keys"
2. Clique em "Generate a private key"
3. Um arquivo .pem será baixado automaticamente
4. ⚠️ Guarde este arquivo com segurança
```

#### Passo 5: Instalar o App

```
1. No sidebar, vá em "Install App"
2. Clique em "Install"
3. Selecione:
   - "All repositories" (acesso total)
   - OU "Only select repositories" (selecionar específicos)
4. Clique em "Install"
5. ⚠️ Anote o Installation ID (número na URL após /installations/)
```

#### Passo 6: Adicionar Chave Privada no Coolify

```
1. No Coolify: Dashboard > Keys & Tokens > Private Keys
2. Clique em "+ Add"
3. Nome: "GitHub App Key"
4. Cole o conteúdo do arquivo .pem baixado
5. Clique em "Continue"
```

#### Passo 7: Configurar GitHub App no Coolify

```
1. Volte em Sources > GitHub App criado
2. Preencha:
   - App ID: (anotado no Passo 2)
   - Installation ID: (anotado no Passo 5)
   - Client ID: (anotado no Passo 2)
   - Client Secret: (anotado no Passo 3)
   - Webhook Secret: (gerado automaticamente)
   - Private Key: selecione a chave criada no Passo 6
3. Clique em "Sync Name"
4. Se aparecer sucesso, está configurado!
```

#### Passo 8: Criar Aplicação

```
1. Dashboard > Projeto > "+ New"
2. Selecione "Private Repository (with GitHub App)"
3. Selecione o servidor
4. Selecione o GitHub App configurado
5. Selecione o repositório da lista
6. Configure build pack, porta, etc.
7. Clique em "Deploy"
```

### 4.5 Passo a Passo — Instalação Manual

Para GitHub Enterprise ou configuração personalizada:

#### Passo 1: Criar App no GitHub

```
1. Acesse GitHub > Settings > Developer settings > GitHub Apps
2. Clique em "New GitHub App"
3. Configure:
   - GitHub App name: "coolify-deploy"
   - Homepage URL: https://coolify.seudominio.com
   - Webhook URL: https://coolify.seudominio.com/github webhook
   - Webhook secret: gere um secreto aleatório
4. Permissões:
   - Repository permissions:
     - Contents: Read-only
     - Metadata: Read-only
     - Pull requests: Read and Write
   - Account permissions:
     - Email addresses: Read-only
5. Where can this GitHub App be installed:
   - Only on this account
6. Clique em "Create GitHub App"
7. ⚠️ Anote: App ID, Client ID
```

#### Passo 2: Configurar Credenciais

```
1. No GitHub App:
   - Generate a new client secret → Anote
   - Generate a private key → Baixe o .pem
2. Anote o Installation ID:
   - Install App > Install > URL contiene /installations/<ID>
```

#### Passo 3: Adicionar no Coolify

```
1. Sources > + Add > GitHub App
2. Preencha todos os campos manualmente
3. Adicione a private key
4. Teste com "Sync Name"
```

### 4.6 Deploy via CLI (GitHub App)

```bash
# GitHub Apps são integrados via Dashboard
# CLI usa o contexto já configurado

# Listar repositórios acessíveis
coolify github list
coolify github repos <github-app-uuid>

# Criar app (usando dados do GitHub App)
coolify app create public \
  --server-uuid <SERVER_UUID> \
  --project-uuid <PROJECT_UUID> \
  --environment-name production \
  --git-repository https://github.com/usuario/repo \
  --git-branch main \
  --build-pack nixpacks \
  --ports-exposes 3000

# Deploy
coolify deploy name <app-name>
```

### 4.7 Preview Deployments (GitHub App Only)

```
1. No Coolify, vá em Configuration > Preview Deployments
2. Ative "Preview Deployments"
3. Configure URL Template: {{pr_id}}.{{domain}}
4. Ative "Auto Deploy" para PRs

Agora:
- Todo PR cria automaticamente um ambiente de preview
- URL: 123.app.seudominio.com (onde 123 é o PR ID)
- Merge fecha o ambiente automaticamente
```

### 4.8 Auto Deploy Nativo (GitHub App Only)

```
1. No Coolify: Configuration > Advanced > Auto Deploy → Ativo
2. Não precisa configurar webhook manualmente!
3. O GitHub App já configura o webhook automaticamente
4. Toda alteração no branch configurado dispara deploy
```

---

## 5. Fluxograma de Decisão

```
Precisa deploy de repositório GitHub?
│
├─ O repositório é PÚBLICO?
│  │
│  └─ SIM → Use "Public Repository"
│     │      (URL HTTPS, sem autenticação)
│     │      Setup: 2 minutos
│     │
│  └─ NÃO (PRIVADO) → Precisa de múltiplos repositórios?
│     │
│     └─ NÃO (apenas 1 repo) → Pode instalar GitHub App?
│        │
│        ├─ NÃO → Use "Deploy Key"
│        │         (SSH key, 1 repo, read-only)
│        │         Setup: 5 minutos
│        │
│        └─ SIM → Use "GitHub App" (melhor opção)
│                  (múltiplos repos, auto deploy, PR previews)
│                  Setup: 15 minutos
│
│     └─ SIM (múltiplos repos) → Use "GitHub App"
│                                  (única opção para múltiplos repos)
│                                  Setup: 15 minutos
```

---

## 6. Segurança e Boas Práticas

### 6.1 Deploy Keys

| Prática | Recomendação |
|---------|--------------|
| **Write access** | ❌ NUNCA marcar para Coolify |
| **Uma key por repo** | ✅ Ideal para isolamento |
| **Rotacionar keys** | ✅ A cada 90 dias ou se comprometida |
| **Monitorar uso** | ✅ Verificar logs de acesso |

### 6.2 GitHub Apps

| Prática | Recomendação |
|---------|--------------|
| **Escopo** | ✅ Apenas repos necessários |
| **Permissões** | ✅ Mínimo necessário |
| **Webhook secret** | ✅ Sempre usar e rotacionar |
| **Private key** | ✅ Armazenar em local seguro |
| **Installation ID** | ✅ Não expor em logs |

### 6.3 Variáveis de Ambiente

| Prática | Recomendação |
|---------|--------------|
| **Secrets** | ✅ Usar Coolify Environment Variables |
| **Hardcoded** | ❌ NUNCA committar no repo |
| **.env.example** | ✅ Template sem valores reais |
| **.gitignore** | ✅ Excluir .env de todos os ambientes |

---

## 7. Troubleshooting

### 7.1 Deploy Key — Falha no Clone

```
Erro: Permission denied (publickey)

Solução:
1. Verificar se a chave pública está no GitHub (Settings > Deploy keys)
2. Verificar se a chave privada está no Coolify (Keys & Tokens)
3. Verificar se está usando URL SSH (não HTTPS)
4. Testar: ssh -T git@github.com (deve retornar "successfully authenticated")
```

### 7.2 GitHub App — Repositórios Não Aparecem

```
Erro: Nenhum repositório listado ao criar app

Solução:
1. Verificar se o App foi instalado (GitHub > Settings > Installations)
2. Verificar permissões de Contents (Read-only)
3. Clique em "Update Repositories" no Coolify
4. Selecione os repositórios corretos
```

### 7.3 Auto Deploy Não Funciona

```
Erro: Push não dispara deploy

Solução (Deploy Key):
1. Verificar se webhook foi adicionado no GitHub
2. Verificar se Auto Deploy está ativo no Coolify
3. Verificar URL do webhook
4. Testar: enviar push de teste

Solução (GitHub App):
1. Verificar se App está instalado
2. Verificar eventos: push precisa estar habilitado
3. Verificar logs do webhook no Coolify
```

### 7.4 Preview Deployments Não Criam Ambientes

```
Erro: PR não gera ambiente de preview

Solução:
1. Verificar se Preview Deployments está ativo
2. Verificar permissão Pull Requests (Read & Write)
3. Verificar URL Template configurado
4. Verificar se o PR está aberto (não merged/closed)
```

---

## 8. Comandos CLI de Referência

```bash
# ─── Contextos ──────────────────────────────────────────────────
coolify context add -d production <url> <token>
coolify context verify

# ─── GitHub Apps ────────────────────────────────────────────────
coolify github list                        # Listar apps integrados
coolify github repos <app-uuid>            # Listar repositórios
coolify github branches <app-uuid> owner/repo  # Listar branches

# ─── Aplicações ────────────────────────────────────────────────
# Criar (Público)
coolify app create public \
  --server-uuid <uuid> \
  --project-uuid <uuid> \
  --environment-name production \
  --git-repository https://github.com/user/repo \
  --git-branch main \
  --build-pack nixpacks \
  --ports-exposes 3000

# Deploy
coolify deploy name <app-name>
coolify deploy uuid <app-uuid>
coolify deploy batch app1,app2,app3

# Status
coolify deploy list
coolify deploy get <deploy-uuid>
coolify app get <app-uuid>
coolify app logs <app-uuid> --lines 50

# Variáveis
coolify app env list <app-uuid>
coolify app env create <app-uuid> --key KEY --value VALUE
coolify app env sync <app-uuid> --file .env
```

---

## 9. Checklist por Tipo de Repositório

### Repositório Público

- [ ] URL HTTPS do repositório copiada
- [ ] Coolify CLI autenticado (se usando CLI)
- [ ] Build pack configurado (nixpacks/dockerfile/static)
- [ ] Porta da aplicação definida
- [ ] Variáveis de ambiente configuradas
- [ ] Domínio configurado (opcional)
- [ ] Deploy executado com sucesso
- [ ] Webhook configurado (para auto deploy)

### Repositório Privado — Deploy Key

- [ ] Chave SSH gerada no Coolify
- [ ] Chave pública adicionada no GitHub (Deploy Keys)
- [ ] URL SSH do repositório copiada (não HTTPS)
- [ ] Build pack configurado
- [ ] Porta da aplicação definida
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy executado com sucesso
- [ ] Webhook configurado (para auto deploy)

### Repositório Privado — GitHub App

- [ ] GitHub App criado no Coolify
- [ ] App registrado no GitHub
- [ ] Client Secret gerado e anotado
- [ ] Private Key (.pem) baixada e adicionada no Coolify
- [ ] App instalado no GitHub (selecionar repos)
- [ ] Source ID, App ID, Installation ID, Client ID anotados
- [ ] GitHub App configurado no Coolify (Sync Name = sucesso)
- [ ] Repositório selecionado na criação do recurso
- [ ] Build pack configurado
- [ ] Porta da aplicação definida
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy executado com sucesso
- [ ] Preview Deployments configurado (opcional)

---

**Próximo passo**: Escolher o tipo de repositório e seguir o passo a passo correspondente
