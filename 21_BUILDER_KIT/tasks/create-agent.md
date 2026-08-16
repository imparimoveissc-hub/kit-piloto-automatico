# Task — Create Agent

```yaml
owner: forge
model_profile: strategy-frontier
objective: Criar agente novo seguindo padrao V30, com wrapper e indices atualizados.
inputs:
  required:
    - nome (kebab-case)
    - funcao em 1 frase
    - sinais que ativam
    - gate aplicavel
  optional:
    - tier
    - diretrizes a carregar
    - handoff target
output_contract:
  - arquivo `02_AGENTS/<nome>.md` (ou stack)
  - wrapper `.claude/agents/<nome>.md`
  - linha em `00_OS/router.md`
  - linha em `00_OS/cos.md` (classificacao)
  - linha em `00_INDEX.md` (camadas + rotas)
  - linha em `02_AGENTS/README.md`
  - linha em `22_CLAUDE_DESKTOP/knowledge-files.md`
  - linha em `22_CLAUDE_DESKTOP/commands-keywords.md`
acceptance_gate: GATE-INTAKE (pre-flight Forge)
budget: medio
```

## Action items

1. Pre-flight: funcao ja existe?
2. Coletar 5 inputs essenciais.
3. Aplicar scaffold de `21_BUILDER_KIT/scaffolds/agent-scaffold.md`.
4. Criar arquivo do agente.
5. Criar wrapper.
6. Atualizar TODOS os indices listados em output_contract.
7. Reportar pendencias manuais (se houver).
