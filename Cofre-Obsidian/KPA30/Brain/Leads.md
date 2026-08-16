---
module: Leads
lastModified: 2026-07-26
status: ativo (Composio MCP indisponível desde 2026-07-26)
---

## Objetivo

Detectar leads novos de imóveis (vindos do Chaves na Mão via email e de outras fontes via CSV)
e disparar automaticamente o contato D0 via WhatsApp Desktop nativo ao lead e notificação ao Jonata.

---

## Fontes de leads

| Fonte | Mecanismo de entrada | Canal |
|-------|---------------------|-------|
| Chaves na Mão | Email Outlook (jonata_oliveira@outlook.com.br) via Composio MCP | `chaves_na_mao` |
| Facebook / Marketplace | Adicionado manualmente ao CSV pelo operador | `facebook` / `marketplace` |
| Site | Adicionado manualmente ao CSV | `site` |

---

## Arquivos principais

| Arquivo | Propósito |
|---------|-----------|
| `05_WORKSPACE/clientes/impar-imoveis/whatsapp/leads-followup.csv` | CSV mestre de leads (49 linhas em 2026-07-26) |
| `~/.local/impar-automation/leads-planilha/leads_watcher.py` | Watcher Python (zero tokens sem lead novo) |
| `~/.local/impar-automation/chaves-na-mao/checkpoint.json` | Deduplicação 24h dos leads Chaves na Mão |
| `05_WORKSPACE/clientes/impar-imoveis/whatsapp/follow-up-lead-email.md` | Spec da cadência D1-D30 |

**Fonte do watcher no kit (para replicação):**
`18_AUTOMATION_STACK/impar-leads-planilha-watcher/leads_watcher.py`

---

## CSV de leads — colunas

```
telefone | nome | link_imovel | ref_imovel | descricao_imovel | canal_entrada
data_entrada | ultimo_passo_enviado | data_ultimo_passo | proximo_passo
data_proximo_passo | respondeu_whatsapp | opt_out | status | observacao
```

- `opt_out = sim` → não contatar nunca mais
- `status = encerrado` → lead finalizado
- `ultimo_passo_enviado` = D0, D1, D3, D7, D14, D21, D30

---

## Tarefas agendadas

| Task ID | Frequência | Mecanismo | Status |
|---------|-----------|-----------|--------|
| `leads-chaves-na-mao-whatsapp` | a cada 30 min | CronCreate durable (scheduled_tasks.json) | ativo (falha sem Composio) |
| `impar-leads-chaves-na-mao` | a cada 30 min | MCP scheduled-tasks | desativado (redundante) |
| `com.impar.leads-planilha-watcher` | a cada 5 min | LaunchAgent Python | ativo — zero tokens se sem lead |
| `impar-atende-leads-dia` | diário 8:32 | MCP scheduled-tasks | ativo |
| `impar-followup-manha` | diário 8:30 | MCP (ad-hoc/orphan) | a validar |

---

## Estado e logs

| Item | Localização |
|------|-------------|
| Estado CSV watcher | `~/.local/impar-automation/leads-planilha/ultimo-estado.json` |
| Checkpoint Chaves na Mão | `~/.local/impar-automation/chaves-na-mao/checkpoint.json` |
| Log leads Chaves na Mão | `07_LOGS/chaves-na-mao.log` |
| Log notificações CSV | `07_LOGS/notificar-leads-planilha.log` |
| Log watcher Python | `~/.local/impar-automation/leads-planilha/watcher.log` |

---

## Fluxo Chaves na Mão

```
Email recebido (nospam@chavesnamao.com.br) → Outlook Jonata
    ↓
Composio MCP consulta Outlook (a cada 30 min)
    ↓
Parser extrai: nome, telefone, ref, descrição, link
    ↓
Verifica blocklist (leads-followup.csv, col opt_out)
    ↓
Verifica deduplicação 24h (checkpoint.json)
    ↓
Envia D0 ao lead via WhatsApp Desktop + notifica Jonata
    ↓
Atualiza checkpoint.json
```

---

## Fluxo CSV Watcher (zero tokens)

```
LaunchAgent dispara a cada 5 min
    ↓
leads_watcher.py lê CSV e compara com ultimo-estado.json
    ↓
Sem novidade → sai em <50ms, 0 tokens
    ↓
Com lead novo → chama claude -p "Envie WhatsApp..." (1 sessão pequena)
    ↓
Salva novo estado
```

---

## Como diagnosticar sem abrir código

1. **Nenhum lead processado?** Checar `07_LOGS/chaves-na-mao.log` — buscar "ERRO Composio".
2. **Composio down?** Verificar status no checkpoint: `cat ~/.local/impar-automation/chaves-na-mao/checkpoint.json`.
3. **CSV watcher não disparando?** `launchctl list | grep leads-planilha` — deve mostrar o job.
4. **Lead novo não notificado?** Checar `ultimo-estado.json` (ultima_linha) vs `wc -l leads-followup.csv`.
5. **Follow-up atrasado?** Ver CSV coluna `data_proximo_passo` + `ultimo_passo_enviado`.

---

## Problemas conhecidos

- **Composio MCP indisponível** desde 2026-07-26 03:31Z — bloqueia processamento de emails Chaves na Mão.
- 14 leads acumulados em `impar-atende-leads-dia` aguardando autorização no CLAUDE.md.
- `impar-leads-chaves-na-mao` é redundante com `leads-chaves-na-mao-whatsapp` — ambos fazem D0, ambos dependem de Composio.
