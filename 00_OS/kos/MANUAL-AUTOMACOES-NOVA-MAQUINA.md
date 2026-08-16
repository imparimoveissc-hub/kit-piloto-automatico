# Manual de Automações — Instalação em Nova Máquina

**Atualizado:** 2026-07-26  
**Contexto:** Estado pós-otimização de tokens (sessão 2026-07-26)

---

## O que este manual cobre

Dois grupos de automações rodam em paralelo na máquina:

1. **MCP Scheduled Tasks** — gerenciadas pelo Claude Code via `mcp__scheduled-tasks`. Os prompts ficam em `~/.claude/scheduled-tasks/<taskId>/SKILL.md`. O backup-claude copia esses arquivos, mas as *registrações* no scheduler precisam ser recriadas manualmente com os comandos abaixo.

2. **LaunchAgents macOS** — processos Python gerenciados pelo `launchd`. Os `.plist` ficam em `~/Library/LaunchAgents/`. O backup-claude os copia, mas é preciso registrá-los no `launchd` na nova máquina.

---

## Parte 1 — MCP Scheduled Tasks

### Estado atual (2026-07-26)

| taskId | Cron | Janela | Status | Observação |
|--------|------|--------|--------|------------|
| `impar-gerente-digital` | `13 8-18 * * *` | 8h–18h horário | ✅ ativo | Otimizado em 2026-07-26 (era 24h) |
| `impar-messenger-inbox` | `*/15 * * * *` | 24h | ✅ ativo | Composio voltou 2026-08-16 |
| `impar-leads-chaves-na-mao` | `*/30 * * * *` | 24h | ✅ ativo | Composio voltou 2026-08-16 |
| `impar-reativador-marketplace` | `0 8-20/2 * * *` | 8h–20h | ✅ ativo | A cada 2h |
| `impar-relatorio-marketplace-manha` | `57 7 * * *` | 7:57 diário | ✅ ativo | |
| `impar-atende-leads-dia` | `32 8 * * *` | 8:32 diário | ✅ ativo | |
| `emissao-notas-fiscais` | `0 8 20,25,29,30 * *` | 8h nos dias 20/25/29/30 | ✅ ativo | |
| `vigia-reajustes-semanal` | `0 8 * * 1` | toda segunda 8h | ✅ ativo | |
| `impar-notificar-leads-planilha` | `*/5 * * * *` | — | ❌ desativada | substituída por LaunchAgent |
| `impar-manutencao-horaria` | `0 * * * *` | — | ❌ desativada | incorporada ao gerente-digital |

### Como recriar as tasks no scheduler

Após restaurar os arquivos `~/.claude/scheduled-tasks/` via backup-claude, abra uma sessão Claude Code e execute os comandos abaixo (um por um via MCP `mcp__scheduled-tasks__create_scheduled_task`):

```
taskId: impar-gerente-digital
cronExpression: 13 8-18 * * *
description: Saúde + métricas Impar — horário das 8h às 18h, envia só se acionável
enabled: true

taskId: impar-messenger-inbox
cronExpression: */5 * * * *
description: Lê inbox do Messenger Impar e processa leads - a cada 5 min
enabled: true   ← verificar se Composio está ativo antes de habilitar

taskId: impar-leads-chaves-na-mao
cronExpression: */30 * * * *
description: Leads Chaves na Mão - D0 via WhatsApp - a cada 30 min
enabled: true   ← verificar se Composio está ativo antes de habilitar

taskId: impar-reativador-marketplace
cronExpression: 0 8-20/2 * * *
description: Reativador de anúncios Marketplace — a cada 2h (8h-20h)
enabled: true

taskId: impar-relatorio-marketplace-manha
cronExpression: 57 7 * * *
description: Relatório diário de performance do Marketplace - 07:57
enabled: true

taskId: impar-atende-leads-dia
cronExpression: 32 8 * * *
description: Atendimento automático de leads - diário 08:32
enabled: true

taskId: emissao-notas-fiscais
cronExpression: 0 8 20,25,29,30 * *
description: Busca pagamentos recebidos no Asaas e emite NFS-e no Portal Nacional nos dias 20, 25, 29 e 30 do mês
enabled: true

taskId: vigia-reajustes-semanal
cronExpression: 0 8 * * 1
description: Verifica reajustes e vigências de contratos Impar que estão chegando e posta alertas no WhatsApp
enabled: true
```

