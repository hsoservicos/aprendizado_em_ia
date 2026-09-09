# Guia Python 3.14 — Virtual Environments para Projetos Novos

**Versão**: 1.0.0
**Data**: 2026-09-09
**Autor**: Hsantos
**Público-alvo**: Desenvolvedores que vão iniciar projetos novos com Python 3.14 neste repositório.

---

## 1. Visão Geral

Python 3.14 é a versão estável atual (LTS até outubro de 2030). Este guia
explica como criar e gerenciar **virtual environments** (venvs) isolados para
cada projeto novo, garantindo:

- **Isolamento de dependências** — cada projeto tem suas próprias bibliotecas
- **Reprodutibilidade** — qualquer pessoa pode recriar o ambiente exato
- **Segurança** — system Python intocado, sem `sudo pip install` global
- **Modernidade** — acesso a t-strings, free-threading, subinterpreters

### Fluxo Rápido (2 comandos)

```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

Pronto. A partir daqui, todo `pip install` vai apenas para este projeto.

---

## 2. Pré-requisitos

| Ferramenta | Versão Mínima | Verificar | Instalar |
|------------|---------------|-----------|----------|
| Python 3.14 | 3.14.x | `python3.14 --version` | Deadsnakes PPA (já instalado) |
| pip | bundled | `python3.14 -m pip --version` | Incluído no venv |
| Git | >= 2.30 | `git --version` | `sudo apt install git` |

### Verificar Ambiente

```bash
# Python 3.14 disponível?
python3.14 --version
# Saída esperada: Python 3.14.6

# venv funcional?
python3.14 -m venv --help >/dev/null 2>&1 && echo "OK" || echo "FALHOU"
# Saída esperada: OK
```

---

## 3. Criando um Virtual Environment

### 3.1 Estrutura Recomendada

```
projetos/
├── projeto-a/
│   ├── .venv/          ← venv (NUNCA commitar)
│   ├── src/
│   ├── requirements.txt
│   └── .gitignore
└── projeto-b/
    ├── .venv/
    ├── pyproject.toml
    └── .gitignore
```

### 3.2 Comandos de Criação

```bash
# Navegue até o diretório do projeto
cd ~/projetos/meu-projeto

# Crie o venv (nome padrão: .venv)
python3.14 -m venv .venv

# Ou com nome personalizado
python3.14 -m venv ~/venvs/meu-projeto
```

### 3.3 O que é Criado

```
.venv/
├── bin/                ← executáveis (python, pip, activate)
├── lib/
│   └── python3.14/
│       └── site-packages/  ← pacotes instalados aqui
├── include/
├── pyvenv.cfg          ← configuração do venv
└── .gitignore         ← auto-gerado pelo Python 3.14
```

**Python 3.14 automaticamente cria `.gitignore` dentro do venv**, impedindo
que ele seja commitado acidentalmente.

---

## 4. Ativação e Desativação

### 4.1 Ativação

| Sistema | Comando |
|---------|---------|
| **Linux / macOS** | `source .venv/bin/activate` |
| **Windows (cmd)** | `.venv\Scripts\activate` |
| **Windows (PowerShell)** | `.venv\Scripts\Activate.ps1` |
| **fish** | `source .venv/bin/activate.fish` |

### 4.2 Confirmação

Após ativação, o prompt mostra o nome do venv:

```
(.venv) usuario@host:~/projetos/meu-projeto$
```

Verifique que está no venv correto:

```bash
which python
# Saída: /home/usuario/projetos/meu-projeto/.venv/bin/python

python --version
# Saída: Python 3.14.6
```

### 4.3 Desativação

```bash
deactivate
```

O prompt volta ao normal. Nenhuma alteração permanente é feita.

### 4.4 Atalho: Executar sem Ativar

```bash
# Instalar pacotes sem ativar
.venv/bin/pip install requests

# Rodar scripts sem ativar
.venv/bin/python meuscript.py

# Útil para CI/CD, cron jobs, Docker
```

---

## 5. Gerenciando Dependências

### 5.1 Instalar Pacotes

```bash
# Ativar o venv primeiro
source .venv/bin/activate

# Atualizar pip (recomendado em todo venv novo)
python -m pip install --upgrade pip

# Instalar pacotes
pip install requests fastapi uvicorn

# Instalar versão específica
pip install "django>=4.2,<5.0"

# Instalar de um arquivo
pip install -r requirements.txt
```

### 5.2 Exportar Dependências

```bash
# Gerar requirements.txt com versões exatas
pip freeze > requirements.txt
```

Exemplo de `requirements.txt`:

```
fastapi==0.115.0
uvicorn==0.30.0
requests==2.32.3
pydantic==2.9.0
```

### 5.3 Recriar Ambiente (em outra máquina)

```bash
# Clonar repositório
git clone https://github.com/usuario/projeto.git
cd projeto

