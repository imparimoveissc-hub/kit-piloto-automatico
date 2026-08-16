# Contrato da Ponte Financeira

## Entrada esperada

```yaml
message_id: ""
sender: ""
message_type: text | audio | image | pdf
text: ""
attachments:
  - file_name: ""
    mime_type: ""
    path: ""
timestamp: ""
```

## Saida esperada

```yaml
status: confirmed | needs_clarification | duplicate | blocked
reply_text: ""
extracted:
  amount: 0
  date: ""
  description: ""
  category: ""
  entity: pj | pf
  fingerprint: ""
finance_payload:
  description: ""
  amount: 0
  date: ""
  category: ""
  entity: pj
  expenseKind: one_off
```

## Regras

- Se `status = needs_clarification`, nao escrever no financeiro.
- Se `status = duplicate`, responder com aviso e nao escrever de novo.
- Se `status = confirmed`, usar `POST /api/transactions`.

