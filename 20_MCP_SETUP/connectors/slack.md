# Slack — via Composio Rube ou MCP nativo

## Recomendado: Composio Rube

Slack **via Rube** (`connectors/composio-rube.md`) cobre 100% dos casos: enviar mensagem, ler canal, criar canal, gerenciar membros.

## Alternativa: MCP nativo

```bash
claude mcp add slack --command "npx -y @modelcontextprotocol/server-slack"
```

Variavel de ambiente:

```bash
# No .env local (nao commitar):
SLACK_BOT_TOKEN=xoxb-...
SLACK_TEAM_ID=T...
```

## Tools

| Tool | Funcao |
|---|---|
| `slack_list_channels` | Lista canais |
| `slack_post_message` | Envia mensagem |
| `slack_reply_to_thread` | Responde thread |
| `slack_add_reaction` | Adiciona emoji |
| `slack_get_channel_history` | Le historico |
| `slack_get_thread_replies` | Le respostas de thread |
| `slack_get_users` | Lista usuarios |

## Casos de uso

### Notificar deal fechado

```text
Quando um deal no HubSpot passar pra "Fechado-Ganho",
posta no canal #vendas do Slack: "novo deal: [empresa] [valor]"
```

### Resumo diario

```text
Cria receita Rube: toda 18h, resume os deals movidos hoje no HubSpot
e posta no #vendas como thread organizada.
```

### Atendimento interno

```text
Le ultimas 50 mensagens do canal #suporte.
Identifica reclamacoes recorrentes.
Me da top 3 + acao recomendada.
```

## Seguranca

- **Bot tem escopo limitado.** Nao da admin pro Slack bot.
- **Canais especificos.** Nao colocar bot em canais sensiveis (RH, juridico) sem revisar.
