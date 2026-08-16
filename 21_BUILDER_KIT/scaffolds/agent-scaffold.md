# Agent Scaffold V30

> Copie este scaffold quando criar agente novo. Preencha placeholders. Salve em `02_AGENTS/<nome>.md` ou `XX_STACK/agents/<nome>.md`.

```markdown
---
name: <nome-kebab-case>
description: <1 frase do que faz e quando usar>
tier: <0 | 1 | 2 | 3>
---

# @<nome>

## Papel

<2-3 frases descrevendo a funcao do agente, foco, e o que ele NAO faz.>

## Quando usar

<Sinais que ativam o agente: palavras-chave, contextos, situacoes.>

## Inputs obrigatorios

- <input 1>
- <input 2>
- <input 3>

## Inputs opcionais

- <opcional 1>

## Carrega

- <arquivo 1 (max 2 diretrizes)>
- <arquivo 2>

## Workflow

1. <passo 1>
2. <passo 2>
3. <passo 3>

## Output

```yaml
<campo_1>:
<campo_2>:
<campo_3>:
```

## Gate

`GATE-<NOME>` (definido em `00_OS/gates.md`).

## Handoff para

- @<agente proximo se aplicavel>

## Regras

- <regra 1>
- <regra 2>

## Anti-patterns

- <NAO fazer 1>
- <NAO fazer 2>
```

## Pos-criacao (Forge faz automaticamente)

1. Cria wrapper em `.claude/agents/<nome>.md`:

```markdown
---
name: <nome>
description: <descricao curta>
---

# Wrapper Claude Agent - <Nome>

Leia e siga `02_AGENTS/<nome>.md`.
```

2. Atualiza `02_AGENTS/README.md` (tabela de agentes).

3. Atualiza `00_INDEX.md` (camadas, rotas, arquivos-chave).

4. Atualiza `00_OS/cos.md` (classificacao).

5. Atualiza `00_OS/router.md` (roteamento).

6. Atualiza `22_CLAUDE_DESKTOP/knowledge-files.md` (incluir arquivo no Project).

7. Atualiza `22_CLAUDE_DESKTOP/commands-keywords.md` (palavra-chave).
