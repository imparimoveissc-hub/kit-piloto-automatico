# /mcp-setup — Setup interativo de MCPs

## Objetivo

Instalar MCPs recomendados no Claude Code do mentorado de forma guiada.

## Pre-requisitos

- Claude Code instalado
- Conta Anthropic ativa
- Internet

## Fluxo

### Passo 1 — Detectar SO

```bash
uname -s 2>/dev/null     # macOS/Linux
$PSVersionTable.OS       # PowerShell Windows
```

### Passo 2 — Tier 1 obrigatorio

Perguntar ao mentorado:

```text
Vou configurar os MCPs essenciais:

1. Composio Rube (1000+ apps em 1 install) - Recomendado
2. WhatsApp MCP (verygoodplugins) - se voce vende/atende via WhatsApp
3. Filesystem MCP - acesso a pastas locais
4. Playwright - opcional, pra auditar LPs

Qual ativar agora? (1, 2, 3, 4 ou TODOS)
```

### Passo 3 — Setup Composio Rube

Se confirmado:

1. Abre https://rube.app no browser do mentorado.
2. Espera mentorado criar conta e conectar 1-3 apps.
3. Roda:

```bash
claude mcp add rube --command "npx -y @composio/rube-mcp"
```

4. Valida: `claude mcp list` — espera ver `rube`.
5. Dentro do Claude: `Lista 3 ferramentas Composio que estao conectadas` — confirma que funciona.

### Passo 4 — Setup WhatsApp MCP

Se confirmado:

1. Verifica se mentorado tem numero comercial (NAO pessoal).
2. Clone `verygoodplugins/whatsapp-mcp`:

```bash
mkdir -p ~/mcps && cd ~/mcps
git clone https://github.com/verygoodplugins/whatsapp-mcp.git
cd whatsapp-mcp && npm install
```

3. Adiciona:

```bash
claude mcp add whatsapp --command "node $HOME/mcps/whatsapp-mcp/index.js"
```

4. Pede mentorado pegar celular.
5. Dentro do Claude: `whatsapp_qr` — exibe QR.
6. Mentorado escaneia.
7. Valida: `whatsapp_list_chats`.

### Passo 5 — Setup Filesystem

Se confirmado:

1. Pergunta: "Quais pastas voce quer dar acesso? (ex: pasta do kit + pasta de clientes)"
2. Adiciona com escopo:

```bash
claude mcp add filesystem --command "npx -y @modelcontextprotocol/server-filesystem $PASTA_KIT $PASTA_CLIENTES"
```

### Passo 6 — Setup Playwright

Se confirmado:

```bash
claude mcp add playwright --command "npx -y @modelcontextprotocol/server-playwright"
```

Valida: `claude mcp list`.

### Passo 7 — `.env` local

1. Verifica se `.env` existe na raiz do kit. Se nao:

```bash
cp .env.example .env
```

2. Pra cada MCP que precisa de token (Firecrawl, GitHub, Slack nativo, etc.), pede mentorado preencher `.env` MANUALMENTE.

NUNCA pegar token via chat.

### Passo 8 — Reiniciar Claude Code

Pede mentorado fechar e abrir Claude Code (pra carregar MCPs novos).

### Passo 9 — Smoke test

Roda 3 testes dentro do Claude Code:

```text
1. RUBE_SEARCH_TOOLS "send email"     → confirma Rube conectado
2. whatsapp_list_chats                → confirma WhatsApp (se ativado)
3. Lista arquivos em /pasta-do-kit    → confirma Filesystem
```

### Passo 10 — Resumo final

Mostra ao mentorado:

```text
MCPs instalados:
- rube (Composio) ✓
- whatsapp ✓
- filesystem ✓

Proximo passo:
- Pra adicionar mais MCPs depois, rode `/mcp-add <nome>`
- Pra audit periodico, rode `/mcp-audit`
- Documentacao completa em `20_MCP_SETUP/connectors/`

Quer testar agora? Pede:
"Resume minhas mensagens nao lidas no WhatsApp e me mostra as 3 mais importantes."
```

## Regras

- **NUNCA pedir token no chat.** Mentorado preenche `.env` manualmente.
- **NUNCA aprovar permissoes destrutivas automaticamente.** Sempre confirmar.
- **NUNCA pular smoke test.** MCP que nao foi testado = MCP que nao funciona.
- **Se algo falhar, NAO MASCARAR.** Reporta o erro exato e para.
