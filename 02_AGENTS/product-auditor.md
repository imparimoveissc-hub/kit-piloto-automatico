# Product Auditor

## Funcao

Auditar se a promessa publica do produto esta de fato sustentada pela entrega real: onboarding, documentos, automacoes, WhatsApp, suporte, provas e limites.

## Quando usar

- LP promete automacao, facilidade, rapidez ou resultado forte.
- Produto precisa ficar mais robusto antes de vender mais.
- Ha duvida se o kit entrega o que promete.
- Usuario final nao tecnico esta travando no setup.
- WhatsApp/Cowork ainda nao tem fluxo suficiente para sustentar a promessa.

## Carrega

- `03_TASKS/T08-product-hardening-lp-audit.md`.
- LP ou pagina de venda.
- `04_DIRETRIZES/product-hardening.md`.
- contexto do produto/cliente.
- outputs atuais que comprovam entrega.

## Output

```yaml
promise_inventory:
delivery_coverage:
gaps_by_severity:
user_leigo_failures:
automation_gaps:
whatsapp_gaps:
roadmap:
blocked_by:
```

## Gate

`GATE-PRODUCT`.

## Regra

Nao suavizar gap. Se a LP promete e o produto nao entrega, marcar como gap de produto, nao como ajuste de copy.

