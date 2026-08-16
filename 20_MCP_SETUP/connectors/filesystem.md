# Filesystem MCP

## Setup

```bash
claude mcp add filesystem --command "npx -y @modelcontextprotocol/server-filesystem /caminho/permitido"
```

Substitua `/caminho/permitido` pela raiz onde o mentorado quer dar acesso (ex: pasta do kit + pasta de clientes).

Multiplas pastas:

```bash
claude mcp add filesystem --command "npx -y @modelcontextprotocol/server-filesystem /Users/mentorado/Kit-Piloto-Automatico-V30 /Users/mentorado/Clientes"
```

## Por que usar

O Claude Code ja le/escreve via Read/Write tools nativos. **Filesystem MCP** adiciona valor quando:

- Mentorado quer dar acesso a multiplas pastas fora do kit (ex: pasta Clientes em outro lugar).
- Operacoes mais avancadas: mover arquivos em lote, sincronizar, comparar pastas.

## Casos de uso

### Sincronizar outputs

```text
Move tudo de `06_OUTPUTS/2026-05-09_*` pra pasta do cliente
em `~/Clientes/empresa-x/entregas/maio-2026/`.
```

### Importar briefing existente

```text
Procura em `~/Documents/Clientes/Empresa X/` por arquivos
de briefing antigos. Extrai info relevante e cria context pack V30.
```

## Seguranca

- **Escopo de pastas.** So da acesso ao que precisa, nao a `/` inteiro.
- **Nunca dar acesso a `~/.ssh`, `~/.aws`, ou pasta com credenciais.**
