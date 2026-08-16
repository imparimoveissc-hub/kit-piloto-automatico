# Skill Scaffold V30

> Salve em `XX_STACK/skills/<nome>/SKILL.md` ou similar.

```markdown
---
name: <nome-kebab-case>
description: <quando ativa esta skill — frase com palavras-chave>
metadata:
  priority: <numero>
  triggers:
    phrases:
      - "<frase 1>"
      - "<frase 2>"
    pathPatterns:
      - "<glob opcional>"
---

# Skill: <Nome em Title Case>

## Quando usar

<situacoes que disparam a skill>

## Pre-requisitos

- <pre 1>
- <pre 2>

## Workflow

1. <passo 1>
2. <passo 2>
3. <passo 3>
4. <passo 4>
5. <passo 5>

## Inputs minimos

```yaml
<campo_1>:
<campo_2>:
```

## Output esperado

```yaml
<output_1>:
<output_2>:
```

## Regras

- <regra 1>
- <regra 2>

## Anti-patterns

- <NAO fazer 1>
- <NAO fazer 2>

## Quando ativada

- Triggers diretos: `<frase>`, `<frase>`
- Triggers indiretos: <descricao>

## Referencias

- <link doc>
- <link recurso>
```
