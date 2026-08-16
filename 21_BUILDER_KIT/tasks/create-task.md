# Task — Create Task (meta-task)

```yaml
owner: forge
model_profile: router-cheap
objective: Criar task nova com contrato fechado seguindo padrao V30.
inputs:
  required:
    - nome (TNN-descricao)
    - owner (qual agente)
    - model_profile
    - output_contract (lista verificavel)
    - acceptance_gate
  optional:
    - budget
    - bloqueio_provavel
output_contract:
  - arquivo `03_TASKS/T<NN>-<nome>.md`
  - linha em `03_TASKS/README.md`
acceptance_gate: GATE-INTAKE
budget: baixo
```

## Action items

1. Pre-flight: task ja existe? Pode estender existente?
2. Identificar proximo numero TNN livre.
3. Aplicar `task-scaffold.md`.
4. Criar arquivo.
5. Atualizar `03_TASKS/README.md`.
