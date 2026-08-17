---
module: Marketplace
lastModified: 2026-08-16
status: ativo
---

## Objetivo

Publicar imóveis da Impar Imóveis no Facebook Marketplace e em 96 grupos aprovados.
Pipeline 100% automático: geração de fila → publicação diária → crosspost em grupos (3 turnos).

---

## Geração de conteúdo (tags, título, descrição)

| Arquivo | Papel |
|---------|-------|
| `~/impar-marketplace-automacao/claude_enhance.py` | Gera título + descrição + 20 tags via Claude API (requer ANTHROPIC_API_KEY) |
| `~/impar-marketplace-automacao/tag_generator.py` | Fallback local — gera 20 tags por regras sem API |
| `~/impar-marketplace-automacao/enrich_fila.py` | Enriquece fila.json existente; roda após `build_fila.py` |
| `~/impar-marketplace-automacao/.env` | Config: ANTHROPIC_API_KEY, CLAUDE_ENHANCE_MODEL, CLAUDE_ENHANCE_ENABLED |

**Fluxo de geração:**
```
build_fila.py (coleta site) → claude_enhance.py (Claude API) → fila.json com tags+título+desc
                                      ↓ se sem API key
                              tag_generator.py (local, fallback)
```

**Para ativar Claude API:**
Editar `~/impar-marketplace-automacao/.env` e descomentar `ANTHROPIC_API_KEY=sk-ant-...`

**Para re-enriquecer a fila existente sem rebuild:**
```bash
cd ~/impar-marketplace-automacao && python3 enrich_fila.py
```

---

## Arquivos principais

| Arquivo | Propósito |
|---------|-----------|
| `18_AUTOMATION_STACK/impar-facebook-marketplace-posting/publish_groups_playwright.py` | Crosspost nos 96 grupos (Playwright) |
| `18_AUTOMATION_STACK/impar-facebook-marketplace-posting/MECANICO-IMPAR-PROCEDIMENTOS.md` | Procedimentos técnicos, erros comuns, contatos |
| `18_AUTOMATION_STACK/impar-facebook-marketplace-posting/deploy/` | Scripts de deploy e configuração |
| `05_WORKSPACE/clientes/impar-imoveis/automacoes/facebook-marketplace/grupos-aprovados.csv` | 96 grupos aprovados (não editar sem validar) |
| `~/.local/impar-automation/marketplace/queue.json` | Fila de publicações (estado ativo) |

---

## Tarefas agendadas

| Task ID | Frequência | Mecanismo | O que faz |
|---------|-----------|-----------|-----------|
| `impar-marketplace-grupos-manha` | 11:30 diário | LaunchAgent (plist) | Crosspost turno manhã nos 96 grupos |
| `impar-marketplace-grupos-tarde` | 17:00 diário | LaunchAgent (plist) | Crosspost turno tarde nos 96 grupos |
| `impar-marketplace-grupos-noite` | 21:30 diário | LaunchAgent (plist) | Crosspost turno noite nos 96 grupos |
| `impar-marketplace-manha` | 08:30 diário | LaunchAgent (plist) | Publisher turno manhã — até 3 imóveis, encerra às 12:00 |
| `impar-marketplace-tarde` | 13:00 diário | LaunchAgent (plist) | Publisher turno tarde — até 3 imóveis, encerra às 17:30 |
| `impar-marketplace-noite` | 18:00 diário | LaunchAgent (plist) | Publisher turno noite — até 4 imóveis, encerra às 21:00 |
| `impar-reativador-marketplace` | a cada 2h (8h-20h) | MCP scheduled-tasks | Verifica anúncios pausados/rejeitados e republica |
| `com.impar.marketplace-leads-captador` | a cada 5 min | LaunchAgent (plist) | Detecta novas conversas no Marketplace → CSV + notifica grupo "Novos Leads" no WhatsApp |

---

## LaunchAgents (~/Library/LaunchAgents/)

