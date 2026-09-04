# BMAD Method — Desarrollo Ágil con Inteligencia Artificial

![Versión](https://img.shields.io/badge/version-6.11.0-blue)
![Skills](https://img.shields.io/badge/skills-57-green)
![CrewAI](https://img.shields.io/badge/CrewAI-1.15.18-purple)
![Coolify](https://img.shields.io/badge/Coolify-4.3.14-orange)
![Licencia](https://img.shields.io/badge/license-MIT-yellow)

**Idiomas:** [English](README.md) | [Português Brasil](README.pt-BR.md) | Español

---

## Resumen

BMAD Method (Breakthrough Method for Agile Development) es un framework de desarrollo impulsado por IA que integra agentes especializados y skills en su flujo de trabajo. Este proyecto proporciona un ambiente completo para desarrollo ágil con asistentes de IA, con soporte de **deploy mediante Coolify** para infraestructura PaaS self-hosted.

**Características Principales:**
- 57 skills especializadas para diferentes tareas de desarrollo
- 4 agentes específicos por tecnología (Docker, Python 3.14, PHP 8.4, PostgreSQL 18)
- Integración con IDEs OpenCode y Claude Code
- Scripts automatizados de validación y renderización
- Compresión de tokens mediante RTK
- **Integración CrewAI** para orquestación de múltiples agentes
- **Guías de deploy Coolify** y scripts de automatización

---

## Primeros Pasos (empiece aquí)

Si usted es un miembro del equipo que va a usar este repositorio para **implementar
un proyecto nuevo** o para **modernizar/actualizar uno heredado**, siga primero la
guía de onboarding:

**➡️ [`_bmad-output/getting-started.md`](_bmad-output/getting-started.md)**

Pre-flight (hágalo una vez, en este orden):

| # | Paso | Comando |
|---|------|---------|
| 0 | Instalar toolchain + ambos agentes | `./_bmad-output/scripts/install-linux.sh --project-dir "$PWD"` |
| 1 | Obtener el repo + rama de trabajo | `git clone … && cd … && git checkout -b feat/setup` |
| 2 | Instalar/actualizar BMAD | `npx bmad-method install` |
| 3 | Verificar toolchain, ambos agentes y RTK | `diff -rq .agents/skills .claude/skills && rtk init --show` |
| 4 | Configurar el proyecto | editar `_bmad/custom/config.toml` + `_bmad/config.user.toml` |
| 5 | Abrir un agente y orientarse | `opencode` o `claude` → `/bmad-help` |

Luego elija la vía:

| Vía | Cuándo | Adónde va |
|-----|--------|-----------|
| **A — Proyecto nuevo (greenfield)** | aún no hay código | `/bmad-help` → ciclo de vida de 5 fases |
| **B — Proyecto heredado (brownfield)** | base de código a modernizar | `/bmad-project-context` → `/bmad-code-review` → `/bmad-build` |

### Paso a paso detallado (cualquier nivel de conocimiento)

Para una guía **totalmente documentada y sin jerga** de ambas vías — conceptos,
comandos exactos, entradas/salidas esperadas, controles de calidad y solución de
problemas — use el **Manual de Implementación**. Está escrito para miembros del
equipo **sin importar su formación en Ingeniería de Software**:

**➡️ [`_bmad-output/implementation-playbook.md`](_bmad-output/implementation-playbook.md)** — *en portugués (PT-BR)*

| Guía | Úsela para |
|------|-----------|
| [`getting-started.md`](_bmad-output/getting-started.md) | Orientación de 5 min + pre-flight + selector de vía |
| [`implementation-playbook.md`](_bmad-output/implementation-playbook.md) | **El paso a paso detallado para proyecto nuevo o heredado (Partes A y B), glosario, Definition of Done, FAQ** |
| [`bmad-project-lifecycle-guide.md`](_bmad-output/bmad-project-lifecycle-guide.md) | Referencia del operador: las 5 fases y la rutina diaria |

---

## Inicio Rápido

### Prerrequisitos

| Herramienta | Versión Mínima | Propósito |
|-------------|----------------|-----------|
| Node.js | >= 20.12 | Runtime JavaScript |
| Python | >= 3.10, < 3.14 | Ejecución de scripts |
| uv | >= 0.12 | Gestor de paquetes Python |
| Git | Cualquier | Control de versiones |
| GitHub CLI (`gh`) | Cualquier | Operaciones de repositorio / PR / release |
| RTK | >= 0.47 | Compresión de tokens para ambos agentes (opcional) |
| ripgrep | >= 14.0 | Búsqueda rápida, dependencia de RTK (recomendado) |
| CrewAI | >= 1.15 | Orquestación de agentes (opcional) |
| Agente de codificación | — | OpenCode >= 1.18 y/o Claude Code >= 2.1 |

> Todas las herramientas anteriores funcionan desde **ambos** agentes, OpenCode
> y Claude Code. Vea [Agentes de Codificación](#agentes-de-codificación).

### Instalación Automatizada

```bash
# Linux (Ubuntu/Debian)
chmod +x _bmad-output/scripts/install-linux.sh
./_bmad-output/scripts/install-linux.sh

# Windows (PowerShell como Administrador)
powershell -ExecutionPolicy Bypass -File _bmad-output/scripts/install-windows.ps1
```

### Instalación Manual

```bash
# Instalar BMAD Method (regenera los dos árboles de skills + comandos OpenCode)
npx bmad-method install

# Conectar RTK a ambos agentes (por máquina)
rtk init -g --auto-patch --opencode

# Iniciar cualquiera de los agentes — los comandos BMAD son idénticos
opencode        # o: claude

# En el agente elegido
/bmad-help
```

---

## Agentes de Codificación

Este proyecto está configurado para **dos agentes de codificación intercambiables**.
Cada skill, comando y herramienta funciona igual en ambos.

| Aspecto | OpenCode | Claude Code |
|---------|----------|-------------|
| Instrucciones | `AGENTS.md` | `CLAUDE.md` (importa `AGENTS.md`) |
| Skills (57) | `.agents/skills/` + `.opencode/commands/*.md` | `.claude/skills/` (descubrimiento nativo) |
| Invocación | `/bmad-help`, `/bmad-build`, … | `/bmad-help`, `/bmad-build`, … |
| Allow-list de herramientas | `PATH` del shell | `.claude/settings.json` → `permissions.allow` |
| Compresión de tokens RTK | `~/.config/opencode/plugins/rtk.ts` | hook `PreToolUse` en `.claude/settings.json` (`rtk hook claude`) |
| Referencia RTK | — | `.claude/RTK.md` |

`.agents/skills/` y `.claude/skills/` se mantienen idénticas byte a byte;
`npx bmad-method install` regenera ambas. Un comando conecta RTK a los dos
agentes en una máquina nueva: `rtk init -g --auto-patch --opencode`.

---

## Estructura del Proyecto

```
/home/hsantos/app/
├── .agents/skills/          # 57 skills BMAD (OpenCode)
├── .claude/                 # Integración Claude Code
│   ├── skills/              # 57 skills BMAD (espejo idéntico)
│   ├── settings.json        # allow-list de herramientas + hook RTK PreToolUse
│   └── RTK.md               # referencia de comandos RTK para el agente
├── .opencode/commands/      # 57 wrappers de comando OpenCode
├── .git/                    # Repositorio Git
├── AGENTS.md                # Instrucciones OpenCode
├── CLAUDE.md                # Instrucciones Claude Code (importa AGENTS.md)
├── _bmad/                   # Framework BMAD
│   ├── _config/             # Manifests y configs
│   ├── core/                # Skills core
│   ├── bmm/                 # Skills BMM
│   ├── scripts/             # Scripts Python
│   ├── config.toml          # Config principal
│   └── config.user.toml     # Config del usuario
├── _bmad-output/            # Artefactos de implementación
│   ├── getting-started.md               # Primeros pasos / onboarding (nuevo + heredado)
│   ├── implementation-playbook.md       # Paso a paso detallado, cualquier nivel (Partes A y B)
│   ├── bmad-project-lifecycle-guide.md  # Guía completa del ciclo de vida
│   ├── coolify-deploy-guide.md         # Resumen del deploy Coolify
│   ├── coolify-github-deploy-guide.md  # Deploy vía GitHub
│   ├── coolify-local-deploy-guide.md   # Deploy local (sin Git)
│   ├── crewai-integration-guide.md     # Integración CrewAI + BMAD
│   ├── docker-skill-implementation.md  # Docs del agente Docker
│   ├── php84-skill-implementation.md   # Docs del agente PHP 8.4
│   ├── postgres18-skill-implementation.md  # Docs PostgreSQL 18
│   ├── project-replication-guide.md    # Guía completa de setup
│   ├── python314-skill-implementation.md   # Docs Python 3.14
│   ├── rtk-installation-guide.md       # Setup del RTK
│   ├── tools-registry.md              # Inventario de herramientas
│   └── scripts/
│       ├── coolify-deploy.sh           # Automatización de deploy Coolify
│       ├── install-linux.sh            # Instalación Linux
│       ├── install-windows.ps1         # Instalación Windows
│       └── ...
├── docs/                    # Conocimiento del proyecto
└── README.md                # Este archivo
```

---

## Skills BMAD (57 Total)

### Skills Core (24)

| Skill | Propósito |
|-------|-----------|
| `bmad-help` | Orientar en el workflow, obtener recomendaciones |
| `bmad-build` | Implementación principal de código |
| `bmad-build-auto` | Loop de build autónomo |
| `bmad-brainstorming` | Ideación y exploración creativa |
| `bmad-forge-idea` | Probar ideas bajo presión |
| `bmad-create-prd` | Documento de requisitos del producto |
| `bmad-architecture` | Diseño de arquitectura del sistema |
| `bmad-ux` | Patrones UX y specs de diseño |
| `bmad-create-epics-and-stories` | Dividir trabajo en stories |
| `bmad-sprint-planning` | Preparación del sprint |
| `bmad-code-review` | Review adversarial de código |
| `bmad-retrospective` | Retrospectiva del épico |
| `bmad-docker` | Contenedorización Docker |
| `bmad-python314` | Funcionalidades Python 3.14 |
| `bmad-php84` | Funcionalidades PHP 8.4 |
| `bmad-postgres18` | Funcionalidades PostgreSQL 18 |
| ... | y más |

### Agentes de Tecnología (4)

| Agente | Skills | Enfoque |
|--------|--------|---------|
| `bmad-agent-docker` | 1 | Contenedorización, Dockerfile, Compose |
| `bmad-agent-python314` | 1 | Free-threading, t-strings, subinterpreters |
| `bmad-agent-php84` | 3 | Arch-PHP, CodeRefactor-PHP, WebSec-PHP |
| `bmad-agent-postgres18` | 5 | DDL, OPT, VEC, CONC, SEC |

---

## Fases del Workflow BMAD

1. **Clarify** — `bmad-help`, `bmad-brainstorming`, `bmad-forge-idea`
2. **Plan** — `bmad-create-prd`, `bmad-architecture`, `bmad-ux`, `bmad-create-epics-and-stories`
3. **Build** — `bmad-build`, `bmad-build-auto`
4. **Review** — `bmad-code-review`, `bmad-checkpoint-preview`
5. **Learn** — `bmad-retrospective`

Los cambios pequeños pueden saltar directamente al build. Los trabajos complejos siguen el camino completo.

---

## Integración CrewAI

Este proyecto incluye **CrewAI** para orquestación de múltiples agentes, permitiendo flujos de trabajo automatizados.

### ¿Qué es CrewAI?

CrewAI es un framework Python open-source para orquestar agentes de IA autónomos con roles definidos. Proporciona:

- **Crews**: Equipos de agentes con roles, objetivos, herramientas y tareas
- **Flows**: Workflows orientados por eventos con gestión de estado
- **Patrones listos para producción**: Human-in-the-loop, ejecución asíncrona, checkpointing

### Inicio Rápido con CrewAI

```bash
# Instalar CrewAI (si aún no está instalado)
uv tool install crewai

# Crear nuevo proyecto CrewAI
crewai create crew bmad-project

# Navegar al proyecto e instalar dependencias
cd bmad-project
crewai install

# Ejecutar el crew
crewai run
```

### Bridge BMAD-CrewAI

```python
from bmad_crewai_bridge import BMADBridge

bridge = BMADBridge(project_root="/home/hsantos/app")
skills = bridge.list_skills()
output = bridge.render_skill("bmad-docker")
```

Vea la guía completa en `_bmad-output/crewai-integration-guide.md`.

---

## Deploy mediante Coolify

Deploy self-hosted usando **Coolify v4.3.14**. Deploy de aplicaciones mediante repositorios Git o localmente sin Git.

### Métodos de Deploy

| Método | Fuente | Auth | Mejor Para |
|--------|--------|------|------------|
| **Repositorio Público** | URL HTTPS Git | Ninguno | Proyectos open source |
| **Deploy Key** | URL SSH Git | Llave SSH | Repo privado único |
| **GitHub App** | Git (multi-repo) | OAuth + Webhook | Equipos, múltiples repos |
| **Imagen Docker** | Registry (Docker Hub/GHCR) | Ninguno/Token | Imágenes pre-construidas |
| **Dockerfile** | Pegado en UI de Coolify | Ninguno | Apps simples sin Git |
| **Docker Compose Empty** | Pegado en UI de Coolify | Ninguno | Stacks multi-servicio |
| **Service One-Click** | Templates de Coolify | Ninguno | Apps populares (300+) |

### Deploy Rápido vía CLI

```bash
# Instalar CLI de Coolify
curl -fsSL https://raw.githubusercontent.com/coollabsio/coolify-cli/main/scripts/install.sh | bash

# Configurar contexto
coolify context add -d production https://coolify.sudominio.com <TOKEN>

# Deploy de repo Git público
./_bmad-output/scripts/coolify-deploy.sh \
  --name mi-app \
  --repo https://github.com/usuario/repo \
  --port 3000

# Deploy de imagen Docker
./_bmad-output/scripts/coolify-deploy.sh \
  --name nginx \
  --docker-image nginx:alpine \
  --port 80
```

### Guías

- **Resumen**: `_bmad-output/coolify-deploy-guide.md` (12 secciones, 26K)
- **Repos GitHub**: `_bmad-output/coolify-github-deploy-guide.md` (9 secciones, 18.5K)
- **Deploy local**: `_bmad-output/coolify-local-deploy-guide.md` (10 secciones, 18.8K)

---

## Stack Tecnológica

### Agente Docker

- **Validación Dockerfile**: 15 reglas (D001-D015)
- **Validación Compose**: 7 reglas (C001-C007)
- **Optimización BuildKit**: Builds multi-stage
- **Hardening de seguridad**: Usuarios non-root, filesystem read-only

### Agente Python 3.14

- **Free-threading**: Modo No-GIL para paralelismo real
- **Subinterpreters**: Ambientes de ejecución aislados
- **t-strings**: Interpolación de strings con tipos
- **compression.zstd**: Soporte built-in a Zstandard

### Agente PHP 8.4

- **Property Hooks**: Hooks get/set reemplazando boilerplate
- **Asymmetric Visibility**: Patrones `public private(set)`
- **DOM API**: Parsing HTML5 nativo
- **Array Functions**: `array_find`, `array_any`, `array_all`

### Agente PostgreSQL 18

- **AIO**: `io_method = io_uring` para 3x de performance
- **B-Tree Skip Scan**: Optimización de índice multi-columna
- **UUIDv7**: Primary keys ordenadas
- **pgvector**: Indexación HNSW, búsqueda híbrida

---

## Scripts de Instalación

| Script | Sistema | Uso |
|--------|---------|-----|
| `install-linux.sh` | Ubuntu/Debian | `./install-linux.sh --project-dir /ruta` |
| `install-windows.ps1` | Windows 10/11 | `powershell -ExecutionPolicy Bypass -File install-windows.ps1` |

Vea `_bmad-output/scripts/README.md` para instrucciones detalladas.

---

## Documentación

### Documentación Principal

| Documento | Ubicación | Descripción |
|-----------|-----------|-------------|
| **Primeros Pasos** | `_bmad-output/getting-started.md` | **Primeros pasos antes de un proyecto nuevo o una modernización de heredado — pre-flight + vías A/B** |
| **Manual de Implementación** | `_bmad-output/implementation-playbook.md` | **Paso a paso detallado y sin jerga para proyecto nuevo O heredado — conceptos, comandos, controles de calidad, FAQ (cualquier nivel)** |
| **Guía del Ciclo de Vida** | `_bmad-output/bmad-project-lifecycle-guide.md` | **Paso a paso completo: 5 fases de la idea a producción** |
| AGENTS.md / CLAUDE.md | `/AGENTS.md`, `/CLAUDE.md` | Instrucciones del proyecto (OpenCode / Claude Code) |
| Registro de Herramientas | `_bmad-output/tools-registry.md` | Inventario de herramientas (v1.3.1) |
| Guía de Replicación | `_bmad-output/project-replication-guide.md` | Guía completa de setup (v1.1.0) |
| Integración CrewAI | `_bmad-output/crewai-integration-guide.md` | Integración CrewAI + BMAD |

### Agentes de Tecnología

| Documento | Ubicación | Descripción |
|-----------|-----------|-------------|
| Implementación Docker | `_bmad-output/docker-skill-implementation.md` | Docs del agente Docker |
| Python 3.14 | `_bmad-output/python314-skill-implementation.md` | Docs Python 3.14 |
| PHP 8.4 | `_bmad-output/php84-skill-implementation.md` | Docs PHP 8.4 |
| PostgreSQL 18 | `_bmad-output/postgres18-skill-implementation.md` | Docs PostgreSQL 18 |
| Instalación RTK | `_bmad-output/rtk-installation-guide.md` | Setup del RTK |

### Deploy Coolify

| Documento | Ubicación | Descripción |
|-----------|-----------|-------------|
| Guía de Deploy | `_bmad-output/coolify-deploy-guide.md` | Resumen, preparación, CLI (12 secciones) |
| Deploy GitHub | `_bmad-output/coolify-github-deploy-guide.md` | Repo público, Deploy Key, GitHub App (9 secciones) |
| Deploy Local | `_bmad-output/coolify-local-deploy-guide.md` | Docker Image, Dockerfile, Compose Empty (10 secciones) |
| Script de Deploy | `_bmad-output/scripts/coolify-deploy.sh` | Automatización CLI (Git + Docker Image) |

---

## Ejemplos de Uso

### Iniciar un Nuevo Proyecto

```bash
# Clonar el repositorio
git clone https://github.com/usuario/su-repo.git
cd su-repo

# Ejecutar script de instalación (instala ambos agentes + conecta RTK a ambos)
chmod +x _bmad-output/scripts/install-linux.sh
./_bmad-output/scripts/install-linux.sh

# Iniciar cualquiera de los agentes
opencode        # o: claude

# En el agente elegido
/bmad-help
```

### Ciclo de Vida Completo (Recomendado)

Para nuevos proyectos, siga el **ciclo de vida de 5 fases** documentado en la guía:

| Fase | Skills | Duración | Salida |
|------|--------|----------|--------|
| **1. Clarify** | `bmad-help` → `bmad-brainstorming` → `bmad-forge-idea` | 30 min | Idea validada |
| **2. Plan** | `bmad-create-prd` → `bmad-architecture` → `bmad-ux` → `bmad-create-epics-and-stories` | 1-2h | PRD + Arquitectura + UX + Stories |
| **3. Build** | `bmad-build` (por story) | Variable | Código funcional |
| **4. Review** | `bmad-code-review` → `bmad-qa-generate-e2e-tests` | 30 min | Código validado |
| **5. Learn** | `bmad-retrospective` → Deploy en Coolify | 30 min | Lecciones aprendidas + Producción |

**📖 Guía completa:** `_bmad-output/bmad-project-lifecycle-guide.md`

### Referencia Rápida: Todas las Fases

```
/bmad-help              → Comience aquí, obtenga orientación
/bmad-brainstorming     → Sesión de ideación estructurada
/bmad-forge-idea        → Pruebe su idea bajo presión
/bmad-create-prd        → Crear Documento de Requisitos del Producto
/bmad-architecture      → Definir spine de arquitectura
/bmad-ux                → Crear DESIGN.md + EXPERIENCE.md
/bmad-create-epics-and-stories → Dividir trabajo en stories rastreables
/bmad-sprint-planning   → Planificar ejecución del sprint
/bmad-build             → Implementar código (una story a la vez)
/bmad-build-auto        → Loop de build autónomo
/bmad-code-review       → Review adversarial de código
/bmad-retrospective     → Retrospectiva del épico con evidencias
```

### Usar Agentes de Tecnología

```
# Tareas Docker
/bmad-docker
/bmad-agent-docker

# Tareas Python 3.14
/bmad-python314
/bmad-agent-python314

# Tareas PHP 8.4
/bmad-php84
/bmad-agent-php84

# Tareas PostgreSQL 18
/bmad-postgres18
/bmad-agent-postgres18
```

---

## Configuración

### Config Principal

`_bmad/config.toml` — Administrado por el instalador, no editar directamente.

### Config del Equipo

`_bmad/custom/config.toml` — Overrides del equipo, commiteado en el repo.

### Config del Usuario

`_bmad/config.user.toml` — Configuraciones personales, en gitignore.

### Config de los Agentes de Codificación

| Archivo | Agente | Commiteado | Propósito |
|---------|--------|------------|-----------|
| `AGENTS.md` | OpenCode | ✅ | Instrucciones del proyecto |
| `CLAUDE.md` | Claude Code | ✅ | Punto de entrada; importa `AGENTS.md` |
| `.claude/settings.json` | Claude Code | ✅ | Allow-list de herramientas + hook RTK `PreToolUse` |
| `.claude/RTK.md` | Claude Code | ✅ | Referencia de comandos RTK |
| `~/.config/opencode/plugins/rtk.ts` | OpenCode | local de la máquina | Plugin RTK |

---

## Actualización

```bash
# Actualizar BMAD Method
npx bmad-method install

# Actualizar herramientas
npm update -g opencode @anthropic-ai/claude-code
```

---

## Soporte

- **Documentación**: Vea `_bmad-output/` para guías detalladas
- **Issues**: Abra una issue en el repositorio del proyecto
- **BMAD Method**: https://github.com/bmadmethod/bmad-method

---

## Licencia

Licencia MIT — Vea `_bmad/core/config.yaml` para detalles.

---

## Contribuidores

- **Hsantos** — Mantenedor del proyecto
- **BMAD Method** — Autores del framework
