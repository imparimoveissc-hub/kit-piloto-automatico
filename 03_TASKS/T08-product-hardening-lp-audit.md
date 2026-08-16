# T08 - Product Hardening e LP Audit

```yaml
owner: CoS
model_profile: reviewer-frontier
objective: Comparar promessa publica da LP com a entrega real do produto e abrir plano de robustez.
inputs:
  required:
    - URL ou arquivo da LP
    - lista de entregaveis atuais
    - onboarding atual
    - fluxos WhatsApp/atendimento atuais
  optional:
    - provas
    - feedback de usuarios
    - tickets de suporte
    - demos ou prints do produto
output_contract:
  - promise inventory
  - delivery coverage map
  - gap list por severidade
  - roadmap de hardening
  - tasks de implementacao
acceptance_gate: GATE-PRODUCT
budget: alto
```

## Action items

- Extrair claims da LP.
- Classificar claims: funcional, resultado, suporte, automacao, velocidade, facilidade, garantia.
- Mapear onde cada claim e entregue no produto.
- Marcar lacunas como `entregue`, `parcial`, `nao entregue`, `sem evidencia`.
- Priorizar gaps que quebram confiança, ativacao, venda ou retencao.
- Criar roadmap em fases: bloquear risco, robustecer core, automatizar, nichar.

## Bloqueio atual

Se a LP nao estiver disponivel na pasta nem em URL, a auditoria real fica `blocked`. Pode-se criar apenas o framework e checklist.