As duas desativadas (`impar-notificar-leads-planilha`, `impar-manutencao-horaria`) **não precisam ser recriadas** — estão obsoletas.

---

## Parte 2 — LaunchAgents macOS

### Estado atual (2026-08-16)

**Grupo A — Kit original (2026-07-26)**

| Label | Script | Trigger | Função |
|-------|--------|---------|--------|
| `com.impar.leads-planilha-watcher` | `leads_watcher.py` | a cada 5 min (StartInterval: 300) | Detecta novo lead no CSV e alerta Jonata |
| `com.impar.marketplace-daily-publish` | `publish_daily_from_fila.py --due --publish --max 2` | a cada 30 min (StartInterval: 1800) | Publica até 2 imóveis/ciclo no Marketplace |
| `com.impar.marketplace-crosspost-manha` | `crosspost_groups_v2.py --cadence 180` | 11:30 diário | Expande fila nos 96 grupos (manhã) |
| `com.impar.marketplace-crosspost-tarde` | `crosspost_groups_v2.py --cadence 180` | 17:00 diário | Expande fila nos 96 grupos (tarde) |
| `com.impar.marketplace-crosspost-noite` | `crosspost_groups_v2.py --cadence 180` | 21:30 diário | Expande fila nos 96 grupos (noite) |
| `com.impar.marketplace-gerar-fila` | `generate_queue.py` | domingo 7h | Gera fila semanal de imóveis |

**Grupo B — Kit Corretor Digital v1 (adicionado 2026-08-16)**

| Label | Script | Trigger | Função |
|-------|--------|---------|--------|
| `com.impar.marketplace-manha` | `run_daemon.sh` (GRUPOS=19, UNTIL=12:00) | 08:30 diário | Publisher Marketplace — turno manhã, máx 3 imóveis |
| `com.impar.marketplace-tarde` | `run_daemon.sh` (GRUPOS=19, UNTIL=18:00) | 14:00 diário | Publisher Marketplace — turno tarde, máx 3 imóveis |
| `com.impar.marketplace-noite` | `run_daemon.sh` (GRUPOS=19, UNTIL=21:00) | 19:30 diário | Publisher Marketplace — turno noite |
| `com.impar.chaves-na-mao-checker` | `run.sh` (chaves-na-mao-lead-checker) | a cada 15 min (StartInterval: 900) | Verifica emails Chaves na Mão e notifica lead novo via WhatsApp |
| `com.impar.messenger-varredura-auto` | `varredura_inbox.py` | a cada 15 min (StartInterval: 900) | Varre inbox Messenger — só Marketplace (is_marketplace obrigatório) |
| `com.impar.wa-pending-sender` | `wa_pending_sender.py` | a cada 2 min (StartInterval: 120) | Envia 1ª mensagem WhatsApp para leads D0 do CSV |
| `com.impar.health-check-rotinas` | `health-check-rotinas.sh` | a cada 2h (StartInterval: 7200) | Health check geral: LaunchAgents + disco + WhatsApp Desktop |

Plists do Grupo B: `06_OUTPUTS/KIT-CORRETOR-DIGITAL-v1.zip` → pasta `plists/`. Instalar via `install.sh`.

### Como instalar os LaunchAgents na nova máquina

Os `.plist` são copiados pelo backup-claude para `~/Library/LaunchAgents/`. Após a cópia:

**1. Ajustar o caminho do Kit nos plist**

Os scripts referenciam o caminho local `/Users/user/Kit-Piloto-Automatico-V30/`. Se o usuário ou o caminho do Kit for diferente na nova máquina, edite cada `.plist`:

```bash
# Substituir o caminho antigo pelo novo (ajuste conforme necessário)
NOVO_PATH="/Users/NOVO_USUARIO/Kit-Piloto-Automatico-V30"
for plist in ~/Library/LaunchAgents/com.impar.*.plist; do
  sed -i '' "s|/Users/user/Kit-Piloto-Automatico-V30|$NOVO_PATH|g" "$plist"
done
```

