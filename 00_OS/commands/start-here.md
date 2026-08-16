# Command - start-here

## Objetivo

Colocar o V30 em estado operacional com o menor contexto possivel.

## Passos

1. Ler `00_INDEX.md`.
2. Ler `manifest.yaml`.
3. Ler `05_WORKSPACE/current-context.md`.
4. Ler `07_LOGS/task-ledger.md`.
5. Se `current-context.md` estiver vazio, executar `03_TASKS/T00-bootstrap.md`.
6. Se houver task `ready`, rotear pelo CoS.

## Saida

```yaml
status:
projeto_ativo:
task_atual:
rota:
modelo_profile:
proximo_passo:
```
