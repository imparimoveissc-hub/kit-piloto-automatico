# Current State — 2026-07-22 (Auto-Updated)

**Last Update:** 2026-07-22 21:00:34 UTC
**Status:** Auto-updated via update-current-state.py (ETAPA 3)

## Status por Automação

| # | Automação | Status | Última | Próxima | Alerta |
|---|-----------|--------|--------|---------|--------|
| 1 | Marketplace Publishing | ✅ | N/A | Próximo | Nenhum |
| 2 | Grupos Crosspost Tarde | ✅ | Auto | 2026-07-23 17:00 | Status OK |
| 3 | Grupos Crosspost Noite | ⏳ | Auto | Retry | Monitorado |
| 4 | NFS-e Lote | ✅ | 2026-07-20 | 2026-07-25 | Nenhum |
| 5 | Chaves na Mão Leads | ✅ | N/A | 10 min | Monitorado |
| 6 | Messenger Responses | ✅ | Auto | Contínuo | Ocasional |
| 7 | Notificar Leads Planilha | ✅ | Auto | Conforme | Status OK |
| 8 | Incluir Imóveis (CRM) | ⏸️ | N/A | N/A | Pausado ref AP0206 |

## Checkpoints (Preserve Always!)

**Marketplace:**
- last_success: Unknown
- imoveis_count: ?

**Leads:**
- last_dedup: Unknown
- 24h_window: ✅ Active

## Problemas Conhecidos (Top 5)

1. **Facebook UI Timeouts** - 15/19 grupos falharam (2026-07-22)
2. **WhatsApp Bridge Intermitente** - Desconexões esporádicas desde 2026-07-16
3. **MSA search_messages Error** - Outlook busca textual com erro
4. **Messenger Browser Pane** - 5 crashes em 24h
5. **Noite Grupos Still in_progress** - Task `...0817` não terminou

## Métricas (24h)

- **Tasks processadas:** 50
- **Taxa sucesso:** ~68%
- **Leads capturados:** 1 novo
- **Imóveis publicados:** 18 (stable)

## Próximas Ações

🔴 BLOCKER: Investigar Facebook UI timeouts
🟠 MÉDIA: Reabrir WhatsApp + reautenticar
🟡 BAIXA: Revisar Messenger crashes

---

**Nota:** Auto-gerado em ETAPA 3 via update-current-state.py
Atualizado: 2026-07-22 21:00:34
