---
module: Automacoes-Mapa
lastModified: 2026-08-10
status: ativo
---

# Mapa Completo de Automações — Impar Imóveis

Inventário atualizado em 2026-08-06 por varredura completa da máquina.

---

## LaunchAgents — Com PID ativo agora (processos rodando)

| LaunchAgent | PID | Função |
|-------------|-----|--------|
| `com.impar.auto-permissions-monitor` | 904 | Monitor de permissões |
| `com.impar.crm` | 906 | Servidor CRM local (http://localhost:8890) |
| `com.impar.messenger-api` | 21945 | Messenger API (:9876) |

---

## LaunchAgents — Monitoramento de Saúde

| LaunchAgent | Intervalo | Função | Estado |
|-------------|-----------|--------|--------|
| `com.impar.health-check-rotinas` | a cada 2h (24/7) | Varredura de todas as rotinas; auto-reparo (exceto WA); notifica Jonata 47996876631 | ✅ ATIVO 2026-08-08 |

Scripts: `~/.impar-n8n-core/scripts/health-check-rotinas.py` (lógica) + `health-check-rotinas.sh` (wrapper)  
Log: `~/.impar-n8n-core/logs/health-check-rotinas.log`  
**Regra**: conexão WhatsApp NUNCA é reparada automaticamente — apenas notificada.

---

## LaunchAgents — Agendados (sem PID = rodaram e saíram, normal)

| LaunchAgent | Horário | Função | Estado |
|-------------|---------|--------|--------|
| `com.impar.marketplace-daily-publish` | 9h–20h (a cada 1h) | Publica imóveis do marketplace | ✅ RESTAURADO 2026-08-19 — plist recriado e carregado (havia sumido) |
| `com.impar.marketplace-manha` | 08:30 → até 12:00, max 3 | Publisher manhã (`runner.py`) | ✅ ATIVO — publicou 3 imóveis às 09:15 em 2026-08-10. Log: `daemon-manha.out.log` |
| `com.impar.marketplace-noite` | 18:00 → até 21:00, max 4 | Publisher noite (`runner.py`) | ✅ ATIVO — publicou 1 imóvel às 16:47 em 2026-08-10. Log: `daemon-noite.out.log` |
| `com.impar.marketplace-tarde` | horário tarde | Publisher tarde | ✅ carregado |
| `com.impar.crosspost` | 11:00 e 17:00 | Crosspost grupos (`/Users/usuario/impar-marketplace-automacao/run_crosspost.sh`) | ✅ REATIVADO 2026-08-10 — rodou 17:01, 4 grupos novos, 2 imóveis, 3299 pares totais |
| `com.impar.messenger-varredura-auto` | automático | Varredura automática inbox | ✅ rodou hoje 08:58 |
| `com.impar.gerente-notificador` | a cada 5 min | Envia WhatsApp se N8N coloca pending | carregado |
| `com.impar.wa-pending-sender` | intervalo | Envia mensagens WA pendentes | carregado |
| `com.impar.bootup-restore` | boot | Restaura automações no boot | carregado |
| `com.impar.reschedule-on-boot` | boot | Reagenda tasks Claude no boot | carregado |

---

## LaunchAgents — Carregados mas INATIVOS / Com problema

| LaunchAgent | Situação |
|-------------|---------|
| `com.impar.leads-planilha-watcher` | ⚠️ Sem atividade desde 2026-07-26 |
| `com.impar.chaves-na-mao-checker` | ⚠️ Sem PID — substituído por `chaves-na-mao-leads-watcher` |
| `com.impar.chaves-na-mao-3leads-checker` | ⚠️ Sem PID — monitor_3leads.py roda via `chaves-na-mao-leads-watcher` |
| `com.impar.chaves-na-mao-email-bridge` | ⚠️ Sem PID — não utilizado atualmente |
| `com.impar.messenger-desktop` | Sem PID (AppleScript — erro `-1728`) |
| `com.impar.marketplace-restore-on-boot` | ❌ Falha: `~/.claude/scheduled-tasks/impar-marketplace-publicar-diario` não existe |

---

## LaunchAgents — DISABLED (plists com sufixo .disabled)

`com.impar.messenger-inbox-5min`, `com.impar.messenger-bridge`, `com.impar.messenger-bridge-health-check`,
`com.impar.messenger-inbox` (renomeado .disabled-n8n → ativo em 2026-08-06),
`com.impar.marketplace` (publisher contínuo), `com.impar.relatorio-marketplace-manha/tarde`,
`com.impar.notificar-leads-planilha`, `com.impar.rotate-task-ledger`, `com.impar.update-current-state`,
`com.impar.bootup-restore` (duplicata), `com.impar.reschedule-on-boot` (duplicata),
`com.impar.claude-desktop-autostart` (duplicata), `com.impar.marketplace-restore-on-boot` (duplicata),
`com.impar.crosspost` (duplicata)

---

## N8N / Docker — ✅ ATIVO (2026-08-08 07:45)

| Container | Porta | Estado |
|-----------|-------|--------|
| `impar-n8n` | 5678 | ✅ Up |
| `impar-financeiro-whatsapp-worker` | 8091 | ✅ Up (reiniciado 2026-08-08 — compose em `18_AUTOMATION_STACK/impar-financeiro-whatsapp/docker-compose.yml`) |

**⚠️ RISCO:** Docker Desktop não está configurado para iniciar no boot automaticamente.
Se a máquina reiniciar, rodar: `docker start impar-financeiro-whatsapp-worker impar-n8n`

---

## Claude Scheduled Tasks — Diretório local (~/.claude/scheduled-tasks/)

Pastas existentes (estado interno não verificável sem API):
`gerente-digital-impar`, `impar-atende-leads-dia`, `impar-followup-manha`, `impar-followup-checagem-0845`,
`impar-leads-chaves-na-mao` (a cada 30 min), `impar-messenger-inbox-hora`, `impar-messenger-inbox-varredura-auto`,
`impar-reativador-marketplace`, `vigia-reajustes-semanal` (segunda 09:23),
`emissao-nfs-dia-20/25/29/30`, `atualizar-apartamentos-na-planta`.

**Último log gerente-digital em 07_LOGS/: 2026-07-27** — verificar se task cloud ainda ativa.

---

## Checkpoints — Estado dos módulos (2026-08-06)

| Módulo | Status |
|--------|--------|
| chaves-na-mao | ⚠️ checkpoint sem dados (`?`) — verificar |
| marketplace | initialized |
| messenger | ✅ ativo (Facebook ca_Fdsklz-EJv2Z, page 111848200561084) |

---

## Scripts em 18_AUTOMATION_STACK/

| Pasta | Função | Estado |
|-------|--------|--------|
| `impar-facebook-marketplace-posting/` | Publisher, geração de fila, Playwright | ✅ Ativo |
| `impar-leads-planilha-watcher/` | Watcher CSV leads | ⚠️ Parado desde 2026-07-26 |
| `chaves-na-mao-lead-checker/` | Verificador leads Chaves na Mão (Outlook) | ⚠️ Sem confirmação |
| `nfem-joinville/` | Pipeline emissão NFS-e | ✅ Ativo |
| `impar-atualizacao-rogga-imobibrasil/` | Atualização imóveis Rogga → CRM | ⏸ Pausado |
| `impar-atualizacao-grupo-jm-imobibrasil/` | Atualização grupo JM → Imobibrasil | ⏸ Pausado |

---

## Alertas Ativos (2026-08-08)

| Problema | Impacto | Ação |
|----------|---------|------|
| **Docker sem autostart no boot** | N8N e finance-worker param se máquina reiniciar | Ativar "Start at Login" no Docker Desktop |
| **Messenger detecção pós-bloqueio FB** | check_unread.py não detecta leads após bloqueio temporário de 06:31 | Aguardar 2-6h para bloqueio expirar — varredura retoma automaticamente |
| **leads-planilha-watcher parado** | CSV watcher inativo desde 26/07 | Substituído por `chaves-na-mao-leads-watcher` (a cada 30 min) — ativo |
| ~~monitor_3leads CSV "Operation not permitted"~~ | ✅ RESOLVIDO 2026-08-10 | Path corrigido: Desktop → iCloud Kit (`05_WORKSPACE/.../leads-followup.csv`) |
| ~~Crosspost sem agendamento ativo~~ | ✅ RESOLVIDO 2026-08-10 | LaunchAgent instalado, roda 11:00 e 17:00 — confirmado às 17:01 |
| ~~marketplace-restore-on-boot falha~~ | ✅ RESOLVIDO — plist já está `.disabled`, não carregado | — |
| ~~Gerente Digital sem log recente~~ | ✅ INFO ERRADA — task rodou 2026-08-07 18:22 (cronExpression `13 8-18 * * *`) | — |
| ~~impar-financeiro-whatsapp-worker DOWN~~ | ✅ RESOLVIDO 2026-08-08 | `docker start` executado, Up |
| ~~Crosspost sem logs confirmados~~ | ✅ RESOLVIDO — crosspost.out.log confirmado, 16 grupos ontem 21:31 | — |
| ~~N8N offline~~ | ✅ RESOLVIDO 2026-08-06 | Docker iniciado, containers Up |
| ~~marketplace-daily-publish disabled~~ | ✅ RESOLVIDO 2026-08-06 | Reativado e rodando |
| ~~messenger-inbox disabled~~ | ✅ RESOLVIDO 2026-08-06 | Reativado |

---

## Como verificar tudo de uma vez

```bash
# LaunchAgents ativos
launchctl list | grep impar | grep -v "^-"

# Logs marketplace hoje
tail -5 ~/Library/Logs/impar-crosspost-noite.log
tail -5 ~/Library/Logs/impar-marketplace-daily-publish.log

# Checkpoints
for f in ~/.local/impar-automation/*/checkpoint.json; do echo "$f:"; cat "$f" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('last_checked','?'), d.get('status','?'))" 2>/dev/null; done

# N8N (quando instalado)
curl -s http://127.0.0.1:5678/healthz
```
