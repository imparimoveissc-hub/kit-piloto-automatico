---
module: Automacoes-Mapa
lastModified: 2026-07-26
status: ativo
---

# Mapa Completo de Automações — Impar Imóveis

Inventário gerado em 2026-07-26 por varredura completa da máquina.
Inclui LaunchAgents, Claude Scheduled Tasks e scripts em 18_AUTOMATION_STACK.

---

## LaunchAgents — Rodando Agora (PID ativo)

| LaunchAgent | PID | Função |
|-------------|-----|--------|
| `com.impar.auto-permissions-monitor` | 721 | Monitora permissões macOS (Accessibility, Full Disk) |
| `com.impar.crm` | 724 | Automação CRM (Imobibrasil / Rogga) |
| `com.impar.marketplace` | 8372 | Publisher contínuo Facebook Marketplace |
| `com.impar.messenger-bridge` | 51328 | Bridge WhatsApp/Messenger 24/7 |

---

## LaunchAgents — Carregados (intervalados, aguardando trigger)

| LaunchAgent | Intervalo | Função |
|-------------|-----------|--------|
| `com.impar.bootup-restore` | boot | Restaura estado das automações após reinício |
| `com.impar.chaves-na-mao-3leads-checker` | intervalo | Verifica lote de 3 leads Chaves na Mão |
| `com.impar.chaves-na-mao-checker` | intervalo | Verifica leads novos Chaves na Mão (email) |
| `com.impar.claude-desktop-autostart` | boot | Autostart Claude Desktop |
| `com.impar.crosspost` | schedule | Crosspost imóveis nos 96 grupos Facebook |
| `com.impar.gerente-digital-whatsapp-startup` | startup | Notifica Jonata no WhatsApp quando sistema inicia |
| `com.impar.marketplace-restore-on-boot` | boot | Restaura fila Marketplace após reinício |
| `com.impar.messenger-bridge-health-check` | intervalo | Health check do bridge Messenger |
| `com.impar.messenger-desktop` | schedule | Automação Messenger via desktop |
| `com.impar.messenger-inbox` | schedule | Varredura inbox Messenger |
| `com.impar.messenger-varredura-auto` | schedule | Varredura automática Messenger (leads) |
| `com.impar.relatorio-marketplace-manha` | 11:30 | Relatório manhã Marketplace |
| `com.impar.relatorio-marketplace-tarde` | 17:00 | Relatório tarde Marketplace |
| `com.impar.reschedule-on-boot` | boot | Reagenda Claude tasks após reinício |
| `com.impar.rotate-task-ledger` | schedule | Rotaciona ledger de tasks (limpeza) |
| `com.impar.whatsapp-startup-notifier` | startup | Notificador WhatsApp na inicialização |

---

## LaunchAgents — Com Erro

| LaunchAgent | Exit | Causa provável |
|-------------|------|----------------|
| `com.impar.leads-planilha-watcher` | 256 | leads_watcher.py falhou na 1ª execução — verificar dependências Python |

**Para diagnosticar:** `cat ~/.local/impar-automation/leads-planilha/watcher.log`

---

## LaunchAgents — Desativados (.disabled)

| LaunchAgent | Motivo |
|-------------|--------|
| `com.impar.bootup-restore.disabled` | Duplicata da versão ativa |
| `com.impar.chaves-na-mao-3leads-checker.disabled` | Duplicata |
| `com.impar.chaves-na-mao-checker.disabled` | Duplicata |
| `com.impar.claude-desktop-autostart.disabled` | Duplicata |
| `com.impar.crosspost.disabled` | Duplicata |
| `com.impar.gerente-digital-whatsapp-startup.disabled` | Duplicata |
| `com.impar.marketplace-daily-publish.disabled` | Substituído pelo publisher contínuo |
| `com.impar.marketplace-restore-on-boot.disabled` | Duplicata |
| `com.impar.marketplace.disabled` | Duplicata |
| `com.impar.messenger-desktop.disabled` | Duplicata |
| `com.impar.messenger-inbox-5min.disabled` | Substituído por versão horária |
| `com.impar.messenger-varredura-auto.disabled` | Duplicata |
| `com.impar.notificar-leads-planilha.disabled` | Aguardando Full Disk Access |
| `com.impar.relatorio-marketplace-manha.disabled` | Duplicata |
| `com.impar.relatorio-marketplace-tarde.disabled` | Duplicata |
| `com.impar.reschedule-on-boot.disabled` | Duplicata |
| `com.impar.update-current-state.disabled` | Aguardando Full Disk Access (`/usr/bin/python3`) |
| `com.impar.whatsapp-responder.disabled` | Em desenvolvimento |
| `com.impar.whatsapp-startup-notifier.disabled` | Duplicata |

---

## Claude Scheduled Tasks (~/.claude/scheduled-tasks/)

### NFS-e (Emissão de Notas Fiscais)

