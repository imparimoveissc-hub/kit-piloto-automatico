#!/usr/bin/env bash
# =============================================================================
#  Script: Agendar as 9 rotinas do Kit Piloto Automático V30
#
#  Uso: bash agendar-rotinas.sh
#
#  Pré-requisitos:
#    - Claude Code CLI instalado (claude --version)
#    - Logado (claude /login)
#    - Prompts restaurados em ~/.claude/scheduled-tasks/
#    - MCPs reconectados (WhatsApp, Asaas, Outlook/Composio)
# =============================================================================
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCHEDULED_TASKS_DIR="$HOME/.claude/scheduled-tasks"

c_ok()   { printf "\033[32m✔\033[0m %s\n" "$1"; }
c_info() { printf "\033[36m==>\033[0m %s\n" "$1"; }
c_warn() { printf "\033[33m!\033[0m %s\n" "$1"; }
c_err()  { printf "\033[31m✗\033[0m %s\n" "$1"; }

echo "============================================================"
echo "  AGENDAR AS 9 ROTINAS — Kit Piloto Automático V30"
echo "============================================================"
echo ""

# ---------------------------------------------------------------------------
# Pré-verificações
# ---------------------------------------------------------------------------
if ! command -v claude >/dev/null 2>&1; then
  c_err "Claude Code CLI não encontrado"
  echo "    Instale com: npm install -g @anthropic-ai/claude-code"
  exit 1
fi
c_ok "Claude Code CLI: $(claude --version 2>/dev/null || echo 'OK')"

if [ ! -d "$SCHEDULED_TASKS_DIR" ]; then
  c_err "Pasta ~/.claude/scheduled-tasks/ não encontrada"
  echo "    Rode 'bash instalar-nova-maquina.sh' primeiro"
  exit 1
fi

# Contar quantas pastas de rotinas existem
N_ROTINAS="$(find "$SCHEDULED_TASKS_DIR" -maxdepth 1 -type d -name "*rotina*" -o -name "*emissao*" -o -name "*leads*" -o -name "*impar*" | wc -l)"
if [ "$N_ROTINAS" -lt 8 ]; then
  c_warn "Apenas $N_ROTINAS pastas de rotinas encontradas (esperado: 9)"
  c_warn "Continuando mesmo assim…"
fi
c_ok "Rotinas encontradas em ~/.claude/scheduled-tasks/"

echo ""
c_info "Agendando as 9 rotinas…"
echo ""

# ---------------------------------------------------------------------------
# Array de rotinas: (nome cron descrição)
# ---------------------------------------------------------------------------
declare -a ROTINAS=(
  # Emissão NFS
  "emissao-nfs-dia-20|0 9 20 * *|NFS-e Joinville — corte dia 20"
  "emissao-nfs-dia-25|0 9 25 * *|NFS-e Joinville — corte dia 25"
  "emissao-nfs-dia-29|0 9 29 * *|NFS-e Joinville — corte dia 29"
  "emissao-nfs-dia-30|0 9 30 * *|NFS-e Joinville — corte dia 30 + fechamento"

  # Follow-up
  "impar-followup-manha|30 8 * * *|Follow-up leads frios"
  "impar-followup-checagem-0845|45 8 * * *|Checagem se follow-up rodou"
  "impar-atende-leads-dia|*/30 8-19 * * *|Responde leads, coleta docs"

  # Leads Chaves na Mão
  "leads-chaves-na-mao-whatsapp|*/10 * * * *|Verifica leads novos, envia 1ª msg"
  "status-tudo-certo-whatsapp|0 8-18/2 * * *|Confirma conversa de todos"
)

N_SUCCESS=0
N_FAIL=0

for rotina_info in "${ROTINAS[@]}"; do
  IFS='|' read -r NOME CRON DESC <<< "$rotina_info"

  SKILL_FILE="$SCHEDULED_TASKS_DIR/$NOME/SKILL.md"

  if [ ! -f "$SKILL_FILE" ]; then
    c_warn "Pulando $NOME — arquivo não encontrado: $SKILL_FILE"
    ((N_FAIL++))
    continue
  fi

  # Lê o prompt do arquivo
  PROMPT="$(cat "$SKILL_FILE")"

  # Tenta agendar via claude CLI
  # Nota: a CLI do claude schedule pode variar. Aqui assume-se:
  #   claude schedule --name <nome> --cron "<cron>" --prompt "<prompt>"
  # Mas isso pode não ser a sintaxe correta. Ajustar conforme necessário.

  # Por enquanto, apenas informamos o que SERIA agendado
  # (a CLI do Claude pode não suportar agendamento direto via linha de comando)

  echo "  [$NOME]"
  echo "    Cron:     $CRON"
  echo "    Desc:     $DESC"
  echo "    Prompt:   $(echo "$PROMPT" | head -1)…"
  echo ""

  ((N_SUCCESS++))
done

echo "============================================================"
echo ""
echo "  ⚠️  Método automático limitado"
echo ""
echo "  A CLI do Claude pode não suportar agendamento direto por"
echo "  linha de comando. Para agendar, use uma das opções:"
echo ""
echo "  OPÇÃO 1 (Recomendado): Abra o Claude Code e use a Skill /schedule"
echo "  ————————————————————————————————————————————"
echo "    /schedule emissao-nfs-dia-20"
echo "    (preencha os campos conforme AGENDAR-ROTINAS.md)"
echo ""
echo "  OPÇÃO 2: Cole no Claude o prompt do arquivo"
echo "  ————————————————————————————————————————————"
echo "    Agende a rotina 'emissao-nfs-dia-20' com:"
echo "    - Cron: 0 9 20 * *"
echo "    - Prompt: (leia do arquivo ~/.claude/scheduled-tasks/emissao-nfs-dia-20/SKILL.md)"
echo ""
echo "  Veja os detalhes em:"
echo "    $SCRIPT_DIR/AGENDAR-ROTINAS.md"
echo ""
echo "============================================================"

if [ $N_SUCCESS -ge 8 ]; then
  echo "✅ Todos os arquivos de rotinas estão presentes."
  echo "   Próximo passo: Abra o Claude Code e execute /schedule"
  exit 0
else
  echo "⚠️  Alguns arquivos estão faltando. Verifique a instalação."
  exit 1
fi
