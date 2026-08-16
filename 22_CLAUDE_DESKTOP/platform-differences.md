# Claude Code vs Claude Desktop — Diferenças Praticas

## Visao geral

| Aspecto | Claude Code (CLI) | Claude Desktop (app) |
|---|---|---|
| Acesso a terminal | Sim, executa comandos | Nao executa, so orienta |
| Slash commands `/` | Sim | Nao — usa palavras-chave |
| Hooks/automations | Sim | Nao |
| MCPs | `claude mcp add` | `claude_desktop_config.json` manual |
| Knowledge persistente | Sessions / memoria | Projects com files + instructions |
| File system local | Read/Write direto | Apenas via MCP filesystem |
| Multi-projeto | Sessions paralelas | Projects na sidebar |
| Custo por uso | Token cost por sessao | Pro/Team subscription |
| Skills (auto-discovery) | Sim, system reminders | Nao |
| Mensagens em batch | Sim | Nao tao agil |

## Cenarios e qual usar

### Use Claude Code quando:

- Trabalho de dev (codigo, repos, testes).
- Operacao que envolve rodar shell (npm install, git, etc.).
- Trabalho em paralelo com varios files.
- Setup inicial do kit (instalar Meta CLI, configurar `.env`).
- Auditoria de codebase / mapeamento profundo.

### Use Claude Desktop quando:

- Operacao do dia a dia: briefing, copy, relatorio.
- Conversa fluida com contexto preservado (Project).
- Mentorado nao-tecnico (que nao quer ver terminal).
- Setup leve (criar copy, planejar campanha, organizar cliente).
- Quer multiplos contextos isolados (Trafego separado de WhatsApp).

## Funcionalidades que SO FUNCIONAM no Code

### Bash/PowerShell execution

```bash
claude mcp add ...
git status
npm install
meta ads campaign list ...
```

No Desktop, Claude orienta o comando mas **mentorado precisa rodar manualmente**.

### Skills auto-discovery

System reminders injetam skills baseado em contexto. No Desktop, nao tem.

### Hooks

```json
{
  "hooks": {
    "preToolUse": "...",
    "postToolUse": "..."
  }
}
```

Sem equivalente no Desktop.

### File system direto

`Read`, `Write`, `Edit`, `Glob`, `Grep`. No Desktop, requer MCP filesystem.

## Funcionalidades que SO FUNCIONAM no Desktop

### Projects com knowledge files

Upload de arquivos no Project, Claude usa como contexto persistente.

No Code, equivalent e `.claude/` + system reminders, mas e diferente.

### Sidebar com multiplos contextos

Clica no Project, ja entra com tudo carregado. Ergonomico pra leigo.

No Code, tem que abrir pasta correta + carregar.

### MCPs com config visual (Settings)

App Desktop tem UI pra ver MCPs ativos. Code so via comando.

## O que voce, dono, precisa garantir

1. **Tudo importante existe em ambas plataformas.**
   - Comando `/X` no Code = palavra-chave `X` no Desktop.
   - Arquivo `02_AGENTS/X.md` = entra no knowledge do Project Desktop.

2. **System prompt do Desktop = denso e completo.** Compensa ausencia de hooks/skills.

3. **Knowledge files do Project = bem escolhidos.** 20 arquivos / 30MB. Use a lista de `knowledge-files.md`.

4. **MCPs disponiveis em ambos.** Mesmo nome, mesma funcao, configuracao diferente.

5. **Mentorado escolhe plataforma.** Se ele prefere app, ele tem 100% do kit. Se prefere CLI, idem.

## Forge update both

Quando o Forge cria novo agente/skill/diretriz, ele:

- Cria arquivo em pasta certa (`02_AGENTS/`, `04_DIRETRIZES/`, etc.).
- Cria wrapper `.claude/agents/` ou `.claude/commands/` (pro Code).
- Atualiza `22_CLAUDE_DESKTOP/knowledge-files.md` (pro Desktop).
- Atualiza `22_CLAUDE_DESKTOP/commands-keywords.md` (pra mentorado saber a palavra-chave).

Sem isso, novo elemento so existe pro Code, nao pro Desktop.

## Migração de uma sessão Code -> Desktop

Se o mentorado começou no Code mas quer migrar:

1. Salve state em `05_WORKSPACE/current-context.md` + `clientes/<cliente>/state.md`.
2. No Desktop, crie Project + upload esses arquivos.
3. Inicia conversa: "Continuando o trabalho. Le o state e me da proximo passo."

## Migracao Desktop -> Code

Quando precisar:

1. No Code, abre pasta do kit.
2. Le os mesmos arquivos do Project Desktop.
3. Continua de onde parou.

Estado vive em arquivos, nao na plataforma. Por design.