| Task | Gatilho | Função |
|------|---------|--------|
| `emissao-nfs-dia-20` | dia 20 do mês | Emite NFS-e via Portal Nacional (Asaas) |
| `emissao-nfs-dia-25` | dia 25 do mês | Emite NFS-e via Portal Nacional (Asaas) |
| `emissao-nfs-dia-29` | dia 29 do mês | Emite NFS-e via Portal Nacional (Asaas) |
| `emissao-nfs-dia-30` | dia 30 do mês | Emite NFS-e via Portal Nacional (Asaas) |

### Leads

| Task | Gatilho | Função |
|------|---------|--------|
| `leads-chaves-na-mao-whatsapp` | `*/10 * * * *` | Processa emails Chaves na Mão → D0 WhatsApp (Composio MCP) |
| `impar-notificar-leads-planilha` | schedule | Notifica leads novos do CSV via WhatsApp |
| `enviar-d0-luciano-1900` | 19:00 | D0 para lead Luciano |
| `enviar-d0-paloma-1814` | 18:14 | D0 para lead Paloma |

### Marketplace

| Task | Gatilho | Função |
|------|---------|--------|
| `impar-marketplace-grupos-manha` | 11:30 | Crosspost turno manhã nos 96 grupos |
| `impar-marketplace-grupos-tarde` | 17:00 | Crosspost turno tarde nos 96 grupos |
| `impar-marketplace-grupos-noite` | 21:30 | Crosspost turno noite nos 96 grupos |
| `impar-marketplace-publicar-diario` | diário | Publicação diária de imóveis no Marketplace |
| `impar-marketplace-reativar-30min` | `*/30 * 8-21 * *` | Reativa anúncios pausados/rejeitados |
| `relatorio-marketplace-manha-impar` | manhã | Relatório de publicações da manhã |
| `relatorio-marketplace-tarde-impar` | tarde | Relatório de publicações da tarde |
| `impar-publicar-grupos-2026-07-18` | manual | Task de publicação pontual (histórico) |

### Messenger

| Task | Gatilho | Função |
|------|---------|--------|
| `impar-messenger-inbox-hora` | horário | Varredura inbox Messenger a cada hora |
| `impar-messenger-desktop-automation` | schedule | Automação Messenger via desktop |
| `impar-messenger-inbox-varredura-auto` | schedule | Varredura automática do inbox |

### Sistema / Saúde

| Task | Gatilho | Função |
|------|---------|--------|
| `gerente-digital-impar` | `13 * * * *` | Auditoria horária: saúde + métricas + alerta Jonata |
| `hourly-impar-maintenance` | horário | Manutenção horária (logs, disco, checkpoints) |
| `impar-update-current-state` | schedule | Atualiza estado atual do sistema |
| `status-tudo-certo-whatsapp` | schedule | Envia "tudo ok" ao Jonata (desativada — evitar spam) |
| `scheduled-tasks` | schedule | Meta-task de gestão de tasks |

---

## Scripts em 18_AUTOMATION_STACK/

| Pasta | Função | Estado |
|-------|--------|--------|
| `impar-facebook-marketplace-posting/` | Publisher, crosspost grupos (96), geração de fila, Playwright | ✅ Ativo |
| `impar-leads-planilha-watcher/` | Watcher CSV leads (zero tokens quando sem lead novo) | ⚠️ Erro exit=256 |
| `chaves-na-mao-lead-checker/` | Verificador leads Chaves na Mão (email Outlook via Composio) | ⚠️ Composio down |
| `nfem-joinville/` | Pipeline emissão NFS-e no Portal Nacional | ✅ Ativo |
| `impar-atualizacao-rogga-imobibrasil/` | Atualização imóveis Rogga → CRM Imobibrasil | ⏸ Pausado |
| `impar-atualizacao-grupo-jm-imobibrasil/` | Atualização grupo JM → Imobibrasil | ⏸ Pausado |
| `cinematic-video-editor/` | Editor de vídeo cinemático (uso pontual) | 🔧 Ferramenta |

---

## Alertas Ativos (2026-07-26)

| Problema | Impacto | Ação |
|----------|---------|------|
| **Composio MCP down** | Leads Chaves na Mão não processados | Aguardar restauração ou verificar conexão |
| **leads-planilha-watcher exit=256** | CSV watcher não funciona | `cat ~/.local/impar-automation/leads-planilha/watcher.log` |
| **Full Disk Access pendente** | `update-current-state` e `notificar-leads-planilha` desativados | System Settings → Privacy → Full Disk Access → adicionar `/usr/bin/python3` |
| **Duplicatas .disabled** | 19 plists duplicados em LaunchAgents | Limpeza futura (não urgente) |

---

## Como verificar tudo de uma vez

```bash
# LaunchAgents ativos
launchctl list | grep impar | grep -v "^-"

# Erro no leads watcher
cat ~/.local/impar-automation/leads-planilha/watcher.log | tail -20

# Claude tasks
ls ~/.claude/scheduled-tasks/

# Último relatório do gerente digital
ls ~/Library/Mobile\ Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/07_LOGS/gerente-digital-*.log 2>/dev/null | tail -1 | xargs tail -30
```
