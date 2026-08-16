# Gate Matrix

## Severidade

| Severidade | Significado | Acao |
|---|---|---|
| S0 | ajuste cosmético | pode seguir |
| S1 | melhoria recomendada | pode seguir com nota |
| S2 | problema relevante | rework se for entrega final |
| S3 | bloqueio | nao avanca |
| S4 | risco alto | parar e escalar |

## Verdict

| Score | Verdict | Regra |
|---:|---|---|
| 9-10 | pass | pode avancar |
| 7-8 | concerns | avanca se nao houver S3 |
| 5-6 | rework | corrigir antes de avancar |
| 0-4 | fail | voltar etapa ou trocar abordagem |

## Bloqueios automaticos

- Copy final sem mecanismo.
- Campanha paga sem evento de conversao.
- Bot WhatsApp sem handoff humano.
- Disparo WhatsApp real sem confirmacao.
- Automacao com API write, CRM update, envio, budget ou publicacao sem confirmacao.
- Automacao sem teste e rollback.
- LP prometendo entrega inexistente sem gap marcado.
- Claim forte sem prova ou sem marcador `[A PREENCHER]`.
- Output final com dados inventados.
- Cliente/contexto errado.
- Falha repetida 3 vezes no mesmo gate.

## Escalada

1. S2: mesmo agente corrige.
2. S3: QA Editor revisa e especialista refaz.
3. S4: CoS bloqueia ledger e pede decisao humana se houver risco real.

## Rework log

Cada rework deve registrar:

```yaml
task_id:
gate:
issue:
severity:
fix:
attempt:
next_action:
```
