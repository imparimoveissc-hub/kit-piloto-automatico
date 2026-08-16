# T07 - Compactar Contexto

```yaml
owner: CoS
model_profile: router-cheap
objective: Reduzir contexto ativo preservando decisoes e proximas tasks.
inputs:
  required:
    - current-context.md
    - task-ledger.md
  optional:
    - decisions.md
    - outputs recentes
output_contract:
  - current-context.md atualizado
  - context-cache.md atualizado
acceptance_gate: GATE-INTAKE
budget: "baixo"
```

## Action items

- Manter apenas o que afeta a proxima task.
- Arquivar detalhes em cache com TTL.
- Registrar descartes importantes.
