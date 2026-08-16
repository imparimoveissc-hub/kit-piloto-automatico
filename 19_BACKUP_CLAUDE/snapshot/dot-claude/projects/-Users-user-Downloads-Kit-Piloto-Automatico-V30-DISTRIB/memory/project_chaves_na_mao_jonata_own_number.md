---
name: project-chaves-na-mao-jonata-own-number
description: Lead do Chaves na Mão (Ímpar Imóveis) com telefone igual ao WhatsApp do próprio Jonata não deve receber contato automático
metadata: 
  node_type: memory
  type: project
  originSessionId: 996bda2d-1940-4978-a510-7aadc594c4c7
---

Em 2026-06-28, a automação `leads-chaves-na-mao-whatsapp` recebeu um lead ("Jaque", referente ao imóvel Ref. CS0097) cujo telefone informado no site Chaves na Mão — (47) 99687-6631 — é o mesmo número do WhatsApp pessoal do Jonata (JID real `554796876631@s.whatsapp.net`, contato salvo como "Jonata Impar Imoveis"; a forma com o 9 extra, `5547996876631`, não resolve no WhatsApp/dá erro "no LID found").

Jonata confirmou: não enviar a mensagem automática de "novo lead" para esse número. Apenas avisar ele por WhatsApp/push quando esse caso ocorrer (lead com telefone = número dele mesmo), sem disparar contato automático.

**Como aplicar:** em execuções futuras da automação de leads do Chaves na Mão, antes de mandar a mensagem inicial automática a um lead, comparar o telefone extraído com o número de Jonata (554796876631 / variações com e sem o 9 extra). Se coincidir, pular o envio automático ao lead e apenas notificar Jonata sobre a anomalia (provável erro de digitação no site).

Também notado: uma execução anterior dessa automação mandou um alerta para o número errado (5547920026017, conta da Ímpar, em vez do Jonata) — o destino correto de alertas para Jonata é sempre `554796876631`, não a variação com o 9 extra.
