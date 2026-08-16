---
name: impar-followup-leads-email
description: Como rodar o follow-up de WhatsApp da Impar para leads que chegaram por e-mail sem conversa
metadata: 
  node_type: memory
  type: project
  originSessionId: 45c74ff0-2dd2-4dda-a7ed-93d3e9c4e9a8
---

Impar Imoveis: leads que chegam por e-mail (Chaves na Mao/site) e nao respondem no WhatsApp recebem uma cadencia de follow-up **operada pelo Claude** via WhatsApp MCP local.

- Mensagem com link do imovel = **D0, dispara UMA UNICA VEZ** (antes reenviava repetido). Spec: `05_WORKSPACE/clientes/impar-imoveis/whatsapp/mensagem-lead-chaves-na-mao.md`.
- Cadencia: **D1/D3/D5/D7/D14/D21/D30** contados a partir de `data_entrada` (dia do D0). Spec: `.../whatsapp/follow-up-lead-email.md`.
- Estado por lead na planilha `.../whatsapp/leads-followup.csv` (coluna `ultimo_passo_enviado` impede reenvio).
- Stop rules: lead respondeu → parar + handoff/avisos para o Jonata 47 99687-6631 (554796876631) — NAO para o numero da Impar; opt-out → parar. Excecao: numero pessoal do Jonata (554796876631) nunca recebe.

- Fonte de leads: e-mail no **Outlook** (Chaves na Mao). ATENCAO: o Mac roda macOS Monterey (screenshot do computer-use exige macOS 14 = indisponivel) e o Outlook esta no modo "Novo Outlook" (nao expoe nada via AppleScript nem SQLite). Por isso a fonte de verdade pratica hoje e o **historico do WhatsApp da Impar (5547920026017)**: as mensagens D0 ("Recebemos seu contato...") revelam quem ja recebeu.
- **Papo AI e o dono do atendimento** (chatbot "assistente virtual em fase de testes") — ele envia o D0 e responde os leads. E a fonte do bug de repeticao e da confusao cadeira=imovel. Jonata optou por MANTER o Papo AI por ora.
- Rotinas que EU criei (`impar-followup-manha` 8:30, `impar-atende-leads-dia` a cada 30min, `impar-followup-checagem-0845`) estao **DESLIGADAS** (enabled=false) desde 02/07 para nao duplicar mensagem com o Papo AI. So reativar se o Papo AI for pausado e eu assumir o atendimento.
- Jonata prefere disparo automatico (respondeu em 2026-07-02).

**Why:** o disparo e feito pelo Claude, entao preciso consultar/atualizar o CSV a cada rodada; a leitura do Outlook esta bloqueada nesta maquina.
**How to apply:** ao rodar follow-up, use o WhatsApp como fonte de verdade + o CSV de estado; envie o passo devido de cada em_followup e atualize a planilha.

## Objetivo do atendimento (definido 2026-07-02)
Ao interagir com os leads que respondem: **qualificar → coletar os DOCUMENTOS antes da visita → agendar visita com os interessantes** → handoff pro corretor nos quentes. Doc = para compra/financiamento (renda/IR/holerite) ou fianca locaticia (dados do locatario).

## NAO CONTATAR (nao sao leads de imovel)
- O WhatsApp da Impar tambem vende **moveis/eletro usados** via Facebook Marketplace: **cadeira, mesa, ar condicionado** etc. Jonata ja vendeu — NAO contatar como lead. Marcados `excluido_nao_lead` no CSV (ex: 554797518459, 554792707987, 554784648526 = anuncio de cadeira).
- **554784779151** = Studio Ana Homss (salao de beleza, autoresposta) — nao e lead.

## Disparador do D0 IDENTIFICADO (04/07) — tarefa agendada, nao o CSV
O disparador externo do D0 e a **tarefa agendada `leads-chaves-na-mao-whatsapp`** (`~/.claude/scheduled-tasks/leads-chaves-na-mao-whatsapp/SKILL.md`), que roda **a cada 10 min** lendo o Outlook e enviando a 1a mensagem. O alerta "🔔 NOVO LEAD SEM CONTATO" que o Jonata recebe e o passo 4b dela. **Ela NAO consulta o leads-followup.csv** — por isso opt-out/encerrado no CSV nao a impede.
- Bug de repeticao: a unica trava contra reenvio era `list_chats` (passo 3), que falha por variacao de formato do numero (com/sem 9 extra) → cada execucao trata o lead como novo e reenvia o D0 + realerta o Jonata a cada 10 min.
- **Correcao aplicada 04/07:** adicionei ao SKILL (1) LISTA DE BLOQUEIO fixa (Bruce 5547991833276/554791833276) + regra de tratar como bloqueado quem tiver opt_out=sim ou status opt_out/encerrado/excluido_nao_lead no CSV; (2) passo 3 robusto (checa contato anterior via get_last_interaction nas duas variacoes do numero); (3) **TRAVA DIARIA passo 3.5: no maximo 1 mensagem por lead por dia**, garantia final contra o loop de 10 min.
- Para bloquear um lead dessa automacao: adicionar a LISTA DE BLOQUEIO no SKILL.md da tarefa E marcar opt_out=sim/status=encerrado no CSV (os dois estao sincronizados agora).
