# 20_MCP_SETUP — Conectores MCP prontos

Stack de **MCPs (Model Context Protocol)** recomendados pro Kit V30. Cada conector deixa o Claude Code interagir diretamente com uma ferramenta externa (Drive, WhatsApp, Slack, Meta, etc.) sem o mentorado precisar copiar e colar dados.

## Filosofia

- **Composio Rube primeiro.** Cobre 1000+ apps com 1 instalacao. Use sempre que possivel antes de adicionar MCP nativo.
- **MCP nativo so quando faz diferenca.** WhatsApp Web (verygoodplugins), Playwright (browser), Filesystem nativo — sao casos onde MCP especifico ganha.
- **Token nunca no kit.** Toda credencial vive no `.env` local OU no provedor (Composio gerencia OAuth).
- **Confirmacao antes de qualquer escrita real.** Read-only = OK rodar full-auto. Write/delete/post/disparo = pede confirmacao humana.

## Setup rapido

Dentro do Claude Code, na raiz do kit:

```text
/mcp-setup
```

O comando:
1. Detecta qual SO (Mac/Windows/Linux/WSL).
2. Pergunta quais MCPs ativar (Tier 1 obrigatorios, Tier 2/3 opcionais).
3. Instala via `claude mcp add` ou edita `~/.claude.json` direto quando precisa.
4. Valida cada conector com `claude mcp list`.
5. Salva tudo em `.env` local (gitignored).

## Tiers recomendados

| Tier | MCP | Por que |
|---|---|---|
| 1 | **Composio Rube** | 1000+ apps em 1 install. Cobre Drive, Slack, Notion, Gmail, Linear, ClickUp, X/Twitter, GitHub, Salesforce, HubSpot, Figma, Microsoft 365 |
| 1 | **WhatsApp MCP** (verygoodplugins) | WhatsApp Web nativo — leitura e envio de mensagens |
| 1 | **Meta Ads CLI** | Ja coberto por `/meta-cli-install` — nao precisa MCP separado |
| 1 | **Filesystem** | Acesso a pastas locais sem permissao repetida |
| 2 | **Playwright** | Browser automation, screenshots, auditoria de LP |
| 2 | **Firecrawl** ou **Exa** | Scraping/research de concorrentes |
| 2 | **Context7** | Docs de bibliotecas atualizadas |
| 3 | **GitHub** | Versionar projetos do mentorado |
| 3 | **Sequential Thinking** | Raciocinio passo-a-passo pra tasks complexas |

## Conectores documentados

| Arquivo | O que tem |
|---|---|
| `connectors/composio-rube.md` | Setup rube.app + 1000 apps |
| `connectors/whatsapp-mcp.md` | verygoodplugins/whatsapp-mcp (WhatsApp Web) |
| `connectors/google-drive.md` | Google Drive nativo (alternativa ao Rube) |
| `connectors/slack.md` | Slack nativo (alternativa ao Rube) |
| `connectors/gmail.md` | Gmail (via Rube ou nativo) |
| `connectors/notion.md` | Notion (via Rube) |
| `connectors/meta-ads.md` | Meta Ads (Facebook/Instagram via Rube ou CLI nativo) |
| `connectors/playwright.md` | Playwright browser |
| `connectors/firecrawl.md` | Firecrawl scraper |
| `connectors/github.md` | GitHub MCP |
| `connectors/filesystem.md` | Filesystem MCP nativo |

## Seguranca

| Documento | Quando usar |
|---|---|
| `security/token-policy.md` | Antes de adicionar qualquer MCP que pede token |
| `security/audit-checklist.md` | Mensal: revisar permissoes ativas, tokens expirados, MCPs nao usados |

## Comandos

| Comando | Funcao |
|---|---|
| `/mcp-setup` | Setup interativo guiado |
| `/mcp-audit` | Lista MCPs ativos, permissoes, ultima vez usado |
| `/mcp-add <nome>` | Adiciona MCP especifico |
| `/mcp-remove <nome>` | Remove MCP (e revoga tokens onde possivel) |

## Regras inegociaveis

1. **Nunca pedir token no chat.** OAuth via browser sempre.
2. **Nunca escrever token em arquivo do kit.** Tokens vivem so em `.env` local OU no provedor.
3. **Read antes de Write.** Cada novo MCP comeca em modo read-only. Write so depois de teste manual.
4. **Confirmar antes de disparo real.** Postar em rede social, enviar WhatsApp em massa, deletar arquivo — sempre confirmacao humana.
5. **Auditar mensalmente.** Token expirado, MCP nao usado em 30 dias, permissao excessiva — limpar.
