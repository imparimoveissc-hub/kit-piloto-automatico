# Procedimentos Técnicos — Automação Marketplace + Grupos Impar

**Atualizado:** 2026-07-21  
**Responsável:** Mecânico da Impar (Jonata)

🆕 **CORREÇÕES 2026-07-21:**
- ✅ Regex de extração de fotos CORRIGIDA: agora captura até 12 fotos/imóvel (antes capturava só 1)
- ✅ Limite de fotos aumentado: `baixar_fotos(max_fotos=10)` em `publish_daily_from_fila.py`
- ✅ Novo "Reativador" criado: `impar-marketplace-reativar-30min` (a cada 30 min, 08h-21h)
- ✅ Retry automático em falhas transientes (vencimentos não publicados)

🆕 **CORREÇÕES 2026-07-18:**
- ✅ Messenger Bridge reabilitado (porta 8791)
- ✅ FASE 3 em execução: 2588 imóveis + 768 posts
- ✅ WhatsApp automático: leads → WhatsApp Impar
- ✅ Tarefas agendadas confirmadas (11:30, 17:00, 21:30)

---

## 🔄 Fluxo Automático (NOVO 2026-07-21)

A automação agora roda **100% automática** com 3 camadas:

### Camada 1: Reativador (A CADA 30 MIN)
Tarefa: `impar-marketplace-reativar-30min` (08h-21h)  
O que faz: **Verifica se há postagens vencidas e tenta publicar com retry automático.**
- Se houver postagem com `data_hora_sugerida` ≤ agora: publica
- Se falhar (FB bloqueio, transiente): tenta novamente na próxima rodada (30 min depois)
- Máx 2 publicações/rodada (saúde da conta)
- **Você não precisa fazer nada.** Roda sozinho.

### Camada 2: Grupos (3 HORÁRIOS FIXOS)
| Horário | Período | O que faz |
|---------|---------|----------|
| **11:30** | Manhã (08:00-11:00) | Expande imóvel mais recente em 96 grupos |
| **17:00** | Tarde (13:30-16:30) | Expande imóvel mais recente em 96 grupos |
| **21:30** | Noite (18:30-21:00) | Expande imóvel mais recente em 96 grupos |

**Você não precisa fazer nada.** As tarefas rodão sozinhas todos os dias.

---

## 📊 Cadência de Postagens

### Marketplace (Diário)
- **Fins de semana:** 7-9 imóveis/dia
- **Dias úteis:** 8-10 imóveis/dia
- **Intervalo entre posts:** 7-20 minutos (aleatório = parece humano)
- **Distribuição:** 3 períodos (manhã, tarde, noite)

### Grupos (Automático 3x/dia)
- **Grupos por imóvel:** 96 grupos (lista completa em `grupos-aprovados.csv`)
- **Cadência:** 3 minutos entre grupos
- **Total/dia:** ~8 imóveis × 96 grupos = ~768 publicações

---

## 📂 Arquivos Principais

### Configuração
| Arquivo | O que é | Ação |
|---------|---------|------|
| `grupos-aprovados.csv` | Lista de 96 grupos | **Não editar** (atualizado em 17/07) |
| `.env` | Credenciais Marketplace | Manter em `.gitignore` |
| `fila-postagens.csv` | Fila diária do Marketplace | Auto-gerado |
| `fila-grupos-postagens.csv` | Fila de grupos (3x/dia) | Auto-gerado |

### Scripts
| Script | Função | Rodas quando |
|--------|--------|-------------|
| `generate_queue.py` | Coleta imóveis + monta fila | Manual (CLI) ou cron |
| `generate_group_queue.py` | Expande em grupos | 11:30, 17:00, 21:30 (automático) |
| `publish_marketplace_playwright.py` | Publica no browser | Manual (beta) |

---

## ❓ Se algo der errado

### Erro: "Nenhum imóvel encontrado em [data]"
**Causa:** Fila do Marketplace não foi gerada.  
**Solução:** Rodar `python3 generate_queue.py` manualmente.

### Erro: "Grupos com placeholders [A PREENCHER]"
**Causa:** `grupos-aprovados.csv` incompleto.  
**Solução:** Verificar se os 96 grupos estão preenchidos (linha 1-96).

### Nenhuma publicação apareceu nos grupos
**Verificar:**
1. Fila de grupos foi gerada? → Checar `fila-grupos-postagens.csv`
2. Horário da tarefa passou? → Aguardar próxima execução
3. Grupos estão corretos? → Validar em `grupos-aprovados.csv`

### Nenhuma publicação apareceu no Marketplace
**Verificar:**
1. Há anúncios com horário ≤ agora? → Checar coluna `data_hora_sugerida` do CSV
2. Reativador rodou? → Conferir log: `marketplace-publicados-log.csv` (linha mais recente tem timestamp de hoje?)
3. Bloqueio FB? → Log mostra "BLOQUEIO_TEMPORARIO"? → Aguardar desbloqueio (24-48h típico)
4. Erro transiente? → Task tenta novamente a cada 30 min (automático)

### Fotos não aparecem no anúncio publicado (ou só 1 foto)
**Verificar:**
1. Fila foi regenerada após 2026-07-21? → Se não: rodar `python3 generate_venda_queue.py`
2. CSV tem múltiplas fotos? → Checar campo "fotos" do CSV (deve ter URLs pipe-separated)
3. Arquivos foram baixados? → Conferir pasta `uploads-diario/<codigo_imovel>/` (deve ter 10 JPGs)
4. Se FB não exibe múltiplas fotos: pode ser limitação do tipo "item" (FB suporta 1 foto) — verificar em teste manual

