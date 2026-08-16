# Familia — Servico Local

## Contexto

Negocio com atendimento regional, demanda por WhatsApp e alta friccao de agenda/orcamento.

Exemplos: estetica, oficina, assistencia tecnica, escola local, limpeza, manutencao, pet shop.

## Primeira tarefa util

Criar um roteiro de atendimento para transformar mensagem solta em pedido claro:

```text
/whatsapp-system
Objetivo: atendimento inicial para servico local.
```

## Automacao sugerida

Nome: triagem de novo atendimento.

Trigger: nova mensagem no WhatsApp.

Fluxo:

1. coletar nome;
2. entender servico desejado;
3. coletar bairro/cidade;
4. checar urgencia;
5. oferecer horarios ou pedir fotos;
6. encaminhar para humano quando houver preco, desconto, reclamacao ou caso fora do padrao.

## WhatsApp sugerido

Mensagem inicial:

```text
Oi, [NOME]. Pra eu te ajudar rapido, me responde 3 coisas:

1. Qual servico voce precisa?
2. E para qual bairro/cidade?
3. Tem alguma urgencia ou prazo?
```

## Squad inicial

- CoS;
- WhatsApp Orchestrator;
- Automation Architect;
- QA Editor.

## Riscos

- prometer horario sem agenda real;
- passar preco errado;
- ignorar caso urgente;
- nao registrar origem do lead.

## Comandos recomendados

- `/setup-nicho`
- `/whatsapp-system`
- `/automatizar-processo`

