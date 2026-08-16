# 🚀 Agendar as 9 Rotinas — Mac Novo

**Status:** Os prompts já foram restaurados em `~/.claude/scheduled-tasks/`  
**Próximo:** Agende os horários (cron) de cada uma

---

## ✅ Opção 1: Colar este prompt no Claude Code

Abra o Claude Code e digite:

```
/schedule emissao-nfs-dia-20
```

Quando perguntar os dados:
- **Nome:** `emissao-nfs-dia-20`
- **Descrição:** `Emissão automática de NFS-e Joinville — corte do dia 20`
- **Agenda (cron):** `0 9 20 * *`  (09:00 AM, dia 20 de cada mês)
- **Prompt:** Cole o conteúdo de: `~/.claude/scheduled-tasks/emissao-nfs-dia-20/SKILL.md`

**OU** deixe o Claude ler direto:

```
Agende a rotina "emissao-nfs-dia-20" com horário "0 9 20 * *" (09:00 AM no dia 20 de cada mês). 
O prompt está em ~/.claude/scheduled-tasks/emissao-nfs-dia-20/SKILL.md — leia e use.
```

Repita para cada uma das 9 rotinas abaixo.

---

## 📋 As 9 Rotinas (nome + cron + descrição)

### Emissão de Notas Fiscais (4 rotinas)

| Nome | Cron | Horário | Descrição |
|------|------|---------|-----------|
| `emissao-nfs-dia-20` | `0 9 20 * *` | 09:00 AM, dia 20 | NFS-e Joinville — corte dia 20 |
| `emissao-nfs-dia-25` | `0 9 25 * *` | 09:00 AM, dia 25 | NFS-e Joinville — corte dia 25 |
| `emissao-nfs-dia-29` | `0 9 29 * *` | 09:00 AM, dia 29 | NFS-e Joinville — corte dia 29 |
| `emissao-nfs-dia-30` | `0 9 30 * *` | 09:00 AM, dia 30 | NFS-e Joinville — corte dia 30 + fechamento |

### Atendimento / Follow-up (WhatsApp) (3 rotinas)

| Nome | Cron | Horário | Descrição |
|------|------|---------|-----------|
| `impar-followup-manha` | `30 8 * * *` | 08:30 AM, todos os dias | Follow-up leads frios via WhatsApp |
| `impar-followup-checagem-0845` | `45 8 * * *` | 08:45 AM, todos os dias | Checagem se follow-up 8:30 rodou |
| `impar-atende-leads-dia` | `*/30 8-19 * * *` | A cada 30 min, 08h-20h | Responde leads, coleta docs, agenda visita |

### Leads Chaves na Mão (Outlook + WhatsApp) (2 rotinas)

| Nome | Cron | Horário | Descrição |
|------|------|---------|-----------|
| `leads-chaves-na-mao-whatsapp` | `*/10 * * * *` | A cada 10 minutos | Verifica leads novos, envia 1ª msg, alerta Jonata |
| `status-tudo-certo-whatsapp` | `0 8-18/2 * * *` | A cada 2 horas (8h-18h) | Confirma que todos têm conversa iniciada |

---

## 🛠️ Opção 2: Script automático (Bash)

Se quiser agendar TUDO de uma vez por linha de comando, use:

```bash
#!/bin/bash
# Agendar as 9 rotinas

echo "Agendando as 9 rotinas…"

# Emissão NFS
claude schedule --name emissao-nfs-dia-20 --cron "0 9 20 * *" --prompt-file ~/.claude/scheduled-tasks/emissao-nfs-dia-20/SKILL.md
claude schedule --name emissao-nfs-dia-25 --cron "0 9 25 * *" --prompt-file ~/.claude/scheduled-tasks/emissao-nfs-dia-25/SKILL.md
claude schedule --name emissao-nfs-dia-29 --cron "0 9 29 * *" --prompt-file ~/.claude/scheduled-tasks/emissao-nfs-dia-29/SKILL.md
claude schedule --name emissao-nfs-dia-30 --cron "0 9 30 * *" --prompt-file ~/.claude/scheduled-tasks/emissao-nfs-dia-30/SKILL.md

# Follow-up
claude schedule --name impar-followup-manha --cron "30 8 * * *" --prompt-file ~/.claude/scheduled-tasks/impar-followup-manha/SKILL.md
claude schedule --name impar-followup-checagem-0845 --cron "45 8 * * *" --prompt-file ~/.claude/scheduled-tasks/impar-followup-checagem-0845/SKILL.md
claude schedule --name impar-atende-leads-dia --cron "*/30 8-19 * * *" --prompt-file ~/.claude/scheduled-tasks/impar-atende-leads-dia/SKILL.md

# Leads Chaves na Mão
claude schedule --name leads-chaves-na-mao-whatsapp --cron "*/10 * * * *" --prompt-file ~/.claude/scheduled-tasks/leads-chaves-na-mao-whatsapp/SKILL.md
claude schedule --name status-tudo-certo-whatsapp --cron "0 8-18/2 * * *" --prompt-file ~/.claude/scheduled-tasks/status-tudo-certo-whatsapp/SKILL.md

echo "✅ Todas as 9 rotinas agendadas!"
```

Salve como `agendar-rotinas.sh`, dê permissão e rode:

```bash
bash ~/Library/Mobile\ Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/19_BACKUP_CLAUDE/agendar-rotinas.sh
```

---

## ✅ Verificar se funcionou

Dentro do Claude Code:

```
claude schedule list
```

Deve mostrar as 9 rotinas com seus horários.

---

## 🚨 Pré-requisitos

Antes de agendar, certifique-se de que:

1. ✅ **Prompts restaurados:** `ls ~/.claude/scheduled-tasks/` deve listar as 9 pastas
2. ✅ **Logado:** `claude` dentro do CLI deve funcionar
3. ✅ **MCPs reconectados:** WhatsApp, Asaas, Outlook/Composio devem estar autorizados no app Claude
4. ✅ **Kit restaurado:** `/Users/usuario/Library/Mobile Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/` deve estar completo

---

## 📞 Se algo falhar

- **"comando não encontrado claude"** → faça `/login` no Claude Code
- **"arquivo SKILL.md não existe"** → rode `bash instalar-nova-maquina.sh` novamente
- **"permissão negada"** → use `chmod +x agendar-rotinas.sh`
- **"MCPs não conectados"** → abra o app Claude → Conectores → reconecte WhatsApp, Asaas, Outlook

---

**Gerado em:** 2026-07-10  
**Arquivo:** `19_BACKUP_CLAUDE/AGENDAR-ROTINAS.md`
