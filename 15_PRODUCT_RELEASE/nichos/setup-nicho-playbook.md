# Playbook — Setup de Nicho Adaptativo

## Objetivo

Configurar o kit para qualquer empresa sem depender de existir um pacote pronto daquele nicho.

## Entrada minima

```yaml
business_description:
main_service:
target_audience:
main_channel:
current_bottleneck:
uses_whatsapp:
tools:
risk_or_restrictions:
```

## Procedimento

1. Ler `family-classifier.md`.
2. Classificar familia operacional.
3. Verificar preset existente em `nichos/`.
4. Selecionar templates.
5. Selecionar WhatsApp pack.
6. Selecionar automacoes iniciais.
7. Criar ou atualizar `.claude/config.md`.
8. Sugerir squad inicial.
9. Sugerir primeira tarefa.

## Output esperado

```yaml
setup_status: draft
business:
  segment:
  family:
  description:
  target_audience:
  offer:
routes:
  primary_templates:
  niche_preset:
  whatsapp_flow:
  automation_flow:
squad:
  active_roles:
  inactive_roles:
  review_trigger:
commands:
  recommended:
  recurrent:
risks:
  - risk:
    mitigation:
first_task:
  command:
  expected_output:
```

## Squads iniciais por familia

| Familia | Squad |
|---|---|
| servico local | CoS, WhatsApp, Automation, QA |
| profissional liberal | CoS, Briefing, WhatsApp, Automation, QA |
| B2B consultivo | CoS, SDR, Strategy, Automation, QA |
| ecommerce | CoS, WhatsApp, CS, Automation, QA |
| infoproduto | CoS, CS, Copy, Automation, QA |
| agencia/servico digital | CoS, Briefing, Criacao, Revisao, Entrega, Automation |
| clinica/saude | CoS, WhatsApp, CS, Automation, QA |
| juridico/regulado | CoS, Briefing, Automation, QA, humano responsavel |

## Regras

- Se o nicho for regulado, aumentar rigor de QA.
- Se o usuario nao souber ferramentas, seguir com processo manual assistido.
- Se houver WhatsApp, sempre criar handoff.
- Se houver automacao, sempre criar teste e rollback.

