# Docker Agent & Skill — Documentação da Implementação

**Data:** 2026-09-03
**Status:** Implementado e Validado
**Versão:** 1.0.0

---

## Resumo

Implementação completa de um **Docker Agent** (persona especializada) e uma **Docker Skill** (capacidade técnica) para o framework BMAD Method. O sistema inclui:

- **Docker Skill** (`bmad-docker`): Geração, validação e manutenção de Dockerfiles e docker-compose
- **Docker Agent** (`bmad-agent-docker`): Persona Docker Architect com menu interativo
- **3 Scripts Python** nativos: Validação Dockerfile, validação Compose, DocSync
- **15 regras de validação** hadolint-like implementadas em Python puro
- **8 templates** padronizados para diferentes stacks
- **Mecanismo DocSync**: Cache local + fetch sob demanda de docs.docker.com

---

## Arquivos Criados

### Docker Skill

| Caminho | Descrição |
|---------|-----------|
| `.agents/skills/bmad-docker/SKILL.md` | Ponto de entrada da skill |
| `.agents/skills/bmad-docker/customize.toml` | Configuração de customização |
| `.agents/skills/bmad-docker/workflow.md` | Workflow principal (6 fases) |
| `.agents/skills/bmad-docker/references/docker-rules.md` | 15 regras de validação detalhadas |
| `.agents/skills/bmad-docker/references/templates.md` | 8 templates (Node, Python, Go, Rust, Java, React, Compose Full Stack, Compose Dev) |

### Docker Agent

| Caminho | Descrição |
|---------|-----------|
| `.agents/skills/bmad-agent-docker/SKILL.md` | Ativação do agente com persona |
| `.agents/skills/bmad-agent-docker/customize.toml` | Persona, menu (7 itens), principles, persistent_facts |

### Scripts Python

| Caminho | Descrição | Regras |
|---------|-----------|--------|
| `_bmad/scripts/validate_dockerfile.py` | Validador Dockerfile | D001-D015 (15 regras) |
| `_bmad/scripts/validate_compose.py` | Validador Compose | C001-C007 (7 regras) |
| `_bmad/scripts/docsync_docker.py` | Sincronização de docs | Cache TTL 14 dias |

### Comandos OpenCode

| Caminho | Descrição |
|---------|-----------|
| `.opencode/commands/bmad-docker.md` | Comando para Docker Skill |
| `.opencode/commands/bmad-agent-docker.md` | Comando para Docker Agent |

### Espelhamento Claude Code

Todos os arquivos da skill e agent foram espelhados em `.claude/skills/bmad-docker/` e `.claude/skills/bmad-agent-docker/`.

---

## Regras de Validação Implementadas

### Dockerfile (D001-D015)

| ID | Severidade | Regra |
|----|------------|-------|
| D001 | ERROR | Syntax pragma obrigatório (`# syntax=docker/dockerfile:1`) |
| D002 | ERROR | MAINTAINER obsoleto → usar `LABEL maintainer=` |
| D003 | WARNING | FROM sem tag de versão |
| D004 | WARNING | FROM com tag `:latest` |
| D005 | INFO | CMD em shell form ao invés de exec form |
| D006 | WARNING | apt-get install sem limpeza de lists |
| D007 | INFO | Falta `--no-install-recommends` |
| D008 | ERROR | ADD ao invés de COPY |
| D009 | WARNING | Falta USER não-root |
| D010 | INFO | Falta HEALTHCHECK |
| D011 | WARNING | Gerenciador de pacotes sem cache mount |
| D012 | WARNING | Múltiplos RUNs consecutivos |
| D013 | WARNING | npm install sem cache mount |
| D014 | WARNING | pip install sem cache mount |
| D015 | WARNING | Falta .dockerignore |

### Compose (C001-C007)

| ID | Severidade | Regra |
|----|------------|-------|
| C001 | ERROR | Campo `version` obsoleto |
| C002 | INFO | Nome de arquivo legado (docker-compose.yml) |
| C003 | INFO | CLI legado (docker-compose com hífen) |
| C004 | WARNING | `links` deprecado → usar `networks` |
| C005 | INFO | `depends_on` sem `condition` |
| C006 | WARNING | Dependência sem healthcheck |
| C007 | WARNING | Sem limites de recursos |

