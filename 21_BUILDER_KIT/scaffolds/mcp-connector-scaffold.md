# MCP Connector Scaffold V30

> Salve em `20_MCP_SETUP/connectors/<nome>.md`.

```markdown
# <Nome do MCP> — <Descricao curta>

## Por que usar

<2-3 frases sobre quando este MCP faz diferenca>

## Pre-requisito

- <conta no servico>
- <permissao>
- <versao minima>

## Setup

### Passo 1 — <acao>

```bash
<comando>
```

### Passo 2 — Adicionar no Claude Code

```bash
claude mcp add <nome> --command "..."
```

OU em `~/.claude.json`:

```json
{
  "mcpServers": {
    "<nome>": {
      "command": "...",
      "args": ["..."]
    }
  }
}
```

### Passo 3 — Adicionar no Claude Desktop

Editar `claude_desktop_config.json` (caminho em `22_CLAUDE_DESKTOP/claude-desktop-config.json`):

```json
{
  "mcpServers": {
    "<nome>": { ... }
  }
}
```

### Passo 4 — Validar

```bash
claude mcp list
```

## Tools disponiveis

| Tool | Funcao |
|---|---|
| `<tool 1>` | <descricao> |
| `<tool 2>` | <descricao> |

## Casos de uso

### <Caso 1>

```text
<prompt exemplo>
```

### <Caso 2>

```text
<prompt exemplo>
```

## Seguranca

- <regra 1>
- <regra 2>

## Limitacoes

- <limite 1>

## Troubleshooting

| Problema | Solucao |
|---|---|
| <sintoma> | <correcao> |

## Referencias

- <doc oficial>
- <repo>
```
