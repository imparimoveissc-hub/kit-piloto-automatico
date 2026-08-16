#!/bin/bash
# Wrapper manual para rodar notificar_lead_whatsapp.py (uso interativo/debug).
# O launchd (com.impar.notificar-leads-planilha.plist) NAO usa este wrapper —
# ele chama python3 direto em ~/.local/impar-automation/notificar-leads-planilha/,
# porque launchd nao consegue abrir arquivos dentro do iCloud Drive (EPERM).
# Log: ~/.local/impar-automation/notificar-leads-planilha/logs/launchd-*.log

export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

SCRIPT_DIR="$HOME/.local/impar-automation/notificar-leads-planilha"
LOG_FILE="$SCRIPT_DIR/logs/manual-run.log"

{
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iniciando notificar_lead_whatsapp.py --from-planilha"
  cd "$SCRIPT_DIR" || exit 1
  python3 notificar_lead_whatsapp.py --from-planilha 2>&1
  EXIT_CODE=$?
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Concluído com exit code: $EXIT_CODE"
} >> "$LOG_FILE" 2>&1

exit $EXIT_CODE