```
com.impar.marketplace-manha.plist             → 08:30 (max 3 imóveis, until 12:00)
com.impar.marketplace-tarde.plist             → 13:00 (max 3 imóveis, until 17:30)
com.impar.marketplace-noite.plist             → 18:00 (max 4 imóveis, until 21:00)
com.impar.marketplace-crosspost-manha.plist   → 11:30
com.impar.marketplace-crosspost-tarde.plist   → 17:00
com.impar.marketplace-crosspost-noite.plist   → 21:30
com.impar.marketplace-gerar-fila.plist        → geração semanal da fila
com.impar.marketplace.plist.disabled-turnos   → antigo daemon contínuo (desativado)
com.impar.marketplace-leads-captador.plist    → a cada 5 min — captador de leads Marketplace → CSV + WA grupo
```

---

## Estado e logs

| Item | Localização |
|------|-------------|
| Fila ativa | `~/.local/impar-automation/marketplace/queue.json` |
| Log reativador | `07_LOGS/marketplace-reativador.log` |
| Log crosspost | `18_AUTOMATION_STACK/impar-facebook-marketplace-posting/logs/` |
| Checkpoint publicações | `~/.local/impar-automation/marketplace/` |

---

## Fluxo de execução

```
Fila gerada (semanal)
    ↓
Publisher (a cada 30 min) → publica imóvel da fila no Marketplace
    ↓
Crosspost (11:30 / 17:00 / 21:30) → expande imóvel mais recente nos 96 grupos
    ↓
Reativador (a cada 2h) → identifica pausados/rejeitados e republica
```

---

## Como diagnosticar sem abrir código

1. **Publicações pararam?** Checar `07_LOGS/marketplace-reativador.log` — última linha.
2. **Grupos falhando?** Checar `18_AUTOMATION_STACK/.../logs/` — buscar "ERRO" ou "blocked".
3. **Fila vazia?** Checar `~/.local/impar-automation/marketplace/queue.json` — campo `items`.
4. **Playwright quebrado?** Reinstalar: ver seção "Playwright" em MECANICO-IMPAR-PROCEDIMENTOS.md.
5. **Login Facebook expirado?** Executar login manual: ver "Login" em MECANICO-IMPAR-PROCEDIMENTOS.md.

---

## Problemas conhecidos

- Login do Facebook expira periodicamente → executar `login-facebook.log` manualmente.
- Playwright pode quebrar após update do macOS → reinstalar via brew.
- Checkpoint pode ficar desatualizado (bug benigno) → verificar log CSV para confirmar publicações.
- Facebook pode bloquear temporariamente → aguardar 1-2h e reativar.
- 96 grupos: não editar `grupos-aprovados.csv` sem validar que o grupo ainda existe.

---

## ⚠️ Diagnóstico 2026-08-09 — Publisher duplicado

**Sintoma:** 17+ imóveis postados num único dia (limite esperado: 10).

**Causa:** Dois publishers rodando em paralelo com bancos de dados separados:

| Sistema | Plist | Banco | Aparece no relatório? |
|---------|-------|-------|-----------------------|
| `runner.py` | `marketplace-manha/tarde/noite` | `~/.impar-marketplace/` SQLite | ✅ Sim |
| `publish_daily_from_fila.py` | `marketplace-daily-publish` | `fila-postagens.csv` + `marketplace-publicados-log.csv` | ❌ Não |

Os dois sistemas não se comunicam → posts do `daily-publish` não contam no `DAILY_LIMIT` do runner e não aparecem no relatório das 09:00.

**Resolução:** `com.impar.marketplace-daily-publish.plist` desativado (→ `.disabled3`). O scheduled task cloud `impar-marketplace-publicar-diario` já estava `.DISABLED`.

**Regra:** manter ativo SOMENTE `marketplace-manha/tarde/noite`. Se `com.impar.marketplace-daily-publish.plist` reaparecer sem `.disabled`, desativar imediatamente.

**Relatório** (`relatorio-marketplace-manha-impar`) lê exclusivamente `~/.impar-marketplace/runner.log` — nunca `fila-postagens.csv`.
