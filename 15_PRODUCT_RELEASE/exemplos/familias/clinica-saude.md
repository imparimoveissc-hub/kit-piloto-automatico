# Familia — Clinica e Saude

## Contexto

Atendimento sensivel com agendamento, triagem, confirmacao, pos-atendimento e restricoes de promessa.

Exemplos: clinica medica, odontologia, estetica, fisioterapia, psicologia, nutricao.

## Primeira tarefa util

Criar fluxo de agendamento seguro.

```text
/whatsapp-system
Objetivo: agendamento e triagem inicial sem diagnostico.
```

## Automacao sugerida

Nome: triagem de agendamento.

Trigger: paciente pede horario.

Fluxo:

1. coletar nome;
2. entender tipo de atendimento;
3. checar urgencia;
4. oferecer orientacao administrativa;
5. encaminhar para humano em caso sensivel;
6. confirmar agenda apenas com fonte validada.

## WhatsApp sugerido

```text
Oi, [NOME]. Posso te ajudar com o agendamento.

Me diga:
1. qual atendimento voce procura;
2. melhor dia/periodo;
3. se e primeira vez na clinica.

Se for urgencia ou sintoma importante, procure atendimento adequado imediatamente.
```

## Squad inicial

- CoS;
- WhatsApp Orchestrator;
- Customer Success Bot;
- Automation Architect;
- QA Editor.

## Riscos

- dar diagnostico;
- prometer resultado;
- tratar urgencia como atendimento comum;
- expor dados sensiveis;
- automatizar decisao clinica.

## Comandos recomendados

- `/setup-nicho`
- `/whatsapp-system`
- `/automatizar-processo`