# Criar e ativar venv
python3.14 -m venv .venv
source .venv/bin/activate

# Instalar dependências exatas
pip install -r requirements.txt
```

### 5.4 pyproject.toml (Projetos Modernos)

Para projetos que usam `pyproject.toml` em vez de `requirements.txt`:

```bash
# Instilar o projeto em modo desenvolvimento
pip install -e ".[dev]"

# Ou com uv (mais rápido)
uv pip install -e ".[dev]"
```

---

## 6. Novidades Python 3.14

### 6.1 Template Strings (t-strings) — PEP 750

```python
# F-strings existentes
name = "Mundo"
print(f"Olá, {name}!")  # str

# Novas t-strings (retornam Template, não str)
from string.templatelib import Template

template = t"Olá, {name}!"
print(type(template))  # <class 'string.templatelib.Template'>

# Uso prático: sanitização de HTML
def sanitize_html(template):
    """Permite apenas interpolações seguras."""
    return template  # Lógica de sanitização

user_input = "<script>alert('xss')</script>"
safe = sanitize_html(t"Perfil: {user_input}")
```

### 6.2 Free-Threading (sem GIL) — PEP 779

```python
# Python 3.14 suporta execução paralela real
# (requer build com --disable-gil)

import sys
print(sys._is_gil_enabled())  # False no build free-threaded

# Threads Python agora rodam em paralelo real
import threading

def trabalho_cpu(n):
    return sum(i * i for i in range(n))

