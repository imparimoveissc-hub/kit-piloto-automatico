# 21_BUILDER_KIT — Forge agent + scaffolds

> Pra quando o kit precisa **crescer**: criar agente novo, skill nova, task nova, diretriz nova, ou conector MCP novo. Tudo segue o padrao V30 e os indices se atualizam automaticamente.

## Por que existe

Quando o mentorado (ou voce, dono) precisa estender o kit, antes era preciso:
- decorar a estrutura V30 inteira
- copiar e adaptar arquivo manual
- lembrar de atualizar `00_INDEX.md`, `CLAUDE.md`, routing tables
- lembrar de criar wrapper em `.claude/agents/`
- lembrar de fazer Project no Claude Desktop refletir

Com Forge, voce so descreve **o que quer** e ele:
1. Pergunta o minimo (5 perguntas essenciais).
2. Cria o(s) arquivo(s) seguindo a convencao V30.
3. Atualiza indices automaticamente.
4. Cria wrapper em `.claude/agents/` quando aplicavel.
5. Lista o que ainda precisa ser feito manualmente (se houver).

## Quando usar Forge

| Sinal | Acao |
|---|---|
| "preciso de um agente que faca X" | `/forge` -> create-agent |
| "quero adicionar uma skill especifica" | `/forge` -> create-skill |
| "tem uma task recorrente, vou padronizar" | `/forge` -> create-task |
| "preciso documentar como fazer Y" | `/forge` -> create-diretriz |
| "quero conectar [ferramenta nova]" | `/forge` -> create-mcp-connector |

## Estrutura

```
21_BUILDER_KIT/
├── README.md                          # este arquivo
├── agents/
│   └── forge.md                       # Forge agent V30 completo
├── tasks/
│   ├── create-agent.md                # contrato pra criar agente
│   ├── create-skill.md                # idem skill
│   ├── create-task.md                 # idem task
│   ├── create-diretriz.md             # idem diretriz
│   └── create-mcp-connector.md        # idem MCP
├── scaffolds/
│   ├── agent-scaffold.md              # template agente V30
│   ├── skill-scaffold.md
│   ├── task-scaffold.md
│   ├── diretriz-scaffold.md
│   └── mcp-connector-scaffold.md
├── conventions.md                     # nomenclatura, headers, gates V30
└── checklists/
    ├── new-agent-checklist.md
    └── index-update-checklist.md
```

## Comando

```text
/forge
```

OU no Claude Desktop (sem `/`), basta dizer:

```text
"forge: criar agente novo de research de concorrente"
"forge: nova skill pra montar VSL"
"forge: documentar processo de cobranca como diretriz"
```

## Regras do Forge

1. **Nao cria sem necessidade.** Se a funcao ja existe em outro agente/skill, sugere reutilizar.
2. **Sempre segue convencao V30** (`conventions.md`).
3. **Atualiza indices automaticamente.** Sem isso, o kit fica inconsistente.
4. **Wrapper em `.claude/agents/`** quando o novo elemento for agent.
5. **Atualiza Project Claude Desktop** se houver instrucoes em `22_CLAUDE_DESKTOP/`.
6. **Roda gate de qualidade** antes de declarar pronto: nome claro, gate definido, contrato fechado.

## Quando NAO criar coisa nova

- Funcao ja existe em outro agente.
- Demanda e unica (vai usar 1 vez) — melhor task avulsa.
- Conhecimento e generico (provavelmente cabe em diretriz existente).
- Complexidade nao justifica novo componente.

Forge **sempre pergunta** "tem certeza que precisa criar isso?" antes de criar.