**2. Registrar no launchd**

```bash
for plist in ~/Library/LaunchAgents/com.impar.*.plist; do
  launchctl load "$plist"
  echo "Carregado: $(basename $plist)"
done
```

**3. Verificar se estão rodando**

```bash
launchctl list | grep impar
```

Saída esperada: 6 entradas `com.impar.*` listadas (PID ou `-` se estiver em espera).

---

## Parte 3 — Arquivos de estado (checkpoints)

Estes arquivos rastreiam o que já foi processado. O backup-claude **não** os copia (ficam em `~/.local/`, fora do Kit). Na nova máquina eles são criados automaticamente na primeira execução — mas os primeiros ciclos podem reprocessar eventos antigos.

| Arquivo | Criado por | Função |
|---------|-----------|--------|
| `~/.local/impar-automation/marketplace/checkpoint.json` | publisher | Último anúncio publicado |
| `~/.local/impar-automation/marketplace/queue.json` | gerar-fila | Fila semanal de imóveis |
| `~/.local/impar-automation/chaves-na-mao/checkpoint.json` | leads task | Leads já notificados (24h) |
| `~/.local/impar-automation/leads-planilha/ultimo-estado.json` | leads_watcher.py | Última linha processada no CSV |
| `~/.local/impar-automation/messenger/checkpoint.json` | messenger task | Mensagens do Messenger já processadas |

Para criar as pastas na nova máquina antes da primeira execução:

```bash
mkdir -p ~/.local/impar-automation/{marketplace,chaves-na-mao,leads-planilha,messenger}
```

---

## Parte 4 — Dependências externas

| Dependência | Usado por | Como verificar |
|-------------|-----------|----------------|
| Composio MCP (Outlook) | `impar-messenger-inbox`, `impar-leads-chaves-na-mao` | `mcp__composio__*` disponível no Claude |
| WhatsApp Desktop nativo (macOS) | todas as tasks que alertam Jonata | App aberto + Accessibility permission |
| Playwright + cookies Facebook | LaunchAgents marketplace | `playwright install chromium` + cookies válidos |
| Python 3 em `/usr/local/bin/python3` | LaunchAgents marketplace | `which python3` |
| Python 3 em `/usr/bin/python3` | leads_watcher.py | pré-instalado no macOS |
| Asaas API | `emissao-notas-fiscais` | `.env` em `18_AUTOMATION_STACK/nfem-joinville/.env` |
| Portal NFS-e (Chrome ativo) | tasks de nota fiscal | Chrome com sessão logada |

---

## Parte 5 — Otimizações de token aplicadas (2026-07-26)

Registradas aqui para não regredir numa nova instalação:

| O que foi feito | Motivo |
|-----------------|--------|
| `impar-gerente-digital` restrito a 8h–18h | Madrugada não tem nada acionável — economiza 13 rodadas/dia |
| `impar-manutencao-horaria` desativada | Lógica incorporada ao gerente-digital; task duplicada |
| `impar-notificar-leads-planilha` desativada | Substituída por LaunchAgent (zero tokens quando não há lead novo) |
| KOS Brain + Policy carregado antes de qualquer arquivo | Reduz leituras de código desnecessárias em 10× |
| Header KOS injetado em todas as SKILL.md das tasks | Claude lê Brain antes de abrir qualquer arquivo do projeto |

---

## Checklist de verificação pós-instalação

- [ ] `launchctl list | grep impar` → 13 entradas (6 Grupo A + 7 Grupo B)
- [ ] MCP scheduled tasks: `list_scheduled_tasks` → 8 tasks ativas
- [ ] `impar-gerente-digital` com cron `13 8-18 * * *` (não `13 * * * *`)
- [ ] Pasta `~/.local/impar-automation/` criada com subpastas
- [ ] WhatsApp Desktop aberto e com sessão ativa
- [ ] `.env` em `18_AUTOMATION_STACK/nfem-joinville/.env` copiado
- [ ] Cookies do Facebook válidos para o Playwright
- [ ] Composio MCP: verificar status antes de habilitar as tasks de Leads/Messenger
