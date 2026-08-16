---
name: impar-followup-checagem-0845
description: Checa às 8:45 se a rotina de follow-up da Impar rodou às 8:30 e reporta o status.
---

Tarefa de VERIFICAÇÃO (somente leitura — NÃO envie nenhuma mensagem de WhatsApp). Opere em pt-BR.

Objetivo: confirmar se a rotina de follow-up da Impar Imóveis (`impar-followup-manha`, agendada para ~8:30) rodou hoje e reportar o status.

Passos:
1. Leia a planilha de estado: `/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/05_WORKSPACE/clientes/impar-imoveis/whatsapp/leads-followup.csv`.
2. Verifique se houve envios hoje: leads em_followup cuja coluna `data_ultimo_passo` = a data de hoje indicam que a rotina enviou. Se nenhum lead tem `data_ultimo_passo` = hoje, a rotina provavelmente NÃO rodou ou pausou.
3. Confirmação cruzada opcional (só leitura): use o MCP do WhatsApp (mcp__whatsapp__list_messages, sem enviar nada) para ver se saíram mensagens da Impar (5547920026017) hoje de manhã.
4. Escreva um resumo curto e claro para o Jonata:
   - Se rodou: "✅ A rotina de follow-up rodou às ~8:30. Enviados hoje: <nomes + passo>."
   - Se NÃO rodou/pausou: "⚠️ A rotina de follow-up das 8:30 NÃO enviou nada hoje — provavelmente pausou pedindo aprovação ou o app estava fechado. Me chame com 'roda o follow-up' que eu executo agora."
Não faça nenhum envio. Apenas leia e reporte.