# Command - nova-task

## Objetivo

Transformar um pedido novo em task pronta.

## Passos

1. Classificar pedido no `00_OS/router.md`.
2. Criar task usando `03_TASKS/task-contract.md`.
3. Definir owner.
4. Definir `model_profile` pelo `00_OS/model-router.yaml`.
5. Definir gate.
6. Registrar em `07_LOGS/task-ledger.md`.
7. Registrar premissa em `07_LOGS/decisions.md` se houver escolha relevante.

## Saida

```yaml
task_id:
owner:
model_profile:
gate:
status: ready
```