---

## 🚀 Rodar Manualmente (Se Necessário)

### Gerar fila de Marketplace
```bash
cd 18_AUTOMATION_STACK/impar-facebook-marketplace-posting
python3 generate_queue.py
```

### Gerar fila de grupos (hoje)
```bash
python3 generate_group_queue.py
```

### Gerar fila de grupos (data específica)
```bash
python3 generate_group_queue.py 2026-07-18
```

---

## 📋 Checklist Diário (Opcional)

- [ ] Verificar se fila de Marketplace foi gerada (antes de 11:30)
- [ ] Confirmar se grupos-aprovados.csv está preenchido
- [ ] Validar publicações nos primeiros grupos (após 11:30)
- [ ] Monitorar se todas as 3 tarefas rodaram

**Nota:** Tudo é automático. Checklist é só para monitoramento.

---

## 🔑 Pontos-Chave (Evitar Erros)

1. **NÃO editar `grupos-aprovados.csv`** sem necessidade → pode quebrar a automação
2. **Manter `.env` seguro** → não fazer commit no Git
3. **Tarefas agendadas rodão diariamente** → sem ação manual necessária
4. **Cadência é humanizada** → intervalos aleatórios parecem reais (não bot)
5. **Se houver dúvida, não mexer** → chamar suporte antes de editar

---

## 📲 Notificação WhatsApp de Lead Capturado (Jonata → Impar)

**Ativa desde 2026-07-19.** Arquitetura em 2 etapas (gatilho = planilha):
1. A rotina do Messenger (`impar-messenger-inbox-hora`, a cada 5 min) captura o telefone do lead e **só grava** em `leads_marketplace_captura.csv` (com link do anúncio em Link/Item e resumo em Observações).
2. A task **`impar-notificar-leads-planilha`** (a cada 5 min) roda `notificar_lead_whatsapp.py --from-planilha`: lê a planilha, detecta **contatos novos** (controle em `logs/planilha-notificados.json`) e envia UMA mensagem **do WhatsApp do Jonata (app do Mac, já logado) para o celular da Impar (5547920026017)** com: nome, telefone normalizado, link do imóvel, resumo e um **link wa.me** que abre a conversa com o lead com a mensagem padrão pré-preenchida (quem estiver com o celular da Impar toca no link e envia manualmente).

Vantagem: qualquer processo que gravar um contato na planilha (não só o Messenger) dispara a notificação.

**Regras fixas:**
- NUNCA envia WhatsApp direto pro lead — só notificação interna Jonata→Impar.
- NUNCA toca na ponte/porta WhatsApp da Impar (whatsmeow `~/mcps/whatsapp-mcp` fica parada, sem parear).

**Como funciona o envio:** `open "whatsapp://send?phone=...&text=..."` + tecla Enter via osascript (System Events). **Pré-requisito:** o app que roda o Claude Code precisa de permissão em *Ajustes > Privacidade e Segurança > Acessibilidade* (sem ela, erro 1002 "não tem permissão para acionar teclas" e a mensagem vai pro outbox).

**Arquivos:**
- Script: `notificar_lead_whatsapp.py` (nesta pasta)
- Log: `logs/notificacoes-whatsapp.jsonl`
- Outbox (falhas p/ reenvio): `logs/notificacoes-whatsapp-outbox.jsonl`

**Comandos úteis:**
- Rodar o watcher manualmente: `./notificar_lead_whatsapp.py --from-planilha` (a task de 5 min já faz isso; inclui o flush do outbox)
- Simular sem enviar: `./notificar_lead_whatsapp.py --from-planilha --dry-run`
- Marcar contatos atuais como já processados (sem enviar): `./notificar_lead_whatsapp.py --seed-planilha`
- Envio avulso de 1 lead: `./notificar_lead_whatsapp.py --nome "X" --telefone "47..." --resumo "..." --link-imovel "..."` (com `--dry-run` para testar)
- Dedupe: contato novo = telefone+data ainda não processados (`logs/planilha-notificados.json`); e o mesmo telefone não é notificado 2x no mesmo dia.

**Falhas tratadas automaticamente (vão pro outbox e reenviam na próxima rodada, a cada 5 min):** tela bloqueada, permissão de Acessibilidade ausente, foco roubado por outro app.

**Automação permanente (launchd):** a task roda automaticamente a cada 5 minutos, mesmo após reinicialização do Mac, via:
- Plist: `~/.LaunchAgents/com.impar.notificar-leads-planilha.plist`
- Script: `18_AUTOMATION_STACK/impar-facebook-marketplace-posting/run-notificar-planilha.sh`
- Log: `~/Library/Logs/com.impar.notificar-leads-planilha.log`

**Comandos úteis (gerenciar launchd):**
- Ver status: `launchctl list | grep com.impar.notificar`
- Recarregar: `launchctl unload ~/.LaunchAgents/com.impar.notificar-leads-planilha.plist && launchctl load -w ~/.LaunchAgents/com.impar.notificar-leads-planilha.plist`
- Desabilitar (temporário): `launchctl unload ~/.LaunchAgents/com.impar.notificar-leads-planilha.plist`
- Logs: `tail -50f ~/Library/Logs/com.impar.notificar-leads-planilha.log`

---

## 📞 Contato para Dúvidas

- **Logs de erro:** `07_LOGS/`
- **Arquivos gerados:** `05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/`
- **Documentação completa:** Ver README.md na mesma pasta

---

**Tudo configurado. A automação funciona sozinha.** ✅
