# 🎯 Passo-a-Passo: Agendar as 9 Rotinas no Mac Novo

## ✅ Checklist Pré-requisitos

Antes de começar, verifique:

```bash
# 1. Prompts restaurados?
ls ~/.claude/scheduled-tasks/
# Deve listar: emissao-nfs-dia-20, emissao-nfs-dia-25, ... (9 pastas)

# 2. Claude CLI instalado?
claude --version

# 3. Logado no Claude Code?
claude
# Se pedir login, digite: /login
```

Se tudo OK, continue. Se algo falhar, rode primeiro:
```bash
bash ~/Library/Mobile\ Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/19_BACKUP_CLAUDE/instalar-nova-maquina.sh
```

---

## 🚀 Método 1: Agendar uma por uma (RECOMENDADO)

### Passo 1: Abra o Claude Code

```bash
claude
```

### Passo 2: Para cada rotina, digite:

```
/schedule emissao-nfs-dia-20
```

### Passo 3: Preencha os campos

Quando o Claude perguntar:

| Campo | Valor | Exemplo |
|-------|-------|---------|
| **Nome da rotina** | Veja tabela abaixo | `emissao-nfs-dia-20` |
| **Descrição** | Descrição curta | `Emissão de NFS-e — corte dia 20` |
| **Cron/Horário** | Veja tabela abaixo | `0 9 20 * *` |
| **Prompt** | Leia do arquivo | Cole conteúdo de `~/.claude/scheduled-tasks/emissao-nfs-dia-20/SKILL.md` |

### Tabela: As 9 Rotinas

```
EMISSÃO DE NOTAS FISCAIS (09:00 AM em dias específicos):
─────────────────────────────────────────────────────────
Nome                    Cron          Descrição
─────────────────────────────────────────────────────────
emissao-nfs-dia-20     0 9 20 * *    NFS-e — corte dia 20
emissao-nfs-dia-25     0 9 25 * *    NFS-e — corte dia 25
emissao-nfs-dia-29     0 9 29 * *    NFS-e — corte dia 29
emissao-nfs-dia-30     0 9 30 * *    NFS-e — corte dia 30 + fechamento


FOLLOW-UP (WhatsApp):
─────────────────────────────────────────────────────────
Nome                        Cron              Descrição
─────────────────────────────────────────────────────────
impar-followup-manha        30 8 * * *        Follow-up 08:30 AM
impar-followup-checagem-0845 45 8 * * *       Checagem 08:45 AM
impar-atende-leads-dia      */30 8-19 * * *   A cada 30 min (8h-20h)


LEADS CHAVES NA MÃO (Outlook + WhatsApp):
─────────────────────────────────────────────────────────
Nome                            Cron              Descrição
─────────────────────────────────────────────────────────
leads-chaves-na-mao-whatsapp   */10 * * * *      A cada 10 minutos
status-tudo-certo-whatsapp     0 8-18/2 * * *    A cada 2 horas (8h-18h)
```

### Passo 4: Confirme cada uma

O Claude vai agendar e confirmar. Você verá:

```
✅ Rotina agendada: emissao-nfs-dia-20
   Próxima execução: 20 de julho de 2026 às 09:00
```

### Passo 5: Repita para as 9

Use o copiar-colar acima para as 9 rotinas.

**Tempo total:** ~15 minutos

---

## 🤖 Método 2: Automático (Experimento)

Se quiser tentar agendar TUDO de uma vez:

```bash
bash ~/Library/Mobile\ Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/19_BACKUP_CLAUDE/agendar-rotinas.sh
```

> ⚠️ Este método pode não funcionar completamente (depende de suporte CLI do Claude). Se falhar, use o **Método 1** acima.

---

## ✅ Verificar se funcionou

### No Claude Code:

```
/schedule list
```

Deve mostrar algo como:

```
Rotinas agendadas (9):
  ✓ emissao-nfs-dia-20       — 09:00 AM, dia 20
  ✓ emissao-nfs-dia-25       — 09:00 AM, dia 25
  ✓ emissao-nfs-dia-29       — 09:00 AM, dia 29
  ✓ emissao-nfs-dia-30       — 09:00 AM, dia 30
  ✓ impar-followup-manha     — 08:30 AM, todos os dias
  ✓ impar-followup-checagem-0845 — 08:45 AM, todos os dias
  ✓ impar-atende-leads-dia   — A cada 30 min (8h-20h)
  ✓ leads-chaves-na-mao-whatsapp — A cada 10 minutos
  ✓ status-tudo-certo-whatsapp — A cada 2 horas (8h-18h)
```

---

## 🚨 Troubleshooting

### "comando /schedule não reconhecido"
- Atualize o Claude Code: `npm install -g @anthropic-ai/claude-code@latest`
- Ou use `/anthropic-skills:schedule` em vez de `/schedule`

### "arquivo SKILL.md não encontrado"
```bash
# Restaure os prompts:
bash ~/Library/Mobile\ Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/19_BACKUP_CLAUDE/instalar-nova-maquina.sh
```

### "permissão negada"
```bash
chmod +x ~/Library/Mobile\ Documents/com~apple~CloudDocs/Kit-Piloto-Automatico-V30-DISTRIB/19_BACKUP_CLAUDE/*.sh
```

### "MCPs desconectados"
Abra o app Claude → Conectores → reconecte:
- ✅ WhatsApp
- ✅ Asaas
- ✅ Outlook/Composio

---

## 📚 Referências

| Arquivo | Função |
|---------|--------|
| `AGENDAR-ROTINAS.md` | Detalhes técnicos + sintaxe |
| `agendar-rotinas.sh` | Script automático (experimental) |
| `rotinas.yaml` | Manifesto de todas as 9 rotinas |
| `~/.claude/scheduled-tasks/` | Prompts restaurados |

---

## 🎉 Pronto!

Depois que agendar as 9 rotinas, elas rodarão automaticamente nos horários definidos. 

**Teste agora:**
```bash
claude
# Digite: "emissao nfs"
# Deve executar a rotina manualmente
```

---

**Última atualização:** 2026-07-10  
**Mac novo usuario:** $USER  
**Fuso:** America/Sao_Paulo
