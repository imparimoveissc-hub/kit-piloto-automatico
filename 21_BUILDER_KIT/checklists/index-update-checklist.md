# Index Update Checklist

> Lista de TODOS os indices que podem precisar de atualizacao apos criar elemento novo.

## Para QUALQUER elemento novo

- [ ] `00_INDEX.md` — adicionar na tabela de camadas se for pasta nova
- [ ] `00_INDEX.md` — adicionar em "Arquivos-chave" se for arquivo central
- [ ] `22_CLAUDE_DESKTOP/knowledge-files.md` — adicionar arquivo no Project

## Se for AGENT

- [ ] `00_OS/cos.md` — tabela de classificacao
- [ ] `00_OS/router.md` — tabela de roteamento primario
- [ ] `00_OS/router.md` — edge cases se aplicavel
- [ ] `00_INDEX.md` — tabela de rotas principais
- [ ] `02_AGENTS/README.md` — tabela de agentes
- [ ] `.claude/agents/<nome>.md` — wrapper criado
- [ ] `22_CLAUDE_DESKTOP/commands-keywords.md` — palavras-chave

## Se for SKILL

- [ ] `XX_STACK/README.md` — tabela de skills da stack
- [ ] `22_CLAUDE_DESKTOP/knowledge-files.md`

## Se for TASK

- [ ] `03_TASKS/README.md` — listagem
- [ ] `01_PIPELINE/kpa-v30-pipeline.yaml` se for parte de pipeline mestre

## Se for DIRETRIZ

- [ ] `04_DIRETRIZES/README.md`
- [ ] `00_OS/knowledge-loader.md` — mapa de carregamento

## Se for MCP CONNECTOR

- [ ] `20_MCP_SETUP/README.md` — tabela de tiers
- [ ] `20_MCP_SETUP/recommended-stack.md` — por uso e segmento
- [ ] `20_MCP_SETUP/commands/mcp-setup.md` — se for Tier 1
- [ ] `22_CLAUDE_DESKTOP/claude-desktop-config.json` — template config

## Se for COMMAND (slash)

- [ ] `00_OS/commands/<nome>.md` — arquivo principal
- [ ] `.claude/commands/<nome>.md` — wrapper
- [ ] `22_CLAUDE_DESKTOP/commands-keywords.md` — equivalente em palavra-chave (sem `/`)

## Se for GATE NOVO

- [ ] `00_OS/gates.md` — definicao do gate
- [ ] `08_CHECKLISTS/<gate-nome>.md` — checklist do gate
- [ ] `00_OS/gate-matrix.md` se mudar severidade

## Smoke test final

- [ ] Abre Claude Code, roda elemento novo, valida output.
- [ ] Abre Claude Desktop (Project), pede pela palavra-chave, valida resposta.
- [ ] Documenta resultado.

## Validacao do nome

- [ ] `grep` em `00_INDEX.md`, `02_AGENTS/README.md`, `03_TASKS/README.md`, `04_DIRETRIZES/README.md` pra garantir nome unico.
