# T06 - Operacao Semanal

```yaml
owner: Traffic Analyst
model_profile: analytics-balanced
objective: Rodar ciclo semanal de leitura, decisao e proximas pecas.
inputs:
  required:
    - metricas da semana
    - outputs ativos
  optional:
    - feedback comercial
    - novos comentarios/VOC
output_contract:
  - diagnostico curto
  - decisao por hipotese
  - proximas tasks
  - riscos
acceptance_gate: GATE-TRAFFIC
budget: "medio"
```

## Action items

- Separar problema de oferta, copy, criativo, pagina, publico e tracking.
- Atualizar ledger.
- Criar no maximo 3 proximas tasks.
