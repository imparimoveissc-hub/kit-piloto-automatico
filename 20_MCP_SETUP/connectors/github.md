# GitHub MCP

## Setup

```bash
claude mcp add github --command "npx -y @modelcontextprotocol/server-github"
```

Variavel:

```bash
# No .env local:
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_...
```

Token em https://github.com/settings/tokens (escopos: `repo`, `read:user`).

## Tools

| Tool | Funcao |
|---|---|
| `create_repository` | Cria repo |
| `create_pull_request` | Abre PR |
| `get_file_contents` | Le arquivo |
| `push_files` | Commit |
| `search_repositories` | Busca repos |
| `create_issue` | Abre issue |

## Casos de uso

### Versionar configuracoes do mentorado

```text
Cria repo privado "meu-kit-piloto-config" no meu GitHub.
Sobe so as configuracoes adaptadas: `.claude/config.md`,
`05_WORKSPACE/current-context.md`, `squad-manifest.yaml`.
Ignora `.env` e qualquer credencial.
```

### Backup de outputs

```text
Toda quinta, commita o que esta em `06_OUTPUTS/` no repo de backup.
Tag com a data. Excluir nada que tenha "[REAL_CLIENT]".
```

## Seguranca

- **Token com escopo minimo.** So `repo` privado.
- **Nunca commit `.env`.** O `.gitignore` do kit ja protege.
- **Rotacao trimestral** do token.
