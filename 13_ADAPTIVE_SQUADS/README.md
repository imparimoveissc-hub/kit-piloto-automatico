# 13_ADAPTIVE_SQUADS — Squads Adaptativos V30

Camada para montar squads especificos por cliente, fase, canal e gargalo. O objetivo e evitar agentes genericos e permitir que o CoS adapte comandos, papeis e contexto conforme a conversa real evolui.

## Principio

Squad nao e lista fixa de agentes. Squad e uma configuracao viva:

- objetivo do cliente;
- fase do funil;
- gargalo atual;
- canais ativos;
- nivel tecnico do operador;
- decisoes recentes;
- comandos mais usados;
- limites de automacao.

## Arquivo vivo por cliente

Todo cliente maduro deve ter:

```text
05_WORKSPACE/clientes/<cliente>/squad-manifest.yaml
```

Esse arquivo define:

- squad ativo;
- papeis ligados/desligados;
- comandos curtos do cliente;
- contexto que cada papel pode carregar;
- quando revisar a estrutura;
- quais gates bloqueiam entrega.

## Ciclo adaptativo

```text
conversa/task
  -> CoS identifica intencao e gargalo
  -> escolhe squad minimo
  -> executa especialista
  -> gate
  -> handoff
  -> atualiza manifest se houve aprendizado
```

## Quando adaptar o squad

- O cliente pede repetidamente o mesmo tipo de entrega.
- Uma pergunta vira processo recorrente.
- Um gargalo muda de canal: ads -> LP -> WhatsApp -> atendimento.
- O operador precisa de comandos mais simples.
- Um agente carregou contexto demais.
- Uma etapa falhou 2 vezes no mesmo gate.
- A conversa revelou nova restricao, oferta, prova ou SLA.

## Squads base

| Squad | Quando usar | Nucleo |
|---|---|---|
| `growth-diagnostic` | entender onde esta quebrando | CoS, Traffic, Funnel, Attribution, QA |
| `offer-copy-build` | criar promessa e pecas | CoS, Research, Strategy, Copy, QA |
| `whatsapp-revenue` | WhatsApp vendas/atendimento | CoS, WhatsApp Orchestrator, SDR, Follow-up, QA |
| `customer-success` | pos-venda e churn | CoS, CS Bot, Automation, QA |
| `automation-cowork` | bot/documentos runtime | CoS, Cowork Architect, Conversation QA |
| `process-automation` | automatizar rotina do cliente | CoS, Automation Architect, QA |
| `product-hardening` | promessa vs entrega | CoS, Product Auditor, Strategy, WhatsApp, QA |
| `niche-kit-builder` | criar kit por nicho | CoS, Research, Strategy, Compliance, QA |

## Regras

- Comecar com o menor squad que resolve.
- Adicionar especialista apenas quando muda a decisao ou melhora a entrega.
- Adaptar comandos por cliente, mas manter contratos e gates padrao.
- Nunca deixar um agente "morando" no contexto se ele nao afeta a proxima task.
- Comando novo precisa ter owner, output e gate.
