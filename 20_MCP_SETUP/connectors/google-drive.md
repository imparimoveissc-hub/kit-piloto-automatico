# Google Drive — via Composio Rube ou MCP nativo

## Recomendado: Composio Rube

A forma mais simples: usar Drive **via Rube** (`connectors/composio-rube.md`). Cobre tudo: ler, criar, editar, pesquisar arquivos, compartilhar.

## Alternativa: MCP nativo Google Drive

Se quiser MCP nativo (sem depender da Composio):

### Setup

```bash
claude mcp add gdrive --command "npx -y @modelcontextprotocol/server-gdrive"
```

Antes precisa autenticar:

```bash
npx -y @modelcontextprotocol/server-gdrive auth
```

Vai abrir browser pra OAuth.

### Tools

| Tool | Funcao |
|---|---|
| `search` | Busca em todo o Drive |
| `read_file` | Le conteudo de arquivo |

## Casos de uso

### Briefing automatico de cliente

```text
Le todos os Docs na pasta "Clientes/Empresa X" do meu Drive.
Resume em briefing de operacao usando template de `10_TEMPLATES_OPERACIONAIS/cliente-template/`.
Salva em `05_WORKSPACE/clientes/empresa-x/context.md`.
```

### Pesquisa de material existente

```text
Procura no Drive todos arquivos com "proposta comercial".
Lista os 5 mais recentes com link.
```

## Seguranca

- **Permissao read-only por padrao.** Add write so se necessario.
- **Pasta especifica.** Nao da acesso a todo o Drive — configura escopo.
- **Audit log** no Google Workspace.