---

## Templates Disponíveis

| Template | Stack | Estágios | Tamanho |
|----------|-------|----------|---------|
| A | Node.js (Express/Nest) | 3 (deps, build, runtime) | ~210MB |
| B | Python (FastAPI/Django) | 2 (wheels, runtime) | ~120MB |
| C | Go (Gin/Echo) | 2 (builder, distroless) | ~2MB |
| D | Rust (Axum/Actix) | 2 (builder, distroless) | ~5MB |
| E | Java (Spring Boot) | 2 (jdk, jre) | ~180MB |
| F | React/Nginx (SPA) | 2 (build, serve) | ~25MB |
| G | Compose Full Stack | app + db + redis | — |
| H | Compose Development | dev com watch | — |

---

## Menu do Docker Agent

| Code | Descrição | Ação |
|------|-----------|------|
| `DF` | Criar ou refatorar Dockerfile | bmad-docker |
| `DC` | Criar ou refatorar docker-compose | bmad-docker |
| `VL` | Validar Dockerfile/Compose | bmad-docker |
| `DS` | DocSync — verificar docs | bmad-docker |
| `SC` | Security scan (Scout/Trivy) | prompt direto |
| `MB` | Multi-platform build (Buildx) | prompt direto |
| `OP` | Otimizar imagem existente | bmad-docker |

---

## Uso dos Scripts

### Validação de Dockerfile

```bash
# Validar arquivo específico
python3 _bmad/scripts/validate_dockerfile.py Dockerfile

# Validar com formato JSON
python3 _bmad/scripts/validate_dockerfile.py Dockerfile --format json

# Modo estrito (warnings viram errors)
python3 _bmad/scripts/validate_dockerfile.py Dockerfile --strict

# Validar todos os Dockerfiles do projeto
python3 _bmad/scripts/validate_dockerfile.py --check-project
```

### Validação de Compose

```bash
# Validar compose.yaml
python3 _bmad/scripts/validate_compose.py compose.yaml

# Validar todos os compose files do projeto
python3 _bmad/scripts/validate_compose.py --check-project
```

### DocSync

```bash
# Verificar se cache está fresco
python3 _bmad/scripts/docsync_docker.py --check

# Atualizar cache (busca docs.docker.com)
python3 _bmad/scripts/docsync_docker.py --refresh

# Ver status do cache
python3 _bmad/scripts/docsync_docker.py --status

# Validar arquivo contra docs cached
python3 _bmad/scripts/docsync_docker.py --validate Dockerfile
```

---

## Integração com BMAD

### Comandos OpenCode

```bash
# Invocar Docker Skill
bmad-docker

# Invocar Docker Agent
bmad-agent-docker
```

### Renderização de Skill

```bash
uv run _bmad/scripts/render_skill.py --project-root /home/hsantos/app --skill .claude/skills/bmad-docker
```

---

## Dependências

### Obrigatórias

- **Python** >= 3.10
- **uv** (para renderização de skills)

### Opcionais

- **PyYAML** (`pip install pyyaml`) — Validação completa de Compose (sem ele, usa fallback text-based)
- **requests** (`pip install requests`) — DocSync para buscar docs.docker.com (sem ele, cache não funciona)

---

## Atualizações Futuras

1. **Integração Hadolint**: Wrapper opcional para hadolint nativo
2. **Docker Scout integration**: Scan automático de CVEs via CLI
3. **Buildx Bake templates**: Templates para docker-bake.hcl
4. **CI/CD templates**: GitHub Actions e GitLab CI para Docker
5. **Kubernetes manifests**: Geração de deployment.yaml a partir do compose
6. **SBOM generation**: Integração com `docker buildx --sbom=true`
7. **Atualização automática do cache DocSync**: Cron job ou hook de build

---

## Estatísticas da Implementação

| Métrica | Valor |
|---------|-------|
| Total de arquivos criados | 22 |
| Skills novas | 2 (bmad-docker, bmad-agent-docker) |
| Scripts Python | 3 |
| Regras de validação | 22 (15 Dockerfile + 7 Compose) |
| Templates | 8 |
| Linhas de código (scripts) | ~850 |
| Documentação | ~400 linhas |
