---
module: Sistema
lastModified: 2026-07-26
status: ativo
---

## Objetivo

Monitorar saúde de todas as automações da Impar Imóveis e reportar ao Jonata apenas quando há algo acionável.
Task unificada: substitui `impar-gerente-digital` + `impar-manutencao-horaria` (mescladas em 2026-07-26).

---

## Task ativa

| Task ID | Frequência | Mecanismo |
|---------|-----------|-----------|
| `impar-gerente-digital` | horário (cron: 13 * * * *) | MCP scheduled-tasks |

**impar-manutencao-horaria** — desativada em 2026-07-26, lógica incorporada ao gerente-digital.

---

## O que a task verifica (por ordem)

**Parte 1 — Saúde do sistema:**
1. Logs da última hora em `07_LOGS/` (marketplace, chaves-na-mao, messenger-bridge)
2. Espaço em disco — alerta se logs > 500MB; compacta arquivos > 7 dias
3. Checkpoints em `~/.local/impar-automation/*/` atualizados nas últimas 2h
4. Classifica: ✅ OK | ⚠️ AVISO | 🚨 CRÍTICO

**Parte 2 — Métricas das automações:**
5. Marketplace: posts realizados, bloqueios
6. Grupos Facebook: rodadas manhã/tarde/noite OK
7. Leads Chaves na Mão: leads recebidos e processados
8. Messenger inbox: mensagens novas, leads com telefone

---

## Regra de envio WhatsApp

| Condição | Ação |
|----------|------|
| Status CRÍTICO | Enviar sempre para 554796876631 (Jonata) |
| Lead de alto valor sem resposta | Enviar |
| Bloqueio Facebook | Enviar |
| Automação parada há +2h | Enviar |
| Status OK ou AVISO menor | NÃO enviar — evitar spam |

---

## Logs produzidos

| Log | Localização | Retenção |
|-----|-------------|---------|
| Relatório completo horário | `07_LOGS/gerente-digital-YYYY-MM-DD-HH.log` | 7 dias |
| Status resumido (compatibilidade) | `07_LOGS/manutencao-horaria.log` | 30 dias |

---

## Checkpoints monitorados

```
~/.local/impar-automation/marketplace/     → publisher e crosspost
~/.local/impar-automation/chaves-na-mao/checkpoint.json
~/.local/impar-automation/leads-planilha/ultimo-estado.json
~/.local/impar-automation/messenger/checkpoint.json
```

---

## Como diagnosticar o sistema sem abrir código

1. **Estado atual rápido:** `tail -20 ~/Library/.../07_LOGS/manutencao-horaria.log`
2. **Último relatório completo:** `ls 07_LOGS/gerente-digital-*.log | tail -1 | xargs tail -30`
3. **Disco:** `df -h /` — acima de 90% é crítico.
4. **Todos os checkpoints:** `for f in ~/.local/impar-automation/*/checkpoint.json; do echo "$f:"; cat "$f" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('last_checked','?'))"; done`
5. **LaunchAgents ativos:** `launchctl list | grep impar`

---

## Problemas conhecidos

- Disco chegou a 96% em 2026-07-26 (resolvido: baixou para 84%).
- Composio MCP indisponível desde 2026-07-26 — afeta Chaves na Mão + Messenger.
- Gerente Digital não envia WhatsApp quando status é AVISO (correto — evitar spam).

## ⛔ Restrição ativa (ordem 2026-07-26)

WhatsApp Bridge/Messenger **totalmente desativado** por ordem escrita do usuário.
Único canal permitido: **WhatsApp Desktop nativo macOS** (app, PID dinâmico).

Componentes proibidos de reativar sem nova ordem escrita:
- `com.impar.messenger-bridge` e derivados (9 LaunchAgents)
- Claude tasks: messenger-desktop-automation, messenger-inbox-hora, messenger-inbox-varredura-auto, leads-chaves-na-mao-whatsapp
- `start-bridge.sh` e `install-launchd-macos.sh` (já proibidos desde 2026-07-26 no CLAUDE.md)