# Em Python 3.14 free-threaded, isso usa múltiplos cores
threads = [threading.Thread(target=trabalho_cpu, args=(10**7,)) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

### 6.3 Subinterpreters — PEP 734

```python
from concurrent.futures import InterpreterPoolExecutor

def tarefa(n):
    return n * n

# Cada worker roda em seu próprio interpretador Python
with InterpreterPoolExecutor(max_workers=4) as executor:
    resultados = list(executor.map(tarefa, range(10)))
    print(resultados)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

### 6.4 Deferred Annotations — PEP 649/749

```python
# Annotations são avaliadas sob demanda, não na importação
from annotationlib import get_annotations

class MeuModelo:
    nome: str
    idade: int

# Antes (Python < 3.14): annotations eram avaliadas na importação
# Agora: avaliadas apenas quando solicitado
anotacoes = get_annotations(MeuModelo)
print(anotacoes)  # {'nome': <class 'str'>, 'idade': <class 'int'>}
```

### 6.5 Outras Melhorias

| Feature | Descrição |
|---------|-----------|
| `except` sem parânteses | `except ValueError, TypeError:` (PEP 758) |
| `compression.zstd` | Compressão nativa, sem bibliotecas externas |
| REPL melhorado | Syntax highlighting, mensagens de erro mais claras |
| GC incremental | Menos pausas na coleta de lixo |
| JIT experimental | Compilador just-in-time para hot loops |

---

## 7. venv vs uv — Comparação

| Aspecto | venv (stdlib) | uv (Rust) |
|---------|---------------|-----------|
| **Velocidade** | Padrão | 10-100x mais rápido |
| **Instalação** | Já vem com Python | `pip install uv` ou binário standalone |
| **Criação de venv** | `python -m venv .venv` | `uv venv .venv` |
| **Instalar pacotes** | `pip install requests` | `uv pip install requests` |
| **Lock file** | Não (usa requirements.txt) | `uv lock` gera `uv.lock` |
| **Gerenciar Python** | Não | `uv python install 3.14` |
| **Ideal para** | Aprendizado, scripts simples | Projetos novos, CI/CD, produção |

### Quando usar cada um

```
┌─────────────────────────────────────────────────────┐
│  Projeto novo, sem dependências complexas           │
│  → uv (mais rápido, gerencia tudo)                 │
├─────────────────────────────────────────────────────┤
│  Aprendizado, scripts pequenos                      │
│  → venv (padrão, sem instalar nada)                │
├─────────────────────────────────────────────────────┤
│  Projeto existente com requirements.txt            │
│  → venv (compatibilidade total)                    │
├─────────────────────────────────────────────────────┤
│  CI/CD, Docker, automação                          │
│  → uv (velocidade importa)                         │
└─────────────────────────────────────────────────────┘
```

### Exemplo rápido com uv

```bash
# Criar venv
uv venv .venv

# Ativar (mesmo comando)
source .venv/bin/uv

# Instalar (10-100x mais rápido que pip)
uv pip install requests fastapi

# Freeze
uv pip freeze > requirements.txt
```

---

## 8. Boas Práticas

### 8.1 Regras Obrigatórias

| # | Regra | Por quê |
|---|-------|---------|
| 1 | **Um venv por projeto** | Isolamento total de dependências |
| 2 | **Nome `.venv`** | Padrão da indústria, tools detectam automaticamente |
| 3 | **Nunca commitar `.venv/`** | Binários são específicos da máquina |
| 4 | **Sempre commitar `requirements.txt`** | Reprodutibilidade para toda a equipe |
| 5 | **`pip freeze` após cada instalação** | Mantém requirements.txt atualizado |
| 6 | **Recriar, não consertar** | Mais rápido deletar e recriar do que debugar |

### 8.2 .gitignore

```gitignore
# Python virtual environments
.venv/
venv/
__pycache__/
*.pyc

# Distribution
dist/
build/
*.egg-info/

# Environment variables
.env
.env.local
```

### 8.3 Atalhos Úteis

```bash
# Criar venv + ativar + instalar requirements (uma linha)
python3.14 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

# Listar pacotes instalados
pip list

# Verificar versão de um pacote
pip show requests

# Desatualizar um pacote
pip install --upgrade requests

# Remover um pacote
pip uninstall requests

# Buscar pacotes
pip search "web framework"  # (descontinuado, usar pypi.org)
```

---

## 9. Integração com BMAD

### 9.1 Usando com Skills

As skills do BMAD que envolvem Python usam `uv` para renderizar:

```bash
# Renderizar skill Python 3.14
uv run _bmad/scripts/render_skill.py \
  --project-root /home/hsantos/app \
  --skill .claude/skills/bmad-python314

# Renderizar skill Docker (que pode gerar Dockerfiles Python)
uv run _bmad/scripts/render_skill.py \
  --project-root /home/hsantos/app \
  --skill .claude/skills/bmad-docker
```

### 9.2 Dockerfile para Projetos Python 3.14

```dockerfile
FROM python:3.14-slim AS base

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Executar
CMD ["python", "main.py"]
```

### 9.3 pyproject.toml para Novos Projetos

```toml
[project]
name = "meu-projeto"
version = "0.1.0"
description = "Descrição do projeto"
readme = "README.md"
requires-python = ">=3.14"
dependencies = [
    "requests>=2.31",
    "fastapi>=0.115",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "ruff>=0.6",
]

[build-system]
requires = ["setuptools>=75"]
build-backend = "setuptools.build_meta"
```

---

## 10. Solução de Problemas

### Erro: "externally-managed-environment"

```
error: externally-managed-environment
```

**Causa**: Tentou instalar pacotes no Python do sistema.
**Solução**: Crie e ative um venv primeiro.

```bash
python3.14 -m venv .venv
source .venv/bin/activate
pip install <pacote>
```

### Erro: "No module named venv"

```
ModuleNotFoundError: No module named 'venv'
```

**Causa**: Pacote `python3.14-venv` não instalado.
**Solução**:

```bash
sudo apt install python3.14-venv
```

### Erro: "python: command not found" após ativar

**Causa**: Shell não encontrou o script de ativação.
**Solução**: Use caminho absoluto:

```bash
source /home/usuario/projetos/meu-projeto/.venv/bin/activate
```

### Erro: pip instalou no lugar errado

**Causa**: Venv não estava ativado.
**Solução**:

```bash
# Verifique onde está o pip
which pip
# Deve apontar para .venv/bin/pip

# Se não apontar, ative o venv
source .venv/bin/activate
```

### Erro: "No such file or directory" ao ativar

**Causa**: Venv corrompido ou movido.
**Solução**: Recrie o venv:

```bash
rm -rf .venv
python3.14 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Ambiente Perdido — Recriação Completa

```bash
# 1. Salvar dependências atuais (se possível)
pip freeze > requirements.txt

# 2. Deletar venv corrompido
rm -rf .venv

# 3. Recriar do zero
python3.14 -m venv .venv
source .venv/bin/activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Verificar
pip list
```

---

## Referências

| Recurso | URL |
|---------|-----|
| Python 3.14 Docs | https://docs.python.org/3/whatsnew/3.14.html |
| venv Module | https://docs.python.org/3/library/venv.html |
| PEP 750 (t-strings) | https://peps.python.org/pep-0750/ |
| PEP 779 (free-threading) | https://peps.python.org/pep-0779/ |
| PEP 734 (subinterpreters) | https://peps.python.org/pep-0734/ |
| PyPI | https://pypi.org |
| uv Documentation | https://docs.astral.sh/uv/ |

---

**Manutenção**: Este documento deve ser revisado quando novas versões do
Python 3.14.x forem lançadas (patches de segurança) ou quando as tools
do projeto forem atualizadas.
