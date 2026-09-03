# Aprendizado em IA — Engenharia de Software com LLMs via CLI

> Repositório público dedicado a documentar, ensinar e compartilhar boas práticas de Engenharia de Software aplicadas ao desenvolvimento de projetos com Modelos de Linguagem (LLMs) através de interfaces de linha de comando (CLI).

---

## Visao Geral

O uso de LLMs como ferramentas de desenvolvimento de software esta crescendo exponencialmente. Ferramentas como **Claude Code**, **OpenCode**, **Cursor**, **Codex CLI**, **Aider** e **Copilot** transformaram a forma como escrevemos, revisamos e mantemos codigo.

Este repositorio serve como um **hub central de conhecimento** para:

- Equipes que desejam adotar LLMs em seus fluxos de trabalho de Engenharia de Software
- Desenvolvedores individuais que querem maximizar produtividade com agentes de IA
- Comunidades que compartilham aprendizados sobre prompts, workflows e automacoes

---

## Estrutura do Repositorio

```
aprendizado_em_ia/
├── README.md                          # Este arquivo
├── .gitignore                         # Ignorar artefatos desnecessarios
│
├── docs/                              # Documentacao principal
│   ├── guia-inicio-rapido.md          # Primeiros passos com LLMs + CLI
│   ├── arquitetura-agentes.md         # Arquitetura de agentes de IA
│   ├── comparative-tools.md           # Comparativo de ferramentas CLI
│   └── glossario.md                   # Termos e definicoes
│
├── tools/                             # Ferramentas e configuracoes
│   ├── rtk/                           # RTK (Rust Token Killer)
│   │   ├── README.md                  # Documentacao do RTK
│   │   └── config-examples/           # Exemplos de configuracao
│   ├── opencode/                      # Configuracoes OpenCode
│   │   └── plugins/                   # Plugins uteis
│   ├── claude-code/                   # Configuracoes Claude Code
│   └── scripts/                       # Scripts de automacao
│
├── templates/                         # Templates reutilizaveis
│   ├── AGENTS.md                      # Template para agentes
│   ├── .opencode/                     # Template de configuracao OpenCode
│   └── prompts/                       # Prompts prontos para uso
│       ├── code-review.md
│       ├── refactor.md
│       ├── testing.md
│       └── documentation.md
│
├── examples/                          # Exemplos praticos
│   ├── bug-fix/                       # Exemplo: correcao de bug
│   ├── feature-dev/                   # Exemplo: desenvolvimento de feature
│   └── refactor/                      # Exemplo: refatoracao
│
├── workflows/                         # Workflows de automacao
│   ├── sprint-flow.md                 # Fluxo de sprint com agentes
│   ├── code-review-flow.md            # Fluxo de revisao de codigo
│   └── testing-flow.md               # Fluxo de testes automatizados
│
└── _bmad-output/                      # Artefatos gerados por agentes
    └── .gitkeep
```

---

## Topicos Cobertos

### 1. Fundamentos

- O que sao LLMs e como funcionam no contexto de desenvolvimento
- Diferenca entre ChatGPT/Claude web vs. ferramentas CLI integradas
- conceitos de tokens, context window e custo operacional
- Seguranca e boas práticas ao usar IA no codigo

### 2. Ferramentas CLI para Desenvolvimento com IA

| Ferramenta | Tipo | Descricao |
|------------|------|-----------|
| **Claude Code** | Agente CLI | Agente de codigo da Anthropic com execucao nativa |
| **OpenCode** | CLI Framework | Framework extensivel para agentes de IA |
| **Codex CLI** | Agente CLI | Agente da OpenAI para desenvolvimento |
| **Cursor** | IDE + Agent | Editor com IA integrada |
| **Aider** | CLI Pair | Par de programacao via terminal |
| **Copilot** | Plugin | Assistente de codigo da GitHub |

### 3. Otimizacao de Tokens

- Uso do **RTK (Rust Token Killer)** para comprimir saidas de comandos
- Estrategias de filtragem inteligente
- Monitoramento de economia de tokens
- Configuracao de filtros customizados

### 4. Workflows Recomendados

- **Sprint Planning** com agentes de IA
- **Code Review** automatizado e semi-automatizado
- **Testes** assistidos por IA
- **Documentacao** gerada e mantida por agentes
- **Debug** e resolucao de problemas com LLMs

### 5. Boas Praticas

- Prompt engineering para desenvolvimento de software
- Estruturacao de projetos para trabalhar bem com IA
- Versionamento e controle de alteracoes geradas por IA
- Revisao humana como gate de qualidade

---

## Como Contribuir

1. **Fork** este repositorio
2. Crie uma branch para sua contribuicao: `git checkout -b feat/nova-documentacao`
3. Faca suas alteracoes seguindo o padrao do projeto
4. Commit com mensagens claras: `git commit -m "docs: adiciona guia de testes com pytest"`
5. Push e abra um **Pull Request**

### Padroes de Commits

Utilize o padrao [Conventional Commits](https://www.conventionalcommits.org/):

- `docs:` — Alteracoes em documentacao
- `feat:` — Nova funcionalidade ou conteudo
- `fix:` — Correcao de erros
- `refactor:` — Reestruturacao sem alterar funcionalidade
- `test:` — Adicao ou correcao de testes

---

## Pre-requisitos

Para utilizar as ferramentas e templates deste repositorio:

- **Node.js** >= 20.x
- **Python** >= 3.10
- **Git** >= 2.x
- **Rust** (opcional, para RTK via cargo)
- **uv** (gerenciador de pacotes Python rapido)

---

## Recursos Uteis

- [RTK — Rust Token Killer](https://github.com/rtk-ai/rtk) — Compressao de tokens para agentes
- [OpenCode](https://opencode.ai) — Framework CLI para agentes de IA
- [Claude Code](https://docs.anthropic.com/claude-code) — Documentacao oficial
- [BMAD Method](https://github.com/bmad-sim/bmad-method) — Metodologia para agentes de IA

---

## Status

| Modulo | Status | Descricao |
|--------|--------|-----------|
| `docs/` | 🟡 Em construcao | Documentacao sendo estruturada |
| `tools/rtk/` | 🟢 Funcional | RTK configurado e documentado |
| `templates/` | 🟡 Em construcao | Templates em desenvolvimento |
| `examples/` | 🔴 Pendente | Exemplos ainda nao criados |
| `workflows/` | 🟡 Em construcao | Workflows sendo documentados |

---

## Licenca

Este repositorio esta disponibilizado sob a licenca **MIT**. Sinta-se livre para usar, modificar e distribuir.

---

## Contato

- **Autor:** Hsantos
- **GitHub:** [@hsoservicos](https://github.com/hsoservicos)
- **Issues:** [Abrir issue](https://github.com/hsoservicos/aprendizado_em_ia/issues)

---

*Feito com 💜 para a comunidade de desenvolvedores que acreditam no poder da IA como ferramenta de produtividade.*
