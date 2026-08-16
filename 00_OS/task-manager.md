# Task Manager do CoS

## Ciclo de vida

```text
intake -> task contract -> route -> execute -> gate -> handoff -> ledger update -> next task
```

## Estados

| Estado | Significado |
|---|---|
| `backlog` | capturada, ainda nao priorizada |
| `ready` | pronta para execucao |
| `blocked` | falta dado, arquivo, acesso ou aprovacao |
| `in_progress` | sendo executada |
| `gate_review` | aguardando validacao |
| `done` | entregue e registrada |
| `rework` | voltou por falha de gate |
| `concerns` | pode avancar com nota se nao houver S3 |

## Formato minimo de task

```yaml
task_id:
status:
owner:
model_profile:
objective:
inputs:
output_contract:
acceptance_gate:
budget:
assumptions:
blocked_by:
next:
```

## Politica full-auto

- Se a task cabe em ate 2 horas e nao depende de aprovacao externa, executar.
- Se a task depende de escolha estrategica mas existe default seguro, executar e registrar premissa.
- Se a task exige credencial, publicacao real, gasto de midia ou mudanca irreversivel, bloquear e pedir confirmacao.

## Ledger

O ledger vive em `07_LOGS/task-ledger.md`. O CoS atualiza:

- task id;
- status;
- rota;
- modelo profile;
- arquivo de output;
- proxima acao.

## Rework

Se falhar no mesmo gate:

1. Primeira falha: corrigir dentro da mesma abordagem.
2. Segunda falha: trocar abordagem ou subir modelo.
3. Terceira falha: voltar etapa anterior e revisar premissas.

Se `gate-matrix.md` marcar S4, bloquear task e registrar risco antes de continuar.
