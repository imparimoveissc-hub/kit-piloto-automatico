# Task Scaffold V30

> Salve em `03_TASKS/T<NN>-<descricao>.md`.

```markdown
# T<NN> - <Nome>

```yaml
owner: <agent>
model_profile: <slot do model-router>
objective: <1 frase do que a task entrega>
inputs:
  required:
    - <obrigatorio 1>
    - <obrigatorio 2>
  optional:
    - <opcional>
output_contract:
  - <verificavel 1>
  - <verificavel 2>
  - <verificavel 3>
acceptance_gate: GATE-<NOME>
budget: baixo | medio | alto
```

## Action items

- <item 1>
- <item 2>
- <item 3>

## Bloqueio

<quando a task fica blocked (falta dado/acesso/aprovacao)>

## Handoff

<para qual agente envia depois de completar>
```
