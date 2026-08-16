# Exemplo — Automacao de Onboarding de Cliente

Status: exemplo preenchido

## Pedido do usuario

```text
Quero automatizar o onboarding quando um cliente novo fecha comigo.
```

## Resumo do processo

Quando um cliente fecha, o sistema deve coletar informacoes, organizar briefing, criar pasta do cliente, gerar proximos passos e preparar uma mensagem de boas-vindas.

## Blueprint

```yaml
automation_status: draft
process_name: "Onboarding de cliente novo"
segment: "servico digital"
goal: "reduzir friccao apos fechamento e padronizar inicio do projeto"
trigger:
  type: manual
  description: "usuario informa que cliente fechou"
inputs:
  - name: "nome do cliente"
    source: "usuario/CRM"
    required: true
  - name: "servico contratado"
    source: "proposta"
    required: true
  - name: "contato WhatsApp"
    source: "CRM"
    required: false
steps:
  - id: "S1"
    name: "Criar pasta do cliente"
    mode: ai_assisted
    actor: ai_agent
    approval_required: true
  - id: "S2"
    name: "Gerar briefing inicial"
    mode: ai_assisted
    actor: ai_agent
    approval_required: false
  - id: "S3"
    name: "Criar mensagem de boas-vindas"
    mode: ai_assisted
    actor: ai_agent
    approval_required: true
  - id: "S4"
    name: "Enviar mensagem"
    mode: blocked
    actor: human
    approval_required: true
human_handoff:
  required: true
  when: "antes de enviar mensagem ao cliente"
tools:
  - name: "WhatsApp"
    purpose: "boas-vindas e coleta de informacoes"
    risk_level: high
  - name: "Pasta local/Drive"
    purpose: "organizar briefing e entregas"
    risk_level: medium
test_plan:
  dry_run_input: "cliente ficticio"
  expected_output: "briefing + mensagem draft + checklist"
rollback_plan:
  how_to_stop: "nao ativar envio automatico"
  how_to_restore: "apagar/arquivar pasta teste"
```

## SOP resumido

1. Confirmar dados basicos do cliente.
2. Criar pasta.
3. Gerar briefing inicial.
4. Criar mensagem de boas-vindas.
5. Humano revisa.
6. Humano envia ou autoriza envio.
7. Registrar proximos passos.

## Mensagem draft

```text
Oi, [NOME]. Seja bem-vindo(a).

Ja organizei o inicio do seu projeto por aqui. Para deixar tudo certo, me responde essas 3 perguntas:

1. Qual e o principal objetivo deste projeto?
2. Existe alguma data importante ou prazo limite?
3. Quais materiais voce ja tem prontos para me enviar?

Assim que eu tiver isso, monto o briefing inicial e te mando os proximos passos.
```

## Proximo passo

Testar com cliente ficticio antes de usar com cliente real.

