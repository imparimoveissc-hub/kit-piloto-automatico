# 22_CLAUDE_DESKTOP — Adaptacao do Kit para Claude Desktop (app)

> **90% dos mentorados vao usar o Claude Desktop (app)**, nao o Claude Code (terminal). Esta pasta garante que o kit funcione 100% no app.

## Por que existe

Claude Code (CLI) tem:
- Slash commands (`/preflight-acessos`)
- `.claude/agents/` (wrappers automaticos)
- Hooks, settings.json, Bash/PowerShell tools
- MCPs via `claude mcp add`

Claude Desktop (app) **NAO tem** nada disso. Em vez disso, tem:
- **Projects** (cada um com system prompt + knowledge + custom instructions)
- **MCPs via `claude_desktop_config.json`** (editado manualmente)
- **Triggers por palavra-chave** (sem `/`)

Esta pasta traduz tudo do Code pro Desktop sem perder funcionalidade.

## Arquivos principais

| Arquivo | Funcao |
|---|---|
| `setup-project.md` | Como criar Project do CoS no Claude Desktop |
| `cos-desktop-system-prompt.md` | System prompt completo do CoS (cola no Project) |
| `custom-instructions.md` | Instructions adicionais pro Project |
| `knowledge-files.md` | Quais arquivos do kit fazer upload no Project |
| `claude-desktop-config.json` | Template de MCPs pro app desktop |
| `commands-keywords.md` | Mapping: comando `/` -> palavra-chave que aciona no Desktop |
| `platform-differences.md` | Code vs Desktop: o que muda na pratica |
| `projects-recommended.md` | Quais Projects criar (nao 1, varios focados) |

## Fluxo recomendado pro mentorado

```text
1. Abrir Claude Desktop
2. Criar Project "Kit Piloto Automatico V30 - CoS"
3. Colar system prompt (copia de `cos-desktop-system-prompt.md`)
4. Upload de arquivos (lista em `knowledge-files.md`)
5. Adicionar custom instructions (copia de `custom-instructions.md`)
6. Configurar MCPs (`claude_desktop_config.json` pro Claude Desktop)
7. Reiniciar app
8. Conversar com o Project como se fosse Claude Code: "preflight acessos", "primeira tarefa", "setup nicho", etc.
```

## Tres Projects recomendados

Em vez de 1 Project gigante, **3 Projects focados** funcionam melhor (cada um com knowledge isolado e system prompt enxuto):

| Project | Foco | Quando usar |
|---|---|---|
| **CoS V30** | Roteador geral, primeira tarefa, setup | Qualquer pedido genérico, comeco do dia |
| **Trafego DR** | Meta Ads, criativos, atribuicao, escala | Quando vai operar campanha paga |
| **WhatsApp + Cowork** | Fluxos WhatsApp, SDR, automacao | Quando vai operar WhatsApp/atendimento |

Detalhes em `projects-recommended.md`.

## Comparativo de funcionalidades

| Funcao | Claude Code | Claude Desktop |
|---|---|---|
| Slash commands `/cmd` | ✅ | ❌ -> usar palavra-chave |
| Bash/PowerShell automatico | ✅ | ❌ -> Claude orienta passo a passo |
| `.claude/agents/` wrappers | ✅ | ❌ -> System prompt do Project |
| MCPs | `claude mcp add` | `claude_desktop_config.json` manual |
| Hooks (PreTool, PostTool) | ✅ | ❌ |
| Multi-projeto simultaneo | sessoes | Projects (sidebar) |
| Memoria persistente | sessions | Project (knowledge + instructions) |
| Bash tools execucao | ✅ | ❌ |
| File system acesso | ✅ | apenas via MCP filesystem |
| Output em pasta local | ✅ direto | so via copy-paste OU MCP filesystem |

## Limitacoes do Desktop a comunicar

- **Sem execucao de comando shell.** Mentorado precisa rodar manualmente o que Code faria sozinho.
- **Sem leitura de arquivo local** sem MCP filesystem.
- **Sem hooks**. Validacoes ficam por conta de instructions.
- **Sem atualizacao em real-time** de arquivos do kit (Project usa snapshot).

## Atualizacao do Project

Quando o kit muda (novo agente, nova skill, etc.):

1. Forge atualiza `22_CLAUDE_DESKTOP/knowledge-files.md`.
2. Mentorado abre Project no Desktop.
3. Re-upload os arquivos modificados (ou faz upload de novos).
4. Atualiza system prompt se necessario.

**Forge pode gerar pacote ZIP com knowledge files prontos pra upload.**

## Triggers no Desktop

Em vez de `/preflight-acessos`, mentorado digita:

```text
preflight acessos
```

OU

```text
rodar preflight
```

OU

```text
preciso fazer o preflight de acessos antes de começar
```

O system prompt do CoS Desktop reconhece todos. Detalhes em `commands-keywords.md`.

## Seguranca

- **Knowledge files do Project sao privados** (so quem tem acesso ao Project ve).
- **Nunca subir `.env`** no knowledge.
- **Nunca subir documentos com dados reais de cliente** sem permissao.
- **`_DONO_PRODUTO/` NAO vai pro Project.**
