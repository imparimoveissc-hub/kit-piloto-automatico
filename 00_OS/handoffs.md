# Handoffs

## Contrato padrao

Todo handoff deve responder:

```yaml
from:
to:
task_id:
output:
used_inputs:
assumptions:
open_gaps:
gate_result:
next_step:
files:
```

## Handoffs criticos

| De | Para | Nao pode faltar |
|---|---|---|
| Researcher | Strategist | VOC ouro, objecoes, linguagem literal |
| Strategist | Copy Director | DRE, awareness, MUP, MUS, promessa, prova |
| Copy Director | Production Lead | copy aprovada, hierarquia, CTAs, assets necessarios |
| Production Lead | Traffic Analyst | formatos, URLs/assets, claims usados |
| Traffic Analyst | QA Editor | hipotese, KPI, evento, plano de leitura |
| QA Editor | CoS | verdict, issues, fixes, se bloqueia ou nao |

## Regra

Handoff bom reduz contexto futuro. Handoff ruim faz o proximo agente reler tudo.
